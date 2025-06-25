import time

from piper_sdk import C_PiperInterface_V2


def command_enable() -> None:
    piper = C_PiperInterface_V2()
    piper.ConnectPort()

    while True:
        piper.EnableArm(7)
        piper.MotionCtrl_2(0x01, 0x01, 100, 0x00)
        piper.JointCtrl(0, 0, 0, 0, 0, 0)
        time.sleep(0.05)


__all__ = ["command_enable"]
