# SPDX-License-Identifier: MIT

import os
import sys
f = os.readlink(__file__) if os.path.islink(__file__) else __file__
path = os.path.realpath(os.path.join(f, "..", "..", "src"))

if path not in sys.path:
    sys.path.insert(0, path)

import fcntl  # noqa: 402
import threading  # noqa: 402

import libevdev  # noqa: 402
import pyudev  # noqa: 402

import ratbag_emu  # noqa: 402

import pytest  # noqa: 402
import shutil  # noqa: 402
import subprocess  # noqa: 402

from pathlib import Path  # noqa: 402
from time import sleep  # noqa: 402

from ratbag_emu.util import EventData  # noqa: 402


class TestBase(object):
    def reload_udev_rules(self):
        subprocess.run('udevadm control --reload-rules'.split())

    @pytest.fixture(scope='session', autouse=True)
    def udev_rules(self):
        rules_file = '61-ratbag-emu-ignore-test-devices.rules'
        rules_dir = Path('/run/udev/rules.d')

        rules_src = Path('rules.d') / rules_file
        rules_dest = rules_dir / rules_file

        rules_dir.mkdir(exist_ok=True)
        shutil.copyfile(rules_src, rules_dest)
        self.reload_udev_rules()

        yield

        if rules_dest.is_file():
            rules_dest.unlink()
            self.reload_udev_rules()

    @pytest.fixture()
    def events(self, device, endpoint=0):
        events = []
        for d in pyudev.Context().list_devices(subsystem='input'):
            if 'NAME' in list(d.properties) and d.properties['NAME'].startswith(f'"ratbag-emu {device.id}'):
                for c in d.children:
                    if c.properties['DEVNAME'].startswith('/dev/input/event'):
                        events.append(c.properties['DEVNAME'])

        return events

    def catch_evdev_events(self, device, events, callback, wait=1):
        evdev_devices = []
        for node in events:
            fd = open(node, 'rb')
            fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
            evdev_devices.append(libevdev.Device(fd))

        evs = []
        def collect_events(stop):  # noqa: 306
            nonlocal evs
            while not stop.is_set():
                for evdev_device in evdev_devices:
                    evs += list(evdev_device.events())

        stop_event_thread = threading.Event()
        event_thread = threading.Thread(target=collect_events,
                                        args=(stop_event_thread,))
        event_thread.start()

        callback(device)

        sleep(wait)
        stop_event_thread.set()
        event_thread.join()

        for evdev_device in evdev_devices:
            evdev_device.fd.close()

        received = EventData()
        for e in evs:
            if e.matches(libevdev.EV_REL.REL_X):
                received.x += e.value
            elif e.matches(libevdev.EV_REL.REL_Y):
                received.y += e.value

        return received

    def simulate(self, device, events, action):
        def callback(device):
            nonlocal action
            device.simulate_action(action)

        return self.catch_evdev_events(device, events, callback, wait=action['duration']/1000 + 0.5)
