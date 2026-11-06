---
title: "Supplementary material"
subtitle: "Strong at home, going global: China's rise in immune checkpoint therapy patents, 2010–2023"
---

Maxime Descartes Mbogning Fonkou · CognosX, Burnaby, British Columbia, Canada

All tables are also available as CSV files at github.com/descartesmbogning/immune-checkpoint-patent-explorer (folder paper/tables).

# Table S1. Lens.org search query

Search run on Lens.org on 28 January 2024 (patent documents, all jurisdictions). Spelling variants of some names are shortened here.

```
(Abatacept OR atezolizumab OR Ipilimumab OR lisavanbulin OR Nivolumab OR pembrolizumab OR "PHI-101"
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
 OR Zynyz OR Loqtorzi)
```

# Table S2. Keyword rules for checkpoint targets and therapeutic strategies

Rules are case-insensitive regular expressions applied to the title and abstract. A document can match several rules. Documents with no target match are "Not stated"; documents with no strategy match are "Single agent / not stated".

- **PD-1** (target): `\bpd-?1\b|programmed (?:cell )?death[- ]1\b|programmed death receptor 1|\bcd279\b`
- **PD-L1** (target): `\bpd-?l1\b|programmed (?:cell )?death[- ]ligand[- ]1|\bb7-?h1\b|\bcd274\b`
- **CTLA-4** (target): `\bctla-?4\b|cytotoxic t[- ]lymphocyte[- ]associated|\bcd152\b`
- **LAG-3** (target): `\blag-?3\b|lymphocyte[- ]activation gene[- ]3|\bcd223\b`
- **TIM-3** (target): `\btim-?3\b|\bhavcr2\b`
- **TIGIT** (target): `\btigit\b`
- **Other checkpoint** (target): `\bvista\b|\bb7-?h3\b|\bcd47\b|\bnkg2a\b|\bido1?\b|\bcd73\b|\ba2ar\b|\bsiglec-?15\b|\bbtla\b`
- **Combination therapy** (strategy): `\bcombination|\bcombined (?:with|for|use|administration|application|treatment)|\bin combination|co-?administ|joint(?:ly)? (?:use|administ)|synergi|in conjunction with|used together`
- **Bispecific / multispecific** (strategy): `bi-?specific|multi-?specific|tri-?specific|bifunctional`
- **Formulation / delivery** (strategy): `formulation|subcutaneous|dosage form|dosing regimen|lyophili|sustained release|nanoparticle`
- **Biomarker / diagnostic** (strategy): `biomarker|predict(?:ing|ive|s)? (?:the )?response|companion diagnostic|\bdiagnos`
- **Cell therapy** (strategy): `\bcar-?t\b|chimeric antigen receptor|\bcar-?nk\b|cell therapy|adoptive|\btil\b`
- **Vaccine / oncolytic virus** (strategy): `vaccin|oncolytic`
- **Antibody–drug conjugate** (strategy): `antibody[- ]drug conjugate|\badc\b`
- **Small molecule** (strategy): `small molecule|compound of formula|compounds of formula|\bformula \(i\)`

# Table S3. Agreement between keyword labels and hand coding

Random sample of 200 documents from 2010–2021 (100 with a Chinese applicant, 100 with a US applicant), coded by the author from titles and abstracts without seeing the rule labels. Precision: share of rule "yes" labels that the coder also marked yes. Recall: share of coder "yes" labels that the rule found. Kappa: Cohen's kappa. Ten of 1,200 decisions differed.

| Label | Group | Coded yes | Rule yes | Agreement (%) | Precision (%) | Recall (%) | Kappa |
|:-------|:-----|---:|---:|---:|---:|---:|---:|
| PD-1 | All (n = 200) | 101 | 100 | 99.5 | 100.0 | 99.0 | 0.99 |
| PD-1 | China (n = 100) | 56 | 56 | 100.0 | 100.0 | 100.0 | 1.00 |
| PD-1 | US (n = 100) | 45 | 44 | 99.0 | 100.0 | 97.8 | 0.98 |
| PD-L1 | All (n = 200) | 57 | 58 | 99.5 | 98.3 | 100.0 | 0.99 |
| PD-L1 | China (n = 100) | 35 | 35 | 100.0 | 100.0 | 100.0 | 1.00 |
| PD-L1 | US (n = 100) | 22 | 23 | 99.0 | 95.7 | 100.0 | 0.97 |
| CTLA-4 | All (n = 200) | 28 | 28 | 100.0 | 100.0 | 100.0 | 1.00 |
| CTLA-4 | China (n = 100) | 14 | 14 | 100.0 | 100.0 | 100.0 | 1.00 |
| CTLA-4 | US (n = 100) | 14 | 14 | 100.0 | 100.0 | 100.0 | 1.00 |
| LAG-3 / TIM-3 / TIGIT | All (n = 200) | 6 | 7 | 99.5 | 85.7 | 100.0 | 0.92 |
| LAG-3 / TIM-3 / TIGIT | China (n = 100) | 2 | 2 | 100.0 | 100.0 | 100.0 | 1.00 |
| LAG-3 / TIM-3 / TIGIT | US (n = 100) | 4 | 5 | 99.0 | 80.0 | 100.0 | 0.88 |
| Combination therapy | All (n = 200) | 93 | 93 | 97.0 | 96.8 | 96.8 | 0.94 |
| Combination therapy | China (n = 100) | 35 | 34 | 95.0 | 94.1 | 91.4 | 0.89 |
| Combination therapy | US (n = 100) | 58 | 59 | 99.0 | 98.3 | 100.0 | 0.98 |
| Bispecific / multispecific | All (n = 200) | 17 | 18 | 99.5 | 94.4 | 100.0 | 0.97 |
| Bispecific / multispecific | China (n = 100) | 11 | 11 | 100.0 | 100.0 | 100.0 | 1.00 |
| Bispecific / multispecific | US (n = 100) | 6 | 7 | 99.0 | 85.7 | 100.0 | 0.92 |

# Table S4. Targets and strategies by applicant country, 2010–2021

Documents with Chinese (and no US) applicants (n = 780) and US (and no Chinese) applicants (n = 962). Shares (%) with Wilson 95% confidence intervals; p from a two-sided two-proportion z-test. These values are plotted in Figure 3.

| Label | China, % (95% CI) | United States, % (95% CI) | Difference (points) | p |
|:--|:--|:--|--:|--:|
| PD-1 | 55.5 (52.0–59.0) | 42.9 (39.8–46.1) | +12.6 | <0.001 |
| PD-L1 | 44.6 (41.2–48.1) | 30.5 (27.6–33.4) | +14.2 | <0.001 |
| CTLA-4 | 8.7 (6.9–10.9) | 14.6 (12.5–16.9) | -5.8 | <0.001 |
| LAG-3, TIM-3 or TIGIT | 2.6 (1.7–3.9) | 4.7 (3.5–6.2) | -2.1 | 0.021 |
| Combination therapy | 33.5 (30.2–36.8) | 53.8 (50.7–57.0) | -20.4 | <0.001 |
| Bispecific / multispecific | 10.6 (8.7–13.0) | 4.2 (3.1–5.6) | +6.5 | <0.001 |
| Biomarker / diagnostic | 10.0 (8.1–12.3) | 7.9 (6.4–9.8) | +2.1 | 0.125 |
| Cell therapy | 2.8 (1.9–4.2) | 4.0 (2.9–5.4) | -1.1 | 0.199 |
| Formulation / delivery | 3.6 (2.5–5.1) | 6.2 (4.9–7.9) | -2.6 | 0.012 |
| Small molecule | 6.5 (5.0–8.5) | 2.7 (1.9–3.9) | +3.8 | <0.001 |

# Table S5. PD-1 or PD-L1 × VEGF bispecific documents

Documents with a PD-1 or PD-L1 label, a bispecific or multispecific label and the term "VEGF" in the title or abstract (all application years). Office: WO = international PCT application.

| Year | Office | Applicant country | Title | Lens ID |
|--:|:--|:----|:---------------------|:-------|
| 2019 | CN | China | Anti-PD-L1/VEGF bifunctional antibody and application thereof | [006-156-871-991-364](https://lens.org/006-156-871-991-364) |
| 2019 | CN | China | Anti-VEGF-anti-PD1 bispecific antibody with brand-new sequence | [016-976-152-765-295](https://lens.org/016-976-152-765-295) |
| 2019 | WO | China | Anti-vegf-anti-pd1 bispecific antibody with new-type structure | [034-989-868-512-248](https://lens.org/034-989-868-512-248) |
| 2019 | EP | China | Anti-pd-1/anti-vegf natural antibody structure-like heterodimeric form bispecific antibody and preparation thereof | [076-646-730-845-444](https://lens.org/076-646-730-845-444) |
| 2019 | CN | China | Anti-VEGF and anti-PD1 bispecific antibody with novel structure | [169-312-582-824-538](https://lens.org/169-312-582-824-538) |
| 2020 | CN | Other | Anti-PD-L1/VEGF/TGF-beta multispecific antibody and application thereof | [025-060-456-173-340](https://lens.org/025-060-456-173-340) |
| 2020 | EP | China | Anti-pd-1-anti-vegfa bispecific antibody, pharmaceutical composition and use thereof | [149-024-907-093-330](https://lens.org/149-024-907-093-330) |
| 2021 | CN | China | Anti-VEGF-anti-PD-L1 bispecific antibody as well as pharmaceutical composition and application thereof | [013-938-200-146-717](https://lens.org/013-938-200-146-717) |
| 2021 | CN | China | Bifunctional protein aiming at VEGF and TGF-beta and application of bifunctional protein | [051-587-902-928-840](https://lens.org/051-587-902-928-840) |
| 2021 | CN | China | Anti-PD-1/VEGF bispecific antibody liquid preparation | [063-425-249-565-453](https://lens.org/063-425-249-565-453) |
| 2021 | WO | China | Bifunctional fusion protein having anticancer activity | [136-629-167-747-860](https://lens.org/136-629-167-747-860) |
| 2021 | CN | China | Bispecific anti-PD-L1/VEGF antibody and application thereof | [150-018-177-029-517](https://lens.org/150-018-177-029-517) |
| 2021 | PH | China | Anti-pd-1/vegfa bifunctional antibody, pharmaceutical composition thereof and use thereof | [194-462-485-651-006](https://lens.org/194-462-485-651-006) |
| 2022 | WO | China | A bispecific anti-pd-l1/vegf antibody and uses thereof | [020-528-710-380-396](https://lens.org/020-528-710-380-396) |
| 2022 | TW | United States | Methods and compositions for treating cancer | [062-033-375-765-385](https://lens.org/062-033-375-765-385) |
| 2022 | EP | China | Pharmaceutical combination containing anti-pd-1-anti-vegfa bispecific antibody, and use thereof | [135-690-562-217-137](https://lens.org/135-690-562-217-137) |
| 2022 | CN | China | Use of antibodies in anti-tumor therapy | [189-598-565-664-95X](https://lens.org/189-598-565-664-95X) |
| 2023 | WO | China | Anti-pd-l1, vegf and egfr trispecific antibody and use thereof | [028-805-830-990-985](https://lens.org/028-805-830-990-985) |
| 2023 | WO | China | Anti-pd-l1 and vegf bispecific antibody and use thereof | [064-378-054-048-904](https://lens.org/064-378-054-048-904) |
| 2023 | WO | China | Pharmaceutical composition comprising anti-tigit antibody and anti-pd-1-anti-vegfa bispecific antibody, and use | [198-878-549-199-667](https://lens.org/198-878-549-199-667) |
| 2023 | WO | China | Pharmaceutical composition and use thereof | [198-930-667-352-795](https://lens.org/198-930-667-352-795) |
