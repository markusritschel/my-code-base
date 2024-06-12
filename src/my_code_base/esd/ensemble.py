# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-26
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from abc import ABC, abstractmethod
import logging


log = logging.getLogger(__name__)


class EnsembleAccessor(ABC):
    def __init__(self, data_obj) -> None:
        super().__init__()
        self._obj = data_obj
        self._key_template = None

    @property
    def key_template(self):
        """Return the key template"""
        if not self._key_template:
            raise KeyError("key_template not set. Make sure the attributes of the "
                           "'member' coordinate comprise a 'key_template' value. "
                           "You can set this via ds.ens.key_template = 'your.template'.")
        return self._key_template

    @key_template.setter
    def key_template(self, template_string):
        if '.' not in template_string: 
            raise ValueError("Elements must be divided by a dot (.).")
        if 'member' in template_string.split('.'):
            raise ValueError("key_template must not contain 'member'! "
                             "Please choose a different identifier.")
        self._key_template = template_string

