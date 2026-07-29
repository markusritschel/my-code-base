# Change Log

All notable changes to this project will be documented in this file.
<!-- This project adheres to [Semantic Versioning](http://semver.org/) -->

## Unreleased

### Added
- `TSAccessor` registered as `"ts"` on both `xr.Dataset` and `xr.DataArray`,
  providing `fill_years()` for expanding annual data to monthly resolution.
  Replaces `StatsAccessor.fill_months_with_annual_value()`.
- `_mask_after_threshold_crossing` in `stats/timeseries.py` — generalized version
  of `_mask_after_first_zero_crossing` with configurable threshold.
- `TestHasSeasonalFrequency` test class in `tests/test_xarray_utils.py` covering
  all code paths of `_has_seasonal_frequency`.

### Changed
- `StatsAccessor` now focuses on statistical operations only; time-series reshaping
  moved to the new `TSAccessor`.
- `xr_linregress`: Deseasonalization in DOF branches is now conditional on data
  having sub-annual frequency (new `deseasonalize` parameter and
  `_has_seasonal_frequency` helper).
- `xr_linregress`: `dof` parameter accepts a tuple to select the autocorrelation
  cutoff method, e.g. `dof=('integral_timescale', '1/e')` for 1/e decay threshold
  instead of zero-crossing.
- `xr_linregress`: Output DataArrays now carry CF-style `long_name` and `units`
  attributes.
- `ndof_integral_timescale`: removed duplicate NaN removal / mean subtraction;
  `n_eff` is now clamped to `[2, n]` with a warning when out of bounds.
- `effective_sample_size`: `n_eff` clamped to `[2, n]` with a warning; guards
  against division by zero when `r1 * r2 ≈ -1`.

### Fixed
- `_has_seasonal_frequency`: now handles `ValueError` from `pd.infer_freq` for
  series with fewer than 3 dates, falling back to the median-spacing heuristic.
- `_mask_after_first_zero_crossing`: returns input unchanged instead of crashing
  with `IndexError` when no zero crossing exists.
- `integral_timescale`: raises `ValueError` on NaN input (previously dropped NaNs
  silently, destroying temporal structure); replaced deprecated `np.trapz` with
  `np.trapezoid`; fixed docstring typo.
- `lag1_autocorrelation`: raises `ValueError` for inputs with fewer than 3 elements
  (2-element input would silently return `NaN` due to zero degrees of freedom in `np.corrcoef`).
- `ndof_lag1_autocorrelation`: fixed docstring — `y` is 1-D, not 2-D.

### Removed
- **Breaking:** `StatsAccessor.fill_months_with_annual_value()` — superseded by
  `TSAccessor.fill_years()`. Call sites must switch from `.stats` to the `.ts`
  accessor; there is no deprecation shim.

## 0.1.0

- _TODO: Update_
