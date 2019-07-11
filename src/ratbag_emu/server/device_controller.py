import connexion
import six

from ratbag_emu.device_handler import DeviceHandler

from ratbag_emu_server.models.device import Device  # noqa: E501
from ratbag_emu_server.models.event_data import EventData  # noqa: E501
from ratbag_emu_server import util

def add_device(shortname):  # noqa: E501
    """Creates a simulated device

    Tells ratbag-emu to create a new simulated device # noqa: E501

    :param shortname: Short name name of the device to add
    :type shortname: str

    :rtype: None
    """
    return DeviceHandler.add_device(shortname)

def device_event(device_id, event_data):  # noqa: E501
    """Send an event to a simulated device

    Send raw HID event data to the target device # noqa: E501

    :param device_id: ID of the device to return
    :type device_id: int
    :param event_data: Event data
    :type event_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        event_data = EventData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'device_event()'


def get_device(device_id):  # noqa: E501
    """Returns a simulated device

    Returns one the of devices currently simulated by ratbag-emu # noqa: E501

    :param device_id: ID of the device to return
    :type device_id: int

    :rtype: Device
    """
    return DeviceHandler.get_openapi_device(device_id)


def list_devices():  # noqa: E501
    """List of simulated devices

    Provides the list of devices that are being currently simulated by ratbag-emu # noqa: E501


    :rtype: List[Device]
    """
    return DeviceHandler.get_openapi_devices()
