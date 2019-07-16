from .protocol.descriptors import report_descriptor_simple, \
                                  report_descriptor_g_pro
from .protocol.base import MouseData
from .protocol.hidpp20 import HIDPP20Device
from .protocol.steelseries import SteelseriesDevice


class DeviceHandler(object):
    devices = []

    @staticmethod
    def handle():
        name = 'Simple Device'

        DeviceHandler.devices = [
            HIDPP20Device(report_descriptor_simple, (0x3, 0x0001, 0x0001), name)
        ]

        while True:
            for device in DeviceHandler.devices:
                device.dispatch()

    @staticmethod
    def add_device(shortname):
        if shortname == "steelseries-rival310":
            DeviceHandler.devices.append(SteelseriesDevice(report_descriptor_g_pro, (0x3, 0x01038, 0x1720), 'Steelseriesw Rival 310', 2))
        elif shortname == "logitech-g-pro":
            DeviceHandler.devices.append(HIDPP20Device(report_descriptor_g_pro, (0x3, 0x046d, 0xc4079), 'Logitech G Pro'))
        else:
            return None

        return True

    @staticmethod
    def get_openapi_devices():
        openapi_devices = dict()

        i = 0
        for device in DeviceHandler.devices:
            openapi_devices[i] = device.name
            i += 1

        return openapi_devices

    @staticmethod
    def get_openapi_device(device_id):
        if device_id > len(DeviceHandler.devices) - 1:
            return None

        return {device_id: DeviceHandler.devices[device_id].name}

    @staticmethod
    def create_event(device_id, event_data):
        if device_id > len(DeviceHandler.devices) - 1 or event_data is None:
            return None

        event = MouseData(DeviceHandler.devices[device_id])

        for data in event_data:
            for key, prop in data.items():
                setattr(event, key, prop)

        data = DeviceHandler.devices[device_id].create_report(event, 0x11)
        DeviceHandler.devices[device_id].send_raw(data)

        return True

