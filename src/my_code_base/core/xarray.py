# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
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


