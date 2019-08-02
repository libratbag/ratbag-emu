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


def test_add_device(client, name='steelseries-rival310'):
    data = {
        'shortname': name
    }
    response = client.post('/devices/add',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert 'shortname' in data
    assert 'name' in data
    return data['id']


def test_get_device(client):
    id = test_add_device(client)

    response = client.get('/devices/{}'.format(id))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert 'shortname' in data
    assert 'name' in data


def test_delete_device(client):
    id = test_add_device(client)

    response = client.delete('/devices/{}'.format(id))
    assert response.status_code == 204


def test_get_led(client):
    id = test_add_device(client)

    response = client.get('/devices/{}/leds/0'.format(id))
    assert response.status_code == 200


def test_set_led(client):
    id = test_add_device(client)

    data = [
        0xFF,
        0xFF,
        0xFF
    ]
    response = client.put('/devices/{}/leds/0'.format(id),
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 200
