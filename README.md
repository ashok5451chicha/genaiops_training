# GenAI Ops training – homework

Take-home assignments for the GenAI Ops training, organised **week → day**. This repository is the holding area; the
final submission goes to GitLab later (see [What to push to GitLab](#what-to-push-to-gitlab-later)).

All data is synthetic. **No API keys are in this repository.** `.env.example` holds a placeholder key only.

---

## 1. What this repository is (and is not)

* Each day of the course has its own **course repository** on GitHub, owned by the trainer:

  | Day | Course repo (the lab code you start from) |
  |---|---|
  | Day 1, Day 2 | https://github.com/digibhatia/automation-to-agentic-spectrum |
  | Day 3 | https://github.com/digibhatia/cosine-vector-mathematics |

* Every assignment means changing or adding files in that course repo, running them and writing up the results.
* **This repository holds only the files that were changed or added for the homework.** The unchanged course files are
  not copied here. Each file sits at **the same path as in the course repo**, so you can copy a day folder over a fresh
  clone of its course repo and run everything.
* The assignment documents (the `.docx` briefs from the trainer) are in the course repos, not here:
  * Day 1: `docs/assignments/Day1_Take_Home_Assignment.docx` (automation-to-agentic-spectrum)
  * Day 2: `docs/assignments/Day2_Take_Home_Assignment.docx` (automation-to-agentic-spectrum)
  * Day 3: `Day3_Unguided_Session_Assignment_Outline.docx` and `Day3_Vector_Mathematics_Participant_Guide.docx`
    (cosine-vector-mathematics)

---

## 2. Folder structure

```
genaiops_training/
├── README.md                       ← this file
├── capstone-1/                     ← Weekly mini-capstone 1: Policy Clause Finder (has its own README)
├── week1/                          ← 1 assignment
│   └── day1/                       ← Day 1 homework (overlay for automation-to-agentic-spectrum)
└── week2/                          ← 2 assignments
    ├── day2/                       ← Day 2 homework (overlay for automation-to-agentic-spectrum)
    ├── day3/                       ← Day 3 homework (overlay for cosine-vector-mathematics)
    └── day5-6/
        └── kyc-vector-math-lab-starter/   ← Days 5-6 KYC lab (complete project, from kyc-starter-participants.zip)
```

The day folders keep the assignment numbers (Day 1, Day 2, Day 3) so they match the assignment briefs and the file
names inside them (`IMPLEMENTATION_DAY2.md`, `Day2_Writeup.pdf`). Later weeks go in `week3/` and so on.

### What each assignment says to submit (copied from the briefs) → where it is

Yes, the `.py` files are required: every brief asks for the changed code and the tests.

| Brief says "What to submit" | File(s) in this repo |
|---|---|
| **Day 1** – a single Word or PDF write-up with Parts A to D | `week1/day1/docs/Day1_Writeup.pdf` |
| **Day 1** – a zip of the files you changed (dispute_tools.py, policy.md, tickets.json, new tests) | `solutions/day1_ai_spectrum/*.py`, `data/policy.md`, `data/tickets.json`, `data/orders.json`, `tests/test_day1_assignment.py` |
| **Day 1** – scoreboards before and after your change | `outputs/day1_runs/00_before_*`, `10_/11_partB_*`, `20_partC_*`, `30_after_*` |
| **Day 2** – one Word or PDF write-up with Parts A to E | `week2/day2/docs/Day2_Writeup.pdf` (+ `Approved_Tools_Guideline_DRAFT.pdf` for Part E) |
| **Day 2** – outputs/tier_comparison_Q1/Q2/Q3.md and the completed homework_comparison.md | `outputs/tier_comparison_Q1.md`, `_Q2.md`, `_Q3.md`, `outputs/homework_comparison.md` |
| **Day 2** – a zip of changed files (sentences.json, verify_outputs.py, tests) | `solutions/day2_models_and_embeddings/data/sentences.json`, `verify_outputs.py`, `embeddings_map.py`, `data/my_query.txt`, `tests/test_day2.py` |
| **Day 3** – Task A table and photo or scan of your working | Table in `docs/Day3_Writeup.pdf`; typed working in `docs/TaskA_hand_working.md`. **Photo: you must add it** |
| **Day 3** – my_vector_math.py (with nearest()), your tests, checker output showing 4/4 PASS | `my_vector_math.py`, `test_mine.py`, `tests/test_vector_math.py`, `outputs/step3_check_my_code.txt`, `outputs/taskB_step3_after_nearest.txt` |
| **Day 3** – prompt log from Task B | `docs/TaskB_prompt_log.md` |
| **Day 3** – data/my_scenario.json, scenario_matrix.py output, prediction note | `data/my_scenario.json`, `outputs/taskC_scenario_matrix.txt`, `docs/TaskC_scenario.md` |
| **Day 3** – Task D table and Task E write-up | `docs/Day3_Writeup.pdf` (Task D and Task E sections), `taskE_and_stretch.py` |
| **Day 3** – a short checklist at the top | First section of `docs/Day3_Writeup.pdf` |
| **All days** – do not submit `.env`, API keys, `.venv`, real data | None of these are in this repo |

### How to read the labels below

| Label | Meaning |
|---|---|
| **SUBMIT** | Part of the assignment deliverable. Push it to GitLab. |
| **EVIDENCE** | Output of a real run, which the write-up quotes. Push it, so the reviewer can check the numbers. |
| **REFERENCE** | For our own understanding: how the work was done and how to re-run it. Not required by the assignment, but harmless to push. |

---

## 3. Week 1 / Day 1 – the automation-to-agentic spectrum

**Assignment:** Part A: place a real business process on the 5-level spectrum. Part B: add a business rule change.
Part C: attack the agent with prompt injection and add a code-level control. Part D: compare cost, speed and risk
across levels.

```
week1/day1/
├── IMPLEMENTATION_DAY1.md          REFERENCE  How Day 1 was done, step by step, with the bugs found and how to re-run
├── .env.example                    SUBMIT     Template for the API key settings (placeholder only). Missing upstream; one test needs it
├── docs/
│   ├── Day1_Writeup.pdf            SUBMIT     The write-up: Parts A–D answered (the main document to read)
│   └── Day1_Writeup.md             SUBMIT     Same write-up as editable Markdown
├── solutions/day1_ai_spectrum/
│   ├── dispute_tools.py            SUBMIT     Part B: loyalty grace rule (1 day instead of 3). Part C: rule 7 enforced in code
│   │                                          (find_instructions() blocks refunds on tickets containing injected instructions)
│   ├── data/orders.json            SUBMIT     New orders ORD-1009 (loyalty), ORD-1010, ORD-1011
│   ├── data/tickets.json           SUBMIT     New tickets T-09 (loyalty), T-10 (hidden P.S. injection), T-11 (fake team lead)
│   ├── data/policy.md              SUBMIT     Policy text updated for the loyalty rule and the expanded rule 7
│   ├── _report.py                  SUBMIT     Scoreboard ground truth now also applies rule 7
│   ├── level1_traditional_automation.py  SUBMIT  Passes the ticket text so rule 7 is checked
│   ├── level2_ai_automation.py     SUBMIT     Same
│   ├── level3_ai_agent.py          SUBMIT     Part D: prints total tokens for --all
│   ├── level4_multi_agent.py       SUBMIT     Part D: token tally per agent role
│   └── level5_agentic_ai.py        SUBMIT     Bug fix: max_tokens 1024 → 4096 (it silently handled 0/8 tickets before)
├── tests/test_day1_assignment.py   SUBMIT     10 new tests for the loyalty rule and the injection control (suite: 65/65 OK)
└── outputs/day1_runs/*.txt         EVIDENCE   Every run, before and after each change, with wall time
                                               (00_ = baseline, 10/11_ = Part B, 20_ = Part C, 30_ = final Part D, 40_ = token check)
```

**Result in one line:** Level 2 (fixed workflow plus AI) is recommended: 11/11 correct, cheapest and most predictable.
Level 5 also scored 11/11 but needs more oversight.

---

## 4. Week 2 / Day 2 – model tiers, embeddings, verification, approved tools

**Assignment:** Part A: compare Opus, Sonnet and Haiku on the same prompts. Part B: compare chat tools and their privacy
settings, with your own query. Part C: embeddings map with your own topic. Part D: verify model output against the
source document. Part E: a one-page approved-tools guideline.

```
week2/day2/
├── IMPLEMENTATION_DAY2.md          REFERENCE  How Day 2 was done, part by part, and how to re-run it
├── .env.example                    SUBMIT     API key template (placeholder only)
├── docs/
│   ├── Day2_Writeup.pdf            SUBMIT     The write-up: Parts A–E answered (main document)
│   ├── Day2_Writeup.md             SUBMIT     Editable version
│   ├── Approved_Tools_Guideline_DRAFT.pdf  SUBMIT  Part E: one-page guideline (DRAFT for Security and Legal)
│   └── Approved_Tools_Guideline_DRAFT.md   SUBMIT  Editable version
├── solutions/day2_models_and_embeddings/
│   ├── verify_outputs.py           SUBMIT     Part D: new checked item, rounding-bug fix, coverage check for uncited clauses,
│   │                                          failures now written to the audit log
│   ├── embeddings_map.py           SUBMIT     Part C: bug fix (a 5th topic was silently dropped from the map), --query option
│   ├── data/sentences.json         SUBMIT     Part C: new topic finance_expenses (8 sentences)
│   └── data/my_query.txt           SUBMIT     Part B: own synthetic card-terms query with known answers
├── tests/test_day2.py              SUBMIT     New tests for the verification changes (suite: 63 OK, 3 skipped, 1 expected failure)
└── outputs/
    ├── tier_comparison_Q1/Q2/Q3.md SUBMIT     Part A: tier comparison reports
    ├── tier_comparison_custom.md   SUBMIT     Part B: own query on the three tiers
    ├── homework_comparison.md      SUBMIT     Part B: chat-tool comparison sheet and privacy settings
    ├── embedding_map.png           SUBMIT     Part C: the embeddings map
    ├── verification_audit.jsonl    EVIDENCE   Part D: audit log of the verification runs
    └── day2_runs/*                 EVIDENCE   Raw output of every run (partA_, partB_, partC_, partD_)
```

**Gaps in Day 2:** ChatGPT and Gemini were not run (no access), so their columns say "not run". Real embeddings did not
run because this machine is missing the Microsoft Visual C++ runtime, so the toy embedder was used.

---

## 5. Week 2 / Day 3 – vector mathematics and cosine similarity

**Assignment:** Guided Steps 1–4 (by hand, in code, check, why cosine). Task A: hand working. Task B: build `nearest()`
with Claude and log the prompts. Task C: your own scenario matrix. Task E: misleading similarity. Stretch tasks.

```
week2/day3/
├── IMPLEMENTATION_DAY3.md          REFERENCE  How Day 3 was done, decisions taken, how to re-run
├── STEP1_HAND_WORKING.md           SUBMIT     Guided Step 1: calculations worked by hand
├── STEP4_NOTES.md                  SUBMIT     Guided Step 4: notes on why cosine beats distance for text
├── my_vector_math.py               SUBMIT     Step 2: dot, norm, cosine_similarity, euclidean_distance; Task B: nearest() v2
├── test_mine.py                    SUBMIT     12 own tests (functions and nearest())
├── taskE_and_stretch.py            SUBMIT     Task E pairs plus stretch (unit-vector identity, centroid, sensitivity)
├── data/my_scenario.json           SUBMIT     Task C: KYC document-remediation scenario (6 items × 4 dimensions)
├── tests/test_vector_math.py       SUBMIT     Small fix so the course test still passes once the functions are written (16/16 OK)
├── docs/
│   ├── Day3_Writeup.pdf            SUBMIT     The write-up (main document)
│   ├── Day3_Writeup.md             SUBMIT     Editable version
│   ├── TaskA_hand_working.md       SUBMIT     Task A working (typed; the assignment wants a handwritten photo, see below)
│   ├── TaskB_prompt_log.md         SUBMIT     Task B: prompts sent to Claude and what was accepted or fixed
│   └── TaskC_scenario.md           SUBMIT     Task C explanation
└── outputs/*.txt                   EVIDENCE   Output of every step and task run
```

**Still to do yourself for Day 3:**
1. Copy `docs/TaskA_hand_working.md` by hand, then add a photo or scan of it.
2. Task E now has an own-work example (GenAI operations: RAG assistant retrieving an old policy clause with the opposite meaning). Replace it if you have a better one.

---

## 5a. Week 2 / Days 5–6 – KYC remediation: vector mathematics in practice

**Brief:** `docs/Participant_Starter_Brief_Days5-6_KYC.docx` inside the lab (from `kyc-starter-participants.zip`).
A half-finished, partly wrong KYC helper: run it, list every inconsistency, write the missing pieces M1–M6, fix
everything, prove it end to end.

Unlike Days 1–3, this folder is the **complete project** (the starter came as a zip, not a course repo), so it runs
as is. Everything in it is **SUBMIT** except `evidence/` (**EVIDENCE**: output of every run, before and after each
fix). `output/` is git-ignored, as the brief requires; `python run_pipeline.py` re-creates it.

| File | What it is |
|---|---|
| `inconsistency_log.md` | The 20 inconsistencies found (17 fixed, 3 explained): where, what, how found |
| `README.md` (end section) | What was changed, results, one limitation of the toy embedder |
| `by_hand/worksheet_answers.md`, `by_hand/my_answers.json` | Worksheet worked by hand; all 9 match `check_by_hand.py` |
| `vector_math.py`, `embedder.py`, `kyc_pipeline.py`, `run_pipeline.py`, `why_cosine.py` | Fixed code and missing pieces M1–M5 |
| `tests/test_pipeline.py` | M6: 30 new tests (suite 46/46 OK) |
| `data/*.json`, `config.json` | Fixed data (K014 id, ISO date, status) and threshold (review_cosine 0.70) |

Results: notes classified 1/20 → **20/20**; probable-duplicate precision 0.095 → **1.0**; all 3 known duplicates
reach a human; no raw ID in any output.

GitLab (from the brief): branch `your-name-days5-6`, commit `Days 5-6 KYC vector maths`, merge request to the
trainer. Check `git status` shows no `.env` and no `output/`.

---

## 5b. Capstone 1 – Policy Clause Finder

**Brief:** `Weekly Mini Capatone- 1.pdf` (CGI GenAIOps weekly mini-capstones), set Fri 30-Oct-2026, due Mon 2-Nov-2026.
A semantic search tool that ranks 19 synthetic bank policy clauses against an analyst's question by cosine
similarity (written by hand), shows the top 3 with verified quotes, and says "not found" below a threshold.

Everything is in [`capstone-1/`](capstone-1/), with its own [README](capstone-1/README.md): purpose, how to run,
results table, two limitations, one improvement idea and the acceptance checklist. The whole folder is **SUBMIT**
(the brief says to push the code, README, test results and architecture diagram in a folder named `capstone-1`).
`docs/WALKTHROUGH.md` is the script for the 8-minute trainer walkthrough (REFERENCE).

Results: 8/8 test questions right first time (keyword baseline 3/8, Euclidean 0/8); a 6-question stress set with
unseen wording scores 1/6 first time (6/6 in the top 3), reported as is; 23/23 unit tests.

---

## 6. What is NOT in this repository, and must never be pushed

| Item | Why |
|---|---|
| `.env` | Contains the real API key. It stays only on the local machine (git-ignored). |
| `.venv/`, `__pycache__/` | Local environment, rebuilt with `pip install -r requirements.txt` |
| Unchanged course files | They belong to the trainer's repos; clone those instead |
| `outputs/submission/*.zip`, `submission/*.zip` | Zips of exactly what is in each day folder; redundant in git |

---

## 7. What to push to GitLab later

**Rule:** push the whole `weekN/dayN/` folders: everything labelled SUBMIT and EVIDENCE. The REFERENCE files
(`IMPLEMENTATION_DAYn.md`) are for our understanding. Pushing them is fine, but if GitLab should contain only the
deliverables, leave them out.

### Option A – push the homework files only (recommended)

```bash
# 1. Get the homework from this GitHub repo
git clone https://github.com/ashok5451chicha/genaiops_training.git

# 2. Clone the GitLab repo you were given (replace the URL)
git clone <your-gitlab-repo-url> gitlab_repo

# 3. Copy the week/day folders across
cp -r genaiops_training/week1 genaiops_training/week2 gitlab_repo/
# optional: leave out the reference notes
# rm gitlab_repo/week*/day*/IMPLEMENTATION_DAY*.md

# 4. Check that no key is included, then push
cd gitlab_repo
grep -rE "sk-ant-[A-Za-z0-9_-]{20,}" . --exclude-dir=.git   # must print nothing
git add week1 week2
git commit -m "Week 1 and week 2 homework: day 1-3"
git push
```

### Option B – the GitLab repo must contain the full runnable project

If the trainer wants the full course code with your changes on top:

```bash
# Day 1 (Day 2 uses the same course repo: repeat with genaiops_training/week2/day2 into a folder day2)
git clone https://github.com/digibhatia/automation-to-agentic-spectrum.git day1
cp -r genaiops_training/week1/day1/. day1/          # overlay the homework files
# Day 3
git clone https://github.com/digibhatia/cosine-vector-mathematics.git day3
cp -r genaiops_training/week2/day3/. day3/
```

Then point each folder at GitLab (`git remote set-url origin <gitlab-url>`), commit and push. To check before
pushing: `python -m unittest discover -s tests` should pass in each folder (it needs a `.env` with your key for the
live runs, never committed).

### Checklist before any GitLab push

- [ ] No `.env` file and no real `sk-ant-…` key (run the `grep` above)
- [ ] Day 3: handwritten photo for Task A added
- [x] Day 3: own-work example for Task E added (GenAI operations case)
- [ ] Day 1 Part A: replace the assumed process (retail-bank complaint handling) if yours is different
