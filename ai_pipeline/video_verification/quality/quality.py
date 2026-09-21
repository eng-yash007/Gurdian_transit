from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from ..detection.face_detector import FaceDetection


@dataclass
class QualityResult:
    is_acceptable: bool
    face_width: int
    face_height: int
    sharpness: float
    brightness: float
    reasons: list[str]


class FaceQualityAssessor:
    def __init__(
        self,
        min_face_size: int = 50,
        min_sharpness: float = 50.0,
        min_brightness: float = 40.0,
        max_brightness: float = 220.0,
    ) -> None:
        if min_face_size <= 0:
            raise ValueError("min_face_size must be positive")

        if min_sharpness < 0:
            raise ValueError("min_sharpness cannot be negative")

        if not 0 <= min_brightness <= 255:
            raise ValueError("min_brightness must be between 0 and 255")

        if not 0 <= max_brightness <= 255:
            raise ValueError("max_brightness must be between 0 and 255")

        if min_brightness >= max_brightness:
            raise ValueError(
                "min_brightness must be less than max_brightness"
            )

        self.min_face_size = min_face_size
        self.min_sharpness = min_sharpness
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness

    def assess(
        self,
        image: np.ndarray,
        detection: FaceDetection,
    ) -> QualityResult:
        if image is None or image.size == 0:
            raise ValueError("Image cannot be empty")

        x, y, width, height = detection.box

        image_height, image_width = image.shape[:2]

        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(image_width, x + width)
        y2 = min(image_height, y + height)

        if x1 >= x2 or y1 >= y2:
            raise ValueError("Face bounding box is outside the image")

        face_crop = image[y1:y2, x1:x2]

        actual_width = x2 - x1
        actual_height = y2 - y1

        gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)

        sharpness = float(cv2.Laplacian(gray_face, cv2.CV_64F).var())
        brightness = float(np.mean(gray_face))

        reasons: list[str] = []

        if min(actual_width, actual_height) < self.min_face_size:
            reasons.append("face_too_small")

        if sharpness < self.min_sharpness:
            reasons.append("face_too_blurry")

        if brightness < self.min_brightness:
            reasons.append("face_too_dark")

        if brightness > self.max_brightness:
            reasons.append("face_overexposed")

        return QualityResult(
            is_acceptable=len(reasons) == 0,
            face_width=actual_width,
            face_height=actual_height,
            sharpness=sharpness,
            brightness=brightness,
            reasons=reasons,
        )