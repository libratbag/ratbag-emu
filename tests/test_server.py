# SPDX-License-Identifier: MIT

import fcntl
import os
import shutil
import subprocess
import threading
import warnings

import pytest
import requests
import libevdev

from time import time, sleep
from pathlib import Path

from ratbag_emu.util import MM_TO_INCH
from ratbag_emu.protocol.base import MouseData


class Client(object):
    def __init__(self, url='http://localhost:8080'):
        self.url = url

    def get(self, path):
        return requests.get(f'{self.url}{path}')

    def post(self, path, data=None, json=None):
        return requests.post(f'{self.url}{path}',
                             data=data,
                             json=json)

    def delete(self, path):
        return requests.delete(f'{self.url}{path}')

    def put(self, path, data=None, json=None):
        return requests.put(f'{self.url}{path}',
                            data=data,
                            json=json)


class TestServer(object):
    def reload_udev_rules(self):
        subprocess.run('udevadm control --reload-rules'.split())

    @pytest.fixture(scope='session', autouse=True)
    def udev_rules(self):
        rules_dir = Path('/run/udev/rules.d')
        rules_dir.mkdir(exist_ok=True)
        shutil.copyfile('rules.d/61-ratbag-emu-ignore-test-devices.rules', '/run/udev/rules.d/61-ratbag-emu-ignore-test-devices.rules')
        self.reload_udev_rules()

        yield

        rules = rules_dir.joinpath('61-ratbag-emu-ignore-test-devices.rules')
        if rules.is_file():
            rules.unlink()
            self.reload_udev_rules()

    @pytest.fixture(autouse=True)
    def client(self):
        yield Client()

    def add_device(self, client, hw_settings={}):
        data = {
            'hw_settings': hw_settings
        }
        response = client.post('/devices/add', json=data)
        assert response.status_code == 201
        return response.json()['id']

    @pytest.mark.dependency(name='test_add_device')
    def test_add_device(self, client, name='steelseries-rival310'):
        data = {
            'shortname': 'logitech-g-pro-wireless'
        }
        response = client.post('/devices/add', json=data)
        assert response.status_code == 201
        answer = response.json()
        assert 'id' in answer
        assert 'shortname' in answer
        assert 'name' in answer
        assert 'input_nodes' in answer
        client.delete(f"/devices/{answer['id']}")

    @pytest.mark.dependency(name='test_delete_device',
                            depends=['test_add_device'])
    def test_delete_device(self, client):
        id = self.add_device(client)

        response = client.delete(f'/devices/{id}')
        assert response.status_code == 204

    @pytest.mark.dependency(name='test_list_devices',
                            depends=['test_add_device', 'test_delete_device'])
    def test_list_devices(self, client):
        response = client.get('/devices')
        assert response.status_code == 200
        assert response.json() == []

        id = self.add_device(client)

        response = client.get('/devices')
        assert response.status_code == 200
        answer = response.json()
        assert len(answer) == 1
        assert answer[0]['id'] == id

        client.delete(f'/devices/{id}')

    @pytest.mark.dependency(name='test_get_device',
                            depends=['test_add_device', 'test_delete_device'])
    def test_get_device(self, client):
        id = self.add_device(client)

        response = client.get(f'/devices/{id}')
        assert response.status_code == 200
        answer = response.json()
        assert 'id' in answer
        assert 'shortname' in answer
        assert 'name' in answer
        assert 'input_nodes' in answer

        client.delete(f'/devices/{id}')

    @pytest.mark.dependency(name='test_get_dpi',
                            depends=['test_add_device', 'test_delete_device'])
    def test_get_dpi(self, client, dpi_id=0):
        dpi = 800

        id = self.add_device(client,{
            'is_active': True,
            'resolutions': [
                {
                    'is_active': True,
                    'xres': dpi,
                    'dpi_min': 100,
                    'dpi_max': 16000
                }
            ]
        })
        response = client.get(f'/devices/{id}/phys_props/dpi/{dpi_id}')
        assert response.status_code == 200
        assert response.json() == dpi

        client.delete(f'/devices/{id}')

    @pytest.mark.dependency(name='test_set_dpi',
                            depends=['test_add_device', 'test_delete_device', 'test_get_dpi'])
    def test_set_dpi(self, client, dpi_id=0):
        id = self.add_device(client, {
            'is_active': True,
            'resolutions': [
                {
                    'is_active': True,
                    'xres': 800,
                    'dpi_min': 100,
                    'dpi_max': 16000
                }
            ]
        })

        new_dpi = 6666
        response = client.put(f'/devices/{id}/phys_props/dpi/{dpi_id}', json=new_dpi)
        assert response.status_code == 200

        response = client.get(f'/devices/{id}/phys_props/dpi/{dpi_id}')
        assert response.status_code == 200
        assert response.json() == new_dpi

        client.delete(f'/devices/{id}')

    @pytest.mark.dependency(name='test_get_active_dpi',
                            depends=['test_add_device', 'test_delete_device', 'test_get_dpi'])
    def test_get_active_dpi(self, client):
        self.test_get_dpi(client, 'active')

    @pytest.mark.dependency(name='test_set_active_dpi',
                            depends=['test_add_device', 'test_delete_device', 'test_set_dpi', 'test_get_active_dpi'])
    def test_set_active_dpi(self, client):
        self.test_set_dpi(client, 'active')

    @pytest.mark.dependency(name='test_get_led',
                            depends=['test_add_device', 'test_delete_device'])
    def test_get_led(self, client):
        led_id = 0

        color = [
            0xFF,
            0xFF,
            0xFF
        ]

        id = self.add_device(client, {
            'is_active': True,
            'leds': [
                {
                    'color': color
                }
            ]
        })

        response = client.get(f'/devices/{id}/phys_props/leds/{led_id}')
        assert response.status_code == 200
        assert response.json() == color

        client.delete(f'/devices/{id}')

    @pytest.mark.dependency(name='test_set_led',
                            depends=['test_add_device', 'test_delete_device', 'test_get_led'])
    def test_set_led(self, client):
        led_id = 0

        id = self.add_device(client, {
            'is_active': True,
            'leds': [
                {
                    'color': [0xFF, 0xFF, 0xFF]
                }
            ]
        })

        color = [
            0xAA,
            0xBB,
            0xCC
        ]

        response = client.put(f'/devices/{id}/phys_props/leds/{led_id}', json=color)
        assert response.status_code == 200

        response = client.get(f'/devices/{id}/phys_props/leds/{led_id}')
        assert response.status_code == 200
        assert response.json() == color

        client.delete(f'/devices/{id}')

    @pytest.mark.dependency(name='test_device_event',
                            depends=['test_add_device', 'test_delete_device'])
    def test_device_event(self, client):
        id = self.add_device(client, {
            'is_active': True,
            'resolutions': [
                {
                    'is_active': True,
                    'xres': 1000,
                    'rate': 1000
                }
            ]
        })
        input_nodes = []

        start = time()
        while len(input_nodes) == 0:
            input_nodes = client.get(f'/devices/{id}').json()['input_nodes']
            sleep(0.1)
            if time() > start + 3:
                break

        # Claim the event nodes
        event_nodes = []
        for node in set(input_nodes):
            fd = open(node, 'rb')
            fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
            event_nodes.append(libevdev.Device(fd))

        # make this exit on a timeout
        events = []
        def collect_events(stop):
            nonlocal events
            while not stop.is_set():
                for node in event_nodes:
                    events += list(node.events())

        stop_event_thread = threading.Event()
        event_thread = threading.Thread(target=collect_events, args=(stop_event_thread,))
        event_thread.start()

        # Send event
        x = y = 5
        data = [
            {
                'start': 0,
                'end': 500,
                'action': {
                    'type': 'xy',
                    'x': x,
                    'y': y
                }
            }
        ]
        response = client.post(f'/devices/{id}/event', json=data)
        assert response.status_code == 200

        sleep(1)
        stop_event_thread.set()
        event_thread.join()

        for node in event_nodes:
            node.fd.close()

        received = MouseData()
        for e in events:
            if e.matches(libevdev.EV_REL.REL_X):
                received.x += e.value
            elif e.matches(libevdev.EV_REL.REL_Y):
                received.y += e.value

        dpi = client.get(f'/devices/{id}/phys_props/dpi/active').json()

        expected = MouseData()
        expected.x = int(x * MM_TO_INCH * dpi)
        expected.y = int(y * MM_TO_INCH * dpi)

        assert expected.x - 1 <= received.x <= expected.x + 1
        assert expected.y - 1 <= received.y <= expected.y + 1

        client.delete(f'/devices/{id}')
