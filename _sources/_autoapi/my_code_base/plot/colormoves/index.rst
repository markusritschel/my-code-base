:py:mod:`my_code_base.plot.colormoves`
======================================

.. py:module:: my_code_base.plot.colormoves

.. autoapi-nested-parse::

   This module provides functions to read in colormaps generated with ColorMoves.
   https://sciviscolor.org/colormoves/overview/
   https://sciviscolor.org/colormaps/
   https://sciviscolor.org/tools/



Module Contents
---------------

.. py:function:: plot_cmap(colormap)

   This is a quick example plotting the 8 by 1 gradient of the colormap


.. py:function:: xml_to_cmap(xml)

   Convert an XML file to a matplotlib colormap.

   :param xml: The path to the XML file.
   :type xml: str

   :returns: The generated colormap.
   :rtype: matplotlib.colors.LinearSegmentedColormap

   :raises ValueError: If the length of position is not the same as colors.
   :raises ValueError: If position does not start with 0 and end with 1.

   Source: http://schubert.atmos.colostate.edu/~cslocum/custom_cmap.html


