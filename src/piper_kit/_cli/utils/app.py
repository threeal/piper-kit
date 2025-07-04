import curses
import threading
import time
from typing import Self


class App:
    KEY_ESC = 27

    def __init__(self) -> None:
        self.exit = False

    def __enter__(self) -> Self:
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)  # noqa: FBT003

        curses.curs_set(0)
        curses.noecho()

        self.on_init()
        self.stdscr.refresh()

        self._thread = threading.Thread(target=self.thread_worker)
        self._thread.start()

        return self

    def __exit__(self, *args: object) -> None:
        self.exit = True
        self._thread.join()
        curses.endwin()

    def thread_worker(self) -> None:
        while not self.exit:
            key = self.stdscr.getch()
            self.on_refresh(key)
            self.stdscr.refresh()
            time.sleep(1 / 30)

    def on_init(self) -> None:
        pass

    def on_refresh(self, key: int) -> None:
        pass


__all__ = ["App"]
