from .base import BaseDevice


class SteelseriesReport():
    Command                     = 0
    Arguments                   = 2

    # Dpi
    DpiId                       = 2
    DpiSteps                    = 3


class SteelseriesReportType():
    ShortSize                   = 64
    LongSize                    = 262


class Steelseries2Commands():
    Dpi                         = 0x53
    LEDs                        = 0x5b
    ReadFirmware                = 0x90
    ReadSettings                = 0x92


class SteelseriesDevice(BaseDevice):
    '''
    Device properties
    '''
    version_major = 1
    version_minor = 33

    step = 100

    active_dpi = 2
    dpi = [
        3000,
        6000
    ]

    led_color = [
        [0xff, 0xff, 0xff],
        [0xff, 0xff, 0xff]
    ]

    '''
    Init routine
    '''
    def __init__(self, rdesc=None, info=None, protocol_version=2,
     name='Generic Steelseries Device'):
        self.protocol = 'Steelseries v{}'.format(protocol_version)
        super().__init__(rdesc, info, name)

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
            self.Commands.LEDs:                 self.ReportType.LongSize,
            self.Commands.ReadFirmware:         self.ReportType.ShortSize,
            self.Commands.ReadSettings:         self.ReportType.ShortSize
        }

        self.commands = {
            self.Commands.Dpi:                  self.change_dpi,
            self.Commands.LEDs:                 self.change_leds,
            self.Commands.ReadFirmware:         self.read_firmware,
            self.Commands.ReadSettings:         self.read_settings
        }

    '''
    Interface functions
    '''
    def protocol_send(self, command, buf):
        data = [0] * self.report_size[command]
        data[self.Report.Command] = command
        for i in range(len(buf)):
            data[self.Report.Arguments + i] = buf[i]

        super().protocol_send(data)

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

        self.dpi[dpi_id + 1] = self.step + self.step * dpi_steps
        return

    def change_leds(self, command, data, args):
        return

    def read_firmware(self, command, data, args):
        self.protocol_send(command, [self.version_major, self.version_minor])
        return

    def read_settings(self, command, data, args):
        data = [0]
        data.append(self.active_dpi)
        data.append(self.dpi)
        data.append(self.led_color)
        self.protocol_send(command, data)
        return

