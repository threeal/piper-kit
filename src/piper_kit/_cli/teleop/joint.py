import argparse
import curses
import threading
import time
from typing import Self

from piper_kit import PiperInterface


class Screen:
    KEY_ESC = 27

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

        self.exit = False
        self.feedbacks = [0, 0, 0, 0, 0, 0]
        self.positions = [0, 0, 0, 0, 0, 0]
        self.gripper_position = 0

    def __enter__(self) -> Self:
        self._stdscr = curses.initscr()
        self._stdscr.nodelay(True)  # noqa: FBT003

        curses.curs_set(0)
        curses.noecho()

        title = "PiPER Joint Teleoperation"
        self._stdscr.addstr(0, (55 - len(title)) // 2, title, curses.A_BOLD)

        self._stdscr.addstr(3, 2, "Joint Information:", curses.A_BOLD)

        headers = f"{'Joint':<15} {'Target':<12} {'Current':<12} {'Diff':<10}"
        self._stdscr.addstr(4, 2, headers, curses.A_UNDERLINE)

        self._stdscr.addstr(5, 2, "Base (J1):")
        self._stdscr.addstr(6, 2, "Shoulder (J2):")
        self._stdscr.addstr(7, 2, "Elbow (J3):")
        self._stdscr.addstr(8, 2, "Wrist1 (J4):")
        self._stdscr.addstr(9, 2, "Wrist2 (J5):")
        self._stdscr.addstr(10, 2, "Wrist3 (J6):")
        self._stdscr.addstr(11, 2, "Gripper:")

        self._stdscr.addstr(13, 2, "Keyboard Controls:", curses.A_BOLD)
        self._stdscr.addstr(14, 4, "Base (J1):     A/D - Rotate left/right")
        self._stdscr.addstr(15, 4, "Shoulder (J2): W/S - Move up/down")
        self._stdscr.addstr(16, 4, "Elbow (J3):    I/K - Move up/down")
        self._stdscr.addstr(17, 4, "Wrist1 (J4):   J/L - Rotate left/right")
        self._stdscr.addstr(18, 4, "Wrist2 (J5):   Q/E - Rotate left/right")
        self._stdscr.addstr(19, 4, "Wrist3 (J6):   U/O - Rotate left/right")
        self._stdscr.addstr(20, 4, "Gripper:       F/H - Open/close")
        self._stdscr.addstr(22, 4, "ESC - Exit teleoperation", curses.A_BOLD)

        self._stdscr.refresh()

        self._thread = threading.Thread(target=self.thread_worker)
        self._thread.start()

        return self

    def __exit__(self, *args: object) -> None:
        self.exit = True
        self._thread.join()
        curses.endwin()

    def thread_worker(self) -> None:  # noqa: C901, PLR0912
        while not self.exit:
            key = self._stdscr.getch()
            if key == self.KEY_ESC:
                self.exit = True
            elif key == ord("w"):
                self.positions[1] += 5000
            elif key == ord("s"):
                self.positions[1] -= 5000
            elif key == ord("a"):
                self.positions[0] += 5000
            elif key == ord("d"):
                self.positions[0] -= 5000
            elif key == ord("q"):
                self.positions[4] += 5000
            elif key == ord("e"):
                self.positions[4] -= 5000
            elif key == ord("i"):
                self.positions[2] -= 5000
            elif key == ord("k"):
                self.positions[2] += 5000
            elif key == ord("j"):
                self.positions[3] -= 5000
            elif key == ord("l"):
                self.positions[3] += 5000
            elif key == ord("u"):
                self.positions[5] -= 5000
            elif key == ord("o"):
                self.positions[5] += 5000
            elif key == ord("f"):
                self.gripper_position += 5000
            elif key == ord("h"):
                self.gripper_position -= 5000

            for i in range(6):
                diff = self.positions[i] - self.feedbacks[i]
                info = f"{self.positions[i]:<12} {self.feedbacks[i]:<12} {diff:<10}"
                self._stdscr.addstr(5 + i, 18, info)

            self._stdscr.addstr(11, 18, f"{self.gripper_position:<12}")
            self._stdscr.refresh()

            time.sleep(1 / 30)


def command_teleop_joint(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper, Screen() as screen:
        while not screen.exit:
            screen.feedbacks = piper.read_all_joint_feedbacks()

            piper.set_motion_control_b("joint", 20)
            piper.set_joint_control(*screen.positions)
            piper.set_gripper_control(screen.gripper_position)


__all__ = ["command_teleop_joint"]
