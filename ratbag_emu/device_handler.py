# SPDX-License-Identifier: MIT

import hidtools.uhid
import logging
from time import time, sleep
from threading import RLock


logger = logging.getLogger('ratbagemu.devicehandler')


class DeviceHandler(object):
    devices = {}

    lock = RLock()
    pool_lock = RLock()

    @staticmethod
    def append_device(device):
        for id in DeviceHandler.devices:
            assert device.id != id
        DeviceHandler.devices[device.id] = device
        logger.debug(f'device {device.id}: added {device}')

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
        device = DeviceHandler.devices[device_id]
        logger.debug(f'device {device_id}: removed {device}')
        del DeviceHandler.devices[device_id]
        DeviceHandler.lock.release()

    @staticmethod
    def handle():
        while True:
            # TODO: we should ensure UHIDDevice deals with new devices as they
            #       are added, instead of requiring us to interrupt the poll
            hidtools.uhid.UHIDDevice.dispatch(timeout=0.5)
