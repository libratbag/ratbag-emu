#!/bin/bash

# Server
openapi-generator-cli generate -i src/openapi/ratbag-emu.yaml --package-name ratbag_emu_server -g python-flask -o src/server_gen/

# Client
openapi-generator-cli generate -i src/openapi/ratbag-emu.yaml --package-name ratbag_emu_client -g python -o src/client_gen/
