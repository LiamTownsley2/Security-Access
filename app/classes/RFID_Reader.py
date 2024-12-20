import logging
from mfrc522 import SimpleMFRC522
import threading
from aws import db
import util.general as general_util
from . import DoorControl, Camera
import RPi.GPIO as GPIO # type: ignore
import os

GPIO.setwarnings(False)
thread_logger_file_name = "thread_reader.log"
thread_logger = logging.getLogger("ThreadLogger")
thread_logger.setLevel(logging.INFO)
thread_file_handler = logging.FileHandler(thread_logger_file_name)
thread_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
thread_logger.addHandler(thread_file_handler)
thread_log_path = os.path.abspath(thread_logger_file_name)

door_controller = DoorControl.DoorController()

class RFID_Reader:
    def __init__(self):
        
        self.status = False
        self.reader = SimpleMFRC522()
        self.logger = thread_logger
        self.camera = Camera.Camera()
        self.thread = threading.Thread(target=self._start_reader, daemon=True)

    def get_status(self):
        return self.status

    def read_key(self):
        self.logger.info("RFID Reader is awaiting Key Presentation")
        id, text = self.reader.read()
        filtered_text = general_util.clean_text(text)
        return id, filtered_text

    def validate_key(user, text):
        if not user:
            return False
        if not text == "secret":
            return False
        return True

    def toggle_reading(self):
        if self.get_status():
            self.stop_reading()
            thread_logger.log(logging.CRITICAL, "RFID READING STATUS STOPPED")
        else:
            self.start_reading()
            thread_logger.log(logging.CRITICAL, "RFID READING STATUS STARTED")
    
    def start(self, stdscr):
        self.start_reading()
        stdscr.refresh()
        return

    def start_reading(self):
        self.thread.start()
        self.status = True
        return True

    def stop_reading(self):
        self.thread.terminate()
        self.thread.join()
        self.status = False
        return True

    def _start_reader(self):
        try:
            while True:
                self.logger.info("start_reader() | Awaiting Key Presentation")
                id, text = self.read_key()
                self.logger.debug(
                    f"start_reader() | Card Read Event -> (Tag ID: {id}) {text}"
                )
                user = db.get_user_by_card(str(id))
                is_valid = self.validate_key(user, text)
                self.logger.info(
                    f"*{'VALID' if is_valid else 'INVALID'} TAG READ* | ID: {id} | Text: '{text}'"
                )

                if is_valid:
                    bucket, file_object = self.camera.record_and_upload(
                        5, user["UserID"]
                    )

                    db.register_entry(str(id), user["UserID"], file_object)
                    entries = db.get_entries_count(user["UserID"])
                    self.logger.info(
                        f"This employee has entered this building {entries} time(s) before."
                    )
                    door_controller.unlock(3)
                else:
                    self.camera.record_and_upload(5)

        except Exception as e:
            self.logger.error(e)
