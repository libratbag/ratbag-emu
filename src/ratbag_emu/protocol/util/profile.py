'''
Imeplemnts a profile with all the mouse settings
'''
class Profile(object):

    '''
    Hardware properties
    '''
    buttons = []

    active_dpi = 0
    x_dpi = y_dpi = [
        3000,
        6000
    ]
    step = 100

    report_rate = 1000  # Hz

    leds = [
        [0xff, 0xff, 0xff],
        [0xff, 0xff, 0xff]
    ]

    def __init__(self, obj=None):
        if obj is None:
            return
        for i, profile in enumerate(obj):
            if hasattr(profile, 'is_active'):
                if not getattr(profile, 'is_active'):
                    continue

            if hasattr(profile, 'resolutions'):
                for i, res in enumerate(getattr(profile, 'resolutions')):
                    self.x_dpi[i] = getattr(res, 'xres')
                    self.y_dpi[i] = getattr(res, 'yres')

                    if hasattr(res, 'is_active'):
                        if getattr(res, 'is_active'):
                            self.active_dpi = i

    @property
    def dpi(self):
        return self.x_dpi

    @dpi.setter
    def dpi(self, dpi):
        self.x_dpi = self.y_dpi = dpi
