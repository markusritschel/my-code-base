# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-08
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import matplotlib.colors as mcolors
import numpy as np


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


def build_continuous_cmap(hex_list: list[str], float_list=None, N=256, name='my_cmap') -> mcolors.LinearSegmentedColormap:
    """Create and return a color map that can be used in heat map figures.
    If `float_list` is not provided, colour map graduates linearly between each color in hex_list.
    If `float_list` is provided, each color in `hex_list` is mapped to the respective location in `float_list`.

    Source: https://towardsdatascience.com/beautiful-custom-colormaps-with-matplotlib-5bab3d1f0e72

    Parameters
    ----------
    hex_list: list of hex code strings
    float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.

    Returns
    -------
    colour map
    """
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], 
                     rgb_list[i][num], 
                     rgb_list[i][num]] 
                    for i in range(len(float_list))]
        cdict[col] = col_list
    cmap = mcolors.LinearSegmentedColormap(name, segmentdata=cdict, N=N)
    return cmap

