import cv2
import time
from cursers import Thread
from pathlib import Path
from typing import Self

import h5py
import numpy as np


class Recorder:

    class CameraCaptureThread(Thread):
        def __init__(self, idx: int, device: str, recorder: "Recorder") -> None:
            super().__init__()
            self._idx = idx
            self._device = device
            self._recorder = recorder

        def run(self) -> None:
            cap = cv2.VideoCapture(self._device)
            cap.set(cv2.CAP_PROP_FPS, 60)

            while self._recorder.is_recording() and cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    success, encoded_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    if success:
                        self._recorder.record_camera_frame(self._idx, encoded_frame)


    def __init__(self, *, record_file: str | None = None, camera_devices: list[str] = []) -> None:
        self._record_file = Path(record_file) if record_file is not None else None

        self._camera_captures = []
        for idx, device in enumerate(camera_devices):
            self._camera_captures.append(self.CameraCaptureThread(idx, device, self))

        self._is_recording = False
        self._reset_records()

    def __enter__(self) -> Self:
        if self._record_file is not None:
            self.start_recording()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop_recording()

    def start_recording(self) -> None:
        self._is_recording = True
        self._reset_records()
        for camera_capture in self._camera_captures:
            camera_capture.__enter__()

    def stop_recording(self) -> None:
        if self._is_recording:
            self._is_recording = False

            for camera_capture in self._camera_captures:
                camera_capture.__exit__()

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

                for camera_idx in range(len(self._camera_captures)):
                    for i, frame in enumerate(self._cameras_frames[camera_idx]):
                        data = np.array(frame)
                        f.create_dataset(f"camera_frames_{camera_idx}/{i}", data=data, compression="gzip")

                    data = np.array(self._cameras_frame_times[camera_idx])
                    f.create_dataset(f"camera_frame_times_{camera_idx}", data=data, compression="gzip")

        self._reset_records()

    def _reset_records(self) -> None:
        self._start_time = time.time()

        self._joint_controls_12 = []
        self._joint_controls_34 = []
        self._joint_controls_56 = []
        self._gripper_controls = []

        self._joint_feedbacks_12 = []
        self._joint_feedbacks_34 = []
        self._joint_feedbacks_56 = []
        self._gripper_feedbacks = []

        self._cameras_frames = [[] for _ in range(len(self._camera_captures))]
        self._cameras_frame_times = [[] for _ in range(len(self._camera_captures))]

    def is_recording(self) -> bool:
        return self._is_recording

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

    def record_camera_frame(self, camera_idx: int, frame: np.ndarray) -> None:
        if self._is_recording:
            t = time.time() - self._start_time
            self._cameras_frames[camera_idx].append(frame)
            self._cameras_frame_times[camera_idx].append(t)


__all__ = ["Recorder"]
