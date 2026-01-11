import csv
from collections import Counter, defaultdict
from pathlib import Path

CSV_PATH = r"C:\Users\ALI\Desktop\indirilen fotolar\quality_out\results.csv"

def main():
    total = 0
    decision_cnt = Counter()
    label_cnt = Counter()
    label_co = Counter()
    scores = []

    # score'a göre örnek seçmek için
    best_accept = None   # (score, path, labels)
    worst_reject = None  # (score, path, labels)

    # label bazlı "en kötü örnek" için
    worst_by_label = {}  # label -> (score, path, labels)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            score = int(row["quality_score"])
            decision = row["decision"].strip()
            labels = row["labels"].strip()
            path = row["path"]

            scores.append(score)
            decision_cnt[decision] += 1

            labs = [l for l in labels.split("|") if l] if labels else []
            for l in labs:
                label_cnt[l] += 1

            # co-occurrence (dark+noisy gibi)
            labs_sorted = tuple(sorted(labs))
            if len(labs_sorted) >= 2:
                # ikili kombinasyon say
                for i in range(len(labs_sorted)):
                    for j in range(i+1, len(labs_sorted)):
                        label_co[(labs_sorted[i], labs_sorted[j])] += 1

            # en iyi ACCEPT
            if decision == "accept":
                if best_accept is None or score > best_accept[0]:
                    best_accept = (score, path, labs)

            # en kötü REJECT
            if decision == "reject":
                if worst_reject is None or score < worst_reject[0]:
                    worst_reject = (score, path, labs)

            # label bazlı en kötü örnek
            for l in labs:
                cur = worst_by_label.get(l)
                if cur is None or score < cur[0]:
                    worst_by_label[l] = (score, path, labs)

    scores_sorted = sorted(scores)
    def pct(p):
        idx = int(round((p/100) * (len(scores_sorted)-1)))
        return scores_sorted[idx]

    print("==== DATASET SUMMARY ====")
    print(f"Total images: {total}")
    print(f"ACCEPT: {decision_cnt['accept']} | REJECT: {decision_cnt['reject']}")
    print(f"Score min/median/max: {min(scores)} / {pct(50)} / {max(scores)}")
    print(f"Score p10/p90: {pct(10)} / {pct(90)}")
    print()

    print("==== TOP LABELS (most common issues) ====")
    for l, c in label_cnt.most_common(10):
        print(f"{l:14s} {c}")
    print()

    print("==== TOP LABEL PAIRS (co-occurrence) ====")
    for (a,b), c in label_co.most_common(10):
        print(f"{a}+{b:14s} {c}")
    print()

    print("==== EXEMPLARS ====")
    print("Best ACCEPT:")
    print(best_accept)
    print("Worst REJECT:")
    print(worst_reject)
    print()

    print("Worst example per label (score, path):")
    for l, tup in sorted(worst_by_label.items(), key=lambda x: x[0]):
        print(f"{l:14s} -> {tup[0]} | {tup[1]}")

if __name__ == "__main__":
    main()
