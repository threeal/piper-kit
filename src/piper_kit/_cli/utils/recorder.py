import time
from pathlib import Path
from typing import Self

import h5py
import numpy as np


class Recorder:
    def __init__(self, *, record_file: str | None = None) -> None:
        self._record_file = Path(record_file) if record_file is not None else None
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
        if self._is_recording:
            self._is_recording = False

            self._record_file.parent.mkdir(parents=True, exist_ok=True)
            with h5py.File(self._record_file, "w") as f:
                data = np.array(self._joint_controls_12)
                f.create_dataset("joint_controls_12", data=data, compression="gzip")

                data = np.array(self._joint_controls_34)
                f.create_dataset("joint_controls_34", data=data, compression="gzip")

                data = np.array(self._joint_controls_56)
                f.create_dataset("joint_controls_56", data=data, compression="gzip")

                data = np.array(self._gripper_controls)
                f.create_dataset("gripper_controls", data=data, compression="gzip")

                data = np.array(self._joint_feedbacks_12)
                f.create_dataset("joint_feedbacks_12", data=data, compression="gzip")

                data = np.array(self._joint_feedbacks_34)
                f.create_dataset("joint_feedbacks_34", data=data, compression="gzip")

                data = np.array(self._joint_feedbacks_56)
                f.create_dataset("joint_feedbacks_56", data=data, compression="gzip")

                data = np.array(self._gripper_feedbacks)
                f.create_dataset("gripper_feedbacks", data=data, compression="gzip")

                for i, frame in enumerate(self._frames):
                    data = np.array(self._frames[i])
                    f.create_dataset(f"frames/{i}", data=data, compression="gzip")

                data = np.array(self._frame_times)
                f.create_dataset("frame_times", data=data, compression="gzip")

    def reset_records(self) -> None:
        self._start_time = time.time()

        self._joint_controls_12 = []
        self._joint_controls_34 = []
        self._joint_controls_56 = []
        self._gripper_controls = []

        self._joint_feedbacks_12 = []
        self._joint_feedbacks_34 = []
        self._joint_feedbacks_56 = []
        self._gripper_feedbacks = []

        self._frames = []
        self._frame_times = []

    def record_joint_control_12(self, joint_1: int, joint_2: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._joint_controls_12.append([t, joint_1, joint_2])

    def record_joint_control_34(self, joint_3: int, joint_4: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._joint_controls_34.append([t, joint_3, joint_4])

    def record_joint_control_56(self, joint_5: int, joint_6: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._joint_controls_56.append([t, joint_5, joint_6])

    def record_gripper_control(self, gripper: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._gripper_controls.append([t, gripper])

    def record_joint_feedback_12(self, joint_1: int, joint_2: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._joint_feedbacks_12.append([t, joint_1, joint_2])

    def record_joint_feedback_34(self, joint_3: int, joint_4: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._joint_feedbacks_34.append([t, joint_3, joint_4])

    def record_joint_feedback_56(self, joint_5: int, joint_6: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._joint_feedbacks_56.append([t, joint_5, joint_6])

    def record_gripper_feedback(self, gripper: int) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._gripper_feedbacks.append([t, gripper])

    def record_frame(self, frame: np.ndarray) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._frames.append(frame)
            self._frame_times.append(t)


__all__ = ["Recorder"]
