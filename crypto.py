# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
import os
import base64
import rsa
from dotenv import load_dotenv

load_dotenv()


public_key = os.getenv("PUBLIC_KEY").replace('/\\n/g', '\n')
private_key = os.getenv("PRIVATE_KEY").replace('/\\n/g', '\n')

public_key = rsa.PublicKey.load_pkcs1(public_key)
private_key = rsa.PrivateKey.load_pkcs1(private_key)


def encrypt(msg):
    ciphertext = rsa.encrypt(msg.encode(), public_key)
    encoded = base64.b64encode(ciphertext)
    return encoded.decode()


def decrypt(msg):
    msg = base64.b64decode(msg)
    return rsa.decrypt(msg, private_key).decode('utf-8')


# print(encrypt('hello msg'))
# print(decrypt(encrypt('hello msg')))
