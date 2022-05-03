import json
import paho.mqtt.client as mqtt
import CommandType

HOST = "localhost"
PORT = 1883


class Light_Device():
    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]
    _SUCCESS = 200
    _BAD_REQUEST = 400

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"
        self._registration_status = []

    def _register_device(self, device_id, room_type, device_type):
        self._device_registration_flag = True
        self._registration_status = []
        device_properties = {'device_id': device_id, 'device_type': device_type, 'room': room_type,
                             'register_flag': self._device_registration_flag}
        msgpayload = json.dumps(device_properties)
        self.client.publish(f"home/register/", str(msgpayload))
        self.client.subscribe(f'home/register_status/{device_id}', 0)

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe(f"home/{self._room_type}/{self._device_type}/{self._device_id}", 0)

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        msgpayload = json.loads(msg.payload)
        if ("command_type" in msgpayload):
            if msgpayload["command_type"] == CommandType.CommandType.GET_SWITCH_STATUS.value:
                self._get_switch()
            elif msgpayload["command_type"] == CommandType.CommandType.SET_SWITCH_STATUS.value:
                if msgpayload["set_switch_value"] == "OFF" or msgpayload["set_switch_value"] == "ON":
                    self._set_switch(msgpayload)
            elif msgpayload["command_type"] == CommandType.CommandType.GET_LIGHT_INTENSITY.value:
                self._get_light_intensity_with_response()
            elif msgpayload["command_type"] == CommandType.CommandType.SET_LIGHT_INTENSITY.value:
                self._set_light_intensity_with_response(msgpayload)

        if ("registration" in msgpayload):
            self._registration_status.append(msgpayload)


    # method to process the request and create response model for switch staus.
    def _get_switch(self):
        status = self._get_switch_status()
        device_status = {'device_id': self._device_id, 'switch_status': status,
                         'command_response_type': CommandType.CommandType.GET_SWITCH_STATUS.value,
                         'status_code': 200}
        self._create_response_publish(device_status)

    # method to parse the msg payload validate the state that needs to be set
    # construct response for the caller.
    def _set_switch(self, msgpayload):
        device_status = {'device_id': self._device_id,
                         'command_response_type': CommandType.CommandType.SET_SWITCH_STATUS.value}
        if msgpayload["set_switch_value"] == "OFF" or msgpayload["set_switch_value"] == "ON":
            self._set_switch_status(msgpayload["set_switch_value"])
            device_status['status_code'] = self._SUCCESS
            device_status['switch_status'] = self._switch_status
            self._create_response_publish(device_status)
        else:
            device_status['status_code'] = self._BAD_REQUEST
            device_status['error'] = "Switch state" + {msgpayload["set_switch_value"]} + "is not supported."
            self._create_response_publish(device_status)

    # creates response model for Switch status or light intensity based on the request.
    def _create_response_publish(self, device_status):
        response_payload = json.dumps(device_status)
        self.client.publish(f"home/{self._room_type}/{self._device_type}/{self._device_id}/status",
                            str(response_payload))

    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state

    # Get the Light intensity and prepare response for the request.
    def _get_light_intensity_with_response(self):
        switch_status = self._get_switch_status()
        light_intensity = self._get_light_intensity()
        device_status = {'device_id': self._device_id, 'switch_status': switch_status,
                         'light_intensity': light_intensity,
                         'command_response_type': CommandType.CommandType.GET_LIGHT_INTENSITY.value,
                         'status_code': self._SUCCESS}
        self._create_response_publish(device_status)

    # Set the Light intensity and prepare response for the request.
    def _set_light_intensity_with_response(self, msgpayload):
        device_status = {'device_id': self._device_id,
                         'command_response_type': CommandType.CommandType.SET_LIGHT_INTENSITY.value}
        if msgpayload["set_light_intensity"] and msgpayload["set_light_intensity"].upper() in self._INTENSITY:
                self._set_light_intensity(msgpayload["set_light_intensity"].upper())
                device_status['light_intensity'] = self._light_intensity
                device_status['status_code'] = self._SUCCESS
        else:
            device_status['status_code'] = self._BAD_REQUEST
            device_status['error'] = "Light Intensity value is required."

        self._create_response_publish(device_status)

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        self._light_intensity = light_intensity
