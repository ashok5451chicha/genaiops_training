"""
vector_math.py - the mathematics of "closeness", written from scratch (standard library only).

    dot(a, b)                 multiply matching numbers, then add them up
    norm(a)                   length of a vector (Pythagoras in many dimensions)
    normalize(a)              the same direction, but length exactly 1
    cosine_similarity(a, b)   do the vectors point the SAME WAY?   -1 .. 1   (higher = more similar)
                              (0 .. 1 for this project: every embedder value is >= 0, so no angle passes 90 degrees)
    euclidean_distance(a, b)  how FAR APART are the end points?    0 .. infinity (lower = more similar)

Worked example, a = (3, 4), b = (4, 3):
    dot = 3*4 + 4*3 = 24        |a| = |b| = 5        cosine = 24 / (5*5) = 0.96
    distance = sqrt((3-4)^2 + (4-3)^2) = sqrt(2) = 1.414
"""
import math


def _same_length(a, b):
    if len(a) != len(b):
        raise ValueError(f"Vectors must have the same length (got {len(a)} and {len(b)})")


def dot(a, b):
    """a1*b1 + a2*b2 + ..."""
    _same_length(a, b)
    return sum(x * y for x, y in zip(a, b))   # pair up matching positions, multiply each pair, add them all


def norm(a):
    """Length of a vector: square root of (a1^2 + a2^2 + ...)."""
    return math.sqrt(sum(x * x for x in a))   # square root of the sum of squares (Pythagoras)


def normalize(a):
    """Scale a vector to length 1 (same direction). A zero vector has no direction, so it is an error."""
    length = norm(a)
    if length == 0:
        raise ValueError("Cannot normalize a zero vector: it has no direction")
    return [x / length for x in a]            # same direction, length exactly 1


def cosine_similarity(a, b):
    """cos(angle) = (a . b) / (|a| x |b|).  1 = same direction, 0 = at right angles, -1 = opposite."""
    _same_length(a, b)
    la, lb = norm(a), norm(b)
    if la == 0 or lb == 0:
        raise ValueError("Cosine similarity is undefined for a zero vector (it has no direction)")
    return dot(a, b) / (la * lb)


def euclidean_distance(a, b):
    """Straight-line distance: sqrt((a1-b1)^2 + (a2-b2)^2 + ...)."""
    _same_length(a, b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))   # squared gaps, added, then square root
