# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-05
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import pytest
import cartopy.crs as ccrs
from matplotlib import pyplot as plt


@pytest.fixture(scope="module")
def ax_northpolar(request):
    ax = plt.subplot(projection=ccrs.NorthPolarStereo())
    return ax

