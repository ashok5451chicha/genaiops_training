"""
rank.py - the vector maths, written by hand (no numpy), and the top-k ranker.

    dot(a, b)       = a1*b1 + a2*b2 + ... + an*bn
    norm(a)         = sqrt(dot(a, a))                 (the length of the arrow)
    cosine(a, b)    = dot(a, b) / (norm(a) * norm(b))  (1 = same direction, 0 = unrelated)
    euclidean(a, b) = sqrt((a1-b1)^2 + ... + (an-bn)^2) (straight-line distance; lower = closer)

Cosine is the ranking metric because it compares DIRECTION only: a long clause and a short question about
the same topic point the same way even though the clause's vector is much longer. Euclidean distance is
also reported so the difference can be seen (evaluate.py ranks with both).
"""
from __future__ import annotations

import math


def _check_same_length(a: list[float], b: list[float]) -> None:
    if len(a) != len(b):
        raise ValueError(f"vectors have different lengths: {len(a)} and {len(b)}")


def dot(a: list[float], b: list[float]) -> float:
    _check_same_length(a, b)
    total = 0.0
    for x, y in zip(a, b):      # multiply matching positions and add them up
        total += x * y
    return total


def norm(a: list[float]) -> float:
    return math.sqrt(dot(a, a))  # length of the vector: Pythagoras in n dimensions


def cosine_similarity(a: list[float], b: list[float]) -> float:
    na, nb = norm(a), norm(b)
    if na == 0 or nb == 0:
        raise ValueError("cosine similarity is undefined for a zero vector")
    return dot(a, b) / (na * nb)


def euclidean_distance(a: list[float], b: list[float]) -> float:
    _check_same_length(a, b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def rank(query_vec: list[float], items: list[tuple[str, list[float]]], top_k: int = 3,
         metric: str = "cosine") -> list[tuple[str, float]]:
    """
    Rank (item_id, vector) pairs against the query.

    metric="cosine": highest score first. metric="euclidean": smallest distance first.
    Ties keep the input order (Python's sort is stable). Returns [] when the query vector is all zeros
    (no recognisable words), which the finder reports as "not found".
    """
    if metric not in ("cosine", "euclidean"):
        raise ValueError(f"unknown metric {metric!r}: use 'cosine' or 'euclidean'")
    if norm(query_vec) == 0:
        return []
    if metric == "cosine":
        scored = [(item_id, cosine_similarity(query_vec, vec)) for item_id, vec in items if norm(vec) > 0]
        scored.sort(key=lambda pair: -pair[1])
    else:
        scored = [(item_id, euclidean_distance(query_vec, vec)) for item_id, vec in items]
        scored.sort(key=lambda pair: pair[1])
    return scored[:top_k]
