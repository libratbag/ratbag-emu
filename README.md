# ratbag-emu

HID emulation stack. Used as a test suite for libratbag.

### Architecture

- ratbag-emu provides an API to create virtual devices
- ratbag-emu handles the firmware/protocol-specific bits and pretends to be
  the specific model created
- through the API the device can be ordered to do things (e.g. move by 5 mm),
  ratbag-emu generates HID reports to that effect, matching the DPI
  rate of the device, etc
- The test suite ties it all together and verifies that a device with 1000
  DPI moved by 5mm generates N events, etc.


### Dependencies

Dependencies:
  - hid-tools

Dependencies for running the tests:
  - pytest
