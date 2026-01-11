import json
from pathlib import Path
from typing import List, Dict, Any, Iterable
from .config import SUPPORTED_EXTS

def list_images(folder: str) -> List[str]:
    folder_path = Path(folder)
    out: List[str] = []
    for p in folder_path.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            out.append(str(p))
    return sorted(out)

def save_jsonl(rows: Iterable[Dict[str, Any]], out_path: str) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def save_csv(rows: Iterable[Dict[str, Any]], out_path: str) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "path","quality_score","decision","labels",
        "blur_lap_var","brightness_mean","contrast_rms",
        "sat_low_ratio","sat_high_ratio","noise_hf"
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            row = [
                str(r["path"]).replace(",", "_"),
                str(r["quality_score"]),
                r["decision"],
                "|".join(r["labels"]),
                f"{r['blur_lap_var']:.3f}",
                f"{r['brightness_mean']:.3f}",
                f"{r['contrast_rms']:.3f}",
                f"{r['sat_low_ratio']:.5f}",
                f"{r['sat_high_ratio']:.5f}",
                f"{r['noise_hf']:.5f}",
            ]
            f.write(",".join(row) + "\n")
