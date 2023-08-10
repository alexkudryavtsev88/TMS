# import threading
import time


class Lock:
    """
    Very primitive Lock implementation
    just for visualisation
    """

    def __init__(self):
        self._state = 0

    def acquire(self):
        if not self.is_locked():
            self._state += 1
        else:
            self.wait()

    def release(self):
        self._state -= 1

    def is_locked(self) -> bool:
        return self._state != 0

    def wait(self):
        while True:
            if self.is_locked():
                time.sleep(0.1)
            else:
                self._state = 1
                return
