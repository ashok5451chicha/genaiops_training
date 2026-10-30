# Task B – prompt log

Tool: Claude Code (in VS Code). The work was done by Claude Code acting on the prompts below. Every claim was then
checked by running the tests and, where tests and code disagreed, by hand.

| # | Prompt used | What Claude Code produced | What was wrong or missing | What changed |
|---|---|---|---|---|
| 1 | Prompt 1: implement `dot`, `norm`, `cosine_similarity`, `euclidean_distance`; standard library only; comment above each line; `ValueError` for zero vectors and different lengths; do not open `vector_math.py` | The four functions plus a shared `_check_same_length()` guard | Nothing found. `step3_check_my_code.py` → 4/4 PASS. The answer key was never opened | – |
| 2 | Prompt 2: walk through `cosine_similarity([3, 4], [4, 3])` line by line | dot 24, lengths 5 and 5, cosine 24/25 = 0.96 | Matches my hand calculation (Step 1, E1) | – |
| 3 | Prompt 5: add `nearest(query, candidates, metric="cosine")` returning names from most to least similar; cosine higher is better, euclidean lower is better | **Version 1**: an `if metric == "cosine"` branch, and *everything else* fell through to euclidean | **Bug:** `metric="Cosine"`, `"manhattan"` or the typo `"euclidian"` silently gave a euclidean ranking, a confidently wrong answer with no error. **Gap:** a zero-vector candidate raised a bare "undefined for a zero vector" error without saying which candidate | **Version 2:** unknown metrics raise `ValueError`; the failing candidate is named in the error; the docstring states that ties keep input order and an empty dict gives `[]` |
| 4 | Prompt 4, extended: unittest tests for the four functions (zero vector, different lengths, negative numbers) and for `nearest` (both metrics, ties, empty, unknown metric, zero vector) → `test_mine.py` | 12 tests | Run against v1: 5 failures. 4 were real (unknown metrics, unnamed zero vector). **1 was my test's mistake:** I expected loan's ranking to end `fraud, complaint`, but by hand complaint is 0.370 and fraud 0.344, so the code was right. I also avoided the classic "test that cannot fail": every ranking test checks the full order, not just the length | Expected order corrected, with the hand calculation in a comment. v2: **12/12 pass**; `step3_check_my_code.py` still **4/4 PASS** |

**The thing I challenged:** the metric fall-through in version 1. It passed every happy-path test, which only used
`"cosine"` and `"euclidean"`, so it would have shipped. In a bank tool, a typo in a config file would have flipped the
ranking direction with no warning.

**Lesson:** the checker and the hand maths are the judges, in both directions. They caught a bug in the generated code,
and they also caught a wrong expectation in a test I wrote myself.

Evidence: `outputs/taskB_tests_v1.txt` (5 failures), `outputs/taskB_tests_v2.txt` (OK),
`outputs/taskB_step3_after_nearest.txt` (4/4 PASS).
