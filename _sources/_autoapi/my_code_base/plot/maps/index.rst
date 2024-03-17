:py:mod:`my_code_base.plot.maps`
================================

.. py:module:: my_code_base.plot.maps


Module Contents
---------------

.. py:class:: GeoAxesAccessor(ax)




   Helper class that provides a standard way to create an ABC using
   inheritance.

   .. py:method:: add_coastlines(*args, **kwargs)


   .. py:method:: add_features()
      :abstractmethod:


   .. py:method:: add_gridlines()
      :abstractmethod:


   .. py:method:: add_land(**kwargs)


   .. py:method:: add_ocean(**kwargs)


   .. py:method:: set_extent(extent, crs=cartopy.crs.PlateCarree())



.. py:class:: StereographicAxisAccessor(ax)




   An accessor to handle features and finishing of stereographic plots produced with `cartopy`.
   Can handle both :class:`ccrs.NorthPolarStereo` and :class:`ccrs.SouthPolarStereo` projections.

   .. py:property:: lat_limits


   .. py:method:: add_coastlines(*args, **kwargs)


   .. py:method:: add_features(gridlines=True, ruler=True, **kwargs)

      Perform the following steps:
      - add ocean
      - add land
      - add coastlines
      - add ruler
      - make the boundary circular
      - add gridlines


   .. py:method:: add_gridlines(**kwargs)


   .. py:method:: add_land(**kwargs)


   .. py:method:: add_ocean(**kwargs)


   .. py:method:: add_ruler(**kwargs)


   .. py:method:: lat_limits()


   .. py:method:: make_circular()


   .. py:method:: rotate_lat_labels(**kwargs)


   .. py:method:: rotate_lon_labels()


   .. py:method:: set_extent(extent, crs=cartopy.crs.PlateCarree())



.. py:function:: add_circular_ruler(ax, segment_length=30, offset=0, primary_color='k', secondary_color='w', width=1)

   Add a ruler around a polar stereographic plot.

   :param ax: The GeoAxes object to which the ruler should be added
   :type ax: GeoAxes
   :param segment_length: The length of each segment in degrees
   :type segment_length: int
   :param offset: An optional offset
   :type offset: int
   :param primary_color: The color of the background ruler segments
   :type primary_color: str
   :param secondary_color: The color of the top ruler segments
   :type secondary_color: str
   :param width: The scaled thickness of the ruler. Defaults to 1/80 of the axes' width.
   :type width: float


.. py:function:: register_geoaxes_accessor(accessor_name)

   Register an accessor for a cartopy.GeoAxes object.

   .. rubric:: Example

   >>> pytest.skip()
   >>> @register_geoaxes_accessor("my_accessor")
   >>> class MyCustomAccessor:
   >>>     def some_method(self):
   >>>         pass
   >>>
   >>> ax = plt.subplot(projection=cartopy.crs.NorthPolarStereo())
   >>> ax.my_accessor.some_method()


.. py:function:: rotate_polar_plot_lat_labels(gl, target_lon=118, orig_lon=150)

   Move the latitude labels to another longitude.

   :param gl: The gridlines object holding the labels.
   :type gl: gridlines
   :param target_lon: The longitude to which the labels should be moved.
   :type target_lon: int
   :param orig_lon: The longitude at which the labels are located per default [default: 150].
   :type orig_lon: int
   :param Following the solution on https:
   :type Following the solution on https: //stackoverflow.com/a/66587492/5925453 with some minor adaptions.


.. py:function:: rotate_polar_plot_lon_labels(gl, pole='north')

   Rotate the longitude labels of a stereographic plot for better readability and nicer look.

   :param gl: The gridlines object holding the labels.
   :type gl: gridlines
   :param pole: The pole to rotate the labels towards. Can be either 'north' or 'south' [default: 'north'].
   :type pole: str (optional)


.. py:function:: set_circular_boundary(ax)

   Compute a circle in axes coordinates, which we can use as a boundary for the map.
   We can pan/zoom as much as we like – the boundary will be permanently circular.


