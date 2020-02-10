# SPDX-License-Identifier: MIT

import logging

from typing import Any


class HWComponent(object):
    '''
    Represents a physical hardware component

    This is the "brain" of the device. The custom logic is implemented here.
    '''
    def __init__(self, state: Any = None):
        self.__logger = logging.getLogger('ratbag-emu.hw_component')

        self.state = state
