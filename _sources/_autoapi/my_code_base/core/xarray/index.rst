:py:mod:`my_code_base.core.xarray`
==================================

.. py:module:: my_code_base.core.xarray


Module Contents
---------------

.. py:class:: HistoryAccessor(xr_obj)


   .. py:method:: add(msg)

      Add an entry to the history.



.. py:function:: compress_xarray(data, complevel)

   Compress :class:`xr.Dataset` or :class:`xr.DataArray`.

   :param data: Data to compress.
   :type data: xr.Dataset | xr.DataArray
   :param complevel: Compression level.
   :type complevel: int

   :returns: Compressed data.
   :rtype: xr.Dataset | xr.DataArray


.. py:function:: get_dim_index(da, dim)

   Get the index of a dimension in a DataArray.

   :param da: DataArray to get the dimension index from.
   :type da: xr.DataArray
   :param dim: Dimension name.
   :type dim: str

   :rtype: Index of the dimension in the DataArray. Can be used for specifying the axis in a numpy operation.

   .. rubric:: Examples

   >>> da = xr.DataArray(np.random.rand(2, 3, 4), dims=['time', 'lat', 'lon'])
   >>> get_dim_index(da, 'lat')
   1


