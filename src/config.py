from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Thresholds:
    blur: float = 120.0
    dark: float = 70.0
    bright: float = 185.0
    low_contrast: float = 35.0
    sat_high: float = 0.08
    sat_low: float = 0.08
    noise: float = 0.12

@dataclass(frozen=True)
class Weights:
    blur: float = 0.30
    exposure: float = 0.25
    contrast: float = 0.20
    noise: float = 0.15
    brightness: float = 0.10

DEFAULT_THRESHOLDS = Thresholds()
DEFAULT_WEIGHTS = Weights()

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

DEFAULT_DECISION_SCORE_THRESHOLD = 60  # score < 60 => reject
CRITICAL_LABELS = {"blurred", "overexposed", "underexposed"}
