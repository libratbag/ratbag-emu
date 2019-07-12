import connexion

from ratbag_emu.device_handler import DeviceHandler

def add_device(shortname):
    return DeviceHandler.add_device(shortname)


def device_event(device_id):
    if connexion.request.is_json:
        return DeviceHandler.create_event(device_id, connexion.request.json)


def get_device(device_id):
    return DeviceHandler.get_openapi_device(device_id)


def list_devices():
    return DeviceHandler.get_openapi_devices()
