from netmiko import ConnectHandler
import getpass

# Retrieving the device information
IP = input("What is the IP address of the device? \n")
username = input("What is the username? \n")
password = getpass.getpass()

# Device paramters
cisco_switch = {
    "device_type": "cisco_ios",
    "host": IP,
    "username": username,
    "password": password
}
# Making the connection to the device
ssh = ConnectHandler(**cisco_switch)


# What commands to run
command = ssh.send_command("show ip interface brief")
print(command)
