# SPDX-License-Identifier: MIT

from ratbag_emu.hw_component import HWComponent


class LedComponent(HWComponent):
    '''
    Represents a simple led (on/off)
    '''
    def __init__(self, state: bool = True):
        super().__init__()
        self.state: bool = state
