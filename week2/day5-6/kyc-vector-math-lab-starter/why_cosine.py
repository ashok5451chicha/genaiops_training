"""
why_cosine.py - four small experiments that show WHY we use cosine similarity, and how it relates to distance.

    python why_cosine.py
"""
import json
from pathlib import Path

from embedder import embed
from vector_math import cosine_similarity, euclidean_distance, normalize

V = json.loads((Path(__file__).resolve().parent / "data" / "hand_vectors.json").read_text(encoding="utf-8"))
P, Q, R, S = V["P"], V["Q"], V["R"], V["S"]

print(f"1. Direction versus size:  P={P} and Q={Q} (Q is P doubled)")
print(f"   cosine = {cosine_similarity(P, Q):.3f}  (same direction)   distance = {euclidean_distance(P, Q):.3f}  (far apart)")
print("   The same kind of customer can look 'far' on distance only because one record has more of everything.\n")

short = "address proof expired"
long = "the address proof is expired, the utility bill is outdated, the lease is old, the residence proof has lapsed"
a, b = embed(short), embed(long)
print("2. A short note and a long note about the same topic")
print(f"   cosine = {cosine_similarity(a, b):.3f}   distance = {euclidean_distance(a, b):.3f}")
print("   Cosine says 'same topic'. Distance is large because the long note simply has bigger numbers.\n")

print("3. The link between the two: after scaling to length 1, distance^2 = 2 - 2 x cosine")
ua, ub = normalize(a), normalize(b)
d = euclidean_distance(ua, ub)
print(f"   distance on unit vectors = {d:.3f}   so distance^2 = {d*d:.3f}   and 2 - 2 x cosine = {2 - 2 * cosine_similarity(a, b):.3f}\n")

print(f"4. Unrelated: P={P} and S={S}")
print(f"   cosine = {cosine_similarity(P, S):.3f}  (nothing in common, right angles)")
