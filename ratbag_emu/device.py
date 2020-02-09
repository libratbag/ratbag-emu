# SPDX-License-Identifier: MIT

import copy
import logging
import random
import sched
import time
import threading

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

    def __init__(self, name: str = 'Generic Device',
                 info: Tuple[int, int, int] = (0x03, 0x0001, 0x0001),
                 rdescs: List[List[int]] = [[
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
                     ]]):
        self.__logger = logging.getLogger('ratbag-emu.device')
        self._name = name
        self._info = info
        self._rdescs = rdescs

        # Find a unique ID for this device
        unique = False
        while not unique:
            self.id = self.generate_name()
            try:
                for id in self.device_list:
                    assert id != self.id
                unique = True
            except AssertionError:
                pass

        self.endpoints = []
        for i, r in enumerate(rdescs):
            self.endpoints.append(Endpoint(self, r, i))

        self.report_rate = 100
        self.fw = Firmware(self)
        self.hw: Dict[str, HWComponent] = {}
        self.actuators: List[Actuator] = []

    @classmethod
    def generate_name(cls) -> str:
        '''
        Generates a random name
        '''
        device_names = [
                'mara', 'capybara', 'porcupine', 'paca',
                'vole', 'woodrat', 'gerbil', 'shrew',
                'hutia', 'beaver', 'squirrel', 'chinchilla',
                'rabbit', 'viscacha', 'hare', 'degu',
                'gundi', 'acouchy', 'nutria', 'paca',
                'hamster', 'zokor', 'chipmunk', 'gopher',
                'marmot', 'groundhog', 'suslik', 'agouti',
                'blesmol',
        ]

        device_attr = [
                'sobbing', 'whooping', 'barking', 'yapping',
                'howling', 'squawking', 'cheering', 'warbling',
                'thundering', 'booming', 'blustering', 'humming',
                'crying', 'bawling', 'roaring', 'raging',
                'chanting', 'crooning', 'murmuring', 'bellowing',
                'wailing', 'weeping', 'screaming', 'yelling',
                'yodeling', 'singing', 'honking', 'hooting',
                'whispering', 'hollering',
        ]

        name = device_names[random.randint(0, len(device_names)-1)]
        attr = device_attr[random.randint(0, len(device_attr)-1)]
        return '-'.join([attr, name])

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return self._info

    @property
    def rdescs(self):
        return self._rdescs

    @property
    def actuators(self):
        return self._actuators

    @actuators.setter
    def actuators(self, val):
        # Make sure we don't have actuators which will act on the same keys
        seen = []
        for keys in [a.keys for a in val]:
            for el in keys:
                assert el not in seen
                seen.append(el)

        self._actuators = val

    def destroy(self):
        for endpoint in self.endpoints:
            endpoint.destroy()

    def transform_action(self, data: Dict[str, Any]):
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

    def send_hid_action(self, action: object):
        '''
        Sends a HID action

        We assume there's only one endpoint for each type of action (mouse,
        keyboard, button, etc.) so we send the action to all endpoints. The
        endpoint will only act on the action if it supports it.

        :param action:  HID action
        '''
        for endpoint in self.endpoints:
            endpoint.send(endpoint.create_report(action))

    def _simulate_action_xy(self, action: Dict[str, Any], packets: Dict[int, EventData], report_count: int):
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

        i = 0
        while real_dot_buffer['x'] != 0:
            if i not in packets:
                packets[i] = EventData()

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
                    setattr(packets[i], attr, diff)
                    real_dot_buffer[attr] -= diff
            i += 1

    def _simulate_action_button(self, action: Dict[str, Any], packets: Dict[int, EventData], report_count: int):
        for i in range(report_count):
            if i not in packets:
                packets[i] = EventData()

            setattr(packets[i], 'b{}'.format(action['data']['id']), 1)

    def simulate_action(self, action: Dict[str, Any], type: int = None):
        '''
        Simulates action

        Translates physical values according to the device properties and
        converts action into HID reports.

        :param action:  high-level action
        :param type:    HID report type
        '''

        packets: Dict[int, EventData] = {}

        report_count = int(round(ms2s(action['duration']) * self.report_rate))

        if not report_count:
            report_count = 1

        if action['type'] == ActionType.XY:
            self._simulate_action_xy(action, packets, report_count)
        elif action['type'] == ActionType.BUTTON:
            self._simulate_action_xy(action, packets, report_count)

        def send_packets():
            nonlocal packets
            s = sched.scheduler(time.time, time.sleep)
            next_time = 0
            for i in range(len(packets)):
                s.enter(next_time, 1, self.send_hid_action,
                        kwargs={'action': packets[i]})
                next_time += 1 / self.report_rate
            s.run()

        sim_thread = threading.Thread(target=send_packets)
        sim_thread.start()
