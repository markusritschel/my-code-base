:py:mod:`my_code_base.plot.z_overlap`
=====================================

.. py:module:: my_code_base.plot.z_overlap


Module Contents
---------------

.. py:function:: fix_overlap(da, ax)

   Fix overlapping geographic dimensions.
   This avoids artifacts when plotting contour lines of geographic data on a stereographic map
   projection.

   Calls :func:`z_masked_overlap` to perform the data transformation.

   :param da: An :class:`xr.DataArray` object with dimensions to be transformed.
   :type da: xr.DataArray
   :param ax: A matplotlib geoAxes object with stereographic projection.
   :type ax: plt.Axes


.. py:function:: z_masked_overlap(axe, X, Y, Z, source_projection=None)

   .. warning::
       Normally, one should avoid calling this function.
       Instead, use :func:`.fix_overlap` to fix the overlap.

   This function performs the actual transformation of the data for the :func:`.fix_overlap` function.

   It follows the solutions provided in the following issues:
       - https://github.com/SciTools/cartopy/issues/1225
       - https://github.com/SciTools/cartopy/issues/1421

   The function finds and masks the overlaps in the data that are more than half the range of the projection of the axes.

   :param axe: The axes object with the projection.
   :type axe: object
   :param X: The coordinates in the projection of the axes or the longitudes and latitudes.
   :type X: array_like
   :param Y: The coordinates in the projection of the axes or the longitudes and latitudes.
   :type Y: array_like
   :param Z: The data to be transformed.
   :type Z: array_like
   :param source_projection: If provided and is a geodetic CRS, the data is in geodetic coordinates and should first be projected in the projection of the axes.
   :type source_projection: ccrs.CRS, optional
   :param X:
   :param Y are 2D arrays with the same dimensions as Z for contour and contourf operations. They can also have an extra row and column for pcolor and pcolormesh operations.:

   :returns: **ptx, pty, Z** -- The transformed coordinates and data.
   :rtype: array_like


