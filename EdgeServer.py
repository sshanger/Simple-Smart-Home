
import json
import time
import DeviceType
import paho.mqtt.client as mqtt
import CommandType

HOST = "localhost"
PORT = 1883     
WAIT_TIME = 0.25

class Edge_Server:
    
    def __init__(self, instance_name):
        
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []
        self._device_status_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe(f"home/register/", 0)
        
    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        recieved_message = json.loads(msg.payload)
        if recieved_message['device_id']:
            if 'register_flag' in recieved_message:
                self.register_devices(recieved_message['device_type'],
                                      recieved_message['device_id'],
                                      recieved_message['room'])
            elif 'Registration' in recieved_message:
                self._device_status_list.append(recieved_message)
            elif 'command_response_type' in recieved_message:
                recieved_message.pop('command_response_type')
                self._device_status_list.append(recieved_message)


    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices by device_type
    def get_status_device_type(self, device_type):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        for device in device_list:
            if device_type.upper() == DeviceType.DeviceType.ALL.name or device['device_type'] == device_type:
                payload = {'command_type': CommandType.CommandType.GET_SWITCH_STATUS.value}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
        time.sleep(WAIT_TIME)
        if (len(self._device_status_list) > 0):
            return self._device_status_list

    # Getting the status for the connected devices by Room
    def get_status_room(self, room):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        for device in device_list:
            if room == "all" or room == device['room']:
                payload = {'command_type': CommandType.CommandType.GET_SWITCH_STATUS.value}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
        time.sleep(WAIT_TIME)
        if (len(self._device_status_list) > 0):
            return self._device_status_list

    # Getting the status for the connected devices by device_id
    def get_status_deviceid(self, device_id):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device['device_id'] == device_id or device_id.lower() == "all":
                payload = {'command_type': CommandType.CommandType.GET_SWITCH_STATUS.value}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i+1
        if i == 0:
            return f"device_id {device_id} is not registered."
        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0 :
            return self._device_status_list

    # Getting the intensity value for the device only if it is a valid Light Device
    def get_light_intensity_device_id(self, device_id):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device['device_id'] == device_id or device_id.lower() == "all" \
                    and device['device_type'] == DeviceType.DeviceType.LIGHT:
                payload = {'command_type': CommandType.CommandType.GET_LIGHT_INTENSITY.value}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1
        if i == 0:
            return f"device_id {device_id} is not registered."
        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list


    # Getting the intensity value for the device only if it is a valid AC Device
    def get_temperature_device_id(self, device_id):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if (device['device_id'] == device_id or device_id.lower() == "all" and device['device_type'] == DeviceType.DeviceType.AC):
                payload = {'command_type': CommandType.CommandType.GET_TEMPERATURE.value}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1
        if i == 0:
            return f"device_id {device_id} is not registered."
        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
           return self._device_status_list

    # This method publish and subscribes to the appropriate topic.
    def pub_sub_device_status(self, device, payload):
        self.client.publish(f"home/{device['room']}/{device['device_type']}/{device['device_id']}", str(payload))
        self.client.subscribe(f"home/{device['room']}/{device['device_type']}/{device['device_id']}/status", 0)

    # Controlling and performing the operations on the devices by device id or all devices
    # based on the request received
    def set_switch_status_by_deviceid(self, device_id, switch_status):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device['device_id'] == device_id or device_id.lower() == "all":
                payload = {'command_type': CommandType.CommandType.SET_SWITCH_STATUS.value,
                           'set_switch_value': switch_status}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1
        if i == 0:
            return f"device_id {device_id} is not registered."
        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

    # Controlling and performing the operations on the devices by room or all devices in the home
    # based on the request received
    def set_switch_status_by_room(self, room, switch_status):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device['room'] == room or room.lower() == "all":
                payload = {'command_type': CommandType.CommandType.SET_SWITCH_STATUS.value,
                           'set_switch_value': switch_status}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1
        if i == 0:
            return f"Room {room} is not a valid room in the home."
        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

    # Controlling and performing the operations on the devices by room or all devices in the home
    # based on the request received
    def set_switch_status_by_device_type(self, device_type, switch_status):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device['device_type'] == device_type or device_type.lower() == "all":
                payload = {'command_type': CommandType.CommandType.SET_SWITCH_STATUS.value,
                           'set_switch_value': switch_status}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1

            if i == 0:
                return f"DeviceType {device_type} is not a valid device type in the home."

        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

    # Controlling and performing the operations on the devices by room or all devices in the home
    # based on the request received
    def set_light_intensity_by_room(self, room, light_intensity):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if (device['room'].lower() == room.lower() or room.lower() == "all") and \
                    (device['device_type'] == DeviceType.DeviceType.LIGHT.name):
                payload = {'command_type': CommandType.CommandType.SET_LIGHT_INTENSITY.value,
                            'set_light_intensity': light_intensity}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1

        if i == 0:
            return f"Room {room} doesn't have any light device to set the intensity."

        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

    # Controlling and performing the operations on the devices by room or all devices in the home
    # based on the request received
    def set_light_intensity_by_deviceid(self, device_id, light_intensity):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device_id.lower() == "all" or device['device_id'] == device_id \
                    and device['device_type'] == DeviceType.DeviceType.LIGHT.name:
                payload = {'command_type': CommandType.CommandType.SET_LIGHT_INTENSITY.value,
                           'set_light_intensity': light_intensity}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1

        if i == 0:
            return f"Device id {device_id} is not a light device."

        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

        # Controlling and performing the operations on the devices by room or all devices in the home
        # based on the request received

    def set_temperature_by_room(self, room, temperature):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if (device['room'].lower() == room.lower() or room.lower() == "all") and \
                    (device['device_type'] == DeviceType.DeviceType.AC.name):
                payload = {'command_type': CommandType.CommandType.SET_TEMPERATURE.value,
                           'set_temperature': temperature}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1

        if i == 0:
            return f"Room {room} doesn't have any AC device to set the temperature."

        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

        # Controlling and performing the operations on the devices by room or all devices in the home
        # based on the request received

    def set_temperature_by_deviceid(self, device_id, temperature):
        device_list = self.get_registered_device_list()
        self._device_status_list = []
        i = 0
        for device in device_list:
            if device_id.lower() == "all" or device['device_id'] == device_id \
                    and device['device_type'] == DeviceType.DeviceType.AC.name:
                payload = {'command_type': CommandType.CommandType.SET_TEMPERATURE.value,
                           'set_temperature': temperature}
                command_payload = json.dumps(payload)
                self.pub_sub_device_status(device, command_payload)
                i = i + 1

        if i == 0:
            return f"Device id {device_id} is not an AC device."

        time.sleep(WAIT_TIME)
        if len(self._device_status_list) > 0:
            return self._device_status_list

    # Method to Register the devices
    # Check the device type is supported and return error for invalid type
    # Only when the above condition passes register the device.
    def register_devices(self, devicetype, deviceid, room):
        if devicetype == DeviceType.DeviceType.AC.name:
            return self.__register_ac(deviceid, room)
        elif devicetype == DeviceType.DeviceType.LIGHT.name:
            return self.__register_light(deviceid, room)

    def __register_ac(self, deviceid, room):
        self._device_status_list = []
        already_registered = False
        for device in self._registered_list:
            if device['device_id'] == deviceid:
                already_registered = True

        if already_registered:
            command = {'registration': 'Failure', 'device_id': deviceid, 'status_code': 400,
                       'error': f"{deviceid} is already registered."}
        else:
            device_properties = {'device_id': deviceid, 'device_type': DeviceType.DeviceType.AC.name,
                                 'room': room}
            self._registered_list.append(device_properties)
            command = {'registration': 'success', 'device_id': deviceid, 'status_code': 200}

        payload = json.dumps(command)
        self.client.publish(f'home/register_status/{deviceid}', str(payload))

    def __register_light(self, deviceid, room):
        already_registered = False
        for device in self._registered_list:
            if device['device_id'] == deviceid:
                already_registered = True

        if already_registered:
            command = {'registration': 'Failure', 'device_id': deviceid, 'status_code': 400,
                       'error': f"{deviceid} is already registered."}
        else:
            device_properties = {'device_id': deviceid, 'device_type': DeviceType.DeviceType.LIGHT.name, 'room': room}
            self._registered_list.append(device_properties)
            command = {'registration': 'success', 'device_id': deviceid, 'status_code': 200}
        payload = json.dumps(command)
        self.client.publish(f'home/register_status/{deviceid}', str(payload))