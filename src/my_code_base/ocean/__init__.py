# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-03
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
"""This module provides routines for tackling oceanic biogeochemistry related tasks.

- temperature and salinity normalization
- temperature decomposition
- fgCO2 <-> pCO2 and other conversions
# TODO: check content of `oceanpack` package and move/copy to `ocean_bgc` if necessary
"""
import logging


log = logging.getLogger(__name__)

from .utils import *
