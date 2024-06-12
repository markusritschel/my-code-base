# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
import pandas as pd

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

