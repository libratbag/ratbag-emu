# SPDX-License-Identifier: MIT

import hidtools.uhid
from time import time, sleep
from threading import RLock


class DeviceHandler(object):
    devices = {}
    cur_id = -1

    lock = RLock()
    pool_lock = RLock()

    @staticmethod
    def append_device(device):
        DeviceHandler.lock.acquire()
        DeviceHandler.cur_id += 1
        # TODO: ensure we do not overwrite a previous ID set in device
        device.id = DeviceHandler.cur_id
        DeviceHandler.devices[device.id] = device
        DeviceHandler.lock.release()

    @staticmethod
    def wait_for_device_nodes(device_id, timeout=3):
        start = time()
        for endpoint in DeviceHandler.devices[device_id].endpoints:
            while not endpoint.device_nodes:
                sleep(0.1)
                if time() > start + timeout:
                    return

    @staticmethod
    def get_device(device_id):
        DeviceHandler.lock.acquire()
        ret = {
            'id': device_id,
            'name': DeviceHandler.devices[device_id].name,
            'shortname': DeviceHandler.devices[device_id].shortname,
            'input_nodes': DeviceHandler.devices[device_id].device_nodes
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
            # TODO: we should ensure UHIDDevice deals with new devices as they
            #       are added, instead of requiring us to interrupt the poll
            hidtools.uhid.UHIDDevice.dispatch(timeout=0.5)
