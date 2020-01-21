# SPDX-License-Identifier: MIT

import pyudev
import pytest

from ratbag_emu import Device
from ratbag_emu.actuators import SensorActuator
from ratbag_emu.util import EventData

from tests import TestBase


class TestDevice(TestBase):
    name = 'Test Device'
    vid = pid = 0x9999

    @pytest.fixture()
    def device(self):
        d = Device(name=self.name, info=(3, self.vid, self.pid))

        yield d

        d.destroy()

    def test_create(self, device):
        '''
        Make sure the correct device is created
        '''
        name = f'ratbag-emu {device.id} ({self.name}, {self.vid:04x}:' \
               f'{self.pid:04x}, 0)'
        assert list(pyudev.Context().list_devices(subsystem='hid',
                                                  HID_NAME=name))

    def test_duplicated_actuators(self, device):
        '''
        Make sure we raise an error on actuators that operate on the same keys
        '''
        with pytest.raises(AssertionError):
            device.actuators += [
                SensorActuator(device, dpi=1000),
                SensorActuator(device, dpi=1000)
            ]

    def test_mouse_report(self, device, events):
        '''
        Test single HID report
        '''
        x = y = 5

        expected = EventData(x, y)

        def callback(device):
            nonlocal expected
            device.send_hid_action(expected)

        received = self.catch_events(device, events, callback)

        assert expected.x <= received.x <= expected.x
        assert expected.y <= received.y <= expected.y

    def test_movement(self, device, events):
        '''
        Test normal mouse movement
        '''
        dpi = 1000

        device.actuators += [
            SensorActuator(device, dpi)
        ]

        action = {
            'type': 'xy',
            'duration': 500,
            'data': {
                'x': 5,
                'y': 5
            }
        }

        received = self.simulate(device, events, action)

        expected = EventData.from_action(dpi, action)

        assert received.x == expected.x
        assert received.y == expected.y

    def test_movement_max(self, device, events):
        '''
        Make sure we raise an error when we try to move more than possible
        '''
        device.report_rate = 1000
        device.actuators += [
            SensorActuator(device, dpi=1000)
        ]

        action = {
            'type': 'xy',
            'duration': 1,
            'data': {
                'x': 5,
                'y': 5
            }
        }

        with pytest.raises(AssertionError):
            self.simulate(device, events, action)
