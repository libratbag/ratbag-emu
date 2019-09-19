# ratbag-emu

Mouse emulation stack. Used as a test suite for libratbag.

### Architecture

- ratbag-emu starts a Flask web server
- through the REST API new devices can be created, ratbag-emu creates a UHID
  device for those that will be picked up by ratbagd as if it was a real
  device
- ratbag-emu handles the firmware/protocol-specific bits and pretends to be
  the specific model created
- through the REST API the device can be ordered to do things (e.g. move by
  5 mm), ratbag-emu generates HID reports to that effect, matching the DPI
  rate of the device, etc
- The test suite ties it all together and verifies that a device with 1000
  DPI moved by 5mm generates N events, etc.


### Dependencies

Dependencies for the server:
  - connexion
  - hid-tools
  - connexion[swagger-ui] (optional)

Dependencies for running the tests:
  - pytest
  - pytest-dependency

### Usage

Run the server:
```
sudo python3 -m ratbag_emu
```

Run the test suite:
```
sudo pytest-3
```


If you have `swagger-ui` installed, you will be able to access the `/ui` page on the server where you will be presented with the auto generated openapi web interface. There you can find curl commands to interface with the API.
