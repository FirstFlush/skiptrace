
import nacl.secret
import nacl.utils
import nacl.pwhash
import json
# import os

from getpass import getpass


class FileEncryptor:

    def encrypt_data(self, data:dict, password:str) -> bytes:
        # Serialize data
        serialized_data = json.dumps(data).encode()

        # Derive a key from the password
        salt = nacl.utils.random(nacl.pwhash.argon2i.SALTBYTES)
        key = nacl.pwhash.argon2i.kdf(
            nacl.secret.SecretBox.KEY_SIZE, password.encode(), salt,
            opslimit=nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
            memlimit=nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
        )

        # Encrypt serialized data
        box = nacl.secret.SecretBox(key)
        encrypted = box.encrypt(serialized_data)

        # Return salt and encrypted data for storage
        return salt + encrypted


    def encrypt(self, data:dict):
        password = getpass("Enter a password: ")
        encrypted_data = self.encrypt_data(data, password)
        with open("./client.bin", "w+b") as f:
            f.write(encrypted_data)
        return


    def decrypt_data(self, encrypted_data:bytes, password:str) -> dict:
        # Extract salt and encrypted part
        salt = encrypted_data[:nacl.pwhash.argon2i.SALTBYTES]
        encrypted_part = encrypted_data[nacl.pwhash.argon2i.SALTBYTES:]

        # Derive key from password and salt
        key = nacl.pwhash.argon2i.kdf(
            nacl.secret.SecretBox.KEY_SIZE, password.encode(), salt,
            opslimit=nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
            memlimit=nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
        )

        # Decrypt
        box = nacl.secret.SecretBox(key)
        decrypted_data = box.decrypt(encrypted_part)

        # Deserialize and return
        return json.loads(decrypted_data.decode())


    def decrypt(self):
        with open("./client.bin", "rb") as f:
            stored_encrypted_data = f.read()
        password = getpass("Enter your password to decrypt: ")
        decrypted_data = self.decrypt_data(stored_encrypted_data, password)
        return decrypted_data


if __name__ == '__main__':
    #pass in whatever you want to encrypt as the 'data' param
    #sample data:
    FileEncryptor().encrypt(data={
        "X-API-KEY" : "O9khu_E4PGZL5YfWLsWCbS5oKxPsZC5AjF-7GVhqPLcmvIzNlHG65-sc65hbpDRINPdqEttosrlyqND-6ahPtg",
        "X-ACCESS" : "42863bb8-6ccb-485e-947c-f0f68bac012c"
    })


