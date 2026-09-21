from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from video_verification.detection.face_detector import FaceDetection


@dataclass
class FaceCrop:
    image: np.ndarray
    x: int
    y: int
    width: int
    height: int

    @property
    def box(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height


class FaceCropper:
    def __init__(self, padding_ratio: float = 0.20) -> None:
        if padding_ratio < 0:
            raise ValueError("padding_ratio cannot be negative")

        self.padding_ratio = padding_ratio

    def crop(
        self,
        image: np.ndarray,
        detection: FaceDetection,
    ) -> FaceCrop:
        if image is None or image.size == 0:
            raise ValueError("Image cannot be empty")

        image_height, image_width = image.shape[:2]

        x, y, width, height = detection.box

        if width <= 0 or height <= 0:
            raise ValueError("Face bounding box must have positive dimensions")

        # Calculate padding around the detected face.
        pad_x = int(width * self.padding_ratio)
        pad_y = int(height * self.padding_ratio)

        # Clamp coordinates to image boundaries.
        crop_x1 = max(0, x - pad_x)
        crop_y1 = max(0, y - pad_y)

        crop_x2 = min(image_width, x + width + pad_x)
        crop_y2 = min(image_height, y + height + pad_y)

        if crop_x1 >= crop_x2 or crop_y1 >= crop_y2:
            raise ValueError("Face crop lies outside image boundaries")

        cropped_image = image[crop_y1:crop_y2, crop_x1:crop_x2].copy()

        return FaceCrop(
            image=cropped_image,
            x=crop_x1,
            y=crop_y1,
            width=crop_x2 - crop_x1,
            height=crop_y2 - crop_y1,
        )