import argparse
import curses
from typing import Self

from piper_kit import PiperInterface
from piper_kit._cli.utils import App, Thread
from piper_kit.messages import (
    GripperFeedbackMessage,
    JointFeedback12Message,
    JointFeedback34Message,
    JointFeedback56Message,
)


class TeleopFollowApp(App):
    def __init__(self) -> None:
        super().__init__()

        self.leader_pos = [0, 0, 0, 0, 0, 0, 0]
        self.follower_pos = [0, 0, 0, 0, 0, 0, 0]

    def on_init(self) -> Self:
        title = "PiPER Leader-Follower Teleoperation"
        self.stdscr.addstr(0, (55 - len(title)) // 2, title, curses.A_BOLD)

        self.stdscr.addstr(3, 2, "Joint Information:", curses.A_BOLD)

        headers = f"{'Joint':<15} {'Leader':<12} {'Follower':<12} {'Diff':<10}"
        self.stdscr.addstr(4, 2, headers, curses.A_UNDERLINE)

        self.stdscr.addstr(5, 2, "Base (J1):")
        self.stdscr.addstr(6, 2, "Shoulder (J2):")
        self.stdscr.addstr(7, 2, "Elbow (J3):")
        self.stdscr.addstr(8, 2, "Wrist1 (J4):")
        self.stdscr.addstr(9, 2, "Wrist2 (J5):")
        self.stdscr.addstr(10, 2, "Wrist3 (J6):")
        self.stdscr.addstr(11, 2, "Gripper:")

        self.stdscr.addstr(13, 2, "Keyboard Controls:", curses.A_BOLD)
        self.stdscr.addstr(14, 4, "ESC - Exit teleoperation", curses.A_BOLD)

        return self

    def on_refresh(self, key: int) -> None:
        if key == self.KEY_ESC:
            self.exit()

        for i in range(6):
            diff = self.leader_pos[i] - self.follower_pos[i]
            info = f"{self.leader_pos[i]:<12} {self.follower_pos[i]:<12} {diff:<10}"
            self.stdscr.addstr(5 + i, 18, info)

        self.stdscr.addstr(11, 18, info)


class FollowerThread(Thread):
    def __init__(self, follower: PiperInterface, app: TeleopFollowApp) -> None:
        super().__init__()
        self.follower = follower
        self.app = app

    def worker(self) -> None:
        while not self.is_exited():
            match self.follower.read_message():
                case JointFeedback12Message() as msg:
                    self.app.follower_pos[0] = msg.joint_1
                    self.app.follower_pos[1] = msg.joint_2

                case JointFeedback34Message() as msg:
                    self.app.follower_pos[2] = msg.joint_3
                    self.app.follower_pos[3] = msg.joint_4

                case JointFeedback56Message() as msg:
                    self.app.follower_pos[4] = msg.joint_5
                    self.app.follower_pos[5] = msg.joint_6

                case GripperFeedbackMessage() as msg:
                    self.app.follower_pos[6] = msg.position


def command_teleop_follow(args: argparse.Namespace) -> None:
    with (
        PiperInterface(args.leader_can) as leader,
        PiperInterface(args.follower_can) as follower,
        TeleopFollowApp() as app,
        FollowerThread(follower, app),
    ):
        while not app.is_exited():
            match leader.read_message():
                case JointFeedback12Message() as msg:
                    app.leader_pos[0] = msg.joint_1
                    app.leader_pos[1] = msg.joint_2

                    follower.set_motion_control_b("joint", 100)
                    follower.set_joint_control_12(msg.joint_1, msg.joint_2)

                case JointFeedback34Message() as msg:
                    app.leader_pos[2] = msg.joint_3
                    app.leader_pos[3] = msg.joint_4

                    follower.set_joint_control_34(msg.joint_3, msg.joint_4)

                case JointFeedback56Message() as msg:
                    app.leader_pos[4] = msg.joint_5
                    app.leader_pos[5] = msg.joint_6

                    follower.set_joint_control_56(msg.joint_5, msg.joint_6)

                case GripperFeedbackMessage() as msg:
                    app.leader_pos[6] = msg.position
                    follower.set_gripper_control(msg.position, 1000)


__all__ = ["command_teleop_follow"]
