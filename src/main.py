#!/usr/bin/env python3
from time import sleep

from protocol.hidpp20 import HIDPP20Device

"""
# Endpoint 0
report_descriptor = [
    0x05, 0x01,                    # Usage Page (Generic Desktop)        0
    0x09, 0x06,                    # Usage (Keyboard)                    2
    0xa1, 0x01,                    # Collection (Application)            4
    0x05, 0x07,                    #  Usage Page (Keyboard)              6
    0x19, 0xe0,                    #  Usage Minimum (224)                8
    0x29, 0xe7,                    #  Usage Maximum (231)                10
    0x15, 0x00,                    #  Logical Minimum (0)                12
    0x25, 0x01,                    #  Logical Maximum (1)                14
    0x75, 0x01,                    #  Report Size (1)                    16
    0x95, 0x08,                    #  Report Count (8)                   18
    0x81, 0x02,                    #  Input (Data,Var,Abs)               20
    0x81, 0x03,                    #  Input (Cnst,Var,Abs)               22
    0x95, 0x05,                    #  Report Count (5)                   24
    0x05, 0x08,                    #  Usage Page (LEDs)                  26
    0x19, 0x01,                    #  Usage Minimum (1)                  28
    0x29, 0x05,                    #  Usage Maximum (5)                  30
    0x91, 0x02,                    #  Output (Data,Var,Abs)              32
    0x95, 0x01,                    #  Report Count (1)                   34
    0x75, 0x03,                    #  Report Size (3)                    36
    0x91, 0x01,                    #  Output (Cnst,Arr,Abs)              38
    0x95, 0x06,                    #  Report Count (6)                   40
    0x75, 0x08,                    #  Report Size (8)                    42
    0x15, 0x00,                    #  Logical Minimum (0)                44
    0x26, 0xa4, 0x00,              #  Logical Maximum (164)              46
    0x05, 0x07,                    #  Usage Page (Keyboard)              49
    0x19, 0x00,                    #  Usage Minimum (0)                  51
    0x2a, 0xa4, 0x00,              #  Usage Maximum (164)                53
    0x81, 0x00,                    #  Input (Data,Arr,Abs)               56
    0xc0,                          # End Collection                      58
]
"""

# Endpoint 2
report_descriptor = [
    0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  0
    0x09, 0x01,                    # Usage (Vendor Usage 1)              3
    0xa1, 0x01,                    # Collection (Application)            5
    0x85, 0x10,                    #  Report ID (16)                     7
    0x75, 0x08,                    #  Report Size (8)                    9
    0x95, 0x06,                    #  Report Count (6)                   11
    0x15, 0x00,                    #  Logical Minimum (0)                13
    0x26, 0xff, 0x00,              #  Logical Maximum (255)              15
    0x09, 0x01,                    #  Usage (Vendor Usage 1)             18
    0x81, 0x00,                    #  Input (Data,Arr,Abs)               20
    0x09, 0x01,                    #  Usage (Vendor Usage 1)             22
    0x91, 0x00,                    #  Output (Data,Arr,Abs)              24
    0xc0,                          # End Collection                      26
    0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  27
    0x09, 0x02,                    # Usage (Vendor Usage 2)              30
    0xa1, 0x01,                    # Collection (Application)            32
    0x85, 0x11,                    #  Report ID (17)                     34
    0x75, 0x08,                    #  Report Size (8)                    36
    0x95, 0x13,                    #  Report Count (19)                  38
    0x15, 0x00,                    #  Logical Minimum (0)                40
    0x26, 0xff, 0x00,              #  Logical Maximum (255)              42
    0x09, 0x02,                    #  Usage (Vendor Usage 2)             45
    0x81, 0x00,                    #  Input (Data,Arr,Abs)               47
    0x09, 0x02,                    #  Usage (Vendor Usage 2)             49
    0x91, 0x00,                    #  Output (Data,Arr,Abs)              51
    0xc0,                          # End Collection                      53
    0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  54
    0x09, 0x04,                    # Usage (Vendor Usage 0x04)           57
    0xa1, 0x01,                    # Collection (Application)            59
    0x85, 0x20,                    #  Report ID (32)                     61
    0x75, 0x08,                    #  Report Size (8)                    63
    0x95, 0x0e,                    #  Report Count (14)                  65
    0x15, 0x00,                    #  Logical Minimum (0)                67
    0x26, 0xff, 0x00,              #  Logical Maximum (255)              69
    0x09, 0x41,                    #  Usage (Vendor Usage 0x41)          72
    0x81, 0x00,                    #  Input (Data,Arr,Abs)               74
    0x09, 0x41,                    #  Usage (Vendor Usage 0x41)          76
    0x91, 0x00,                    #  Output (Data,Arr,Abs)              78
    0x85, 0x21,                    #  Report ID (33)                     80
    0x95, 0x1f,                    #  Report Count (31)                  82
    0x15, 0x00,                    #  Logical Minimum (0)                84
    0x26, 0xff, 0x00,              #  Logical Maximum (255)              86
    0x09, 0x42,                    #  Usage (Vendor Usage 0x42)          89
    0x81, 0x00,                    #  Input (Data,Arr,Abs)               91
    0x09, 0x42,                    #  Usage (Vendor Usage 0x42)          93
    0x91, 0x00,                    #  Output (Data,Arr,Abs)              95
    0xc0,                          # End Collection                      97
]
name = 'Logitech G Pro'


test = HIDPP20Device(report_descriptor, (0x3, 0x046d, 0xc539), name)
test.create_kernel_device()

test.start(None)

while True:
    test.dispatch()
