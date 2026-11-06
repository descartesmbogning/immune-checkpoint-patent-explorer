# medRxiv submission sheet

Everything the medRxiv form asks for, ready to paste. Submit at https://submit.medrxiv.org (free; register first).

## Files to upload

| Item | File |
|---|---|
| Manuscript (single PDF, figures and tables in the text) | `build/manuscript.pdf` |
| Same manuscript as Word, if you prefer medRxiv to convert it | `build/manuscript.docx` |
| Supplementary material | `build/supplementary.pdf` |
| Figures, high resolution (only if asked) | `../figures/figure1_country_shares.png`, `figure2_filing_route.png`, `figure3_what_is_protected.png` (300 dpi; PDF versions also available) |

## Form fields

- **Article type:** New Results
- **Subject area:** Health Policy (alternative: Oncology)
- **Title:** Strong at home, going global: China's rise in immune checkpoint therapy patents, 2010–2023
- **Author:** Maxime Descartes Mbogning Fonkou, CognosX, Burnaby, British Columbia, Canada. ORCID 0000-0001-5581-3891. Corresponding author.
- **Abstract:** paste the abstract from `manuscript.md` (about 330 words; medRxiv has no strict limit).
- **Keywords:** immune checkpoint inhibitors; PD-1; patents; China; bispecific antibodies; patent landscape; health policy
- **License:** CC BY 4.0 (recommended: lets others reuse the figures with credit)

## Declarations (medRxiv asks each as a checkbox or text box)

- **Competing interests:** The author founded CognosX, which provides science-intelligence services, including patent landscape analyses. No other competing interests.
- **Funding:** This work received no specific funding.
- **Ethics:** Not applicable. The study used only publicly available patent records; it involved no human participants, patient data or intervention, so no ethics committee approval or consent was required. (On the form: tick that all relevant ethical guidelines were followed; answer "not applicable" to IRB approval and consent.)
- **Clinical trial registration:** Not applicable (not a clinical trial).
- **Reporting guidelines:** No EQUATOR guideline applies to patent landscape studies; all steps are reported in Methods, the supplement and the public code.
- **Data availability:** All processed data and code are openly available at https://github.com/descartesmbogning/immune-checkpoint-patent-explorer (release `v1.0-preprint`). Interactive explorer: https://cognosx.ca/dashboards/immune-checkpoint.html. Raw patent records are available from Lens.org under its terms of use.
- **AI use:** An AI assistant (Claude, Anthropic) helped write analysis code and draft and edit text; the author checked all analyses and takes full responsibility.

## Before you press submit

1. Read the PDF once end to end.
2. Optional: connect the GitHub repository to Zenodo and create a DOI for release `v1.0-preprint`, then add the DOI to the data-availability statement and rebuild (`python scripts/build_manuscript.py`).
3. Confirm the correspondence e-mail (currently cognosxx@gmail.com).
4. After posting, add the medRxiv DOI to the explorer's About section and to the repository README.

## Rebuild

```bash
python scripts/paper_analysis.py      # numbers, tables, figures
python scripts/build_manuscript.py    # Word + PDF of manuscript and supplement
```
