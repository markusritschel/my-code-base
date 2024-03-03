# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging


log = logging.getLogger(__name__)


def find_nearest(items: list, pivot: float) -> float:
    """Find the element inside `items` that is closest to the `pivot` element.

    Examples
    --------
    >>> nearest(np.array([2,4,5,7,9,10]), 4.6)
    5
    """
    return min(items, key=lambda x: abs(x - pivot))
