#!/bin/bash


# Server
echo 'Updating server code...'
openapi-generator-cli generate \
    -i src/ratbag_emu/openapi/ratbag-emu.yaml \
    --package-name ratbag_emu_server \
    -g python-flask \
    -o src/server_gen/ \
    > /dev/null

mv src/server_gen/ratbag_emu_server/controllers/device_controller.py src/server_gen/ratbag_emu_server/controllers/device_controller_gen.py
cp src/ratbag_emu/server/device_controller.py src/server_gen/ratbag_emu_server/controllers/device_controller.py

# Client
echo 'Updating client code...'
openapi-generator-cli generate \
    -i src/ratbag_emu/openapi/ratbag-emu.yaml \
    --package-name ratbag_emu_client \
    -g python \
    -o src/client_gen/ \
    > /dev/null
