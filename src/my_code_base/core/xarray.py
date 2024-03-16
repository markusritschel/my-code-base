# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import warnings
import numpy as np
import xarray as xr

log = logging.getLogger(__name__)



@xr.register_dataset_accessor("history")
class HistoryAccessor:
    def __init__(self, xr_obj):
        self._obj = xr_obj
        self._ensure_history()

    def _ensure_history(self):
        if 'history' not in self._obj.attrs.keys():
            self._obj.attrs['history'] = ""

    def add(self, msg):
        """Add an entry to the history."""
        self._obj.attrs['history'] += msg
        log.debug("Wrote '%s' to history", msg)
        return


def compress_xarray(data: xr.Dataset | xr.DataArray, complevel: int) -> xr.Dataset | xr.DataArray:
    """Compress :class:`xr.Dataset` or :class:`xr.DataArray`.
    
    Parameters
    ----------
    data : xr.Dataset | xr.DataArray
        Data to compress.
    complevel : int
        Compression level.
    
    Returns
    -------
    xr.Dataset | xr.DataArray
        Compressed data.
    """
    compression_dict = dict(zlib=True, complevel=complevel)
    if isinstance(data, xr.Dataset):
        for variable in data:
            data[variable].encoding.update(compression_dict)
    elif isinstance(data, xr.DataArray):
        data.encoding.update(compression_dict)
    return data


def get_dim_index(da: xr.DataArray, dim: str) -> int:
    """Get the index of a dimension in a DataArray.

    Parameters
    ----------
    da : xr.DataArray
        DataArray to get the dimension index from.
    dim : str
        Dimension name.

    Returns
    -------
    Index of the dimension in the DataArray. Can be used for specifying the axis in a numpy operation.
    
    Examples
    --------
    >>> da = xr.DataArray(np.random.rand(2, 3, 4), dims=['time', 'lat', 'lon'])
    >>> get_dim_index(da, 'lat')
    1
    """
    warnings.warn(
        "Will be removed in a future version."
        "Use xr.DataArray.get_dim_index(dim) instead.",
        DeprecationWarning,
        stacklevel=2
    )
    assert isinstance(da, xr.DataArray), "First argument must be of type xr.DataArray."
    return da.dims.index(dim)
