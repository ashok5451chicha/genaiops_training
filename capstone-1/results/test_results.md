# Policy Clause Finder - test results

Embedder: `concept lexicon (19 concepts + 32 hashed word dims)` · threshold for "not found": **0.40** (cosine) · 19 clauses

## Summary

| Test set | Ranking | Right first time | In top 3 |
|---|---|---|---|
| 8 main questions | concept embedder + **cosine** (the tool) | **8/8** | 8/8 |
| 8 main questions | concept embedder + euclidean | 0/8 | 0/8 |
| 8 main questions | concept embedder, unit-length vectors + euclidean | 8/8 | 8/8 |
| 8 main questions | keyword baseline + cosine | 3/8 | 6/8 |
| 6 stress questions (unknown words, not tuned) | concept embedder + cosine | **1/6** | 6/6 |
| 2 out-of-scope questions | must say "not found" | 2/2 | - |

Every quote shown was verified verbatim in its source clause: yes.

## 1. Main test set: the tool (concept embedder + cosine)

| # | Question | Expected | Top 3 (cosine) | Right first time | In top 3 |
|---|---|---|---|---|---|
| Q1 | Customer says they cannot pay their EMI this month. What happens to the loan? | LN-01 | LN-01 0.848, LN-04 0.798, LN-03 0.466 | yes | yes |
| Q2 | Customer lost their job and wants a break from loan payments for a while | LN-02 | LN-02 0.962, LN-04 0.282, LN-01 0.276 | yes | yes |
| Q3 | There is a purchase on my card that I never made | CC-02 | CC-02 0.755, CC-01 0.494, CC-03 0.405 | yes | yes |
| Q4 | I paid my credit card bill two days late, will I be charged anything? | CC-03 | CC-03 0.793, CP-02 0.547, LN-04 0.518 | yes | yes |
| Q5 | How long does the bank have to reply to my complaint? | CP-01 | CP-01 0.951, CP-02 0.937, CP-03 0.559 | yes | yes |
| Q6 | I have moved house recently, what do I need to send you? | KY-03 | KY-03 0.725, KY-02 0.203, KY-04 0.147 | yes | yes |
| Q7 | Is there a penalty if I pay off my personal loan early? | LN-03 | LN-03 0.945, LN-05 0.462, LN-04 0.439 | yes | yes |
| Q8 | The shop never delivered the item I paid for with my card | CC-04 | CC-04 0.958, CC-02 0.393, CC-03 0.323 | yes | yes |

## 2. Same questions ranked by Euclidean distance

| # | Question | Expected | Top 3 (distance) | Right first time | In top 3 |
|---|---|---|---|---|---|
| Q1 | Customer says they cannot pay their EMI this month. What happens to the loan? | LN-01 | AC-01 4.657, CC-05 5.043, LN-04 5.078 | **no** | **no** |
| Q2 | Customer lost their job and wants a break from loan payments for a while | LN-02 | CC-05 4.620, AC-01 4.648, KY-02 4.826 | **no** | **no** |
| Q3 | There is a purchase on my card that I never made | CC-02 | AC-01 4.313, CC-05 4.530, KY-02 4.947 | **no** | **no** |
| Q4 | I paid my credit card bill two days late, will I be charged anything? | CC-03 | AC-01 4.096, CC-05 4.688, KY-02 4.702 | **no** | **no** |
| Q5 | How long does the bank have to reply to my complaint? | CP-01 | AC-01 3.676, KY-02 4.402, CC-05 5.043 | **no** | **no** |
| Q6 | I have moved house recently, what do I need to send you? | KY-03 | AC-01 4.195, CC-05 4.620, KY-02 4.634 | **no** | **no** |
| Q7 | Is there a penalty if I pay off my personal loan early? | LN-03 | AC-01 4.678, CC-05 5.132, KY-02 5.268 | **no** | **no** |
| Q8 | The shop never delivered the item I paid for with my card | CC-04 | AC-01 5.157, CC-05 5.340, KY-02 5.698 | **no** | **no** |

## 3. Same questions with the keyword baseline (no synonyms)

| # | Question | Expected | Top 3 (cosine) | Right first time | In top 3 |
|---|---|---|---|---|---|
| Q1 | Customer says they cannot pay their EMI this month. What happens to the loan? | LN-01 | LN-03 0.206, LN-04 0.172, LN-01 0.154 | **no** | yes |
| Q2 | Customer lost their job and wants a break from loan payments for a while | LN-02 | LN-03 0.178, AC-02 0.146, LN-01 0.134 | **no** | **no** |
| Q3 | There is a purchase on my card that I never made | CC-02 | CC-01 0.430, CC-03 0.289, CC-02 0.183 | **no** | yes |
| Q4 | I paid my credit card bill two days late, will I be charged anything? | CC-03 | CC-03 0.486, CC-04 0.279, CC-01 0.263 | yes | yes |
| Q5 | How long does the bank have to reply to my complaint? | CP-01 | CP-01 0.252, CP-02 0.144, LN-01 0.000 | yes | yes |
| Q6 | I have moved house recently, what do I need to send you? | KY-03 | CP-03 0.167, LN-01 0.000, LN-02 0.000 | **no** | **no** |
| Q7 | Is there a penalty if I pay off my personal loan early? | LN-03 | LN-03 0.548, LN-01 0.232, LN-05 0.145 | yes | yes |
| Q8 | The shop never delivered the item I paid for with my card | CC-04 | CC-01 0.310, CC-03 0.250, CC-04 0.197 | **no** | yes |

## 4. Stress set (written after the main set scored, lexicon not changed afterwards)

| # | Question | Expected | Top 3 (cosine) | Right first time | In top 3 |
|---|---|---|---|---|---|
| S1 | The ATM swallowed my debit card and did not give it back | CC-01 | CC-01 0.668, CC-03 0.498, CC-02 0.317 | yes | yes |
| S2 | Can I get a bigger spending allowance on my credit card? | CC-05 | CC-01 0.623, CC-03 0.502, CC-05 0.275 | **no** | yes |
| S3 | My husband passed away last month, how quickly will you deal with my complaint? | CP-03 | CP-02 0.494, CP-03 0.306, CP-01 0.163 | **no** | yes |
| S4 | I haven't touched my savings account in three years and now it is frozen | AC-02 | KY-02 0.269, AC-01 0.261, AC-02 0.144 | **no** | yes |
| S5 | You are putting up the interest on my loan, can I get out of it? | LN-05 | LN-04 0.553, LN-01 0.545, LN-05 0.481 | **no** | yes |
| S6 | We are a limited company. How often do you check who owns us? | KY-04 | CC-05 0.589, KY-04 0.509, KY-02 0.062 | **no** | yes |

## 5. Out-of-scope questions

| # | Question | Result | Best cosine |
|---|---|---|---|
| X1 | What time does the staff canteen open on Fridays? | not found | 0.255 |
| X2 | How do I reset my email password on my laptop? | not found | 0.127 |

## 6. Score distribution (used to choose the threshold)

* Best score of each in-scope question (main + stress): min **0.269**, max 0.962
* Best score of each out-of-scope question: max **0.255**
* Main-set best scores: min **0.725**. Threshold **0.40** sits between the out-of-scope maximum and the main-set minimum.
* In-scope questions answered "not found" (below the threshold; a safe failure, the analyst is sent to the policy team): S4 (0.269)
