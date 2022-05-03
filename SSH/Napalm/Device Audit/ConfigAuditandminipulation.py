import json
from napalm import get_network_driver

# This script will audit the devices' configuration already on the device via SSH using NAPALM
# If the config is not on the device it will apply the CFG file.
# 03/05/2022 by Kris Morrison

# PARAMETERS
IP = ["192.168.2.1", "192.168.2.2"]
USERNAME = "kris"
PASSWORD = "cisco123"

for IP in IP:
    driver = get_network_driver("ios")
    iosv2 = driver(IP, USERNAME, PASSWORD, optional_args={'global_delay_factor': 2})
    iosv2.open()

    print("----------------------------------------------------")
    print(f"Accessing device {IP}")
    iosv2.load_merge_candidate(filename='ACL1.cfg')
    differences = iosv2.compare_config()
    if len(differences) > 0:
        print("These are the changes made")
        print(differences)
        iosv2.commit_config()
    else:
        print("No changes to the config")
        iosv2.discard_config()
    iosv2.close()
