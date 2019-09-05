from .logitech_g_pro_wireless import *

class DeviceList(object):
    device_list = {
        # Logitech
        'logitech-g-pro-wireless': LogitechGProWirelessDevice
    }

    @classmethod
    def exists(cls,shortname):
        return shortname in cls.device_list

    @classmethod
    def get(cls, shortname):
        assert cls.exists(shortname), f"Device '{shortname}' doesn't exist"
        return cls.device_list[shortname]
