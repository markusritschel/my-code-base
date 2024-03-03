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

