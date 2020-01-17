# SPDX-License-Identifier: MIT

import logging
import typing

from abc import ABC, abstractmethod
from typing import List

if typing.TYPE_CHECKING:
    from ratbag_emu.device import Device  # pragma: no cover


class Actuator(ABC):
    '''
    Represents the firmware of the device

    Transforms actions based on physical properties
    '''
    def __init__(self, owner: 'Device'):
        self.__logger = logging.getLogger('ratbag-emu.actuator')

        self._owner = owner

        self._keys: List[str] = []

    @property
    def keys(self):
        return self._keys

    @abstractmethod
    def transform(self, action):
        '''
        Transforms action
        '''
