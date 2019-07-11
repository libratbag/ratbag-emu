#!/usr/bin/env python3
import threading

import connexion
from ratbag_emu_server import encoder

from ratbag_emu.device_handler import DeviceHandler

if __name__ == "__main__":
    # Start handling devices
    devices_thread = threading.Thread(target=DeviceHandler.handle)
    devices_thread.start()

    # Run server
    server = connexion.App(__name__,
                    specification_dir='server_gen/ratbag_emu_server/openapi')
    server.app.json_encoder = encoder.JSONEncoder
    server.add_api('openapi.yaml',
                    arguments={'title': 'ratbag-emu'},
                    pythonic_params=True)
    server.run(port=8080)
