from __future__ import annotations

from dataclasses import dataclass

from ..detection.face_detector import FaceDetection


@dataclass
class Track:
    track_id: int
    detection: FaceDetection
    missed_frames: int = 0
    age: int = 1


def calculate_iou(
    box_a: tuple[int, int, int, int],
    box_b: tuple[int, int, int, int],
) -> float:
    """
    Calculate Intersection over Union between two bounding boxes.

    Box format: (x, y, width, height)
    """

    ax, ay, aw, ah = box_a
    bx, by, bw, bh = box_b

    ax2 = ax + aw
    ay2 = ay + ah

    bx2 = bx + bw
    by2 = by + bh

    intersection_x1 = max(ax, bx)
    intersection_y1 = max(ay, by)
    intersection_x2 = min(ax2, bx2)
    intersection_y2 = min(ay2, by2)

    intersection_width = max(0, intersection_x2 - intersection_x1)
    intersection_height = max(0, intersection_y2 - intersection_y1)

    intersection_area = intersection_width * intersection_height

    area_a = aw * ah
    area_b = bw * bh

    union_area = area_a + area_b - intersection_area

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


class IoUTracker:
    def __init__(
        self,
        iou_threshold: float = 0.3,
        max_missed_frames: int = 5,
    ) -> None:
        if not 0.0 <= iou_threshold <= 1.0:
            raise ValueError("iou_threshold must be between 0 and 1")

        if max_missed_frames < 0:
            raise ValueError("max_missed_frames cannot be negative")

        self.iou_threshold = iou_threshold
        self.max_missed_frames = max_missed_frames
        self.next_track_id = 1
        self.tracks: dict[int, Track] = {}

    def update(self, detections: list[FaceDetection]) -> list[Track]:
        """
        Update tracks using detections from the current frame.
        """

        if not detections:
            self._handle_missing_detections()
            return list(self.tracks.values())

        unmatched_detections = set(range(len(detections)))
        matched_track_ids: set[int] = set()

        # Match existing tracks with the best available detection.
        for track_id, track in list(self.tracks.items()):
            best_index = None
            best_iou = 0.0

            for index in unmatched_detections:
                current_detection = detections[index]

                iou = calculate_iou(
                    track.detection.box,
                    current_detection.box,
                )

                if iou > best_iou:
                    best_iou = iou
                    best_index = index

            if best_index is not None and best_iou >= self.iou_threshold:
                track.detection = detections[best_index]
                track.missed_frames = 0
                track.age += 1

                unmatched_detections.remove(best_index)
                matched_track_ids.add(track_id)

        # Increase missed-frame count for unmatched tracks.
        for track_id, track in list(self.tracks.items()):
            if track_id not in matched_track_ids:
                track.missed_frames += 1

        # Remove tracks missing for too long.
        expired_track_ids = [
            track_id
            for track_id, track in self.tracks.items()
            if track.missed_frames > self.max_missed_frames
        ]

        for track_id in expired_track_ids:
            del self.tracks[track_id]

        # Create new tracks for unmatched detections.
        for index in unmatched_detections:
            new_track = Track(
                track_id=self.next_track_id,
                detection=detections[index],
            )

            self.tracks[self.next_track_id] = new_track
            self.next_track_id += 1

        return list(self.tracks.values())

    def _handle_missing_detections(self) -> None:
        for track in self.tracks.values():
            track.missed_frames += 1

        expired_track_ids = [
            track_id
            for track_id, track in self.tracks.items()
            if track.missed_frames > self.max_missed_frames
        ]

        for track_id in expired_track_ids:
            del self.tracks[track_id]

    def reset(self) -> None:
        self.next_track_id = 1
        self.tracks.clear()