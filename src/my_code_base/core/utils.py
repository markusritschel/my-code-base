# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import functools
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from .xarray_utils import HistoryAccessor

logging.basicConfig(level="INFO")

log = logging.getLogger(__name__)


import matplotlib.pyplot as plt
@functools.singledispatch
def save(obj, *args, **kwargs):
    """
    Save the given object.

    Parameters
    ----------
    obj : object
        The object to be saved.

    Raises
    ------
    NotImplementedError
        If the according function is not dispatched.

    Notes
    -----
    This function raises a NotImplementedError because it is meant to be overridden by subclasses.
    To save objects of a specific type, please use the native method provided by that type.

    Examples
    --------
    >>> save(my_object)        # doctest: +SKIP
    NotImplementedError: Cannot save object of type <class 'type'> using `save` method. Please use the native method.
    """
    raise NotImplementedError(f"No implementation of `save` found for object of type {type(obj)}. "
                               "Please use the native method.")


@save.register(plt.Figure)
def _(fig, path, *args, **kwargs):
    plt.savefig(path, *args, **kwargs)

@save.register(pd.DataFrame)
def _(df, path, *args, **kwargs):
    df.to_csv(path, *args, **kwargs)


@save.register(xr.Dataset)
def _(ds, path, *args, **kwargs):
    ds = ds.history.add("Test")
    ds.to_netcdf(path, *args, **kwargs)


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
