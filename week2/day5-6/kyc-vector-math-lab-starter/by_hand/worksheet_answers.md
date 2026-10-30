# Worksheet answers (worked on paper first, then checked with `python check_by_hand.py`: all 9 match)

P = [3, 4, 0, 0], Q = [6, 8, 0, 0], R = [4, 3, 0, 0], S = [0, 0, 5, 12]

1. **dot(P, R)** = 3×4 + 4×3 + 0×0 + 0×0 = **24**
2. **|P|** = √(9 + 16) = **5**; **|R|** = √(16 + 9) = **5**
3. **cosine(P, R)** = 24 / (5 × 5) = **0.96**
4. **distance(P, R)** = √((3−4)² + (4−3)²) = √2 = **1.414**
5. **P and Q**: cosine = (18 + 32) / (5 × 10) = **1.0**; distance = √(3² + 4²) = **5.0**.
   Cosine says they point the same way: the same *mix* of checks (id and address in the ratio 3 : 4). Distance says they
   are far apart, only because Q has twice as many checks of each kind. To decide "same kind of customer" I would use
   **cosine**, because it compares the profile's shape, not its size.
6. **P and S**: cosine = 0 / (5 × 13) = **0.0**; distance = √(9 + 16 + 25 + 144) = √194 = **13.928**.
   A cosine of 0 means the two have **nothing in common**: P's signals are all id and address checks, S's are all funds
   checks and risk flags. For an analyst, S is a completely different kind of case. With risk flags = 12 it looks like a
   high-risk / source-of-funds review, and nothing learned from P applies to it.

Note: before the fix, `data/hand_vectors.json` had R = [4, 3, 0, 1], so the checker reported 3 differences
(inconsistency #6). The paper answers above were right; the data was wrong.
