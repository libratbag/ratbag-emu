import json

import connexion
import pytest

server = connexion.FlaskApp(__name__,
                            specification_dir='../src/ratbag_emu/openapi/',
                            debug=True)
server.add_api('ratbag-emu.yaml',
                options={"swagger_ui": True},
                arguments={'title': 'ratbag-emu'},
                strict_validation=True,
                validate_responses=True)


def test_permissions():
    from hidtools.uhid import UHIDDevice

    try:
        assert UHIDDevice() is not None
    except PermissionError:
        pytest.exit('Not enough permissions to create UHID devices')


@pytest.fixture
def handle_devices():
    import threading

    from . import ratbag_emu

    import ratbag_emu.server
    from ratbag_emu.device_handler import DeviceHandler

    devices_thread = threading.Thread(target=DeviceHandler.handle)
    devices_thread.daemon = True
    devices_thread.start()

    yield devices_thread


@pytest.fixture(autouse=True)
def client():
    yield server.app.test_client()


def test_list_devices(client):
    response = client.get('/devices')
    assert response.status_code == 200


@pytest.fixture
def test_add_device(client):
    data = {
        'shortname': 'steelseries-rival310'
    }
    response = client.post('/devices/add',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 201


def test_get_device(client, test_add_device):
    response = client.get('/devices/0')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert 'shortname' in data
    assert 'name' in data
