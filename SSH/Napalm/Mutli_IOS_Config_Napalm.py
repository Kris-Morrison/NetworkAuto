from napalm import get_network_driver
import json


# This script will carry out data retrieval from multiple devices on the network via SSH using napalm.
# 03/05/2022 written by Kris Morrison
# Parameters
IP_ADDRESSES = ["192.168.2.1", "192.168.2.2"]
USERNAME = "kris"
PASSWORD = "cisco123"

for IP in IP_ADDRESSES:
    print("----------------------------------------------------")
    print(f"You are connecting to : {IP}")
    # connection to device
    driver = get_network_driver("ios")
    ios = driver(IP, USERNAME, PASSWORD)
    ios.open()

    # what information to retrieve from the device
    data = ios.get_facts()
    print(json.dumps(data, indent=4))
    print("----------------------------------------------------")
    # get BGP information
    data2 = ios.get_bgp_neighbors()
    print("----------------------------------------------------")
    print(json.dumps(data2, indent=4))
    ios.close()
