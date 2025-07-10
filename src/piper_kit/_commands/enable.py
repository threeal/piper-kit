import argparse
import time

from piper_kit import PiperInterface


def on_command(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper:
        piper.enable_all_joints()

        while True:
            infos = piper.read_all_motor_info_bs()
            if all(i.driver_status.driver_enabled for i in infos):
                break

        piper.set_motion_control_b("joint", 20)
        time.sleep(0.1)

        piper.set_joint_control(0, 0, 0, 0, 0, 0)
        piper.set_gripper_control(45000, 1000)


def register_enable_command(subparsers: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("enable", help="enable the PiPER arm")
    parser.set_defaults(func=on_command)
    parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )


__all__ = ["register_enable_command"]
