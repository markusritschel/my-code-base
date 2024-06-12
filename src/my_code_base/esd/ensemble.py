# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-26
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from abc import ABC, abstractmethod
import logging


log = logging.getLogger(__name__)


class EnsembleAccessor(ABC):
    def __init__(self, data_obj) -> None:
        super().__init__()
        self._obj = data_obj
        self._key_template = None
        self.member_keys = None

    @property
    def key_template(self):
        """Return the key template"""
        if not self._key_template:
            raise KeyError("key_template not set. Make sure the attributes of the "
                           "'member' coordinate comprise a 'key_template' value. "
                           "You can set this via ds.ens.key_template = 'your.template'.")
        return self._key_template

    @key_template.setter
    def key_template(self, template_string):
        if '.' not in template_string: 
            raise ValueError("Elements must be divided by a dot (.).")
        if 'member' in template_string.split('.'):
            raise ValueError("key_template must not contain 'member'! "
                             "Please choose a different identifier.")
        self._key_template = template_string

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

