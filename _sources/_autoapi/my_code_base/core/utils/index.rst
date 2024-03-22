:py:mod:`my_code_base.core.utils`
=================================

.. py:module:: my_code_base.core.utils


Module Contents
---------------

.. py:function:: centered_bins(x)

   Create centered bin boundaries from a given array with the values of the array as centers.

   .. rubric:: Example

   >>> x = np.arange(-3, 4)
   >>> x
   array([-3, -2, -1,  0,  1,  2,  3])
   >>> centered_bins(x)
   array([-3.5, -2.5, -1.5, -0.5,  0.5,  1.5,  2.5,  3.5])


.. py:function:: find_nearest(items, pivot)

   Find the element inside `items` that is closest to the `pivot` element.

   :param items: A list of elements to search from.
   :type items: list
   :param pivot: The pivot element to find the closest element to.
   :type pivot: float

   :returns: The element from `items` that is closest to the `pivot` element.
   :rtype: float

   .. rubric:: Examples

   >>> find_nearest(np.array([2,4,5,7,9,10]), 4.6)
   5


.. py:function:: grid_dataframe(points, vals, xi, export_grid=False)

   Bin the values with `points` coordinates by the given target coordinates `xi` and put the average of each bin onto the target grid.

   :param points: A tuple `(x, y)` consisting of two lists holding the respective x and y coordinates of the source data.
   :type points: tuple[list, list]
   :param values: The actual data values that are meant to be regridded
   :type values: list
   :param xi: A tuple `(x, y)` consisting of two lists holding the target coordinates.
   :type xi: tuple[list, list]

   .. rubric:: Example

   >>> pytest.skip()
   >>> df = pd.DataFrame({'lon': np.linspace(0, 40, 100),
   >>>                    'lat': np.sin(np.linspace(0, 3, 100))*10 + 40,
   >>>                    'data': np.linspace(240,200,100)})
   >>> xi = np.linspace(-5, 45, 40)
   >>> yi = np.linspace(35, 53, 50)
   >>> gridded = grid_dataframe((df.lon, df.lat), df.data, (xi, yi))
   >>> plt.pcolormesh(xi, yi, gridded, shading='auto', cmap='Greens_r')
   >>> plt.scatter(df.lon, df.lat, c=df.data, marker='.', lw=.75, cmap='Reds', label='raw data')
   >>> plt.xlabel('Longitude')
   >>> plt.ylabel('Latitude')
   >>> plt.legend()
   >>> plt.show()

   .. image:: /_static/grid_dataframe_plot.png
      :width: 450px
      :alt: example plot
      :align: left


.. py:function:: order_of_magnitude(x)

   Determine the order of magnitude of the numeric input.

   .. rubric:: Examples

   >>> order_of_magnitude(11)
   array([1.])
   >>> order_of_magnitude(234)
   array([2.])
   >>> order_of_magnitude(1)
   array([0.])
   >>> order_of_magnitude(.15)
   array([-1.])
   >>> order_of_magnitude(np.array([24.13, 254.2]))
   array([1., 2.])
   >>> order_of_magnitude(pd.Series([24.13, 254.2]))
   array([1., 2.])


