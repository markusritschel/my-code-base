# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging

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

