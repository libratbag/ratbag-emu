from .base import BaseDevice


class HIDPP20Report():
    ReportType                  = 0
    Device                      = 1
    Feature                     = 2
    ASE                         = 3
    Arguments                   = 4


class HIDPP20ReportType():
    Short                       = 0x10
    Long                        = 0x11
    ShortSize                   = 7
    LongSize                    = 20


class HIDPP20Features():
    IRoot                       = 0x0000
    IFeatureSet                 = 0x0001
    IFeatureInfo                = 0x0002
    DeviceInformation           = 0x0003
    DeviceNameAndType           = 0x0005
    DeviceGroups                = 0x0006
    ConfigChange                = 0x0020
    UniqueIdentifier            = 0x0021
    WirelessSignalStrength      = 0x0080
    DFUControl0                 = 0x00c0
    DFUControl1                 = 0x00c1
    DFU                         = 0x00d0


class HIDPP20Errors():
    NoError                     = 0
    Unknown                     = 1
    InvalidArgument             = 2
    OutOfRange                  = 3
    HWError                     = 4
    LogitechInternal            = 5
    INVALID_FEATURE_INDEX       = 6
    INVALID_FUNCTION_ID         = 7
    Busy                        = 8
    Unsupported                 = 9


class HIDPP20Device(BaseDevice):
    '''
    Internal variables
    '''
    expecting_reply = False

    '''
    Init routine
    '''
    def __init__(self):
        assert hasattr(self, 'feature_table'), 'Feature table missing'
        super().__init__({}, self.name, self.info, self.rdescs, self.shortname)

        # Protocol declarations
        self.Report         = HIDPP20Report
        self.ReportType     = HIDPP20ReportType
        self.Features       = HIDPP20Features
        self.Errors         = HIDPP20Errors

        self.report_size = {
            self.ReportType.Short:              self.ReportType.ShortSize,
            self.ReportType.Long:               self.ReportType.LongSize
        }

        # Function mapping
        self.features = {
            self.Features.IRoot:                self.IRoot,
            self.Features.IFeatureSet:          self.IFeatureSet,
            self.Features.IFeatureInfo:         self.IFeatureInfo
        }

        self.events = {}

        # Device proprieties
        self.version_major = 4
        self.version_minor = 2

    '''
    Interface functions
    '''
    def protocol_send(self, report_type, device, feature, ase, sw_id, args):
        data = [0] * self.report_size[report_type]
        data[self.Report.ReportType]    = report_type
        data[self.Report.Device]        = device
        data[self.Report.Feature]       = feature
        data[self.Report.ASE]           = ase << 4 + sw_id
        for i in range(len(args)):
            data[self.Report.Arguments + i] = args[i]

        super().send_raw(data)

    def protocol_reply(self, data, args):
        assert len(data) >= self.Report.Arguments + len(args), \
               'Report too small to send the arguments'

        for i in range(len(args)):
            data[self.Report.Arguments + i] = args[i]

        super().send_raw(data)

    def protocol_error(self, data, error):
        super().send_raw([
            self.ReportType.Short,
            data[self.Report.Device],
            0x8f,
            data[self.Report.Feature],
            data[self.Report.ASE],
            error,
            0
        ])

    '''
    Logic definition
    '''
    def protocol_receive(self, data, size, rtype):
        report_type = data[self.Report.ReportType]
        device      = data[self.Report.Device]
        feature     = data[self.Report.Feature]
        ase         = data[self.Report.ASE] >> 4
        sw_id       = data[self.Report.ASE] - ase
        args        = data[self.Report.Arguments:]

        assert report_type in self.report_size, f'Invalid report type ({report_type:2x})'

        assert len(data) == self.report_size[report_type], 'Wrong report size.' \
            f'Expected {self.report_size[report_type]}, got {len(data)}'

        # Event
        if self.expecting_reply:
            return
        # Function
        else:
            print(f'# DEBUG: Got feature {feature}, ASE {ase}')
            self.features[feature](data, ase, args)

    '''
    Event definitions
    '''

    '''
    Feature definitions
    '''
    def IRoot(self, data, ase, args):
        # featIndex, featType, featVer = getFeature(featId)
        if ase == 0:
            featId = (args[0] << 4) + args[1]
            print(f'# DEBUG: getFeature({featId}) = {self.feature_table[featId]}')
            # we won't support any hidden features and we are also not planning
            # to support obsolete features ATM so we will set featType to 0
            self.protocol_reply(data, [self.feature_table.index(featId), 0, 0])

        # protocolNum, targetSw, pingData = getProtocolVersion(0, 0, pingData)
        elif ase == 1:
            print(f'# DEBUG: getProtocolVersion() = {self.version_major}.{self.version_minor}')
            self.protocol_reply(data,
                [self.version_major, self.version_minor, args[2]])

    def IFeatureSet(self, data, ase, args):
        # count = getCount()
        if ase == 0:
            print(f'# DEBUG: getCount() = {len(self.feature_table)}')
            self.protocol_reply(data, [len(self.feature_table)])

        # featureID, featureType, featureVersion = getFeatureID(featureIndex)
        elif ase == 1:
            featureIndex = args[0]

            if featureIndex >= len(self.feature_table):
                self.protocol_error(data, self.Errors.OutOfRange)
                return

            print(f'# DEBUG: getFeatureID({featureIndex}) = {self.feature_table[featureIndex]}')
            # we won't support any hidden features and we are also not planning
            # to support obsolete features ATM so we will set featType to 0
            print(self.feature_table[featureIndex])
            self.protocol_reply(data, [self.feature_table[featureIndex], 0, 0])

    def IFeatureInfo(self, data, ase, args):
        return


'''
Devices
'''


class LogitechGProWirelessDevice(HIDPP20Device):
    def __init__(self):
        self.name = 'Logitech G Pro'
        self.shortname = 'logitech-g-pro'
        self.info = (0x03, 0x046d, 0x4079)
        self.rdescs = [
            [
                0x05, 0x01,                    # Usage Page (Generic Desktop)        0
                0x09, 0x06,                    # Usage (Keyboard)                    2
                0xa1, 0x01,                    # Collection (Application)            4
                0x85, 0x01,                    #  Report ID (1)                      6
                0x95, 0x08,                    #  Report Count (8)                   8
                0x75, 0x01,                    #  Report Size (1)                    10
                0x15, 0x00,                    #  Logical Minimum (0)                12
                0x25, 0x01,                    #  Logical Maximum (1)                14
                0x05, 0x07,                    #  Usage Page (Keyboard)              16
                0x19, 0xe0,                    #  Usage Minimum (224)                18
                0x29, 0xe7,                    #  Usage Maximum (231)                20
                0x81, 0x02,                    #  Input (Data,Var,Abs)               22
                0x95, 0x06,                    #  Report Count (6)                   24
                0x75, 0x08,                    #  Report Size (8)                    26
                0x15, 0x00,                    #  Logical Minimum (0)                28
                0x26, 0xff, 0x00,              #  Logical Maximum (255)              30
                0x05, 0x07,                    #  Usage Page (Keyboard)              33
                0x19, 0x00,                    #  Usage Minimum (0)                  35
                0x2a, 0xff, 0x00,              #  Usage Maximum (255)                37
                0x81, 0x00,                    #  Input (Data,Arr,Abs)               40
                0x85, 0x0e,                    #  Report ID (14)                     42
                0x05, 0x08,                    #  Usage Page (LEDs)                  44
                0x95, 0x05,                    #  Report Count (5)                   46
                0x75, 0x01,                    #  Report Size (1)                    48
                0x15, 0x00,                    #  Logical Minimum (0)                50
                0x25, 0x01,                    #  Logical Maximum (1)                52
                0x19, 0x01,                    #  Usage Minimum (1)                  54
                0x29, 0x05,                    #  Usage Maximum (5)                  56
                0x91, 0x02,                    #  Output (Data,Var,Abs)              58
                0x95, 0x01,                    #  Report Count (1)                   60
                0x75, 0x03,                    #  Report Size (3)                    62
                0x91, 0x01,                    #  Output (Cnst,Arr,Abs)              64
                0xc0,                          # End Collection                      66
                0x05, 0x01,                    # Usage Page (Generic Desktop)        67
                0x09, 0x02,                    # Usage (Mouse)                       69
                0xa1, 0x01,                    # Collection (Application)            71
                0x85, 0x02,                    #  Report ID (2)                      73
                0x09, 0x01,                    #  Usage (Pointer)                    75
                0xa1, 0x00,                    #  Collection (Physical)              77
                0x05, 0x09,                    #   Usage Page (Button)               79
                0x19, 0x01,                    #   Usage Minimum (1)                 81
                0x29, 0x10,                    #   Usage Maximum (16)                83
                0x15, 0x00,                    #   Logical Minimum (0)               85
                0x25, 0x01,                    #   Logical Maximum (1)               87
                0x95, 0x10,                    #   Report Count (16)                 89
                0x75, 0x01,                    #   Report Size (1)                   91
                0x81, 0x02,                    #   Input (Data,Var,Abs)              93
                0x05, 0x01,                    #   Usage Page (Generic Desktop)      95
                0x16, 0x01, 0x80,              #   Logical Minimum (-32767)          97
                0x26, 0xff, 0x7f,              #   Logical Maximum (32767)           100
                0x75, 0x10,                    #   Report Size (16)                  103
                0x95, 0x02,                    #   Report Count (2)                  105
                0x09, 0x30,                    #   Usage (X)                         107
                0x09, 0x31,                    #   Usage (Y)                         109
                0x81, 0x06,                    #   Input (Data,Var,Rel)              111
                0x15, 0x81,                    #   Logical Minimum (-127)            113
                0x25, 0x7f,                    #   Logical Maximum (127)             115
                0x75, 0x08,                    #   Report Size (8)                   117
                0x95, 0x01,                    #   Report Count (1)                  119
                0x09, 0x38,                    #   Usage (Wheel)                     121
                0x81, 0x06,                    #   Input (Data,Var,Rel)              123
                0x05, 0x0c,                    #   Usage Page (Consumer Devices)     125
                0x0a, 0x38, 0x02,              #   Usage (AC Pan)                    127
                0x95, 0x01,                    #   Report Count (1)                  130
                0x81, 0x06,                    #   Input (Data,Var,Rel)              132
                0xc0,                          #  End Collection                     134
                0xc0,                          # End Collection                      135
                0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  136
                0x09, 0x01,                    # Usage (Vendor Usage 1)              139
                0xa1, 0x01,                    # Collection (Application)            141
                0x85, 0x10,                    #  Report ID (16)                     143
                0x75, 0x08,                    #  Report Size (8)                    145
                0x95, 0x06,                    #  Report Count (6)                   147
                0x15, 0x00,                    #  Logical Minimum (0)                149
                0x26, 0xff, 0x00,              #  Logical Maximum (255)              151
                0x09, 0x01,                    #  Usage (Vendor Usage 1)             154
                0x81, 0x00,                    #  Input (Data,Arr,Abs)               156
                0x09, 0x01,                    #  Usage (Vendor Usage 1)             158
                0x91, 0x00,                    #  Output (Data,Arr,Abs)              160
                0xc0,                          # End Collection                      162
                0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  163
                0x09, 0x02,                    # Usage (Vendor Usage 2)              166
                0xa1, 0x01,                    # Collection (Application)            168
                0x85, 0x11,                    #  Report ID (17)                     170
                0x75, 0x08,                    #  Report Size (8)                    172
                0x95, 0x13,                    #  Report Count (19)                  174
                0x15, 0x00,                    #  Logical Minimum (0)                176
                0x26, 0xff, 0x00,              #  Logical Maximum (255)              178
                0x09, 0x02,                    #  Usage (Vendor Usage 2)             181
                0x81, 0x00,                    #  Input (Data,Arr,Abs)               183
                0x09, 0x02,                    #  Usage (Vendor Usage 2)             185
                0x91, 0x00,                    #  Output (Data,Arr,Abs)              187
                0xc0,                          # End Collection                      189
                0x06, 0x00, 0xff,              # Usage Page (Vendor Defined Page 1)  190
                0x09, 0x04,                    # Usage (Vendor Usage 0x04)           193
                0xa1, 0x01,                    # Collection (Application)            195
                0x85, 0x20,                    #  Report ID (32)                     197
                0x75, 0x08,                    #  Report Size (8)                    199
                0x95, 0x0e,                    #  Report Count (14)                  201
                0x15, 0x00,                    #  Logical Minimum (0)                203
                0x26, 0xff, 0x00,              #  Logical Maximum (255)              205
                0x09, 0x41,                    #  Usage (Vendor Usage 0x41)          208
                0x81, 0x00,                    #  Input (Data,Arr,Abs)               210
                0x09, 0x41,                    #  Usage (Vendor Usage 0x41)          212
                0x91, 0x00,                    #  Output (Data,Arr,Abs)              214
                0x85, 0x21,                    #  Report ID (33)                     216
                0x95, 0x1f,                    #  Report Count (31)                  218
                0x15, 0x00,                    #  Logical Minimum (0)                220
                0x26, 0xff, 0x00,              #  Logical Maximum (255)              222
                0x09, 0x42,                    #  Usage (Vendor Usage 0x42)          225
                0x81, 0x00,                    #  Input (Data,Arr,Abs)               227
                0x09, 0x42,                    #  Usage (Vendor Usage 0x42)          229
                0x91, 0x00,                    #  Output (Data,Arr,Abs)              231
                0xc0,                          # End Collection                      233
            ]
        ]

        # HID++ 2.0 specific settings
        self.feature_table = [
            HIDPP20Features.IRoot,
            HIDPP20Features.IFeatureSet,
            HIDPP20Features.IFeatureInfo,
            HIDPP20Features.DeviceNameAndType,
            0x1d4b,
            0x0020,
            0x1001,
            0x8070,
            0x1300,
            0x8100,
            0x8110,
            0x8060,
            0x2201,
            0x1802,
            0x1803,
            0x1805,
            0x1806,
            0x1811,
            0x1830,
            0x1890,
            0x1891,
            0x18a1,
            0x1801,
            0x18b1,
            0x1df3,
            0x1e00,
            0x1eb0,
            0x1863,
            0x1e22
        ]

        super().__init__()
