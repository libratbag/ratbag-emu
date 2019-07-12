#!/bin/bash -e

# Validate
echo 'Validating...'
openapi-generator-cli validate -i src/ratbag_emu/openapi/ratbag-emu.yaml > /dev/null

# Client
echo 'Updating client code...'
openapi-generator-cli generate \
    -i src/ratbag_emu/openapi/ratbag-emu.yaml \
    --package-name ratbag_emu_client \
    -g python \
    -o src/client_gen/ \
    > /dev/null
