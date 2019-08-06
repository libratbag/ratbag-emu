from time import sleep
from threading import RLock

from .protocol.util.descriptors import report_descriptor_simple, \
                                       report_descriptor_g_pro
from .protocol.hidpp20 import HIDPP20Device
from .protocol.steelseries import SteelseriesDevice


class DeviceHandler(object):
    devices = dict()
    cur_id = -1

    lock = RLock()
    pool_lock = RLock()

    @staticmethod
    def append_device(device):
        DeviceHandler.lock.acquire()
        DeviceHandler.cur_id += 1
        DeviceHandler.devices[DeviceHandler.cur_id] = device
        DeviceHandler.lock.release()

    @staticmethod
    def get_device(device_id):
        DeviceHandler.lock.acquire()
        ret = {
            'id':           device_id,
            'name':         DeviceHandler.devices[device_id].name,
            'shortname':    DeviceHandler.devices[device_id].shortname,
            'input_nodes':  DeviceHandler.devices[device_id].device_nodes
        }
        DeviceHandler.lock.release()
        return ret

    @staticmethod
    def destroy_device(device_id):
        DeviceHandler.lock.acquire()
        DeviceHandler.devices[device_id].destroy()
        DeviceHandler.devices[device_id] = None
        DeviceHandler.lock.release()

    @staticmethod
    def handle():
        name = 'Simple Device'

        DeviceHandler.append_device(HIDPP20Device(
            report_descriptor_simple, (0x3, 0x0001, 0x0001), [], name))

        while True:
            DeviceHandler.lock.acquire()
            devices = DeviceHandler.devices.copy()
            DeviceHandler.lock.release()
            for device_id, device in devices.items():
                if device is not None:
                    DeviceHandler.pool_lock.acquire()
                    device.dispatch()
                    DeviceHandler.pool_lock.release()
