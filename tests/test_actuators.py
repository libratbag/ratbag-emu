# SPDX-License-Identifier: MIT

from ratbag_emu.actuators import SensorActuator

from tests.test_device import TestDeviceBase


class TestSensorActuator(TestDeviceBase):
    def test_transform(self):
        dpi = 1000

        actuator = SensorActuator(dpi)

        data = {
            'x': 5,
            'y': 3
        }

        hid_data = actuator.transform(data)

        assert hid_data['x'] == 197
        assert hid_data['y'] == 118
