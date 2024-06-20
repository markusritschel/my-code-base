# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-19
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import xarray as xr


log = logging.getLogger(__name__)


@xr.register_dataset_accessor("stats")
@xr.register_dataarray_accessor("stats")
class StatsAccessor:
    """
    This class provides statistical operations on xarray data.

    Parameters
    ----------
    obj : xarray.Dataset or xarray.DataArray
        The xarray object on which statistical operations will be performed.

    """

    def __init__(self, obj):
        self._obj = obj

