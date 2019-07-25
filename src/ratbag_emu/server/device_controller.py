import json

import connexion
from hidtools.hid import RangeError

from ratbag_emu.protocol.descriptors import report_descriptor_simple, \
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
    devices = []

    for device_id, device in DeviceHandler.devices.items():
        if not device:
            continue

        devices.append({
            'id':           device_id,
            'name':         device.name,
            'shortname':    device.shortname
        })

    return devices, 200


'''
Device
'''
def get_device(device_id):
    if device_id > len(DeviceHandler.devices) - 1:
        return json.dumps("Device '{}' does not exist".format(device_id)), 404

    return {
        'id':           device_id,
        'name':         DeviceHandler.devices[device_id].name,
        'shortname':    DeviceHandler.devices[device_id].shortname
    }, 200


def add_device():
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    shortname = connexion.request.json['shortname']

    if shortname == "steelseries-rival310":
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
        return \
            json.dumps("Specification '{}' does not exist".format(shortname)), \
            404

    return json.dumps('Device added'), 201


def delete_device(device_id):
    if device_id > len(DeviceHandler.devices) - 1:
        return False

    DeviceHandler.devices[device_id].destroy()
    DeviceHandler.devices[device_id] = None


'''
LEDs
'''
def get_led(device_id, led_id):
    if device_id > len(DeviceHandler.devices) - 1 or \
       DeviceHandler.devices[device_id] is None:
        return json.dumps("Device '{}' doesn't exist".format(device_id)), 404

    if led_id > len(DeviceHandler.devices[device_id].leds) - 1:
        return \
            json.dumps("LED '{}' doesn't exist for device '{}'".format(
                        device_id, led_id)), \
            404

    return DeviceHandler.devices[device_id].leds[led_id]


def set_led(device_id, led_id, value):
    if device_id > len(DeviceHandler.devices) - 1 or \
       DeviceHandler.devices[device_id] is None:
        return json.dumps("Device '{}' doesn't exist".format(device_id)), 404

    if led_id > len(DeviceHandler.devices[device_id].leds) - 1:
        return \
            json.dumps("LED '{}' doesn't exist for device '{}'".format(
                        device_id, led_id)), \
            404

    if len(value) != 3:
        return json.dumps('Invalid value'), 400

    DeviceHandler.devices[device_id].leds[led_id] = value

    return json.dumps('Value updated'), 200


'''
Event
'''
def device_event(device_id):
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    actions = connexion.request.json

    if device_id > len(DeviceHandler.devices) - 1:
        return json.dumps("Device '{}' doesn't exist".format(device_id)), 404

    if actions is None:
        return json.dumps('Invalid value'), 400

    DeviceHandler.devices[device_id].simulate_action(actions)

    return json.dumps('Success'), 200


def device_event_raw(device_id):
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    event_data = connexion.request.json

    if device_id > len(DeviceHandler.devices) - 1:
        return json.dumps("Device '{}' doesn't exist".format(device_id)), 404

    if event_data is None:
        return json.dumps('Invalid value'), 400

    event = MouseData(DeviceHandler.devices[device_id])

    for data in event_data:
        for key, prop in data.items():
            if hasattr(event, key):
                setattr(event, key, prop)
            else:
                print('Invalid attribute ({})'.format(key))

    data = None
    try:
        data = DeviceHandler.devices[device_id].generate_report(event, 0x11)
    except KeyError:
        return \
            json.dumps('Invalid event'), 500
    except RangeError:
        return \
            json.dumps('The X or Y values exceed the maximum supported'), \
            400

    DeviceHandler.devices[device_id].send_raw(data)

    return json.dumps('Success'), 200
