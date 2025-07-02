import argparse
import time

from piper_sdk import C_PiperInterface_V2

from piper_cli import PiperInterface


def command_enable(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as p:
        p.enable_all_joints()

        piper = C_PiperInterface_V2(args.can_interface)
        piper.ConnectPort()

        while True:
            infos = p.read_all_motor_info_bs()
            if all(i.driver_status.driver_enabled for i in infos):
                break

        p.set_motion_control_b("joint", 20)
        time.sleep(0.1)

        piper.JointCtrl(0, 0, 0, 0, 0, 0)


__all__ = ["command_enable"]
