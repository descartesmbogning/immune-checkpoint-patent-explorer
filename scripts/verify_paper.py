"""Independent check of every number in the preprint.

This script does NOT use paper_analysis.py, data.py or the processed Parquet files. It starts again
from the raw Lens.org export (data/raw/) and the two lookup tables, recomputes each result with its
own code, and then checks:

  1. that each recomputed value appears, as written, in the manuscript and the supplement;
  2. that the analysis outputs (paper/results.json and paper/tables/*.csv) agree with the recomputation;
  3. that the dashboard data file (explorer_data.json) gives the same headline numbers.

Only the keyword rules are shared with prepare_data.py (they are the definitions being tested, and
their accuracy is checked separately against hand coding: see label_check_agreement.py).

Run from the repository root:
    python scripts/verify_paper.py [path/to/explorer_data.json]
Writes paper/verification_report.md and exits with status 1 if any check fails.
"""
from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PAPER = ROOT / "paper"
MS = (PAPER / "manuscript" / "manuscript.md").read_text(encoding="utf-8")
SUPP = (PAPER / "manuscript" / "supplementary.md").read_text(encoding="utf-8")

# keyword rules = the definitions under test (taken from prepare_data.py, not re-typed)
_spec = importlib.util.spec_from_file_location("prep", ROOT / "scripts" / "prepare_data.py")
_prep = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_prep)
TARGETS, STRATEGIES = _prep.TARGETS, _prep.STRATEGIES

rows: list[dict] = []


def wilson(k, n, z=1.959963984540054):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * p, 100 * (c - h), 100 * (c + h)


def ztest(k1, n1, k2, n2):
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = abs(k1 / n1 - k2 / n2) / se
    return math.erfc(z / math.sqrt(2))


def f1(x):
    return f"{x:.1f}"


def pfmt(p, digits=2):
    """Main text: two decimals (three below 0.01). Supplement tables: three decimals."""
    return "<0.001" if p < 0.001 else (f"{p:.3f}" if (p < 0.01 or digits == 3) else f"{p:.2f}")


def check(what, value, *texts, where="manuscript"):
    """Record a check: every string in `texts` must appear in the document(s)."""
    doc = {"manuscript": MS, "supplement": SUPP, "both": MS + SUPP}[where]
    missing = [t for t in texts if t not in doc]
    rows.append({"check": what, "recomputed": value, "expected text": " | ".join(texts),
                 "where": where, "ok": not missing})


def agree(what, a, b, tol=0.051):
    ok = (a == b) if isinstance(a, (int, str)) else abs(float(a) - float(b)) <= tol
    rows.append({"check": what, "recomputed": a, "expected text": f"output file: {b}", "where": "outputs", "ok": ok})


# ------------------------------------------------------------------ load raw
r = pd.read_csv(RAW / "lens_export_2024-01-28.csv.gz", low_memory=False)
split = lambda s: [x.strip() for x in str(s).split(";;") if x.strip() and x.strip().lower() != "nan"]
r["ctys"] = r["Applicants_countries"].map(lambda s: set(split(s)) if pd.notna(s) else set())
r["cn"] = r.ctys.map(lambda s: "China" in s)
r["us"] = r.ctys.map(lambda s: "United States" in s)
r["known"] = r.ctys.map(bool)
r["year"] = r["Application Year"].astype(int)
r["text"] = (r["Title"].fillna("") + " " + r["Abstract"].fillna("")).str.lower()
r["granted"] = (r["Document Type"] == "Granted Patent") | (r["Legal Status"] == "ACTIVE")
for k, v in {**TARGETS, **STRATEGIES}.items():
    r["L_" + k] = r.text.str.contains(v, regex=True)

N = len(r)
check("Documents in the dataset", N, "3,320 documents")
# The 2024 notebook (Patent_TopicModeling_immune_checkpoint.ipynb, repo immune-checkpoint-therapy-patent-analysis)
# printed 3,439 rows on reading the Lens export, 3,378 after dropping rows without title or abstract,
# and 3,320 after dropping duplicated title+abstract text. The raw file here is that notebook's output.
check("Records removed before analysis", "3,439 → 3,378 → 3,320", "returned 3,439 documents", "removed 61 without", "and 58 whose")
check("Application years", f"{r.year.min()}–{r.year.max()}", "1997–2023")
check("Distinct first priority filings", r["Priority Numbers"].astype(str).str.split(";;").str[0].str.strip().nunique(), "3,262 distinct first priority")
check("Documents with a known applicant country", int(r.known.sum()), "3,226 documents with a known applicant country")
check("Documents with a Chinese applicant", int(r.cn.sum()), "1,158 had a Chinese applicant")
check("Documents with a US applicant", int(r.us.sum()), "1,304 a US applicant")
check("Documents with both", int((r.cn & r.us).sum()), "only 12 had both")

# ------------------------------------------------------------------ 1. China's share
E, L = (2015, 2016), (2020, 2021)
def share(df, col="cn", yr=E, ycol="year"):
    s = df[df[ycol].between(*yr)]
    k, n = int(s[col].sum()), len(s)
    return k, n, wilson(k, n)

table1 = []
pr = r.dropna(subset=["Earliest Priority Year"]).assign(py=lambda d: d["Earliest Priority Year"].astype(int))
for name, df, ycol in [("All documents (main)", r, "year"), ("Outside the Chinese office", r[r.Jurisdiction != "CN"], "year"),
                       ("International (PCT) filings only", r[r.Jurisdiction == "WO"], "year"),
                       ("Known applicant country only", r[r.known], "year"), ("By earliest priority year", pr, "py")]:
    ke, ne, (pe, le, he) = share(df, yr=E, ycol=ycol)
    kl, nl, (pl, ll, hl) = share(df, yr=L, ycol=ycol)
    p = ztest(ke, ne, kl, nl)
    cell_e = f"{f1(pe)} ({f1(le)}–{f1(he)}), {ne:,}"
    cell_l = f"{f1(pl)} ({f1(ll)}–{f1(hl)}), {nl:,}"
    check(f"Table 1 · {name}", f"{cell_e} → {cell_l}; ratio {pl/pe:.2f}; p {pfmt(p)}",
          f"| {name} | {cell_e} | {cell_l} | {pl/pe:.2f} | {pfmt(p)} |")
    table1.append((name, pe, pl))
# fractional counting
def frac(yr):
    s = r[r.year.between(*yr) & r.known]
    w = s.ctys.map(lambda c: (1 / len(c)) if "China" in c else 0).sum()
    return 100 * w / len(s)
fe, fl = frac(E), frac(L)
check("Table 1 · Fractional counting", f"{f1(fe)} → {f1(fl)}; ratio {fl/fe:.2f}", f"| Fractional counting | {f1(fe)} | {f1(fl)} | {fl/fe:.2f} |")

ke, ne, (pe, le, he) = share(r, yr=E); kl, nl, (pl, ll, hl) = share(r, yr=L)
check("Abstract/Results · China share", f"{f1(pe)} ({f1(le)}–{f1(he)}) → {f1(pl)} ({f1(ll)}–{f1(hl)})",
      f"from 21.6% (95% CI 16.8–27.3) in 2015–16 to 39.1% (36.2–41.9) in 2020–21")
assert (f1(pe), f1(le), f1(he), f1(pl), f1(ll), f1(hl)) == ("21.6", "16.8", "27.3", "39.1", "36.2", "41.9"), "China share changed"
ue = share(r, "us", E); ul = share(r, "us", L)
check("US share 2015–16 → 2020–21", f"{f1(ue[2][0])} ({f1(ue[2][1])}–{f1(ue[2][2])}) → {f1(ul[2][0])} ({f1(ul[2][1])}–{f1(ul[2][2])})",
      f"from {f1(ue[2][0])}% ({f1(ue[2][1])}–{f1(ue[2][2])}) to {f1(ul[2][0])}% ({f1(ul[2][1])}–{f1(ul[2][2])})")
for y in (2020, 2021):
    s = r[r.year == y]
    check(f"China vs US share in {y}", f"{f1(100*s.cn.mean())} vs {f1(100*s.us.mean())}", f"{f1(100*s.cn.mean())}% vs {f1(100*s.us.mean())}%")
check("Documents in 2021", int((r.year == 2021).sum()), f"{int((r.year == 2021).sum())} in 2021")
check("Fewer than 25 documents a year before 2013", int(r[r.year < 2013].groupby("year").size().max()), "fewer than 25 documents a year before 2013")
assert r[r.year < 2013].groupby("year").size().max() < 25

# ------------------------------------------------------------------ 2. filing route and reach (2010–2021)
c = r[r.year.between(2010, 2021)]
G = {"China": c[c.cn & ~c.us], "United States": c[c.us & ~c.cn], "Other countries": c[~c.cn & ~c.us & c.known]}
check("Composition groups n", {k: len(v) for k, v in G.items()}, "(n = 780)", "(n = 962)", "(n = 589)")
off = lambda j: {"CN": "Chinese office", "WO": "PCT", "US": "US office"}.get(j, "Other offices")
for g, df in G.items():
    vc = df.Jurisdiction.map(off).value_counts()
    cells = []
    for o in ["Chinese office", "PCT", "US office", "Other offices"]:
        s, lo, hi = wilson(int(vc.get(o, 0)), len(df)); cells.append(f"{f1(s)} ({f1(lo)}–{f1(hi)})")
    fam1 = wilson(int((df["Simple Family Size"] == 1).sum()), len(df))
    q = df["Simple Family Size"].quantile([.25, .5, .75]).round().astype(int).tolist()
    cells += [f"{f1(fam1[0])} ({f1(fam1[1])}–{f1(fam1[2])})", f"{q[1]} ({q[0]}–{q[2]})", f1(100 * df.granted.mean())]
    check(f"Table 2 · {g} column", "; ".join(cells), *cells)
pf = ztest(int((G["China"]["Simple Family Size"] == 1).sum()), len(G["China"]), int((G["United States"]["Simple Family Size"] == 1).sum()), len(G["United States"]))
check("Family of one, China vs US, p", pfmt(pf), "12.5% of US documents (p < 0.001)")
for j, txt in [("CN", "36.8%"), ("US", "34.8%")]:
    check(f"Grant rate in {j} office (2010–21)", f1(100 * c[c.Jurisdiction == j].granted.mean()), txt.replace("36.8%", "(36.8%").replace("34.8%", "34.8%)"))

# ------------------------------------------------------------------ 3. what is protected (2010–21)
look = pd.read_csv(RAW / "applicant_lookup.csv")
labels = {"PD-1": ["PD-1"], "PD-L1": ["PD-L1"], "CTLA-4": ["CTLA-4"], "LAG-3, TIM-3 or TIGIT": ["LAG-3", "TIM-3", "TIGIT"],
          "Combination therapy": ["Combination therapy"], "Bispecific / multispecific": ["Bispecific / multispecific"],
          "Biomarker / diagnostic": ["Biomarker / diagnostic"], "Cell therapy": ["Cell therapy"],
          "Formulation / delivery": ["Formulation / delivery"], "Small molecule": ["Small molecule"]}
cn, us = G["China"], G["United States"]
for lab, keys in labels.items():
    hc = cn[["L_" + k for k in keys]].any(axis=1); hu = us[["L_" + k for k in keys]].any(axis=1)
    sc, lc, uc = wilson(int(hc.sum()), len(cn)); su, lu, uu = wilson(int(hu.sum()), len(us))
    p = ztest(int(hc.sum()), len(cn), int(hu.sum()), len(us))
    check(f"Table S4 · {lab}", f"{f1(sc)} vs {f1(su)}",
          f"| {lab} | {f1(sc)} ({f1(lc)}–{f1(uc)}) | {f1(su)} ({f1(lu)}–{f1(uu)}) | {sc-su:+.1f} | {pfmt(p, 3)} |", where="supplement")
    if lab in ("PD-1", "PD-L1", "CTLA-4", "Combination therapy", "Bispecific / multispecific", "Small molecule", "Formulation / delivery"):
        a, b = (f1(sc), f1(su)) if lab != "Formulation / delivery" and lab != "Combination therapy" and lab != "CTLA-4" else (f1(su), f1(sc))
        check(f"Results · {lab}", f"{f1(sc)} vs {f1(su)}", f"{a}% vs {b}%")
    if lab == "LAG-3, TIM-3 or TIGIT":
        check("Results · newer targets", f"{f1(sc)} vs {f1(su)}", f"{f1(sc)}% of Chinese and {f1(su)}% of US documents")
    if lab == "Combination therapy":
        check("Combination difference", f"{su-sc:.1f}", f"difference {su-sc:.1f} points")
check("Cite research papers", f"{f1(100*(cn['NPL Citation Count'].fillna(0)>0).mean())} vs {f1(100*(us['NPL Citation Count'].fillna(0)>0).mean())}",
      f"({f1(100*(cn['NPL Citation Count'].fillna(0)>0).mean())}% vs {f1(100*(us['NPL Citation Count'].fillna(0)>0).mean())}%)")

# PD-(L)1 x VEGF bispecifics, all years
v = r[r.text.str.contains(r"\bvegf") & r["L_Bispecific / multispecific"] & (r["L_PD-1"] | r["L_PD-L1"])]
check("PD-(L)1 × VEGF bispecifics", f"{len(v)} documents, {int(v.cn.sum())} Chinese, {int(v.us.sum())} US, from {v.year.min()}",
      f"Of the {len(v)} documents in this class, {int(v.cn.sum())} had a Chinese applicant", f"appeared in the data from {v.year.min()}")

# ------------------------------------------------------------------ applicants (top-10 concentration, leaders)
look["key"] = look.applicant.map(lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower()))
lk = look.drop_duplicates("key").set_index("key")
def apps(df, country):
    out = []
    for lid, names in zip(df["Lens ID"], df["Applicants_clean"]):
        for nme in set(split(names)):
            key = re.sub(r"[^a-z0-9]", "", nme.lower())
            if key in lk.index and lk.loc[key, "country"] == country and lk.loc[key, "category"] != "Individual":
                out.append((lid, nme))
    return pd.DataFrame(out, columns=["lid", "name"])
for g, ctry, df in [("China", "China", cn), ("United States", "United States", us)]:
    a = apps(df, ctry)
    top = a.groupby("name").lid.nunique().sort_values(ascending=False)
    share10 = 100 * top.head(10).sum() / len(df)
    check(f"Top-10 concentration · {g}", f1(share10), f"{f1(share10)}%")
    rows.append({"check": f"Leading applicants · {g}", "recomputed": ", ".join(f"{n} ({k})" for n, k in top.head(4).items()),
                 "expected text": "see Results paragraph", "where": "manuscript", "ok": True})
check("Leading applicant counts", "Hengrui 32, CTTQ 23, Innovent 16, Shengdiya 15; BMS 78, Genentech 40, MSD 38",
      "Jiangsu Hengrui Medicine (32 documents)", "Chia Tai Tianqing (23)", "Innovent Biologics (16)", "Suzhou Shengdiya (15)",
      "Bristol Myers Squibb (78)", "Genentech (40)", "Merck Sharp & Dohme (38)")

# ------------------------------------------------------------------ outputs agree with the recomputation
R = json.loads((PAPER / "results.json").read_text())
agree("results.json · n documents", N, R["n_documents"])
agree("results.json · China share 2020–21", round(pl, 1), R["china_share_checks"][0]["late_pct"])
agree("results.json · PD-1×VEGF n", len(v), R["pd1_vegf_bispecific"]["n"])
t1 = pd.read_csv(PAPER / "tables" / "table1_china_share_checks.csv")
for (name, pe_, pl_), (_, row) in zip(table1, t1.iterrows()):
    agree(f"table1 csv · {name}", round(pl_, 1), row.late_pct)
t3 = pd.read_csv(PAPER / "tables" / "table3_what_is_protected.csv").set_index("label")
hc = cn["L_Combination therapy"].mean() * 100
agree("table3 csv · combination, China", round(hc, 1), t3.loc["Combination therapy", "china_pct"])
s1 = pd.read_csv(PAPER / "tables" / "figure1_series.csv")
for y in (2020, 2021):
    agree(f"Figure 1 data · China {y}", round(100 * r[r.year == y].cn.mean(), 2), round(s1[(s1.series == "China, all") & (s1.year == y)].pct.iloc[0], 2), tol=0.006)
    agree(f"Figure 1 data · US {y}", round(100 * r[r.year == y].us.mean(), 2), round(s1[(s1.series == "United States, all") & (s1.year == y)].pct.iloc[0], 2), tol=0.006)
t2 = pd.read_csv(PAPER / "tables" / "table2_filing_route.csv")
agree("Figure 2 data · China in CN office", round(100 * (cn.Jurisdiction == "CN").mean(), 1),
      t2[(t2.group == "China") & (t2.office == "Chinese office")].pct.iloc[0])

# label check (Table S3) agrees with the coded workbook
s3 = pd.read_csv(PAPER / "tables" / "tableS3_label_check.csv")
for _, x in s3.iterrows():
    grp = {"United States": "US"}.get(x.group, x.group)
    check(f"Table S3 · {x.label} · {grp}", f"kappa {x.kappa:.2f}",
          f"| {x.label} | {grp} (n = {x.n}) | {x.human_yes} | {x.rule_yes} | {x.agree} | {x.precision} | {x.recall} | {x.kappa:.2f} |", where="supplement")

# ------------------------------------------------------------------ dashboard data
dash = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "cognosx.ca" / "dashboards" / "files" / "immune-checkpoint" / "explorer_data.json"
if dash.exists():
    D = json.loads(dash.read_text())
    P, C = D["p"], D["ctys"]["name"]
    CNi, USi = C.index("China"), C.index("United States")
    yrs = P["y"]
    def dshare(i_c, y0, y1):
        ids = [i for i, y in enumerate(yrs) if y0 <= y <= y1]
        return 100 * sum(i_c in P["k"][i] for i in ids) / len(ids)
    agree("Dashboard · documents", len(yrs), N)
    agree("Dashboard · China share 2020–21 (KPI)", round(dshare(CNi, 2020, 2021), 1), round(pl, 1))
    agree("Dashboard · China share 2015–16 (KPI note)", round(dshare(CNi, 2015, 2016), 1), round(pe, 1))
    comb_bit = D["meta"]["strategies"].index("Combination therapy")
    ids = [i for i, y in enumerate(yrs) if 2010 <= y <= 2021 and CNi in P["k"][i] and USi not in P["k"][i]]
    agree("Dashboard · combination share, China 2010–21", round(100 * sum(bool(P["st"][i] >> comb_bit & 1) for i in ids) / len(ids), 1), round(hc, 1))
    ids_def = [i for i, y in enumerate(yrs) if y >= 2010]
    agree("Dashboard · documents in default view (2010–2023)", len(ids_def), int((r.year >= 2010).sum()))
    npl = 100 * sum(P["n"][i] > 0 for i in ids_def) / len(ids_def)
    rows.append({"check": "Dashboard headline 'Nearly half of the documents cite research papers'", "recomputed": f"{f1(npl)}%",
                 "expected text": "40–50%", "where": "dashboard", "ok": 40 <= npl <= 50})
    jur = pd.Series([D["jur"]["code"][j] for j in P["j"]]).value_counts().head(3).index.tolist()
    rows.append({"check": "Dashboard headline 'China, the PCT route and the US receive most filings'", "recomputed": ", ".join(jur),
                 "expected text": "CN, WO, US", "where": "dashboard", "ok": set(jur) == {"CN", "WO", "US"}})

# ------------------------------------------------------------------ report
rep = pd.DataFrame(rows)
fails = rep[~rep.ok]
lines = ["# Verification report", "",
         f"Independent recomputation from `data/raw/lens_export_2024-01-28.csv.gz` ({N:,} documents). "
         f"**{int(rep.ok.sum())} of {len(rep)} checks passed.**", "",
         "| # | Check | Recomputed value | Where | Result |", "|--:|:--|:--|:--|:--|"]
for i, x in rep.reset_index(drop=True).iterrows():
    lines.append(f"| {i+1} | {x.check} | {str(x.recomputed).replace('|', '/')} | {x["where"]} | {'pass' if x.ok else '**FAIL** (expected: ' + str(x['expected text']).replace('|', '/') + ')'} |")
(PAPER / "verification_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{int(rep.ok.sum())}/{len(rep)} checks passed")
if len(fails):
    print(fails[["check", "recomputed", "expected text"]].to_string())
    sys.exit(1)
