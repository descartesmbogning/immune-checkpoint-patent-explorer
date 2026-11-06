# Verification report

Independent recomputation from `data/raw/lens_export_2024-01-28.csv.gz` (3,320 documents). **92 of 92 checks passed.**

| # | Check | Recomputed value | Where | Result |
|--:|:--|:--|:--|:--|
| 1 | Documents in the dataset | 3320 | <bound method NDFrame.where of check            Documents in the dataset
recomputed                           3320
expected text             3,320 documents
where                          manuscript
ok                                   True
Name: 0, dtype: object> | pass |
| 2 | Records removed before analysis | 3,439 → 3,378 → 3,320 | <bound method NDFrame.where of check                              Records removed before analysis
recomputed                                   3,439 → 3,378 → 3,320
expected text    returned 3,439 documents | removed 61 without ...
where                                                   manuscript
ok                                                            True
Name: 1, dtype: object> | pass |
| 3 | Application years | 1997–2023 | <bound method NDFrame.where of check            Application years
recomputed               1997–2023
expected text            1997–2023
where                   manuscript
ok                            True
Name: 2, dtype: object> | pass |
| 4 | Distinct first priority filings | 3262 | <bound method NDFrame.where of check            Distinct first priority filings
recomputed                                  3262
expected text      3,262 distinct first priority
where                                 manuscript
ok                                          True
Name: 3, dtype: object> | pass |
| 5 | Documents with a known applicant country | 3226 | <bound method NDFrame.where of check                  Documents with a known applicant country
recomputed                                                 3226
expected text    3,226 documents with a known applicant country
where                                                manuscript
ok                                                         True
Name: 4, dtype: object> | pass |
| 6 | Documents with a Chinese applicant | 1158 | <bound method NDFrame.where of check            Documents with a Chinese applicant
recomputed                                     1158
expected text         1,158 had a Chinese applicant
where                                    manuscript
ok                                             True
Name: 5, dtype: object> | pass |
| 7 | Documents with a US applicant | 1304 | <bound method NDFrame.where of check            Documents with a US applicant
recomputed                                1304
expected text             1,304 a US applicant
where                               manuscript
ok                                        True
Name: 6, dtype: object> | pass |
| 8 | Documents with both | 12 | <bound method NDFrame.where of check            Documents with both
recomputed                        12
expected text       only 12 had both
where                     manuscript
ok                              True
Name: 7, dtype: object> | pass |
| 9 | Table 1 · All documents (main) | 21.6 (16.8–27.3), 236 → 39.1 (36.2–41.9), 1,119; ratio 1.81; p <0.001 | <bound method NDFrame.where of check                               Table 1 · All documents (main)
recomputed       21.6 (16.8–27.3), 236 → 39.1 (36.2–41.9), 1,11...
expected text    | All documents (main) | 21.6 (16.8–27.3), 236...
where                                                   manuscript
ok                                                            True
Name: 8, dtype: object> | pass |
| 10 | Table 1 · Outside the Chinese office | 9.1 (5.8–14.1), 186 → 17.7 (15.1–20.7), 717; ratio 1.94; p 0.004 | <bound method NDFrame.where of check                         Table 1 · Outside the Chinese office
recomputed       9.1 (5.8–14.1), 186 → 17.7 (15.1–20.7), 717; r...
expected text    | Outside the Chinese office | 9.1 (5.8–14.1),...
where                                                   manuscript
ok                                                            True
Name: 9, dtype: object> | pass |
| 11 | Table 1 · International (PCT) filings only | 14.0 (7.3–25.3), 57 → 24.4 (19.6–30.0), 258; ratio 1.74; p 0.09 | <bound method NDFrame.where of check                   Table 1 · International (PCT) filings only
recomputed       14.0 (7.3–25.3), 57 → 24.4 (19.6–30.0), 258; r...
expected text    | International (PCT) filings only | 14.0 (7.3...
where                                                   manuscript
ok                                                            True
Name: 10, dtype: object> | pass |
| 12 | Table 1 · Known applicant country only | 22.2 (17.3–28.0), 230 → 40.3 (37.4–43.2), 1,085; ratio 1.82; p <0.001 | <bound method NDFrame.where of check                       Table 1 · Known applicant country only
recomputed       22.2 (17.3–28.0), 230 → 40.3 (37.4–43.2), 1,08...
expected text    | Known applicant country only | 22.2 (17.3–28...
where                                                   manuscript
ok                                                            True
Name: 11, dtype: object> | pass |
| 13 | Table 1 · By earliest priority year | 17.0 (13.7–20.8), 430 → 40.9 (38.0–43.9), 1,078; ratio 2.41; p <0.001 | <bound method NDFrame.where of check                          Table 1 · By earliest priority year
recomputed       17.0 (13.7–20.8), 430 → 40.9 (38.0–43.9), 1,07...
expected text    | By earliest priority year | 17.0 (13.7–20.8)...
where                                                   manuscript
ok                                                            True
Name: 12, dtype: object> | pass |
| 14 | Table 1 · Fractional counting | 21.5 → 39.9; ratio 1.85 | <bound method NDFrame.where of check                           Table 1 · Fractional counting
recomputed                            21.5 → 39.9; ratio 1.85
expected text    | Fractional counting | 21.5 | 39.9 | 1.85 |
where                                              manuscript
ok                                                       True
Name: 13, dtype: object> | pass |
| 15 | Abstract/Results · China share | 21.6 (16.8–27.3) → 39.1 (36.2–41.9) | <bound method NDFrame.where of check                               Abstract/Results · China share
recomputed                     21.6 (16.8–27.3) → 39.1 (36.2–41.9)
expected text    from 21.6% (95% CI 16.8–27.3) in 2015–16 to 39...
where                                                   manuscript
ok                                                            True
Name: 14, dtype: object> | pass |
| 16 | US share 2015–16 → 2020–21 | 50.8 (44.5–57.2) → 35.4 (32.6–38.2) | <bound method NDFrame.where of check                             US share 2015–16 → 2020–21
recomputed               50.8 (44.5–57.2) → 35.4 (32.6–38.2)
expected text    from 50.8% (44.5–57.2) to 35.4% (32.6–38.2)
where                                             manuscript
ok                                                      True
Name: 15, dtype: object> | pass |
| 17 | China vs US share in 2020 | 36.6 vs 35.2 | <bound method NDFrame.where of check            China vs US share in 2020
recomputed                    36.6 vs 35.2
expected text               36.6% vs 35.2%
where                           manuscript
ok                                    True
Name: 16, dtype: object> | pass |
| 18 | China vs US share in 2021 | 41.2 vs 35.5 | <bound method NDFrame.where of check            China vs US share in 2021
recomputed                    41.2 vs 35.5
expected text               41.2% vs 35.5%
where                           manuscript
ok                                    True
Name: 17, dtype: object> | pass |
| 19 | Documents in 2021 | 594 | <bound method NDFrame.where of check            Documents in 2021
recomputed                     594
expected text          594 in 2021
where                   manuscript
ok                            True
Name: 18, dtype: object> | pass |
| 20 | Fewer than 25 documents a year before 2013 | 11 | <bound method NDFrame.where of check            Fewer than 25 documents a year before 2013
recomputed                                               11
expected text    fewer than 25 documents a year before 2013
where                                            manuscript
ok                                                     True
Name: 19, dtype: object> | pass |
| 21 | Composition groups n | {'China': 780, 'United States': 962, 'Other countries': 589} | <bound method NDFrame.where of check                                         Composition groups n
recomputed       {'China': 780, 'United States': 962, 'Other co...
expected text                    (n = 780) | (n = 962) | (n = 589)
where                                                   manuscript
ok                                                            True
Name: 20, dtype: object> | pass |
| 22 | Table 2 · China column | 70.1 (66.8–73.2); 13.5 (11.2–16.0); 6.5 (5.0–8.5); 9.9 (8.0–12.2); 31.8 (28.6–35.1); 2 (1–4); 36.4 | <bound method NDFrame.where of check                                       Table 2 · China column
recomputed       70.1 (66.8–73.2); 13.5 (11.2–16.0); 6.5 (5.0–8...
expected text    70.1 (66.8–73.2) | 13.5 (11.2–16.0) | 6.5 (5.0...
where                                                   manuscript
ok                                                            True
Name: 21, dtype: object> | pass |
| 23 | Table 2 · United States column | 8.9 (7.3–10.9); 26.9 (24.2–29.8); 35.1 (32.2–38.2); 29.0 (26.2–31.9); 12.5 (10.5–14.7); 7 (3–13); 18.0 | <bound method NDFrame.where of check                               Table 2 · United States column
recomputed       8.9 (7.3–10.9); 26.9 (24.2–29.8); 35.1 (32.2–3...
expected text    8.9 (7.3–10.9) | 26.9 (24.2–29.8) | 35.1 (32.2...
where                                                   manuscript
ok                                                            True
Name: 22, dtype: object> | pass |
| 24 | Table 2 · Other countries column | 11.0 (8.8–13.8); 25.0 (21.6–28.6); 22.2 (19.1–25.8); 41.8 (37.8–45.8); 16.3 (13.5–19.5); 6 (2–13); 20.4 | <bound method NDFrame.where of check                             Table 2 · Other countries column
recomputed       11.0 (8.8–13.8); 25.0 (21.6–28.6); 22.2 (19.1–...
expected text    11.0 (8.8–13.8) | 25.0 (21.6–28.6) | 22.2 (19....
where                                                   manuscript
ok                                                            True
Name: 23, dtype: object> | pass |
| 25 | Family of one, China vs US, p | <0.001 | <bound method NDFrame.where of check                Family of one, China vs US, p
recomputed                                  <0.001
expected text    12.5% of US documents (p < 0.001)
where                                   manuscript
ok                                            True
Name: 24, dtype: object> | pass |
| 26 | Grant rate in CN office (2010–21) | 36.8 | <bound method NDFrame.where of check            Grant rate in CN office (2010–21)
recomputed                                    36.8
expected text                               (36.8%
where                                   manuscript
ok                                            True
Name: 25, dtype: object> | pass |
| 27 | Grant rate in US office (2010–21) | 34.8 | <bound method NDFrame.where of check            Grant rate in US office (2010–21)
recomputed                                    34.8
expected text                               34.8%)
where                                   manuscript
ok                                            True
Name: 26, dtype: object> | pass |
| 28 | Table S4 · PD-1 | 55.5 vs 42.9 | <bound method NDFrame.where of check                                              Table S4 · PD-1
recomputed                                            55.5 vs 42.9
expected text    | PD-1 | 55.5 (52.0–59.0) | 42.9 (39.8–46.1) |...
where                                                   supplement
ok                                                            True
Name: 27, dtype: object> | pass |
| 29 | Results · PD-1 | 55.5 vs 42.9 | <bound method NDFrame.where of check            Results · PD-1
recomputed         55.5 vs 42.9
expected text    55.5% vs 42.9%
where                manuscript
ok                         True
Name: 28, dtype: object> | pass |
| 30 | Table S4 · PD-L1 | 44.6 vs 30.5 | <bound method NDFrame.where of check                                             Table S4 · PD-L1
recomputed                                            44.6 vs 30.5
expected text    | PD-L1 | 44.6 (41.2–48.1) | 30.5 (27.6–33.4) ...
where                                                   supplement
ok                                                            True
Name: 29, dtype: object> | pass |
| 31 | Results · PD-L1 | 44.6 vs 30.5 | <bound method NDFrame.where of check            Results · PD-L1
recomputed          44.6 vs 30.5
expected text     44.6% vs 30.5%
where                 manuscript
ok                          True
Name: 30, dtype: object> | pass |
| 32 | Table S4 · CTLA-4 | 8.7 vs 14.6 | <bound method NDFrame.where of check                                            Table S4 · CTLA-4
recomputed                                             8.7 vs 14.6
expected text    | CTLA-4 | 8.7 (6.9–10.9) | 14.6 (12.5–16.9) |...
where                                                   supplement
ok                                                            True
Name: 31, dtype: object> | pass |
| 33 | Results · CTLA-4 | 8.7 vs 14.6 | <bound method NDFrame.where of check            Results · CTLA-4
recomputed            8.7 vs 14.6
expected text       14.6% vs 8.7%
where                  manuscript
ok                           True
Name: 32, dtype: object> | pass |
| 34 | Table S4 · LAG-3, TIM-3 or TIGIT | 2.6 vs 4.7 | <bound method NDFrame.where of check                             Table S4 · LAG-3, TIM-3 or TIGIT
recomputed                                              2.6 vs 4.7
expected text    | LAG-3, TIM-3 or TIGIT | 2.6 (1.7–3.9) | 4.7 ...
where                                                   supplement
ok                                                            True
Name: 33, dtype: object> | pass |
| 35 | Results · newer targets | 2.6 vs 4.7 | <bound method NDFrame.where of check                             Results · newer targets
recomputed                                     2.6 vs 4.7
expected text    2.6% of Chinese and 4.7% of US documents
where                                          manuscript
ok                                                   True
Name: 34, dtype: object> | pass |
| 36 | Table S4 · Combination therapy | 33.5 vs 53.8 | <bound method NDFrame.where of check                               Table S4 · Combination therapy
recomputed                                            33.5 vs 53.8
expected text    | Combination therapy | 33.5 (30.2–36.8) | 53....
where                                                   supplement
ok                                                            True
Name: 35, dtype: object> | pass |
| 37 | Results · Combination therapy | 33.5 vs 53.8 | <bound method NDFrame.where of check            Results · Combination therapy
recomputed                        33.5 vs 53.8
expected text                   53.8% vs 33.5%
where                               manuscript
ok                                        True
Name: 36, dtype: object> | pass |
| 38 | Combination difference | 20.4 | <bound method NDFrame.where of check            Combination difference
recomputed                         20.4
expected text    difference 20.4 points
where                        manuscript
ok                                 True
Name: 37, dtype: object> | pass |
| 39 | Table S4 · Bispecific / multispecific | 10.6 vs 4.2 | <bound method NDFrame.where of check                        Table S4 · Bispecific / multispecific
recomputed                                             10.6 vs 4.2
expected text    | Bispecific / multispecific | 10.6 (8.7–13.0)...
where                                                   supplement
ok                                                            True
Name: 38, dtype: object> | pass |
| 40 | Results · Bispecific / multispecific | 10.6 vs 4.2 | <bound method NDFrame.where of check            Results · Bispecific / multispecific
recomputed                                10.6 vs 4.2
expected text                           10.6% vs 4.2%
where                                      manuscript
ok                                               True
Name: 39, dtype: object> | pass |
| 41 | Table S4 · Biomarker / diagnostic | 10.0 vs 7.9 | <bound method NDFrame.where of check                            Table S4 · Biomarker / diagnostic
recomputed                                             10.0 vs 7.9
expected text    | Biomarker / diagnostic | 10.0 (8.1–12.3) | 7...
where                                                   supplement
ok                                                            True
Name: 40, dtype: object> | pass |
| 42 | Table S4 · Cell therapy | 2.8 vs 4.0 | <bound method NDFrame.where of check                                      Table S4 · Cell therapy
recomputed                                              2.8 vs 4.0
expected text    | Cell therapy | 2.8 (1.9–4.2) | 4.0 (2.9–5.4)...
where                                                   supplement
ok                                                            True
Name: 41, dtype: object> | pass |
| 43 | Table S4 · Formulation / delivery | 3.6 vs 6.2 | <bound method NDFrame.where of check                            Table S4 · Formulation / delivery
recomputed                                              3.6 vs 6.2
expected text    | Formulation / delivery | 3.6 (2.5–5.1) | 6.2...
where                                                   supplement
ok                                                            True
Name: 42, dtype: object> | pass |
| 44 | Results · Formulation / delivery | 3.6 vs 6.2 | <bound method NDFrame.where of check            Results · Formulation / delivery
recomputed                             3.6 vs 6.2
expected text                        6.2% vs 3.6%
where                                  manuscript
ok                                           True
Name: 43, dtype: object> | pass |
| 45 | Table S4 · Small molecule | 6.5 vs 2.7 | <bound method NDFrame.where of check                                    Table S4 · Small molecule
recomputed                                              6.5 vs 2.7
expected text    | Small molecule | 6.5 (5.0–8.5) | 2.7 (1.9–3....
where                                                   supplement
ok                                                            True
Name: 44, dtype: object> | pass |
| 46 | Results · Small molecule | 6.5 vs 2.7 | <bound method NDFrame.where of check            Results · Small molecule
recomputed                     6.5 vs 2.7
expected text                6.5% vs 2.7%
where                          manuscript
ok                                   True
Name: 45, dtype: object> | pass |
| 47 | Cite research papers | 54.2 vs 42.8 | <bound method NDFrame.where of check            Cite research papers
recomputed               54.2 vs 42.8
expected text        (54.2% vs 42.8%)
where                      manuscript
ok                               True
Name: 46, dtype: object> | pass |
| 48 | PD-(L)1 × VEGF bispecifics | 21 documents, 19 Chinese, 1 US, from 2019 | <bound method NDFrame.where of check                                   PD-(L)1 × VEGF bispecifics
recomputed               21 documents, 19 Chinese, 1 US, from 2019
expected text    Of the 21 documents in this class, 19 had a Ch...
where                                                   manuscript
ok                                                            True
Name: 47, dtype: object> | pass |
| 49 | Top-10 concentration · China | 20.5 | <bound method NDFrame.where of check            Top-10 concentration · China
recomputed                               20.5
expected text                           20.5%
where                              manuscript
ok                                       True
Name: 48, dtype: object> | pass |
| 50 | Leading applicants · China | Jiangsu Hengrui Medicine Co. Ltd. (32), Chia Tai Tianqing Pharmaceutical Group Co. Ltd. (23), Innovent Biologics (Suzhou) Co. Ltd. (16), Suzhou Shengdiya Biological Medicine Co. Ltd. (15) | <bound method NDFrame.where of check                                   Leading applicants · China
recomputed       Jiangsu Hengrui Medicine Co. Ltd. (32), Chia T...
expected text                                see Results paragraph
where                                                   manuscript
ok                                                            True
Name: 49, dtype: object> | pass |
| 51 | Top-10 concentration · United States | 33.8 | <bound method NDFrame.where of check            Top-10 concentration · United States
recomputed                                       33.8
expected text                                   33.8%
where                                      manuscript
ok                                               True
Name: 50, dtype: object> | pass |
| 52 | Leading applicants · United States | Bristol Myers Squibb Co. (78), Genentech Inc. (40), Merck Sharp & Dohme Corp. (38), University of Texas (37) | <bound method NDFrame.where of check                           Leading applicants · United States
recomputed       Bristol Myers Squibb Co. (78), Genentech Inc. ...
expected text                                see Results paragraph
where                                                   manuscript
ok                                                            True
Name: 51, dtype: object> | pass |
| 53 | Leading applicant counts | Hengrui 32, CTTQ 23, Innovent 16, Shengdiya 15; BMS 78, Genentech 40, MSD 38 | <bound method NDFrame.where of check                                     Leading applicant counts
recomputed       Hengrui 32, CTTQ 23, Innovent 16, Shengdiya 15...
expected text    Jiangsu Hengrui Medicine (32 documents) | Chia...
where                                                   manuscript
ok                                                            True
Name: 52, dtype: object> | pass |
| 54 | results.json · n documents | 3320 | <bound method NDFrame.where of check            results.json · n documents
recomputed                             3320
expected text             output file: 3320
where                               outputs
ok                                     True
Name: 53, dtype: object> | pass |
| 55 | results.json · China share 2020–21 | 39.1 | <bound method NDFrame.where of check            results.json · China share 2020–21
recomputed                                     39.1
expected text                     output file: 39.1
where                                       outputs
ok                                             True
Name: 54, dtype: object> | pass |
| 56 | results.json · PD-1×VEGF n | 21 | <bound method NDFrame.where of check            results.json · PD-1×VEGF n
recomputed                               21
expected text               output file: 21
where                               outputs
ok                                     True
Name: 55, dtype: object> | pass |
| 57 | table1 csv · All documents (main) | 39.1 | <bound method NDFrame.where of check            table1 csv · All documents (main)
recomputed                                    39.1
expected text                    output file: 39.1
where                                      outputs
ok                                            True
Name: 56, dtype: object> | pass |
| 58 | table1 csv · Outside the Chinese office | 17.7 | <bound method NDFrame.where of check            table1 csv · Outside the Chinese office
recomputed                                          17.7
expected text                          output file: 17.7
where                                            outputs
ok                                                  True
Name: 57, dtype: object> | pass |
| 59 | table1 csv · International (PCT) filings only | 24.4 | <bound method NDFrame.where of check            table1 csv · International (PCT) filings only
recomputed                                                24.4
expected text                                output file: 24.4
where                                                  outputs
ok                                                        True
Name: 58, dtype: object> | pass |
| 60 | table1 csv · Known applicant country only | 40.3 | <bound method NDFrame.where of check            table1 csv · Known applicant country only
recomputed                                            40.3
expected text                            output file: 40.3
where                                              outputs
ok                                                    True
Name: 59, dtype: object> | pass |
| 61 | table1 csv · By earliest priority year | 40.9 | <bound method NDFrame.where of check            table1 csv · By earliest priority year
recomputed                                         40.9
expected text                         output file: 40.9
where                                           outputs
ok                                                 True
Name: 60, dtype: object> | pass |
| 62 | table3 csv · combination, China | 33.5 | <bound method NDFrame.where of check            table3 csv · combination, China
recomputed                                  33.5
expected text                  output file: 33.5
where                                    outputs
ok                                          True
Name: 61, dtype: object> | pass |
| 63 | Figure 1 data · China 2020 | 36.57 | <bound method NDFrame.where of check            Figure 1 data · China 2020
recomputed                            36.57
expected text            output file: 36.57
where                               outputs
ok                                     True
Name: 62, dtype: object> | pass |
| 64 | Figure 1 data · US 2020 | 35.24 | <bound method NDFrame.where of check            Figure 1 data · US 2020
recomputed                         35.24
expected text         output file: 35.24
where                            outputs
ok                                  True
Name: 63, dtype: object> | pass |
| 65 | Figure 1 data · China 2021 | 41.25 | <bound method NDFrame.where of check            Figure 1 data · China 2021
recomputed                            41.25
expected text            output file: 41.25
where                               outputs
ok                                     True
Name: 64, dtype: object> | pass |
| 66 | Figure 1 data · US 2021 | 35.52 | <bound method NDFrame.where of check            Figure 1 data · US 2021
recomputed                         35.52
expected text         output file: 35.52
where                            outputs
ok                                  True
Name: 65, dtype: object> | pass |
| 67 | Figure 2 data · China in CN office | 70.1 | <bound method NDFrame.where of check            Figure 2 data · China in CN office
recomputed                                     70.1
expected text                     output file: 70.1
where                                       outputs
ok                                             True
Name: 66, dtype: object> | pass |
| 68 | Table S3 · PD-1 · All | kappa 0.99 | <bound method NDFrame.where of check                                        Table S3 · PD-1 · All
recomputed                                              kappa 0.99
expected text    | PD-1 | All (n = 200) | 101 | 100 | 99.5 | 10...
where                                                   supplement
ok                                                            True
Name: 67, dtype: object> | pass |
| 69 | Table S3 · PD-1 · China | kappa 1.00 | <bound method NDFrame.where of check                                      Table S3 · PD-1 · China
recomputed                                              kappa 1.00
expected text    | PD-1 | China (n = 100) | 56 | 56 | 100.0 | 1...
where                                                   supplement
ok                                                            True
Name: 68, dtype: object> | pass |
| 70 | Table S3 · PD-1 · US | kappa 0.98 | <bound method NDFrame.where of check                                         Table S3 · PD-1 · US
recomputed                                              kappa 0.98
expected text    | PD-1 | US (n = 100) | 45 | 44 | 99.0 | 100.0...
where                                                   supplement
ok                                                            True
Name: 69, dtype: object> | pass |
| 71 | Table S3 · PD-L1 · All | kappa 0.99 | <bound method NDFrame.where of check                                       Table S3 · PD-L1 · All
recomputed                                              kappa 0.99
expected text    | PD-L1 | All (n = 200) | 57 | 58 | 99.5 | 98....
where                                                   supplement
ok                                                            True
Name: 70, dtype: object> | pass |
| 72 | Table S3 · PD-L1 · China | kappa 1.00 | <bound method NDFrame.where of check                                     Table S3 · PD-L1 · China
recomputed                                              kappa 1.00
expected text    | PD-L1 | China (n = 100) | 35 | 35 | 100.0 | ...
where                                                   supplement
ok                                                            True
Name: 71, dtype: object> | pass |
| 73 | Table S3 · PD-L1 · US | kappa 0.97 | <bound method NDFrame.where of check                                        Table S3 · PD-L1 · US
recomputed                                              kappa 0.97
expected text    | PD-L1 | US (n = 100) | 22 | 23 | 99.0 | 95.7...
where                                                   supplement
ok                                                            True
Name: 72, dtype: object> | pass |
| 74 | Table S3 · CTLA-4 · All | kappa 1.00 | <bound method NDFrame.where of check                                      Table S3 · CTLA-4 · All
recomputed                                              kappa 1.00
expected text    | CTLA-4 | All (n = 200) | 28 | 28 | 100.0 | 1...
where                                                   supplement
ok                                                            True
Name: 73, dtype: object> | pass |
| 75 | Table S3 · CTLA-4 · China | kappa 1.00 | <bound method NDFrame.where of check                                    Table S3 · CTLA-4 · China
recomputed                                              kappa 1.00
expected text    | CTLA-4 | China (n = 100) | 14 | 14 | 100.0 |...
where                                                   supplement
ok                                                            True
Name: 74, dtype: object> | pass |
| 76 | Table S3 · CTLA-4 · US | kappa 1.00 | <bound method NDFrame.where of check                                       Table S3 · CTLA-4 · US
recomputed                                              kappa 1.00
expected text    | CTLA-4 | US (n = 100) | 14 | 14 | 100.0 | 10...
where                                                   supplement
ok                                                            True
Name: 75, dtype: object> | pass |
| 77 | Table S3 · LAG-3 / TIM-3 / TIGIT · All | kappa 0.92 | <bound method NDFrame.where of check                       Table S3 · LAG-3 / TIM-3 / TIGIT · All
recomputed                                              kappa 0.92
expected text    | LAG-3 / TIM-3 / TIGIT | All (n = 200) | 6 | ...
where                                                   supplement
ok                                                            True
Name: 76, dtype: object> | pass |
| 78 | Table S3 · LAG-3 / TIM-3 / TIGIT · China | kappa 1.00 | <bound method NDFrame.where of check                     Table S3 · LAG-3 / TIM-3 / TIGIT · China
recomputed                                              kappa 1.00
expected text    | LAG-3 / TIM-3 / TIGIT | China (n = 100) | 2 ...
where                                                   supplement
ok                                                            True
Name: 77, dtype: object> | pass |
| 79 | Table S3 · LAG-3 / TIM-3 / TIGIT · US | kappa 0.88 | <bound method NDFrame.where of check                        Table S3 · LAG-3 / TIM-3 / TIGIT · US
recomputed                                              kappa 0.88
expected text    | LAG-3 / TIM-3 / TIGIT | US (n = 100) | 4 | 5...
where                                                   supplement
ok                                                            True
Name: 78, dtype: object> | pass |
| 80 | Table S3 · Combination therapy · All | kappa 0.94 | <bound method NDFrame.where of check                         Table S3 · Combination therapy · All
recomputed                                              kappa 0.94
expected text    | Combination therapy | All (n = 200) | 93 | 9...
where                                                   supplement
ok                                                            True
Name: 79, dtype: object> | pass |
| 81 | Table S3 · Combination therapy · China | kappa 0.89 | <bound method NDFrame.where of check                       Table S3 · Combination therapy · China
recomputed                                              kappa 0.89
expected text    | Combination therapy | China (n = 100) | 35 |...
where                                                   supplement
ok                                                            True
Name: 80, dtype: object> | pass |
| 82 | Table S3 · Combination therapy · US | kappa 0.98 | <bound method NDFrame.where of check                          Table S3 · Combination therapy · US
recomputed                                              kappa 0.98
expected text    | Combination therapy | US (n = 100) | 58 | 59...
where                                                   supplement
ok                                                            True
Name: 81, dtype: object> | pass |
| 83 | Table S3 · Bispecific / multispecific · All | kappa 0.97 | <bound method NDFrame.where of check                  Table S3 · Bispecific / multispecific · All
recomputed                                              kappa 0.97
expected text    | Bispecific / multispecific | All (n = 200) |...
where                                                   supplement
ok                                                            True
Name: 82, dtype: object> | pass |
| 84 | Table S3 · Bispecific / multispecific · China | kappa 1.00 | <bound method NDFrame.where of check                Table S3 · Bispecific / multispecific · China
recomputed                                              kappa 1.00
expected text    | Bispecific / multispecific | China (n = 100)...
where                                                   supplement
ok                                                            True
Name: 83, dtype: object> | pass |
| 85 | Table S3 · Bispecific / multispecific · US | kappa 0.92 | <bound method NDFrame.where of check                   Table S3 · Bispecific / multispecific · US
recomputed                                              kappa 0.92
expected text    | Bispecific / multispecific | US (n = 100) | ...
where                                                   supplement
ok                                                            True
Name: 84, dtype: object> | pass |
| 86 | Dashboard · documents | 3320 | <bound method NDFrame.where of check            Dashboard · documents
recomputed                        3320
expected text        output file: 3320
where                          outputs
ok                                True
Name: 85, dtype: object> | pass |
| 87 | Dashboard · China share 2020–21 (KPI) | 39.1 | <bound method NDFrame.where of check            Dashboard · China share 2020–21 (KPI)
recomputed                                        39.1
expected text                        output file: 39.1
where                                          outputs
ok                                                True
Name: 86, dtype: object> | pass |
| 88 | Dashboard · China share 2015–16 (KPI note) | 21.6 | <bound method NDFrame.where of check            Dashboard · China share 2015–16 (KPI note)
recomputed                                             21.6
expected text                             output file: 21.6
where                                               outputs
ok                                                     True
Name: 87, dtype: object> | pass |
| 89 | Dashboard · combination share, China 2010–21 | 33.5 | <bound method NDFrame.where of check            Dashboard · combination share, China 2010–21
recomputed                                               33.5
expected text                               output file: 33.5
where                                                 outputs
ok                                                       True
Name: 88, dtype: object> | pass |
| 90 | Dashboard · documents in default view (2010–2023) | 3280 | <bound method NDFrame.where of check            Dashboard · documents in default view (2010–2023)
recomputed                                                    3280
expected text                                    output file: 3280
where                                                      outputs
ok                                                            True
Name: 89, dtype: object> | pass |
| 91 | Dashboard headline 'Nearly half of the documents cite research papers' | 45.4% | <bound method NDFrame.where of check            Dashboard headline 'Nearly half of the documen...
recomputed                                                   45.4%
expected text                                               40–50%
where                                                    dashboard
ok                                                            True
Name: 90, dtype: object> | pass |
| 92 | Dashboard headline 'China, the PCT route and the US receive most filings' | CN, WO, US | <bound method NDFrame.where of check            Dashboard headline 'China, the PCT route and t...
recomputed                                              CN, WO, US
expected text                                           CN, WO, US
where                                                    dashboard
ok                                                            True
Name: 91, dtype: object> | pass |
