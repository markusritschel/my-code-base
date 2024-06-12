# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-04-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from functools import singledispatch
import logging
import numpy as np
import pandas as pd


log = logging.getLogger(__name__)




@singledispatch
def inv(x):
    """Invert a quadratic-shape :class:`numpy.ndarray` object."""
    return np.linalg.inv(x)


@inv.register(pd.DataFrame)
def _(df: pd.DataFrame):
    """Invert a quadratic-shape :class:`pandas.DataFrame` object."""
    assert np.equal(*df.shape), "Cannot invert non-quadratic object."
    inverted = np.linalg.inv(df)
    return pd.DataFrame(inverted, columns=df.columns, index=df.index)


def empirical_covariance(x, bias=False):
    """
    Compute the empirical covariance matrix of a given dataset:

    .. math::
        \\Sigma = \\frac{1}{\\text{dof}} DD^\\intercal

    where :math:`D` is the matrix of the anomalies (:math:`x-\\mu`) and dof is the degrees of freedom.
    Since for the matrix of the anomalies the mean has to be build first, one degree of freedom is gone. 
    Therefore, for the empirical covariance matrix, the normalization is usually done by ``(m-1)``.

    Depending on the parameter ``bias``, the degrees of freedom (``dof``) are either ``m`` or ``(m-1)``.

    Parameters
    ----------
    x : array-like
        Input dataset. It should be a 2-dimensional array-like object.
    bias : bool, optional
        If False, the normalization by the degrees of freedom (dof) is ``(m-1)``. Otherwise (``bias=True``), the normalization is by ``m``.

    Returns
    -------
    array-like
        The empirical covariance matrix of the input dataset.

    Example
    -------
    >>> import numpy as np
    >>> x = np.array([[92, 80], [60, 30], [100, 70]])
    >>> empirical_covariance(x)
    array([[ 72., 180., 180.],
           [180., 450., 450.],
           [180., 450., 450.]])

    >>> df = pd.DataFrame({"A": [92, 60, 100], "B": [80, 30, 70]}, index=[1, 2, 3])
    >>> df
         A   B
    1   92  80
    2   60  30
    3  100  70
    >>> empirical_covariance(df)
           1      2      3
    1   72.0  180.0  180.0
    2  180.0  450.0  450.0
    3  180.0  450.0  450.0
    """
    X = x.T
    µ = X.mean(axis=0)
    D = (X - µ)
    dof = X.shape[0] if bias else (X.shape[0] - 1)
    Σ = D.T.dot(D) / dof
    return Σ

