:py:mod:`my_code_base.esd.utils`
================================

.. py:module:: my_code_base.esd.utils


Module Contents
---------------

.. py:function:: compute_weighted_mean(ds)

   Compute the weighted mean of a given xarray dataset.

   :param ds (xarray.Dataset):
   :type ds (xarray.Dataset): The input dataset.

   :returns: **xarray.DataArray**
   :rtype: The computed weighted mean.


.. py:function:: rename_obs(ds, rename_dict=None)

   Homogenize observation datasets to common naming.
   Following the function :function:`cmip6_preprocessing.preprocess.rename_cmip6`, thereby
   omitting `source_id` and extending the renaming_dict.


