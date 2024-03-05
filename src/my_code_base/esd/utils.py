# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

log = logging.getLogger(__name__)


"""A universal renaming dict. Keys correspond to source id (model name)
and values are a dict of target name (key) and a list of variables that
should be renamed into the target."""
_RENAME_DICT = {
    # dim labels (order represents the priority when checking for the dim labels)
    "x": ["x", "i", "ni", "xh", "nlon", "lon", "longitude"],
    "y": ["y", "j", "nj", "yh", "nlat", "lat", "latitude"],
    "lev": ["lev", "deptht", "olevel", "zlev", "olev", "depth"],
    "bnds": ["bnds", "axis_nbounds", "d2"],
    "vertex": ["vertex", "nvertex", "vertices"],
    # coordinate labels
    "lon": ["lon", "longitude", "nav_lon"],
    "lat": ["lat", "latitude", "nav_lat"],
    "lev_bounds": [
        "lev_bounds",
        "deptht_bounds",
        "lev_bnds",
        "olevel_bounds",
        "zlev_bnds",
        ],
    "lon_bounds": [
        "bounds_lon",
        "bounds_nav_lon",
        "lon_bnds",
        "x_bnds",
        "vertices_longitude",
        ],
    "lat_bounds": [
        "bounds_lat",
        "bounds_nav_lat",
        "lat_bnds",
        "y_bnds",
        "vertices_latitude",
        ],
    "time_bounds": ["time_bounds", "time_bnds"],
    }


def rename_obs(ds, rename_dict=None):
    """Homogenize observation datasets to common naming.
    Following the function :function:`cmip6_preprocessing.preprocess.rename_cmip6`, thereby 
    omitting `source_id` and extending the renaming_dict."""
    ds = ds.copy()

    if rename_dict is None:
        log.debug("Load default dictionary for renaming variables")
        rename_dict = _RENAME_DICT

        # add new entries
        rename_dict['x'][1:1] = ['xc', 'xgrid']
        rename_dict['y'][1:1] = ['yc', 'ygrid']

    # rename variables
    if len(rename_dict) == 0:
        warnings.warn(
            "Input dictionary empty.",
            UserWarning,
            )
    else:
        for di in rename_dict.keys():

            # make sure the input is a list
            if not isinstance(rename_dict[di], list):
                raise ValueError(
                    f"Input dict must have a list as value. Got {rename_dict[di]} for key {di}"
                    )

            if di not in ds.variables:

                # For now just stop in the list if the dimension is already there, or one 'hit'
                # was already encountered.
                trigger = False
                for wrong in rename_dict[di]:
                    if wrong in ds.variables or wrong in ds.dims:
                        if not trigger:
                            log.debug("Rename %s with %s", wrong, di)
                            ds = ds.rename({wrong: di})
                            trigger = True

    log.debug(ds)
    return ds
