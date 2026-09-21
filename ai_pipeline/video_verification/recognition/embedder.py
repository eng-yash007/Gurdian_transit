from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class FaceEmbedder(ABC):
    @abstractmethod
    def generate_embedding(self, face_image: np.ndarray) -> np.ndarray:
        """
        Convert a face image into a numerical embedding.
        """
        raise NotImplementedError


class DummyFaceEmbedder(FaceEmbedder):
    def __init__(self, embedding_dimension: int = 128) -> None:
        if embedding_dimension <= 0:
            raise ValueError("embedding_dimension must be positive")

        self.embedding_dimension = embedding_dimension

    def generate_embedding(self, face_image: np.ndarray) -> np.ndarray:
        if face_image is None or face_image.size == 0:
            raise ValueError("Face image cannot be empty")

        # Temporary deterministic embedding for architecture testing.
        mean_value = float(np.mean(face_image))

        embedding = np.full(
            self.embedding_dimension,
            mean_value,
            dtype=np.float32,
        )

        norm = np.linalg.norm(embedding)

        if norm > 0:
            embedding = embedding / norm

        return embedding