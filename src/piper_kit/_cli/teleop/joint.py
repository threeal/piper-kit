import argparse
import curses
from typing import Self

from piper_kit import PiperInterface
from piper_kit._cli.utils import App
from piper_kit.messages import (
    GripperFeedbackMessage,
    JointFeedback12Message,
    JointFeedback34Message,
    JointFeedback56Message,
)


class TeleopJointApp(App):
    def __init__(self) -> None:
        super().__init__()

        self.current_pos = [0, 0, 0, 0, 0, 0, 0]
        self.target_pos = [0, 0, 0, 0, 0, 0, 45000]

    def on_init(self) -> Self:
        title = "PiPER Joint Teleoperation"
        self.stdscr.addstr(0, (55 - len(title)) // 2, title, curses.A_BOLD)

        self.stdscr.addstr(3, 2, "Joint Information:", curses.A_BOLD)

        headers = f"{'Joint':<15} {'Target':<12} {'Current':<12} {'Diff':<10}"
        self.stdscr.addstr(4, 2, headers, curses.A_UNDERLINE)

        self.stdscr.addstr(5, 2, "Base (J1):")
        self.stdscr.addstr(6, 2, "Shoulder (J2):")
        self.stdscr.addstr(7, 2, "Elbow (J3):")
        self.stdscr.addstr(8, 2, "Wrist1 (J4):")
        self.stdscr.addstr(9, 2, "Wrist2 (J5):")
        self.stdscr.addstr(10, 2, "Wrist3 (J6):")
        self.stdscr.addstr(11, 2, "Gripper:")

        self.stdscr.addstr(13, 2, "Keyboard Controls:", curses.A_BOLD)
        self.stdscr.addstr(14, 4, "Base (J1):     A/D - Rotate left/right")
        self.stdscr.addstr(15, 4, "Shoulder (J2): W/S - Move up/down")
        self.stdscr.addstr(16, 4, "Elbow (J3):    I/K - Move up/down")
        self.stdscr.addstr(17, 4, "Wrist1 (J4):   J/L - Rotate left/right")
        self.stdscr.addstr(18, 4, "Wrist2 (J5):   Q/E - Rotate left/right")
        self.stdscr.addstr(19, 4, "Wrist3 (J6):   U/O - Rotate left/right")
        self.stdscr.addstr(20, 4, "Gripper:       F/H - Open/close")
        self.stdscr.addstr(22, 4, "ESC - Exit teleoperation", curses.A_BOLD)

        return self

    def on_refresh(self, key: int) -> None:  # noqa: C901, PLR0912
        if key == self.KEY_ESC:
            self.exit()
        elif key == ord("w"):
            self.target_pos[1] += 5000
        elif key == ord("s"):
            self.target_pos[1] -= 5000
        elif key == ord("a"):
            self.target_pos[0] += 5000
        elif key == ord("d"):
            self.target_pos[0] -= 5000
        elif key == ord("q"):
            self.target_pos[4] += 5000
        elif key == ord("e"):
            self.target_pos[4] -= 5000
        elif key == ord("i"):
            self.target_pos[2] -= 5000
        elif key == ord("k"):
            self.target_pos[2] += 5000
        elif key == ord("j"):
            self.target_pos[3] -= 5000
        elif key == ord("l"):
            self.target_pos[3] += 5000
        elif key == ord("u"):
            self.target_pos[5] -= 5000
        elif key == ord("o"):
            self.target_pos[5] += 5000
        elif key == ord("f"):
            self.target_pos[6] += 5000
        elif key == ord("h"):
            self.target_pos[6] -= 5000

        for i in range(7):
            diff = self.target_pos[i] - self.current_pos[i]
            info = f"{self.target_pos[i]:<12} {self.current_pos[i]:<12} {diff:<10}"
            self.stdscr.addstr(5 + i, 18, info)

        self.stdscr.addstr(11, 18, info)


def command_teleop_joint(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper, TeleopJointApp() as app:
        while not app.is_exited():
            match piper.read_message():
                case JointFeedback12Message() as msg:
                    app.current_pos[0] = msg.joint_1
                    app.current_pos[1] = msg.joint_2

                    piper.set_motion_control_b("joint", 20)
                    piper.set_joint_control_12(*app.target_pos[0:2])

                case JointFeedback34Message() as msg:
                    app.current_pos[2] = msg.joint_3
                    app.current_pos[3] = msg.joint_4

                    piper.set_joint_control_34(*app.target_pos[2:4])

                case JointFeedback56Message() as msg:
                    app.current_pos[4] = msg.joint_5
                    app.current_pos[5] = msg.joint_6

                    piper.set_joint_control_56(*app.target_pos[4:6])

                case GripperFeedbackMessage() as msg:
                    app.current_pos[6] = msg.position
                    piper.set_gripper_control(app.target_pos[6], 1000)


__all__ = ["command_teleop_joint"]
