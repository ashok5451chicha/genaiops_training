# Inconsistency log

Found by running everything first (`evidence/00_before_*`), then fixing one thing at a time and re-running after
each fix (`evidence/01_` … `07_`, final run `evidence/10_final_*`). Several problems only became visible after an
earlier one was fixed. For example, the duplicate-ID and threshold problems could only be seen once `dot()`, `norm()`
and `classify_note()` worked.

| # | File and line or field | What you observed | What it should be | How you found it | Fixed? |
|---|---|---|---|---|---|
| 1 | `vector_math.py` `norm()` | Returns the **sum of squares** (`norm([3,4])` = 25) | Square root of the sum of squares (= 5), as the docstring and the brief say | `test_norm` failed; `check_by_hand.py` lengths | Fixed |
| 2 | `vector_math.py` `euclidean_distance()` | Sums **absolute** differences: Manhattan distance, `[0,0]`→`[1,1]` = 2 | sqrt of the sum of **squared** differences (= 1.414) | `test_euclidean_345`, `test_euclidean_is_not_manhattan` failed | Fixed |
| 3 | `vector_math.py` `cosine_similarity()` | A zero vector raises `ZeroDivisionError` | `ValueError` ("no direction"), as the test TODO and `normalize()` require | Reading the TODO in `tests/test_vector_math.py`; new test `test_zero_vector_is_an_error` | Fixed |
| 4 | `vector_math.py` docstring vs README "Rules" | Docstring: cosine is −1 … 1. README: "always between 0 and 1" | Both are true in context: −1 … 1 in general, 0 … 1 here because every embedder value is ≥ 0 | Reading docstrings vs README | Explained; docstring now says both |
| 5 | `tests/test_vector_math.py` `test_cosine_known_value` | Expects cosine([1,0],[1,1]) = **0.5** | 1 / (1 × √2) = **0.7071**. The test was wrong, not the code | Test still failed after the maths was right; worked by hand | Fixed (test) |
| 6 | `data/hand_vectors.json` R | R = [4, 3, 0, **1**] | [4, 3, 0, **0**], as in `by_hand/worksheet.md` and the docstring example (cosine 0.96, distance 1.414) | `check_by_hand.py`: 3 answers DIFFERENT (5.099 / 0.941 / 1.732). The paper answers were right; the data was wrong | Fixed (data) |
| 7 | `embedder.py` `tokenize()` | Does not lower-case: "Passport EXPIRED" ≠ "passport expired" | Lower-case first, as its docstring says | `test_case_does_not_matter` failed | Fixed |
| 8 | `embedder.py` module docstring | Says names fall into **32** hashed buckets | The code uses `BUCKETS = 16` | Reading docstring vs code | Fixed the docstring. The code is kept at 16: changing it would change every score the thresholds were set on |
| 9 | `data/concepts.json` `id_document` | Contains `"proof-of-identity"`, which can never match: the tokenizer splits on `-` | Single words only | Checked every lexicon entry against `tokenize()` | Fixed (removed; "identity" already covers it) |
| 10 | `kyc_pipeline.py` `classify_note()` | Uses `min()`, so the **least** similar category won: every note went to MANUAL_REVIEW, **1/20** correct | `max()`, "highest cosine wins" (docstring, architecture diagram) | First full pipeline run (`evidence/03_after_mask_fix.txt`) | Fixed: **20/20** |
| 11 | `kyc_pipeline.py` `find_duplicates()` | Inner loop `range(i, …)` compared every record **with itself**: 20 fake "probable duplicates" at cosine 1.0, precision 0.095 | `range(i + 1, …)`: every pair once, i < j (docstring, diagram) | Pipeline output (`evidence/04_after_classify_fix.txt`) | Fixed: precision **1.0** |
| 12 | `kyc_pipeline.py` `build_queue()` | Column `masked_id` held the **raw** `id_number`. The README rule "IDs are masked in every output" was stated but not enforced | `mask_id(id_number, cfg["mask_visible_chars"])` | The privacy guard added to `run_pipeline.py` stopped the first run: "17 raw ID number(s) would appear" (`evidence/02_first_pipeline_run.txt`) | Fixed; guard kept |
| 13 | `config.json` `review_cosine` | **0.9**: higher than `duplicate_cosine` (0.85), so "possible" could never happen, and it contradicts the README, the diagram and the function default (0.70). Known duplicate K002/K019 (cosine 0.825) was hidden from humans | **0.70**, as documented. Thresholds belong to the process owner; this restores the documented decision, it does not invent a new one | Pipeline: duplicate recall 0.667, then scored K002/K019 by hand | Fixed: recall incl. possible **1.0** |
| 14 | `data/kyc_records.json` | Two records with `record_id` **K013** (CUST-1013 and CUST-1014). K014 is missing | Second one is **K014** (its customer_ref CUST-1014 confirms) | Reading the records; the duplicate list showed "K011–K013" and nobody could tell which K013 | Fixed |
| 15 | `data/kyc_records.json` K009 `last_review` | `"27/05/2025"` (DD/MM/YYYY) | `"2025-05-27"`: every other record uses ISO dates | Reading the records; `test_dates_are_iso_and_not_in_the_future` | Fixed |
| 16 | `data/kyc_records.json` K011 `status` | `"ACTIVE"` | `"active"`: every other record is lower case | Reading the records; `test_status_values` | Fixed |
| 17 | `why_cosine.py` experiments 1 and 4 | Printed "P=[3,4] and Q=[6,8]" although the vectors have four numbers | Print the real vectors | Comparing the output with `hand_vectors.json` | Fixed (prints the data) |
| 18 | `data/concepts.json` | "photo" is in both `id_document` and `photo_quality` | Allowed: a blurry ID photo is both an ID problem and a quality problem, and the embedder supports a word in several concepts | Checked every lexicon word for duplicates | Explained, not changed |
| 19 | `README.md` "Run it", step 2 | "everything should pass". In the starter, 11 of 14 tests failed or errored | True only after the fixes | First run (`evidence/00_before_tests.txt`) | Explained (true now: 46/46) |
| 20 | `tests/` | `test_pipeline.py` missing; zero-vector test only a TODO | Written (missing piece M6) | README / MISSING_PIECES | Fixed |

Not an inconsistency, but worth knowing: masked IDs are not unique (K008 `SYNID-**456` and K013 `SYNID-**456`).
Refer to records by `record_id`, never by the masked ID.
