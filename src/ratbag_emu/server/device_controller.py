import json
from time import sleep

import connexion
from hidtools.hid import RangeError

from ratbag_emu.protocol.util.descriptors import report_descriptor_simple, \
                                                 report_descriptor_g_pro

from ratbag_emu.device_handler import DeviceHandler
from ratbag_emu.protocol.base import MouseData
from ratbag_emu.protocol.hidpp20 import HIDPP20Device
from ratbag_emu.protocol.hidpp20 import HIDPPFeatures as HIDPP20Features
from ratbag_emu.protocol.steelseries import SteelseriesDevice


'''
Devices
'''
def list_devices():
    device_list = []

    DeviceHandler.lock.acquire()
    devices = DeviceHandler.devices.copy()
    DeviceHandler.lock.release()
    for device_id, device in devices.items():
        if not device:
            continue

        device_list.append(DeviceHandler.get_device(device_id))

    return device_list, 200


'''
Device
'''
def get_device(device_id):
    try:
        return DeviceHandler.get_device(device_id), 200
    except KeyError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404


def add_device():
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    shortname = connexion.request.json['shortname']

    if shortname == "generic-hidpp20":
        DeviceHandler.append_device(HIDPP20Device(
            report_descriptor_simple, (0x3, 0x0001, 0x0001), []))
    elif shortname == "steelseries-rival310":
        DeviceHandler.append_device(SteelseriesDevice(
            report_descriptor_g_pro, (0x3, 0x01038, 0x1720),
            'Steelseriesw Rival 310', shortname, 2))
    elif shortname == "logitech-g-pro":
        DeviceHandler.append_device(HIDPP20Device(
            report_descriptor_g_pro, (0x3, 0x046d, 0x4079),
            [
                HIDPP20Features.IRoot,
                HIDPP20Features.IFeatureSet,
                HIDPP20Features.IFeatureInfo,
                HIDPP20Features.DeviceNameAndType,
                0x1d4b,
                0x0020,
                0x1001,
                0x8070,
                0x1300,
                0x8100,
                0x8110,
                0x8060,
                0x2201,
                0x1802,
                0x1803,
                0x1805,
                0x1806,
                0x1811,
                0x1830,
                0x1890,
                0x1891,
                0x18a1,
                0x1801,
                0x18b1,
                0x1df3,
                0x1e00,
                0x1eb0,
                0x1863,
                0x1e22
            ],
            'Logitech G Pro', shortname))
    else:
        return json.dumps(f"Specification '{shortname}' does not exist"), 404

    id = DeviceHandler.cur_id
    DeviceHandler.wait_for_device_nodes(id)

    sleep(0.1)

    return DeviceHandler.get_device(id), 201


def delete_device(device_id):
    try:
        DeviceHandler.destroy_device(device_id)
        return json.dumps('Device deleted'), 204
    except KeyError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

'''
DPI
'''
def get_dpi(device_id, dpi_id):
    try:
        device = DeviceHandler.devices[device_id]
    except KeyError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    if dpi_id == 'active':
        dpi_id = device.hw_profile.active_dpi
    else:
        dpi_id = int(dpi_id)

    try:
        return device.hw_profile.dpi[dpi_id], 200
    except IndexError:
        return json.dumps(f"DPI '{dpi_id}' doesn't exist for device '{device_id}'"), 404


def set_dpi(device_id, dpi_id):
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    value = connexion.request.json

    try:
        device = DeviceHandler.devices[device_id]
    except KeyError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    if dpi_id == 'active':
        dpi_id = device.hw_profile.active_dpi
    else:
        dpi_id = int(dpi_id)

    try:
        device.hw_profile.dpi[dpi_id] = value
        return json.dumps('Value updated'), 200
    except IndexError:
        return json.dumps(f"DPI '{dpi_id}' doesn't exist for device '{device_id}'"), 404


'''
LEDs
'''
def get_led(device_id, led_id):
    try:
        device = DeviceHandler.devices[device_id]
    except IndexError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    try:
        return device.hw_profile.leds[led_id]
    except IndexError:
        return json.dumps(f"LED '{device_id}' doesn't exist for device '{led_id}'"), 404



def set_led(device_id, led_id):
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    value = connexion.request.json

    try:
        device = DeviceHandler.devices[device_id]
    except IndexError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    if len(value) != 3:
        return json.dumps('Invalid value'), 400

    try:
        device.hw_profile.leds[led_id] = value

        return json.dumps('Value updated'), 200
    except IndexError:
        return json.dumps(f"LED '{device_id}' doesn't exist for device '{led_id}'"), 404


'''
Event
'''
def device_event(device_id):
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    actions = connexion.request.json

    try:
        device = DeviceHandler.devices[device_id]
    except IndexError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    if actions is None:
        return json.dumps('Invalid value'), 400

    device.simulate_action(actions)

    return json.dumps('Success'), 200
