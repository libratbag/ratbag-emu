'''
Imeplemnts a profile with all the mouse settings
'''
class Profile(object):

    '''
    Hardware properties
    '''
    buttons = []

    active_dpi = 0
    dpi = [
        3000,
        6000
    ]
    step = 100

    report_rate = 1000  # Hz

    leds = [
        [0xff, 0xff, 0xff],
        [0xff, 0xff, 0xff]
    ]
