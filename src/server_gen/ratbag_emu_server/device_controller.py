import connexion
import six

from ratbag_emu_server.models.device import Device  # noqa: E501
from ratbag_emu_server.models.movement_data import MovementData  # noqa: E501
from ratbag_emu_server import util


def device_move(device_id, movement_data):  # noqa: E501
    """Moves a simulated device

    Send movement data to the target device # noqa: E501

    :param device_id: ID of the device to return
    :type device_id: str
    :param movement_data: Movement data
    :type movement_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        movement_data = MovementData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'device_move()'


def get_device(device_id):  # noqa: E501
    """Returns a simulated device

    Returns one the of devices currently simulated by ratbag-emu # noqa: E501

    :param device_id: ID of the device to return
    :type device_id: str

    :rtype: Device
    """
    return 'get_device()'


def list_devices():  # noqa: E501
    """List of simulated devices

    Provides the list of devices that are being currently simulated by ratbag-emu # noqa: E501


    :rtype: List[Device]
    """
    return openapi_devices
