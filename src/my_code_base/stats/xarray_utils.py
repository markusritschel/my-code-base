# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-19
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import xarray as xr
from multipledispatch import dispatch
from .timeseries import weighted_annual_mean


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

    Methods
    -------
    weighted_mean(dim)
        Calculate the weighted mean based on the given dimension.
    """

    def __init__(self, obj):
        self._obj = obj

    @dispatch(str)
    def weighted_mean(self, dim):
        """
        Calculate the weighted annual mean (taking days of months into account).

        Parameters
        ----------
        dim : str
            The dimension along which to calculate the weighted mean.

        Returns
        -------
        weighted_mean : xarray.Dataset or xarray.DataArray
            The weighted annual mean.

        """
        log.debug(f"Identified single dimension {dim}. Building weighted annual mean.")
        return weighted_annual_mean(self._obj)

