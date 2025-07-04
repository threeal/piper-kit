import argparse
import csv
import sys
import time
from pathlib import Path

from piper_kit import PiperInterface


def interpolate(x0: float, y0: float, x1: float, y1: float, x: float) -> float:
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def command_play(args: argparse.Namespace) -> None:
    sys.stdout.write("initializing...\n")
    with (
        PiperInterface(args.can_interface) as piper,
        Path(args.csv_file).open() as csv_file,
    ):
        reader = csv.reader(csv_file)

        sys.stdout.write("reading joint and gripper positions...\n")
        prev_joints = piper.read_all_joint_feedbacks()
        prev_gripper = piper.read_gripper_feedback().position
        next_joints = prev_joints
        next_gripper = prev_gripper

        try:
            start_t = time.time()
            prev_t = start_t
            next_t = start_t
            while True:
                t = time.time()
                while t >= next_t:
                    prev_t = next_t
                    prev_joints = next_joints
                    prev_gripper = next_gripper

                    row = next(reader)
                    next_t = start_t + float(row[0])
                    next_joints = [float(v) for v in row[1:7]]
                    next_gripper = float(row[7])

                    sys.stdout.write(f"next target: {[*next_joints, next_gripper]}\n")

                joints = [
                    interpolate(prev_t, prev_joints[i], next_t, next_joints[i], t)
                    for i in range(6)
                ]
                gripper = interpolate(prev_t, prev_gripper, next_t, next_gripper, t)

                piper.set_motion_control_b("joint", 100)
                piper.set_joint_control(*(round(j) for j in joints))
                piper.set_gripper_control(round(gripper), 1000)

                time.sleep(1 / 100)

        except StopIteration:
            piper.set_motion_control_b("joint", 100)
            piper.set_joint_control(*(round(j) for j in prev_joints))
            piper.set_gripper_control(round(prev_gripper), 1000)

        sys.stdout.write("finished playing trajectories\n")


__all__ = ["command_play"]
