import numpy as np
import pytest

from video_verification.detection.face_detector import FaceDetection
from video_verification.recognition.face_cropper import FaceCropper


def test_face_cropper_returns_correct_crop():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    detection = FaceDetection(
        x=20,
        y=20,
        width=30,
        height=30,
    )

    cropper = FaceCropper(padding_ratio=0.0)

    result = cropper.crop(image, detection)

    assert result.image.shape == (30, 30, 3)
    assert result.box == (20, 20, 30, 30)


def test_face_cropper_applies_padding():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    detection = FaceDetection(
        x=30,
        y=30,
        width=20,
        height=20,
    )

    cropper = FaceCropper(padding_ratio=0.5)

    result = cropper.crop(image, detection)

    assert result.box == (20, 20, 40, 40)
    assert result.image.shape == (40, 40, 3)


def test_face_cropper_clamps_to_image_boundaries():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    detection = FaceDetection(
        x=0,
        y=0,
        width=20,
        height=20,
    )

    cropper = FaceCropper(padding_ratio=0.5)

    result = cropper.crop(image, detection)

    assert result.x == 0
    assert result.y == 0
    assert result.width == 30
    assert result.height == 30


def test_face_cropper_rejects_empty_image():
    cropper = FaceCropper()

    detection = FaceDetection(
        x=10,
        y=10,
        width=20,
        height=20,
    )

    with pytest.raises(ValueError):
        cropper.crop(np.array([]), detection)


def test_face_cropper_rejects_invalid_box():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    detection = FaceDetection(
        x=10,
        y=10,
        width=0,
        height=20,
    )

    cropper = FaceCropper()

    with pytest.raises(ValueError):
        cropper.crop(image, detection)


def test_face_cropper_rejects_negative_padding():
    with pytest.raises(ValueError):
        FaceCropper(padding_ratio=-0.1)