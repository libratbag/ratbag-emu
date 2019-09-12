import json
from time import sleep

import connexion

from ratbag_emu.device_handler import DeviceHandler
from ratbag_emu.protocol.base import BaseDevice
from ratbag_emu.protocol.devices import DeviceList


#
# Devices
#
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


#
# Device
#
def get_device(device_id):
    try:
        return DeviceHandler.get_device(device_id), 200
    except KeyError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404


def add_device():
    if not connexion.request.is_json:
        return json.dumps('The request is not valid JSON.'), 400

    shortname = connexion.request.json.get('shortname')
    hw_settings = connexion.request.json.get('hw_settings')

    # Normal Device
    if shortname:
        if not DeviceList.exists(shortname):
            return json.dumps(f"Unknown device '{shortname}'"), 404

        DeviceHandler.append_device(DeviceList.get(shortname)(DeviceHandler.cur_id+1))

    # Generic Device
    elif hw_settings:
        DeviceHandler.append_device(BaseDevice(hw_settings, id=DeviceHandler.cur_id+1))

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

#
# DPI
#
def get_dpi(device_id, dpi_id):
    try:
        device = DeviceHandler.devices[device_id]
    except KeyError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    if dpi_id == 'active':
        dpi_id = device.hw_settings.active_dpi
    else:
        dpi_id = int(dpi_id)

    try:
        return device.hw_settings.dpi[dpi_id], 200
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
        dpi_id = device.hw_settings.active_dpi
    else:
        dpi_id = int(dpi_id)

    try:
        device.hw_settings.dpi[dpi_id] = value
        return json.dumps('Value updated'), 200
    except IndexError:
        return json.dumps(f"DPI '{dpi_id}' doesn't exist for device '{device_id}'"), 404


#
# LEDs
#
def get_led(device_id, led_id):
    try:
        device = DeviceHandler.devices[device_id]
    except IndexError:
        return json.dumps(f"Device '{device_id}' doesn't exist"), 404

    try:
        return list(device.hw_settings.leds[led_id])
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
        device.hw_settings.leds[led_id] = device.hw_settings.Led(*value)
        return json.dumps('Value updated'), 200
    except IndexError:
        return json.dumps(f"LED '{device_id}' doesn't exist for device '{led_id}'"), 404


#
# Event
#
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

    try:
        device.simulate_action(actions)
        return json.dumps('Success'), 200
    except Exception as e:
        return json.dumps(str(e)), 400

