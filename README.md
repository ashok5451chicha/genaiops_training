# GenAI Ops training – submissions

CGI GenAIOps Programme: take-home assignments and weekly mini-capstones, organised **week → day**.
All data is synthetic. No `.env`, API keys or real customer data are included.

## Contents

```
├── capstone-1/                              Capstone 1: Policy Clause Finder (see capstone-1/README.md)
├── week1/
│   └── day1/                                Day 1: the automation-to-agentic spectrum
└── week2/
    ├── day2/                                Day 2: model tiers, embeddings, output verification, approved tools
    ├── day3/                                Day 3: vector mathematics and cosine similarity
    └── day5-6/
        └── kyc-vector-math-lab-starter/     Days 5-6: KYC remediation with vector mathematics (see its README)
```

| Work | Write-up / main document | Code and tests | Results |
|---|---|---|---|
| Day 1 | `week1/day1/docs/Day1_Writeup.pdf` (Parts A–D) | `solutions/day1_ai_spectrum/`, `tests/test_day1_assignment.py` | `outputs/day1_runs/` (scoreboards before and after) |
| Day 2 | `week2/day2/docs/Day2_Writeup.pdf` (Parts A–E), `docs/Approved_Tools_Guideline_DRAFT.pdf` | `solutions/day2_models_and_embeddings/`, `tests/test_day2.py` | `outputs/tier_comparison_*.md`, `outputs/homework_comparison.md`, `outputs/day2_runs/` |
| Day 3 | `week2/day3/docs/Day3_Writeup.pdf`, `docs/TaskA_hand_working.md`, `docs/TaskB_prompt_log.md`, `docs/TaskC_scenario.md` | `my_vector_math.py`, `test_mine.py`, `tests/`, `taskE_and_stretch.py`, `data/my_scenario.json` | `outputs/` (checker 4/4 PASS, scenario matrix) |
| Days 5–6 | `kyc-vector-math-lab-starter/README.md` (changes, limitation), `inconsistency_log.md` | the whole project, `tests/` (46/46) | `evidence/` (every run before and after each fix) |
| Capstone 1 | `capstone-1/README.md` | `capstone-1/` (23 unit tests) | `capstone-1/results/` |

### Day 1–3 folders

They contain the files changed or added for the assignment, at the same paths as in the course repositories:

* Day 1, Day 2: https://github.com/digibhatia/automation-to-agentic-spectrum
* Day 3: https://github.com/digibhatia/cosine-vector-mathematics

To run them, copy the day folder over a fresh clone of its course repository. Days 1 and 2 need a `.env` with an API
key, created from `.env.example` and never committed.

### Days 5–6 and Capstone 1

These are complete projects that use only the Python standard library (Capstone 1 also uses numpy for its library
cross-check). Each one's README explains how to run it.
