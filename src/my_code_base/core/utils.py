# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np


log = logging.getLogger(__name__)


def centered_bins(x):
    """Create centered bin boundaries from a given array with the values of the array as centers.

    Example
    -------
    >>> x = np.arange(-3, 4)
    >>> x
    array([-3, -2, -1,  0,  1,  2,  3])
    >>> centered_bins(x)
    array([-3.5, -2.5, -1.5, -0.5,  0.5,  1.5,  2.5,  3.5])
    """
    x = np.array(x)
    x = np.append(x, x[-1] + np.diff(x[-2:]))

    differences = np.gradient(x, 2)

    return x - differences


def find_nearest(items: list, pivot: float) -> float:
    """Find the element inside `items` that is closest to the `pivot` element.

    Examples
    --------
    >>> nearest(np.array([2,4,5,7,9,10]), 4.6)
    5
    """
    return min(items, key=lambda x: abs(x - pivot))


def order_of_magnitude(x):
    """Determine the order of magnitude of the numeric input (`int`, `float`, :meth:`numpy.array` or :meth:`pandas.Series`).

    Examples
    --------
    >>> order_of_magnitude(11)
    array(1.)
    >>> order_of_magnitude(234)
    array(2.)
    >>> order_of_magnitude(1)
    array(0.)
    >>> order_of_magnitude(.15)
    array(-1.)
    >>> order_of_magnitude(np.array([24.13, 254.2]))
    array([1., 2.])
    >>> order_of_magnitude(pd.Series([24.13, 254.2]))
    array([1., 2.])
    """
    x = np.asarray(x)
    if np.all(x == 0):
        return None
    x = x[x != 0]
    oom = np.floor(np.log10(x))
    # oom = (np.int32(np.log10(np.abs(x))) + 1)
    return np.array(oom)
