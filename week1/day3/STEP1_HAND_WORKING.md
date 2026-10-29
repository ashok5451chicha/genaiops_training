# Step 1 – hand working

Formulas:

* dot(A, B) = a1·b1 + a2·b2 + …
* length |A| = √(a1² + a2² + …)
* cosine = dot(A, B) / (|A| · |B|)
* Euclidean distance = √((a1−b1)² + (a2−b2)² + …), with **one** square root at the end

## E1 – 2-D warm-up: A = [3, 4], B = [4, 3]

* dot = 3·4 + 4·3 = 12 + 12 = **24**
* |A| = √(9 + 16) = √25 = 5;  |B| = √(16 + 9) = 5
* cosine = 24 / (5 · 5) = 24 / 25 = **0.96**
* distance = √((3−4)² + (4−3)²) = √(1 + 1) = √2 = **1.414**

## E2 – same direction, different length: A = [3, 4], B = [6, 8]

* dot = 3·6 + 4·8 = 18 + 32 = **50**
* |A| = 5;  |B| = √(36 + 64) = √100 = 10
* cosine = 50 / (5 · 10) = **1.00** (B is exactly 2 × A, so the direction is identical)
* distance = √((3−6)² + (4−8)²) = √(9 + 16) = √25 = **5.00** (far apart, even though the direction is the same)

## E3 – loan vs mortgage: A = [5, 1, 2, 2], B = [5, 1, 3, 1]

Dimensions: lending, fraud_risk, kyc_compliance, customer_service.

* dot = 25 + 1 + 6 + 2 = **34**
* |loan| = √(25 + 1 + 4 + 4) = √34 ≈ 5.8310;  |mortgage| = √(25 + 1 + 9 + 1) = √36 = 6
* cosine = 34 / (5.8310 · 6) = 34 / 34.986 ≈ **0.972**
* distance = √(0 + 0 + 1 + 1) = √2 ≈ **1.414**

## E4 – loan vs fraud: A = [5, 1, 2, 2], B = [0, 5, 2, 1]

* dot = 0 + 5 + 4 + 2 = **11**
* |loan| ≈ 5.8310;  |fraud| = √(0 + 25 + 4 + 1) = √30 ≈ 5.4772
* cosine = 11 / (5.8310 · 5.4772) = 11 / 31.937 ≈ **0.344**
* distance = √(25 + 16 + 0 + 1) = √42 ≈ **6.481**

## What the numbers say

* E2 is the key lesson: cosine 1.00 (same direction) but distance 5. Cosine ignores length; distance does not.
* loan–mortgage (0.972) are almost the same "meaning"; loan–fraud (0.344) are mostly unrelated. Their only overlap is
  a little KYC and customer service.
