# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2026-04-16
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np
import pytest
import xarray as xr

from my_code_base.stats.timeseries import (
    _mask_after_first_zero_crossing,
    _mask_after_threshold_crossing,
    effective_sample_size,
    integral_timescale,
    lag1_autocorrelation,
    ndof_integral_timescale,
    ndof_lag1_autocorrelation,
    xr_autocorr,
)

log = logging.getLogger(__name__)

N = 200


@pytest.fixture(scope="module")
def white_noise():
    return np.random.default_rng(42).standard_normal(N)


@pytest.fixture(scope="module")
def ar1_series():
    """AR(1) process with φ=0.8 — strong positive autocorrelation."""
    rng = np.random.default_rng(0)
    phi = 0.8
    x = np.zeros(N)
    for t in range(1, N):
        x[t] = phi * x[t - 1] + rng.standard_normal()
    return x


@pytest.fixture(scope="module")
def da_white_noise(white_noise):
    return xr.DataArray(white_noise, dims=["time"])


# ---------------------------------------------------------------------------
# _mask_after_threshold_crossing
# ---------------------------------------------------------------------------


class TestMaskAfterThresholdCrossing:
    def test_masks_at_and_after_first_crossing(self):
        arr = np.array([3.0, 2.0, 1.0, -1.0, -2.0, -3.0])
        result = _mask_after_threshold_crossing(arr)
        np.testing.assert_array_equal(result[:3], arr[:3])
        assert np.all(np.isnan(result[3:]))

    def test_no_crossing_returns_unchanged(self):
        arr = np.array([3.0, 2.0, 1.0, 0.5])
        result = _mask_after_threshold_crossing(arr)
        np.testing.assert_array_equal(result, arr)

    def test_first_element_below_threshold_gives_all_nan(self):
        arr = np.array([-1.0, 2.0, 3.0])
        result = _mask_after_threshold_crossing(arr)
        assert np.all(np.isnan(result))

    def test_custom_threshold(self):
        arr = np.array([5.0, 3.0, 2.0, 0.5, -1.0])
        result = _mask_after_threshold_crossing(arr, threshold=1.0)
        # first value below 1.0 is 0.5 at index 3
        np.testing.assert_array_equal(result[:3], arr[:3])
        assert np.all(np.isnan(result[3:]))

    def test_does_not_mutate_input(self):
        arr = np.array([1.0, -1.0, 2.0])
        original = arr.copy()
        _mask_after_threshold_crossing(arr)
        np.testing.assert_array_equal(arr, original)


# ---------------------------------------------------------------------------
# _mask_after_first_zero_crossing
# ---------------------------------------------------------------------------


class TestMaskAfterFirstZeroCrossing:
    def test_equivalent_to_threshold_zero(self):
        arr = np.array([2.0, 1.0, -0.5, -1.0])
        np.testing.assert_array_equal(
            _mask_after_first_zero_crossing(arr),
            _mask_after_threshold_crossing(arr, threshold=0.0),
        )

    def test_all_positive_returns_unchanged(self):
        arr = np.array([3.0, 2.0, 1.0, 0.1])
        result = _mask_after_first_zero_crossing(arr)
        np.testing.assert_array_equal(result, arr)


# ---------------------------------------------------------------------------
# xr_autocorr
# ---------------------------------------------------------------------------


class TestXrAutocorr:
    def test_returns_dataarray(self, da_white_noise):
        assert isinstance(xr_autocorr(da_white_noise), xr.DataArray)

    def test_output_length_equals_input(self, da_white_noise):
        result = xr_autocorr(da_white_noise)
        assert len(result) == len(da_white_noise)

    def test_normalized_peak_at_lead_zero_is_one(self, da_white_noise):
        result = xr_autocorr(da_white_noise, normalize=True)
        assert float(result.sel(lead=0)) == pytest.approx(1.0)

    def test_normalized_max_is_one(self, da_white_noise):
        result = xr_autocorr(da_white_noise, normalize=True)
        assert float(result.max()) == pytest.approx(1.0)

    def test_unnormalized_max_differs_from_one(self, da_white_noise):
        result = xr_autocorr(da_white_noise, normalize=False)
        assert float(result.max()) != pytest.approx(1.0)

    def test_output_dim_renamed_to_lead(self, da_white_noise):
        result = xr_autocorr(da_white_noise)
        assert "lead" in result.dims
        assert "time" not in result.dims

    def test_custom_new_dim_name(self, da_white_noise):
        result = xr_autocorr(da_white_noise, new_dim="lag")
        assert "lag" in result.dims

    def test_lead_range_symmetric_around_zero(self, da_white_noise):
        result = xr_autocorr(da_white_noise)
        leads = result["lead"].values
        nlags = len(da_white_noise) // 2
        assert leads[0] == -nlags
        assert leads[-1] == nlags - 1


# ---------------------------------------------------------------------------
# integral_timescale
# ---------------------------------------------------------------------------


class TestIntegralTimescale:
    def test_raises_on_nan_input(self):
        with pytest.raises(ValueError, match="NaN"):
            integral_timescale(np.array([1.0, np.nan, 3.0]))

    def test_returns_positive_value(self, white_noise):
        assert integral_timescale(white_noise) > 0

    def test_white_noise_has_small_timescale(self, white_noise):
        # White noise ACF decays immediately — τ should be well below 2 time steps
        assert integral_timescale(white_noise) < 2.0

    def test_ar1_has_larger_timescale_than_white_noise(self, white_noise, ar1_series):
        assert integral_timescale(ar1_series) > integral_timescale(white_noise)

    def test_dt_scales_result_linearly(self, white_noise):
        τ1 = integral_timescale(white_noise, dt=1)
        τ2 = integral_timescale(white_noise, dt=2)
        assert τ2 == pytest.approx(2 * τ1)


# ---------------------------------------------------------------------------
# ndof_integral_timescale
# ---------------------------------------------------------------------------


class TestNdofIntegralTimescale:
    def test_returns_namedtuple_with_timescale_and_dof(self, white_noise):
        result = ndof_integral_timescale(white_noise)
        assert hasattr(result, "timescale")
        assert hasattr(result, "dof")

    def test_dof_is_non_negative(self, white_noise):
        assert ndof_integral_timescale(white_noise).dof >= 0

    def test_dof_does_not_exceed_n_minus_2(self, white_noise):
        assert ndof_integral_timescale(white_noise).dof <= N - 2

    def test_nan_in_input_is_handled(self):
        rng = np.random.default_rng(1)
        data = rng.standard_normal(100)
        data[::10] = np.nan
        result = ndof_integral_timescale(data)
        assert result.dof >= 0

    def test_ar1_has_fewer_dof_than_white_noise(self, white_noise, ar1_series):
        dof_white = ndof_integral_timescale(white_noise).dof
        dof_ar1 = ndof_integral_timescale(ar1_series).dof
        assert dof_ar1 < dof_white


# ---------------------------------------------------------------------------
# lag1_autocorrelation
# ---------------------------------------------------------------------------


class TestLag1Autocorrelation:
    def test_raises_for_empty_array(self):
        with pytest.raises(ValueError, match="Need at least 3 data points"):
            lag1_autocorrelation(np.array([]))

    def test_raises_for_single_element(self):
        with pytest.raises(ValueError, match="Need at least 3 data points"):
            lag1_autocorrelation(np.array([1.0]))

    def test_raises_for_length_two(self):
        with pytest.raises(ValueError, match="Need at least 3 data points"):
            lag1_autocorrelation(np.array([1.0, 2.0]))

    def test_length_three_works(self):
        r = lag1_autocorrelation(np.array([1.0, 2.0, 3.0]))
        assert -1.0 <= r <= 1.0

    def test_ascending_series_is_highly_correlated(self):
        r = lag1_autocorrelation(np.arange(50, dtype=float))
        assert r > 0.99

    def test_alternating_series_is_highly_anti_correlated(self):
        r = lag1_autocorrelation(np.array([1.0, -1.0] * 50))
        assert r < -0.99

    def test_result_in_valid_range(self, white_noise):
        r = lag1_autocorrelation(white_noise)
        assert -1.0 <= r <= 1.0


# ---------------------------------------------------------------------------
# effective_sample_size
# ---------------------------------------------------------------------------


class TestEffectiveSampleSize:
    def test_result_in_valid_range(self, white_noise):
        n_eff = effective_sample_size(white_noise, white_noise)
        assert 2 <= n_eff <= N

    def test_uncorrelated_series_gives_n_eff_close_to_n(self):
        rng = np.random.default_rng(99)
        x = rng.standard_normal(500)
        y = rng.standard_normal(500)
        n_eff = effective_sample_size(x, y)
        # r1 ≈ 0, r2 ≈ 0 → n_eff ≈ n; allow 20% margin for finite-sample noise
        assert n_eff > 0.8 * 500

    def test_ar1_reduces_n_eff(self, ar1_series):
        n_eff = effective_sample_size(ar1_series, ar1_series)
        assert n_eff < N

    def test_alternating_series_clamped_to_two(self):
        # r1 = r2 = -1 → r1*r2 = 1 → n_eff_raw = 0 → clamped to 2
        x = np.array([1.0, -1.0] * 100)
        assert effective_sample_size(x, x) == 2

    def test_n_eff_never_exceeds_n(self, white_noise):
        assert effective_sample_size(white_noise, white_noise) <= N


# ---------------------------------------------------------------------------
# ndof_lag1_autocorrelation
# ---------------------------------------------------------------------------


class TestNdofLag1Autocorrelation:
    def test_dof_equals_n_eff_minus_two(self):
        rng = np.random.default_rng(7)
        x = rng.standard_normal(100)
        y = rng.standard_normal(100)
        assert ndof_lag1_autocorrelation(x, y) == pytest.approx(
            effective_sample_size(x, y) - 2
        )

    def test_dof_is_non_negative(self, white_noise):
        assert ndof_lag1_autocorrelation(white_noise, white_noise) >= 0

    def test_ar1_has_fewer_dof_than_white_noise(self, white_noise, ar1_series):
        dof_white = ndof_lag1_autocorrelation(white_noise, white_noise)
        dof_ar1 = ndof_lag1_autocorrelation(ar1_series, ar1_series)
        assert dof_ar1 < dof_white
