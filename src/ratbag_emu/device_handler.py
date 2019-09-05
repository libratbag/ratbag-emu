from time import time, sleep
from threading import RLock

from .protocol.util.descriptors import report_descriptor_simple, \
                                       report_descriptor_g_pro
from .protocol.hidpp20 import HIDPP20Device
from .protocol.steelseries import SteelseriesDevice


class DeviceHandler(object):
    devices = {}
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
    def wait_for_device_nodes(device_id, timeout=3):
        start = time()
        for endpoint in DeviceHandler.devices[device_id].endpoints:
            while not endpoint.device_nodes or len(endpoint.device_nodes) == 0:
                sleep(0.1)
                if time() > start + timeout:
                    return

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
        del DeviceHandler.devices[device_id]
        DeviceHandler.lock.release()

    @staticmethod
    def handle():
        while True:
            DeviceHandler.lock.acquire()
            devices = DeviceHandler.devices.copy()
            DeviceHandler.lock.release()
            for device in devices.values():
                if device is not None:
                    DeviceHandler.pool_lock.acquire()
                    device.dispatch()
                    DeviceHandler.pool_lock.release()
