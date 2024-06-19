# !/usr/bin/env python3
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
import xarray as xr
import xarrayutils

log = logging.getLogger(__name__)


def weighted_annual_mean(ds: xr.Dataset | xr.DataArray):
    """Compute the annual mean of an :class:`xr.Dataset`, thereby considering the
    different lengths of the months. That is, the function weights each month of the
    year by the number of days it comprises.

    Source: https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/
    """
    def check_for_frequency(ds):
        try:
            estimated_frequency = xr.infer_freq(ds.time)
            if not estimated_frequency.startswith('M'):
                log.warning("Frequency seems to be not monthly. Consider another averaging method.")
        except:
            log.warning("Cannot infer frequency")
            return
    
    check_for_frequency(ds)

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


def xr_deseasonalize(da, freq=12, dim='time'):
    """Remove the seasonal cycle of an :class:`xr.Dataset` object.
    Data get first detrended, then the long-term average of every season is subtracted for
    each season. Finally, the trend is added again.

    Parameters
    ----------
    freq : int
        The frequency of the data. Default is 12 for monthly resolution.
    dim : str
        The name of the time dimension.
    """
    res = xarrayutils.linear_trend(da, dim=dim)
    time_index = xr.DataArray(np.arange(da[dim].size), dims={dim:da[dim]}, coords={dim:da[dim]})
    trend = res.intercept + time_index*res.slope

    detrended = da - trend

    deseasonalized_detrended = (
        detrended.groupby(f'{dim}.month') - detrended.groupby(f'{dim}.month').mean()
        )
    return deseasonalized_detrended + trend
    
    
def xr_seasonal_decompose(da, dim='time'):
    """
    Perform seasonal decomposition of a time series using the given dataset.

    Parameters
    ----------
    da: xarray.DataArray
        The input data array containing the time series.
    dim: str
        The dimension along which the decomposition is performed. Default is 'time'.

    Returns
    -------
    xarray.Dataset: 
        A new dataset containing the decomposed components: trend, detrended, seasonality, residuals, and deseasonalized.
    """
    assert isinstance(da, xr.DataArray), "Input should be xarray.DataArray"
    
    res = xarrayutils.linear_trend(da, dim=dim)
    time_index = xr.DataArray(np.arange(da[dim].size), dims={dim:da[dim]}, coords={dim:da[dim]})

    trend = res.intercept + time_index*res.slope
    detrended = da - trend
    seasonality = detrended.groupby(f'{dim}.month').mean()
    residuals = detrended.groupby(f'{dim}.month') - seasonality
    deseasonalized = residuals + trend

    # Create a new dataset to store the results
    result = xr.Dataset()
    result['trend'] = trend
    result['detrended'] = detrended
    result['seasonality'] = seasonality
    result['residuals'] = residuals
    result['deseasonalized'] = deseasonalized
    
    return result


