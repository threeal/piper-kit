import threading
from typing import Self


class Thread:
    def __init__(self) -> None:
        self._thread = None
        self._is_exited = False

    def __enter__(self) -> Self:
        self._thread = threading.Thread(target=self.worker)
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.exit()

    def exit(self) -> None:
        self._is_exited = True
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def is_exited(self) -> bool:
        return self._is_exited

    def worker(self) -> None:
        pass


__all__ = ["Thread"]
