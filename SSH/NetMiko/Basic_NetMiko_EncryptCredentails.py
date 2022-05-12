from pprint import pprint
from netmiko import ConnectHandler, NetMikoTimeoutException, NetmikoAuthenticationException
import csv
from paramiko.ssh_exception import SSHException
import os
from Encryption import Encrpytor
import threading


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.HEADER + """# This script is using netmiko with SSH to connect to devices and enter SHOW commands from txt file.
# This will retrieve the ip and creds from a csv file in the same dir that can be encrypted or decrypted with base64.
# To remove the blowfish warning, please comment out the transport.py in paramiko for blowfish-cbc.
# Written by Kris Morrison.
""")

key = Encrpytor()
option = ""
device_list = []
progress = "no"
config_threads_list = []
device_output = {}
command_output = {}
output = []
device = 0


# =======================================================================================================
def config_worker( ip, user, password):
    cisco_switch = {"device_type": "cisco_ios", "host": ip, "username": user, "password": password}
    # Error handling
    try:
        connect = ConnectHandler(**cisco_switch)
        print(bcolors.FAIL + f"connecting to device {ip}")
    except NetmikoAuthenticationException:
        print(bcolors.FAIL + f'Authentication failure: ' + ip)
    except NetMikoTimeoutException:
        print(bcolors.FAIL + f'Timeout to device: ' + ip)
    except EOFError:
        print(bcolors.FAIL + f'End of file while attempting device ' + ip)
    except SSHException:
        print(bcolors.FAIL + f'SSH Issue. Are you sure SSH is enabled? ' + ip)
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
    # Sends the commands to the device

    for line in commands:
        command_output[str(ip) + str(line)] = connect.send_command(line)



# ===========================================================================================================================================
while option != "end":
    print(bcolors.OKBLUE + "This script will provide base64 encryption on the files. \n")
    option = input(
        "Do you require to encrypt the files?\nWould you like to run the main script?\nor end?\n(options: yes, "
        "script, end)\n").lower()
    # =====================================================================================================================================
    # Encrypting the file
    if option == "yes":
        my_key = key.key_creation()
        key.encyrpt(key_file=my_key)

    # =======================================================================================================================================
    # Will decrypt the file and abstract the information into a list. After will delete the decrypted file after retreival.

    elif option == "script":
        # decrypt the file for use.
        new_file = key.decyrpt("mykey.key")
        with open(new_file, newline="", encoding='utf-8-sig') as f:
            device_information = csv.reader(f)
            for info in device_information:
                device_list.append(info)
        os.remove(new_file)

        print("This is the device information in the file. ")
        print("------------------------------------------------------------------------")
        pprint(device_list)
        print("------------------------------------------------------------------------")
        progress = input("Would you like to continue? 'yes' or 'no'\n").lower()

        if progress == "yes":
            # Retrieving the device commands`
            command_file = input("What is the name of the command file (.txt) ? \n")
            with open(command_file) as f:
                commands = f.read().splitlines()

            # Device parameters
            for host in device_list:
                IP = host[0]
                USER = host[1]
                PASS = host[2]
                device += 1

                print('Creating thread for: ', IP)
                config_threads_list.append(threading.Thread(target=config_worker, args=(IP, USER, PASS)))

            for config_thread in config_threads_list:
                config_thread.start()

            for config_thread in config_threads_list:
                config_thread.join()

            for host in device_list:
                ip = host[0]
                print(f"================================DEVICE / {ip}===================================")
                for line in commands:
                    print(f"Information for the commands '{line}' :-")
                    print(command_output[str(ip) + str(line)])
                    print("------------------------------------------------------------------------")
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
