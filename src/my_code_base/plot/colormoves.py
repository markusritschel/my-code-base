# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-10
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
"""This module provides functions to read in colormaps generated with ColorMoves.

Sources:

- https://sciviscolor.org/colormoves/overview/
- https://sciviscolor.org/colormaps/
- https://sciviscolor.org/tools/
"""
import logging
from lxml import etree

import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np


log = logging.getLogger(__name__)


def xml_to_cmap(xml):
    """
    Convert an XML file to a matplotlib colormap.

    Args:
        xml (str): The path to the XML file.

    Returns:
        matplotlib.colors.LinearSegmentedColormap: The generated colormap.

    Raises:
        ValueError: If the length of position is not the same as colors.
        ValueError: If position does not start with 0 and end with 1.

    Source: http://schubert.atmos.colostate.edu/~cslocum/custom_cmap.html
    """
    vals = _load_xml(xml)
    colors, position = vals["color_vals"], vals["data_vals"]

    if len(position) != len(colors):
        raise ValueError("position length must be the same as colors")
    if position[0] != 0 or position[-1] != 1:
        raise ValueError("position must start with 0 and end with 1")

    cdict = {color: [(pos, col, col) for pos, col in zip(position, cols)] for color, cols in zip(["red", "green", "blue"], zip(*colors))}

    return mpl.colors.LinearSegmentedColormap("my_colormap", cdict, 256)



def _load_xml(xml):
    try:
        xmldoc = etree.parse(xml)
    except IOError:
        raise IOError('Invalid input file. It must be a colormap xml file. Visit' 
                      'https://sciviscolor.org/home/colormaps/ for options. '
                      'Visit https://sciviscolor.org/matlab-matplotlib-pv44/ for an example use of this script.')

    points = [(float(s.attrib['x']),
               (float(s.attrib['r']),
                float(s.attrib['g']),
                float(s.attrib['b'])))
              for s in xmldoc.getroot().findall('.//Point')]

    data_vals, color_vals = zip(*points)
    return {'color_vals': color_vals, 'data_vals': data_vals}


def plot_cmap(colormap):
    """This is a quick example plotting the 8 by 1 gradient of the colormap"""
    plt.imshow(np.vstack((np.linspace(0, 1, 256),) * 2), aspect='auto', cmap=plt.get_cmap(colormap))
    plt.axis('off')
    plt.tight_layout()
    plt.show()
