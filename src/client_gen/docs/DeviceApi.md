# ratbag_emu_client.DeviceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ratbag_emu_server_add_device**](DeviceApi.md#ratbag_emu_server_add_device) | **GET** /devices/add/{shortname} | Creates a simulated device
[**ratbag_emu_server_device_event**](DeviceApi.md#ratbag_emu_server_device_event) | **POST** /devices/{device_id}/event | Send an event to a simulated device
[**ratbag_emu_server_get_device**](DeviceApi.md#ratbag_emu_server_get_device) | **GET** /devices/{device_id} | Returns a simulated device
[**ratbag_emu_server_list_devices**](DeviceApi.md#ratbag_emu_server_list_devices) | **GET** /devices | List of simulated devices


# **ratbag_emu_server_add_device**
> ratbag_emu_server_add_device(shortname)

Creates a simulated device

Tells ratbag-emu to create a new simulated device

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()
shortname = 'shortname_example' # str | Short name name of the device to add

try:
    # Creates a simulated device
    api_instance.ratbag_emu_server_add_device(shortname)
except ApiException as e:
    print("Exception when calling DeviceApi->ratbag_emu_server_add_device: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shortname** | **str**| Short name name of the device to add | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Can&#39;t add device |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ratbag_emu_server_device_event**
> ratbag_emu_server_device_event(device_id, request_body)

Send an event to a simulated device

Send HID event data to the target device

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()
device_id = 56 # int | ID of the device to use as the event source
request_body = None # list[dict(str, int)] | Event data

try:
    # Send an event to a simulated device
    api_instance.ratbag_emu_server_device_event(device_id, request_body)
except ApiException as e:
    print("Exception when calling DeviceApi->ratbag_emu_server_device_event: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **int**| ID of the device to use as the event source | 
 **request_body** | [**list[dict(str, int)]**](dict.md)| Event data | 

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

# **ratbag_emu_server_get_device**
> object ratbag_emu_server_get_device(device_id)

Returns a simulated device

Returns one the of devices currently simulated by ratbag-emu

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()
device_id = 56 # int | ID of the device to return

try:
    # Returns a simulated device
    api_response = api_instance.ratbag_emu_server_get_device(device_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeviceApi->ratbag_emu_server_get_device: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **int**| ID of the device to return | 

### Return type

**object**

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

# **ratbag_emu_server_list_devices**
> object ratbag_emu_server_list_devices()

List of simulated devices

Provides the list of devices that are being currently simulated by ratbag-emu

### Example

```python
from __future__ import print_function
import time
import ratbag_emu_client
from ratbag_emu_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = ratbag_emu_client.DeviceApi()

try:
    # List of simulated devices
    api_response = api_instance.ratbag_emu_server_list_devices()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeviceApi->ratbag_emu_server_list_devices: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

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

