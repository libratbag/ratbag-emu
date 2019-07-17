from .protocol.descriptors import report_descriptor_simple, \
                                  report_descriptor_g_pro
from .protocol.base import MouseData
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

    @staticmethod
    def add_device(shortname):
        if shortname == "steelseries-rival310":
            DeviceHandler.append_device(SteelseriesDevice(
                report_descriptor_g_pro, (0x3, 0x01038, 0x1720),
                'Steelseriesw Rival 310', shortname, 2))
        elif shortname == "logitech-g-pro":
            DeviceHandler.append_device(HIDPP20Device(
                report_descriptor_g_pro, (0x3, 0x046d, 0xc4079),
                'Logitech G Pro', shortname))
        else:
            return None

        return True

    @staticmethod
    def get_openapi_devices():
        openapi_devices = []

        for device_id, device in DeviceHandler.devices.items():
            if device is None:
                continue

            openapi_devices.append({
                'id':           device_id,
                'name':         device.name,
                'shortname':    device.shortname
            })

        return openapi_devices

    @staticmethod
    def get_openapi_device(device_id):
        if device_id > len(DeviceHandler.devices) - 1:
            return None

        return {
                'id':           device_id,
                'name':         DeviceHandler.devices[device_id].name,
                'shortname':    DeviceHandler.devices[device_id].shortname
            }

    @staticmethod
    def delete_device(device_id):
        if device_id > len(DeviceHandler.devices) - 1:
            return False

        DeviceHandler.devices[device_id] = None

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

