# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from abc import ABC
import logging


log = logging.getLogger(__name__)


class GeoAxesAccessor(ABC):
    def __init__(self, ax):
        log.debug('Initialize accessor')
        self.geo_axes = ax

