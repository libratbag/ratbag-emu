# ratbag-emu

Mouse emulation stack. Used as a test suite for libratbag.

### Usage

To run you first need to install the `ratbag_emu_server` module.

```
pip3 install src/ratbag_emu_server
```

Then you can run the server.

```
src/main.py
```

After that you can access thye `/ui` page in the server where you will be presented with the auto generated openapi web interface. There you can find curl commands to interface with the API.

If you whish you can also use the client present in `src/client_gen`.
