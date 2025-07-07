import argparse

from cursers import ThreadedApp

from piper_kit import PiperInterface
from piper_kit.messages import GripperFeedbackMessage


class TeleopEndPoseApp(ThreadedApp):
    def __init__(self) -> None:
        super().__init__()

        self.target_x = 50000
        self.target_y = 0
        self.target_z = 260000

        self.target_pitch = -90000
        self.target_roll = 0
        self.target_yaw = -90000

        self.current_gripper = 0
        self.target_gripper = 0

    def on_enter(self) -> None:
        title = "PiPER End-Effector Pose Teleoperation"
        self.draw_text(0, (55 - len(title)) // 2, title, bold=True)

        self.draw_text(3, 2, "End-Effector Pose Information:", bold=True)
        self.draw_text(4, 4, "Position (XYZ):")
        self.draw_text(5, 4, "Rotation (PRY):")

        self.draw_text(7, 2, "Gripper Information:", bold=True)
        self.draw_text(8, 4, "Target Position:")
        self.draw_text(9, 4, "Current Position:")

        self.draw_text(11, 2, "Keyboard Controls:", bold=True)
        self.draw_text(14, 4, "W/S - Move X position")
        self.draw_text(15, 4, "A/D - Move Y position")
        self.draw_text(16, 4, "Q/E - Move Z position")
        self.draw_text(18, 4, "I/K - Rotate pitch rotation")
        self.draw_text(17, 4, "U/O - Rotate roll rotation")
        self.draw_text(19, 4, "J/L - Rotate yaw rotation")
        self.draw_text(20, 4, "F/H - Open/close gripper")
        self.draw_text(22, 4, "ESC - Exit teleoperation", bold=True)

    def on_update(self, key: int) -> None:  # noqa: C901, PLR0912
        match chr(key) if key != -1 else None:
            case "\x1b":  # ESC
                self.exit()
                return
            case "w" | "W":
                self.target_x += 5000
            case "s" | "S":
                self.target_x -= 5000
            case "a" | "A":
                self.target_y += 5000
            case "d" | "D":
                self.target_y -= 5000
            case "q" | "Q":
                self.target_z -= 5000
            case "e" | "E":
                self.target_z += 5000
            case "i" | "I":
                self.target_pitch += 5000
            case "k" | "K":
                self.target_pitch -= 5000
            case "j" | "J":
                self.target_yaw += 5000
            case "l" | "L":
                self.target_yaw -= 5000
            case "u" | "U":
                self.target_roll -= 5000
            case "o" | "O":
                self.target_roll += 5000
            case "f" | "F":
                self.target_gripper += 5000
            case "h" | "H":
                self.target_gripper -= 5000

        text = f"{self.target_x:>8} {self.target_y:>8} {self.target_z:>8}"
        self.draw_text(4, 22, text)

        text = f"{self.target_pitch:>8} {self.target_roll:>8} {self.target_yaw:>8}"
        self.draw_text(5, 22, text)

        self.draw_text(8, 22, f"{self.target_gripper:>8}")
        self.draw_text(9, 22, f"{self.current_gripper:>8}")


def command_teleop_end_pose(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper, TeleopEndPoseApp() as app:
        while app.is_running():
            match piper.read_message():
                case GripperFeedbackMessage() as msg:
                    app.current_gripper = msg.position

                    piper.set_motion_control_b("end_pose", 20)
                    piper.set_end_pose_control(
                        app.target_x,
                        app.target_y,
                        app.target_z,
                        app.target_pitch,
                        app.target_roll,
                        app.target_yaw,
                    )

                    piper.set_gripper_control(app.target_gripper, 1000)


__all__ = ["command_teleop_end_pose"]
