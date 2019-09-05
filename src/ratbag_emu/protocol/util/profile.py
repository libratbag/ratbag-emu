from collections import namedtuple


'''
Imeplemnts a profile with all the mouse settings
'''
class Profile(object):
    Led = namedtuple('Led', ['red', 'green', 'blue'])

    class Button(object):
        def __init__(action_type, val=None):
            self.action_type = action_type
            self.button = None
            self.special = None
            self.macro = None

            setattr(self, self.action_type, val)

    def __init__(self, obj):
        '''
        Hardware properties
        '''
        self.default_dpi = None
        self.active_dpi = None
        self.dpi = []
        if 'resolutions' in obj:
            for i, dpi in enumerate(obj['resolutions']):
                self.dpi.append(dpi['xres'])
                try:
                    if dpi['is_active']:
                        self.active_dpi = i
                except KeyError:
                    pass
                try:
                    if dpi['is_default']:
                        self.default_dpi = i
                except KeyError:
                    pass
            try:
                self.dpi_step = obj['dpi_step']
            except KeyError:
                pass

        self.active_report_rate = 0
        self.report_rates = [] # Hz
        try:
            self.report_rates = obj['report_rates']
        except KeyError:
            pass

        try:
            if not self.report_rates:
                self.report_rates.append(obj['rate'])
            else:
                self.active_report_rate = self.report_rates.index(obj['rate'])
        except KeyError:
            pass

        if not self.report_rates:
            self.report_rates.append(10000)
            self.active_report_rate = 0

        self.leds = []
        if 'leds' in obj:
            for led in obj['leds']:
                try:
                    self.leds.append(self.Led(*led['color']))
                except KeyError:
                    self.leds.append(self.Led(0xFF, 0xFF, 0xFF))

        self.buttons = []
        if 'buttons' in obj:
            for btn in obj['buttons']:
                if btn['action_type'] != 'none':
                    self.buttons.append(self.Button(btn['action_type'], btn[btn['action_type']]))
                else:
                    self.buttons.append(self.Button(btn['action_type']))

        self.is_disabled = False
        try:
            self.is_disabled = obj['is_disabled']
        except KeyError:
            pass

    def get_dpi_value(self):
        return self.dpi[self.active_dpi]

    def get_report_rate(self):
        return self.report_rates[self.active_report_rate]
