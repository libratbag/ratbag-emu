import json

import connexion
from hidtools.hid import RangeError

from ratbag_emu.protocol.descriptors import report_descriptor_simple, \
                                            report_descriptor_g_pro

from ratbag_emu.device_handler import DeviceHandler
from ratbag_emu.protocol.base import MouseData
from ratbag_emu.protocol.hidpp20 import HIDPP20Device
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
        return json.dumps('The request is not balid JSON.'), 400

    shortname = connexion.request.json['shortname']

    if shortname == "steelseries-rival310":
        DeviceHandler.append_device(SteelseriesDevice(
            report_descriptor_g_pro, (0x3, 0x01038, 0x1720),
            'Steelseriesw Rival 310', shortname, 2))
    elif shortname == "logitech-g-pro":
        DeviceHandler.append_device(HIDPP20Device(
            report_descriptor_g_pro, (0x3, 0x046d, 0xc4079),
            'Logitech G Pro', shortname))
    else:
        return \
            json.dumps("Specification '{}' does not exist".format(shortname)), \
            404

    return json.dumps('Device added'), 201


def delete_device(device_id):
    if device_id > len(DeviceHandler.devices) - 1:
        return False

    # TODO: Destroy device
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
def device_event(device_id, event_data):
    if device_id > len(DeviceHandler.devices) - 1:
        return json.dumps("Device '{}' doesn't exist".format(device_id)), 404

    if event_data is None:
        return json.dumps('Invalid value'), 400

    event = MouseData(DeviceHandler.devices[device_id])

    for data in event_data:
        for key, prop in data.items():
            setattr(event, key, prop)

    data = DeviceHandler.devices[device_id].create_report(event, 0x11)
    try:
        DeviceHandler.devices[device_id].send_raw(data)
    except KeyError:
        return \
            json.dumps('Invalid event'), 500
    except RangeError:
        return \
            json.dumps('The X or Y values exceed the maximum supported'), \
            400

    return json.dumps('Success'), 200
