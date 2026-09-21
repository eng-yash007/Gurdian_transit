import numpy as np

from video_verification.video.frame_selector import FrameSelector
from video_verification.video.frame_types import FramePacket


def create_packet(frame_id: int, value: int) -> FramePacket:
    image = np.full(
        (100, 100, 3),
        value,
        dtype=np.uint8,
    )

    return FramePacket(
        frame_id=frame_id,
        timestamp_ms=frame_id * 100.0,
        image=image,
        width=100,
        height=100,
        source_fps=10.0,
    )


def test_first_frame_is_processed():
    selector = FrameSelector(difference_threshold=5.0)

    packet = create_packet(0, 100)

    assert selector.should_process(packet) is True


def test_similar_frame_is_skipped():
    selector = FrameSelector(difference_threshold=5.0)

    first = create_packet(0, 100)
    second = create_packet(1, 102)

    assert selector.should_process(first) is True
    assert selector.should_process(second) is False


def test_different_frame_is_processed():
    selector = FrameSelector(difference_threshold=5.0)

    first = create_packet(0, 100)
    second = create_packet(1, 120)

    assert selector.should_process(first) is True
    assert selector.should_process(second) is True


def test_reset_clears_previous_frame():
    selector = FrameSelector()

    first = create_packet(0, 100)

    assert selector.should_process(first) is True

    selector.reset()

    assert selector.previous_gray is None