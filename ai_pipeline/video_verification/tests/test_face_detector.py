import numpy as np
import pytest

from video_verification.detection.face_detector import FaceDetector


def test_face_detector_initializes():
    detector = FaceDetector()

    assert detector.detector is not None


def test_empty_image_raises_error():
    detector = FaceDetector()

    with pytest.raises(ValueError):
        detector.detect(np.array([]))


def test_blank_image_returns_list():
    detector = FaceDetector()

    image = np.zeros((200, 200, 3), dtype=np.uint8)

    detections = detector.detect(image)

    assert isinstance(detections, list)