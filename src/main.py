#!/usr/bin/env python3
import sys
import threading
import traceback

import connexion

import ratbag_emu.server
from ratbag_emu.device_handler import DeviceHandler


def main():
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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc(file=sys.stdout)
