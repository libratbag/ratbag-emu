from ratbag_emu.protocol.steelseries import SteelseriesDevice

class SteelseriesRival310Device(SteelseriesDevice):
    def __init__(self, id=None):
        self.name = 'Steelseries Rival 310'
        self.shortname = 'steelseries-rival310'
        self.info = (0x03, 0x1038, 0x1720)
        self.rdescs = [
            [
                0x05, 0x01,                    # Usage Page (Generic Desktop)        0
                0x09, 0x02,                    # Usage (Mouse)                       2
                0xa1, 0x01,                    # Collection (Application)            4
                0x09, 0x01,                    # .Usage (Pointer)                    6
                0xa1, 0x00,                    # .Collection (Physical)              8
                0xa1, 0x02,                    # ..Collection (Logical)              10
                0x05, 0x09,                    # ...Usage Page (Button)              12
                0x19, 0x01,                    # ...Usage Minimum (1)                14
                0x29, 0x08,                    # ...Usage Maximum (8)                16
                0x15, 0x00,                    # ...Logical Minimum (0)              18
                0x25, 0x01,                    # ...Logical Maximum (1)              20
                0x95, 0x08,                    # ...Report Count (8)                 22
                0x75, 0x01,                    # ...Report Size (1)                  24
                0x81, 0x02,                    # ...Input (Data,Var,Abs)             26
                0x05, 0x01,                    # ...Usage Page (Generic Desktop)     28
                0x09, 0x30,                    # ...Usage (X)                        30
                0x09, 0x31,                    # ...Usage (Y)                        32
                0x16, 0x01, 0x80,              # ...Logical Minimum (-32767)         34
                0x26, 0xff, 0x7f,              # ...Logical Maximum (32767)          37
                0x75, 0x10,                    # ...Report Size (16)                 40
                0x95, 0x02,                    # ...Report Count (2)                 42
                0x81, 0x06,                    # ...Input (Data,Var,Rel)             44
                0x09, 0x38,                    # ...Usage (Wheel)                    46
                0x15, 0x81,                    # ...Logical Minimum (-127)           48
                0x25, 0x7f,                    # ...Logical Maximum (127)            50
                0x75, 0x08,                    # ...Report Size (8)                  52
                0x95, 0x01,                    # ...Report Count (1)                 54
                0x81, 0x06,                    # ...Input (Data,Var,Rel)             56
                0xc0,                          # ..End Collection                    58
                0xa1, 0x02,                    # ..Collection (Logical)              59
                0x05, 0x0c,                    # ...Usage Page (Consumer Devices)    61
                0x0a, 0x38, 0x02,              # ...Usage (AC Pan)                   63
                0x15, 0x81,                    # ...Logical Minimum (-127)           66
                0x25, 0x7f,                    # ...Logical Maximum (127)            68
                0x75, 0x08,                    # ...Report Size (8)                  70
                0x95, 0x01,                    # ...Report Count (1)                 72
                0x81, 0x06,                    # ...Input (Data,Var,Rel)             74
                0xc0,                          # ..End Collection                    76
                0xa1, 0x02,                    # ..Collection (Logical)              77
                0x06, 0xc1, 0xff,              # ...Usage Page (Vendor Usage Page 0xffc1) 79
                0x15, 0x00,                    # ...Logical Minimum (0)              82
                0x26, 0xff, 0x00,              # ...Logical Maximum (255)            84
                0x75, 0x08,                    # ...Report Size (8)                  87
                0x09, 0xf0,                    # ...Usage (Vendor Usage 0xf0)        89
                0x95, 0x02,                    # ...Report Count (2)                 91
                0x81, 0x02,                    # ...Input (Data,Var,Abs)             93
                0xc0,                          # ..End Collection                    95
                0xc0,                          # .End Collection                     96
                0xc0,                          # End Collection                      97
            ],
            [
                 0x05, 0x01,                    # Usage Page (Generic Desktop)        0
                 0x09, 0x06,                    # Usage (Keyboard)                    2
                 0xa1, 0x01,                    # Collection (Application)            4
                 0x85, 0x01,                    # .Report ID (1)                      6
                 0x05, 0x07,                    # .Usage Page (Keyboard)              8
                 0x19, 0xe0,                    # .Usage Minimum (224)                10
                 0x29, 0xe7,                    # .Usage Maximum (231)                12
                 0x15, 0x00,                    # .Logical Minimum (0)                14
                 0x25, 0x01,                    # .Logical Maximum (1)                16
                 0x75, 0x01,                    # .Report Size (1)                    18
                 0x95, 0x08,                    # .Report Count (8)                   20
                 0x81, 0x02,                    # .Input (Data,Var,Abs)               22
                 0x75, 0x08,                    # .Report Size (8)                    24
                 0x95, 0x01,                    # .Report Count (1)                   26
                 0x81, 0x01,                    # .Input (Cnst,Arr,Abs)               28
                 0x05, 0x07,                    # .Usage Page (Keyboard)              30
                 0x19, 0x00,                    # .Usage Minimum (0)                  32
                 0x2a, 0xff, 0x00,              # .Usage Maximum (255)                34
                 0x15, 0x00,                    # .Logical Minimum (0)                37
                 0x26, 0xff, 0x00,              # .Logical Maximum (255)              39
                 0x75, 0x08,                    # .Report Size (8)                    42
                 0x95, 0x06,                    # .Report Count (6)                   44
                 0x81, 0x00,                    # .Input (Data,Arr,Abs)               46
                 0xc0,                          # End Collection                      48
                 0x05, 0x0c,                    # Usage Page (Consumer Devices)       49
                 0x09, 0x01,                    # Usage (Consumer Control)            51
                 0xa1, 0x01,                    # Collection (Application)            53
                 0x85, 0x02,                    # .Report ID (2)                      55
                 0x05, 0x0c,                    # .Usage Page (Consumer Devices)      57
                 0x19, 0x00,                    # .Usage Minimum (0)                  59
                 0x2a, 0xff, 0x0f,              # .Usage Maximum (4095)               61
                 0x15, 0x00,                    # .Logical Minimum (0)                64
                 0x26, 0xff, 0x0f,              # .Logical Maximum (4095)             66
                 0x75, 0x10,                    # .Report Size (16)                   69
                 0x95, 0x02,                    # .Report Count (2)                   71
                 0x81, 0x00,                    # .Input (Data,Arr,Abs)               73
                 0xc0,                          # End Collection                      75
            ]
        ]
        self.id = id

        # Steelseries specific settings
        self.protocol_version = 2

        self.hw_settings = {
            'is_active': True,
            'resolutions': [
                {
                    'is_active': True,
                    'xres': 800,
                    'dpi_min': 100,
                    'dpi_max': 12000,
                    'dpi_step': 100
                },
                {
                    'xres': 1600,
                    'dpi_min': 100,
                    'dpi_max': 12000,
                    'dpi_step': 100
                }
            ]
        }

        super().__init__()

