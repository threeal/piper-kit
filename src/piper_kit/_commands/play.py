import argparse
import csv
import sys
import time
from pathlib import Path

from piper_kit import Piper


def interpolate(x0: float, y0: float, x1: float, y1: float, x: float) -> float:
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def on_command(args: argparse.Namespace) -> None:
    sys.stdout.write("initializing...\n")
    with (
        Piper(args.can_interface) as piper,
        Path(args.csv_file).open() as csv_file,
    ):
        reader = csv.reader(csv_file)

        sys.stdout.write("reading joint and gripper positions...\n")
        prev_joints = piper.read_all_joint_feedbacks()
        prev_gripper = piper.read_gripper_feedback().position
        next_joints = prev_joints
        next_gripper = prev_gripper

        try:
            prev_t = time.time()
            dt = 0
            max_dt = 0
            while True:
                t = time.time()
                dt += t - prev_t
                prev_t = t

                while dt >= max_dt:
                    dt -= max_dt

                    prev_joints = next_joints
                    prev_gripper = next_gripper

                    row = next(reader)
                    max_dt = float(row[0])
                    next_joints = [float(v) for v in row[1:7]]
                    next_gripper = float(row[7])

                    sys.stdout.write(
                        f"next target: {[max_dt, *next_joints, next_gripper]}\n"
                    )

                joints = [
                    interpolate(0, prev_joints[i], max_dt, next_joints[i], dt)
                    for i in range(6)
                ]
                gripper = interpolate(0, prev_gripper, max_dt, next_gripper, dt)

                piper.set_motion_control_b("joint", 100)
                piper.set_joint_control(*(round(j) for j in joints))
                piper.set_gripper_control(round(gripper), 1000)

                time.sleep(1 / 100)

        except StopIteration:
            piper.set_motion_control_b("joint", 100)
            piper.set_joint_control(*(round(j) for j in prev_joints))
            piper.set_gripper_control(round(prev_gripper), 1000)

        sys.stdout.write("finished playing trajectories\n")


def register_play_command(subparsers: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("play", help="play trajectories with the PiPER arm")
    parser.set_defaults(func=on_command)
    parser.add_argument("csv_file", help="CSV file containing trajectory data")
    parser.add_argument(
        "can_interface", nargs="?", default="can0", help="CAN interface to use"
    )


__all__ = ["register_play_command"]
