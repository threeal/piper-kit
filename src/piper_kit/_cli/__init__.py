import argparse

from .clear import register_clear_command
from .disable import register_disable_command
from .enable import register_enable_command
from .play import register_play_command
from .teleop import register_teleop_commands


def register_commands(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(required=True)

    register_clear_command(subparsers)
    register_disable_command(subparsers)
    register_enable_command(subparsers)
    register_play_command(subparsers)
    register_teleop_commands(subparsers)


__all__ = ["register_commands"]
