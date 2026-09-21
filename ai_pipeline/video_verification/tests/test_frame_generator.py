import cv2
import numpy as np

from video_verification.video.frame_generator import FrameGenerator


def create_test_video(path, frame_count=30, fps=10):
    height, width = 100, 100

    writer = cv2.VideoWriter(
        str(path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    for i in range(frame_count):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = (i % 255, 0, 0)
        writer.write(frame)

    writer.release()


def test_frame_generator(tmp_path):
    video_path = tmp_path / "test_video.mp4"

    create_test_video(video_path, frame_count=30, fps=10)

    generator = FrameGenerator(
        source=video_path,
        sample_fps=5,
        max_frames=3,
    )

    frames = list(generator)

    assert len(frames) == 3
    assert frames[0].frame_id == 0
    assert frames[1].frame_id == 2
    assert frames[2].frame_id == 4

    assert frames[0].width == 100
    assert frames[0].height == 100
    assert frames[0].source_fps == 10