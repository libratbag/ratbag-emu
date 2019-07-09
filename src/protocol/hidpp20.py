from .base import BaseDevice


class HIDPPReport():
    ReportType                  = 0
    Device                      = 1
    Feature                     = 2
    ASE                         = 3
    Arguments                   = 4


class HIDPPReportType():
    Short                       = 0x10
    Long                        = 0x11
    ShortSize                   = 7
    LongSize                    = 20


class HIDPPFeatures():
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


class HIDPP20Device(BaseDevice):
    '''
    Device properties
    '''
    version_major = 4
    version_minor = 2

    '''
    Internal variables
    '''
    expecting_reply = False

    '''
    Init routine
    '''
    def __init__(self, rdesc=None, info=None, name='Generic HID++ 2.0 Device'):
        self.protocol = 'HID++ 2.0'
        super().__init__(rdesc, info, name)

        self.Report         = HIDPPReport
        self.ReportType     = HIDPPReportType
        self.Features       = HIDPPFeatures

        self.features = {
            self.Features.IRoot:                self.IRoot,
            self.Features.IFeatureSet:          self.IFeatureSet,
            self.Features.IFeatureInfo:         self.IFeatureInfo
        }

        self.report_size = {
            self.ReportType.Short:              self.ReportType.ShortSize,
            self.ReportType.Long:               self.ReportType.LongSize
        }

        self.events = {}

    '''
    Interface functions
    '''
    def protocol_send(report_type, device, feature, ase, sw_id, args):
        data = [0] * self.report_size[report_type]
        data[self.Report.ReportType]    = report_type
        data[self.Report.Device]        = device
        data[self.Report.Feature]       = feature
        data[self.Report.ASE]           = ase << 4 + sw_id
        for i in range(len(args)):
            data[self.Report.Arguments + i] = args[i]

        super().protocol_send(data)

    def protocol_reply(self, data, args):
        assert len(data) >= self.Report.Arguments + len(args), \
               'Report too small to send the arguments'

        for i in range(len(args)):
            data[self.Report.Arguments + i] = args[i]

        super().protocol_send(data)

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

        assert report_type in self.report_size, \
               'Invalid report type ({:2x})'.format(report_type)

        assert len(data) == self.report_size[report_type], \
               'Wrong report size. Expected {}, got {}'. \
               format(self.report_size[report_type], len(data))

        # Event
        if self.expecting_reply:
            return
        # Function
        else:
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
            return

        # protocolNum, targetSw, pingData = getProtocolVersion(0, 0, pingData)
        elif ase == 1:
            self.protocol_reply(data, [4, 2, args[2]])

    def IFeatureSet(self, data, ase, args):
        return

    def IFeatureInfo(self, data, ase, args):
        return

