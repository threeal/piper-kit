import argparse

from piper_kit import PiperInterface


def command_clear(args: argparse.Namespace) -> None:
    with PiperInterface(args.can_interface) as piper:
        piper.set_all_joint_configs(clear_error=True)


__all__ = ["command_clear"]
