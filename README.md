# Immune Checkpoint Patents Explorer

An interactive dashboard on **3,320 immune checkpoint therapy patent documents** (PD-1, PD-L1, CTLA-4,
LAG-3, TIM-3, TIGIT and others), exported from [Lens.org](https://www.lens.org) on 28 January 2024.

It answers five questions, each on its own page, and every page follows one shared set of filters
(years, legal status, checkpoint target, strategy, applicant type):

| Page | Question |
| --- | --- |
| Overview | How has filing grown, and how much is granted or still pending? |
| Organisations | Which companies, universities and hospitals file, and is the mix changing? |
| Countries | Where are applicants based, and how fast is China's share growing? |
| Technologies | Which checkpoints are targeted, and which strategies (combinations, bispecifics, formulations…) are used? |
| Filing offices | Where is protection sought (national offices, PCT, EPO)? |
| Science links | How often do patents cite research papers, and which patents are cited most? |
| Inventors | Who is named as inventor (names not disambiguated)? |
| About | Data, methods, labels and limits. |

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                                          # http://127.0.0.1:8050
```

## Deploy on Render

The repository includes `render.yaml`. In Render, choose **New → Blueprint**, pick this repository,
and confirm. Or create a **Web Service** by hand with:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:server --workers 2 --timeout 120`
- Environment variable: `PYTHON_VERSION=3.12.7`

## Repository layout

```
app.py                 Dash entry point (multi-page, shared filter bar)
components.py          navigation, filters, number cards, tables, footer
data.py                loads the processed tables and applies the filters
theme.py               CognosX colours and Plotly template
pages/                 one file per page
assets/style.css       styles (CognosX charter: black, white, amber; Inter)
scripts/prepare_data.py  rebuilds data/processed/ from data/raw/
data/raw/              Lens.org export used in the 2024 analysis + small lookup tables
data/processed/        tables read by the app (Parquet)
```

## Rebuild the data

No new data is collected. To rebuild the processed tables after changing a rule (for example a keyword
for a strategy):

```bash
python scripts/prepare_data.py
```

## Methods in brief

- Target and strategy labels are keyword flags on titles and abstracts; a document can carry several. The combination rule includes phrasing common in machine-translated Chinese abstracts ("combined for use", "synergistic").
- Applicant country and type come from the cleaned 2024 applicant table; hospitals, universities and
  institutes that were labelled commercial are moved to academic / research.
- Activity classes (continuant, newcomer, terminator, transient) compare each entity's first and last
  filing year with the last year selected.
- Years after 2021 are incomplete because patents are published about 18 months after filing.

Full details are on the **About** page.

## What changed from the 2024 dashboard

- One repository instead of several copies; no virtual environment or cache files committed.
- Pages organised by question, with filters shared across all pages.
- Fixed: South Korea, Taiwan, Russia and others missing from maps (wrong country codes); maps opening on
  an empty 1997 frame; misaligned activity class for 32 applicants; Dana-Farber and other institutes
  labelled commercial; top-inventor headline based on an ambiguous name; requirements file saved in UTF-16.
- New: legal status split, checkpoint target and strategy labels, incomplete-year shading, links to
  Lens.org from every organisation and patent, and an About page with the search and limits.

## Credits

Analysis and code: Maxime Descartes Mbogning Fonkou. The method follows the phage therapy patent
landscape published in [Nature Biotechnology (2024)](https://doi.org/10.1038/s41587-024-02493-9).
Patent data © Lens.org, used under its terms of use.
