# Capstone 1 – 8-minute walkthrough script

The brief asks for: problem, architecture, live run (one normal and one tricky input), results and what failed,
one limitation and what comes next.

## 1. Problem and outcome (30 s)

"Analysts lose time finding the one policy clause that answers a customer, and keyword search misses it when the
customer says 'cannot pay my EMI' and the policy says 'repayment default'. This tool ranks 19 synthetic clauses by
meaning, shows the top three with a score and a quote checked against the source, and says 'not found' when
nothing is close enough."

## 2. Architecture (1 min) – show `docs/architecture.png`

Question → `embed.py` (19 banking concepts + hashed words) → `rank.py` (cosine by hand, top 3) → `verify.py`
(quote must appear verbatim) → answer or NOT FOUND below 0.40. `crosscheck.py` proves the hand-written cosine
matches numpy and scikit-learn.

Why a concept embedder: the real local model can't load on this machine (missing Visual C++ runtime), and the
brief allows the lab embedder. Why cosine: Euclidean scored 0/8 because it measures text length, not topic.

## 3. Live run (3 min)

```bash
python finder.py "Customer says they cannot pay their EMI this month. What happens to the loan?" --explain
```
Normal case: LN-01 first (0.848). Point at `'cannot pay' -> repayment_trouble` and `'emi' -> loan`: no shared words
with the clause, yet it is found. The quote is marked verified.

```bash
python finder.py "I paid my credit card bill two days late, will I be charged anything?" --explain
```
Tricky case (near-duplicate): the credit-card fee CC-03 (0.793) beats the loan late charge LN-04 (0.518).

```bash
python finder.py "What time does the staff canteen open on Fridays?"
```
Out of scope: NOT FOUND (0.255 < 0.40).

Optional failure demo:
```bash
python finder.py "My husband passed away last month, how quickly will you deal with my complaint?" --explain
```
Only 'complaint' is recognised, so CP-02 comes first instead of CP-03 (vulnerable customers).

## 4. Results and what failed (2 min) – show the README results table

* 8/8 right first time on the test questions; keyword baseline 3/8; Euclidean 0/8.
* Stress set written afterwards, with the lexicon frozen: 1/6 right first time (6/6 in the top 3). Failures are all
  unknown synonyms ("passed away", "spending allowance", "owns us").
* 23/23 unit tests; cross-check identical to 6 decimal places.

## 5. Limitation and next step (1 min)

"The tool is only as good as its synonym list: 1/6 on wording it hasn't seen. Next I would swap in a real local
embedding model, keep the ranker, verifier and threshold, and re-run the same 14 questions to compare."

## Likely questions

* *Why 0.40?* Out-of-scope maximum 0.255, main-set minimum 0.725; 0.40 sits in the gap. Raising it gives fewer
  wrong answers and more "not found".
* *Why verify a quote the code cut itself?* It guards against later changes (or a model) altering or inventing a
  quote. The test suite checks that an altered quote is rejected.
* *Why are scores like 0.951 vs 0.937 (Q5) so close?* Near-duplicate topics. The tool finds the topic; the analyst
  confirms the right clause. That is the human review point.
