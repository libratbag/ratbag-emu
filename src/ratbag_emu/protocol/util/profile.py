from collections import namedtuple


class Profile(object):
    '''
    Implements a profile with all the mouse settings
    '''
    Led = namedtuple('Led', ['red', 'green', 'blue'])

    class Button(object):
        def __init__(self, action_type, val=None):
            self.action_type = action_type
            self.button = None
            self.special = None
            self.macro = None

            setattr(self, self.action_type, val)

    def __init__(self, obj):
        '''
        Hardware properties
        '''

        # DPI
        self.default_dpi = None
        self.active_dpi = None
        self.dpi = []

        resolutions = obj.get('resolutions', {})
        for i, dpi in enumerate(resolutions):
            self.dpi.append(dpi['xres'])
            if dpi.get('is_active') is True:
                self.active_dpi = i
            if dpi.get('is_default') is True:
                self.default_dpi = i
            if dpi.get('dpi_step'):
                self.dpi_step = dpi.get('dpi_step')

        if not self.dpi:
            self.dpi = [1000]
            self.active_dpi = self.default_dpi = 0

        # Report Rates
        self.active_report_rate = 0
        self.report_rates = obj.get('report_rates', [])  # Hz

        if not self.report_rates:
            self.report_rates.append(obj.get('rate', 1000))
        else:
            self.active_report_rate = self.report_rates.index(obj['rate'])

        # LEDs
        self.leds = []

        leds = obj.get('leds', [])
        for led in leds:
            if led.get('color'):
                self.leds.append(self.Led(*led['color']))
            else:
                self.leds.append(self.Led(0xFF, 0xFF, 0xFF))

        # Buttons
        self.buttons = []

        buttons = obj.get('buttons', [])
        for btn in buttons:
            if btn['action_type'] != 'none':
                self.buttons.append(self.Button(btn['action_type'],
                                    btn[btn['action_type']]))
            else:
                self.buttons.append(self.Button(btn['action_type']))

        self.is_disabled = obj.get('is_disabled', False)

    def get_dpi_value(self):
        return self.dpi[self.active_dpi]

    def get_report_rate(self):
        return self.report_rates[self.active_report_rate]
