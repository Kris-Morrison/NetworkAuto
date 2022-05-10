from netmiko import ConnectHandler, NetMikoTimeoutException, NetmikoAuthenticationException
import csv
from paramiko.ssh_exception import SSHException
import os
from Encryption import Encrpytor

# This script is using netmiko with SSH to connect to device and enter commands
# This will retrieve the commands from a file in the same dir that can be encrypted or decrypted with base64
# called - command_file and IP - device_list
# Written by Kris Morrison

key = Encrpytor()
option = ""
device_list = []
while option != "end":
    option = input("Do you require to encrypt the files? Would you like to run the scripts? or end? (yes, script, "
                   "end)\n")
    option.lower()

    if option == "yes":
        # encrypt my file
        key.encyrpt()

    elif option == "script":
        # decrypt the file for use.
        new_file = key.decyrpt()
        with open(new_file, newline="", encoding='utf-8-sig') as f:
            device_information = csv.reader(f)
            for info in device_information:
                device_list.append(info)
        os.remove(new_file)
        # Retrieving the device commands`
        with open("command_file.txt") as f:
            commands = f.read().splitlines()

        # Device parameters
        for host in device_list:
            IP = host[0]
            cisco_switch = {"device_type": "cisco_ios", "host": host[0], "username": host[1], "password": host[2]}
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

            # # Check software versions
            # for software_ver in list_versions:
            #     print ('Checking for ' + software_ver)
            #     output_version = net_connect.send_command('show version')
            #     int_version = 0 # Reset integer value
            #     int_version = output_version.find(software_ver) # Check software version
            #     if int_version > 0:
            #         print ('Software version found: ' + software_ver)
            #         break
            #     else:
            #         print ('Did not find ' + software_ver)
