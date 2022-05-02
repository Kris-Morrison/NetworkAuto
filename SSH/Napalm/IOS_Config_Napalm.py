from napalm import get_network_driver
import json

# Parameters
IP = "192.168.1.1"
USERNAME = "kris"
PASSWORD = "cisco123"

# connection to device
driver = get_network_driver("ios")
ios = driver(IP, USERNAME, PASSWORD)
ios.open()

# what information to retrieve from the device
data = ios.get_facts()
print(json.dumps(data, indent=4))

