# SPDX-License-Identifier: MIT

import logging
import typing

from typing import Any

if typing.TYPE_CHECKING:
    from ratbag_emu.device import Device  # pragma: no cover


class HWComponent(object):
    '''
    Represents a physical hardware component

    This is the "brain" of the device. The custom logic is implemented here.
    '''
    def __init__(self, owner: 'Device', state: Any = None):
        self.__logger = logging.getLogger('ratbag-emu.hw_component')

        self._owner = owner

        self.state = state
