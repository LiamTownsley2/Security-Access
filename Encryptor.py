import os
import base64

def generate_master_password():
    random = os.urandom(24)
    b64_string = base64.b64encode(random).decode("utf-8")
    return b64_string[:32]