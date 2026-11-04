"""Build the tables the explorer reads, from the original Lens.org export.

No new data is collected. Input: data/raw/lens_export_2024-01-28.csv.gz (the export used
in the 2024 analysis, already cleaned and topic-modelled) plus two small lookup tables.
Output: data/processed/*.parquet

Run from the repository root:  python scripts/prepare_data.py
"""
from __future__ import annotations

import re
from itertools import combinations
from pathlib import Path

import networkx as nx
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
SEP = ";;"

# ---------------------------------------------------------------- keyword rules
# Labels come from title + abstract. They are keyword flags, not expert coding:
# a patent can carry several labels, and "Not stated" means no keyword matched.
TARGETS = {
    "PD-1": r"\bpd-?1\b|programmed (?:cell )?death[- ]1\b|programmed death receptor 1|\bcd279\b",
    "PD-L1": r"\bpd-?l1\b|programmed (?:cell )?death[- ]ligand[- ]1|\bb7-?h1\b|\bcd274\b",
    "CTLA-4": r"\bctla-?4\b|cytotoxic t[- ]lymphocyte[- ]associated|\bcd152\b",
    "LAG-3": r"\blag-?3\b|lymphocyte[- ]activation gene[- ]3|\bcd223\b",
    "TIM-3": r"\btim-?3\b|\bhavcr2\b",
    "TIGIT": r"\btigit\b",
    "Other checkpoint": r"\bvista\b|\bb7-?h3\b|\bcd47\b|\bnkg2a\b|\bido1?\b|\bcd73\b|\ba2ar\b|\bsiglec-?15\b|\bbtla\b",
}
STRATEGIES = {
    "Combination therapy": r"\bcombination|\bcombined with|\bin combination|co-?administ",
    "Bispecific / multispecific": r"bi-?specific|multi-?specific|tri-?specific|bifunctional",
    "Formulation / delivery": r"formulation|subcutaneous|dosage form|dosing regimen|lyophili|sustained release|nanoparticle",
    "Biomarker / diagnostic": r"biomarker|predict(?:ing|ive|s)? (?:the )?response|companion diagnostic|\bdiagnos",
    "Cell therapy": r"\bcar-?t\b|chimeric antigen receptor|\bcar-?nk\b|cell therapy|adoptive|\btil\b",
    "Vaccine / oncolytic virus": r"vaccin|oncolytic",
    "Antibody–drug conjugate": r"antibody[- ]drug conjugate|\badc\b",
    "Small molecule": r"small molecule|compound of formula|compounds of formula|\bformula \(i\)",
}

ACADEMIC_HINT = re.compile(
    r"universit|hospital|institut|cancer cent|medical cent|foundation|inserm|cnrs|college|school|"
    r"academy|clinic\b|ziekenhuis|stichting|centre hospitalier|chu\b|research council|national cancer|\bnih\b|memorial sloan|dana[- ]farber",
    re.I,
)


def split(s) -> list[str]:
    if pd.isna(s) or str(s).strip() == "":
        return []
    return [x.strip() for x in str(s).split(SEP) if x.strip() and x.strip().lower() != "nan"]


def norm(name: str) -> str:
    """Case- and punctuation-insensitive key for matching applicant names."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def flag(text: str, rules: dict[str, str]) -> list[str]:
    hits = [k for k, p in rules.items() if re.search(p, text)]
    return hits


def status_group(legal: str, doc_type: str) -> str:
    if doc_type == "Granted Patent" or legal == "ACTIVE":
        return "Granted / in force"
    if legal == "PENDING":
        return "Pending application"
    if legal in ("DISCONTINUED", "EXPIRED", "INACTIVE"):
        return "Discontinued / expired"
    return "Other / unknown"


def main() -> None:
    raw = pd.read_csv(RAW / "lens_export_2024-01-28.csv.gz", low_memory=False)
    countries = pd.read_csv(RAW / "country_lookup.csv")
    jur = pd.read_csv(RAW / "jurisdiction_lookup.csv")

    # ------------------------------------------------------------ one row per document
    p = pd.DataFrame({
        "lens_id": raw["Lens ID"],
        "title": raw["Title"].fillna(""),
        "abstract": raw["Abstract"].fillna(""),
        "year": raw["Application Year"].astype("Int64"),
        "priority_year": raw["Earliest Priority Year"].astype("Int64"),
        "jurisdiction": raw["Jurisdiction"],
        "doc_type": raw["Document Type"].fillna("Unknown"),
        "legal_status": raw["Legal Status"].fillna("UNKNOWN"),
        "cited_by_patents": raw["Cited by Patent Count"].fillna(0).astype(int),
        "npl_citations": raw["NPL Citation Count"].fillna(0).astype(int),
        "npl_resolved": raw["NPL Resolved Citation Count"].fillna(0).astype(int),
        "family_size": raw["Simple Family Size"].fillna(1).astype(int),
        "topic": raw["Topic N°"].fillna("Unassigned").str.replace(r'^Topic \d+: "?|"$', "", regex=True),
        "url": raw["URL"],
    })
    p["status"] = [status_group(l, d) for l, d in zip(p.legal_status, p.doc_type)]
    text = (p.title + " " + p.abstract).str.lower()
    p["targets"] = [SEP.join(flag(t, TARGETS) or ["Not stated"]) for t in text]
    p["strategies"] = [SEP.join(flag(t, STRATEGIES) or ["Single agent / not stated"]) for t in text]

    # ------------------------------------------------------------ applicants (long)
    # The export's per-document country/category lists are de-duplicated sets, so they do not
    # line up with the applicant list. Country and type therefore come from the 2024
    # applicant table (one row per applicant), with the type corrected below.
    look = pd.read_csv(RAW / "applicant_lookup.csv")
    look["key"] = look["applicant"].map(norm)
    look = look.drop_duplicates("key").set_index("key")
    TYPE = {"Commercial": "Commercial", "Academic": "Academic / research",
            "Individual": "Individual", "Governmental": "Government"}
    rows = []
    for lid, names in zip(raw["Lens ID"], raw["Applicants_clean"].map(split)):
        for n in names:
            info = look.loc[norm(n)] if norm(n) in look.index else None
            cat = TYPE.get(info["category"], "Unknown") if info is not None else "Unknown"
            if cat in ("Commercial", "Unknown") and ACADEMIC_HINT.search(n):
                cat = "Academic / research"          # fixes e.g. Dana-Farber, hospitals
            rows.append({"lens_id": lid, "applicant": n,
                         "country": info["country"] if info is not None else None, "type": cat})
    app = pd.DataFrame(rows).drop_duplicates(["lens_id", "applicant"])
    app["country"] = app["country"].where(app["country"].notna(), None)

    # one row per document-country pair (a document counts once per applicant country)
    cty = (raw[["Lens ID", "Applicants_countries"]].assign(country=lambda d: d["Applicants_countries"].map(split))
           .explode("country").dropna(subset=["country"]).rename(columns={"Lens ID": "lens_id"})
           [["lens_id", "country"]].drop_duplicates()
           .merge(countries[["country", "region", "iso3"]], on="country", how="left"))

    # ------------------------------------------------------------ inventors (long)
    inv = (raw[["Lens ID", "Inventors_clean"]].assign(inventor=lambda d: d["Inventors_clean"].map(split))
           .explode("inventor").dropna(subset=["inventor"])
           .rename(columns={"Lens ID": "lens_id"})[["lens_id", "inventor"]].drop_duplicates())
    inv["inventor"] = inv["inventor"].str.title()

    # ------------------------------------------------------------ network centrality (full data)
    def centrality(long: pd.DataFrame, col: str) -> pd.DataFrame:
        g = nx.Graph()
        g.add_nodes_from(long[col].unique())
        for _, grp in long.groupby("lens_id")[col]:
            for a, b in combinations(sorted(set(grp)), 2):
                w = g[a][b]["weight"] + 1 if g.has_edge(a, b) else 1
                g.add_edge(a, b, weight=w)
        deg = nx.degree_centrality(g)
        btw = nx.betweenness_centrality(g, k=min(500, len(g)), seed=7) if len(g) > 1 else {}
        return pd.DataFrame({col: list(deg), "degree_centrality": list(deg.values()),
                             "betweenness_centrality": [btw.get(n, 0.0) for n in deg]})

    org_net = centrality(app[app.type != "Individual"], "applicant")
    cty_net = centrality(cty, "country")

    # ------------------------------------------------------------ write
    p.to_parquet(OUT / "patents.parquet", index=False)
    app.to_parquet(OUT / "applicants.parquet", index=False)
    cty.to_parquet(OUT / "countries.parquet", index=False)
    inv.to_parquet(OUT / "inventors.parquet", index=False)
    org_net.to_parquet(OUT / "applicant_network.parquet", index=False)
    cty_net.to_parquet(OUT / "country_network.parquet", index=False)
    jur.to_parquet(OUT / "jurisdictions.parquet", index=False)

    print(f"documents {len(p):,} | applicant links {len(app):,} | organisations "
          f"{app.loc[app.type != 'Individual', 'applicant'].nunique():,} | inventors {inv.inventor.nunique():,}")
    print(p.status.value_counts().to_string())
    print(p.targets.str.split(SEP).explode().value_counts().to_string())
    print(p.strategies.str.split(SEP).explode().value_counts().to_string())
    print(app.type.value_counts().to_string())


if __name__ == "__main__":
    main()
