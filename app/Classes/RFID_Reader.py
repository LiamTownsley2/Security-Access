import sys
from mfrc522 import SimpleMFRC522
import multiprocessing
from AWS import db
import Util.general
from Classes.GPIO_Pin import GPIO_Pin

sys.path.append("..")


class RFID_Reader:
    def __init__(self, logger, camera):
        self.status = False
        self.reader = SimpleMFRC522()
        self.logger = logger
        self.camera = camera
        self.thread = multiprocessing.Process(target=self.start_reader, daemon=True)

    def get_status(self):
        return self.status

    def read_key(self):
        self.logger.info("RFID Reader is awaiting Key Presentation")
        id, text = self.reader.read()
        filtered_text = Util.general.clean_text(text)
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
        else:
            self.start_reading()

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
                    green_led = GPIO_Pin(
                        12
                    )  # The Green LED represents unlocking the door.
                    green_led.enable(3)
                else:
                    self.camera.record_and_upload(5)

        except Exception as e:
            self.logger.error(e)
