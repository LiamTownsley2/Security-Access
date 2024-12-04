import sys
sys.path.append("..")

from mfrc522 import SimpleMFRC522
import Util

class RFID_Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
        
    def read_key(self):
        print("Awaiting Key Presentation...")
        id, text = self.reader.read()
        filtered_text = Util.clean_text(text)        
        return id, filtered_text