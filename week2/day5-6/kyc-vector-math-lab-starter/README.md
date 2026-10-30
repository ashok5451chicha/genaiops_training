# KYC Remediation: Vector Mathematics in Practice (Days 5 and 6) - STARTER PACKAGE

A small, end-to-end KYC remediation helper built on three ideas: **dot product**, **cosine similarity** and
**Euclidean distance**. It sorts free-text analyst notes into remediation categories and spots probable duplicate customer
profiles, and it never merges or decides on its own. Standard library only, no API key, synthetic data only.

```
data/kyc_records.json            20 synthetic KYC records (names, addresses, analyst notes, masked-on-output IDs)
data/remediation_categories.json 5 categories with a description, priority and action
data/concepts.json               the small word-to-concept lexicon our toy embedder uses
data/hand_vectors.json           four tiny vectors for the by-hand worksheet
data/gold_duplicates.json        the known duplicate pairs (used only to measure quality)
config.json                      thresholds (see "Decisions" below)
vector_math.py                   dot, norm, normalize, cosine_similarity, euclidean_distance
embedder.py                      text -> vector
kyc_pipeline.py                  classify notes, find duplicates, mask IDs, evaluate
run_pipeline.py                  the end-to-end run, writes output/
by_hand/worksheet.md             6 exercises to do on paper first
check_by_hand.py                 compares your paper answers with the code
why_cosine.py                    four experiments: direction vs size, short vs long, the distance link
tests/                           unit tests
```

## Run it
1. `python --version` (3.9 or newer). Open the folder in VS Code and open a terminal here.
2. `python -m unittest discover -s tests` (everything should pass)
3. Do `by_hand/worksheet.md` on paper, fill `by_hand/my_answers.json`, then `python check_by_hand.py`
4. `python why_cosine.py`
5. `python run_pipeline.py`  (writes `output/remediation_queue.csv`, `output/duplicate_pairs.csv`, `output/summary.md`)

## Decisions (all in config.json, owned by the process owner, not by the code)
* `duplicate_cosine` 0.85: at or above this a pair is a PROBABLE duplicate. `review_cosine` 0.70: at or above this, POSSIBLE.
  Both go to a human. Nothing is ever merged automatically.
* `min_note_score` 0.30: a note whose best category scores below this goes to a person.
* `mask_visible_chars` 3: IDs are masked in every output.

## Rules
* Synthetic data only. Never put real customer or bank data in any file or prompt.
* No `.env`, keys or secrets in this repository (none are needed).
* Cosine similarity is always between 0 and 1.
* The toy embedder is for learning. A real embedding model replaces `embedder.py`; the maths and the pipeline stay the same.

## About this starter package
This copy is **not finished and not fully correct**. Your job on Days 5 and 6:
1. Run everything and **observe** what happens (tests, `check_by_hand.py`, `why_cosine.py`, `run_pipeline.py`).
2. **List every inconsistency** you can find in `inconsistency_log.md` (code vs documentation, data vs data, test vs maths).
3. **Write the missing pieces** (search for `TODO (missing piece`) with Claude Code, and fix each inconsistency.
4. Prove it works end to end with `python run_pipeline.py` and passing tests, then push to GitLab.

---

## Days 5–6: what I changed (status: finished)

**Result.** `python -m unittest discover -s tests` → **46 tests OK** (14 in the starter, 11 of them failing or
erroring). `python check_by_hand.py` → all 9 answers match. `python run_pipeline.py` runs end to end and writes the
three files. No raw ID appears on screen or in any output, and the run refuses to finish if one would.

| | Starter (first full run) | Now |
|---|---|---|
| Notes classified correctly | 1/20 | **20/20** |
| Probable-duplicate precision | 0.095 (20 records "duplicated" with themselves) | **1.0** |
| Known duplicates reaching a human (probable + possible) | 2/3 | **3/3** |
| Raw IDs in the queue | yes (17) | **none** |

**Missing pieces written:** M1 `dot()`, M2 `normalize()`, M3 `mask_id()`, M4 `write_csv()`, M5
`run_pipeline.main()` (two tables, three files, plus a privacy guard that deletes the outputs and stops if a raw ID
would leak), M6 `tests/test_pipeline.py` (30 tests: masking, classification, duplicates, end-to-end quality, data
hygiene), plus the zero-vector test.

**Inconsistencies:** 20 found, 17 fixed and 3 explained. See `inconsistency_log.md`. The main ones were `norm()`
without the square root, Euclidean distance that was really Manhattan, `min()` instead of `max()` in classification,
records compared with themselves, raw IDs in the "masked" column, `review_cosine` 0.9 contradicting the documented
0.70, a duplicated record ID (K013), and a test whose expected value (0.5) was mathematically wrong (0.7071).

**Thresholds:** only `review_cosine` changed, from 0.9 back to the documented 0.70 (#13). It is the process owner's
decision; I restored the documented value, I did not choose a new one.

**Evidence:** `evidence/` holds the output of every run, before, during (one fix at a time) and after.
`output/` is git-ignored, as the brief requires; re-create it with `python run_pipeline.py`.

**Bug in my own code, caught by my own test:** the first version of M5 crashed when the output folder was outside the
project (`Path.relative_to`). `test_run_pipeline_writes_three_files_without_raw_ids` found it, and it is fixed.

### One limitation of the toy embedder

Words that are not in the 12-concept lexicon fall into only **16 hashed buckets**, so unrelated words collide. Profile
vectors (name + address + occupation) are mostly made of such words, so different people can look alike. Four of the
five POSSIBLE pairs are not duplicates (for example K005/K015, two retired people, 0.77). They go to a human,
so nothing breaks, but it is review work. The real duplicates also share the same `id_number`, a much stronger signal
than cosine, which this vector-only design ignores. A real embedding model would replace `embedder.py` (the maths and
pipeline stay the same), and an exact-ID check could be added before the cosine step.
