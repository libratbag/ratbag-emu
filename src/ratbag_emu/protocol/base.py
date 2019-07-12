import struct

from hidtools.uhid import UHIDDevice


class BaseDevice(UHIDDevice):

    _protocol = None
    _buttons = []

    def __init__(self, rdesc=None, info=None, name='Generic Device'):
        super().__init__()
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

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, value):
        self._buttons = value


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
