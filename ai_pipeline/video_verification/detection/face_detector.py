from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class FaceDetection:
    x: int
    y: int
    width: int
    height: int
    confidence: float | None = None

    @property
    def box(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height


class FaceDetector:
    def __init__(
        self,
        scale_factor: float = 1.1,
        min_neighbors: int = 5,
        min_size: tuple[int, int] = (30, 30),
    ) -> None:
        cascade_path = cv2.data.haarcascades + (
            "haarcascade_frontalface_default.xml"
        )

        self.detector = cv2.CascadeClassifier(cascade_path)

        if self.detector.empty():
            raise RuntimeError("Unable to load Haar Cascade face detector")

        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, image: np.ndarray) -> list[FaceDetection]:
        if image is None or image.size == 0:
            raise ValueError("Image cannot be empty")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
        )

        return [
            FaceDetection(
                x=int(x),
                y=int(y),
                width=int(width),
                height=int(height),
            )
            for x, y, width, height in faces
        ]