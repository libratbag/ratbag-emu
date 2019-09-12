import copy
import sched
import struct
import os
import threading
import time

from hidtools.uhid import UHIDDevice

from ratbag_emu.util import AbsInt, MM_TO_INCH
from ratbag_emu.protocol.util.profile import Profile


class Endpoint(UHIDDevice):
    verbose = True

    def __init__(self, owner, rdesc):
        try:
            super().__init__()
        except PermissionError:
            print('Error: Not enough permissions to create UHID devices')
            os._exit(1)

        self._owner = owner

        self._info = owner.info
        self.rdesc = rdesc

        id = ''
        if owner.id is not None:
            id = f'#{owner.id} '

        self.name = f'ratbag-emu test device {id}({owner.name}, {hex(self.vid)}:{hex(self.pid)})'

        self.hw_settings = None

        self._output_report = self._protocol_receive

        self.create_kernel_device()
        self.start(None)

    def log(self, msg):
        '''
        Logs message to the console

        Prints target message as well as the timestamp
        '''
        if Endpoint.verbose:
            print('{:20}{}'.format(f'{time.time()}:', msg))

    def _protocol_receive(self, data, size, rtype):
        '''
        Output report callback

        Is called when we receive a report. Logs the buffer to the console and calls
        our own callback named protocol_receive().

        Classes built on top of BaseDevice should implement a protocol_receive()
        function to be used as callback. They are not supposed to change
        _output_report.
        '''
        data = [struct.unpack(">H", b'\x00' + data[i:i+1])[0]
                for i in range(0, size)]

        if size > 0:
            self.log('read ' + ''.join(f' {byte:02x}' for byte in data))

        self._owner.protocol_receive(data, size, rtype)

    def _send_raw(self, data):
        '''
        Internal routine used to send raw output reports

        Logs the buffer to the console and send the packet trhough UHID
        '''
        if not data:
            return

        self.log('write' + ''.join(f' {byte:02x}' for byte in data))

        self.call_input_event(data)

    def send_raw(self, data):
        '''
        Routine used to send raw output reports
        '''
        self._send_raw(data)

    def create_report(self, data, type=None):
        '''
        Create report routine

        We overwrite super's behavior to ignore empty reports
        '''
        empty = True
        for attr in data.__dict__:
            if getattr(data, attr):
                empty = False
                break

        if empty:
            return

        return super().create_report(data, type)

    def simulate_action(self, actions):
        '''
        Simulates user actions
        '''
        packets = {}
        duration = 0

        for action in actions:
            start_report = int(action['start'] / 1000 * self.hw_settings.get_report_rate())
            end_report = int(action['end'] / 1000 * self.hw_settings.get_report_rate())
            report_count = end_report - start_report

            if report_count == 0:
                continue

            if action['end'] > duration:
                duration = action['end']

            # XY movement
            if action['action']['type'] == 'xy':
                # We assume a straight movement
                pixel_buffer = {}
                step = {}

                '''
                Initialize pixel_buffer, real_pixel_buffer and step for X and Y

                pixel_buffer holds the ammount of pixels left to send (kinda,
                read bellow).

                We actually have two variables for this, real_pixel_buffer and
                pixel_buffer. pixel_buffer mimics the user movement and
                real_pixel_buffer holds true number of pixels left to send.
                When using high report rates (ex. 1000Hz) we usually don't
                have a full pixel to send, that's why we need two variables. We
                subtract the step to pixel_buffer at each iteration, when the
                difference between pixel_buffer and real_pixel_buffer is equal
                or higher than 1 pixel we then send a HID report to the device
                with that difference (int! we send the int part of the
                difference) and update real_pixel_buffer to include this
                changes.
                '''
                for attr in ['x', 'y']:
                    # move_value * inch_to_mm * active_dpi
                    pixel_buffer[attr] = AbsInt((action['action'][attr] *
                                         MM_TO_INCH *
                                         self.hw_settings.get_dpi_value()))
                    step[attr] = pixel_buffer[attr] / report_count
                real_pixel_buffer = copy.deepcopy(pixel_buffer)

                for i in range(start_report, end_report):
                    if i not in packets:
                        packets[i] = MouseData()

                    for attr in ['x', 'y']:
                        pixel_buffer[attr] -= step[attr]
                        diff = real_pixel_buffer[attr] - pixel_buffer[attr]
                        '''
                        The max is 127, if this happens we need to leave the
                        excess in the buffer for it to be sent in the next
                        report
                        '''
                        if abs(diff) >= 1:
                            if abs(diff) > 127:
                                diff = 127 if diff > 0 else -127
                            setattr(packets[i], attr, int(diff))
                            real_pixel_buffer[attr] -= int(diff)

            # Button
            elif action['action']['type'] == 'button':
                for i in range(start_report, end_report):
                    if i not in packets:
                        packets[i] = MouseData()

                    setattr(packets[i], f"b{action['action']['id']}", 1)

        sim_thread = threading.Thread(target=self._send_packets,
                args=(packets, int(duration / 1000 * self.hw_settings.get_report_rate())))
        sim_thread.start()

    def _send_packets(self, packets, total):
        '''
        Helper function: Send packets
        '''
       s = sched.scheduler(time.time, time.sleep)
        next_time = 0
        for i in range(total):
            s.enter(next_time, 1, self.send_raw,
                    kwargs={'data': self.create_report(packets[i], 0x11)})
            next_time += 1 / self.hw_settings.get_report_rate()
        s.run()

    @property
    def info(self):
        return self._owner.info

    @property
    def shortname(self):
        return self._owner.shortname


class BaseDevice(object):

    def __init__(self, hw_settings={}, name='Generic Device',
        info=(0x03, 0x0001, 0x0001), rdescs=[
            [
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
            ]
        ], shortname='custom-generic-device', id=None):
        self.name = name
        self.shortname = shortname
        self.info = info
        self.rdescs = rdescs
        self.id = id

        self.endpoints = []

        for r in rdescs:
            self.endpoints.append(Endpoint(self, r))

        self.hw_settings = Profile(hw_settings)

        # Fill missing endpoints, we default to 0
        for attr in ['mouse_endpoint', 'keyboard_endpoint', 'media_endpoint']:
            if not hasattr(self, attr):
                setattr(self, attr, 0)

    def protocol_receive(self, data, size, rtype):
        '''
        Callback called upon receiving output reports from the kernel

        Dummy protocol receiver implementation.
        '''
        return

    def create_report(self, data, type=None):
        '''
        Pass to the correct endpoint
        '''
        self.endpoints[self.mouse_endpoint].create_report(data, type)

    def simulate_action(self, actions):
        self.endpoints[self.mouse_endpoint].simulate_action(actions)

    def send_raw(self, data):
        self.endpoints[self.mouse_endpoint].send_raw(data)

    def dispatch(self):
        for endpoint in self.endpoints:
            endpoint.dispatch()

    def destroy(self):
        for endpoint in self.endpoints:
            endpoint.destroy()

    @property
    def device_nodes(self):
        nodes = []
        for endpoint in self.endpoints:
            nodes += endpoint.device_nodes
        return nodes

    @property
    def hw_settings(self):
        return self._hw_settings

    @hw_settings.setter
    def hw_settings(self, value):
        self._hw_settings = value
        if hasattr(self, 'endpoints'):
            for endpoint in self.endpoints:
                endpoint.hw_settings = value


class MouseData(object):
    '''
    Holds event data
    '''

    def __init__(self):
        self.x = 0
        self.y = 0
