# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np

from ..core.units import pressure2atm, pressure2mbar, temperature2C, temperature2K


log = logging.getLogger(__name__)


def cond2sal(C, T, p):
    """Compute salinity from conductivity, according to :cite:t:`lewis_practical_1981`.

    Example
    -------
    >>> cond2sal(C=52, T=25, p=1013)
    34.20810771080768
    """
    p = pressure2mbar(p)/100  # convert hPa (mbar) -> dbar
    T = temperature2C(T)

    a0 = 0.008
    a1 = -0.1692
    a2 = 25.3851
    a3 = 14.0941
    a4 = -7.0261
    a5 = 2.7081

    b0 = 0.0005
    b1 = -0.0056
    b2 = -0.0066
    b3 = -0.0375
    b4 = 0.0636
    b5 = -0.0144

    c0 = 6.766097e-1
    c1 = 2.00564e-2
    c2 = 1.104259e-4
    c3 = -6.9698e-7
    c4 = 1.0031e-9

    A1 = 2.070e-5
    A2 = -6.370e-10
    A3 = 3.989e-15
    B1 = 3.426e-2
    B2 = 4.464e-4
    B3 = 4.215e-1
    B4 = -3.107e-3

    R = C/42.914  # units: mS/cm
    # TODO: check input units of Conductivity! "If you are working in conductivity units of Siemens/meter (S/m), multiply your conductivity values by 10 before using the PSS 1978 equations. "
    # TODO: maybe use units from log file for auto-conversion and print a hint or so (this could be already done during the read routine)

    rT = c0 + c1*T + c2*T**2 + c3*T**3 + c4*T**4

    alpha = (A1*p + A2*p**2 + A3*p**3)/(1 + B1*T + B2*T**2 + B3*R + B4*T*R)

    Rp = 1 + alpha

    RT = R/(rT*Rp)

    k = 0.0162  # TODO: check sign! +/-?

    ξ = np.sqrt(RT)
    ψ = b0 + b1*ξ + b2*ξ**2 + b3*ξ**3 + b4*ξ**4 + b5*ξ**5
    dSal = ψ*(T - 15)/(1 + k*(T - 15))

    salinity = a0 + a1*ξ + a2*ξ**2 + a3*ξ**3 + a4*ξ**4 + a5*ξ**5 + dSal

    return salinity


def water_vapor_pressure(T, S):
    """Compute the water vapor pressure by means of the temperature [K] and the salinity [PSU]
    following :cite:t:`weiss_nitrous_1980`.

    Parameters
    ----------
    S: float or pandas.Series
        Salinity in PSU
    T: float or pandas.Series
        Temperature (°C gets converted into Kelvin)
    """
    T = temperature2K(T)

    pH2O = np.exp(24.4543 - 67.4509*(100/T) - 4.8489*np.log(T/100) - 0.000544*S)
    return pH2O


def ppm2uatm(xCO2, p_equ, input='wet', T=None, S=None):
    """Convert mole fraction concentration (in ppm) into partial pressure (in µatm) following :cite:t:`dickson_guide_2007`

    .. math::
        pCO_2 = xCO_2 \\cdot p_\\text{equ}

    Parameters
    ----------
    xCO2: float or pandas.Series
        The measured CO2 concentration (in ppm)
    p_equ: float or pandas.Series
        The measured pressure (in hPa, Pa or atm) at the equilibrator (hint: you might want to smoothen your time series)
    input: str [default: "wet"]
        Either "wet" or "dry", specifying the type of air, in which the concentration is measured.
        If the CO2 concentration is measured in dry air, one must correct for the water vapor pressure.
        In this case, make sure to also provide T (temperature in Kelvin) and S (salinity in PSU) as arguments.
    T: float or pandas.Series [default: None]
        Temperature in Kelvin (needs to be provided if xCO2 is measured in dry air)
    S: float or pandas.Series [default: None]
        Salinity in PSU (needs to be provided if xCO2 is measured in dry air)
    """
    # Pa or hPa -> atm
    p_equ = pressure2atm(p_equ)

    if input == "dry":
        pH2O = water_vapor_pressure(T, S)
    elif input == "wet":
        pH2O = 0
    else:
        raise IOError("Input must be either 'dry' or 'wet'.")

    pCO2_wet_equ = xCO2*(p_equ - pH2O)

    return pCO2_wet_equ

