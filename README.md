# Image Quality Assessment

Multi-metric, explainable, rule-based image quality scoring system
designed as a pre-filter for computer vision models.

## Features
- Blur detection
- Noise estimation
- Illumination and contrast analysis
- Accept / reject decision

## Project Structure (Where is what?)

```text
image-quality-assessment/
├─ src/                      # Core system
│  ├─ main.py                # Entry point: processes a folder, writes outputs
│  ├─ inspector.py           # "Brain": metrics → score → labels → accept/reject
│  ├─ metrics.py             # Blur / noise / brightness / contrast / exposure metrics
│  ├─ io_utils.py            # list_images, save_csv, save_jsonl helpers
│  ├─ config.py              # Thresholds + weights (system behavior tuning)
│  └─ tools/
│     ├─ summary.py          # Reads results.csv, prints summary stats
│     └─ plot_scores.py      # Generates score distribution plots
│
├─ quality_out/              # Outputs (evidence)
│  ├─ results.csv            # Table: score + labels + decision per image
│  └─ results.jsonl          # Log: per-image detailed JSON records
│
├─ assests/                  # Visual evidence for report (plots + examples)
│  ├─ hist_all.png
│  ├─ hist_accept_reject.png
│  ├─ scores_sorted_curve.png
│  └─ model sonuçlarımız/
│     ├─ accept/             # High-score examples
│     └─ reject/             # Low-score examples
│
├─ doc/
│  └─ RESULTS_TR.md          # Turkish results summary
│
├─ requirements.txt
└─ README.md

