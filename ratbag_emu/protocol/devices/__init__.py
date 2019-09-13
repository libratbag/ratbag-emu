# SPDX-License-Identifier: MIT

from .logitech_g_pro_wireless import LogitechGProWirelessDevice
from .steelseries_rival_310 import SteelseriesRival310Device

__all__ = ['DeviceList']


class DeviceList(object):
    device_list = {
        # Logitech
        'logitech-g-pro-wireless': LogitechGProWirelessDevice,
        # Steelseries
        'steelseries-rival310': SteelseriesRival310Device,
    }

    @classmethod
    def exists(cls, shortname):
        return shortname in cls.device_list

    @classmethod
    def get(cls, shortname):
        assert cls.exists(shortname), f"Device '{shortname}' doesn't exist"
        return cls.device_list[shortname]
