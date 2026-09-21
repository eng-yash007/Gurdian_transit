from video_verification.detection.face_detector import FaceDetection
from video_verification.tracking.tracker import (
    IoUTracker,
    calculate_iou,
)


def create_detection(x, y, width=50, height=50):
    return FaceDetection(
        x=x,
        y=y,
        width=width,
        height=height,
    )


def test_iou_for_identical_boxes():
    box = (10, 10, 50, 50)

    assert calculate_iou(box, box) == 1.0


def test_iou_for_non_overlapping_boxes():
    box_a = (0, 0, 20, 20)
    box_b = (100, 100, 20, 20)

    assert calculate_iou(box_a, box_b) == 0.0


def test_tracker_creates_new_track():
    tracker = IoUTracker()

    tracks = tracker.update([
        create_detection(10, 10),
    ])

    assert len(tracks) == 1
    assert tracks[0].track_id == 1


def test_tracker_keeps_same_id():
    tracker = IoUTracker(iou_threshold=0.3)

    first_tracks = tracker.update([
        create_detection(10, 10),
    ])

    second_tracks = tracker.update([
        create_detection(12, 12),
    ])

    assert first_tracks[0].track_id == second_tracks[0].track_id
    assert second_tracks[0].age == 2


def test_tracker_creates_second_track():
    tracker = IoUTracker()

    tracker.update([
        create_detection(10, 10),
    ])

    tracks = tracker.update([
        create_detection(12, 12),
        create_detection(200, 200),
    ])

    assert len(tracks) == 2

    track_ids = {track.track_id for track in tracks}

    assert track_ids == {1, 2}


def test_track_expires_after_missed_frames():
    tracker = IoUTracker(max_missed_frames=2)

    tracker.update([
        create_detection(10, 10),
    ])

    tracker.update([])
    tracker.update([])

    assert len(tracker.tracks) == 1

    tracker.update([])

    assert len(tracker.tracks) == 0


def test_tracker_reset():
    tracker = IoUTracker()

    tracker.update([
        create_detection(10, 10),
    ])

    tracker.reset()

    assert len(tracker.tracks) == 0
    assert tracker.next_track_id == 1