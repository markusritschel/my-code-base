:py:mod:`my_code_base.plot`
===========================

.. py:module:: my_code_base.plot

.. autoapi-nested-parse::

   This module contains various helper functions for plotting.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   colormoves/index.rst
   maps/index.rst
   utils/index.rst
   z_overlap/index.rst


Package Contents
----------------

.. py:function:: xml_to_cmap(xml)

   Convert an XML file to a matplotlib colormap.

   :param xml: The path to the XML file.
   :type xml: str

   :returns: The generated colormap.
   :rtype: matplotlib.colors.LinearSegmentedColormap

   :raises ValueError: If the length of position is not the same as colors.
   :raises ValueError: If position does not start with 0 and end with 1.

   Source: http://schubert.atmos.colostate.edu/~cslocum/custom_cmap.html


