# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-11
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from my_code_base.core.xarray_utils import *
from my_code_base.stats.xarray_utils import _has_seasonal_frequency

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def fixture_ds(request):
    return xr.tutorial.load_dataset("air_temperature")


@pytest.fixture(scope="module")
def da_6hourly(fixture_ds):
    return fixture_ds["air"]


@pytest.fixture(scope="module")
def da_monthly(fixture_ds):
    return fixture_ds["air"].resample(time="ME").mean()


@pytest.fixture(scope="module")
def da_annual():
    dates = pd.date_range("2000", periods=10, freq="YS")
    return xr.DataArray(np.ones(len(dates)), dims=["time"], coords={"time": dates})


@pytest.fixture
def da_integer_years():
    return xr.DataArray(
        np.ones(10), dims=["time"], coords={"time": np.arange(2000, 2010)}
    )


@pytest.fixture
def da_irregular_subannual():
    """Irregular monthly-ish dates: pd.infer_freq returns None, median ~30 days."""
    rng = np.random.default_rng(0)
    base = pd.date_range("2000-01-01", periods=24, freq="ME")
    jitter = pd.to_timedelta(rng.integers(-10, 10, 24), unit="D")
    dates = base + jitter
    return xr.DataArray(np.ones(len(dates)), dims=["time"], coords={"time": dates})


@pytest.fixture
def da_irregular_annual():
    """One sample per year but not on a regular anchor: pd.infer_freq returns None, median ~365 days."""
    dates = pd.to_datetime(
        [
            "2000-03-17",
            "2001-03-18",
            "2002-03-16",
            "2003-03-19",
            "2004-03-17",
            "2005-03-18",
            "2006-03-17",
            "2007-03-19",
        ]
    )
    return xr.DataArray(np.ones(len(dates)), dims=["time"], coords={"time": dates})


def test_history_accessor(fixture_ds):
    ds = fixture_ds
    ds.history.add("new entry")
    assert ds.attrs["history"].endswith("new entry; "), (
        "Couldn't find the expected entry in the history"
    )


class TestHasSeasonalFrequency:
    # --- infer_freq succeeds ---

    def test_6hourly_is_seasonal(self, da_6hourly):
        assert _has_seasonal_frequency(da_6hourly)

    def test_monthly_is_seasonal(self, da_monthly):
        assert _has_seasonal_frequency(da_monthly)

    def test_annual_is_not_seasonal(self, da_annual):
        assert not _has_seasonal_frequency(da_annual)

    # --- non-datetime dimension ---

    def test_integer_year_dim_is_not_seasonal(self, da_integer_years):
        assert not _has_seasonal_frequency(da_integer_years)

    # --- fallback path (pd.infer_freq returns None) ---

    def test_irregular_subannual_fallback_is_seasonal(self, da_irregular_subannual):
        assert _has_seasonal_frequency(da_irregular_subannual)

    def test_irregular_annual_fallback_is_not_seasonal(self, da_irregular_annual):
        assert not _has_seasonal_frequency(da_irregular_annual)

    # --- custom dim name ---

    def test_custom_dim_name(self, da_monthly):
        da = da_monthly.rename({"time": "t"})
        assert _has_seasonal_frequency(da, dim="t")
