import dash
from dash import dcc, html

import components as c
import data

dash.register_page(__name__, path="/about", name="About", order=7)

QUERY = """(Abatacept OR atezolizumab OR Ipilimumab OR lisavanbulin OR Nivolumab OR pembrolizumab OR "PHI-101"
 OR quemliclustat OR relatlimab OR sotorasib OR spartalizumab OR Camrelizumab OR Tislelizumab OR avelumab
 OR durvalumab OR cemiplimab OR Tremelimumab OR Toripalimab OR Dostarlimab OR Retifanlimab OR Lambrolizumab)
OR (Sintilimab OR Vopratelimab OR Spartalizumab OR Camrelizumab OR Tislelizumab OR "INCMGA00012"
 OR Acrixolimab OR Cosibelimab)
OR ("Checkpoint Inhibitors" OR "Immune Checkpoint Inhibitor" OR "Immune Checkpoint Blockers"
 OR "Checkpoint Blockers" OR "Immune Checkpoint Blockade" OR "Immune Checkpoint Inhibition" OR "Checkpoint Inhibition")
OR ("PD-L1 Inhibitor(s)" OR "Programmed Death-Ligand 1 Inhibitors" OR "PD-1-PD-L1 Blockade"
 OR "CTLA-4 Inhibitor(s)" OR "Cytotoxic T-Lymphocyte-Associated Protein 4 Inhibitor(s)" OR "PD-1 Inhibitor(s)"
 OR "Programmed Cell Death Protein 1 Inhibitor(s)" OR "anti-PD-1" OR "anti-PD-L1" OR "anti-CTLA-4")
OR (yervoy OR keytruda OR opdivo OR Imjudo OR Tecentriq OR Bavencio OR Imfinzi OR Libtayo OR Jemperli
 OR Zynyz OR Loqtorzi)"""

TEXT = f"""
### Data

Patent documents were exported from [Lens.org](https://www.lens.org) on **{data.DATA_DATE}** with the search
below (spelling variants shortened here). After cleaning, the explorer holds **{len(data.PATENTS):,} documents**
with application years {data.YEAR_MIN}–{data.YEAR_MAX}. The export holds about one document per patent family:
the {len(data.PATENTS):,} documents have 3,262 distinct first priority numbers.

### How the labels were made

- **Legal status** groups Lens statuses: granted or active; pending; discontinued, expired or inactive; other.
- **Checkpoint target** and **strategy** are keyword flags on titles and abstracts (for example "bispecific",
  "combination", "subcutaneous"). A document can carry several labels. They are indicative, not expert coding.
- **Topics** come from the topic model run in the 2024 analysis.
- **Applicant type** comes from the 2024 applicant table. Hospitals, universities, institutes and foundations
  that were labelled "commercial" were moved to "academic / research".
- **Activity class** compares an entity's first and last filing year with the last year selected:
  *continuant* (started earlier, still filing), *newcomer* (first filing in the last year),
  *terminator* (several years of filing, stopped earlier), *transient* (one year only, earlier).
- **Centrality** (degree and betweenness) comes from the co-applicant network of the full dataset.

### Limits

- Patents are published about 18 months after filing, so years after {data.LAST_COMPLETE_YEAR} are incomplete.
- Inventor names are not disambiguated; common names may merge several people.
- Counts are documents, not drugs or products. Many filings never become granted patents.
- Applicant country is the applicant's address as recorded, not where the research was done.

### Search used in Lens.org
"""

layout = html.Div([
    c.page_header("About this explorer", "Data, methods and limits."),
    c.card(html.Div([dcc.Markdown(TEXT, link_target="_blank"), html.Pre(QUERY, className="query")])),
    c.card(dcc.Markdown(
        "Built by Maxime Descartes Mbogning Fonkou. Code: "
        "[GitHub](https://github.com/descartesmbogning) · More work: [cognosx.ca](https://cognosx.ca). "
        "The method follows the author's phage therapy patent landscape published in "
        "[Nature Biotechnology (2024)](https://doi.org/10.1038/s41587-024-02493-9).",
        link_target="_blank"), "Credits"),
])
