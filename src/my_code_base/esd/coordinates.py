# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import xarray as xr

log = logging.getLogger(__name__)


def adjust_lons(ds, lon_name="lon"):
    """Adjust longitude values to make sure they are in the range between -180° and 180°."""
    ds["_longitude_adjusted"] = xr.where(ds[lon_name] > 180, ds[lon_name] - 360, ds[lon_name])

    # Carried over explicitly: the helper coordinate only inherits these because
    # `xr.where` keeps the attrs of its second argument by default.
    attributes = ds[lon_name].attrs.copy()

    # reassign the new coordinates to as the main lon coordinates
    # and sort DataArray using new coordinate values
    ds = (
        ds.swap_dims({lon_name: "_longitude_adjusted"})
        .sel(**{"_longitude_adjusted": sorted(ds._longitude_adjusted)})
        .drop_vars(lon_name)
    )

    ds = ds.rename({"_longitude_adjusted": lon_name})
    ds[lon_name].attrs.update(attributes)
    ds[lon_name].attrs["units"] = "degrees_east"
    ds[lon_name].attrs["standard_name"] = "longitude"
    return ds
