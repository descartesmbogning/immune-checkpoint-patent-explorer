"""Agreement between the keyword labels and the hand-coded validation sample (Supplementary Table S3).

Input: paper/label_check_200_coded.xlsx (sheet "Code here" = the author's blind coding; sheet
"Auto labels (open after coding)" = rule labels at the time of sampling). The rule labels are also
recomputed from data/processed/patents.parquet to confirm they have not changed since sampling.
Output: paper/tables/tableS3_label_check.csv

Run from the repository root:  python scripts/label_check_agreement.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
X = pd.read_excel(ROOT / "paper" / "label_check_200_coded.xlsx", sheet_name=None)
human, auto = X["Code here"], X["Auto labels (open after coding)"]
assert (human["row"].values == auto["row"].values).all(), "rows out of order"
p = pd.read_parquet(ROOT / "data" / "processed" / "patents.parquet").set_index("lens_id")

LABELS = {"PD-1": ("targets", ["PD-1"]), "PD-L1": ("targets", ["PD-L1"]), "CTLA-4": ("targets", ["CTLA-4"]),
          "LAG-3 / TIM-3 / TIGIT": ("targets", ["LAG-3", "TIM-3", "TIGIT"]),
          "Combination therapy": ("strategies", ["Combination therapy"]),
          "Bispecific / multispecific": ("strategies", ["Bispecific / multispecific"])}
yes = lambda s: s.astype(str).str.strip().str.lower().str.startswith("y").values


def kappa(h, a):
    po = (h == a).mean(); pe = h.mean() * a.mean() + (1 - h.mean()) * (1 - a.mean())
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


rows = []
for lab, (col, vals) in LABELS.items():
    H = yes(human[lab])
    A = np.array([bool(set(vals) & set(p.loc[i, col].split(";;"))) for i in auto["lens_id"]])
    assert (A == yes(auto[lab])).all(), f"rule labels for {lab} changed since sampling"
    for g in ["All", "China", "United States"]:
        m = np.ones(len(H), bool) if g == "All" else (auto["group"] == g).values
        h, a = H[m], A[m]
        tp, fp, fn, tn = (h & a).sum(), (~h & a).sum(), (h & ~a).sum(), (~h & ~a).sum()
        rows.append({"label": lab, "group": g, "n": int(m.sum()), "human_yes": int(h.sum()), "rule_yes": int(a.sum()),
                     "agree": round(100 * (tp + tn) / m.sum(), 1),
                     "precision": round(100 * tp / (tp + fp), 1) if tp + fp else np.nan,
                     "recall": round(100 * tp / (tp + fn), 1) if tp + fn else np.nan, "kappa": round(kappa(h, a), 2)})
out = pd.DataFrame(rows)
out.to_csv(ROOT / "paper" / "tables" / "tableS3_label_check.csv", index=False)
d = sum(int((yes(human[l]) != yes(auto[l])).sum()) for l in LABELS)
print(out.to_string(index=False)); print(f"decisions that differ: {d} of {len(human) * len(LABELS)}")
