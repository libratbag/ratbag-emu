# SPDX-License-Identifier: MIT

from enum import Enum
from typing import Any, Dict, Union


def mm2inch(mm: Union[int, float]) -> float:
    return mm * 0.0393700787


def ms2s(ms: Union[int, float]) -> float:
    return ms / 1000.0


class EventData(object):
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    @staticmethod
    def from_mm(dpi: int,
                x: Union[int, float] = 0,
                y: Union[int, float] = 0) -> 'EventData':
        return EventData(x=int(round(mm2inch(x) * dpi)),
                         y=int(round(mm2inch(y) * dpi)))

    @staticmethod
    def from_action(dpi: int, action: Dict[str, Any]) -> 'EventData':
        assert action['type'] == ActionType.XY
        return EventData(x=int(round(mm2inch(action['data']['x']) * dpi)),
                         y=int(round(mm2inch(action['data']['y']) * dpi)))


class ActionType(Enum):
    XY = 1
    BUTTON = 2
