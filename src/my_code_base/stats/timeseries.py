# !/usr/bin/env python3
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
from collections import namedtuple

import numpy as np
import pandas as pd
import xarray as xr
import xarrayutils

log = logging.getLogger(__name__)


def weighted_annual_mean(ds: xr.Dataset | xr.DataArray):
    """
    Compute the weighted annual mean of an :class:`xarray.Dataset` or :class:`xarray.DataArray`.

    Parameters
    ----------
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
            if not estimated_frequency.startswith("M"):
                log.warning(
                    "Frequency seems to be not monthly. Consider another averaging method."
                )
        except:
            log.warning("Cannot infer frequency")
            return
    
    check_for_frequency(ds)

    # Determine the month length
    month_length = ds.time.dt.days_in_month

    # Calculate the weights
    # In each 4th year, the total amount of days differs compared to other years
    # Therefore, weights need to be calculated on an annual base
    weights = (
        month_length.groupby("time.year") / month_length.groupby("time.year").sum()
    )

    # Make sure the weights in each year add up to 1
    assert np.allclose(weights.groupby("time.year").sum(xr.ALL_DIMS), 1.0), (
        "The sum of the weights should be 1.0!"
    )

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

    output = output.assign_coords(
        year=("time", output.time.dt.year.values), keep_attrs=True
    )
    return output.swap_dims({"time": "year"}).drop_vars("time")


def xr_deseasonalize(da, freq=12, dim="time"):
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
    time_index = xr.DataArray(
        np.arange(da[dim].size), dims={dim: da[dim]}, coords={dim: da[dim]}
    )
    trend = res.intercept + time_index * res.slope

    detrended = da - trend

    deseasonalized_detrended = (
        detrended.groupby(f"{dim}.month") - detrended.groupby(f"{dim}.month").mean()
        )
    return deseasonalized_detrended + trend
    
    
def xr_seasonal_decompose(da, dim="time"):
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
    time_index = xr.DataArray(
        np.arange(da[dim].size), dims={dim: da[dim]}, coords={dim: da[dim]}
    )

    trend = res.intercept + time_index * res.slope
    detrended = da - trend
    seasonality = detrended.groupby(f"{dim}.month").mean()
    residuals = detrended.groupby(f"{dim}.month") - seasonality
    deseasonalized = residuals + trend

    # Create a new dataset to store the results
    result = xr.Dataset()
    result["trend"] = trend
    result["detrended"] = detrended
    result["seasonality"] = seasonality
    result["residuals"] = residuals
    result["deseasonalized"] = deseasonalized
    
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
    df["trend"] = df["raw"].rolling(window=freq + 1, center=True).mean()

    # detrend the series
    df["detrended"] = df["raw"] - df["trend"]

    # calculate the seasonal component
    df.index = pd.to_datetime(df.index)
    df["seasonality"] = df.groupby(df.index.month)["detrended"].transform("mean")

    # get the residuals
    df["residuals"] = df["detrended"] - df["seasonality"]

    return df[["raw", "trend", "seasonality", "detrended", "residuals"]]


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
    if "year" not in ds.dims:
        ds = (ds.assign_coords(year=("time", ds.time.dt.year.values))
              .swap_dims({"time": "year"})).drop_vars(["time"])

    assert "year" in ds.dims, "Dataset needs to have `year` as dimension"

    ds_monthly = ds.expand_dims(month=np.arange(1, 13))
    ds_stacked = ds_monthly.stack(year_month=("year", "month"))

    # Convert `year` coordinate back to `time`
    _datetime = pd.to_datetime(
        [f"{y}-{m}" for y in ds_monthly.year.values for m in np.arange(1, 13)]
    )
    ds_stacked = ds_stacked.assign_coords(time=("year_month", _datetime))
    ds_stacked = ds_stacked.swap_dims({"year_month": "time"})

    ds_stacked = ds_stacked.drop_vars(["year", "month", "year_month"])
    return ds_stacked


def zero_crossings(x):
    """Find the zero crossings of a time series.
    
    Example
    -------
    >>> x = np.array([1, 2, -1, -2, 1, 2])     # crossing at 2 -> -1 and -2 -> 1
    >>> zero_crossings(x)
    array([1, 3])
    """
    return np.where(np.diff(np.sign(x)))[0]


def _mask_after_threshold_crossing(arr, threshold=0.0):
    """Mask values after the signal first drops below *threshold*."""
    below = arr < threshold
    if not np.any(below):
        return arr
    first_idx = np.argmax(below)
    out = arr.copy()
    out[first_idx:] = np.nan
    return out


def _mask_after_first_zero_crossing(x):
    return _mask_after_threshold_crossing(x, threshold=0.0)


def xr_autocorr(x, dim="time", normalize=True, new_dim="lead"):
    """Calculate the autocorrelation of a time series.
    
    Parameters
    ----------
    x : xarray.DataArray
        The input data array containing the time series.
    dim : str, optional
        The dimension along which to calculate the autocorrelation. Defaults to 'time'.
    normalize : bool, optional
        Whether to normalize the autocorrelation. Defaults to True.
    new_dim : str, optional
        The name of the new dimension. Defaults to 'lead'.

    Returns
    -------
    xarray.DataArray
        The autocorrelation of the time series.
    """
    from scipy import signal

    corr = xr.apply_ufunc(
        signal.correlate,
        x,
        x,
        kwargs=dict(mode="same"),
        input_core_dims=[[dim], [dim]],
        output_core_dims=[[dim]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[x.dtype],
        keep_attrs=False,
    )

    if normalize:
        corr /= corr.max(dim=dim)
    corr = corr.rename({dim: new_dim})
    nlags = len(x[dim]) // 2
    corr[new_dim] = np.arange(-nlags, nlags)
    
    return corr


def integral_timescale(data, dt=1):
    """
    Calculate the integral timescale of decorrelation of a time series.

    Parameters
    ----------
    data : np.ndarray
        The input data array containing the time series.
        Must be NaN-free; pass pre-cleaned data to avoid
        destroying temporal structure.
    dt : float
        The time step of the data.

    Returns
    -------
    float
        The integral timescale of the time series.

    Raises
    ------
    ValueError
        If the input data contains NaN values.

    Notes
    -----
    The integral timescale is calculated as the integral of the
    autocorrelation function (ACF) of the time series up to the
    first zero crossing.
    """
    from scipy.signal import correlate

    if np.any(np.isnan(data)):
        raise ValueError(
            "Input data contains NaN values. Remove NaNs before calling this function."
        )

    data = data - data.mean()

    # Calculate autocorrelation, use only 2nd half (non-negative lags), and normalize
    autocorr = correlate(data, data, mode="full")
    autocorr = autocorr[autocorr.size // 2 :]
    autocorr = autocorr / autocorr.max()


    autocorr = _mask_after_first_zero_crossing(autocorr)
    autocorr = np.nan_to_num(autocorr)

    τ = np.trapezoid(autocorr, dx=dt)

    return τ


# alias
decorrelation_timescale = integral_timescale


def ndof_integral_timescale(data, dt=1):
    """
    Calculate the number of degrees of freedom (dof) of the integral
    timescale of decorrelation of a time series.

    Parameters
    ----------
    data : np.ndarray
        The input data array containing the time series.
    dt : float
        The time step of the data.

    Returns
    -------
    IntegralTimescaleResult
        Named tuple with fields ``timescale`` (the integral timescale)
        and ``dof`` (the degrees of freedom).

    Notes
    -----
    The effective sample size is calculated as ``n * dt / τ`` following
    Emery & Thomson (2004), eq. (3.15.17). It is clamped to ``[2, n]``
    to ensure valid degrees of freedom.
    """
    data = data[~np.isnan(data)]
    data = data - data.mean()

    τ = integral_timescale(data, dt)
    m = len(data)
    n_eff_raw = m * dt / τ if τ > 0 else float(m)
    n_eff = np.clip(n_eff_raw, 2, m)
    if n_eff != n_eff_raw:
        log.warning(
            "Effective sample size clamped to [2, %d] (raw n_eff=%.2f)", m, n_eff_raw
        )
    dof = n_eff - 2
    return _IntegralTimescaleResult(τ, dof)


_IntegralTimescaleResult = namedtuple("IntegralTimescaleResult", ["timescale", "dof"])


def lag1_autocorrelation(x):
    """Calculate the lag-1 autocorrelation of a time series."""
    if len(x) < 3:
        raise ValueError(
            f"Need at least 3 data points for lag-1 autocorrelation, got {len(x)}."
        )
    return np.corrcoef(x[:-1], x[1:])[0, 1]


def effective_sample_size(x, y):
    """
    Calculate the effective sample size of two time series based on the lag-1 autocorrelation.

    Parameters
    ----------
    x : np.ndarray
        The first time series data.
    y : np.ndarray
        The second time series data.

    Returns
    -------
    float
        The effective sample size of the two time series.
    """
    r1 = lag1_autocorrelation(x)
    r2 = lag1_autocorrelation(y)

    n = x.size
    denom = 1 + r1 * r2
    if np.isclose(denom, 0):
        log.warning(
            "r1*r2 ≈ -1 (denom=%.4f); effective sample size "
            "is ill-defined, clamping to n=%d",
            denom,
            n,
        )
        return float(n)

    n_eff_raw = n * (1 - r1 * r2) / denom
    # Following Bretherton et al. (1999), eq. 31
    # DOI: 10.1175/1520-0442(1999)012<1990:TENOSD>2.0.CO;2
    n_eff = np.clip(n_eff_raw, 2, n)
    if n_eff != n_eff_raw:
        log.warning(
            "Effective sample size clamped to [2, %d] (raw n_eff=%.2f)", n, n_eff_raw
        )

    return n_eff


def ndof_lag1_autocorrelation(x, y):
    """
    Calculate the number of degrees of freedom (ndof) based on the lag-1 autocorrelation
    of two time series.

    Parameters
    ----------
    x: 1-D array-like
        The first time series data.
    y: 1-D array-like
        The second time series data.

    Returns
    -------
    dof: float
        The number of degrees of freedom.
    """
    n_eff = effective_sample_size(x, y)
    dof = n_eff - 2
    return dof


