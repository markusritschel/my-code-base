# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

import numpy as np


log = logging.getLogger(__name__)


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
