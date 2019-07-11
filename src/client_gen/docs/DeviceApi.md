# ratbag_emu_client.DeviceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_device**](DeviceApi.md#add_device) | **GET** /devices/add | Creates a simulated device
[**device_event**](DeviceApi.md#device_event) | **POST** /devices/{device_id}/event | Send an event to a simulated device
[**get_device**](DeviceApi.md#get_device) | **GET** /devices/{device_id} | Returns a simulated device
[**list_devices**](DeviceApi.md#list_devices) | **GET** /devices | List of simulated devices


# **add_device**
> list[Device] add_device()

Creates a simulated device

Tells ratbag-emu to create a new simulated device

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
    # Creates a simulated device
    api_response = api_instance.add_device()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeviceApi->add_device: %s\n" % e)
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

# **device_event**
> device_event(device_id, event_data)

Send an event to a simulated device

Send raw HID event data to the target device

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()
device_id = 56 # int | ID of the device to return
event_data = ratbag_emu_client.EventData() # EventData | Event data

try:
    # Send an event to a simulated device
    api_instance.device_event(device_id, event_data)
except ApiException as e:
    print("Exception when calling DeviceApi->device_event: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **int**| ID of the device to return | 
 **event_data** | [**EventData**](EventData.md)| Event data | 

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
**400** | Error sending data to the device |  -  |
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
device_id = 56 # int | ID of the device to return

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
 **device_id** | **int**| ID of the device to return | 

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

