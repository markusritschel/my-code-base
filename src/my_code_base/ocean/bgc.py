# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
import pandas as pd

from ..core.units import pressure2atm, temperature2K


log = logging.getLogger(__name__)


def temperature_correction(
    CO2: float | pd.Series,
    T_out: float | pd.Series = None,
    T_in: float | pd.Series = None,
    method: str="Takahashi2009",
    **kwargs
):
    """Apply a temperature correction. This might be necessary when the in-situ temperatures (at the water intake,
    often outside the ship) differ from where the CO2 measurement is done (often in a ferry-box onboard the ship).
    The correction used here follows :cite:t:`takahashi_climatological_2009`:

    .. math::
        {(xCO_2)}_{SST} = {(xCO_2)}_{T_\\text{equ}} \\cdot \\exp{\\Big(0.0433\\cdot(SST - T_\\text{equ}) - 4.35\\times 10^{-5}\\cdot(SST^2 - T_\\text{equ}^2)\\Big)}

    for correcting the temperature at the equilibrator :math:`T_\\text{equ}` to the SST.

    `CO2` can be one out of [xCO2 (mole fraction), pCO2 (partial pressure), fCO2 (fugacity)].

    Parameters
    ----------
    CO2:
        The CO2 variable, which shall be corrected for temperature differences.
        Can be one out of the following:
        - xCO2 (mole fraction in ppm)
        - pCO2 (partial pressure in hPa, Pa, atm or µatm)
        - fCO2 (:func:`.fugacity` in hPa, Pa, atm or µatm)
    T_out: 
        The temperature towards which the data shall be corrected. Typically, the in-situ temperature (°C or K), at which the water was sampled.
    T_in: 
        The temperature from which the data shall be corrected. Typically, the temperature (°C or K) at the equilibrator, at which the water was measured.
    method:
        Either "Takahashi2009" :cite:p:`takahashi_climatological_2009` or "Takahashi1993" :cite:p:`takahashi_seasonal_1993`, describing the method of the respectively published paper.
    """
    if T_out is None: T_out = kwargs.pop('T_insitu')
    if T_in is None: T_in = kwargs.pop('T_equ')
    if method=="Takahashi2009":
        CO2_out = CO2 * np.exp(0.0433*(T_out - T_in) - 4.35e-5*(T_out**2 - T_in**2))
    elif method=="Takahashi1993":
        CO2_out = CO2 * np.exp(0.0423*(T_out - T_in))
    else:
        raise IOError("Unknown method for temperature conversion.")

    return CO2_out


def fugacity(pCO2, p_equ, SST, xCO2=None):
    """Calculate the fugacity of CO2. Can be done either before or after a :func:`.temperature_correction`.
    The formulas follow :cite:t:`dickson_guide_2007`, mainly SOP 5, Chapter 8. "Calculation and expression of results".

    .. math::
       (fCO_2)^\\text{wet}_\\text{SST} = (pCO_2)^\\text{wet}_\\text{SST} \\cdot
            \\exp{\\Big(p_\\text{equ}\\cdot\\frac{\\left[ B(CO_2,SST) + 2\\,\\left(1-(xCO_2)^\\text{wet}_{SST}\\right)^2 \\, \\delta(CO_2,SST)\\right]}{R\\cdot SST}\\Big)}

    where :math:`SST` is the sea surface temperature in K, :math:`R` the gas constant and :math:`B(CO_2,SST)` and
    :math:`\delta(CO_2,SST)` are the virial coefficients for :math:`CO_2` (both in :math:`\\text{cm}^3\\,\\text{mol}^{-1}`), which are given as

    .. math::
       B(CO_2,T) = -1636.75 + 12.0408\\,T - 0.0327957\\,T^2 + 0.0000316528\\,T^3

    and

    .. math::
       \\delta(CO_2,T) = 57.7 - 0.188\\,T


    Parameters
    ----------
    pCO2: float or pandas.Series
        The partial pressure of CO2 (in µatm).
        Make sure you have converted xCO2 concentration (mole fraction in ppm) into partial pressure (in µatm).
    p_equ: float or pandas.Series
        The measured pressure (in hPa, Pa or atm) at the equilibrator (hint: you might want to smoothen your time series)
    SST: float or pandas.Series
        The in-situ measurement temperature (in °C or Kelvin)
    xCO2: float or pandas.Series (optional)
        CO2 concentration (mole fraction in ppm). If given, the δ_CO2 virial coefficient in the numerator in the exponential expression is multiplied by (1 - xCO2*1e-6). Else, this term is 1.
    """
    # Pa or hPa -> atm
    p_equ = pressure2atm(p_equ)

    # °C -> K
    SST = temperature2K(SST)

    # respectively in cm³/mol
    B_CO2 = -1636.75 + 12.0408*SST - 3.27957e-2*SST**2 + 3.16528e-5*SST**3
    δ_CO2 = 57.7 - 0.118*SST

    # gas constant
    R = 8.2057366080960e-2 	        #   L⋅atm⋅K−1⋅mol−1
    R *= 1000                       # cm³⋅atm⋅K−1⋅mol−1

    if xCO2 is None:
        x_c = 1
    else:
        x_c = (1 - xCO2*1e-6)       # can be (and is often) neglected in literature

    A = p_equ*(B_CO2 + 2 * δ_CO2 * x_c**2)
    B = R*SST
    f = pCO2 * np.exp(A / B)        # same unit as pCO2 (µatm)

    return f
