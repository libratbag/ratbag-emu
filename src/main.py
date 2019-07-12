#!/usr/bin/env python3
import threading

import connexion
from connexion.resolver import RestyResolver

#from ratbag_emu_server import encoder

import ratbag_emu.server
from ratbag_emu.device_handler import DeviceHandler

if __name__ == "__main__":
    # Start handling devices
    devices_thread = threading.Thread(target=DeviceHandler.handle)
    devices_thread.start()

    # Run server
    server = connexion.FlaskApp(__name__,
                                specification_dir='ratbag_emu/openapi/',
                                debug=True)
    server.add_api('ratbag-emu.yaml',
                   options={"swagger_ui": True},
                   arguments={'title': 'ratbag-emu'},
                   strict_validation=True,
                   validate_responses=True)
    server.run(port=8080)
