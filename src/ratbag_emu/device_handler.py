from ratbag_emu_server.models.device import Device

from .protocol.base import MouseData
from .protocol.hidpp20 import HIDPP20Device
from .protocol.steelseries import SteelseriesDevice


class DeviceHandler(object):
    devices = []

    @staticmethod
    def handle():
        report_descriptor = [
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
        name = 'Simple Device'

        DeviceHandler.devices = [
            HIDPP20Device(report_descriptor, (0x3, 0x0001, 0x0001), name)
        ]

        while True:
            for device in DeviceHandler.devices:
                device.dispatch()

    @staticmethod
    def add_device(shortname):
        report_descriptor = [
            0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  0
            0x09, 0x01,                    # Usage (Vendor Usage 1)              3
            0xa1, 0x01,                    # Collection (Application)            5
            0x85, 0x10,                    #  Report ID (16)                     7
            0x75, 0x08,                    #  Report Size (8)                    9
            0x95, 0x06,                    #  Report Count (6)                   11
            0x15, 0x00,                    #  Logical Minimum (0)                13
            0x26, 0xff, 0x00,              #  Logical Maximum (255)              15
            0x09, 0x01,                    #  Usage (Vendor Usage 1)             18
            0x81, 0x00,                    #  Input (Data,Arr,Abs)               20
            0x09, 0x01,                    #  Usage (Vendor Usage 1)             22
            0x91, 0x00,                    #  Output (Data,Arr,Abs)              24
            0xc0,                          # End Collection                      26
            0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  27
            0x09, 0x02,                    # Usage (Vendor Usage 2)              30
            0xa1, 0x01,                    # Collection (Application)            32
            0x85, 0x11,                    #  Report ID (17)                     34
            0x75, 0x08,                    #  Report Size (8)                    36
            0x95, 0x13,                    #  Report Count (19)                  38
            0x15, 0x00,                    #  Logical Minimum (0)                40
            0x26, 0xff, 0x00,              #  Logical Maximum (255)              42
            0x09, 0x02,                    #  Usage (Vendor Usage 2)             45
            0x81, 0x00,                    #  Input (Data,Arr,Abs)               47
            0x09, 0x02,                    #  Usage (Vendor Usage 2)             49
            0x91, 0x00,                    #  Output (Data,Arr,Abs)              51
            0xc0,                          # End Collection                      53
            0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  54
            0x09, 0x04,                    # Usage (Vendor Usage 0x04)           57
            0xa1, 0x01,                    # Collection (Application)            59
            0x85, 0x20,                    #  Report ID (32)                     61
            0x75, 0x08,                    #  Report Size (8)                    63
            0x95, 0x0e,                    #  Report Count (14)                  65
            0x15, 0x00,                    #  Logical Minimum (0)                67
            0x26, 0xff, 0x00,              #  Logical Maximum (255)              69
            0x09, 0x41,                    #  Usage (Vendor Usage 0x41)          72
            0x81, 0x00,                    #  Input (Data,Arr,Abs)               74
            0x09, 0x41,                    #  Usage (Vendor Usage 0x41)          76
            0x91, 0x00,                    #  Output (Data,Arr,Abs)              78
            0x85, 0x21,                    #  Report ID (33)                     80
            0x95, 0x1f,                    #  Report Count (31)                  82
            0x15, 0x00,                    #  Logical Minimum (0)                84
            0x26, 0xff, 0x00,              #  Logical Maximum (255)              86
            0x09, 0x42,                    #  Usage (Vendor Usage 0x42)          89
            0x81, 0x00,                    #  Input (Data,Arr,Abs)               91
            0x09, 0x42,                    #  Usage (Vendor Usage 0x42)          93
            0x91, 0x00,                    #  Output (Data,Arr,Abs)              95
            0xc0,                          # End Collection                      97
        ]

        DeviceHandler.devices.append(HIDPP20Device(report_descriptor, (0x3, 0x046d, 0xc539), 'Logitech Simple Device'))
        DeviceHandler.devices.append(SteelseriesDevice(report_descriptor, (0x3, 0x01038, 0x1720), 2, 'Steelseriesw Rival 310'))

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

