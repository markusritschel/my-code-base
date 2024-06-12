# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-08
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging


log = logging.getLogger(__name__)

def hex_to_rgb(value: str) -> tuple:
    """Convert hex to rgb colors

    Parameters
    ----------
    value: string
        String of 6 characters representing a hex colour.

    Returns
    -------
        list length 3 of RGB values
        
    Examples
    --------
    >>> hex_to_rgb('#f00')   # red
    (255, 0, 0)
    >>> hex_to_rgb('fff')    # white
    (255, 255, 255)
    """
    value = value.strip("#")  # removes hash symbol if present
    
    if len(value) == 3:
        value = ''.join(c*2 for c in value)
    elif len(value)!=6:
        raise ValueError("HEX value must be of length 3 or 6.")
    return tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))


def rgb_to_dec(value: list[float]) -> tuple[float]:
    """Convert rgb to decimal colours (i.e. divides each value by 255)

    Parameters
    ----------
    value: list (length 3) of RGB values

    Returns
    -------
        list (length 3) of decimal values
        
    Example
    -------
    >>> rgb_to_dec((255, 0, 0))
    (1.0, 0.0, 0.0)
    """
    return tuple([v/255 for v in value])


