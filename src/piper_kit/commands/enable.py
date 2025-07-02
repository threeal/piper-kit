import argparse
import time

from piper_kit import PiperInterface


def command_enable(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper:
        piper.enable_all_joints()

        while True:
            infos = piper.read_all_motor_info_bs()
            if all(i.driver_status.driver_enabled for i in infos):
                break

        piper.set_motion_control_b("joint", 20)
        time.sleep(0.1)

        piper.set_joint_control(0, 0, 0, 0, 0, 0)


__all__ = ["command_enable"]
