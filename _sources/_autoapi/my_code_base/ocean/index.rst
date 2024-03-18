:py:mod:`my_code_base.ocean`
============================

.. py:module:: my_code_base.ocean

.. autoapi-nested-parse::

   This module provides routines for tackling oceanic biogeochemistry related tasks.

   - temperature and salinity normalization
   - temperature decomposition
   - fgCO2 <-> pCO2 and other conversions



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   bgc/index.rst
   utils/index.rst


Package Contents
----------------

.. py:function:: cond2sal(C, T, p)

   Compute salinity from conductivity, according to :cite:t:`lewis_practical_1981`.

   .. rubric:: Example

   >>> cond2sal(C=52, T=25, p=1013)
   34.20810771080768


.. py:function:: ppm2uatm(xCO2, p_equ, input='wet', T=None, S=None)

   Convert mole fraction concentration (in ppm) into partial pressure (in µatm) following :cite:t:`dickson_guide_2007`

   .. math::
       pCO_2 = xCO_2 \cdot p_\text{equ}

   :param xCO2: The measured CO2 concentration (in ppm)
   :type xCO2: float or pd.Series
   :param p_equ: The measured pressure (in hPa, Pa or atm) at the equilibrator (hint: you might want to smoothen your time series)
   :type p_equ: float or pd.Series
   :param input: Either "wet" or "dry", specifying the type of air, in which the concentration is measured.
                 If the CO2 concentration is measured in dry air, one must correct for the water vapor pressure.
                 In this case, make sure to also provide T (temperature in Kelvin) and S (salinity in PSU) as arguments.
   :type input: str [default: "wet"]
   :param T: Temperature in Kelvin (needs to be provided if xCO2 is measured in dry air)
   :type T: float or pd.Series [default: None]
   :param S: Salinity in PSU (needs to be provided if xCO2 is measured in dry air)
   :type S: float or pd.Series [default: None]


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


.. py:function:: water_vapor_pressure(T, S)

   Compute the water vapor pressure by means of the temperature [K] and the salinity [PSU]
   following :cite:t:`weiss_nitrous_1980`.

   :param S: Salinity in PSU
   :type S: float or pd.Series
   :param T: Temperature (°C gets converted into Kelvin)
   :type T: float or pd.Series


