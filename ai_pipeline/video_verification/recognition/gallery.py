from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class GalleryEntry:
    student_id: str
    embedding: np.ndarray


class StudentGallery:
    def __init__(self) -> None:
        self.entries: dict[str, GalleryEntry] = {}

    def add_student(
        self,
        student_id: str,
        embedding: np.ndarray,
    ) -> None:
        if not student_id.strip():
            raise ValueError("student_id cannot be empty")

        if embedding.size == 0:
            raise ValueError("Embedding cannot be empty")

        normalized_embedding = self._normalize(embedding)

        self.entries[student_id] = GalleryEntry(
            student_id=student_id,
            embedding=normalized_embedding,
        )

    def get_embedding(self, student_id: str) -> np.ndarray | None:
        entry = self.entries.get(student_id)

        if entry is None:
            return None

        return entry.embedding

    def remove_student(self, student_id: str) -> bool:
        return self.entries.pop(student_id, None) is not None

    def all_entries(self) -> list[GalleryEntry]:
        return list(self.entries.values())

    @staticmethod
    def _normalize(embedding: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(embedding)

        if norm == 0:
            raise ValueError("Embedding cannot have zero norm")

        return embedding.astype(np.float32) / norm

    def clear(self) -> None:
        self.entries.clear()