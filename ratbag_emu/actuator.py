# SPDX-License-Identifier: MIT

import logging

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Actuator(ABC):
    '''
    Represents the firmware of the device

    Transforms actions based on physical properties
    '''
    def __init__(self) -> None:
        self.__logger = logging.getLogger('ratbag-emu.actuator')

        self._keys: List[str] = []

    @property
    def keys(self) -> List[str]:
        return self._keys

    @abstractmethod
    def transform(self, action: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Transforms action
        '''
