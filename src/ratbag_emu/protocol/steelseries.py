from .base import BaseDevice


class SteelseriesReport():
    Command                     = 0
    Arguments                   = 2

    # Dpi
    DpiId                       = 0
    DpiSteps                    = 1


class SteelseriesReportType():
    ShortSize                   = 64
    LongSize                    = 262


class Steelseries2Commands():
    Dpi                         = 0x53
    ReportRate                  = 0x54
    Save                        = 0x59
    LEDs                        = 0x5b
    ReadFirmware                = 0x90
    ReadSettings                = 0x92


class SteelseriesDevice(BaseDevice):
    '''
    Device properties
    '''
    version_major = 1
    version_minor = 33

    '''
    Init routine
    '''
    def __init__(self, rdesc=None, info=None,name='Generic Steelseries Device',
                 shortname='generic-steelseries', protocol_version=2):
        self.protocol = 'Steelseries v{}'.format(protocol_version)
        super().__init__(rdesc, info, name, shortname)

        self.Commands = None
        if protocol_version == 1:
            pass
        elif protocol_version == 2:
            self.Commands = Steelseries2Commands
        elif protocol_version == 3:
            pass

        assert self.Commands is not None, \
            'Steelseries v{} not implemented'.format(protocol_version)

        self.Report     = SteelseriesReport
        self.ReportType = SteelseriesReportType

        self.report_size = {
            self.Commands.Dpi:                  self.ReportType.ShortSize,
            self.Commands.ReportRate:           self.ReportType.ShortSize,
            self.Commands.Save:                 self.ReportType.ShortSize,
            self.Commands.LEDs:                 self.ReportType.LongSize,
            self.Commands.ReadFirmware:         self.ReportType.ShortSize,
            self.Commands.ReadSettings:         self.ReportType.ShortSize
        }

        self.commands = {
            self.Commands.Dpi:                  self.change_dpi,
            self.Commands.ReportRate:           self.nop,
            self.Commands.Save:                 self.nop,
            self.Commands.LEDs:                 self.change_leds,
            self.Commands.ReadFirmware:         self.read_firmware,
            self.Commands.ReadSettings:         self.read_settings
        }

    '''
    Interface functions
    '''
    def protocol_send(self, command, data):
        buf = [0] * self.report_size[command]
        buf[self.Report.Command] = command
        for i in range(len(data)):
            buf[self.Report.Arguments + i] = data[i]

        super().protocol_send(buf)

    '''
    Logic definition
    '''
    def protocol_receive(self, data, size, rtype):
        command     = data[self.Report.Command]
        args        = data[self.Report.Arguments:]

        assert len(data) == self.report_size[command], \
               'Wrong report size. Expected {}, got {}'. \
               format(self.report_size[command], len(data))

        self.commands[command](command, data, args)

    '''
    Command definitions
    '''
    def change_dpi(self, command, data, args):
        dpi_id      = args[self.Report.DpiId]
        dpi_steps   = args[self.Report.DpiSteps]

        assert dpi_id == 1 or dpi_id == 2, 'Invalid DPI ID'

        self.dpi[dpi_id - 1] = self.step + self.step * dpi_steps
        return

    def change_leds(self, command, data, args):
        return

    def read_firmware(self, command, data, args):
        self.protocol_send(command, [self.version_major, self.version_minor])
        return

    def read_settings(self, command, data, args):
        data = [0]
        data.append(self.active_dpi)
        for dpi in self.dpi:
            data.append(int((dpi - self.step) / self.step))
        for color in self.leds:
            data += color
        self.protocol_send(command, data)
        return

    def nop(self, commandb, data, args):
        pass

