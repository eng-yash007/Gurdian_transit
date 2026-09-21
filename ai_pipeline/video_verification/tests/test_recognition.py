import numpy as np
import pytest

from video_verification.recognition.embedder import DummyFaceEmbedder
from video_verification.recognition.gallery import StudentGallery
from video_verification.recognition.matcher import FaceMatcher


def test_dummy_embedder_generates_embedding():
    embedder = DummyFaceEmbedder(embedding_dimension=128)

    image = np.ones((100, 100, 3), dtype=np.uint8)

    embedding = embedder.generate_embedding(image)

    assert embedding.shape == (128,)
    assert embedding.dtype == np.float32


def test_dummy_embedder_rejects_empty_image():
    embedder = DummyFaceEmbedder()

    with pytest.raises(ValueError):
        embedder.generate_embedding(np.array([]))


def test_gallery_adds_student():
    gallery = StudentGallery()

    embedding = np.array([1.0, 0.0, 0.0], dtype=np.float32)

    gallery.add_student("STU001", embedding)

    stored = gallery.get_embedding("STU001")

    assert stored is not None
    assert np.isclose(np.linalg.norm(stored), 1.0)


def test_gallery_removes_student():
    gallery = StudentGallery()

    embedding = np.array([1.0, 0.0, 0.0], dtype=np.float32)

    gallery.add_student("STU001", embedding)

    assert gallery.remove_student("STU001") is True
    assert gallery.get_embedding("STU001") is None


def test_matcher_finds_student():
    gallery = StudentGallery()

    gallery.add_student(
        "STU001",
        np.array([1.0, 0.0, 0.0], dtype=np.float32),
    )

    gallery.add_student(
        "STU002",
        np.array([0.0, 1.0, 0.0], dtype=np.float32),
    )

    matcher = FaceMatcher(threshold=0.75)

    result = matcher.match(
        np.array([0.9, 0.1, 0.0], dtype=np.float32),
        gallery,
    )

    assert result.is_match is True
    assert result.student_id == "STU001"


def test_matcher_returns_unknown_for_low_similarity():
    gallery = StudentGallery()

    gallery.add_student(
        "STU001",
        np.array([1.0, 0.0, 0.0], dtype=np.float32),
    )

    matcher = FaceMatcher(threshold=0.95)

    result = matcher.match(
        np.array([0.0, 1.0, 0.0], dtype=np.float32),
        gallery,
    )

    assert result.is_match is False
    assert result.student_id is None


def test_empty_gallery_returns_unknown():
    gallery = StudentGallery()
    matcher = FaceMatcher()

    result = matcher.match(
        np.array([1.0, 0.0, 0.0], dtype=np.float32),
        gallery,
    )

    assert result.is_match is False
    assert result.student_id is None