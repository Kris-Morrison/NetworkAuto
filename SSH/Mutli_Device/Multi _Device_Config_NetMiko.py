from netmiko import ConnectHandler
import getpass

# Retrieving the device information
username = input("What is the username? \n")
password = getpass.getpass()

# Device parameters
all_devices = {"cisco_switch1": {
    "device_type": "cisco_ios",
    "host": "192.168.10.1",
    "username": username,
    "password": password
},
    "cisco_switch2": {
        "device_type": "cisco_ios",
        "host": "192.168.10.2",
        "username": username,
        "password": password
    },
    "cisco_switch3": {
        "device_type": "cisco_ios",
        "host": "192.168.10.3",
        "username": username,
        "password": password
    }
}
for device in all_devices:

    # Making the connection to the device
    ssh = ConnectHandler(**all_devices[device])
    print(f"This is configuration been carried out for {device}")
    # What commands to run
    with open("Configuration_baseline.txt") as line:
        lines = line.read().splitlines()
    result = ssh.send_config_set(lines)
    print(result)
