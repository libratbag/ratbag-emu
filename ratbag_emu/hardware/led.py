# SPDX-License-Identifier: MIT

from ratbag_emu.hw_component import HWComponent


class LedComponent(HWComponent):
    '''
    Represents a simple led (on/off)
    '''
    def __init__(self, owner, state=True):
        super().__init__(owner)
        self.state: bool = state
