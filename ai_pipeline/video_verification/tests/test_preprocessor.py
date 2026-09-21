import numpy as np
import pytest

from video_verification.recognition.preprocessor import FacePreprocessor


def test_preprocessor_resizes_image():
    image = np.zeros((80, 100, 3), dtype=np.uint8)

    preprocessor = FacePreprocessor(target_size=(112, 112))
    result = preprocessor.process(image)

    assert result.image.shape == (112, 112, 3)
    assert result.processed_shape == (112, 112, 3)


def test_preprocessor_normalizes_pixels():
    image = np.full((50, 50, 3), 255, dtype=np.uint8)

    preprocessor = FacePreprocessor(normalize=True)
    result = preprocessor.process(image)

    assert result.image.dtype == np.float32
    assert np.allclose(result.image, 1.0)


def test_preprocessor_preserves_pixel_scale_when_disabled():
    image = np.full((50, 50, 3), 128, dtype=np.uint8)

    preprocessor = FacePreprocessor(normalize=False)
    result = preprocessor.process(image)

    assert result.image.dtype == np.float32
    assert np.allclose(result.image, 128.0)


def test_preprocessor_converts_bgr_to_rgb():
    image = np.zeros((20, 20, 3), dtype=np.uint8)

    # BGR pixel: Blue=10, Green=20, Red=30
    image[:, :] = [10, 20, 30]

    preprocessor = FacePreprocessor(normalize=False)
    result = preprocessor.process(image)

    # RGB pixel should be: Red=30, Green=20, Blue=10
    assert np.array_equal(
        result.image[0, 0],
        np.array([30.0, 20.0, 10.0], dtype=np.float32),
    )


def test_preprocessor_rejects_empty_image():
    preprocessor = FacePreprocessor()

    with pytest.raises(ValueError):
        preprocessor.process(np.array([]))


def test_preprocessor_rejects_grayscale_image():
    image = np.zeros((100, 100), dtype=np.uint8)

    preprocessor = FacePreprocessor()

    with pytest.raises(ValueError):
        preprocessor.process(image)


def test_preprocessor_rejects_invalid_target_size():
    with pytest.raises(ValueError):
        FacePreprocessor(target_size=(0, 112))

    with pytest.raises(ValueError):
        FacePreprocessor(target_size=(112, -1))