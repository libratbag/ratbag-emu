# ratbag-emu

Mouse emulation stack. Used as a test suite for libratbag.

### Usage

Dependencies
  - connexion
  - hid-tools
  (optional)
  - connexion[swagger-ui]

Run the server:
```
src/main.py
```

If you have `swagger-ui` installed, you will be able to access the `/ui` page on the server where you will be presented with the auto generated openapi web interface. There you can find curl commands to interface with the API.

If you whish you can also use the client present in `src/client_gen`.
