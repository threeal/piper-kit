import cv2
import h5py
import numpy as np

with h5py.File(".records/record_0.h5py", "r") as f:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 60, (1280, 480))

    times_0 = len(f["camera_frame_times_0"][:])
    times_1 = len(f["camera_frame_times_1"][:])
    for i in range(min(times_0, times_1)):
        frame_0 = cv2.imdecode(f[f"camera_frames_0/{i}"][:], cv2.IMREAD_COLOR)
        frame_1 = cv2.imdecode(f[f"camera_frames_1/{i}"][:], cv2.IMREAD_COLOR)
        out.write(np.hstack((frame_0, frame_1)))
