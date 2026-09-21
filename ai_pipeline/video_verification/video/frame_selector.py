from __future__ import annotations

import cv2
import numpy as np

from .frame_types import FramePacket


class FrameSelector:
    def __init__(self, difference_threshold: float = 5.0) -> None:
        if difference_threshold < 0:
            raise ValueError("difference_threshold cannot be negative")

        self.difference_threshold = difference_threshold
        self.previous_gray: np.ndarray | None = None

    def should_process(self, packet: FramePacket) -> bool:
        """
        Decide whether the current frame should be processed.
        """

        gray_frame = cv2.cvtColor(packet.image, cv2.COLOR_BGR2GRAY)

        if self.previous_gray is None:
            self.previous_gray = gray_frame
            return True

        difference = cv2.absdiff(self.previous_gray, gray_frame)
        mean_difference = float(np.mean(difference))

        if mean_difference >= self.difference_threshold:
            self.previous_gray = gray_frame
            return True

        return False

    def reset(self) -> None:
        """
        Reset the selector state for a new video or sequence.
        """

        self.previous_gray = None