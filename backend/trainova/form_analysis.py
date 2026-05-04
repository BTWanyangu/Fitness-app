"""Pose-analysis utilities for Trainova.

This module is deliberately defensive: the API must remain usable even when a
user uploads an unclear photo/video or when the MediaPipe model is missing. When
`pose_landmarker.task` is present, the engine extracts landmarks, evaluates
configured exercise angle standards, optionally compares against admin-approved
reference media, and returns frontend-friendly overlay data.
"""
from __future__ import annotations

import math
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from django.conf import settings


# MediaPipe Pose landmark names. These strings are what admins should use when
# configuring ExerciseAngleStandard.joint_a / joint_b / joint_c.
MP_NAMES = {
    0: "nose", 1: "left_eye_inner", 2: "left_eye", 3: "left_eye_outer",
    4: "right_eye_inner", 5: "right_eye", 6: "right_eye_outer", 7: "left_ear",
    8: "right_ear", 9: "mouth_left", 10: "mouth_right", 11: "left_shoulder",
    12: "right_shoulder", 13: "left_elbow", 14: "right_elbow", 15: "left_wrist",
    16: "right_wrist", 17: "left_pinky", 18: "right_pinky", 19: "left_index",
    20: "right_index", 21: "left_thumb", 22: "right_thumb", 23: "left_hip",
    24: "right_hip", 25: "left_knee", 26: "right_knee", 27: "left_ankle",
    28: "right_ankle", 29: "left_heel", 30: "right_heel", 31: "left_foot_index",
    32: "right_foot_index",
}

LANDMARK_CONNECTIONS = [
    ("left_shoulder", "right_shoulder"), ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"), ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"), ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"), ("left_hip", "right_hip"),
    ("left_hip", "left_knee"), ("left_knee", "left_ankle"),
    ("right_hip", "right_knee"), ("right_knee", "right_ankle"),
    ("left_ankle", "left_heel"), ("left_heel", "left_foot_index"),
    ("right_ankle", "right_heel"), ("right_heel", "right_foot_index"),
]


def model_status() -> dict:
    """Return a small health payload for the pose engine."""
    model_path = str(getattr(settings, "MEDIAPIPE_POSE_MODEL_PATH", ""))
    return {
        "configured_path": model_path,
        "exists": bool(model_path and os.path.exists(model_path)),
        "expected_filename": "pose_landmarker.task",
    }


def _fallback_analysis(exercise_name: str = "") -> dict:
    return {
        "score": 72,
        "summary": (
            "Technique review completed with safe fallback feedback. "
            "Pose landmarks were not available, so no joint-angle scoring was applied."
        ),
        "feedback": [
            "Keep your full body visible in the frame from start to finish.",
            "Use a stable camera position with good lighting and minimal background clutter.",
            "Record from the recommended side or front angle for the selected exercise.",
            f"For {exercise_name or 'this movement'}, compare yourself against an admin-approved reference video before increasing load.",
        ],
        "detected_landmarks": {},
        "reference_landmarks": {},
        "angle_results": [],
        "overlay_coordinates": [],
        "reference_overlay_coordinates": [],
        "engine": "fallback",
    }


def _point(landmark: dict) -> Tuple[float, float]:
    return float(landmark.get("x", 0)), float(landmark.get("y", 0))


def _angle(a: dict, b: dict, c: dict) -> float:
    ax, ay = _point(a)
    bx, by = _point(b)
    cx, cy = _point(c)
    radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
    degrees = abs(math.degrees(radians))
    if degrees > 180:
        degrees = 360 - degrees
    return round(degrees, 1)


def calculate_angle_from_landmarks(landmarks: Dict, joint_a: str, joint_b: str, joint_c: str) -> Optional[float]:
    if not all(k in landmarks for k in [joint_a, joint_b, joint_c]):
        return None
    return _angle(landmarks[joint_a], landmarks[joint_b], landmarks[joint_c])


@lru_cache(maxsize=1)
def _get_detector():
    model_path = str(getattr(settings, "MEDIAPIPE_POSE_MODEL_PATH", ""))
    if not model_path or not os.path.exists(model_path):
        return None

    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision

    options = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=model_path),
        running_mode=vision.RunningMode.IMAGE,
        num_poses=1,
    )
    return vision.PoseLandmarker.create_from_options(options)


def _read_representative_frame(file_path: str):
    import cv2

    suffix = Path(file_path).suffix.lower()
    if suffix in [".mp4", ".mov", ".avi", ".webm", ".mkv"]:
        cap = cv2.VideoCapture(file_path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 1)
        # Try middle frame first because it often captures the movement depth.
        frame_positions = [max(0, total // 2), max(0, total // 3), 0]
        frame = None
        for pos in frame_positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ok, candidate = cap.read()
            if ok and candidate is not None:
                frame = candidate
                break
        cap.release()
        return frame
    return cv2.imread(file_path)


def extract_pose_landmarks(file_path: str) -> Tuple[Dict, List[dict]]:
    """Extract normalized landmarks and overlay line segments from an image/video."""
    try:
        detector = _get_detector()
        if detector is None:
            return {}, []

        import cv2
        import mediapipe as mp

        frame = _read_representative_frame(file_path)
        if frame is None:
            return {}, []

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)
        if not result.pose_landmarks:
            return {}, []

        pose = result.pose_landmarks[0]
        landmarks = {}
        for idx, name in MP_NAMES.items():
            if idx >= len(pose):
                continue
            lm = pose[idx]
            landmarks[name] = {
                "x": round(float(lm.x), 4),
                "y": round(float(lm.y), 4),
                "z": round(float(lm.z), 4),
                "visibility": round(float(lm.visibility), 4),
            }

        overlay = [
            {"from": a, "to": b, "points": [landmarks.get(a), landmarks.get(b)]}
            for a, b in LANDMARK_CONNECTIONS
            if a in landmarks and b in landmarks
        ]
        return landmarks, overlay
    except Exception as exc:
        # In production this should be logged to Sentry or a central logger. We
        # return fallback output so user uploads do not crash the app.
        print(f"Pose extraction failed: {exc}")
        return {}, []


def score_against_standards(landmarks: Dict, standards: Iterable) -> Tuple[float, List[str], List[dict]]:
    standards = list(standards or [])
    if not landmarks or not standards:
        return 72, ["Angle standards are not configured yet for this exercise."], []

    total_weight = 0.0
    penalties = 0.0
    feedback: List[str] = []
    results: List[dict] = []

    for standard in standards:
        measured = calculate_angle_from_landmarks(landmarks, standard.joint_a, standard.joint_b, standard.joint_c)
        if measured is None:
            feedback.append(f"{standard.name}: not enough visible joints to evaluate this checkpoint.")
            continue

        low, high = float(standard.min_degrees), float(standard.max_degrees)
        deviation = 0.0
        status = "pass"
        if measured < low:
            deviation = low - measured
            status = "low"
            feedback.append(standard.feedback_when_low or f"{standard.name}: increase the angle slightly.")
        elif measured > high:
            deviation = measured - high
            status = "high"
            feedback.append(standard.feedback_when_high or f"{standard.name}: reduce the angle slightly.")

        weight = float(standard.weight or 1.0)
        total_weight += weight
        penalties += min(45, deviation) * weight
        results.append({
            "name": standard.name,
            "joint_a": standard.joint_a,
            "joint_b": standard.joint_b,
            "joint_c": standard.joint_c,
            "measured": measured,
            "expected_min": low,
            "expected_max": high,
            "deviation": round(deviation, 2),
            "status": status,
        })

    if not results:
        return 72, ["Could not match enough visible joints. Retake with full body visible."], []

    score = max(0, min(100, 100 - (penalties / max(total_weight, 1))))
    if not feedback:
        feedback.append("Great control. Your visible joint angles are within the configured safe range.")
    return round(score, 1), feedback[:8], results


def compare_to_reference(user_landmarks: Dict, reference_landmarks: Dict, standards: Iterable) -> List[dict]:
    comparisons: List[dict] = []
    if not user_landmarks or not reference_landmarks:
        return comparisons
    for standard in standards or []:
        user_angle = calculate_angle_from_landmarks(user_landmarks, standard.joint_a, standard.joint_b, standard.joint_c)
        reference_angle = calculate_angle_from_landmarks(reference_landmarks, standard.joint_a, standard.joint_b, standard.joint_c)
        if user_angle is None or reference_angle is None:
            continue
        comparisons.append({
            "name": standard.name,
            "user_angle": user_angle,
            "reference_angle": reference_angle,
            "difference": round(abs(user_angle - reference_angle), 1),
        })
    return comparisons


def analyze_reference_media(file_path: str) -> dict:
    landmarks, overlay = extract_pose_landmarks(file_path)
    return {"landmarks": landmarks, "overlay": overlay}


def analyze_uploaded_form(file_path: str, exercise=None, reference=None) -> dict:
    exercise_name = getattr(exercise, "name", "") if exercise else ""
    user_landmarks, overlay = extract_pose_landmarks(file_path)
    if not user_landmarks:
        return _fallback_analysis(exercise_name)

    standards = list(exercise.angle_standards.all()) if exercise else []
    score, feedback, angle_results = score_against_standards(user_landmarks, standards)

    reference_landmarks = getattr(reference, "landmark_data", {}) or {}
    reference_overlay = getattr(reference, "overlay_data", []) or []
    reference_comparison = compare_to_reference(user_landmarks, reference_landmarks, standards)

    if reference_landmarks and reference_comparison:
        average_diff = sum(item["difference"] for item in reference_comparison) / max(len(reference_comparison), 1)
        # Blend configured angle score with similarity-to-reference score.
        reference_score = max(0, min(100, 100 - average_diff))
        score = round((score * 0.75) + (reference_score * 0.25), 1)

    summary = (
        f"Pose landmarks detected for {exercise_name or 'the uploaded movement'}. "
        "Score is based on configured joint-angle standards"
        + (" and comparison with admin-approved reference media." if reference_landmarks else ".")
    )

    return {
        "score": score,
        "summary": summary,
        "feedback": feedback,
        "detected_landmarks": user_landmarks,
        "reference_landmarks": reference_landmarks,
        "angle_results": angle_results,
        "reference_comparison": reference_comparison,
        "overlay_coordinates": overlay,
        "reference_overlay_coordinates": reference_overlay,
        "engine": "mediapipe_pose_landmarker",
    }
