import argparse
import time

from piper_kit import PiperInterface

JOINT_TOLERANCE = 1000


def command_disable(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper:
        piper.set_motion_control_b("joint", 20)
        time.sleep(0.1)

        positions = [0, 0, 0, 0, 17000, 0]
        piper.set_joint_control(*positions)

        while True:
            feedbacks = piper.read_all_joint_feedbacks()
            if all(
                abs(p - f) <= JOINT_TOLERANCE
                for p, f in zip(positions, feedbacks, strict=False)
            ):
                break

        piper.disable_all_joints()


__all__ = ["command_disable"]
