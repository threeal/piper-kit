import argparse

from cursers import ThreadedApp

from piper_kit import PiperInterface
from piper_kit.messages import (
    GripperFeedbackMessage,
    JointFeedback12Message,
    JointFeedback34Message,
    JointFeedback56Message,
)


class TeleopJointApp(ThreadedApp):
    def __init__(self) -> None:
        super().__init__()

        self.current_pos = [0, 0, 0, 0, 0, 0, 0]
        self.target_pos = [0, 0, 0, 0, 0, 0, 45000]

    def on_enter(self) -> None:
        title = "PiPER Joint Teleoperation"
        self.draw_text(0, (55 - len(title)) // 2, title, bold=True)

        self.draw_text(3, 2, "Joint Information:", bold=True)

        headers = f"{'Joint':<15} {'Target':<12} {'Current':<12} {'Diff':<10}"
        self.draw_text(4, 2, headers, underline=True)

        self.draw_text(5, 2, "Base (J1):")
        self.draw_text(6, 2, "Shoulder (J2):")
        self.draw_text(7, 2, "Elbow (J3):")
        self.draw_text(8, 2, "Wrist1 (J4):")
        self.draw_text(9, 2, "Wrist2 (J5):")
        self.draw_text(10, 2, "Wrist3 (J6):")
        self.draw_text(11, 2, "Gripper:")

        self.draw_text(13, 2, "Keyboard Controls:", bold=True)
        self.draw_text(14, 4, "Base (J1):     A/D - Rotate left/right")
        self.draw_text(15, 4, "Shoulder (J2): W/S - Move up/down")
        self.draw_text(16, 4, "Elbow (J3):    I/K - Move up/down")
        self.draw_text(17, 4, "Wrist1 (J4):   J/L - Rotate left/right")
        self.draw_text(18, 4, "Wrist2 (J5):   Q/E - Rotate left/right")
        self.draw_text(19, 4, "Wrist3 (J6):   U/O - Rotate left/right")
        self.draw_text(20, 4, "Gripper:       F/H - Open/close")
        self.draw_text(22, 4, "ESC - Exit teleoperation", bold=True)

    def on_update(self, key: int) -> None:  # noqa: C901, PLR0912
        match chr(key) if key != -1 else None:
            case "\x1b":  # ESC
                self.exit()
                return
            case "w" | "W":
                self.target_pos[1] += 5000
            case "s" | "S":
                self.target_pos[1] -= 5000
            case "a" | "A":
                self.target_pos[0] += 5000
            case "d" | "D":
                self.target_pos[0] -= 5000
            case "q" | "Q":
                self.target_pos[4] += 5000
            case "e" | "E":
                self.target_pos[4] -= 5000
            case "i" | "I":
                self.target_pos[2] -= 5000
            case "k" | "K":
                self.target_pos[2] += 5000
            case "j" | "J":
                self.target_pos[3] -= 5000
            case "l" | "L":
                self.target_pos[3] += 5000
            case "u" | "U":
                self.target_pos[5] -= 5000
            case "o" | "O":
                self.target_pos[5] += 5000
            case "f" | "F":
                self.target_pos[6] += 5000
            case "h" | "H":
                self.target_pos[6] -= 5000

        for i in range(7):
            diff = self.target_pos[i] - self.current_pos[i]
            info = f"{self.target_pos[i]:<12} {self.current_pos[i]:<12} {diff:<10}"
            self.draw_text(5 + i, 18, info)

        self.draw_text(11, 18, info)


def command_teleop_joint(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper, TeleopJointApp() as app:
        while app.is_running():
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
