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

logging.basicConfig(level="INFO")

log = logging.getLogger(__name__)

def add_metadata(func):
    """
    A decorator that adds metadata to the function's output.

    The metadata includes the relative path of the file, line number, and git commit hash.

    Parameters
    ----------
    func : callable 
        The function to be decorated.

    Returns
    -------
    callable
        The decorated function.
    """
    import os
    import subprocess
    import sys
    from pathlib import Path

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs.setdefault('add_hash', False)

        meta = collect_metadata()
        kwargs['metadata'] = meta

        args = list(args)
        obj = args[0]
        path = Path(args[1])
        suffix = ''
        if kwargs.pop('add_hash'):
            suffix += f"_{meta.git_commit}"
        output_path = f'{path.parent}/{path.stem}{suffix}{path.suffix}'
        args[1] = output_path
        
        obj_type = get_obj_type_str(obj)
        log.info(f"Saved {obj_type} to {output_path}, produced by {meta.relative_code_path}#{meta.line_number} @git-commit:{meta.git_commit}")

        return func(*args, **kwargs)

    def collect_metadata():
        frame = sys._getframe(1).f_back
        code_filename = frame.f_code.co_filename
        line_number = frame.f_lineno #- 1   # TODO: <-- check!
        relative_code_path = os.path.relpath(code_filename)
        git_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

        metadata = {}
        metadata['relative_code_path'] = relative_code_path
        metadata['line_number'] = str(line_number)
        metadata['git_commit'] = git_commit
        return BunchDict(metadata)
        
    return wrapper


class BunchDict(dict):
    """BunchDict is a subclass of the built-in dict class that allows 
    accessing dictionary keys as attributes.

    This class overrides the `__getattr__` and `__setattr__` methods to 
    provide attribute-style access to dictionary keys.
    When an attribute is accessed, it is treated as a dictionary key 
    and the corresponding value is returned.
    When an attribute is set, it is treated as a dictionary key and 
    the corresponding value is updated.

    .. note::
        This is now also implemented in :class:`sklearn.utils.Bunch`

    Example
    -------
    >>> bd = BunchDict()
    >>> bd['key'] = 'value'
    >>> print(bd.key)
    value
    >>> bd.key = 'new value'
    >>> print(bd['key'])
    new value
    """

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def get_obj_type_str(obj):
    """Transform the output of `type` to a simplified descriptor:
    
    Turns
        "<class 'xarray.core.dataset.Dataset'>"
    into "Dataset"
    """
    return str(type(obj)).split("'")[1].split('.')[-1]


@add_metadata
@functools.singledispatch
def save(obj, path, *args, **kwargs):
    """Save the given object including metadata.

    This is a dispatchable function. That is, there are several 
    implementations for different types of objects (e.g. 
    :class:`matplotlib.figure.Figure`, :class:`pandas.DataFrame`, 
    :class:`xarray.Dataset`). In case there is no implementation, 
    the function will throw a :class:`NotImplementedError`.

    Parameters
    ----------
    obj : object
        The object to be saved.
    path : str
        The path to which the object will be saved.

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
    >>> ds = xr.tutorial.load_dataset('air_temperature')       # doctest: +SKIP
    >>> save(ds, '/tmp/mynetcdf.nc', add_hash=True)            # doctest: +SKIP
    >>> !ncdump -h /tmp/mynetcdf_500e15f.nc | grep history     # doctest: +SKIP
    :history = "2024-06-12 16:18:16: File saved by myscript.py#3 @git-commit:500e15f;"
    >>> save(my_object, '/tmp/myobj')                          # doctest: +SKIP
    NotImplementedError: Cannot save object of type <class 'type'> using `save` method. Please use the native method.
    """
    raise NotImplementedError(f"No implementation of `save` found for object of type {type(obj)}. "
                               "Please use the native method.")


@save.register(plt.Figure)
def _(fig, path, *args, **kwargs):
    plt.savefig(path, *args, **kwargs)

@save.register(pd.DataFrame)
def _(df, path, *args, **kwargs):
    del kwargs['metadata']  # df.to_csv cannot interpret `metadata`
    df.to_csv(path, *args, **kwargs)


@save.register(xr.Dataset)
def _(ds, path, *args, **kwargs):
    from .xarray_utils import HistoryAccessor
    metadata = kwargs.pop('metadata')
    msg = f"File saved by {metadata['relative_code_path']}#{metadata['line_number']} @git-commit:{metadata['git_commit']}"
    ds = ds.history.add(msg)
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
