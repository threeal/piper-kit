import argparse

from .end_pose import register_end_pose_command
from .follow import register_follow_command
from .joint import register_joint_command


def register_teleop_commands(subparsers: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("teleop", help="teleop the PiPER arm")
    subparsers = parser.add_subparsers(required=True)

    register_end_pose_command(subparsers)
    register_follow_command(subparsers)
    register_joint_command(subparsers)


__all__ = ["register_teleop_commands"]
