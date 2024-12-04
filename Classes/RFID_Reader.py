import sys
sys.path.append("..")

from mfrc522 import SimpleMFRC522
import Util

class RFID_Reader:
    def __init__(self, logger):
        self.reader = SimpleMFRC522()
        self.logger = logger
        
    def read_key(self):
        self.logger.info("RFID Reader is awaiting Key Presentation")
        id, text = self.reader.read()
        filtered_text = Util.clean_text(text)        
        return id, filtered_text