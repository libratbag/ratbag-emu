# ratbag_emu_client.DeviceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**device_move**](DeviceApi.md#device_move) | **POST** /device/{device_id}/move | Moves a simulated device
[**get_device**](DeviceApi.md#get_device) | **GET** /device/{device_id} | Returns a simulated device
[**list_devices**](DeviceApi.md#list_devices) | **GET** /device | List of simulated devices


# **device_move**
> device_move(device_id, movement_data)

Moves a simulated device

Send movement data to the target device

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()
device_id = 'device_id_example' # str | ID of the device to return
movement_data = ratbag_emu_client.MovementData() # MovementData | Movement data

try:
    # Moves a simulated device
    api_instance.device_move(device_id, movement_data)
except ApiException as e:
    print("Exception when calling DeviceApi->device_move: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| ID of the device to return | 
 **movement_data** | [**MovementData**](MovementData.md)| Movement data | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Error moving the device |  -  |
**404** | Device not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device**
> Device get_device(device_id)

Returns a simulated device

Returns one the of devices currently simulated by ratbag-emu

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()
device_id = 'device_id_example' # str | ID of the device to return

try:
    # Returns a simulated device
    api_response = api_instance.get_device(device_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeviceApi->get_device: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| ID of the device to return | 

### Return type

[**Device**](Device.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**404** | Device not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_devices**
> list[Device] list_devices()

List of simulated devices

Provides the list of devices that are being currently simulated by ratbag-emu

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()

try:
    # List of simulated devices
    api_response = api_instance.list_devices()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeviceApi->list_devices: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Device]**](Device.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

