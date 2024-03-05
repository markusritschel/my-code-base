# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-05
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pytest
from my_code_base.plot.maps import *

import cartopy.crs as ccrs
from matplotlib import pyplot as plt


@pytest.fixture(scope="module")
def ax_northpolar(request):
    ax = plt.subplot(projection=ccrs.NorthPolarStereo())
    return ax


def test_projection_class(ax_northpolar):
    proj_type = type(ax_northpolar._projection_init[1]['projection'])
    assert proj_type == ccrs.NorthPolarStereo, "ax should be instance of ccrs.NorthPolarStereo"
    assert ax_northpolar.geomap._projection == ccrs.NorthPolarStereo, "ax should be instance of ccrs.NorthPolarStereo"
    
    assert ax_northpolar.polar._pole == 'north', "Expected `north` as pole name"