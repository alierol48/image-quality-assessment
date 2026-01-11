import argparse
import os
from pathlib import Path

from .config import DEFAULT_THRESHOLDS, DEFAULT_WEIGHTS
from .io_utils import list_images, save_csv, save_jsonl
from .inspector import inspect_one

def parse_args():
    ap = argparse.ArgumentParser(description="Image Quality Assessment (rule-based) - quality gate for CV pipelines")
    ap.add_argument("--input", "-i", required=True, help="Input folder containing images")
    ap.add_argument("--out", "-o", default="quality_out", help="Output folder (csv/jsonl will be saved here)")
    return ap.parse_args()

def main():
    args = parse_args()

    input_dir = args.input
    out_dir = args.out

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    images = list_images(input_dir)
    print(f"Found {len(images)} images in: {input_dir}")

    results = []
    for p in images:
        r = inspect_one(p, DEFAULT_THRESHOLDS, DEFAULT_WEIGHTS)
        if r is not None:
            results.append(r)

    csv_path = os.path.join(out_dir, "results.csv")
    jsonl_path = os.path.join(out_dir, "results.jsonl")

    save_csv(results, csv_path)
    save_jsonl(results, jsonl_path)

    acc = sum(1 for r in results if r["decision"] == "accept")
    rej = sum(1 for r in results if r["decision"] == "reject")

    print(f"Processed: {len(results)}")
    print(f"ACCEPT: {acc} | REJECT: {rej}")
    print("Saved outputs:")
    print(" -", csv_path)
    print(" -", jsonl_path)

if __name__ == "__main__":
    main()
