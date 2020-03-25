```mermaid
classDiagram

class Device {
    +str name
    +info Tuple[int, int, int]
    +rdescs List[List[int]]
    +report_rate int
    +endpoints List[Endpoint]
    +actuators List[Actuator]
    +hw Dict[str, HWComponent]
    +fw Firmware

    +destroy()
    +transform_action(action) %% Passes the action by the actuators and returns the transformed result ()
    +send_hid_action(action) %% Sends HID action to all endpoints (create_report -> call_input_event)
    +simulate_action(action) %% Transforms high-level action into HID timed events and sends them ()
}

class UHIDDevice

Endpoint --|> UHIDDevice : inherited
class Endpoint {
    -_owner Device
    +rdesc List[int]
    +name str
    +number int
    +uhid_dev_is_ready bool

    -_receive(data, size, rtype) %% HID data receive callback (triggers the firmware callback)
    +send(data) %% Sends HID data ()
    +create_report(action, skip_empty) %% Creates a report based on the HID data ()
}
Endpoint --> Device : owned

class Firmware {
    -_owner Device

    +hid_receive(data, size, rtype, endpoint)
    +hid_send(data, endpoint)
}
Firmware --> Device : owned

class Actuator {
    -keys List[str]

    +transforms(action) %% Transform a high-level action ()
}
Actuator --o Device : used (actuators)

class HWComponent
HWComponent --o Device : used (hw)
