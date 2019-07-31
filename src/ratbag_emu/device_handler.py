from .protocol.util.descriptors import report_descriptor_simple, \
                                       report_descriptor_g_pro
from .protocol.hidpp20 import HIDPP20Device
from .protocol.steelseries import SteelseriesDevice


class DeviceHandler(object):
    devices = dict()
    next_id = 0

    @staticmethod
    def append_device(device):
        DeviceHandler.devices[DeviceHandler.next_id] = device
        DeviceHandler.next_id += 1

    @staticmethod
    def handle():
        name = 'Simple Device'

        DeviceHandler.append_device(HIDPP20Device(report_descriptor_simple,
                                                  (0x3, 0x0001, 0x0001), name))

        while True:
            for device_id, device in DeviceHandler.devices.copy().items():
                device.dispatch()
