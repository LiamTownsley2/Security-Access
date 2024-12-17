from time import sleep
from os import path
from enum import Enum

sysfs_path = "/sys/kernel/led_toggle/led_toggle"

class DoorState(Enum):
    LOCKED = 0, # Light Off [LOW]
    UNLOCKED = 1 # Light On [HIGH]

class DoorControl:
    def __init__(self):
        if not path.exists(sysfs_path):
            raise FileNotFoundError(f"Sysfs File Not Found. Expected Location: {sysfs_path}")

    def get_state(self):
        with open(sysfs_path, "r") as file:
            state = file.read().strip()
        return int(state)

    def lock(self):
        self._write_state(DoorState.LOCKED)

    def unlock(self, seconds: int):
        self._write_state(DoorState.UNLOCKED)
        if seconds:
            sleep(seconds)
            self.lock()

    def toggle_lock(self):
        if self.get_state() == DoorState.LOCKED:
            self.unlock()
        else:
            self.lock()

    def _write_state(self, state:int):
        with open(sysfs_path, "w") as file:
            file.write(str(state))