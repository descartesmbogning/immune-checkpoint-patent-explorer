"""Export the processed tables to one compact JSON file for the static explorer on cognosx.ca.

The static page (cognosx.ca/dashboards/immune-checkpoint) does all filtering in the browser,
so no Python server is needed. Run after prepare_data.py:

    python scripts/export_static.py [output_path]

Default output: data/static/explorer_data.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))
from data import APPLICANT_TYPES, DATA_DATE, LAST_COMPLETE_YEAR, STATUSES, STRATEGIES, TARGETS, SEP  # noqa: E402


def main(out: Path) -> None:
    p = pd.read_parquet(PROC / "patents.parquet").reset_index(drop=True)
    app = pd.read_parquet(PROC / "applicants.parquet")
    cty = pd.read_parquet(PROC / "countries.parquet")
    inv = pd.read_parquet(PROC / "inventors.parquet")
    onet = pd.read_parquet(PROC / "applicant_network.parquet").set_index("applicant")
    cnet = pd.read_parquet(PROC / "country_network.parquet").set_index("country")
    jur = pd.read_parquet(PROC / "jurisdictions.parquet")

    row = {lid: i for i, lid in enumerate(p.lens_id)}
    topics = sorted(p.topic.unique(), key=lambda t: (t == "Unassigned", t))
    jcodes = jur.code.tolist()

    def bits(cell: str, labels: list[str]) -> int:
        return sum(1 << labels.index(x) for x in cell.split(SEP) if x in labels)

    # organisations (individuals kept for the type mix, flagged by type)
    orgs = app.drop_duplicates("applicant")[["applicant", "country", "type"]].reset_index(drop=True)
    oidx = {n: i for i, n in enumerate(orgs.applicant)}
    countries = cty.drop_duplicates("country")[["country", "region", "iso3"]].sort_values("country").reset_index(drop=True)
    cidx = {n: i for i, n in enumerate(countries.country)}
    invs = sorted(inv.inventor.unique())
    iidx = {n: i for i, n in enumerate(invs)}

    def per_doc(long: pd.DataFrame, col: str, idx: dict) -> list[list[int]]:
        out = [[] for _ in range(len(p))]
        for lid, v in zip(long.lens_id, long[col]):
            out[row[lid]].append(idx[v])
        return out

    D = {
        "meta": {"data_date": DATA_DATE, "last_complete_year": LAST_COMPLETE_YEAR,
                 "statuses": STATUSES, "targets": TARGETS, "strategies": STRATEGIES,
                 "types": APPLICANT_TYPES, "topics": topics},
        "jur": {"code": jcodes, "name": jur.name.tolist(), "type": jur.office_type.tolist()},
        "orgs": {"name": orgs.applicant.tolist(), "country": orgs.country.fillna("").tolist(),
                 "type": [APPLICANT_TYPES.index(t) for t in orgs.type],
                 "deg": [round(float(onet.degree_centrality.get(n, 0)), 4) for n in orgs.applicant],
                 "btw": [round(float(onet.betweenness_centrality.get(n, 0)), 4) for n in orgs.applicant]},
        "ctys": {"name": countries.country.tolist(), "region": countries.region.fillna("").tolist(),
                 "iso3": countries.iso3.fillna("").tolist(),
                 "deg": [round(float(cnet.degree_centrality.get(n, 0)), 4) for n in countries.country],
                 "btw": [round(float(cnet.betweenness_centrality.get(n, 0)), 4) for n in countries.country]},
        "invs": invs,
        "p": {
            "id": p.lens_id.tolist(),
            "t": [t[:200] for t in p.title],
            "y": p.year.astype(int).tolist(),
            "j": [jcodes.index(x) for x in p.jurisdiction],
            "s": [STATUSES.index(x) for x in p.status],
            "tg": [bits(x, TARGETS) for x in p.targets],
            "st": [bits(x, STRATEGIES) for x in p.strategies],
            "c": p.cited_by_patents.astype(int).tolist(),
            "n": p.npl_citations.astype(int).tolist(),
            "tp": [topics.index(x) for x in p.topic],
            "a": per_doc(app, "applicant", oidx),
            "k": per_doc(cty, "country", cidx),
            "i": per_doc(inv, "inventor", iidx),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(D, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size/1e6:.2f} MB): {len(p):,} documents, {len(orgs):,} applicants, "
          f"{len(countries)} countries, {len(invs):,} inventors")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "static" / "explorer_data.json")
