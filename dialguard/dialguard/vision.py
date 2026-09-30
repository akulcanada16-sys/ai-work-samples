"""Substantive OpenCV 5 workload; deliberately limited to calibrated frontal dials."""
import os
os.environ.setdefault("OPENCV_IO_MAX_IMAGE_PIXELS", "4000000")
import base64
import math
import time
from dataclasses import dataclass

import cv2
import numpy as np

cv2.setNumThreads(1)
if cv2.__version__.split('.')[0] != '5':
    raise RuntimeError("DialGuard requires OpenCV 5; install the pinned requirements")


@dataclass(frozen=True)
class Calibration:
    cx: float = .5
    cy: float = .5
    radius: float = .4
    start_deg: float = 135
    sweep_deg: float = 270
    minimum: float = 0
    maximum: float = 100
    unit: str = "units"
    review_above: float | None = None

    @classmethod
    def parse(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Calibration must be an object")
        unknown = set(data) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError("Unknown calibration fields")
        args = {}
        for key, val in data.items():
            if key == 'unit':
                if not isinstance(val, str) or len(val) > 24:
                    raise ValueError("Unit must contain at most 24 characters")
                args[key] = val
            elif key == 'review_above' and val is None:
                args[key] = None
            else:
                if isinstance(val, bool):
                    raise ValueError("Calibration values must be numbers")
                args[key] = float(val)
                if not math.isfinite(args[key]):
                    raise ValueError("Calibration values must be finite")
        c = cls(**args)
        if not (0 < c.cx < 1 and 0 < c.cy < 1 and .08 <= c.radius <= .48):
            raise ValueError("Center must be inside image; radius must be 0.08–0.48 of its shorter side")
        if not (0 < c.sweep_deg <= 330 and c.maximum > c.minimum):
            raise ValueError("Use an increasing scale and a sweep between 0 and 330 degrees")
        if not 0 <= c.start_deg < 360:
            raise ValueError("Start angle must be 0–359.99 degrees")
        return c


def decode_image(text):
    if not isinstance(text, str) or len(text) > 2_100_000:
        raise ValueError("Image must be base64 PNG/JPEG, at most 1.5 MiB")
    try:
        raw = base64.b64decode(text, validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("Image is not valid base64") from exc
    if len(raw) > 1_572_864 or not (raw.startswith(b'\x89PNG\r\n\x1a\n') or raw.startswith(b'\xff\xd8')):
        raise ValueError("Only PNG/JPEG images up to 1.5 MiB are supported")
    try:
        frame = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    except cv2.error as exc:
        raise ValueError("Image could not be decoded or exceeds the pixel limit") from exc
    if frame is None or min(frame.shape[:2]) < 128 or frame.shape[0] * frame.shape[1] > 4_000_000:
        raise ValueError("Use an image at least 128 pixels per side and at most 4 megapixels")
    return frame, raw


def angle_distance(a, b):
    return abs((a - b + 180) % 360 - 180)


def _ray_scores(gray, center, radius, angles, threshold):
    # Remap an inner annulus to angle × radius. Rim ticks and hub are excluded.
    rad = np.linspace(.24 * radius, .72 * radius, 120, dtype=np.float32)
    theta = np.deg2rad(angles.astype(np.float32))[:, None]
    mx = (center[0] + np.cos(theta) * rad).astype(np.float32)
    my = (center[1] + np.sin(theta) * rad).astype(np.float32)
    samples = cv2.remap(gray, mx, my, cv2.INTER_LINEAR)
    background = float(np.percentile(samples, 80))
    dark = samples < min(180, background - threshold)
    # Require support in both halves so a short printed mark is less persuasive.
    support = dark.mean(axis=1)
    support *= np.minimum(dark[:, :60].mean(axis=1), dark[:, 60:].mean(axis=1))
    return support, background


def hough_baseline(gray, center, radius):
    """Independent simple baseline: longest center-crossing Hough line."""
    edges = cv2.Canny(gray, 60, 160)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 30,
                            minLineLength=int(.3 * radius), maxLineGap=8)
    candidates = []
    if lines is not None:
        # OpenCV 5 returns N×4 here; older bindings used N×1×4.
        for x1, y1, x2, y2 in lines.reshape(-1, 4):
            p1, p2 = np.array([x1, y1]), np.array([x2, y2])
            d1, d2 = np.linalg.norm(p1 - center), np.linalg.norm(p2 - center)
            near, far = (p1, p2) if d1 < d2 else (p2, p1)
            if np.linalg.norm(near - center) < .22 * radius and .35 * radius < np.linalg.norm(far - center) < .85 * radius:
                candidates.append((float(np.linalg.norm(far - near)), far))
    if not candidates:
        return None
    tip = max(candidates, key=lambda x: x[0])[1]
    return float(np.degrees(np.arctan2(tip[1] - center[1], tip[0] - center[0])) % 360)


def inspect(frame, calibration):
    started = time.perf_counter()
    h, w = frame.shape[:2]
    c = calibration
    center = np.array([c.cx * w, c.cy * h])
    radius = c.radius * min(h, w)
    if not (radius <= center[0] <= w - radius and radius <= center[1] <= h - radius):
        raise ValueError("The calibrated dial circle must fit completely inside the image")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    crop = gray[int(center[1]-radius):int(center[1]+radius), int(center[0]-radius):int(center[0]+radius)]
    sharpness = float(cv2.Laplacian(crop, cv2.CV_64F).var())
    exposure = float(crop.mean())
    trace = [{"tool": "quality", "sharpness": round(sharpness, 2), "mean_brightness": round(exposure, 2)}]
    reasons = []
    reading, chosen = None, None
    support, margin = 0., 0.
    baseline = None
    if sharpness < 35:
        reasons.append("Image is too soft: hold the camera steady and focus on the dial.")
    if exposure < 45:
        reasons.append("Image is too dark: add even light without flash glare.")
    if not reasons:
        baseline = hough_baseline(gray, center, radius)
        trace.append({"tool": "hough_baseline", "angle_deg": baseline})
        angles = np.arange(0., 360., 1.)
        scores, _ = _ray_scores(gray, center, radius, angles, 40)
        i = int(scores.argmax())
        candidate = float(angles[i])
        outside = np.array([angle_distance(a, candidate) > 12 for a in angles])
        support = float(scores[i])
        margin = support - float(scores[outside].max())
        trace.append({"tool": "polar_scan", "angle_deg": candidate,
                      "support": round(support, 4), "peak_margin": round(margin, 4)})
        if support < .55:
            reasons.append("No supported needle: check the center/radius and remove reflections.")
        elif margin < .15:
            reasons.append("Competing needle directions: take a clearer, straight-on photo.")
        else:
            # Visual evidence selects the next tool's search window; independently
            # test contrast settings, then refuse unstable readings rather than guess.
            fine = np.arange(candidate - 3, candidate + 3.01, .1)
            refined = []
            for threshold in (30, 50):
                fs, _ = _ray_scores(gray, center, radius, fine, threshold)
                refined.append(float(fine[int(fs.argmax())] % 360))
            trace.append({"tool": "verify_candidate", "window_center_deg": candidate,
                          "angles_deg": refined, "contrast_thresholds": [30, 50]})
            if angle_distance(*refined) > 2:
                reasons.append("Needle estimate changes with contrast: reduce glare and recapture.")
            else:
                chosen = float((candidate + np.mean([(a - candidate + 180) % 360 - 180 for a in refined])) % 360)
                delta = (chosen - c.start_deg) % 360
                if delta > c.sweep_deg + .75:
                    reasons.append("Needle is outside the configured scale: verify calibration.")
                else:
                    reading = c.minimum + min(delta, c.sweep_deg) / c.sweep_deg * (c.maximum - c.minimum)
    status = "RETAKE" if reasons else "READ"
    action = "request_new_photo" if reasons else "record_reading"
    if reading is not None and c.review_above is not None and reading >= c.review_above:
        status, action = "REVIEW", "request_human_review"
        reasons.append("Reading is at or above your review threshold. Confirm it independently.")
    trace.append({"tool": "decision", "status": status, "action": action})
    annotated = frame.copy()
    cc = tuple(center.astype(int))
    cv2.circle(annotated, cc, int(radius), (255, 180, 30), 2)
    if chosen is not None:
        tip = tuple((center + .75 * radius * np.array([math.cos(math.radians(chosen)), math.sin(math.radians(chosen))])).astype(int))
        cv2.line(annotated, cc, tip, (50, 180, 50) if reading is not None else (30, 30, 220), 3)
    cv2.putText(annotated, status, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, .8, (40, 100, 230), 2)
    if max(h, w) > 1000:
        annotated = cv2.resize(annotated, None, fx=1000/max(h,w), fy=1000/max(h,w))
    ok, encoded = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
    if not ok:
        raise RuntimeError("Could not encode evidence image")
    return {"status": status, "action": action, "reading": None if reading is None else round(reading, 3),
            "unit": c.unit, "angle_deg": chosen, "reasons": reasons, "trace": trace,
            "evidence_score": round(support, 4), "peak_margin": round(margin, 4),
            "baseline_angle_deg": baseline, "opencv_version": cv2.__version__,
            "latency_ms": round((time.perf_counter()-started)*1000, 2),
            "annotated_image": base64.b64encode(encoded).decode('ascii')}
