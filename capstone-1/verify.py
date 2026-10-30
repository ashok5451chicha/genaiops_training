"""
verify.py - make sure every quote shown to the analyst really exists in the source clause.

The finder picks the sentence of a clause that best matches the question and shows it as the quote. Before
it is shown, verify_quote() checks it is a VERBATIM substring of the clause text in the clause store
(exact characters, nothing reworded). This is the same guard used on model output on Day 2: today the quote
is cut from the clause by code, but if a model (or a later change) ever produced or edited the quote, an
invented or altered quote would be caught here instead of reaching a customer.
"""
from __future__ import annotations

import re

from rank import cosine_similarity

_SENTENCE_END = re.compile(r"(?<=[.!?;])\s+")


def split_sentences(text: str) -> list[str]:
    """Split clause text into sentences (or ';'-separated parts). Every part is cut from the original text."""
    return [part for part in _SENTENCE_END.split(text.strip()) if part]


def verify_quote(quote: str, source_text: str) -> bool:
    """True only if the quote appears character for character in the source text."""
    return bool(quote) and quote in source_text


def best_snippet(question_vec: list[float], clause_text: str, embed) -> str:
    """The sentence of the clause most similar to the question (first sentence if none scores)."""
    sentences = split_sentences(clause_text)
    best, best_score = sentences[0], -1.0
    for sentence in sentences:
        vec = embed(sentence)
        try:
            score = cosine_similarity(question_vec, vec)
        except ValueError:          # sentence with no recognisable words
            continue
        if score > best_score:
            best, best_score = sentence, score
    return best
