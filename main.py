import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device
import asyncio

WAIT_TIME = .25

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)

# Creating the light_device
print("Intitate the device creation and registration process." )
print("\nCreating the Light devices for their respective rooms.")

light_device_1 = Light_Device("light_1", "Kitchen")
time.sleep(WAIT_TIME)
print(light_device_1._registration_status)

light_device_2 = Light_Device("light_2", "Kitchen")
time.sleep(WAIT_TIME)
print(light_device_2._registration_status)

light_device_3 = Light_Device("light_3", "BR1")
time.sleep(WAIT_TIME)
print(light_device_3._registration_status)

light_device_4 = Light_Device("light_4", "BR2")
time.sleep(WAIT_TIME)
print(light_device_4._registration_status)

light_device_5 = Light_Device("light_5", "BR1")
time.sleep(WAIT_TIME)
print(light_device_5._registration_status)

light_device_6 = Light_Device("light_6", "BR2")
time.sleep(WAIT_TIME)
print(light_device_6._registration_status)

light_device_7 = Light_Device("light_6", "BR2")
time.sleep(WAIT_TIME)
print(light_device_7._registration_status)

# Creating the ac_device
print("\nCreating the AC devices for their respective rooms. ")
ac_device_1 = AC_Device("ac_1", "BR1")
time.sleep(WAIT_TIME)
print(ac_device_1._registration_status)

ac_device_2 = AC_Device("ac_2", "BR2")
time.sleep(WAIT_TIME)
print(ac_device_2._registration_status)

ac_device_2 = AC_Device("ac_2", "BR2")
time.sleep(WAIT_TIME)
print(ac_device_2._registration_status)

print("----------------------------------------------------------------------------------------------------------")

print("Getting Device status by Device Type")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.get_status_device_type("AC"))

print(edge_server_1.get_status_device_type("LIGHT"))

print(edge_server_1.get_status_device_type("all"))

print("----------------------------------------------------------------------------------------------------------")

print("Getting Device status by Room")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.get_status_room("Kitchen"))
print(edge_server_1.get_status_room("all"))

print("----------------------------------------------------------------------------------------------------------")


print("Getting Device status by Device ID")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.get_status_deviceid("light_2"))
print(edge_server_1.get_status_deviceid("ac_2"))
print(edge_server_1.get_status_deviceid("all"))

print("----------------------------------------------------------------------------------------------------------")

print("Getting light intensity by Device ID")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.get_light_intensity_device_id("light_4"))
print(edge_server_1.get_light_intensity_device_id("light_2"))


print("----------------------------------------------------------------------------------------------------------")

print("Getting temperature by Device ID")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.get_temperature_device_id("ac_2"))
print(edge_server_1.get_temperature_device_id("ac_1"))

print("----------------------------------------------------------------------------------------------------------")

print("Getting Switch status by Device ID")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_switch_status_by_deviceid("ac_2", "ON"))


print("----------------------------------------------------------------------------------------------------------")

print("Getting Switch status by Room")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_switch_status_by_room("all", "ON"))

print("----------------------------------------------------------------------------------------------------------")

print("Set  Switch status by Device Type")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_switch_status_by_device_type("LIGHT", "OFF"))
print(edge_server_1.get_status_device_type("LIGHT"))
print(edge_server_1.get_status_device_type("AC"))

print("----------------------------------------------------------------------------------------------------------")
print("Set Light intensity status by Device ID only for Light devices")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_light_intensity_by_deviceid("light_6", "high"))
print(edge_server_1.set_light_intensity_by_deviceid("ac_1", "high"))
print(edge_server_1.set_light_intensity_by_deviceid("light_2", "medium"))
print(edge_server_1.set_light_intensity_by_deviceid("all", "low"))

print("----------------------------------------------------------------------------------------------------------")
print("Set Light intensity status by Device room only for Light devices")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_light_intensity_by_room("Kitchen", "high"))
print(edge_server_1.set_light_intensity_by_room("all", "medium"))


print("----------------------------------------------------------------------------------------------------------")
print("Set temperature by Device id or room only for AC devices")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_temperature_by_deviceid("ac_1", 34))
print(edge_server_1.set_temperature_by_room("BR2", 28))
print(edge_server_1.set_temperature_by_deviceid("all", 24))

print("----------------------------------------------------------------------------------------------------------")
print("Set temperature by Device room or all devices  only for Light devices")
print("----------------------------------------------------------------------------------------------------------")
print(edge_server_1.set_temperature_by_deviceid("all", 32))
print(edge_server_1.set_temperature_by_room("all", 28))
print(edge_server_1.set_temperature_by_deviceid("light_1", 28))


print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()





