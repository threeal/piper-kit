import argparse

from .disable import command_disable
from .enable import command_enable


def main() -> None:
    parser = argparse.ArgumentParser(prog="piper")
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    subparsers = parser.add_subparsers(required=True)

    disable_parser = subparsers.add_parser("disable", help="disable the PiPER arm")
    disable_parser.set_defaults(func=command_disable)
    disable_parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )

    enable_parser = subparsers.add_parser("enable", help="enable the PiPER arm")
    enable_parser.set_defaults(func=command_enable)
    enable_parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
