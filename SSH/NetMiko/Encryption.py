from cryptography.fernet import Fernet
import os

#Written by Kris Morrison

class Encrpytor():

    def key_creation():
        key = Fernet.generate_key()

        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)

    def encyrpt(self):
        file = input("What is the name of your file :\n")
        key_file = input("What is the name of the key file :\n")
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

    def decyrpt(self):
        file = input("What is the encrypted name of your file :\n")
        new_file = input("What is the name of your new decrypted file :\n")
        key_file = input("What is the name of the key file :\n")
        with open(key_file, 'rb') as mykey:
            key = mykey.read()

        f = Fernet(key)

        with open(file, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        decrypted = f.decrypt(encrypted)

        with open(new_file, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)
        return new_file
