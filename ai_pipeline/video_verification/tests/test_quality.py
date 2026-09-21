import cv2
import numpy as np
import pytest

from video_verification.detection.face_detector import FaceDetection
from video_verification.quality.quality import FaceQualityAssessor


def create_detection(
    x=20,
    y=20,
    width=100,
    height=100,
):
    return FaceDetection(
        x=x,
        y=y,
        width=width,
        height=height,
    )


def create_image(value=128, size=200):
    return np.full(
        (size, size, 3),
        value,
        dtype=np.uint8,
    )


def test_good_quality_face():
    assessor = FaceQualityAssessor(
        min_face_size=50,
        min_sharpness=0.0,
    )

    image = create_image()

    # Add edges to make the crop non-uniform.
    cv2.rectangle(
        image,
        (40, 40),
        (100, 100),
        (255, 255, 255),
        2,
    )

    result = assessor.assess(
        image,
        create_detection(),
    )

    assert result.is_acceptable is True
    assert result.face_width == 100
    assert result.face_height == 100
    assert result.reasons == []


def test_small_face_is_rejected():
    assessor = FaceQualityAssessor(min_face_size=50)

    image = create_image()

    result = assessor.assess(
        image,
        create_detection(width=30, height=30),
    )

    assert result.is_acceptable is False
    assert "face_too_small" in result.reasons


def test_dark_face_is_rejected():
    assessor = FaceQualityAssessor(min_sharpness=0.0)

    image = create_image(value=10)

    result = assessor.assess(
        image,
        create_detection(),
    )

    assert result.is_acceptable is False
    assert "face_too_dark" in result.reasons


def test_bright_face_is_rejected():
    assessor = FaceQualityAssessor(min_sharpness=0.0)

    image = create_image(value=250)

    result = assessor.assess(
        image,
        create_detection(),
    )

    assert result.is_acceptable is False
    assert "face_overexposed" in result.reasons


def test_invalid_image_raises_error():
    assessor = FaceQualityAssessor()

    detection = create_detection()

    with pytest.raises(ValueError):
        assessor.assess(np.array([]), detection)