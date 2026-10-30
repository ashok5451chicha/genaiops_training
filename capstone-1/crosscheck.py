"""
crosscheck.py - check the hand-written cosine (rank.py) against library functions on two examples.

Libraries: numpy (required, see requirements.txt) and scikit-learn (used if installed). The hand-written
result must match each library to 3 decimal places (the acceptance criterion).

    python crosscheck.py
"""
from __future__ import annotations

import sys

import numpy as np

from finder import ClauseFinder
from rank import cosine_similarity, euclidean_distance

EXAMPLES = [
    ("Customer says they cannot pay their EMI this month. What happens to the loan?", "LN-01"),
    ("I paid my credit card bill two days late, will I be charged anything?", "CC-03"),
]


def main() -> int:
    finder = ClauseFinder()
    vectors = dict(finder.vectors)
    try:
        from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
    except ImportError:
        sk_cosine = None

    all_ok = True
    for question, clause_id in EXAMPLES:
        q = finder.embedder.embed(question)
        c = vectors[clause_id]
        mine = cosine_similarity(q, c)
        qa, ca = np.array(q), np.array(c)
        lib = float(np.dot(qa, ca) / (np.linalg.norm(qa) * np.linalg.norm(ca)))
        dist_mine, dist_lib = euclidean_distance(q, c), float(np.linalg.norm(qa - ca))
        print(f"Question: {question}\nClause  : {clause_id}")
        print(f"  cosine    hand-written {mine:.6f} | numpy {lib:.6f}", end="")
        checks = [round(mine, 3) == round(lib, 3)]
        if sk_cosine is not None:
            sk = float(sk_cosine([q], [c])[0][0])
            print(f" | scikit-learn {sk:.6f}", end="")
            checks.append(round(mine, 3) == round(sk, 3))
        print(f"\n  euclidean hand-written {dist_mine:.6f} | numpy {dist_lib:.6f}")
        checks.append(round(dist_mine, 3) == round(dist_lib, 3))
        ok = all(checks)
        all_ok &= ok
        print(f"  match to 3 decimal places: {'YES' if ok else 'NO'}\n")
    if sk_cosine is None:
        print("(scikit-learn not installed: checked against numpy only)")
    print("RESULT:", "all match" if all_ok else "MISMATCH")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
