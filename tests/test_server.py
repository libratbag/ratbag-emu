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


def test_add_device(client):
    data = {
        'shortname': 'steelseries-rival310'
    }
    response = client.post('/devices/add',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 201
