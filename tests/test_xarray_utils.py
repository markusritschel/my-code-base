# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-11
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import pytest
import xarray as xr
from my_code_base.core.xarray_utils import *

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def fixture(request):
    return xr.tutorial.load_dataset('air_temperature')


def test_history_accessor(fixture):
    ds = fixture
    ds.history.add("new entry")
    assert ds.attrs['history'] == "new entry", "Couldn't find the expected entry in the history"
