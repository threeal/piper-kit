import argparse

from .disable import command_disable
from .enable import command_enable
from .play import command_play
from .teleop import command_teleop_follow, command_teleop_joint


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

    play_parser = subparsers.add_parser(
        "play", help="play trajectories with the PiPER arm"
    )
    play_parser.set_defaults(func=command_play)
    play_parser.add_argument("csv_file", help="CSV file containing trajectory data")
    play_parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )

    teleop_parser = subparsers.add_parser("teleop", help="teleop the PiPER arm")
    teleop_subparsers = teleop_parser.add_subparsers(required=True)

    teleop_follow_parser = teleop_subparsers.add_parser(
        "follow", help="teleop the follower PiPER arm using the leader PiPER arm"
    )
    teleop_follow_parser.set_defaults(func=command_teleop_follow)
    teleop_follow_parser.add_argument(
        "leader_can", help="CAN interface of the leader to use"
    )
    teleop_follow_parser.add_argument(
        "follower_can",
        nargs="?",
        default="can0",
        help="CAN interface of the follower to use",
    )

    teleop_joint_parser = teleop_subparsers.add_parser(
        "joint", help="teleop the joint positions of PiPER arm"
    )
    teleop_joint_parser.set_defaults(func=command_teleop_joint)
    teleop_joint_parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
