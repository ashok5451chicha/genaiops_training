"""
my_vector_math.py  -  YOUR file. Claude Code will write these four functions; YOU will check them.
=================================================================================================
Step 2 of the lab: ask Claude Code to fill in the four functions below. Good prompts are in
CLAUDE_CODE_PROMPTS.md. Rules:

  * Use only Python's standard library (the `math` module is fine). No numpy here - the point is to see the maths.
  * Add a short comment above each line of working so you can explain it.
  * Do NOT copy from vector_math.py - that is the answer key used by the checker.

When you think it is done, run:   python step3_check_my_code.py
"""
from __future__ import annotations

import math


def _check_same_length(a: list[float], b: list[float]) -> None:
    """Shared guard: the maths only makes sense when both vectors have the same number of dimensions."""
    # Compare the number of dimensions; a mismatch means the vectors describe different things.
    if len(a) != len(b):
        raise ValueError(f"vectors have different lengths: {len(a)} and {len(b)}")


def dot(a: list[float], b: list[float]) -> float:
    """Return the dot product of two equal-length vectors."""
    # Refuse vectors of different lengths instead of silently ignoring the extra numbers.
    _check_same_length(a, b)
    # Multiply each pair of matching numbers (a1*b1, a2*b2, ...) and add them all up.
    return sum(x * y for x, y in zip(a, b))


def norm(a: list[float]) -> float:
    """Return the length (magnitude) of a vector."""
    # Pythagoras in any number of dimensions: square every number, add them, take one square root.
    return math.sqrt(sum(x * x for x in a))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Return cosine similarity. Raise ValueError for a zero vector or different lengths."""
    # Same-length check first, so the error message is about the real problem.
    _check_same_length(a, b)
    # Work out both lengths once; they are the denominator.
    length_a, length_b = norm(a), norm(b)
    # A zero vector has no direction, so the angle (and the cosine) is undefined - never divide by zero.
    if length_a == 0 or length_b == 0:
        raise ValueError("cosine similarity is undefined for a zero vector")
    # Cosine = how much the vectors point the same way, with their lengths divided out.
    return dot(a, b) / (length_a * length_b)


def euclidean_distance(a: list[float], b: list[float]) -> float:
    """Return straight-line distance. Raise ValueError for different lengths."""
    # Distance between points in different spaces has no meaning.
    _check_same_length(a, b)
    # Subtract matching numbers, square each gap, add them, then take ONE square root at the end.
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def nearest(query: list[float], candidates: dict[str, list[float]], metric: str = "cosine") -> list[str]:
    """
    Return candidate names sorted from most to least similar to the query.

    metric "cosine": higher is more similar. metric "euclidean": lower is more similar.
    Ties keep the order the candidates were given in (Python's sort is stable). An empty dict gives [].
    Raises ValueError for an unknown metric, and names the candidate when one cannot be compared.
    """
    # Refuse anything else: version 1 silently treated ANY other string (e.g. a typo) as euclidean.
    if metric not in ("cosine", "euclidean"):
        raise ValueError(f"unknown metric {metric!r}: use 'cosine' or 'euclidean'")
    # Pick the scoring function, and whether a bigger score means "more similar".
    score_fn, higher_is_better = (cosine_similarity, True) if metric == "cosine" else (euclidean_distance, False)
    scores = {}
    for name, vec in candidates.items():
        try:
            # Score each candidate against the query.
            scores[name] = score_fn(query, vec)
        except ValueError as exc:
            # Say WHICH candidate failed (zero vector, wrong length) instead of a bare error.
            raise ValueError(f"cannot compare candidate {name!r}: {exc}") from exc
    # Sort names by score; reverse for cosine so the most similar comes first.
    return sorted(scores, key=scores.get, reverse=higher_is_better)
