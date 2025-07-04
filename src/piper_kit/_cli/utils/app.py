import curses
import time
from typing import Self

from .thread import Thread


class App(Thread):
    KEY_ESC = 27

    def __enter__(self) -> Self:
        self.stdscr = curses.initscr()
        self.stdscr.nodelay(True)  # noqa: FBT003
        curses.curs_set(0)
        curses.noecho()

        self.on_init()
        self.stdscr.refresh()

        super().__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        super().__exit__(*args)
        curses.endwin()

    def worker(self) -> None:
        while not self.is_exited():
            key = self.stdscr.getch()
            self.on_refresh(key)
            self.stdscr.refresh()
            time.sleep(1 / 30)

    def on_init(self) -> None:
        pass

    def on_refresh(self, key: int) -> None:
        pass


__all__ = ["App"]
