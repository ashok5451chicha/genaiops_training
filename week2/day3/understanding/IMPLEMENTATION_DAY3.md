# Day 3 – how it was implemented

Repository: `https://github.com/digibhatia/cosine-vector-mathematics`, cloned to `training/week2/day3`. **Nothing
committed or pushed.** No API key is needed or used in this lab. Write-up: `docs/Day3_Writeup.md` / `.pdf`.

## Files

| File | New / changed | Purpose |
|---|---|---|
| `my_vector_math.py` | changed | Step 2: `dot`, `norm`, `cosine_similarity`, `euclidean_distance` (standard library, a comment per line, written without opening the answer key). Task B: `nearest()`, version 2 |
| `test_mine.py` | new | 12 unittest tests: 5 for the four functions (Prompt 4), 7 for `nearest()` |
| `taskE_and_stretch.py` | new | Task E misleading-similarity pairs; stretch: unit-vector identity, `centroid()`, sensitivity table |
| `data/my_scenario.json` | new | Task C: KYC document remediation, 6 items × 4 dimensions |
| `tests/test_vector_math.py` | changed | `test_stub_reports_todo` patches in a stub, instead of failing once the participant has written their functions |
| `STEP1_HAND_WORKING.md`, `STEP4_NOTES.md` | new | Guided-lab working and notes |
| `docs/TaskA_hand_working.md`, `TaskB_prompt_log.md`, `TaskC_scenario.md`, `Day3_Writeup.md` | new | Assignment write-up |
| `outputs/*.txt` | new | Output of every run |

## Results

* Step 1: 12/12 · Step 3: 4/4 PASS (before and after adding `nearest`) · repo tests 16/16 · `test_mine.py` 12/12.
* Task B found a real defect in the first `nearest()` (silent euclidean fall-through for unknown metrics) and one wrong
  expectation in my own test. Both are recorded in the prompt log.

## Decisions taken

* Task C use case: **#1 KYC document remediation**, because it is the most banking-specific and fits four clear
  dimensions.
* Zero vectors and different lengths raise `ValueError` (as the lab requires); `nearest()` names the failing
  candidate rather than skipping it silently.
* Ties in `nearest()` keep input order (Python's stable sort), and a test pins this.

## Noticed, not changed

* The repo's `.gitignore` contains a PowerShell command that was pasted in by accident (`@" … "@ | Add-Content
  .gitignore`). The ignore lines inside it still work (`.env`, `.venv/`, `__pycache__/`, `*.pyc`), so it is harmless.
* The assignment outline and the participant guide are in the repository twice (root and `docs/`); the copies are
  identical.

## Needs you

* Task A asks for a **photo or scan of handwritten working**: copy `docs/TaskA_hand_working.md` by hand.
* Task E's own-work example is a GenAI-operations case (a RAG assistant retrieving an old policy clause with the
  opposite meaning). Replace it if you have a better one from your own work.

## Reproduce

```powershell
cd training\week2\day3
python step1_by_hand_check.py --show
python step3_check_my_code.py
python step4_why_cosine.py
python -m unittest discover -s tests
python -m unittest test_mine -v
python scenario_matrix.py data/my_scenario.json
python taskE_and_stretch.py
```
