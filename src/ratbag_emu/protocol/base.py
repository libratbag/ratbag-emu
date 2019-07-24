import copy
import struct
import os
import threading
import time

from hidtools.uhid import UHIDDevice

from ratbag_emu.util import AbsInt


class BaseDevice(UHIDDevice):
    '''
    Represents an hardware device
    '''

    protocol = None

    '''
    Hardware properties
    '''
    buttons = []

    active_dpi = 0
    dpi = [
        3000,
        6000
    ]
    step = 100

    report_rate = 1000  # Hz

    leds = [
        [0xff, 0xff, 0xff],
        [0xff, 0xff, 0xff]
    ]

    profiles = []

    '''
    Init procedure

    Initializes the device attributes and creates the UHID device
    '''
    def __init__(self, rdesc=None, info=None, name='Generic Device',
                 shortname='generic'):
        try:
            super().__init__()
        except PermissionError:
            print('!!! Not enough permissions to create UHID devices. Bailling out. !!!')
            exit(1)
        self.info = info
        self.rdesc = rdesc
        self.name = 'Test {} ({}:{})'.format(name, hex(self.vid), hex(self.pid))
        self.shortname = shortname

        self._output_report = self._protocol_receive

        self.create_kernel_device()
        self.start(None)

    '''
    Output report callback

    Is called when we receive a report. Logs the buffer to the console and calls
    our own callback named protocol_receive().

    Classes built on top of BaseDevice should implement a protocol_receive()
    function to be used as callback. They are not supposed to change
    _output_report.
    '''
    def _protocol_receive(self, data, size, rtype):
        data = [struct.unpack(">H", b'\x00' + data[i:i+1])[0]
                for i in range(0, size)]

        if size > 0:
            print('read ' + ''.join(' {:02x}'.format(byte) for byte in data))

        self.protocol_receive(data, size, rtype)

    '''
    Callback called upon receiving output reports from the kernel

    Dummy protocol receiver implementation.
    '''
    def protocol_receive(self, data, size, rtype):
        return

    '''
    Internal routine used to send raw output reports

    Logs the buffer to the console and send the packet trhough UHID
    '''
    def _send_raw(self, data):
        print('write' + ''.join(' {:02x}'.format(byte) for byte in data))

        self.call_input_event(data)

    '''
    Routine used to send raw output reports
    '''
    def send_raw(self, data):
        self._send_raw(data)

    '''
    Routine used to send event output reports

    Translates the received x and y values to pixels based on the internal
    device DPI property
    '''
    def create_report(self, data, type):
        # Translate mm to pixel
        for attr in ["x", "y"]:
            if hasattr(data, attr):
                setattr(data, attr, int(int(getattr(data, attr)) * 0.0393700787
                                        * self.get_dpi()))

        return super().create_report(data, type)

    '''
    Simulates user actions
    '''
    def simulate_action(self, actions):
        packets = {}
        duration = 0

        #self.report_rate = 100

        print('Start contructing packets...')
        for action in actions:
            start_report = int(action['start'] * self.report_rate)
            end_report = int(action['end'] * self.report_rate)
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
                pixel_buffer. pixel_buffer mimmics the user movement and
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
                                         0.0393700787 * self.get_dpi()))
                    step[attr] = pixel_buffer[attr] / report_count
                real_pixel_buffer = copy.deepcopy(pixel_buffer)

                for i in range(start_report, end_report):
                    if i not in packets:
                        packets[i] = MouseData(self)

                    for attr in ['x', 'y']:
                        pixel_buffer[attr] -= step[attr]
                        diff = real_pixel_buffer[attr] - pixel_buffer[attr]
                        '''
                        The max is 127, if this happens we need to leave the
                        excess in the buffer for it to be sent next in the
                        next report
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
                        packets[i] = MouseData(self)

                    setattr(packets[i], 'b{}'.format(action['action']['id']), 1)

        sim_thread = threading.Thread(target=self._send_packets,
                                    args=(packets, duration * self.report_rate))
        sim_thread.start()
        #self._send_packets(packets, duration * self.report_rate)

    '''
    Helper function: Send packets
    '''
    def _send_packets(self, packets, total):
        print('Start sending packets...')
        for i in range(total):
            # We don't send empty reports
            if i not in packets:
                continue
            empty = True
            for attr in packets[i].__dict__:
                if getattr(packets[i], attr) != 0 or \
                   getattr(packets[i], attr) != None:
                    empty = False
                    break
            if empty:
                return

            if packets[i].x != 0 and packets[i].y != 0:
                self.send_raw([0x00, packets[i].x, packets[i].y])
                #self.send_raw(self.create_report(packets[i], 0x11))
            #time.sleep(1 / self.report_rate)


    '''
    Gets the active DPI value
    '''
    def get_dpi(self):
        return self.dpi[self.active_dpi]



class MouseData(object):
    '''
    Holds event data
    '''

    def __init__(self, device):
        i = 1
        for button in device.buttons:
            setattr(self, 'b{}'.format(i), button)
            i += 1

        self.x = 0
        self.y = 0
        self.wheel = 0
        self.acpan = 0
