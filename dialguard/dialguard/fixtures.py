"""Procedural images, not photos or field-validation evidence."""
import math
import cv2
import numpy as np


def make_dial(value=50., seed=0, condition="clean", size=512):
    rng = np.random.default_rng(seed)
    frame = np.full((size, size, 3), 222, np.uint8)
    center, radius = (size//2, size//2), int(.4 * size)
    cv2.circle(frame, center, radius, (245, 245, 245), -1)
    cv2.circle(frame, center, radius, (65, 65, 65), 4)
    for idx in range(21):
        a = math.radians(135 + idx/20 * 270)
        start = tuple(int(center[j] + .82 * radius * (math.cos(a), math.sin(a))[j]) for j in range(2))
        end = tuple(int(center[j] + .95 * radius * (math.cos(a), math.sin(a))[j]) for j in range(2))
        cv2.line(frame, start, end, (30, 30, 30), 3)
        if idx % 5 == 0:
            pos = tuple(int(center[j] + .78 * radius * (math.cos(a), math.sin(a))[j]) for j in range(2))
            cv2.putText(frame, str(idx*5), pos, cv2.FONT_HERSHEY_SIMPLEX, .35, (40, 40, 40), 1)
    angle = math.radians((135 + value/100 * 270) % 360)
    tip = (int(center[0] + .72*radius*math.cos(angle)), int(center[1] + .72*radius*math.sin(angle)))
    if condition != "missing":
        cv2.line(frame, center, tip, (25,25,25), int(rng.integers(5, 9)))
    if condition == "ambiguous":
        other = angle + math.pi
        tip2 = (int(center[0]+.72*radius*math.cos(other)), int(center[1]+.72*radius*math.sin(other)))
        cv2.line(frame, center, tip2, (25,25,25), 7)
    cv2.circle(frame, center, int(.08*radius), (25,25,25), -1)
    if condition == "noise":
        noise = rng.normal(0, 10, frame.shape)
        frame = np.clip(frame.astype(float)+noise, 0,255).astype(np.uint8)
    if condition == "dim":
        frame = (frame.astype(float)*.12).astype(np.uint8)
    if condition == "blur":
        frame = cv2.GaussianBlur(frame, (41,41), 12)
    return frame
