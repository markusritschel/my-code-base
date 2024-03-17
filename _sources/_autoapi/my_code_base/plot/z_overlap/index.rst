:py:mod:`my_code_base.plot.z_overlap`
=====================================

.. py:module:: my_code_base.plot.z_overlap


Module Contents
---------------

.. py:function:: fix_overlap(da, ax)

   Fix overlapping geographic dimensions.

   This avoids artifacts when plotting contour lines of geographic data on a stereographic map
   projection.

   :param da: An :class:`xr.DataArray` object with dimensions to be transformed.
   :type da: xr.DataArray
   :param ax: A matplotlib geoAxes object with stereographic projection.
   :type ax: plt.Axes


.. py:function:: z_masked_overlap(axe, X, Y, Z, source_projection=None)

   Following
   https://github.com/SciTools/cartopy/issues/1225
   https://github.com/SciTools/cartopy/issues/1421

   for data in projection axe.projection
   find and mask the overlaps (more 1/2 the axe.projection range)

   X, Y either the coordinates in axe.projection or longitudes latitudes
   Z the data
   operation one of 'pcorlor', 'pcolormesh', 'countour', 'countourf'

   if source_projection is a geodetic CRS data is in geodetic coordinates
   and should first be projected in axe.projection

   X, Y are 2D same dimension as Z for contour and contourf
   same dimension as Z or with an extra row and column for pcolor
   and pcolormesh

   return ptx, pty, Z


