from cryptography.fernet import Fernet
import os


# Written by Kris Morrison

class Encrpytor():

    def key_creation(self):
        key = Fernet.generate_key()
        key_file = "mykey.key"
        with open(key_file, 'wb') as mykey:
            mykey.write(key)
        return key_file

    def encyrpt(self,key_file):
        file = input("What is the name of your file (.csv):\n")

        # load the key and decrypt my file
        with open(key_file, 'rb') as mykey:
            key = mykey.read()

        print(key)

        f = Fernet(key)

        with open(file, 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        with open('enc_' + file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        os.remove(file)

    def decyrpt(self,key_file):
        file = input("What is the encrypted name of your file (.csv) :\n")
        new_file = "file.csv"
        with open(key_file, 'rb') as mykey:
            key = mykey.read()

        f = Fernet(key)

        with open(file, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        decrypted = f.decrypt(encrypted)

        with open(new_file, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
        return new_file
