from mfrc522 import SimpleMFRC522
import Util
from ..Encryptor import decrypt_message, encrypt_message
class RFID_Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
        
    def read_key(self):
        print("Awaiting Key Presentation...")
        id, text = self.reader.read()
        filtered_text = Util.clean_text(text)        
        return id, filtered_text
    
    def write_key(self, entries:int):
        print("Awaiting Key Presentation...")
        encrypted_entries = encrypt_message(entries)
        self.reader.write(encrypted_entries)