# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
from copy import copy
from .utils import order_of_magnitude


log = logging.getLogger(__name__)


def pressure2atm(p):
    """Convert pressure given in hPa, Pa or atm into atm.

    Examples
    --------
    >>> pressure2atm(1013.25)
    1.0
    >>> pressure2atm(101325)
    1.0
    >>> pressure2atm(2)
    2
    >>> pressure2atm(pd.Series([1013.25, 1024.0]))
    0    1.000000
    1    1.010609
    dtype: float64
    """
    p = copy(p)
    if 2 <= np.nanmedian(np.rint(order_of_magnitude(p))) <= 3:
        p /= 1013.25
        log.info("Pressure is assumed to be in hPa and was converted to atm")
    elif 4 <= np.nanmedian(np.rint(order_of_magnitude(p))) <= 5:
        p /= 101325
        log.info("Pressure is assumed to be in Pa and was converted to atm")
    elif -1 <= np.nanmedian(np.rint(order_of_magnitude(p))) <= 1:
        log.info("Pressure is assumed to be already in atm (no conversion)")
    else:
        raise IOError("Pressure must be given in hPa, Pa or atm")
    return p


def pressure2mbar(p):
    """Convert pressure given in hPa, Pa or atm into mbar (or hPa).

    Examples
    --------
    >>> pressure2mbar(1013)
    1013
    >>> pressure2mbar(101300)
    1013.0
    >>> pressure2mbar(1.0)
    1013.25
    >>> pressure2mbar(pd.Series([1.013, 2.034]))
    0    1026.42225
    1    2060.95050
    dtype: float64
    """
    p = copy(p)
    if 2 <= np.nanmedian(np.rint(order_of_magnitude(p))) <= 3:
        log.info("Pressure is assumed to be already in mbar (no conversion)")
    elif 4 <= np.nanmedian(np.rint(order_of_magnitude(p))) <= 5:
        p /= 100
        log.info("Pressure is assumed to be in Pa and was converted to mbar (hPa)")
    elif -1 <= np.nanmedian(np.rint(order_of_magnitude(p))) <= 1:
        log.info("Pressure is assumed to be in atm and was converted to mbar (hPa)")
        p *= 1013.25
    else:
        raise IOError("Pressure must be given in hPa, Pa or atm")
    return p


