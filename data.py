"""Loads the processed tables once and applies the explorer's filters."""
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "processed"
SEP = ";;"
DATA_DATE = "28 January 2024"
LAST_COMPLETE_YEAR = 2021          # 2022–2023 are still filling up in a January 2024 export
SHARE_START = 2014               # yearly shares are unstable before 2014 (fewer than 40 documents a year)

PATENTS = pd.read_parquet(DATA / "patents.parquet")
APPLICANTS = pd.read_parquet(DATA / "applicants.parquet")
COUNTRIES = pd.read_parquet(DATA / "countries.parquet")
INVENTORS = pd.read_parquet(DATA / "inventors.parquet")
ORG_NET = pd.read_parquet(DATA / "applicant_network.parquet")
CTY_NET = pd.read_parquet(DATA / "country_network.parquet")
JURISDICTIONS = pd.read_parquet(DATA / "jurisdictions.parquet")

PATENTS["target_list"] = PATENTS["targets"].str.split(SEP)
PATENTS["strategy_list"] = PATENTS["strategies"].str.split(SEP)

YEAR_MIN, YEAR_MAX = int(PATENTS.year.min()), int(PATENTS.year.max())
STATUSES = ["Granted / in force", "Pending application", "Discontinued / expired", "Other / unknown"]
TARGETS = ["PD-1", "PD-L1", "CTLA-4", "LAG-3", "TIM-3", "TIGIT", "Other checkpoint", "Not stated"]
STRATEGIES = ["Combination therapy", "Bispecific / multispecific", "Formulation / delivery",
              "Biomarker / diagnostic", "Cell therapy", "Vaccine / oncolytic virus",
              "Antibody–drug conjugate", "Small molecule", "Single agent / not stated"]
APPLICANT_TYPES = ["Commercial", "Academic / research", "Individual", "Government", "Unknown"]


def _any(lists: pd.Series, wanted: list[str]) -> pd.Series:
    w = set(wanted)
    return lists.map(lambda xs: bool(w.intersection(xs)))


def filter_patents(years=None, statuses=None, targets=None, strategies=None, types=None) -> pd.DataFrame:
    """Return the documents that match every filter. Empty or None means 'no filter'."""
    p = PATENTS
    if years:
        p = p[p.year.between(years[0], years[1])]
    if statuses:
        p = p[p.status.isin(statuses)]
    if targets:
        p = p[_any(p.target_list, targets)]
    if strategies:
        p = p[_any(p.strategy_list, strategies)]
    if types:
        ids = APPLICANTS.loc[APPLICANTS.type.isin(types), "lens_id"].unique()
        p = p[p.lens_id.isin(ids)]
    return p


def lifecycle_class(first: int, last: int, ref: int) -> str:
    """Entity activity relative to the last year shown (rules from the 2024 analysis).

    Continuant: started before and still filing in the reference year.
    Newcomer:   first and only filing year is the reference year.
    Terminator: filed in several years but stopped before the reference year.
    Transient:  filed in a single year before the reference year.
    """
    if last == ref:
        return "Newcomer" if first == ref else "Continuant"
    return "Transient" if first == last else "Terminator"


def entity_table(long: pd.DataFrame, patents: pd.DataFrame, key: str, ref_year: int,
                 extra: list[str] | None = None, network: pd.DataFrame | None = None) -> pd.DataFrame:
    """Per-entity counts for the filtered documents (documents, citations, years, class)."""
    m = long.merge(patents[["lens_id", "year", "cited_by_patents", "status"]], on="lens_id")
    if m.empty:
        return pd.DataFrame(columns=[key, "Documents", "Granted", "Citations", "First year", "Last year", "Class"])
    g = m.groupby([key] + (extra or []), dropna=False)
    t = g.agg(Documents=("lens_id", "nunique"),
              Granted=("status", lambda s: int((s == "Granted / in force").sum())),
              Citations=("cited_by_patents", "sum"),
              **{"First year": ("year", "min"), "Last year": ("year", "max")}).reset_index()
    t["Class"] = [lifecycle_class(f, l, ref_year) for f, l in zip(t["First year"], t["Last year"])]
    t["Share (%)"] = (100 * t.Documents / max(patents.lens_id.nunique(), 1)).round(2)
    if network is not None:
        t = t.merge(network, on=key, how="left")
        t["degree_centrality"] = t["degree_centrality"].round(4)
        t["betweenness_centrality"] = t["betweenness_centrality"].round(4)
        t = t.rename(columns={"degree_centrality": "Degree centrality",
                              "betweenness_centrality": "Betweenness centrality"})
    return t.sort_values(["Documents", "Citations"], ascending=False)


@lru_cache(maxsize=1)
def counts_overall() -> dict:
    p = PATENTS
    return {"documents": len(p), "granted": int((p.status == "Granted / in force").sum()),
            "organisations": APPLICANTS.loc[APPLICANTS.type != "Individual", "applicant"].nunique(),
            "countries": COUNTRIES.country.nunique()}
