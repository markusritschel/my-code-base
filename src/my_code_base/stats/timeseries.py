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
import pandas as pd
import xarray as xr
import xarrayutils

log = logging.getLogger(__name__)


def weighted_annual_mean(ds: xr.Dataset | xr.DataArray):
    """
    Compute the weighted annual mean of an :class:`xarray.Dataset` or :class:`xarray.DataArray`.

    Parameters
    ---------
    ds :
        The input dataset or data array.

    Returns
    -------
    xarray.DataArray
        The weighted annual mean of the input dataset or data array.

    Raises
    ------
    AssertionError
        If the sum of the weights in each year is not equal to 1.0.

    Notes
    -----
    The function computes the annual mean of the input dataset or data array, taking into account the different lengths
    of the months. Each month is weighted by the number of days it comprises. If the frequency of the time dimension is
    '1M', the function applies the weights. If the frequency is '1D' or higher, no weights are applied.

    The function follows the approach described in the following source:
    https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/

    The function assumes that the input dataset or data array has a 'time' dimension.

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
    return output.swap_dims({'time': 'year'}).drop_vars('time')


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


def pd_seasonal_decompose(x, freq=12):
    """Decompose a time series into its trend, the seasonality, and the residuals.

    Parameters
    ----------
    x: pandas.Series
        A :class:`pandas.Series` containing a time series of data
    freq : int
        The frequency of the data, e.g. 12 for monthly data

    Returns
    -------
    A :class:`pandas.DataFrame` containing time series of the raw data, trend,
    seasonality, the detrended time series, and the residuals.
    """
    assert isinstance(x, pd.Series), "The input should be a pandas.Series"

    df = x.to_frame("raw")

    # calculate the trend component
    # TODO: decide if this should be calculated based on a running mean or the linear trend
    df["trend"] = df["raw"].rolling(window=freq+1, center=True).mean()

    # detrend the series
    df["detrended"] = df["raw"] - df["trend"]

    # calculate the seasonal component
    df.index = pd.to_datetime(df.index)
    df["seasonality"] = df.groupby(df.index.month)["detrended"].transform("mean")

    # get the residuals
    df["residuals"] = df["detrended"] - df["seasonality"]

    return df[['raw', 'trend', 'seasonality', 'detrended', 'residuals']]


def extend_annual_series(ds):
    """
    Fill a time series with only annual values (one such timeseries could be generated
    via :func:`weighted_annual_mean`, for example) such that all months are represented again but the value 
    for all 12 months within a year is equal to the annual value.

    Parameters
    ----------
    ds : xarray.Dataset
        The input dataset containing the time series data.

    Returns
    -------
    xarray.Dataset
        The extended time series dataset with monthly values.

    Raises
    ------
    AssertionError
        If the dataset does not have 'year' as a dimension.

    Example
    -------
    >>> ds = xr.Dataset({'time': pd.date_range('2000-01-01', '2001-12-31', freq='ME'),
    ...                  'value': np.random.rand(24)})
    >>> extended_ds = extend_annual_series(ds)
    """
    if 'year' not in ds.dims:
        ds = (ds.assign_coords(year=('time', ds.time.dt.year.values))
              .swap_dims({'time': 'year'})).drop_vars(['time'])

    assert 'year' in ds.dims, 'Dataset needs to have `year` as dimension'

    ds_monthly = ds.expand_dims(month=np.arange(1, 13))
    ds_stacked = ds_monthly.stack(year_month=('year', 'month'))

    _datetime = pd.to_datetime([f"{y}-{m}" for y in ds_monthly.year.values
                                           for m in np.arange(1, 13)])
    ds_stacked = ds_stacked.assign_coords(time=('year_month', _datetime))
    ds_stacked = ds_stacked.swap_dims({'year_month': 'time'})

    ds_stacked = ds_stacked.drop_vars(['year', 'month', 'year_month'])
    return ds_stacked

