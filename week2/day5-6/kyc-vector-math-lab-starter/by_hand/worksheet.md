# By-hand worksheet: four KYC "signal" vectors

Each vector summarises a customer's KYC checks: `[id_checks_passed, address_checks_passed, funds_checks_passed, risk_flags]`.
Do these on paper FIRST. Write your answers in `by_hand/my_answers.json`, then run `python check_by_hand.py`.

| Customer | Vector |
|---|---|
| P | [3, 4, 0, 0] |
| Q | [6, 8, 0, 0] |
| R | [4, 3, 0, 0] |
| S | [0, 0, 5, 12] |

1. Dot product of P and R.
2. Length (norm) of P, and of R.
3. Cosine similarity of P and R = dot / (length x length).
4. Euclidean distance between P and R.
5. Cosine similarity and Euclidean distance between P and Q. Q is P doubled. What does each number say? Which one would you use to decide "same kind of customer"?
6. Cosine similarity of P and S, and distance. What does a cosine of 0 mean for a KYC analyst?

Formulae
* dot(a, b) = a1*b1 + a2*b2 + ...
* norm(a) = square root of (a1^2 + a2^2 + ...)
* cosine(a, b) = dot(a, b) / (norm(a) * norm(b))
* distance(a, b) = square root of ((a1-b1)^2 + (a2-b2)^2 + ...)
