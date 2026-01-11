import cv2
from typing import Dict, Any, List, Tuple
from .config import (
    Thresholds, Weights,
    DEFAULT_DECISION_SCORE_THRESHOLD, CRITICAL_LABELS
)
from .metrics import (
    metric_blur, metric_brightness, metric_contrast,
    metric_exposure, metric_noise
)

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))

def score_from_metrics(
    blur_v: float, bright_m: float, contrast_s: float,
    low_sat: float, high_sat: float, noise_hf: float,
    thr: Thresholds, w: Weights
) -> Tuple[int, Dict[str, float]]:

    blur_good = clamp01(blur_v / thr.blur)

    if bright_m < thr.dark:
        bright_good = clamp01(bright_m / thr.dark)
    elif bright_m > thr.bright:
        bright_good = clamp01((255.0 - bright_m) / (255.0 - thr.bright))
    else:
        bright_good = 1.0

    contrast_good = clamp01(contrast_s / thr.low_contrast)

    exposure_bad = clamp01((low_sat / thr.sat_low) * 0.5 + (high_sat / thr.sat_high) * 0.5)
    exposure_good = 1.0 - exposure_bad

    noise_good = 1.0 - clamp01(noise_hf / thr.noise - 1.0)
    noise_good = clamp01(noise_good)

    total = (
        w.blur * blur_good +
        w.brightness * bright_good +
        w.contrast * contrast_good +
        w.exposure * exposure_good +
        w.noise * noise_good
    )

    score = int(round(total * 100))
    parts = {
        "blur_good": blur_good,
        "brightness_good": bright_good,
        "contrast_good": contrast_good,
        "exposure_good": exposure_good,
        "noise_good": noise_good
    }
    return score, parts

def labels_from_metrics(
    blur_v: float, bright_m: float, contrast_s: float,
    low_sat: float, high_sat: float, noise_hf: float,
    thr: Thresholds
) -> List[str]:
    labels: List[str] = []
    if blur_v < thr.blur:
        labels.append("blurred")
    if bright_m < thr.dark:
        labels.append("dark")
    if bright_m > thr.bright:
        labels.append("too_bright")
    if contrast_s < thr.low_contrast:
        labels.append("low_contrast")
    if high_sat > thr.sat_high:
        labels.append("overexposed")
    if low_sat > thr.sat_low:
        labels.append("underexposed")
    if noise_hf > thr.noise:
        labels.append("noisy")
    return labels

def decide(score: int, labels: List[str], min_score: int = DEFAULT_DECISION_SCORE_THRESHOLD) -> str:
    if score < min_score:
        return "reject"
    if any(l in CRITICAL_LABELS for l in labels):
        return "reject"
    return "accept"

def inspect_one(path: str, thr: Thresholds, w: Weights) -> Dict[str, Any] | None:
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur_v = metric_blur(gray)
    bright_m = metric_brightness(gray)
    contrast_s = metric_contrast(gray)
    low_sat, high_sat = metric_exposure(gray)
    noise_hf = metric_noise(gray)

    score, parts = score_from_metrics(blur_v, bright_m, contrast_s, low_sat, high_sat, noise_hf, thr, w)
    labels = labels_from_metrics(blur_v, bright_m, contrast_s, low_sat, high_sat, noise_hf, thr)
    decision = decide(score, labels)

    return {
        "path": path,
        "blur_lap_var": blur_v,
        "brightness_mean": bright_m,
        "contrast_rms": contrast_s,
        "sat_low_ratio": low_sat,
        "sat_high_ratio": high_sat,
        "noise_hf": noise_hf,
        "quality_score": score,
        "labels": labels,
        "decision": decision,
        "score_parts": parts
    }
