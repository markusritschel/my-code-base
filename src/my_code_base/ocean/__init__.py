# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
"""Provide routines for tackling tasks related to oceanic biogeochemistry.

- temperature and salinity normalization
- temperature decomposition
- fgCO2 <-> pCO2 and other conversions
"""

import logging

log = logging.getLogger(__name__)

from .utils import cond2sal, ppm2uatm, water_vapor_pressure

__all__ = ["cond2sal", "ppm2uatm", "water_vapor_pressure"]
