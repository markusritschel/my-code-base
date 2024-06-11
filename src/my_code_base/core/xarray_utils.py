# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
import xarray as xr

log = logging.getLogger(__name__)


@xr.register_dataset_accessor("history")
class HistoryAccessor:
    def __init__(self, xr_obj):
        """
        A class for accessing and manipulating the 'history' attribute of an xarray object.

        Parameters
        ----------
        xr_obj: xarray.Dataset or xarray.DataArray
            The xarray object to be accessed.
        """
        self._obj = xr_obj
        self._ensure_history()

    def _ensure_history(self):
        """
        Ensure that the 'history' attribute exists in the xarray object.
        If it doesn't exist, create an empty 'history' attribute.
        """
        if 'history' not in self._obj.attrs.keys():
            self._obj.attrs['history'] = ""

    def add(self, msg):
        """
        Add an entry to the history.

        Parameters
        ----------
        msg: str
            The message to be added to the history.

        Example
        -------
        >>> da.history.add("New entry to history")        # doctest: +SKIP
        """
        self._obj.attrs['history'] += msg
        log.debug("Wrote '%s' to history", msg)
        return


