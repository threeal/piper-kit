import argparse
import time

from piper_sdk import C_PiperInterface_V2

from piper_cli import PiperInterface


def command_disable(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as p:
        piper = C_PiperInterface_V2(args.can_interface)
        piper.ConnectPort()

        piper.MotionCtrl_2(0x01, 0x01, 20, 0x00)
        time.sleep(0.1)

        positions = [0, 0, 0, 0, 17000, 0]
        piper.JointCtrl(*positions)

        done = False
        tolerance = 1000
        while not done:
            time.sleep(0.1)
            state = piper.GetArmJointMsgs().joint_state
            done = all(
                [
                    abs(state.joint_1 - positions[0]) <= tolerance,
                    abs(state.joint_2 - positions[1]) <= tolerance,
                    abs(state.joint_3 - positions[2]) <= tolerance,
                    abs(state.joint_4 - positions[3]) <= tolerance,
                    abs(state.joint_5 - positions[4]) <= tolerance,
                    abs(state.joint_6 - positions[5]) <= tolerance,
                ]
            )

        p.disable_all_joints()


__all__ = ["command_disable"]
