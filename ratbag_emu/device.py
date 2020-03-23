# SPDX-License-Identifier: MIT

import copy
import logging
import sched
import time

from typing import Any, ClassVar, Dict, List, Tuple

from ratbag_emu.actuator import Actuator
from ratbag_emu.endpoint import Endpoint
from ratbag_emu.firmware import Firmware
from ratbag_emu.hw_component import HWComponent
from ratbag_emu.util import ActionType, EventData, ms2s


class Device(object):
    '''
    Represents a real device

    :param name:    Device name
    :param info:    Bus information (bus, vid, pid)
    :param rdescs:  Array of report descriptors
    '''
    device_list: ClassVar[List[str]] = []

    def __init__(self, name: str, info: Tuple[int, int, int],
                 rdescs: List[List[int]]):
        self.__logger = logging.getLogger('ratbag-emu.device')
        self._name = name
        self._info = info
        self._rdescs = rdescs

        self.endpoints = []
        for i, r in enumerate(rdescs):
            self.endpoints.append(Endpoint(self, r, i))

        self.report_rate = 100
        self.fw = Firmware(self)
        self.hw: Dict[str, HWComponent] = {}
        self.actuators: List[Actuator] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def info(self) -> Tuple[int, int, int]:
        return self._info

    @property
    def event_nodes(self) -> List[str]:
        return [node for endpoint in self.endpoints for node in endpoint.device_nodes]

    @property
    def hidraw_nodes(self) -> List[str]:
        return [node for endpoint in self.endpoints for node in endpoint.hidraw_nodes]

    @property
    def rdescs(self) -> List[List[int]]:
        return self._rdescs

    @property
    def actuators(self) -> List[Actuator]:
        return self._actuators

    @actuators.setter
    def actuators(self, val: List[Actuator]) -> None:
        # Make sure we don't have actuators which will act on the same keys
        seen: List[str] = []
        for keys in [a.keys for a in val]:
            for el in keys:
                assert el not in seen
                seen.append(el)

        self._actuators = val

    def destroy(self) -> None:
        for endpoint in self.endpoints:
            endpoint.destroy()

    def transform_action(self, data: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Transforms high-level action according to the actuators

        A high-level action will have the x, y values in mm. This values will
        be converted to dots by the device actuators (in this case, the
        sensor/dpi actuator)

        :param action:  high-level action
        '''
        hid_data: Dict[str, Any] = {}

        for actuator in self.actuators:
            hid_data.update(actuator.transform(data.copy()))

        return hid_data

    def send_hid_action(self, action: object) -> None:
        '''
        Sends a HID action

        We assume there's only one endpoint for each type of action (mouse,
        keyboard, button, etc.) so we send the action to all endpoints. The
        endpoint will only act on the action if it supports it.

        :param action:  HID action
        '''
        for endpoint in self.endpoints:
            endpoint.send(endpoint.create_report(action))

    def _simulate_action_xy(self, action: Dict[str, Any], packets: List[EventData], report_count: int) -> None:
        # FIXME: Read max size from the report descriptor
        axis_max = 127
        axis_min = -127

        # We assume a linear motion
        dot_buffer = {}
        step = {}

        '''
        Initialize dot_buffer, real_dot_buffer and step for X and Y

        dot_buffer holds the ammount of dots left to send (kinda,
        read below).

        We actually have two variables for this, real_dot_buffer and
        dot_buffer. dot_buffer mimics the user movement and
        real_dot_buffer holds true number of dots left to send.
        When using high report rates (ex. 1000Hz) we usually don't
        have a full dot to send, that's why we need two variables. We
        subtract the step to dot_buffer at each iteration, when the
        difference between dot_buffer and real_dot_buffer is equal
        or higher than 1 dot we then send a HID report to the device
        with that difference (int! we send the int part of the
        difference) and update real_dot_buffer to include this
        changes.
        '''
        dot_buffer = self.transform_action(action['data'])

        for attr in ['x', 'y']:
            assert dot_buffer[attr] <= axis_max * report_count
            step[attr] = dot_buffer[attr] / report_count

        real_dot_buffer = copy.deepcopy(dot_buffer)

        for packet in packets:
            if not real_dot_buffer['x']:
                break

            for attr in ['x', 'y']:
                dot_buffer[attr] -= step[attr]
                diff = int(round(real_dot_buffer[attr] - dot_buffer[attr]))
                '''
                The max is 127, if this happens we need to leave the
                excess in the buffer for it to be sent in the next
                report
                '''
                if abs(diff) >= 1:
                    if abs(diff) > axis_max:
                        diff = axis_max if diff > 0 else axis_min
                    setattr(packet, attr, diff)
                    real_dot_buffer[attr] -= diff

    def _simulate_action_button(self, action: Dict[str, Any], packets: List[EventData]) -> None:
        for packet in packets:
            setattr(packet, 'b{}'.format(action['data']['id']), 1)

    def simulate_action(self, action: Dict[str, Any]) -> None:
        '''
        Simulates action

        Translates physical values according to the device properties and
        converts action into HID reports.

        :param action:  high-level action
        :param type:    HID report type
        '''

        packets: List[EventData] = []

        report_count = int(round(ms2s(action['duration']) * self.report_rate))

        if not report_count:
            report_count = 1

        for i in range(report_count):
            packets.append(EventData())

        if action['type'] == ActionType.XY:
            self._simulate_action_xy(action, packets, report_count)
        elif action['type'] == ActionType.BUTTON:
            self._simulate_action_xy(action, packets, report_count)

        s = sched.scheduler(time.time, time.sleep)
        next_time = 0.0
        for packet in packets:
            s.enter(next_time, 1, self.send_hid_action,
                    kwargs={'action': packet})
            next_time += 1 / self.report_rate
        s.run()
