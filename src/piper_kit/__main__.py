"""Entry point for running PiPER Kit as a module."""

import argparse

from ._cli import register_commands


def _main() -> None:
    parser = argparse.ArgumentParser(prog="piper")
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    register_commands(parser)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    _main()
