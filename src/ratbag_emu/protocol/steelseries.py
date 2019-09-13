# SPDX-License-Identifier: MIT

from .base import BaseDevice


class SteelseriesReport():
    Command = 0
    Arguments = 2

    # Dpi
    DpiId = 0
    DpiSteps = 1


class SteelseriesReportType():
    ShortSize = 64
    LongSize = 262


class Steelseries2Commands():
    Dpi = 0x53
    ReportRate = 0x54
    Save = 0x59
    LEDs = 0x5b
    ReadFirmware = 0x90
    ReadSettings = 0x92


class SteelseriesDevice(BaseDevice):
    def __init__(self):
        assert hasattr(self, 'protocol_version'), 'Protocol version is missing'
        assert hasattr(self, 'hw_settings'), 'Hardware settings are missing'
        super().__init__(self.hw_settings, self.name, self.info, self.rdescs,
                         self.shortname)

        self.Commands = None
        if self.protocol_version == 1:
            pass
        elif self.protocol_version == 2:
            self.mouse_endpoint = self.keyboard_endpoint = 0
            self.media_endpoint = 1
            self.Commands = Steelseries2Commands
        elif self.protocol_version == 3:
            pass

        self.fw_version = [1, 33]

        assert self.Commands, 'Steelseries protocol v{protocol_version} not implemented'

        self.Report = SteelseriesReport
        self.ReportType = SteelseriesReportType

        self.report_size = {
            self.Commands.Dpi: self.ReportType.ShortSize,
            self.Commands.ReportRate: self.ReportType.ShortSize,
            self.Commands.Save: self.ReportType.ShortSize,
            self.Commands.LEDs: self.ReportType.LongSize,
            self.Commands.ReadFirmware: self.ReportType.ShortSize,
            self.Commands.ReadSettings: self.ReportType.ShortSize
        }

        self.commands = {
            self.Commands.Dpi: self.change_dpi,
            self.Commands.ReportRate: self.nop,
            self.Commands.Save: self.nop,
            self.Commands.LEDs: self.change_leds,
            self.Commands.ReadFirmware: self.read_firmware,
            self.Commands.ReadSettings: self.read_settings
        }

    #
    # Interface functions
    #
    def protocol_send(self, command, data):
        buf = [0] * self.report_size[command]
        buf[self.Report.Command] = command
        for i in range(len(data)):
            buf[self.Report.Arguments + i] = data[i]

        super().send_raw(buf)

    #
    # Logic definition
    #
    def protocol_receive(self, data, size, rtype):
        command = data[self.Report.Command]
        args = data[self.Report.Arguments:]

        assert len(data) == self.report_size[command], 'Wrong report size'

        self.commands[command](command, data, args)

    #
    # Command definitions
    #
    def change_dpi(self, command, data, args):
        dpi_id = args[self.Report.DpiId]
        dpi_steps = args[self.Report.DpiSteps]

        assert dpi_id == 1 or dpi_id == 2, 'Invalid DPI ID'

        dpi = self.hw_settings.dpi_step * (dpi_steps + 1)
        self.hw_settings.dpi[dpi_id - 1] = dpi
        return

    def change_leds(self, command, data, args):
        return

    def read_firmware(self, command, data, args):
        self.protocol_send(command, self.fw_version)
        return

    def read_settings(self, command, data, args):
        data = [0]
        data.append(self.hw_settings.active_dpi)
        dpi_step = self.hw_settings.dpi_step
        for dpi in self.hw_settings.dpi:
            data.append(int((dpi - dpi_step) / dpi_step))
        for color in self.hw_settings.leds:
            data += color
        self.protocol_send(command, data)
        return

    def nop(self, commandb, data, args):
        pass
