# !/usr/bin/env python3
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import numpy as np
import xarray as xr


def weighted_annual_mean(ds: xr.Dataset | xr.DataArray):
    """Compute the annual mean of an :class:`xr.Dataset`, thereby considering the
    different lengths of the months. That is, the function weights each month of the
    year by the number of days it comprises.

    Source: https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/
    """
    # Determine the month length
    month_length = ds.time.dt.days_in_month

    # Calculate the weights
    # In each 4th year, the total amount of days differs compared to other years
    # Therefore, weights need to be calculated on an annual base
    weights = month_length.groupby("time.year") / month_length.groupby("time.year").sum()

    # Make sure the weights in each year add up to 1
    assert np.allclose(weights.groupby("time.year").sum(xr.ALL_DIMS), 1.0), \
        "The sum of the weights should be 1.0!"

    # Setup our masking for nan values
    ones = xr.where(ds.isnull(), 0.0, 1.0)

    # Calculate the annual values, weighted by days in each month
    ds_sum = (ds * weights).resample(time="YS").sum(dim="time", keep_attrs=True)

    # Calculate the NaN weights
    # This gives every NaN in the original data a weight of zero, resulting in a lower
    # weight for affected years
    ones_out = (ones * weights).resample(time="YS").sum(dim="time", keep_attrs=True)

    # Return the weighted average
    output = ds_sum / ones_out

    output = output.assign_coords(year=('time', output.time.dt.year.values), keep_attrs=True)
    return output
