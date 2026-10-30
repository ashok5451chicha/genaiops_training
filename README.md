# GenAI Ops training – homework

Take-home assignments and capstones for the CGI GenAIOps training, organised **week → day**. This repository is the
holding area; the final submission is pushed to GitLab later.

All data is synthetic. **No API keys are in this repository.** `.env.example` holds a placeholder key only.

---

## 0. Two branches, same structure

| Branch | What it holds | Use it for |
|---|---|---|
| **`main`** (this one) | Everything: the submission **plus** the understanding material (`understanding/` folders, editable `.md` copies of the write-ups) | Learning, revising, preparing the walkthroughs |
| **`gitlab-submission`** | **Only what the assignment and capstone briefs ask to be submitted**: no `understanding/` folders, write-ups as PDF only | Copying to GitLab ([section 7](#7-pushing-to-gitlab-from-the-gitlab-submission-branch)) |

Both branches have the same folders. `gitlab-submission` is `main` minus the items marked **main only** below.

| Label used below | On `main` | On `gitlab-submission` |
|---|---|---|
| **SUBMIT** – a deliverable the brief asks for | yes | yes |
| **EVIDENCE** – run output the write-up quotes, so the reviewer can check the numbers | yes | yes |
| **main only** – understanding material or an editable copy | yes | **no** |

---

## 1. Where the work comes from

| Work | Brief | Base code |
|---|---|---|
| Day 1, Day 2 | `docs/assignments/Day1_Take_Home_Assignment.docx`, `Day2_…docx` in the course repo | https://github.com/digibhatia/automation-to-agentic-spectrum |
| Day 3 | `Day3_Unguided_Session_Assignment_Outline.docx` in the course repo | https://github.com/digibhatia/cosine-vector-mathematics |
| Days 5–6 | `docs/Participant_Starter_Brief_Days5-6_KYC.docx` inside the lab | `kyc-starter-participants.zip` (from the trainer) |
| Capstone 1 | `Weekly Mini Capatone- 1.pdf` | built from scratch |

The **Day 1–3** folders hold **only the files that were changed or added**, at the same paths as in the course repo,
so a day folder can be copied over a fresh clone of its course repo and run. The **Days 5–6** and **Capstone 1**
folders are complete projects that run as they are.

---

## 2. Folder structure

```
genaiops_training/
├── README.md
├── capstone-1/                              Weekly mini-capstone 1: Policy Clause Finder (own README)
│   └── understanding/                       main only
├── week1/                                   1 assignment
│   └── day1/                                Day 1 homework
│       └── understanding/                   main only
└── week2/                                   2 assignments + the Days 5-6 lab
    ├── day2/                                Day 2 homework
    │   └── understanding/                   main only
    ├── day3/                                Day 3 homework
    │   └── understanding/                   main only
    └── day5-6/
        ├── kyc-vector-math-lab-starter/     Days 5-6 KYC lab (complete project)
        └── understanding/                   main only
```

The day folders keep the assignment numbers (Day 1, Day 2, Day 3) so they match the briefs and the file names
(`Day2_Writeup.pdf`). Later weeks go in `week3/` and so on, with the same layout.

### What each brief says to submit → where it is

| Brief says "What to submit" | File(s) |
|---|---|
| **Day 1** – a single Word or PDF write-up with Parts A to D | `week1/day1/docs/Day1_Writeup.pdf` |
| **Day 1** – the files you changed (dispute_tools.py, policy.md, tickets.json, new tests) | `solutions/day1_ai_spectrum/*.py`, `data/policy.md`, `data/tickets.json`, `data/orders.json`, `tests/test_day1_assignment.py`, `.env.example` |
| **Day 1** – scoreboards before and after your change | `outputs/day1_runs/` |
| **Day 2** – one Word or PDF write-up with Parts A to E | `week2/day2/docs/Day2_Writeup.pdf` (+ `Approved_Tools_Guideline_DRAFT.pdf`, Part E) |
| **Day 2** – outputs/tier_comparison_Q1/Q2/Q3.md and the completed homework_comparison.md | `outputs/tier_comparison_Q1.md`, `_Q2.md`, `_Q3.md`, `outputs/homework_comparison.md` |
| **Day 2** – the changed files (sentences.json, verify_outputs.py, tests) | `solutions/day2_models_and_embeddings/data/sentences.json`, `verify_outputs.py`, `embeddings_map.py`, `data/my_query.txt`, `tests/test_day2.py`, `.env.example` |
| **Day 3** – Task A table and photo or scan of your working | Table in `docs/Day3_Writeup.pdf`; working in `docs/TaskA_hand_working.md`. **Photo: you must add it** |
| **Day 3** – my_vector_math.py (with nearest()), your tests, checker output showing 4/4 PASS | `my_vector_math.py`, `test_mine.py`, `tests/test_vector_math.py`, `outputs/step3_check_my_code.txt`, `outputs/taskB_step3_after_nearest.txt` |
| **Day 3** – prompt log from Task B | `docs/TaskB_prompt_log.md` |
| **Day 3** – data/my_scenario.json, scenario_matrix.py output, prediction note | `data/my_scenario.json`, `outputs/taskC_scenario_matrix.txt`, `docs/TaskC_scenario.md` |
| **Day 3** – Task D table, Task E write-up, a checklist at the top | `docs/Day3_Writeup.pdf`, `taskE_and_stretch.py` |
| **Days 5–6** – passing tests, checker matches, pipeline end to end, IDs masked, inconsistency log, README note | the whole `kyc-vector-math-lab-starter/` folder (without `output/`, as the brief requires) |
| **Capstone 1** – code, README, test results, architecture diagram, in a folder named `capstone-1` | the whole `capstone-1/` folder except `understanding/` |
| **All** – no `.env`, API keys, `.venv`, real data | none in either branch |

---

## 3. Week 1 / Day 1 – the automation-to-agentic spectrum

**Assignment:** Part A: place a real process on the 5-level spectrum. Part B: change a business rule in code. Part C:
attack the agent with prompt injection and add a code-level control. Part D: compare cost, speed and risk.

```
week1/day1/
├── .env.example                    SUBMIT     API key template (placeholder only); missing upstream, one test needs it
├── docs/
│   ├── Day1_Writeup.pdf            SUBMIT     The write-up: Parts A–D
│   └── Day1_Writeup.md             main only  Editable copy
├── solutions/day1_ai_spectrum/
│   ├── dispute_tools.py            SUBMIT     Part B loyalty grace rule; Part C rule 7 (injected instructions) enforced in code
│   ├── data/orders.json            SUBMIT     New orders ORD-1009 (loyalty), ORD-1010, ORD-1011
│   ├── data/tickets.json           SUBMIT     New tickets T-09, T-10 (hidden injection), T-11 (fake team lead)
│   ├── data/policy.md              SUBMIT     Policy text matches the code
│   ├── _report.py, level1…5_*.py   SUBMIT     Rule 7 wired in; Part D token tallies; Level 5 max_tokens fix
├── tests/test_day1_assignment.py   SUBMIT     10 new tests (suite 65/65 OK)
├── outputs/day1_runs/*.txt         EVIDENCE   Scoreboards before and after every change, with wall time
└── understanding/
    └── IMPLEMENTATION_DAY1.md      main only  How Day 1 was done, bugs found, how to re-run
```

**Result:** Level 2 recommended (11/11, cheapest, most predictable).

---

## 4. Week 2 / Day 2 – model tiers, embeddings, verification, approved tools

**Assignment:** Part A: compare Opus, Sonnet and Haiku. Part B: compare chat tools, privacy settings, own query.
Part C: embeddings map with your own topic. Part D: verify model output against the source. Part E: approved-tools
guideline.

```
week2/day2/
├── .env.example                    SUBMIT     API key template (placeholder only)
├── docs/
│   ├── Day2_Writeup.pdf            SUBMIT     The write-up: Parts A–E
│   ├── Approved_Tools_Guideline_DRAFT.pdf  SUBMIT  Part E
│   ├── Day2_Writeup.md             main only  Editable copy
│   └── Approved_Tools_Guideline_DRAFT.md   main only  Editable copy
├── solutions/day2_models_and_embeddings/
│   ├── verify_outputs.py           SUBMIT     Part D: new item, rounding fix, uncited-clause check, failures logged
│   ├── embeddings_map.py           SUBMIT     Part C: 5th-topic bug fix, --query option
│   ├── data/sentences.json         SUBMIT     Part C: new topic finance_expenses
│   └── data/my_query.txt           SUBMIT     Part B: own synthetic query
├── tests/test_day2.py              SUBMIT     63 OK, 3 skipped, 1 expected failure
├── outputs/
│   ├── tier_comparison_*.md, homework_comparison.md, embedding_map.png   SUBMIT
│   ├── verification_audit.jsonl, day2_runs/*                            EVIDENCE
└── understanding/
    └── IMPLEMENTATION_DAY2.md      main only
```

**Gaps:** ChatGPT and Gemini were not run (no access); real embeddings could not run (Visual C++ runtime missing).

---

## 5. Week 2 / Day 3 – vector mathematics and cosine similarity

```
week2/day3/
├── STEP1_HAND_WORKING.md, STEP4_NOTES.md     SUBMIT    Guided steps (the write-up reports them)
├── my_vector_math.py               SUBMIT     Functions + nearest() v2
├── test_mine.py                    SUBMIT     12 own tests
├── taskE_and_stretch.py            SUBMIT     Task E pairs + stretch
├── data/my_scenario.json           SUBMIT     Task C scenario
├── tests/test_vector_math.py       SUBMIT     16/16 OK
├── docs/
│   ├── Day3_Writeup.pdf            SUBMIT     Write-up with the checklist at the top
│   ├── TaskA_hand_working.md, TaskB_prompt_log.md, TaskC_scenario.md   SUBMIT
│   └── Day3_Writeup.md             main only  Editable copy
├── outputs/*.txt                   EVIDENCE   Checker 4/4 PASS, scenario matrix, every run
└── understanding/
    └── IMPLEMENTATION_DAY3.md      main only
```

**Still to do yourself:** add a photo of the handwritten Task A working; optionally replace the Task E example
with one from your own work.

---

## 6. Week 2 / Days 5–6 – KYC lab, and Capstone 1

### Days 5–6 – KYC remediation: vector mathematics in practice

```
week2/day5-6/
├── kyc-vector-math-lab-starter/    SUBMIT     The whole fixed project: code, tests (46/46), inconsistency_log.md (20),
│                                              README note, by_hand answers; evidence/ = every run before/after (EVIDENCE)
└── understanding/
    ├── KYC_Lab_Understanding.pdf   main only  Study guide: maths, worked examples, every fix, walkthrough script
    └── KYC_Lab_Understanding.md    main only
```

Results: notes 1/20 → **20/20**; duplicate precision 0.095 → **1.0**; all known duplicates reach a human; no raw ID
in any output. GitLab (from the brief): branch `your-name-days5-6`, commit `Days 5-6 KYC vector maths`.

### Capstone 1 – Policy Clause Finder

```
capstone-1/                         SUBMIT     Code, README, data, docs/architecture.png, results/, tests/
└── understanding/
    ├── Capstone1_Understanding.pdf main only  Study guide with a worked example
    ├── Capstone1_Understanding.md  main only
    └── WALKTHROUGH.md              main only  Script for the 8-minute trainer walkthrough
```

Results: 8/8 test questions right first time (keyword 3/8, Euclidean 0/8); stress set 1/6 reported as is; 23/23
tests. Commit message from the brief: `Capstone 1: Policy Clause Finder`.

---

## 7. Pushing to GitLab (from the `gitlab-submission` branch)

```bash
# 1. Take the submission branch only
git clone -b gitlab-submission https://github.com/ashok5451chicha/genaiops_training.git submission

# 2. Clone your GitLab project (URL from the trainer) and copy the folders you are submitting
git clone <your-gitlab-project-url> gitlab_repo
cp -r submission/capstone-1 submission/week1 submission/week2 gitlab_repo/

# 3. Check, commit on a branch, push, open a merge request with the trainer as reviewer
cd gitlab_repo
grep -rE "sk-ant-[A-Za-z0-9_-]{20,}" . --exclude-dir=.git     # must print nothing
git checkout -b <your-branch>
git add . && git status                                        # no .env, no output/, no understanding/
git commit -m "Capstone 1: Policy Clause Finder"               # or the message each brief asks for
git push origin <your-branch>
```

If the trainer wants the full course code for Days 1–3: clone the course repo, copy the day folder over it
(`cp -r submission/week1/day1/. day1/`), then push.

### Checklist before any GitLab push

- [ ] No `.env` and no real `sk-ant-…` key (run the `grep` above)
- [ ] No `understanding/` folder (only possible if you copied from `main` by mistake)
- [ ] Day 3: photo of the handwritten Task A working added
- [ ] Day 1 Part A: replace the assumed process (retail-bank complaint handling) if yours is different

---

## 8. Never pushed anywhere

| Item | Why |
|---|---|
| `.env` | Holds the real API key; local only (git-ignored) |
| `.venv/`, `__pycache__/`, `output/` | Rebuilt locally |
| Unchanged course files | Belong to the trainer's repos |
| `*_submission.zip` | Same content as the folders |
