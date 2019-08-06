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


@pytest.fixture(autouse=True)
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
def client(handle_devices):
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


def test_get_dpi(client, dpi_id=0):
    from ratbag_emu.device_handler import DeviceHandler

    id = test_add_device(client)

    response = client.get('/devices/{}/phys_props/dpi/{}'.format(id, dpi_id))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == DeviceHandler.devices[id].hprof.dpi[dpi_id if
        dpi_id != 'active' else DeviceHandler.devices[id].hprof.active_dpi]


def test_set_dpi(client, dpi_id=0):
    from ratbag_emu.device_handler import DeviceHandler

    id = test_add_device(client)

    DeviceHandler.devices[id].hprof.dpi[dpi_id if dpi_id != 'active' else
        DeviceHandler.devices[id].hprof.active_dpi] = 6666

    response = client.get('/devices/{}/phys_props/dpi/{}'.format(id, dpi_id))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == 6666


def test_get_active_dpi(client):
    test_get_dpi(client, 'active')


def test_set_active_dpi(client):
    test_set_dpi(client, 'active')


def test_get_led(client):
    id = test_add_device(client)

    response = client.get('/devices/{}/phys_props/leds/0'.format(id))
    assert response.status_code == 200


def test_set_led(client):
    id = test_add_device(client)

    data = [
        0xFF,
        0xFF,
        0xFF
    ]
    response = client.put('/devices/{}/phys_props/leds/0'.format(id),
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 200


def test_device_event_raw_xy(client):
    import os

    from time import sleep
    from threading import Thread

    import libevdev
    import fcntl
    import warnings

    from ratbag_emu.device_handler import DeviceHandler

    id = test_add_device(client, 'generic-hidpp20')
    sleep(0.1) # Give time for the event nodes to be created

    # Claim the event nodes
    event_nodes = []
    for node in DeviceHandler.devices[id].device_nodes:
        fd = open(node, 'rb')
        fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
        device = libevdev.Device(fd)
        try:
            device.grab()
        except libevdev.device.DeviceGrabError:
            with pytest.warns(UserWarning):
                warnings.warn("Couldn't grab one of the event nodes", UserWarning)
        event_nodes.append(device)

    # Send event
    data = {
        'x': 127,
        'y': 127
    }
    response = client.post('/devices/{}/raw_event'.format(id),
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200

    # Check if we received the event
    x = y = 0
    for node in event_nodes:
        events = node.events()
        for e in events:
            if e.matches(libevdev.EV_REL.REL_X):
                x += e.value
            elif e.matches(libevdev.EV_REL.REL_Y):
                y += e.value
        node.fd.close()
    assert x == data['x']
    assert y == data['y']

