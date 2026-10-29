"""
taskE_and_stretch.py  -  Task E (a misleading high score) and the three stretch tasks, using MY functions.

    python taskE_and_stretch.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import my_vector_math as m

SCENARIO = json.loads(Path("data/my_scenario.json").read_text(encoding="utf-8"))
ITEMS = SCENARIO["items"]
DIMS = SCENARIO["dimensions"]


def centroid(vectors: list[list[float]]) -> list[float]:
    """Stretch 2: the average vector (the 'centre') of a group. Raises ValueError for an empty or ragged list."""
    # An empty group has no centre.
    if not vectors:
        raise ValueError("cannot take the centroid of an empty list")
    # Every vector must have the same number of dimensions.
    if len({len(v) for v in vectors}) != 1:
        raise ValueError("all vectors must have the same length")
    # Average each dimension separately.
    return [sum(column) / len(vectors) for column in zip(*vectors)]


def unit(v: list[float]) -> list[float]:
    """Scale a vector to length 1 (same direction)."""
    length = m.norm(v)
    return [x / length for x in v]


def task_e() -> None:
    print("TASK E - close vectors, opposite meaning")
    pairs = [
        ("KYC scenario", DIMS, "Address matches records", [0, 5, 0, 2], "Address does NOT match records", [0, 5, 0, 3]),
        ("toy lending space", ["lending", "fraud_risk", "kyc_compliance", "customer_service"],
         "Approve the loan", [5, 1, 2, 2], "Decline the loan", [5, 2, 2, 2]),
    ]
    for space, dims, a_name, a, b_name, b in pairs:
        print(f"  [{space}] dims={dims}")
        print(f"    {a_name:<32}{a}")
        print(f"    {b_name:<32}{b}")
        print(f"    cosine = {m.cosine_similarity(a, b):.3f}   distance = {m.euclidean_distance(a, b):.3f}")
    print()


def stretch_identity() -> None:
    a, b = ITEMS["Blurred ID scan"], ITEMS["Missing field"]
    ua, ub = unit(a), unit(b)
    cos = m.cosine_similarity(a, b)
    d2 = m.euclidean_distance(ua, ub) ** 2
    print("STRETCH 1 - on unit vectors, distance^2 = 2 - 2 x cosine  (Blurred ID scan vs Missing field)")
    print(f"  lengths after normalising: {m.norm(ua):.4f}, {m.norm(ub):.4f}")
    print(f"  cosine = {cos:.4f}   distance^2 (unit) = {d2:.4f}   2 - 2 x cosine = {2 - 2 * cos:.4f}   "
          f"equal: {math.isclose(d2, 2 - 2 * cos)}\n")


def stretch_centroid() -> None:
    # Drift idea (scenario 4): compare the centre of last month's cases with this month's.
    last_month = [ITEMS["Passport scan"], ITEMS["Utility bill"], ITEMS["Salary slip"]]          # mostly clean documents
    this_month = [ITEMS["Blurred ID scan"], ITEMS["Missing field"], ITEMS["Conflicting address"]]  # mostly problems
    c1, c2 = centroid(last_month), centroid(this_month)
    print("STRETCH 2 - centroids (the idea behind a drift check)")
    print(f"  last month centre : {[round(x, 2) for x in c1]}")
    print(f"  this month centre : {[round(x, 2) for x in c2]}")
    print(f"  cosine between centres = {m.cosine_similarity(c1, c2):.3f}   distance = {m.euclidean_distance(c1, c2):.3f}")
    print("  The data_quality dimension moved from 0 to 4.33: the mix of work has shifted towards remediation.\n")


def stretch_sensitivity() -> None:
    base_a, base_b = ITEMS["Utility bill"], ITEMS["Conflicting address"]
    base = m.cosine_similarity(base_a, base_b)
    print(f"STRETCH 3 - change one number of 'Utility bill' by +/-1 or 2 (vs Conflicting address, base cosine {base:.3f})")
    print(f"  {'dimension':<20}{'-2':>8}{'-1':>8}{'+1':>8}{'+2':>8}")
    for i, dim in enumerate(DIMS):
        row = []
        for delta in (-2, -1, 1, 2):
            v = list(base_a)
            v[i] = v[i] + delta
            row.append("n/a" if v[i] < 0 or v[i] > 5 or all(x == 0 for x in v)
                       else f"{m.cosine_similarity(v, base_b) - base:+.3f}")
        print(f"  {dim:<20}" + "".join(f"{x:>8}" for x in row))
    print("  Biggest move: data_quality (+0.21 for +2), where Conflicting address is large (4) and Utility bill is 0.")
    print("  Raising a dimension the other item scores 0 on (identity, income) only lengthens the vector: cosine drops.")
    print("  So a dimension's weight depends on the OTHER vector: raising a number helps most where the OTHER item is large.")


if __name__ == "__main__":
    task_e()
    stretch_identity()
    stretch_centroid()
    stretch_sensitivity()
