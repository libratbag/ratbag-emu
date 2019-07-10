import struct

from hidtools.uhid import UHIDDevice

class BaseDevice(UHIDDevice):

    _protocol = None

    def __init__(self, rdesc=None, info=None, name='Generic Device'):
        super().__init__()
        self.info = info
        self.rdesc = rdesc
        self.name = 'Test {} ({}:{})'.format(name,
                                                    hex(self.vid),
                                                    hex(self.pid))

        self._output_report = self._protocol_receive

    def _protocol_receive(self, data, size, rtype):
        data = [struct.unpack(">H", b'\x00' + data[i:i+1])[0]
                for i in range(0, size)]

        if size > 0:
            print('read ' + ''.join(' {:02x}'.format(byte) for byte in data))

        self.protocol_receive(data, size, rtype)

    def protocol_receive(self, data, size, rtype):
        return

    def _protocol_send(self, data):
        print('write' + ''.join(' {:02x}'.format(byte) for byte in data))

        self.call_input_event(data)

    def protocol_send(self, data):
        self._protocol_send(data)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value
