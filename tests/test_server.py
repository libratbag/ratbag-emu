import threading
from time import sleep

import connexion

from . import ratbag_emu

import ratbag_emu.server
from ratbag_emu.device_handler import DeviceHandler


def create_server():
    # Start handling devices
    devices_thread = threading.Thread(target=DeviceHandler.handle)
    devices_thread.start()

    # Run server
    server = connexion.FlaskApp(__name__,
                                specification_dir='../src/ratbag_emu/openapi/',
                                debug=True)
    server.add_api('ratbag-emu.yaml',
                   options={"swagger_ui": True},
                   arguments={'title': 'ratbag-emu'},
                   strict_validation=True,
                   validate_responses=True)
    server_thread = threading.Thread(target=server.run, kwargs={'port': 8080})
    server_thread.start()

    return server_thread

def test_create_server():
    server = create_server()

    sleep(1)
    server.shutdown()
