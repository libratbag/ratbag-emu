# SPDX-License-Identifier: MIT


def mm2inch(mm):
    return mm * 0.0393700787


def ms2s(ms):
    return ms / 1000.0


class EventData(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @staticmethod
    def from_mm(dpi, x=0, y=0):
        return EventData(x=int(mm2inch(x) * dpi),
                         y=int(mm2inch(y) * dpi))

    @staticmethod
    def from_action(dpi, action: dict):
        assert action['type'] == 'xy'
        return EventData(x=int(mm2inch(action['data']['x']) * dpi),
                         y=int(mm2inch(action['data']['y']) * dpi))
