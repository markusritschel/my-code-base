# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-20
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pytest
import cartopy.crs as ccrs
from matplotlib import pyplot as plt
from my_code_base.plot.maps import *
from my_code_base.plot.maps import _lon2rot


@pytest.fixture(scope="module")
def ax_northpolar(request: pytest.FixtureRequest):
    ax = plt.subplot(projection=ccrs.NorthPolarStereo())
    return ax


@pytest.fixture(scope="module")
def ax_southpolar(request):
    ax = plt.subplot(projection=ccrs.SouthPolarStereo())
    return ax


def test_projection_class(ax_northpolar, ax_southpolar):
    proj_type = type(ax_northpolar._projection_init[1]['projection'])
    assert proj_type == ccrs.NorthPolarStereo, "ax should be instance of ccrs.NorthPolarStereo"
    assert ax_northpolar.polar._projection == ccrs.NorthPolarStereo, "ax should be instance of ccrs.NorthPolarStereo"
    assert ax_southpolar.polar._projection == ccrs.SouthPolarStereo, "ax should be instance of ccrs.SouthPolarStereo"

    assert ax_northpolar.polar._pole == 'north', "Expected `north` as pole name"
    assert ax_southpolar.polar._pole == 'south', "Expected `south` as pole name"


def test_geoaxes_latlimits(ax_northpolar, ax_southpolar):
    assert ax_northpolar.polar.lat_limits == [50, 90], "Expected different latitude limits"
    assert ax_southpolar.polar.lat_limits == [-90, -50], "Expected different latitude limits"
    ax_northpolar.polar.lat_limits = [30, 70]
    assert ax_northpolar.polar.lat_limits == [30, 70], "Expected different latitude limits"
    

def test_helper():
    assert _lon2rot(0, pole='north') == 0, "Incorrect rotation of longitude value"
    assert _lon2rot(30, pole='north') == 30, "Incorrect rotation of longitude value"
    assert _lon2rot(60, pole='north') == 60, "Incorrect rotation of longitude value"
    assert _lon2rot(120, pole='north') == -60, "Incorrect rotation of longitude value"
    assert _lon2rot(160, pole='north') == -20, "Incorrect rotation of longitude value"
    assert _lon2rot(180, pole='north') == 0, "Incorrect rotation of longitude value"

    assert _lon2rot(0, pole='south') == 0, "Incorrect rotation of longitude value"
    assert _lon2rot(30, pole='south') == -30, "Incorrect rotation of longitude value"
    assert _lon2rot(60, pole='south') == -60, "Incorrect rotation of longitude value"
    assert _lon2rot(120, pole='south') == 60, "Incorrect rotation of longitude value"
    assert _lon2rot(160, pole='south') == 20, "Incorrect rotation of longitude value"
    assert _lon2rot(180, pole='south') == 0, "Incorrect rotation of longitude value"
