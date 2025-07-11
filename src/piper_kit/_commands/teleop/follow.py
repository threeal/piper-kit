import argparse

from cursers import Thread, ThreadedApp

from piper_kit import Piper
from piper_kit.messages import (
    GripperFeedbackMessage,
    JointFeedback12Message,
    JointFeedback34Message,
    JointFeedback56Message,
)


class TeleopFollowApp(ThreadedApp):
    def __init__(self) -> None:
        super().__init__()

        self.leader_pos = [0, 0, 0, 0, 0, 0, 0]
        self.follower_pos = [0, 0, 0, 0, 0, 0, 0]

    def on_enter(self) -> None:
        title = "PiPER Leader-Follower Teleoperation"
        self.draw_text(0, (55 - len(title)) // 2, title, bold=True)

        self.draw_text(3, 2, "Joint Information:", bold=True)

        headers = f"{'Joint':<15} {'Leader':<12} {'Follower':<12} {'Diff':<10}"
        self.draw_text(4, 2, headers, underline=True)

        self.draw_text(5, 2, "Base (J1):")
        self.draw_text(6, 2, "Shoulder (J2):")
        self.draw_text(7, 2, "Elbow (J3):")
        self.draw_text(8, 2, "Wrist1 (J4):")
        self.draw_text(9, 2, "Wrist2 (J5):")
        self.draw_text(10, 2, "Wrist3 (J6):")
        self.draw_text(11, 2, "Gripper:")

        self.draw_text(13, 2, "Keyboard Controls:", bold=True)
        self.draw_text(14, 4, "ESC - Exit teleoperation", bold=True)

    def on_update(self, key: int) -> None:
        match chr(key) if key != -1 else None:
            case "\x1b":  # ESC
                self.exit()
                return

        for i in range(6):
            diff = self.leader_pos[i] - self.follower_pos[i]
            info = f"{self.leader_pos[i]:<12} {self.follower_pos[i]:<12} {diff:<10}"
            self.draw_text(5 + i, 18, info)

        self.draw_text(11, 18, info)


class FollowerThread(Thread):
    def __init__(self, follower: Piper, app: TeleopFollowApp) -> None:
        super().__init__()
        self._follower = follower
        self._app = app

    def run(self) -> None:
        while self._app.is_running():
            match self._follower.read_message():
                case JointFeedback12Message() as msg:
                    self._app.follower_pos[0] = msg.joint_1
                    self._app.follower_pos[1] = msg.joint_2

                case JointFeedback34Message() as msg:
                    self._app.follower_pos[2] = msg.joint_3
                    self._app.follower_pos[3] = msg.joint_4

                case JointFeedback56Message() as msg:
                    self._app.follower_pos[4] = msg.joint_5
                    self._app.follower_pos[5] = msg.joint_6

                case GripperFeedbackMessage() as msg:
                    self._app.follower_pos[6] = msg.position


def on_command(args: argparse.Namespace) -> None:
    with (
        Piper(args.leader_can) as leader,
        Piper(args.follower_can) as follower,
        TeleopFollowApp() as app,
        FollowerThread(follower, app),
    ):
        while app.is_running():
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


def register_follow_command(subparsers: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser(
        "follow", help="teleop the follower PiPER arm using the leader PiPER arm"
    )
    parser.set_defaults(func=on_command)
    parser.add_argument("leader_can", help="CAN interface of the leader to use")
    parser.add_argument(
        "follower_can",
        nargs="?",
        default="can0",
        help="CAN interface of the follower to use",
    )


__all__ = ["register_follow_command"]
