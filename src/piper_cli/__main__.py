import argparse
import time
import warnings

from piper_sdk import C_PiperInterface_V2

warnings.filterwarnings("ignore", category=SyntaxWarning, module=r"^piper_sdk(\.|$)")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="piper",
    )
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    parser.parse_args()

    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    while True:
        piper.EnableArm(7)
        piper.MotionCtrl_2(0x01, 0x01, 100, 0x00)
        piper.JointCtrl(0, 0, 0, 0, 0, 0)
        time.sleep(0.05)


if __name__ == "__main__":
    main()
