# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-19
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np
import pandas as pd
import xarray as xr
from multipledispatch import dispatch
from scipy import stats

from .timeseries import extend_annual_series, weighted_annual_mean, xr_deseasonalize

log = logging.getLogger(__name__)


def _has_seasonal_frequency(obj, dim="time"):
    """Check if data has sub-annual temporal resolution."""
    time = obj[dim]
    if not np.issubdtype(time.dtype, np.datetime64):
        return False
    try:
        freq = pd.infer_freq(time.values)
    except ValueError:
        freq = None
    if freq is None:
        # Fallback: check median spacing
        dt = np.diff(time.values).astype("timedelta64[D]").astype(float)
        median_days = np.median(dt)
        return median_days < 360
    return not freq.startswith(("A", "Y", "AS", "YS"))


@xr.register_dataset_accessor("stats")
@xr.register_dataarray_accessor("stats")
class StatsAccessor:
    """
    This class provides statistical operations on xarray data.

    Parameters
    ----------
    obj : xarray.Dataset or xarray.DataArray
        The xarray object on which statistical operations will be performed.

    Methods
    -------
    weighted_mean(dim)
        Calculate the weighted mean based on the given dimension.
    """

    def __init__(self, obj):
        self._obj = obj

    @dispatch(str)
    def weighted_mean(self, dim):
        """
        Calculate the weighted annual mean (taking days of months into account).

        Parameters
        ----------
        dim : str
            The dimension along which to calculate the weighted mean.

        Returns
        -------
        weighted_mean : xarray.Dataset or xarray.DataArray
            The weighted annual mean.

        """
        log.debug(f"Identified single dimension {dim}. Building weighted annual mean.")
        return weighted_annual_mean(self._obj)

    def _is_annual(self):
        """
        Check if the xarray object has a 'year' dimension.

        Returns
        -------
        bool
            True if the xarray object has a 'year' dimension, False otherwise.
        """
        return 'year' in self._obj.dims

    def fill_months_with_annual_value(self):
        """
        Fill the xarray object with annual values for each month.

        Returns
        -------
        xarray.Dataset or xarray.DataArray
            The xarray object with extended annual series.

        Raises
        ------
        ValueError
            If the time series is not of yearly frequency.
        """
        ds = self._obj
        if not self._is_annual():
            raise ValueError("Time series is not of yearly frequency.")
        return extend_annual_series(ds)


def xr_linregress(x, y, dim='time', dof=None, deseasonalize: bool = True):
    """
    Calculate linear regression statistics between two :class:`xarray.DataArray` along a specified dimension.

    Parameters
    ----------
    x : xarray.DataArray
        The independent variable.
    y : xarray.DataArray
        The dependent variable.
    dim : str, optional
        The dimension along which to perform the regression. Defaults to 'time'.
    dof : int, str, or tuple, optional
        The degrees of freedom for the t-distribution. If None, it is calculated as n - 2,
        where n is the sample size. If 'integral_timescale', the integral timescale is 
        calculated and used to determine the degrees of freedom. If 'effective_sample_size', 
        the effective sample size is calculated and used to determine the degrees of freedom. 
        Can also be a tuple ``('integral_timescale', '1/e')`` to use the 1/e decay threshold
        instead of the first zero-crossing when computing the integral timescale.
        Defaults to None.

    Returns
    -------
    xarray.Dataset: 
        A dataset containing the following regression statistics:
        - 'sample_size': The number of non-null values along the specified dimension.
        - 'slope': The slope of the regression line.
        - 'intercept': The intercept of the regression line.
        - 'r_value': The correlation coefficient between x and y.
        - 'p_value': The two-tailed p-value for the null hypothesis that the slope is zero.
        - 'std_err': The standard error of the slope.

    Notes
    -----
    - NaN values are automatically excluded from the calculations.
    - The correlation coefficient, p-value, and standard error are calculated using the 
      t-distribution.
    - If dof is 'integral_timescale', the integral timescale is calculated as the sum 
      of autocorrelation values until the first zero-crossing. The effective sample size 
      is then calculated as the total sample size divided by the integral timescale.
    - If dof is 'effective_sample_size', the effective sample size is calculated as 
      n * (1 - r1*r2) / (1 + r1*r2), where r1 and r2 are the lag-1 autocorrelation 
      coefficients of x and y, respectively.
    """
    from ..stats.timeseries import _mask_after_threshold_crossing, xr_autocorr

    TINY = 1.0e-20

    # n = x[dim].size
    x = x.where(y.notnull())
    y = y.where(x.notnull())

    # COMMENT: If there are NaNs, the `n = x[dim].size` overstates the sample size, which deflates covariance/variance estimates (dividing by too-large N) and inflates DOF.
    # → Using notnull().sum(dim) for correctness. See Issue #16
    n = y.notnull().sum(dim)
    nanmask = np.isnan(y).all(dim)

    xmean = x.mean(dim)
    ymean = y.mean(dim)
    xstd = x.std(dim)
    ystd = y.std(dim)

    cov = ((x - xmean) * (y - ymean)).sum(dim) / n
    cor = cov / (xstd * ystd)

    slope = cov / (xstd**2)
    intercept = ymean - xmean * slope

    out_dict = {'sample_size': n}

    # Parse tuple-based dof parameter, e.g. dof=('integral_timescale', '1/e')
    integral_cutoff = "zero_crossing"
    if isinstance(dof, tuple):
        dof, integral_cutoff = dof
    elif isinstance(dof, int):
        dof = dof - 2
    if dof is None:
        dof = n - 2

    elif dof == "integral_timescale":
        # COMMENT: Seasonal autocorrelation inflates τ, making n_eff artificially small (overly conservative).
        # → Deseasonalize, but only if the data has sub-annual frequency. See Issue #17
        if deseasonalize and _has_seasonal_frequency(x, dim=dim):
            x = xr_deseasonalize(x)
        x_autocorr = xr_autocorr(x, dim=dim, normalize=True)
        positive_r = x_autocorr.sel(lead=slice(0, None))
        threshold = 1 / np.e if integral_cutoff == "1/e" else 0.0
        positive_r_masked = xr.apply_ufunc(
            _mask_after_threshold_crossing,
                positive_r,
            kwargs={"threshold": threshold},
                input_core_dims=[['lead']],
                output_core_dims=[['lead']],
                dask="parallelized",
                vectorize=True,
            output_dtypes=['float'],
        )
        τ = positive_r_masked.fillna(0).integrate(coord="lead")
        log.debug(f"Integral timescale: {τ}")
        n_eff = n / τ  # Following eq. (3.15.17) in Emery & Thomson (2004)
        n_eff = n_eff.where(n_eff < n, n)  # allow a maximum of n for n_eff

        dof = n_eff - 2
        out_dict.update(
            {
                "autocorr": x_autocorr,
                "integral_timescale": τ,
                "effective_sample_size": n_eff,
            }
        )

    elif dof == "effective_sample_size":
        # See Issue #16
        if deseasonalize and _has_seasonal_frequency(x, dim=dim):
            x = xr_deseasonalize(x)
            y = xr_deseasonalize(y)
        r1 = xr_autocorr(x, dim=dim, normalize=True).sel(lead=1)
        r2 = xr_autocorr(y, dim=dim, normalize=True).sel(lead=1)
        n_eff = n * (1 - r1 * r2) / (1 + r1 * r2)
        dof = n_eff - 2
        out_dict.update({'effective_sample_size': n_eff})

    out_dict.update({'dof': dof})
    log.info(f"Degrees of freedom: {dof}")

    tstats = cor * np.sqrt(dof / ((1.0 - cor + TINY) * (1.0 + cor + TINY)))
    stderr = slope / tstats
    # Issue #15: Should we scale with σ?

    pval = (
        xr.apply_ufunc(
            stats.distributions.t.sf,  # sf is the survival function (1 - cdf)
            abs(tstats),
            dof,
            dask="parallelized",
            output_dtypes=[y.dtype],
        )
        * 2  # Convert pval to a two-tailed test
    )

    out_dict.update(
        {
        "slope": slope,
        "intercept": intercept,
        "r_value": cor.fillna(0).where(~nanmask),
        "p_value": pval,
        "std_err": stderr.where(~np.isinf(stderr), 0),
        }
    )

    ds = xr.Dataset(out_dict)

    _metadata = {
        "sample_size": {"long_name": "Number of valid observations"},
        "dof": {"long_name": "Degrees of freedom"},
        "slope": {"long_name": "Regression slope", "units": "[y] / [x]"},
        "intercept": {"long_name": "Regression intercept", "units": "[y]"},
        "r_value": {"long_name": "Pearson correlation coefficient"},
        "p_value": {"long_name": "Two-tailed p-value"},
        "std_err": {"long_name": "Standard error of the slope", "units": "[y] / [x]"},
        "autocorr": {"long_name": "Autocorrelation function"},
        "integral_timescale": {"long_name": "Integral timescale", "units": "[x]"},
        "effective_sample_size": {"long_name": "Effective sample size"},
    }
    for var, attrs in _metadata.items():
        if var in ds:
            ds[var].attrs.update(attrs)

    return ds
