# Task C – my scenario table

**Use case:** #1 KYC document remediation assistant (Document Intelligence & Data Remediation).
**File:** `data/my_scenario.json`, copied from the template.

## Dimensions (0–5)

| Dimension | Meaning |
|---|---|
| identity_proof | How much the item is about proving who the customer is |
| address_proof | How much it is about proving where they live |
| income_proof | How much it is about proving what they earn |
| data_quality_issue | How much it describes a problem with the document or data |

## Items (synthetic)

| Item | identity | address | income | data quality | Why these numbers |
|---|---|---|---|---|---|
| Passport scan | 5 | 1 | 0 | 0 | Clean primary ID; a little address (some passports carry one) |
| Utility bill | 1 | 5 | 0 | 0 | The standard address proof; shows the name |
| Salary slip | 1 | 1 | 5 | 0 | Income proof; shows name and often address |
| Blurred ID scan | 4 | 0 | 0 | 5 | An ID document whose main feature is the quality problem |
| Missing field | 2 | 2 | 1 | 4 | A data problem that can sit on any document |
| Conflicting address | 0 | 4 | 0 | 4 | An address problem: half address, half data issue |

## Predictions (written BEFORE running the script)

* **Most similar pair:** Missing field ↔ Conflicting address. Both are remediation *problems* rather than documents.
* **Least similar pair:** Salary slip ↔ Conflicting address. Income proof versus an address problem: nothing shared.
* **Pair I think will surprise me:** Utility bill ↔ Conflicting address. A *valid* document and a *problem* might score
  quite high, because both are mostly "address".

## Result (`outputs/taskC_scenario_matrix.txt`)

| | Predicted | Actual (cosine) | Actual (distance) |
|---|---|---|---|
| Most similar | Missing field ↔ Conflicting address | **Blurred ID scan ↔ Missing field 0.87**; my pick was a close 2nd (0.85) | **Missing field ↔ Conflicting address 3.00** (my pick); Blurred ↔ Missing 3.16 |
| Least similar | Salary slip ↔ Conflicting address (0.14) | Salary slip ↔ Blurred ID scan **0.12**, tied with Utility bill ↔ Blurred ID scan | Salary slip ↔ Blurred ID scan 7.75 |
| Surprise | Utility bill ↔ Conflicting address | **0.69**, the 3rd most similar of 15 pairs: higher than Passport ↔ Utility bill (0.38) | 4.24 |

**Prediction versus result.** I was nearly right. The top two pairs are separated by 0.02 in cosine, and **the two
metrics disagree on which is closest**: cosine prefers Blurred ID ↔ Missing field, distance prefers Missing field ↔
Conflicting address. With scores that close, "the most similar pair" is not a robust fact, it depends on the metric.
The least-similar pair moved because Blurred ID scan is extreme on two dimensions that salary slips and utility bills
score zero on. The surprise came true: a valid utility bill sits closer to a *problem* item (conflicting address) than
to another valid document (passport). That is because both are mostly "address", and my vectors mix *what a document
is* with *what is wrong with it* in one space. I kept the numbers. They reflect my judgement honestly, and the result
is a real property of this design, not a typo. A production version should separate document type from defect type,
for example as two vectors or a vector plus a label.

**What the closest pair means to a bank team, and what a human still checks.** Blurred ID scan and Missing field being
closest says that, to the assistant, both look like "this case needs remediation". The team could route them to the
same queue and the same playbook (request a new copy, chase the missing data). A human still has to decide *what*
is wrong and whether the customer is who they claim to be. A blurred ID is a possible identity risk, while a missing
field is usually clerical, and similarity cannot tell those apart or verify an identity. Before any account is opened
or remediated, a person checks the actual document against the source record.
