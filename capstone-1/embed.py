"""
embed.py - turn a policy clause or an analyst's question into a vector.

Two embedders, both offline and standard-library only:

* ConceptEmbedder (default) - the "simple lab embedder" idea from Day 2, built for banking text.
  Each of the first dimensions is a banking CONCEPT (repayment trouble, loan, card, fraud, ...).
  Words and short phrases that belong to a concept add 1 to that dimension, so "cannot pay my EMI"
  and "repayment default" land on the same dimensions although they share no words. Words that no
  concept knows are hashed into a few extra dimensions with a small weight, so specific words still
  count a little.
* KeywordEmbedder - a plain bag of words with no synonyms. It stands in for classic keyword search,
  the approach the business problem says fails. It is used as a baseline in evaluate.py.

A real embedding model (for example fastembed bge-small) would replace ConceptEmbedder; see README,
"Limitations". It could not run on the build machine (onnxruntime needs the Microsoft Visual C++ runtime).
"""
from __future__ import annotations

import re
import zlib

# Words too common to carry meaning on their own.
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "by", "at", "from", "is", "are",
    "was", "be", "been", "it", "its", "this", "that", "these", "those", "i", "my", "me", "we", "our", "you",
    "your", "they", "their", "them", "he", "she", "his", "her", "do", "does", "did", "what", "which", "who",
    "how", "will", "would", "can", "could", "should", "may", "must", "if", "any", "all", "has", "have", "had",
    "there", "as", "so", "but", "about", "into", "than", "then", "up", "out", "need", "want", "customer",
    "bank", "says", "anything", "while", "recently", "after", "before", "each", "every", "such", "only",
}

# Banking concepts and the words / phrases that signal them. Entries are written in plain English and
# stemmed at import time with the same stem() used on the input text, so "charged" matches "charge".
CONCEPTS: dict[str, tuple[str, ...]] = {
    "repayment_trouble": ("cannot pay", "can not pay", "unable to pay", "not able to pay", "not paid",
                          "miss", "missed", "arrears", "default", "overdue", "behind", "late", "struggle",
                          "afford", "unpaid", "not received", "bounced"),
    "loan":              ("loan", "emi", "instalment", "installment", "mortgage", "borrow", "borrower",
                          "principal", "term", "tenure", "repay", "repayment"),
    "card":              ("card", "credit card", "debit card", "contactless", "pin"),
    "charge":            ("fee", "charge", "penalty", "fine", "cost"),
    "fraud":             ("fraud", "fraudulent", "unauthorised", "unauthorized", "scam", "never made",
                          "did not make", "not make", "not recognise", "not recognize", "suspicious",
                          "authorise", "authorize", "gross negligence"),
    "merchant_dispute":  ("dispute", "chargeback", "merchant", "shop", "seller", "store", "goods", "item",
                          "order", "never delivered", "not delivered", "not deliver", "never arrived",
                          "not receive", "did not receive", "charged twice", "wrong amount", "refund",
                          "money back"),
    "complaint":         ("complaint", "complain", "unhappy", "dissatisfied", "not satisfied", "escalate",
                          "ombudsman", "grievance", "poor service"),
    "time_limit":        ("how long", "within", "working day", "deadline", "time limit", "reply",
                          "respond", "response", "acknowledge", "acknowledged", "days", "weeks"),
    "identity":          ("kyc", "identity", "id", "passport", "driving licence", "photo", "document",
                          "proof", "verify", "verified", "verification", "documents"),
    "address":           ("address", "moved", "move house", "moved house", "relocate", "new home",
                          "residential", "house"),
    "hardship":          ("hardship", "lost job", "lost their job", "lost my job", "job loss",
                          "unemployed", "redundant", "redundancy", "income", "break", "pause", "holiday",
                          "defer", "moratorium", "restructure", "restructured", "difficulty"),
    "early_settlement":  ("settle", "settlement", "settled", "pay off", "early", "prepay", "prepayment",
                          "foreclose", "before the end", "in full"),
    "lost_stolen":       ("lost card", "lost or stolen", "stolen", "theft", "block", "blocked", "freeze",
                          "replacement", "missing card", "lost"),
    "credit_limit":      ("credit limit", "limit", "increase my limit", "higher limit", "affordability"),
    "closure":           ("close", "closing", "closed", "closure", "cancel", "terminate", "shut"),
    "dormant":           ("dormant", "inactive", "unused", "not used", "reactivate", "reactivates"),
    "rate_change":       ("variable", "interest rate", "rate", "notice"),
    "business":          ("business", "company", "firm", "beneficial owner", "director"),
    "vulnerable":        ("vulnerable", "bereavement", "illness", "serious illness", "priority", "carer"),
}
CONCEPT_NAMES = list(CONCEPTS)

HASH_DIMS = 32          # extra dimensions for words no concept knows
HASH_WEIGHT = 0.3       # each unknown word counts much less than a concept word
MAX_PHRASE = 3          # longest phrase in the lexicon, in words


def stem(word: str) -> str:
    """Very small suffix stripper so 'charged', 'charges' and 'charge' become the same token."""
    w = word.lower()
    if len(w) <= 3:
        return w
    if w.endswith(("ies", "ied")) and len(w) > 4:
        w = w[:-3] + "y"
    elif w.endswith(("sses", "xes", "ches", "shes")):
        w = w[:-2]
    else:
        for suffix in ("ments", "ment", "ings", "ing", "ed", "s"):
            if w.endswith(suffix) and len(w) - len(suffix) >= 3 and not (suffix == "s" and w.endswith("ss")):
                w = w[: -len(suffix)]
                break
    if w.endswith("e") and len(w) > 3:
        w = w[:-1]
    return w


def tokenize(text: str) -> list[str]:
    """Lower-case, expand negative contractions, split into words and stem each one."""
    t = text.lower().replace("’", "'")
    t = t.replace("can't", "cannot").replace("won't", "will not").replace("n't", " not")
    return [stem(w) for w in re.findall(r"[a-z0-9]+", t)]


def _build_phrase_index() -> dict[tuple[str, ...], list[int]]:
    """Map each stemmed phrase to the concept dimensions it belongs to."""
    index: dict[tuple[str, ...], list[int]] = {}
    for dim, name in enumerate(CONCEPT_NAMES):
        for phrase in CONCEPTS[name]:
            key = tuple(tokenize(phrase))
            index.setdefault(key, [])
            if dim not in index[key]:
                index[key].append(dim)
    return index


PHRASES = _build_phrase_index()


class ConceptEmbedder:
    """Banking concept lexicon + hashed leftover words. Dimension count: concepts + HASH_DIMS."""

    name = f"concept lexicon ({len(CONCEPT_NAMES)} concepts + {HASH_DIMS} hashed word dims)"
    dims = len(CONCEPT_NAMES) + HASH_DIMS

    def concepts_found(self, text: str) -> list[tuple[str, str]]:
        """(phrase, concept) pairs found in the text - used by the CLI's --explain option."""
        found = []
        for phrase, dims in self._matches(tokenize(text)):
            found.extend((" ".join(phrase), CONCEPT_NAMES[d]) for d in dims)
        return found

    def _matches(self, tokens: list[str]):
        """Greedy longest-phrase match: 'lost my job' is read as one phrase, not as 'lost' + 'job'."""
        i = 0
        while i < len(tokens):
            for size in range(MAX_PHRASE, 0, -1):
                key = tuple(tokens[i:i + size])
                if len(key) == size and key in PHRASES:
                    yield key, PHRASES[key]
                    i += size
                    break
            else:
                yield (tokens[i],), []
                i += 1

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dims
        for phrase, dims in self._matches(tokenize(text)):
            if dims:
                for d in dims:
                    vec[d] += 1.0
            elif phrase[0] not in STOPWORDS and phrase[0] not in _STEMMED_STOPWORDS:
                # Unknown word: a small, repeatable nudge on one of the hash dimensions.
                vec[len(CONCEPT_NAMES) + zlib.crc32(phrase[0].encode()) % HASH_DIMS] += HASH_WEIGHT
        return vec


class KeywordEmbedder:
    """Baseline: one dimension per distinct (unstemmed) word in the clause store. No synonyms."""

    name = "keyword baseline (bag of words, no synonyms)"

    def __init__(self, corpus: list[str]):
        words = sorted({w for text in corpus for w in self._words(text)})
        self.vocab = {w: i for i, w in enumerate(words)}
        self.dims = len(words)

    @staticmethod
    def _words(text: str) -> list[str]:
        return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS]

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dims
        for w in self._words(text):
            if w in self.vocab:
                vec[self.vocab[w]] += 1.0
        return vec


_STEMMED_STOPWORDS = {stem(w) for w in STOPWORDS}
