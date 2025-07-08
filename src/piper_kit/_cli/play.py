import argparse
import csv
import h5py
import sys
import time
from pathlib import Path

from piper_kit import PiperInterface


def command_play(args: argparse.Namespace) -> None:
    sys.stdout.write("initializing...\n")
    with (
        PiperInterface(args.can_interface) as piper,
        h5py.File(args.csv_file, "r") as f
    ):
        joint_controls_12 = f["joint_controls_12"][:]
        joint_controls_34 = f["joint_controls_34"][:]
        joint_controls_56 = f["joint_controls_56"][:]
        gripper_controls = f["gripper_controls"][:]

        jc12_i = 0
        jc34_i = 0
        jc56_i = 0
        gc_i = 0

        sys.stdout.write("reading joint and gripper positions...\n")
        joints = piper.read_all_joint_feedbacks()
        gripper = piper.read_gripper_feedback().position

        start_t = time.time()
        while jc12_i < len(joint_controls_12) or jc34_i < len(joint_controls_34) or jc56_i < len(joint_controls_56) or gc_i < len(gripper_controls):
            t = time.time() - start_t

            while jc12_i < len(joint_controls_12) and joint_controls_12[jc12_i][0] <= t:
                joints[0] = joint_controls_12[jc12_i][1]
                joints[1] = joint_controls_12[jc12_i][2]
                jc12_i += 1

            while jc34_i < len(joint_controls_34) and joint_controls_34[jc34_i][0] <= t:
                joints[2] = joint_controls_34[jc34_i][1]
                joints[3] = joint_controls_34[jc34_i][2]
                jc34_i += 1

            while jc56_i < len(joint_controls_56) and joint_controls_56[jc56_i][0] <= t:
                joints[4] = joint_controls_56[jc56_i][1]
                joints[5] = joint_controls_56[jc56_i][2]
                jc56_i += 1

            while gc_i < len(gripper_controls) and gripper_controls[gc_i][0] <= t:
                gripper = gripper_controls[gc_i][1]
                gc_i += 1


            piper.set_motion_control_b("joint", 100)
            piper.set_joint_control(*(round(j) for j in joints))
            piper.set_gripper_control(round(gripper), 1000)

            time.sleep(1 / 100)

        piper.set_motion_control_b("joint", 100)
        piper.set_joint_control(*(round(j) for j in joints))
        piper.set_gripper_control(round(gripper), 1000)

        sys.stdout.write("finished playing trajectories\n")


__all__ = ["command_play"]
