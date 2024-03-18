:py:mod:`my_code_base.plot.maps`
================================

.. py:module:: my_code_base.plot.maps


Module Contents
---------------

.. py:class:: GeoAxesAccessor(ax)




   Helper class that provides a standard way to create an ABC using
   inheritance.

   .. py:method:: add_coastlines(*args, **kwargs)

      Add coastlines to the GeoAxes.

      :param \*args: Arguments to be passed to the coastlines method of GeoAxes.
      :type \*args: list
      :param \*\*kwargs: Keyword arguments to be passed to the coastlines method of GeoAxes.
      :type \*\*kwargs: dict


   .. py:method:: add_features()
      :abstractmethod:


   .. py:method:: add_gridlines()
      :abstractmethod:


   .. py:method:: add_land(**kwargs)

      Add land feature to the GeoAxes.

      :param \*\*kwargs: Keyword arguments to be passed to the add_feature method of GeoAxes.
      :type \*\*kwargs: dict


   .. py:method:: add_ocean(**kwargs)

      Add ocean feature to the GeoAxes.

      :param \*\*kwargs: Keyword arguments to be passed to the add_feature method of GeoAxes.
      :type \*\*kwargs: dict


   .. py:method:: set_extent(extent, crs=cartopy.crs.PlateCarree())

      Set the extent of the GeoAxes.

      :param extent: The extent of the GeoAxes. It should be a tuple of the form (xmin, xmax, ymin, ymax).
      :type extent: tuple
      :param crs: The coordinate reference system in which the extent is expressed. Default is PlateCarree.
      :type crs: cartopy.crs



.. py:class:: StereographicAxisAccessor(ax)




   An accessor to handle features and finishing of stereographic plots produced with `cartopy`.
   Can handle both :class:`~cartopy.crs.NorthPolarStereo` and :class:`~cartopy.crs.SouthPolarStereo` projections.

   .. py:property:: lat_limits

      Get the latitude limits for the plot.

   .. py:method:: add_coastlines(*args, **kwargs)

      Add coastlines to the GeoAxes.

      :param \*args: Arguments to be passed to the coastlines method of GeoAxes.
      :type \*args: list
      :param \*\*kwargs: Keyword arguments to be passed to the coastlines method of GeoAxes.
      :type \*\*kwargs: dict


   .. py:method:: add_features(gridlines=True, ruler=True, **kwargs)

      Apply various features to the plot:
          - add ocean
          - add land
          - add coastlines
          - add ruler
          - make the boundary circular
          - add gridlines

      :param gridlines: Whether to add gridlines. Defaults to True.
      :type gridlines: bool, optional
      :param ruler: Whether to add a ruler. Defaults to True.
      :type ruler: bool, optional
      :param \*\*kwargs: Additional keyword arguments for customization.


   .. py:method:: add_gridlines(**kwargs)

      Add gridlines to the plot.

      :param \*\*kwargs: Additional keyword arguments for customization.

      :returns: The gridliner object.
      :rtype: :class:`cartopy.mpl.gridliner.Gridliner`


   .. py:method:: add_land(**kwargs)

      Add land feature to the GeoAxes.

      :param \*\*kwargs: Keyword arguments to be passed to the add_feature method of GeoAxes.
      :type \*\*kwargs: dict


   .. py:method:: add_ocean(**kwargs)

      Add ocean feature to the GeoAxes.

      :param \*\*kwargs: Keyword arguments to be passed to the add_feature method of GeoAxes.
      :type \*\*kwargs: dict


   .. py:method:: add_ruler(**kwargs)

      Add a circular ruler to the plot.

      :param \*\*kwargs: Additional keyword arguments for customization.


   .. py:method:: lat_limits()

      Get the latitude limits for the plot, with default values if not set.


   .. py:method:: make_circular()

      Make the plot boundary circular.


   .. py:method:: rotate_lat_labels(**kwargs)

      Rotate the latitude labels on the plot.

      :param \*\*kwargs: Additional keyword arguments for customization.


   .. py:method:: rotate_lon_labels()

      Rotate the longitude labels on the plot.


   .. py:method:: set_extent(extent, crs=cartopy.crs.PlateCarree())

      Set the extent of the GeoAxes.

      :param extent: The extent of the GeoAxes. It should be a tuple of the form (xmin, xmax, ymin, ymax).
      :type extent: tuple
      :param crs: The coordinate reference system in which the extent is expressed. Default is PlateCarree.
      :type crs: cartopy.crs



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


