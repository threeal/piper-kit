import argparse
import time

from piper_kit import Piper

JOINT_TOLERANCE = 1000


def on_command(args: argparse.Namespace) -> None:
    with Piper(args.can_interface) as piper:
        piper.set_motion_control_b("joint", 20)
        time.sleep(0.1)

        positions = [0, 0, 0, 0, 17000, 0]
        piper.set_joint_control(*positions)
        piper.set_gripper_control(90000, 1000)

        while True:
            feedbacks = piper.read_all_joint_feedbacks()
            if all(
                abs(p - f) <= JOINT_TOLERANCE
                for p, f in zip(positions, feedbacks, strict=False)
            ):
                break

        piper.disable_all_joints()
        piper.disable_gripper()


def register_disable_command(subparsers: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("disable", help="disable the PiPER arm")
    parser.set_defaults(func=on_command)
    parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )


__all__ = ["register_disable_command"]
