:py:mod:`my_code_base.stats.timeseries`
=======================================

.. py:module:: my_code_base.stats.timeseries


Module Contents
---------------

.. py:function:: weighted_annual_mean(ds)

   Compute the annual mean of an :class:`xr.Dataset`, thereby considering the different lengths of the months.
   That is, the function weights each month of the year by the number of days it comprises.

   Source: https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/


.. py:function:: xr_deseasonalize(ds, freq=12, dim='time')

   Remove the seasonal cycle of an :class:`xr.Dataset` object.
   Data get first detrended, then the long-term average of every season is subtracted for
   each season. Finally, the trend is added again.

   :param freq: The frequency of the data. Default is 12 for monthly resolution.
   :type freq: int
   :param dim: The name of the time dimension.
   :type dim: str


