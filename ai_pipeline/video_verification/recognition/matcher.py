from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .gallery import StudentGallery


@dataclass
class MatchResult:
    student_id: str | None
    similarity: float
    is_match: bool


class FaceMatcher:
    def __init__(
        self,
        threshold: float = 0.75,
    ) -> None:
        if not -1.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between -1 and 1")

        self.threshold = threshold

    def match(
        self,
        embedding: np.ndarray,
        gallery: StudentGallery,
    ) -> MatchResult:
        if embedding.size == 0:
            raise ValueError("Embedding cannot be empty")

        query = self._normalize(embedding)

        best_student_id = None
        best_similarity = -1.0

        for entry in gallery.all_entries():
            similarity = float(
                np.dot(query, entry.embedding)
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_student_id = entry.student_id

        if best_student_id is None:
            return MatchResult(
                student_id=None,
                similarity=0.0,
                is_match=False,
            )

        is_match = best_similarity >= self.threshold

        return MatchResult(
            student_id=best_student_id if is_match else None,
            similarity=best_similarity,
            is_match=is_match,
        )

    @staticmethod
    def _normalize(embedding: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(embedding)

        if norm == 0:
            raise ValueError("Embedding cannot have zero norm")

        return embedding.astype(np.float32) / norm