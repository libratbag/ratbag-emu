import struct

from hidtools.uhid import UHIDDevice


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

    polling_rate = 1000

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
                                        * self.dpi[self.active_dpi]))

        return super().create_report(data, type)


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
