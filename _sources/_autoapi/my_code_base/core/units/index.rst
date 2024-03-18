:py:mod:`my_code_base.core.units`
=================================

.. py:module:: my_code_base.core.units


Module Contents
---------------

.. py:function:: pressure2atm(p)

   Convert pressure given in hPa, Pa or atm into atm.

   .. rubric:: Examples

   >>> pressure2atm(1013.25)
   1.0
   >>> pressure2atm(101325)
   1.0
   >>> pressure2atm(2)
   2
   >>> pressure2atm(pd.Series([1013.25, 1024.0]))
   0    1.000000
   1    1.010609
   dtype: float64


.. py:function:: pressure2mbar(p)

   Convert pressure given in hPa, Pa or atm into mbar (or hPa).

   .. rubric:: Examples

   >>> pressure2mbar(1013)
   1013
   >>> pressure2mbar(101300)
   1013.0
   >>> pressure2mbar(1.0)
   1013.25
   >>> pressure2mbar(pd.Series([1.013, 2.034]))
   0    1026.42225
   1    2060.95050
   dtype: float64


.. py:function:: temperature2C(T)

   Convert temperatures given in Kelvin into °C.
   If `T` is a :class:`pandas.Series` object, only values less than 200 are converted. All others are expected to be
   already in °C.

   .. rubric:: Examples

   >>> temperature2C(283.15)
   10.0


.. py:function:: temperature2K(T)

   Convert temperatures given in °C into Kelvin.
   If `T` is a :class:`pandas.Series` object, only values larger than 200 are converted. All others are expected to be
   already in Kelvin.

   .. rubric:: Examples

   >>> temperature2K(10)
   283.15


