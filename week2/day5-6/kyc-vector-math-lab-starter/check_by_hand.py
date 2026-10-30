"""
check_by_hand.py - compares YOUR hand-worked answers (by_hand/my_answers.json) with what vector_math.py computes.
If the two disagree, ONE of them is wrong. Redo your arithmetic first; if you are sure you are right, suspect the code.
"""
import json
from pathlib import Path

from vector_math import cosine_similarity, dot, euclidean_distance, norm

ROOT = Path(__file__).resolve().parent
V = json.loads((ROOT / "data" / "hand_vectors.json").read_text(encoding="utf-8"))
P, Q, R, S = V["P"], V["Q"], V["R"], V["S"]
mine = json.loads((ROOT / "by_hand" / "my_answers.json").read_text(encoding="utf-8"))

checks = {
    "p_r_dot": dot(P, R), "p_norm": norm(P), "r_norm": norm(R),
    "p_r_cosine": cosine_similarity(P, R), "p_r_distance": euclidean_distance(P, R),
    "p_q_cosine": cosine_similarity(P, Q), "p_q_distance": euclidean_distance(P, Q),
    "p_s_cosine": cosine_similarity(P, S), "p_s_distance": euclidean_distance(P, S),
}
bad = 0
print(f"{'Item':<14}{'your answer':>13}{'code says':>12}  Result")
for key, code_value in checks.items():
    ans = mine.get(key)
    ok = ans is not None and abs(ans - code_value) < 0.01
    bad += not ok
    print(f"{key:<14}{ans if ans is not None else '(blank)':>13}{code_value:>12.3f}  {'MATCH' if ok else 'DIFFERENT - investigate'}")
print("\nAll answers match." if not bad else f"\n{bad} answer(s) differ. Who is wrong: you, or the code?")
