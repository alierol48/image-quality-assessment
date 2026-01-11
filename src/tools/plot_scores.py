import csv
import os
import matplotlib.pyplot as plt

CSV_PATH = r"C:\Users\ALI\Desktop\indirilen fotolar\quality_out\results.csv"
OUT_DIR  = r"C:\Users\ALI\Desktop\indirilen fotolar\quality_out"

def read_rows():
    scores_all = []
    scores_acc = []
    scores_rej = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = int(row["quality_score"])
            d = row["decision"].strip()
            scores_all.append(s)
            if d == "accept":
                scores_acc.append(s)
            else:
                scores_rej.append(s)
    return scores_all, scores_acc, scores_rej

def save_hist(scores, title, out_name, bins=20):
    plt.figure()
    plt.hist(scores, bins=bins)
    plt.title(title)
    plt.xlabel("Quality Score (0-100)")
    plt.ylabel("Image Count")
    out_path = os.path.join(OUT_DIR, out_name)
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

def save_dual_hist(scores_acc, scores_rej, out_name, bins=20):
    plt.figure()
    plt.hist(scores_acc, bins=bins, alpha=0.6, label="ACCEPT")
    plt.hist(scores_rej, bins=bins, alpha=0.6, label="REJECT")
    plt.title("Quality Score Distribution (ACCEPT vs REJECT)")
    plt.xlabel("Quality Score (0-100)")
    plt.ylabel("Image Count")
    plt.legend()
    out_path = os.path.join(OUT_DIR, out_name)
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

def main():
    scores_all, scores_acc, scores_rej = read_rows()

    save_hist(scores_all, "Quality Score Distribution (All Images)", "hist_all.png")
    save_dual_hist(scores_acc, scores_rej, "hist_accept_reject.png")

    # İsteğe bağlı: score'ları sıraya dizip çizgi grafiği (çok şık durur)
    scores_sorted = sorted(scores_all)
    plt.figure()
    plt.plot(scores_sorted)
    plt.title("Sorted Quality Scores")
    plt.xlabel("Image Index (sorted)")
    plt.ylabel("Quality Score")
    out_path = os.path.join(OUT_DIR, "scores_sorted_curve.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    main()
