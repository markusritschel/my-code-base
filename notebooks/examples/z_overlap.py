# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: mcb
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Dealing with artifacts when plotting contour lines of curvilinear data
# Sometimes plotting contourlines of some curvilinear data sets, such as the NASA Team/Bootstrap data, can lead to unwanted artifacts.
# Let's assume we loaded the netCDF with xarray and want to plot the 15% SIC contour line for a specific time step.
#
# First, we load some packages and the data set:

# %%
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path
import cartopy.crs as ccrs
import my_code_base.plot.maps
DATA_DIR = Path("../../../../resice/data/")

# %%
ice_da = xr.open_dataset(DATA_DIR/f"raw/merged/observations/siconc/monthly/siconc_NASA-Merged_1979-2021.nc").siconc
ice_da = ice_da.isel(time=-10)

# %% [markdown]
# Now, simply plotting the data on the polar-stereographic projection woud produce a weird looking result:

# %%
ax = plt.subplot(projection=ccrs.NorthPolarStereo())
ice_da.plot.contour(ax=ax, x='lon', y='lat', transform=ccrs.PlateCarree(), 
                    levels=[15], colors=['r'], zorder=10)
ax.polar.add_features()

# %% [markdown]
# The contour lines are placed correctly but the polygons are not properly wrapped around the antimeridian.
#
# This problem is discussed and addressed in the following threads:
#
# - https://github.com/SciTools/cartopy/issues/1225
# - https://github.com/SciTools/cartopy/issues/1421
#
# The solution is the function `z_masked_overlap` they propose in these threads. Just copy it either from the github site or from here, and apply it to your data.
#
# Here, I wrote a small wrapper function (`fix_overlap`) to make it easier to use:

# %%
from my_code_base.plot.maps import fix_overlap

ax = plt.subplot(projection=ccrs.NorthPolarStereo())
ice_da = fix_overlap(ice_da, ax)
ice_da.plot.contour(ax=ax, x='lon', y='lat', 
                    levels=[15], colors=['r'], zorder=10)
ax.polar.add_features()

# %% [markdown]
# Et voilà! 🚀
#
# 👉 Note that after applying `fix_overlap` we don't specify the `transform` option in the plot command!
