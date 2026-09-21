from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class PreprocessedFace:
    image: np.ndarray
    original_shape: tuple[int, ...]
    processed_shape: tuple[int, ...]


class FacePreprocessor:
    def __init__(
        self,
        target_size: tuple[int, int] = (112, 112),
        normalize: bool = True,
    ) -> None:
        target_width, target_height = target_size

        if target_width <= 0 or target_height <= 0:
            raise ValueError("target_size values must be positive")

        self.target_size = target_size
        self.normalize = normalize

    def process(self, face_image: np.ndarray) -> PreprocessedFace:
        if face_image is None or face_image.size == 0:
            raise ValueError("Face image cannot be empty")

        if face_image.ndim != 3 or face_image.shape[2] != 3:
            raise ValueError("Face image must have three color channels")

        original_shape = face_image.shape

        resized = cv2.resize(
            face_image,
            self.target_size,
            interpolation=cv2.INTER_LINEAR,
        )

        rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        processed = rgb_image.astype(np.float32)

        if self.normalize:
            processed = processed / 255.0

        return PreprocessedFace(
            image=processed,
            original_shape=original_shape,
            processed_shape=processed.shape,
        )