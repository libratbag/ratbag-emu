# SPDX-License-Identifier: MIT

import random

import pyudev
import pytest

from ratbag_emu import Device
from ratbag_emu.actuators import SensorActuator
from ratbag_emu.util import ActionType, EventData

from tests import TestBase


class TestDeviceBase(TestBase):
    name = 'Test Device'
    vid = pid = 0x9999
    info = (3, vid, pid)
    rdescs = [[
        # Generic mouse report descriptor
        0x05, 0x01,  # .Usage Page (Generic Desktop)        0
        0x09, 0x02,  # .Usage (Mouse)                       2
        0xa1, 0x01,  # .Collection (Application)            4
        0x09, 0x02,  # ..Usage (Mouse)                      6
        0xa1, 0x02,  # ..Collection (Logical)               8
        0x09, 0x01,  # ...Usage (Pointer)                   10
        0xa1, 0x00,  # ...Collection (Physical)             12
        0x05, 0x09,  # ....Usage Page (Button)              14
        0x19, 0x01,  # ....Usage Minimum (1)                16
        0x29, 0x03,  # ....Usage Maximum (3)                18
        0x15, 0x00,  # ....Logical Minimum (0)              20
        0x25, 0x01,  # ....Logical Maximum (1)              22
        0x75, 0x01,  # ....Report Size (1)                  24
        0x95, 0x03,  # ....Report Count (3)                 26
        0x81, 0x02,  # ....Input (Data,Var,Abs)             28
        0x75, 0x05,  # ....Report Size (5)                  30
        0x95, 0x01,  # ....Report Count (1)                 32
        0x81, 0x03,  # ....Input (Cnst,Var,Abs)             34
        0x05, 0x01,  # ....Usage Page (Generic Desktop)     36
        0x09, 0x30,  # ....Usage (X)                        38
        0x09, 0x31,  # ....Usage (Y)                        40
        0x15, 0x81,  # ....Logical Minimum (-127)           42
        0x25, 0x7f,  # ....Logical Maximum (127)            44
        0x75, 0x08,  # ....Report Size (8)                  46
        0x95, 0x02,  # ....Report Count (2)                 48
        0x81, 0x06,  # ....Input (Data,Var,Rel)             50
        0xc0,        # ...End Collection                    52
        0xc0,        # ..End Collection                     53
        0xc0,        # .End Collection                      54
    ]]

    @pytest.fixture()
    def device(self):
        d = Device(name=self.name, info=self.info, rdescs=self.rdescs)

        yield d

        d.destroy()


class TestDevice(TestDeviceBase):
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
                SensorActuator(dpi=1000),
                SensorActuator(dpi=1000)
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

        received = self.catch_evdev_events(device, events, callback)

        assert expected.x <= received.x <= expected.x
        assert expected.y <= received.y <= expected.y

    def test_movement(self, device, events):
        '''
        Test normal mouse movement
        '''
        dpi = 1000

        device.actuators += [
            SensorActuator(dpi)
        ]

        action = {
            'type': ActionType.XY,
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
            SensorActuator(dpi=1000)
        ]

        action = {
            'type': ActionType.XY,
            'duration': 1,
            'data': {
                'x': 5,
                'y': 5
            }
        }

        with pytest.raises(AssertionError):
            self.simulate(device, events, action)

    def test_duplicated_id(self):
        random.seed(0)
        device1 = Device(name='Test Device 1', info=self.info, rdescs=self.rdescs)

        random.seed(0)
        device2 = Device(name='Test Device 2', info=self.info, rdescs=self.rdescs)

        assert device1.id != device2.id

        device1.destroy()
        device2.destroy()
