import time
from pathlib import Path
from typing import Self

import h5py
import numpy as np


class Recorder:
    def __init__(self, *, record_file: str | None = None) -> None:
        self._record_file = Path(record_file)
        self._is_recording = False
        self.reset_records()

    def __enter__(self) -> Self:
        if self._record_file is not None:
            self.start_recording()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop_recording()

    def start_recording(self) -> None:
        self._is_recording = True

    def stop_recording(self) -> None:
        if self.is_recording:
            self._is_recording = False

            self._record_file.mkdir(parents=True, exist_ok=True)
            with h5py.File(self._record_file, "w") as f:
                data = np.array(self.joint_control_12)
                f.create_dataset("joint_control_12", data=data)

                data = np.array(self.joint_control_34)
                f.create_dataset("joint_control_34", data=data)

                data = np.array(self.joint_control_56)
                f.create_dataset("joint_control_56", data=data)

                data = np.array(self.gripper_control)
                f.create_dataset("gripper_control", data=data)

                data = np.array(self.joint_feedback_12)
                f.create_dataset("joint_feedback_12", data=data)

                data = np.array(self.joint_feedback_34)
                f.create_dataset("joint_feedback_34", data=data)

                data = np.array(self.joint_feedback_56)
                f.create_dataset("joint_feedback_56", data=data)

                data = np.array(self.gripper_feedback)
                f.create_dataset("gripper_feedback", data=data)

    def reset_records(self) -> None:
        self._start_time = time.time()

        self._joint_control_12 = []
        self._joint_control_34 = []
        self._joint_control_56 = []
        self._gripper_control = []

        self._joint_feedback_12 = []
        self._joint_feedback_34 = []
        self._joint_feedback_56 = []
        self._gripper_feedback = []

    def record_joint_control_12(self, joint_1: int, joint_2: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._joint_control_12.append([t, joint_1, joint_2])

    def record_joint_control_34(self, joint_3: int, joint_4: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._joint_control_34.append([t, joint_3, joint_4])

    def record_joint_control_56(self, joint_5: int, joint_6: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._joint_control_56.append([t, joint_5, joint_6])

    def record_gripper_control(self, gripper: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._gripper_control.append([t, gripper])

    def record_joint_feedbackl_12(self, joint_1: int, joint_2: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._joint_feedbackl_12.append([t, joint_1, joint_2])

    def record_joint_feedbackl_34(self, joint_3: int, joint_4: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._joint_feedbackl_34.append([t, joint_3, joint_4])

    def record_joint_feedbackl_56(self, joint_5: int, joint_6: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._joint_feedbackl_56.append([t, joint_5, joint_6])

    def record_gripper_feedbackl(self, gripper: int) -> None:
        if self._is_recording:
            t = time.time() - self.start_time
            self._gripper_feedbackl.append([t, gripper])


__all__ = ["Recorder"]
