from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class FramePacket:
    """
    Represents one frame extracted from a video stream.
    """

    frame_id: int
    timestamp_ms: float
    image: np.ndarray

    width: int
    height: int
    source_fps: float

    @property
    def shape(self) -> tuple[int, int, int]:
        """
        Returns the frame shape as (height, width, channels).
        """
        return self.image.shape