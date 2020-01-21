# SPDX-License-Identifier: MIT

from ratbag_emu.actuators import SensorActuator
from ratbag_emu.util import mm2inch

from tests.test_device import TestDeviceBase


class TestSensorActuator(TestDeviceBase):
    def test_transform(self):
        dpi = 1000

        actuator = SensorActuator(None, dpi)

        data = {
            'x': 5,
            'y': 3
        }

        hid_data = actuator.transform(data)

        assert hid_data['x'] == int(round(mm2inch(data['x']) * dpi))
        assert hid_data['y'] == int(round(mm2inch(data['y']) * dpi))
