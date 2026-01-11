import cv2
import numpy as np
from typing import Tuple

def metric_blur(gray) -> float:
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())

def metric_brightness(gray) -> float:
    return float(gray.mean())

def metric_contrast(gray) -> float:
    return float(gray.std())

def metric_exposure(gray) -> Tuple[float, float]:
    low_ratio = float((gray <= 5).mean())
    high_ratio = float((gray >= 250).mean())
    return low_ratio, high_ratio

def metric_noise(gray) -> float:
    lap = cv2.Laplacian(gray, cv2.CV_32F)
    hf = float(np.mean(np.abs(lap)) / 255.0)  # normalize
    return hf
