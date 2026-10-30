# Task A – by hand again

Dimensions: lending, fraud_risk, kyc_compliance, customer_service (`data/vectors.json`).

## 1. Prediction (written BEFORE calculating)

1. **KYC and AML**: most similar. Both are compliance controls and are usually handled by the same team.
2. **overdraft and chargeback**: in the middle. Both are everyday account and card servicing, but one is lending and
   the other is a dispute.
3. **complaint and fraud**: least similar. A complaint is about service, fraud is about risk.

## 2. Working

**overdraft [4, 2, 1, 3] and chargeback [1, 4, 1, 3]**

* dot = 4·1 + 2·4 + 1·1 + 3·3 = 4 + 8 + 1 + 9 = **22**
* |overdraft| = √(16 + 4 + 1 + 9) = √30 ≈ 5.4772;  |chargeback| = √(1 + 16 + 1 + 9) = √27 ≈ 5.1962
* cosine = 22 / (5.4772 × 5.1962) = 22 / 28.460 ≈ **0.773**
* distance = √((4−1)² + (2−4)² + 0² + 0²) = √(9 + 4) = √13 ≈ **3.606**

**KYC [1, 1, 5, 1] and AML [0, 4, 4, 0]**

* dot = 0 + 4 + 20 + 0 = **24**
* |KYC| = √(1 + 1 + 25 + 1) = √28 ≈ 5.2915;  |AML| = √(0 + 16 + 16 + 0) = √32 ≈ 5.6569
* cosine = 24 / (5.2915 × 5.6569) = 24 / 29.933 ≈ **0.802**
* distance = √(1 + 9 + 1 + 1) = √12 ≈ **3.464**

**complaint [0, 1, 0, 5] and fraud [0, 5, 2, 1]**

* dot = 0 + 5 + 0 + 5 = **10**
* |complaint| = √(0 + 1 + 0 + 25) = √26 ≈ 5.0990;  |fraud| = √30 ≈ 5.4772
* cosine = 10 / (5.0990 × 5.4772) = 10 / 27.928 ≈ **0.358**
* distance = √(0 + 16 + 4 + 16) = √36 = **6.000**

## 3. Table

| Pair | Dot product | Cosine similarity | Euclidean distance | My prediction (rank 1–3) | Actual rank |
|---|---|---|---|---|---|
| overdraft and chargeback | 22 | 0.773 | 3.606 | 2 | 2 |
| KYC and AML | 24 | 0.802 | 3.464 | 1 | 1 |
| complaint and fraud | 10 | 0.358 | 6.000 | 3 | 3 |

Checked afterwards with `python vector_math.py <word1> <word2>`: all nine numbers agree
(`outputs/taskA_check.txt`).

## 4. Was the prediction right?

Yes, the ranking matched, and cosine and distance agree on the order for these three pairs. What intuition missed is
how close the top two are: KYC–AML (0.802) only just beats overdraft–chargeback (0.773). KYC and AML share *only* the
compliance dimension, and AML's heavy fraud-risk score pulls it away. Two concepts I think of as "the same team" are,
in these numbers, barely more alike than two unrelated servicing products.

*Handwritten working for the submission: copy this page by hand and attach a photo. The assignment asks for a photo or
scan of your own working.*
