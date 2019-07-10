# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from ratbag_emu_server.models.device import Device  # noqa: E501
from ratbag_emu_server.models.movement_data import MovementData  # noqa: E501
from ratbag_emu_server.test import BaseTestCase


class TestDeviceController(BaseTestCase):
    """DeviceController integration test stubs"""

    def test_device_move(self):
        """Test case for device_move

        Moves a simulated device
        """
        movement_data = {
  "x" : 0,
  "y" : 6
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/device/{device_id}/move'.format(device_id='device_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(movement_data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_device(self):
        """Test case for get_device

        Returns a simulated device
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/device/{device_id}'.format(device_id='device_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_devices(self):
        """Test case for list_devices

        List of simulated devices
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/device',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
