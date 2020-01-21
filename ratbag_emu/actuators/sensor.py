# SPDX-License-Identifier: MIT

from ratbag_emu.actuator import Actuator
from ratbag_emu.util import mm2inch


class SensorActuator(Actuator):
    '''
    Represents the sensor/dpi actuator

    Transform x and y values based on the DPI value.
    '''
    def __init__(self, owner, dpi):
        super().__init__(owner)
        self._keys = ['x', 'y']
        self.dpi = dpi

    def transform(self, action):
        hid_action = action.copy()

        for key in self._keys:
            if key in hid_action:
                hid_action[key] = int(round(mm2inch(action[key]) * self.dpi))
        return hid_action
