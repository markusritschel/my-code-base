# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-26
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from abc import ABC, abstractmethod
from functools import wraps
import logging
import pandas as pd
import xarray as xr


log = logging.getLogger(__name__)


class _ColumnGroupBy:
    """Proxy around a transposed DataFrameGroupBy that transposes results back,
    so column-wise groupby semantics are preserved without ``axis=1``."""

    def __init__(self, groupby):
        self._groupby = groupby

    def __len__(self):
        return len(self._groupby)

    def __iter__(self):
        for key, group in self._groupby:
            yield key, group.T

    def __getattr__(self, name):
        attr = getattr(self._groupby, name)
        if not callable(attr):
            return attr

        @wraps(attr)
        def wrapper(*args, **kwargs):
            result = attr(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                return result.T
            return result
        return wrapper


class EnsembleAccessor(ABC):
    def __init__(self, data_obj) -> None:
        super().__init__()
        self._obj = data_obj

    @property
    def key_template(self):
        """Return the key template"""
        template = self._obj.attrs.get('_ens_key_template')
        if not template:
            raise KeyError("key_template not set. Make sure the attributes of the "
                           "'member' coordinate comprise a 'key_template' value. "
                           "You can set this via ds.ens.key_template = 'your.template'.")
        return template

    @key_template.setter
    def key_template(self, template_string):
        if '.' not in template_string: 
            raise ValueError("Elements must be divided by a dot (.).")
        if 'member' in template_string.split('.'):
            raise ValueError("key_template must not contain 'member'! "
                             "Please choose a different identifier.")
        self._obj.attrs['_ens_key_template'] = template_string

    @property
    def member_keys(self):
        return self._obj.attrs.get('_ens_member_keys')

    @member_keys.setter
    def member_keys(self, value):
        self._obj.attrs['_ens_member_keys'] = value

    @abstractmethod
    def _init_member_keys(self, member_values):
        self._verify_member_keys(member_values)
        member_table = _build_member_mapping_table(member_values, self.key_template.split('.'))
        self.member_keys = member_table

    def _verify_member_keys(self, member_values):
        def _consistent_key_pattern():
            number_of_keys = [len(x.split('.')) for x in member_values]
            return len(set(number_of_keys)) == 1
        if not _consistent_key_pattern():
            raise ValueError("Column keys must show the same pattern. "
                             "Not all column names have the same number of keys.")
        
        if len(set(member_values)) != len(member_values):
            log.warning("Member IDs are not all different!")


    def groupby(self, key):
        """Group the object by a member key. Member keys are initialized beforehand."""
        self._init_member_keys()
        return self._obj.groupby(self.member_keys[key])


def _build_member_mapping_table(member_values, member_id_elements):
    """Create a mapping table for member keys. Each member name follows the same format, 
    e.g. `source_id.member_id.grid_label`. The mapping represents a table with each key of
    `(source_id, member_id, grid_label)` as a column.

    The `member_values` could be an array of member values as follows:
    array(['ACCESS-CM2.r1i1p1f1.gn', 'ACCESS-CM2.r2i1p1f1.gn',
       'ACCESS-CM2.r3i1p1f1.gn', ...])

    And `member_id_elements` would be a list like ['source_id','member_id','grid_label'].
    """
    member_table = pd.Series(member_values).str.split('.', expand=True)
    member_table.index = member_values
    member_table.index.name = "member"
    member_table.columns = member_id_elements
    return member_table


@pd.api.extensions.register_dataframe_accessor("ens")
class PandasEnsembleAccessor(EnsembleAccessor):
    def _init_member_keys(self, **kwargs):
        super()._init_member_keys(self._obj.columns)

    def groupby(self, key):
        self._init_member_keys()
        return _ColumnGroupBy(self._obj.T.groupby(self.member_keys[key]))


@xr.register_dataset_accessor("ens")
class XarrayEnsembleAccessor(EnsembleAccessor):
    """An :class:`xarray.Dataset` accessor supporting the grouping of ensemble members by 
    model id and similar. The `member` coordinate in the :class:`xr.Dataset` must have a 
    `key_template` attribute of the form 'source_id.member_id.grid_label', following the 
    structure of the entries of the 'member' coordinate.
    """
    def _init_member_keys(self, **kwargs):
        if not 'member' in self._obj.coords:
            raise AttributeError("No coordinate 'member' found in xarray object.")
        super()._init_member_keys(self._obj.member.values)
        self.member_keys = self.member_keys.to_xarray()
