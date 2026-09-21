from __future__ import annotations

from pathlib import Path
from typing import Iterator, Union

import cv2

from .frame_types import FramePacket


VideoSource = Union[str, int, Path]


class FrameGenerator:
    """
    Reads frames from a video file or camera.

    This component is responsible only for frame acquisition
    and basic sampling. It does not perform face detection.
    """

    def __init__(
        self,
        source: VideoSource,
        sample_fps: float = 5.0,
        max_frames: int | None = None,
    ) -> None:

        if sample_fps <= 0:
            raise ValueError("sample_fps must be greater than zero")

        self.source = source
        self.sample_fps = sample_fps
        self.max_frames = max_frames

        self.capture: cv2.VideoCapture | None = None

        self.source_fps = 0.0
        self.frame_interval = 1

    def open(self) -> None:
        """
        Open the video source and determine sampling parameters.
        """

        self.capture = cv2.VideoCapture(self.source)

        if not self.capture.isOpened():
            raise RuntimeError(f"Unable to open video source: {self.source}")

        self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)

        # Webcam FPS may be unavailable or invalid.
        if self.source_fps <= 0:
            self.source_fps = 30.0

        self.frame_interval = max(
            1,
            round(self.source_fps / self.sample_fps),
        )

    def __iter__(self) -> Iterator[FramePacket]:
        """
        Iterate over sampled frames.
        """

        if self.capture is None:
            self.open()

        assert self.capture is not None

        processed_frames = 0
        frame_id = 0

        try:
            while True:

                success, frame = self.capture.read()

                if not success:
                    break

                if frame_id % self.frame_interval == 0:

                    height, width = frame.shape[:2]

                    timestamp_ms = (
                        frame_id / self.source_fps
                    ) * 1000.0

                    yield FramePacket(
                        frame_id=frame_id,
                        timestamp_ms=timestamp_ms,
                        image=frame,
                        width=width,
                        height=height,
                        source_fps=self.source_fps,
                    )

                    processed_frames += 1

                    if (
                        self.max_frames is not None
                        and processed_frames >= self.max_frames
                    ):
                        break

                frame_id += 1

        finally:
            self.close()

    def close(self) -> None:
        """
        Release the video source.
        """

        if self.capture is not None:
            self.capture.release()
            self.capture = None