import threading

class AtomicBoolean:
    def __init__(self, initial_value=False):
        self.lock = threading.Lock()
        self.value = initial_value

    def get(self):
        with self.lock:
            return self.value

    def set(self, new_value):
        with self.lock:
            self.value = new_value