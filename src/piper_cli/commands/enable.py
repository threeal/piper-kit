import argparse
import time

from piper_sdk import C_PiperInterface_V2

from piper_cli import PiperInterface


def command_enable(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as p:
        p.enable_all_joints()

        piper = C_PiperInterface_V2(args.can_interface)
        piper.ConnectPort()

        enabled = False
        while not enabled:
            time.sleep(0.1)
            info = piper.GetArmLowSpdInfoMsgs()
            enabled = all(
                [
                    info.motor_1.foc_status.driver_enable_status,
                    info.motor_2.foc_status.driver_enable_status,
                    info.motor_3.foc_status.driver_enable_status,
                    info.motor_4.foc_status.driver_enable_status,
                    info.motor_5.foc_status.driver_enable_status,
                    info.motor_6.foc_status.driver_enable_status,
                ]
            )

        piper.MotionCtrl_2(0x01, 0x01, 20, 0x00)
        time.sleep(0.1)

        piper.JointCtrl(0, 0, 0, 0, 0, 0)


__all__ = ["command_enable"]
