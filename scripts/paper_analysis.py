"""Numbers, robustness checks and figures for the short paper on China's rise in checkpoint patents.

Uses only data/processed/ (no new data). Run:  python scripts/paper_analysis.py
Writes paper/results.json, paper/tables/*.csv and paper/figures/*.png|pdf
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "paper"
(OUT / "tables").mkdir(parents=True, exist_ok=True)
(OUT / "figures").mkdir(parents=True, exist_ok=True)
SEP = ";;"
COMPLETE = (2010, 2021)                    # complete application years used for comparisons
EARLY, LATE = (2015, 2016), (2020, 2021)

INK, MUTED, LINE, SOFT = "#141414", "#5c5c5c", "#e6e3dd", "#f7f5f0"
CN_COL, US_COL, OTH = "#C24A2E", "#2F64B5", "#9a9890"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.grid": True, "grid.color": LINE, "grid.linewidth": 0.8, "axes.axisbelow": True,
                     "legend.frameon": False, "savefig.dpi": 300, "savefig.bbox": "tight"})


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float, float]:
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * p, 100 * (c - h), 100 * (c + h)


def two_prop_p(k1, n1, k2, n2) -> float:
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return float("nan")
    z = abs(k1 / n1 - k2 / n2) / se
    return math.erfc(z / math.sqrt(2))


def main() -> None:
    p = pd.read_parquet(PROC / "patents.parquet")
    c = pd.read_parquet(PROC / "countries.parquet")
    a = pd.read_parquet(PROC / "applicants.parquet")
    p["cn"] = p.lens_id.isin(set(c.loc[c.country == "China", "lens_id"]))
    p["us"] = p.lens_id.isin(set(c.loc[c.country == "United States", "lens_id"]))
    p["has_country"] = p.lens_id.isin(set(c.lens_id))
    R: dict = {"n_documents": len(p), "n_with_country": int(p.has_country.sum()),
               "n_cn": int(p.cn.sum()), "n_us": int(p.us.sum()), "n_cn_and_us": int((p.cn & p.us).sum())}

    # ---------------------------------------------------------------- 1. China's share, with checks
    def share(df, mask_col="cn", years=EARLY, ycol="year"):
        sub = df[df[ycol].between(*years)]
        k, n = int(sub[mask_col].sum()), len(sub)
        s, lo, hi = wilson(k, n)
        return {"k": k, "n": n, "pct": round(s, 1), "lo": round(lo, 1), "hi": round(hi, 1)}

    pr = p.dropna(subset=["priority_year"]).copy()
    pr["priority_year"] = pr.priority_year.astype(int)
    # fractional count: China's share of applicant-country links
    links = c.merge(p[["lens_id", "year", "jurisdiction"]], on="lens_id")
    links["w"] = 1 / links.groupby("lens_id").lens_id.transform("size")
    def frac(years, digits=1):
        sub = links[links.year.between(*years)]
        v = 100 * sub.loc[sub.country == "China", "w"].sum() / sub.lens_id.nunique()
        return round(v, digits) if digits is not None else v

    checks = {
        "All documents": (p, "year"),
        "Outside the Chinese patent office": (p[p.jurisdiction != "CN"], "year"),
        "International (PCT) filings only": (p[p.jurisdiction == "WO"], "year"),
        "Documents with a known applicant country": (p[p.has_country], "year"),
        "By earliest priority year": (pr, "priority_year"),
    }
    rows = []
    for name, (df, ycol) in checks.items():
        e, l = share(df, years=EARLY, ycol=ycol), share(df, years=LATE, ycol=ycol)
        rows.append({"check": name, "early_pct": e["pct"], "early_ci": f"{e['lo']}–{e['hi']}", "early_n": e["n"],
                     "late_pct": l["pct"], "late_ci": f"{l['lo']}–{l['hi']}", "late_n": l["n"],
                     "ratio": round((l["k"] / l["n"]) / (e["k"] / e["n"]), 2) if e["k"] else None,  # from unrounded shares
                     "p_value": two_prop_p(e["k"], e["n"], l["k"], l["n"])})
    rows.append({"check": "Fractional counting (share of applicant-country links)", "early_pct": frac(EARLY),
                 "early_ci": "", "early_n": None, "late_pct": frac(LATE), "late_ci": "", "late_n": None,
                 "ratio": round(frac(LATE, None) / frac(EARLY, None), 2), "p_value": None})
    t1 = pd.DataFrame(rows)
    t1.to_csv(OUT / "tables" / "table1_china_share_checks.csv", index=False)
    R["china_share_checks"] = t1.to_dict("records")
    us_e, us_l = share(p, "us", EARLY), share(p, "us", LATE)
    R["us_share"] = {"early": us_e, "late": us_l}

    # yearly series for figure 1
    yrs = list(range(2010, 2024))
    def series(df, col):
        out = []
        for y in yrs:
            sub = df[df.year == y]
            s, lo, hi = wilson(int(sub[col].sum()), len(sub))
            out.append((y, s, lo, hi, len(sub)))
        return pd.DataFrame(out, columns=["year", "pct", "lo", "hi", "n"])
    s_cn_all, s_us_all = series(p, "cn"), series(p, "us")
    s_cn_out = series(p[p.jurisdiction != "CN"], "cn")
    s_cn_pct = series(p[p.jurisdiction == "WO"], "cn")
    pd.concat([s_cn_all.assign(series="China, all"), s_us_all.assign(series="United States, all"),
               s_cn_out.assign(series="China, outside CN office"), s_cn_pct.assign(series="China, PCT only")]
              ).to_csv(OUT / "tables" / "figure1_series.csv", index=False)

    # ---------------------------------------------------------------- 2. Where each country files
    comp = p[p.year.between(*COMPLETE)]
    groups = {"China": comp[comp.cn & ~comp.us], "United States": comp[comp.us & ~comp.cn],
              "Other countries": comp[~comp.cn & ~comp.us & comp.has_country]}
    office_map = {"CN": "Chinese office", "WO": "International (PCT)", "US": "US office"}
    rows = []
    for g, df in groups.items():
        off = df.jurisdiction.map(lambda j: office_map.get(j, "Other offices")).value_counts()
        for o in ["Chinese office", "International (PCT)", "US office", "Other offices"]:
            k = int(off.get(o, 0)); s, lo, hi = wilson(k, len(df))
            rows.append({"group": g, "office": o, "k": k, "n": len(df), "pct": round(s, 1), "lo": round(lo, 1), "hi": round(hi, 1)})
    t2 = pd.DataFrame(rows)
    t2.to_csv(OUT / "tables" / "table2_filing_route.csv", index=False)
    R["filing_route"] = t2.to_dict("records")
    # granted share by office for context (grant speed differs by office)
    g = comp.assign(granted=comp.status == "Granted / in force")
    R["granted_by_group"] = {k: round(100 * v.status.eq("Granted / in force").mean(), 1) for k, v in groups.items()}
    # geographic reach: simple family size (number of documents in the same simple patent family)
    R["family_size"] = {}
    for k, v in groups.items():
        k1 = int((v.family_size == 1).sum()); s, lo, hi = wilson(k1, len(v))
        R["family_size"][k] = {"median": float(v.family_size.median()), "q1": float(v.family_size.quantile(.25)),
                               "q3": float(v.family_size.quantile(.75)), "single_pct": round(s, 1),
                               "single_ci": f"{lo:.1f}–{hi:.1f}"}
    R["family_single_p"] = two_prop_p(int((groups["China"].family_size == 1).sum()), len(groups["China"]),
                                      int((groups["United States"].family_size == 1).sum()), len(groups["United States"]))
    R["granted_cn_office_vs_us_office"] = {"CN office": round(100 * g[g.jurisdiction == "CN"].granted.mean(), 1),
                                           "US office": round(100 * g[g.jurisdiction == "US"].granted.mean(), 1)}

    # ---------------------------------------------------------------- 3. What each country protects
    labels = {
        "PD-1": ("targets", "PD-1"), "PD-L1": ("targets", "PD-L1"), "CTLA-4": ("targets", "CTLA-4"),
        "LAG-3, TIM-3 or TIGIT": ("targets", ("LAG-3", "TIM-3", "TIGIT")),
        "Combination therapy": ("strategies", "Combination therapy"),
        "Bispecific / multispecific": ("strategies", "Bispecific / multispecific"),
        "Biomarker / diagnostic": ("strategies", "Biomarker / diagnostic"),
        "Cell therapy": ("strategies", "Cell therapy"),
        "Formulation / delivery": ("strategies", "Formulation / delivery"),
        "Small molecule": ("strategies", "Small molecule"),
    }
    rows = []
    cn_df, us_df = groups["China"], groups["United States"]
    for name, (col, val) in labels.items():
        vals = val if isinstance(val, tuple) else (val,)
        has = lambda df: df[col].str.split(SEP).map(lambda xs: bool(set(vals) & set(xs)))
        kc, ku = int(has(cn_df).sum()), int(has(us_df).sum())
        sc, lc, hc = wilson(kc, len(cn_df)); su, lu, hu = wilson(ku, len(us_df))
        rows.append({"label": name, "china_pct": round(sc, 1), "china_ci": f"{lc:.1f}–{hc:.1f}",
                     "us_pct": round(su, 1), "us_ci": f"{lu:.1f}–{hu:.1f}", "diff_pp": round(sc - su, 1),
                     "p_value": two_prop_p(kc, len(cn_df), ku, len(us_df))})
    t3 = pd.DataFrame(rows)
    t3.to_csv(OUT / "tables" / "table3_what_is_protected.csv", index=False)
    R["what_is_protected"] = t3.to_dict("records")
    R["groups_n"] = {k: len(v) for k, v in groups.items()}

    # applicants
    def apps_for(country, df):
        aa = a[a.lens_id.isin(df.lens_id) & (a.country == country)]
        acad = aa[aa.type == "Academic / research"].lens_id.nunique() / max(df.lens_id.nunique(), 1)
        top = (aa[aa.type != "Individual"].groupby("applicant").lens_id.nunique().sort_values(ascending=False).head(10))
        conc = top.head(10).sum() / max(len(df), 1)
        return round(100 * acad, 1), top, round(100 * conc, 1)
    R["applicants"] = {}
    for k, df in [("China", cn_df), ("United States", us_df)]:
        acad, top, conc = apps_for(k, df)
        R["applicants"][k] = {"academic_pct": acad, "top10_share_pct": conc,
                              "top10": [{"name": n, "docs": int(v)} for n, v in top.items()],
                              "n_orgs": int(a[a.lens_id.isin(df.lens_id) & (a.country == k) & (a.type != "Individual")].applicant.nunique())}
    R["science_links"] = {k: round(100 * (v.npl_citations > 0).mean(), 1) for k, v in groups.items()}

    # PD-(L)1 x VEGF bispecifics (the class of ivonescimab), all years
    txt = (p.title + " " + p.abstract).str.lower()
    pv = p[txt.str.contains(r"\bvegf") & p.strategies.str.contains("Bispecific") & p.targets.str.contains("PD-1|PD-L1")]
    R["pd1_vegf_bispecific"] = {"n": len(pv), "china": int(pv.cn.sum()), "us": int(pv.us.sum()),
                                "first_year": int(pv.year.min()), "by_year": {str(k): int(v) for k, v in pv.year.value_counts().sort_index().items()}}
    pv[["lens_id", "year", "jurisdiction", "title", "cn", "us"]].to_csv(OUT / "tables" / "tableS5_pd1_vegf_bispecifics.csv", index=False)

    # ---------------------------------------------------------------- figures
    def fig1():
        fig, ax = plt.subplots(figsize=(6.6, 3.6))
        ax.axvspan(2021.5, 2023.5, color=SOFT, zorder=0); ax.text(2021.6, 71, "Incomplete", color=MUTED, fontsize=7.5)
        for s, col, lab, ls in [(s_us_all, US_COL, "United States, all documents", "-"), (s_cn_all, CN_COL, "China, all documents", "-"),
                                (s_cn_out, CN_COL, "China, outside the Chinese office", "--"), (s_cn_pct, CN_COL, "China, PCT filings only", ":")]:
            s = s[(s.n >= 30) & (s.year >= 2014)]
            ax.plot(s.year, s.pct, ls, color=col, lw=1.8, marker="o" if ls == "-" else None, ms=3.5, label=lab)
            if ls == "-":
                ax.fill_between(s.year, s.lo, s.hi, color=col, alpha=0.12, lw=0)
        ax.set_ylabel("Share of documents (%)"); ax.set_xlim(2013.6, 2023.5); ax.set_ylim(0, 75)
        ax.set_xticks(range(2014, 2024, 2)); ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.22), fontsize=7.5, ncol=2)
        fig.savefig(OUT / "figures" / "figure1_country_shares.png"); fig.savefig(OUT / "figures" / "figure1_country_shares.pdf"); plt.close(fig)

    def fig2():
        offices = ["Chinese office", "International (PCT)", "US office", "Other offices"]
        cols = [CN_COL, "#C98000", US_COL, OTH]
        fig, ax = plt.subplots(figsize=(6.6, 2.4))
        order = ["China", "United States", "Other countries"]
        for gi, gname in enumerate(order[::-1]):
            left = 0
            sub = t2[t2.group == gname].set_index("office")
            for o, col in zip(offices, cols):
                v = sub.loc[o, "pct"]
                ax.barh(gi, v, left=left, color=col, height=0.6, label=o if gi == 0 else None)
                if v >= 7:
                    ax.text(left + v / 2, gi, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=7.5)
                left += v
        ax.set_yticks(range(3)); ax.set_yticklabels([f"{g}\n(n={R['groups_n'][g]:,})" for g in order[::-1]])
        ax.set_xlim(0, 100); ax.set_xlabel("Share of documents (%)"); ax.grid(axis="y", visible=False)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=4, fontsize=7.5)
        fig.savefig(OUT / "figures" / "figure2_filing_route.png"); fig.savefig(OUT / "figures" / "figure2_filing_route.pdf"); plt.close(fig)

    def fig3():
        t = t3.iloc[::-1].reset_index(drop=True)
        fig, ax = plt.subplots(figsize=(6.6, 3.8))
        for i, r in t.iterrows():
            ax.plot([r.china_pct, r.us_pct], [i, i], color=LINE, lw=2.5, zorder=1)
            for pct, ci, col, off in [(r.china_pct, r.china_ci, CN_COL, 0.12), (r.us_pct, r.us_ci, US_COL, -0.12)]:
                lo, hi = map(float, ci.split("–"))
                ax.errorbar(pct, i + off, xerr=[[pct - lo], [hi - pct]], fmt="o", color=col, ms=5, elinewidth=1, capsize=0, zorder=2)
        ax.set_yticks(range(len(t))); ax.set_yticklabels(t.label)
        ax.set_xlabel("Share of documents with the label (%), 2010–2021, 95% CI")
        ax.plot([], [], "o", color=CN_COL, label=f"China (n={R['groups_n']['China']:,})")
        ax.plot([], [], "o", color=US_COL, label=f"United States (n={R['groups_n']['United States']:,})")
        ax.legend(loc="lower right", fontsize=7.5); ax.grid(axis="y", visible=False); ax.set_xlim(0, None)
        fig.savefig(OUT / "figures" / "figure3_what_is_protected.png"); fig.savefig(OUT / "figures" / "figure3_what_is_protected.pdf"); plt.close(fig)

    fig1(); fig2(); fig3()
    (OUT / "results.json").write_text(json.dumps(R, indent=2, default=float), encoding="utf-8")
    print(json.dumps(R, indent=1, default=float)[:6000])


if __name__ == "__main__":
    main()
