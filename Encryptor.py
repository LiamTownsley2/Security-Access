from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open("private.pem", "rb") as key:
    private_key = serialization.load_pem_private_key(
        key.read(),
        password=None,
    )
    public_key = private_key.public_key()

def encrypt_message(message:str):
    return public_key.encrypt(
        str.encode(message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_message(message:str):
    return private_key.decrypt(
        str.encode(message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )