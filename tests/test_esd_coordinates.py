# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2026-07-29
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np
import pytest
import xarray as xr

from my_code_base.esd.coordinates import adjust_lons

log = logging.getLogger(__name__)


@pytest.fixture
def ds_0_360():
    """A dataset on a 0–360° longitude grid, carrying upstream coordinate metadata."""
    lons = np.array([0.0, 90.0, 180.0, 270.0])
    ds = xr.Dataset(
        {"sst": ("lon", np.arange(len(lons), dtype=float))},
        coords={"lon": lons},
    )
    ds["lon"].attrs = {
        "units": "degrees_east",
        "standard_name": "longitude",
        "long_name": "longitude of the grid cell centre",
        "axis": "X",
    }
    return ds


def test_lons_are_shifted_and_sorted(ds_0_360):
    result = adjust_lons(ds_0_360)
    np.testing.assert_array_equal(result["lon"].values, [-90.0, 0.0, 90.0, 180.0])


def test_data_follows_the_shifted_lons(ds_0_360):
    result = adjust_lons(ds_0_360)
    # sst was [0, 1, 2, 3] at lons [0, 90, 180, 270]; 270° -> -90° moves to the front
    np.testing.assert_array_equal(result["sst"].values, [3.0, 0.0, 1.0, 2.0])


def test_upstream_lon_attrs_are_preserved(ds_0_360):
    result = adjust_lons(ds_0_360)
    assert result["lon"].attrs["long_name"] == "longitude of the grid cell centre"
    assert result["lon"].attrs["axis"] == "X"


def test_cf_attrs_are_enforced(ds_0_360):
    ds_0_360["lon"].attrs["units"] = "degrees"
    ds_0_360["lon"].attrs["standard_name"] = "lon"
    result = adjust_lons(ds_0_360)
    assert result["lon"].attrs["units"] == "degrees_east"
    assert result["lon"].attrs["standard_name"] == "longitude"


def test_helper_coordinate_is_dropped(ds_0_360):
    result = adjust_lons(ds_0_360)
    assert "_longitude_adjusted" not in result.coords
    assert "_longitude_adjusted" not in result.variables
