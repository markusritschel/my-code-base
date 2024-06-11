# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level="INFO")

log = logging.getLogger(__name__)


def find_nearest(items: list | np.ndarray, pivot: float) -> float:
    """
    Find the element inside `items` that is closest to the `pivot` element.

    Parameters
    ----------
    items: 
        A list of elements to search from.
    pivot: 
        The pivot element to find the closest element to.

    Returns
    -------
    float
        The element from `items` that is closest to the `pivot` element.

    Examples
    --------
    >>> find_nearest(np.array([2,4,5,7,9,10]), 4.6)
    5
    """
    return min(items, key=lambda x: abs(x - pivot))


def order_of_magnitude(x: int | float | np.ndarray | pd.Series) -> np.ndarray:
    """Determine the order of magnitude of the numeric input.

    Examples
    --------
    >>> order_of_magnitude(11)
    array([1.])
    >>> order_of_magnitude(234)
    array([2.])
    >>> order_of_magnitude(1)
    array([0.])
    >>> order_of_magnitude(.15)
    array([-1.])
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
