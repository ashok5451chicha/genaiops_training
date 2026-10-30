"""
embedder.py - turn an analyst note or a customer profile into a vector (a toy, explainable stand-in for a real model).

    text -> lower-case -> split into words -> drop stop-words -> light stemming
         -> each word that is in the KYC lexicon (data/concepts.json) switches on its CONCEPT dimension
         -> every other word (names, streets) falls into one of 16 hashed buckets (BUCKETS), so names still leave a fingerprint

So "passport spelling differs" and "licence name mismatch" end up close, because both switch on identity and mismatch
concepts, even though the words are different. A real embedding model learns this from data; here a small lexicon does it,
which makes every number explainable.
"""
import json
import re
import zlib
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
CONCEPTS = json.loads((DATA / "concepts.json").read_text(encoding="utf-8"))
CONCEPT_NAMES = list(CONCEPTS)
BUCKETS = 16
DIM = len(CONCEPT_NAMES) + BUCKETS
STOPWORDS = set("a an the is are was were be to of for in on at by with and or my it this that as if so not no any "
                "from has have had do does their our your we they them there which who".split())


def stem(word):
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)]
    return word


def tokenize(text):
    """Lower-case, letters and digits only, no stop-words, light stemming."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [stem(w) for w in words if w not in STOPWORDS and len(w) > 1]


_LOOKUP = {}
for _i, _name in enumerate(CONCEPT_NAMES):
    for _w in CONCEPTS[_name]:
        _LOOKUP.setdefault(stem(_w), set()).add(_i)


def embed(text, bucket_weight=0.5):
    """text -> list of DIM numbers. An empty text gives the all-zero vector (it has no direction)."""
    vec = [0.0] * DIM
    for tok in tokenize(text):
        hits = _LOOKUP.get(tok)
        if hits:
            for i in hits:
                vec[i] += 1.0
        else:
            vec[len(CONCEPT_NAMES) + zlib.crc32(tok.encode()) % BUCKETS] += bucket_weight
    return vec
