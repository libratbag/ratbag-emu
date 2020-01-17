# SPDX-License-Identifier: MIT

import logging
import typing

from typing import List

if typing.TYPE_CHECKING:
    from ratbag_emu.device import Device  # pragma: no cover


class Firmware(object):
    '''
    Represents the firmware of the device

    This is the "brain" of the device, it is here where we custom logic is
    implemented.
    '''
    def __init__(self, owner: 'Device'):
        self.__logger = logging.getLogger('ratbag-emu.firmware')

        self._owner = owner

    def hid_receive(self, data: List[int], size: int, rtype: int,
                    endpoint: int):
        '''
        Receive data

        Callback called when we receive a HID report.

        :param data:        Received data
        :param size:        Received data size
        :param rtype:       Report type
        :param endpoint:    Endpoint number
        '''
        return

    def hid_send(self, data: List[int], endpoint: int):
        '''
        Send data to endpoint

        Routine used to send a HID report to a certain endpoint.
        Feel free to overwrite this and hardcode the endpoint number.

        :param data:        Data to send
        :param endpoint:    Endpoint number
        '''
        self._owner.endpoints[endpoint].send(data)
