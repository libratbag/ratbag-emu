# SPDX-License-Identifier: MIT

import logging
import struct
import time
import typing

import hidtools.uhid

from typing import List, Optional

if typing.TYPE_CHECKING:
    from ratbag_emu.device import Device  # pragma: no cover


class Endpoint(hidtools.uhid.UHIDDevice):  # type: ignore
    '''
    Represents a device endpoint

    A HID device is created for each endpoint. The enpoint can be used to
    receive and send data

    :param owner:   Endpoint owner
    :param rdesc:   Report descriptor
    :param number:  Endpoint number
    '''

    def __init__(self, owner: 'Device', rdesc: List[int], number: int):
        super().__init__()

        self.__logger = logging.getLogger('ratbag-emu.endpoint')

        self._owner = owner

        self._info = owner.info
        self.rdesc = rdesc
        self.number = number
        self.name = f'ratbag-emu {owner.name} ({self.vid:04x}:{self.pid:04x}, {self.number})'

        self._output_report = self._receive

        self.create_kernel_device()

        end = time.time() + 5
        while (not self.uhid_dev_is_ready or not self.device_nodes or not self.hidraw_nodes) and time.time() <= end:
            self.dispatch(10)  # pragma: no cover

        self.__logger.debug(f'created endpoint {self.number} ({self.name})')

    @property
    def uhid_dev_is_ready(self) -> bool:
        return self.udev_device is not None

    def _receive(self, data: List[int], size: int, rtype: int) -> None:
        '''
        Receive data

        Callback called when we receive a HID report.
        Triggers the firmware's callback.

        :param data:    Received data
        :param size:    Received data size
        :param rtype:   Report type
        '''
        data = [struct.unpack('>H', b'\x00' + data[i:i + 1])[0]  # type: ignore
                for i in range(0, size)]

        if size > 0:
            self.logger.debug('read  {}'.format(' '.join(f' {byte:02x}' for byte in data)))

        self._owner.fw.hid_receive(data, size, rtype, self.number)

    def send(self, data: List[int]) -> None:
        '''
        Send data

        Routine used to send a HID report.

        :param data:    Data to send
        '''
        if not data:
            return

        self.__logger.debug('write {}'.format(' '.join(f'{byte:02x}' for byte in data)))

        self.call_input_event(data)

    def create_report(self, action: object, global_data: Optional[int] = None, skip_empty: bool = True) -> List[int]:
        '''
        Converts action into HID report

        Converts action in HID report according to the report descriptor and
        sends it.

        :param action:      Object holding the desired actions as attributes
        :param global_data: ?
        :param skip_empty:  Enables skipping empty actions
        '''
        empty = True
        for attr in action.__dict__:
            if getattr(action, attr):
                empty = False
                break

        if empty and skip_empty:
            return []

        return super().create_report(action, global_data)  # type: ignore
