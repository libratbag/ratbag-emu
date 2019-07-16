import json

import connexion
from hidtools.hid import RangeError

from ratbag_emu.device_handler import DeviceHandler

def add_device(shortname):
    return DeviceHandler.add_device(shortname), 201


def device_event(device_id):
    res = None
    status = 200

    if connexion.request.is_json:
        try:
            res = DeviceHandler.create_event(device_id, connexion.request.json)
        except KeyError:
            return \
                json.dumps("Invalid event"), 500
        except RangeError:
            return \
                json.dumps("The X or Y values exceed the maximum supported"), \
                400

    if res is None:
        status = 404

    return None, status


def get_device(device_id):
    res = DeviceHandler.get_openapi_device(device_id)
    status = 200

    if res is None:
        status = 404

    return res, status


def list_devices():
    return DeviceHandler.get_openapi_devices(), 200
