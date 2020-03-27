import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes

# return bytes message encoded to string
def bytes_to_string(text_to_encode):
    return b64encode(text_to_encode).decode("utf-8")


# return string message encoded to bytes
def string_to_bytes(text_to_encode):
    return b64decode(text_to_encode)


def encrypt_data(text_to_encrypt, cipher):
    byte_message = text_to_encrypt.encode()
    return cipher.encrypt(byte_message)


def decrypt_data(text_to_decrypt, cipher):
    byte_message = cipher.decrypt(text_to_decrypt)
    return byte_message.decode()


def encrypt_service(service, secret):
    cipher = Salsa20.new(key=secret)
    encrypted_service = []
    for item in service:
        encrypted_service.append(encrypt_data(item, cipher))
    return {
        "service": bytes_to_string(encrypted_service[0]),
        "email": bytes_to_string(encrypted_service[1]),
        "password": bytes_to_string(encrypted_service[2]),
        "key": bytes_to_string(secret),
        "nonce_key": bytes_to_string(cipher.nonce),
    }


def decrypt_service(encrypted_service):
    service_to_decrypt = []
    for item in encrypted_service:
        service_to_decrypt.append(string_to_bytes(encrypted_service[item]))
    cipher = Salsa20.new(key=service_to_decrypt[3], nonce=service_to_decrypt[4])
    return {
        "service": decrypt_data(service_to_decrypt[0], cipher),
        "email": decrypt_data(service_to_decrypt[1], cipher),
        "password": decrypt_data(service_to_decrypt[2], cipher),
    }


# ===============================================================================
# ++++++++++++++++++++++++++++++++  BEGINNING  ++++++++++++++++++++++++++++++++++
# ===============================================================================

service = ["gmail", "name@gmail.com", "senha123"]
secret = get_random_bytes(32)
data_to_store = []
data_to_open = []
services_revealed = []

print("========= ENCRYPTATION ==========")

data_to_store.append(encrypt_service(service, secret))

with open("data.json", "w") as json_file:
    json.dump(data_to_store, json_file, indent=4)

print("========= OPENING JSON FILE ==========")

with open("data.json") as json_file:
    data_to_open = json.load(json_file)

for p in data_to_open:
    print("service: " + p["service"])
    print("email: " + p["email"])
    print("senha: " + p["password"])
    print("key: " + p["key"])
    print("nonce: " + p["nonce_key"])

print("========= DECRYPTATION ==========")

services_revealed.append(decrypt_service(data_to_open[0]))

print("Services Revealed:")

for item in services_revealed[0]:
    # print(item)
    print(f"{item}: {services_revealed[0][item]}")
