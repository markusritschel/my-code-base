:py:mod:`my_code_base.ocean.utils`
==================================

.. py:module:: my_code_base.ocean.utils


Module Contents
---------------

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


.. py:function:: water_vapor_pressure(T, S)

   Compute the water vapor pressure by means of the temperature [K] and the salinity [PSU]
   following :cite:t:`weiss_nitrous_1980`.

   :param S: Salinity in PSU
   :type S: float or pd.Series
   :param T: Temperature (°C gets converted into Kelvin)
   :type T: float or pd.Series


