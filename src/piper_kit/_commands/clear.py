import argparse

from piper_kit import Piper


def on_command(args: argparse.Namespace) -> None:
    with Piper(args.can_interface) as piper:
        piper.set_all_joint_configs(clear_error=True)


def register_clear_command(subparsers: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("clear", help="clear errors of the PiPER arm")
    parser.set_defaults(func=on_command)
    parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )


__all__ = ["register_clear_command"]
