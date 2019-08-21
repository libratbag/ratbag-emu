from collections import namedtuple

'''
Imeplemnts a profile with all the mouse settings
'''
class Profile(object):
    Led = namedtuple('Led', ['red', 'green', 'blue'])

    def __init__(self, obj=None):
        '''
        Hardware properties
        '''
        self.active_dpi = 0
        self.x_dpi = self.y_dpi = [
            3000,
            6000
        ]
        self.step = 100

        self.active_report_rate = 0
        self.report_rates = [ # Hz
            1000
        ]

        self.leds = [
            self.Led(0xff, 0xff, 0xff),
            self.Led(0xff, 0xff, 0xff),
        ]

        # TODO: Add buttons

        if obj is None:
            return

    @property
    def dpi(self):
        return self.x_dpi

    @dpi.setter
    def dpi(self, dpi):
        self.x_dpi = self.y_dpi = dpi

    def get_dpi_value(self):
        return self.x_dpi[self.active_dpi]

    def get_report_rate(self):
        return self.report_rates[self.active_report_rate]
