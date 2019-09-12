from .base import BaseDevice


class HIDPP20Report():
    ReportType = 0
    Device = 1
    Feature = 2
    ASE = 3
    Arguments = 4


class HIDPP20ReportType():
    Short = 0x10
    Long = 0x11
    ShortSize = 7
    LongSize = 20


class HIDPP20Features():
    IRoot = 0x0000
    IFeatureSet = 0x0001
    IFeatureInfo = 0x0002
    DeviceInformation = 0x0003
    DeviceNameAndType = 0x0005
    DeviceGroups = 0x0006
    ConfigChange = 0x0020
    UniqueIdentifier = 0x0021
    WirelessSignalStrength = 0x0080
    DFUControl0 = 0x00c0
    DFUControl1 = 0x00c1
    DFU = 0x00d0


class HIDPP20Errors():
    NoError = 0
    Unknown = 1
    InvalidArgument = 2
    OutOfRange = 3
    HWError = 4
    LogitechInternal = 5
    INVALID_FEATURE_INDEX = 6
    INVALID_FUNCTION_ID = 7
    Busy = 8
    Unsupported = 9


class HIDPP20Device(BaseDevice):
    # Internal variables

    def __init__(self):
        assert hasattr(self, 'feature_table'), 'Feature table missing'
        super().__init__({}, self.name, self.info, self.rdescs, self.shortname, id=self.id)

        # Protocol declarations
        self.Report = HIDPP20Report
        self.ReportType = HIDPP20ReportType
        self.Features = HIDPP20Features
        self.Errors = HIDPP20Errors

        self.report_size = {
            self.ReportType.Short: self.ReportType.ShortSize,
            self.ReportType.Long: self.ReportType.LongSize
        }

        # Function mapping
        self.features = {
            self.Features.IRoot: self.IRoot,
            self.Features.IFeatureSet: self.IFeatureSet,
            self.Features.IFeatureInfo: self.IFeatureInfo
        }

        self.events = {}

        # Device proprieties
        self.version_major = 4
        self.version_minor = 2

        self.expecting_reply = False

    #
    # Interface functions
    #
    def protocol_send(self, report_type, device, feature, ase, sw_id, args):
        data = [0] * self.report_size[report_type]
        data[self.Report.ReportType] = report_type
        data[self.Report.Device] = device
        data[self.Report.Feature] = feature
        data[self.Report.ASE] = ase << 4 + sw_id
        for i in range(len(args)):
            data[self.Report.Arguments + i] = args[i]

        super().send_raw(data)

    def protocol_reply(self, data, args):
        assert len(data) >= self.Report.Arguments + len(args), 'Report too small to send the arguments'

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

    #
    # Logic definition
    #
    def protocol_receive(self, data, size, rtype):
        report_type = data[self.Report.ReportType]
        feature = data[self.Report.Feature]
        ase = data[self.Report.ASE] >> 4
        args = data[self.Report.Arguments:]

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

    #
    # Event definitions
    #

    #
    # Feature definitions
    #
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
                                [self.version_major,
                                 self.version_minor,
                                 args[2]])

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
