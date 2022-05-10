from netmiko import ConnectHandler, NetMikoTimeoutException, NetmikoAuthenticationException
import getpass

# This script is using netmiko with SSH to connect to device and enter commands
# This will retrieve the commands from a file in the same dir, called - command_file and IP - device_list
# Written by Kris Morrison

# Retrieving the device information
# IP = input("What is the IP address of the device? \n")
from paramiko.ssh_exception import SSHException

username = input("What is the username? \n")
password = getpass.getpass()

# Retrieving the device commands
with open("Encrypted Scripts/command_file.txt") as f:
    commands = f.read().splitlines()

print(commands)

# Retrieving the device IP addresses
with open("Encrypted Scripts/device_list.txt") as f:
    ip_lists = f.read().splitlines()

# Device parameters
for IP in ip_lists:
    cisco_switch = {
        "device_type": "cisco_ios",
        "username": username,
        "host": IP,
        "password": password
    }
    # Making the connection to the device and carry out any error messages.
    print("------------------------------------------------------")
    try:
        ssh = ConnectHandler(**cisco_switch)
        print(f"connecting to device {IP}")
    except NetmikoAuthenticationException:
        print('Authentication failure: ' + IP)
        continue
    except NetMikoTimeoutException:
        print('Timeout to device: ' + IP)
        continue
    except EOFError:
        print('End of file while attempting device ' + IP)
        continue
    except SSHException:
        print('SSH Issue. Are you sure SSH is enabled? ' + IP)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue

    # What commands to run
    for line in commands:
        command = ssh.send_command(line)
        print(command)

