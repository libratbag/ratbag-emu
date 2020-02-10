# SPDX-License-Identifier: MIT

from ratbag_emu.hardware import LedComponent

from tests.test_device import TestDeviceBase


class TestHardware(TestDeviceBase):
    def test_led(self, device):
        device.hw['led1'] = LedComponent(state=True)
        assert device.hw['led1'].state

        device.hw['led1'].state = False
        assert not device.hw['led1'].state

        device.hw['led1'].state = True
        assert device.hw['led1'].state
