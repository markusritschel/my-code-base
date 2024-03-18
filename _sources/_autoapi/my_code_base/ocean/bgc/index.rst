:py:mod:`my_code_base.ocean.bgc`
================================

.. py:module:: my_code_base.ocean.bgc


Module Contents
---------------

.. py:function:: fugacity(pCO2, p_equ, SST, xCO2=None)

   Calculate the fugacity of CO2. Can be done either before or after a :func:`.temperature correction`.
   The formulas follow :cite:t:`dickson_guide_2007`, mainly SOP 5, Chapter 8. "Calculation and expression of results"

   .. math::
      (fCO_2)^\text{wet}_\text{SST} = (pCO_2)^\text{wet}_\text{SST} \cdot
           \exp{\Big(p_\text{equ}\cdot\frac{\left[ B(CO_2,SST) + 2\,\left(1-(xCO_2)^\text{wet}_{SST}\right)^2 \, \delta(CO_2,SST)\right]}{R\cdot SST}\Big)}

   where :math:`SST` is the sea surface temperature in K, :math:`R` the gas constant and :math:`B(CO_2,SST)` and
   :math:`\delta(CO_2,SST)` are the virial coefficients for :math:`CO_2` (both in :math:`\text{cm}^3\,\text{mol}^{-1}`), which are given as

   .. math::
      B(CO_2,T) = -1636.75 + 12.0408\,T - 0.0327957\,T^2 + 0.0000316528\,T^3

   and

   .. math::
      \delta(CO_2,T) = 57.7 - 0.188\,T


   :param pCO2: The partial pressure of CO2 (in µatm).
                Make sure you have converted xCO2 concentration (mole fraction in ppm) into partial pressure (in µatm).
   :type pCO2: float or pd.Series
   :param p_equ: The measured pressure (in hPa, Pa or atm) at the equilibrator (hint: you might want to smoothen your time series)
   :type p_equ: float or pd.Series
   :param SST: The in-situ measurement temperature (in °C or Kelvin)
   :type SST: float or pd.Series
   :param xCO2: CO2 concentration (mole fraction in ppm). If given, the δ_CO2 virial coefficient in the numerator in the exponential expression is multiplied by (1 - xCO2*1e-6). Else, this term is 1.
   :type xCO2: float or pd.Series (optional)


.. py:function:: temperature_correction(CO2, T_out=None, T_in=None, method='Takahashi2009', **kwargs)

   Apply a temperature correction. This might be necessary when the in-situ temperatures (at the water intake,
   often outside the ship) differ from where the CO2 measurement is done (often in a ferry-box onboard the ship).
   The correction used here follows :cite:t:`takahashi_climatological_2009`:

   .. math::
       {(xCO_2)}_{SST} = {(xCO_2)}_{T_\text{equ}} \cdot \exp{\Big(0.0433\cdot(SST - T_\text{equ}) - 4.35\times 10^{-5}\cdot(SST^2 - T_\text{equ}^2)\Big)}

   for correcting the temperature at the equilibrator :math:`T_\text{equ}` to the SST.

   `CO2` can be one out of [xCO2 (mole fraction), pCO2 (partial pressure), fCO2 (fugacity)].

   :param CO2: The CO2 variable, which shall be corrected for temperature differences.
               Can be one out of the following:
               - xCO2 (mole fraction in ppm)
               - pCO2 (partial pressure in hPa, Pa, atm or µatm)
               - fCO2 (fugacity in hPa, Pa, atm or µatm)
   :type CO2: float or pd.Series
   :param T_out: The temperature towards which the data shall be corrected. Typically, the in-situ temperature (°C or K), at which the water was sampled.
   :type T_out: float or pd.Series
   :param T_in: The temperature from which the data shall be corrected. Typically, the temperature (°C or K) at the equilibrator, at which the water was measured.
   :type T_in: float or pd.Series
   :param method: Either "Takahashi2009" or "Takahashi1993", describing the method of the respectively published paper by Takahashi et al.
   :type method: str


