import re
import random
import time
from queue import Queue

log_queue = Queue()

def generate_unique_id():
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000, 9999)
    return f"{timestamp}{random_number}"

def repeat(word, n):
    return (f"{word} " * n)[:-1]

def clean_text(text):
    filtered_text = re.sub(r"\W+", "", text)
    return filtered_text

def watch_log_file(file_path, log_queue):
    with open(file_path, "r") as log_file:
        log_file.seek(0, 2)
        while True:
            line = log_file.readline()
            if line:
                log_queue.put(line)
            else:
                time.sleep(0.1)
