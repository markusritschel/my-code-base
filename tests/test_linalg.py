# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-04-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import pytest
import pandas as pd
import numpy as np

from my_code_base.linalg import empirical_covariance, inv

log = logging.getLogger(__name__)


def test_inv_dataframe():
    df = pd.DataFrame({
        'A': [1, 2],
        'B': [3, 4]
    })
    result = inv(df)
    expected = pd.DataFrame(np.linalg.inv(df.values), columns=df.columns, index=df.index)
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_inv_ndarray():
    x = np.array([[1, 2], [3, 4]])
    result = inv(x)
    expected = np.linalg.inv(x)
    assert np.allclose(result, expected), "The function does not return the expected result for ndarray input"


def test_inv_dataframe_non_quadratic():
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    with pytest.raises(AssertionError):
        inv(df)


def test_inv_ndarray_non_quadratic():
    x = np.array([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError):
        inv(x)


def test_empirical_covariance_dataframe():
    df = pd.DataFrame({"A": [92, 60, 100], "B": [80, 30, 70]}, index=[1, 2, 3])
    result = empirical_covariance(df)
    expected = np.cov(df.values, bias=False)
    assert np.allclose(
        result, expected
    ), "The function does not return the expected result for DataFrame input"
    expected = pd.DataFrame(
        np.array([[72, 180, 180], 
                  [180, 450, 450], 
                  [180, 450, 450]]),
        index=[1, 2, 3],
        columns=[1, 2, 3],
    )
    assert np.all(result == expected), "The function does not return the expected result for ndarray input"


def test_empirical_covariance_ndarray():
    x = np.array([[92, 80], [60, 30], [100, 70]])
    result = empirical_covariance(x)
    expected = np.cov(x, bias=False)
    assert np.allclose(result, expected), "The function does not return the expected result for ndarray input"
    expected = np.array([[ 72, 180, 180],
                         [180, 450, 450],
                         [180, 450, 450]])
    assert np.all(result == expected), "The function does not return the expected result for ndarray input"
