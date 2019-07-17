import struct

from hidtools.uhid import UHIDDevice


class BaseDevice(UHIDDevice):

    protocol = None

    '''
    Hardware properties
    '''
    buttons = []

    active_dpi = 2
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

    def __init__(self, rdesc=None, info=None, name='Generic Device'):
        try:
            super().__init__()
        except PermissionError:
            print('!!! Not enough permissions to create UHID devices. Bailing out. !!!')
            exit(1)
        self.info = info
        self.rdesc = rdesc
        self.name = 'Test {} ({}:{})'.format(name,
                                             hex(self.vid),
                                             hex(self.pid))

        self._output_report = self._protocol_receive

        self.create_kernel_device()
        self.start(None)

    def _protocol_receive(self, data, size, rtype):
        data = [struct.unpack(">H", b'\x00' + data[i:i+1])[0]
                for i in range(0, size)]

        if size > 0:
            print('read ' + ''.join(' {:02x}'.format(byte) for byte in data))

        self.protocol_receive(data, size, rtype)

    def protocol_receive(self, data, size, rtype):
        return

    def _send_raw(self, data):
        print('write' + ''.join(' {:02x}'.format(byte) for byte in data))

        self.call_input_event(data)

    def protocol_send(self, data):
        self._send_raw(data)

    def send_raw(self, data):
        self._send_raw(data)

    def create_report(self, data, type):
        # Translate mm to pixel
        for attr in ["x", "y"]:
            if hasattr(data, attr):
                setattr(data, attr,
                        int(getattr(data, attr) * 0.0393700787 * self._dpi))

        return super().create_report(data, type)


class MouseData(object):
    def __init__(self, device):
        i = 1
        for button in device.buttons:
            setattr(self, 'b{}'.format(i), button)
            i += 1

        self.x = 0
        self.y = 0
        self.wheel = 0
        self.acpan = 0
