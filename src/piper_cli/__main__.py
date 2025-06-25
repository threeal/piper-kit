import argparse
import warnings

from .commands import command_enable

warnings.filterwarnings("ignore", category=SyntaxWarning, module=r"^piper_sdk(\.|$)")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="piper",
    )
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    parser.parse_args()

    command_enable()


if __name__ == "__main__":
    main()
