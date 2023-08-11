import threading
import time


class Lock:
    """
    Very primitive Lock implementation
    just for visualisation
    """

    def __init__(self):
        self._state = 0
        self._lock_holders = {}

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def locked(self) -> bool:
        return self._state != 0

    def acquire(self):
        cur_thread = threading.current_thread()
        if not self.locked():
            self._state += 1
            self._lock_holders[cur_thread] = self._state
            print(
                f"{cur_thread.name} ACQUIRED the Lock! "
                f"Lock state is {self._state}"
            )
            return True
        else:
            self.wait()

    def release(self):
        cur_thread = threading.current_thread()
        self._state -= 1
        print(
            f"{cur_thread.name} RELEASED the Lock! "
            f"Lock state is {self._state}"
        )
        self._lock_holders.pop(cur_thread, None)

    def wait(self):
        while True:
            if self.locked():
                lock_holder = next(
                    iter(self._lock_holders.keys()),
                    None
                )
                print(
                    f"{threading.current_thread().name} is WAITING: "
                    f"Lock is already ACQUIRED by "
                    f"{lock_holder.name if lock_holder else 'Unknown Thread'}"
                )
                time.sleep(0.1)
            else:
                self._state += 1
                print(
                    f"{threading.current_thread().name} ACQUIRED the Lock! "
                    f"Lock state is {self._state}"
                )
                break


LOCK = Lock()


def fn():
    with LOCK:
        time.sleep(3)
        print("************************")
        print(f"Hello from {threading.current_thread().name}!")
        print("************************")


for i in range(1, 3):
    threading.Thread(target=fn, name=f"My_Thread-{i}").start()