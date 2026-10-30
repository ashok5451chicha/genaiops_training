"""
finder.py - Policy Clause Finder: command-line entry point.

    python finder.py "Customer cannot pay their EMI this month"
    python finder.py "..." --explain        # also show which banking concepts were recognised
    python finder.py "..." --json           # machine-readable output
    python finder.py --interactive          # ask several questions in a row

Pipeline: question -> embed (embed.py) -> rank clauses by cosine, top 3 (rank.py)
          -> pick and verify the quote (verify.py) -> print clause ID, score and verified quote.
If the best score is below THRESHOLD the answer is "not found" and the analyst is sent to the policy team.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from embed import ConceptEmbedder
from rank import euclidean_distance, rank
from verify import best_snippet, verify_quote

HERE = Path(__file__).resolve().parent
CLAUSES_FILE = HERE / "data" / "clauses.json"

# Below this cosine score the best clause is treated as "not found". Chosen from the score distribution in
# results/test_results.md: every in-scope test question's best score is well above it and both out-of-scope
# questions are below it. See README, "Choosing the threshold".
THRESHOLD = 0.40
TOP_K = 3


def load_clauses(path: Path = CLAUSES_FILE) -> list[dict]:
    """Load and validate the clause store: id, title and text present, ids unique."""
    data = json.loads(path.read_text(encoding="utf-8"))
    clauses = data["clauses"] if isinstance(data, dict) else data
    seen = set()
    for c in clauses:
        for field in ("id", "title", "text"):
            if not str(c.get(field, "")).strip():
                raise ValueError(f"clause {c.get('id', '?')} has no {field}")
        if c["id"] in seen:
            raise ValueError(f"duplicate clause id {c['id']}")
        seen.add(c["id"])
    return clauses


class ClauseFinder:
    def __init__(self, clauses: list[dict] | None = None, embedder=None, threshold: float = THRESHOLD):
        self.clauses = clauses if clauses is not None else load_clauses()
        self.by_id = {c["id"]: c for c in self.clauses}
        self.embedder = embedder or ConceptEmbedder()
        self.threshold = threshold
        # Clauses are embedded once, title + text together (the title often carries the key concept).
        self.vectors = [(c["id"], self.embedder.embed(c["title"] + ". " + c["text"])) for c in self.clauses]

    def search(self, question: str, top_k: int = TOP_K, metric: str = "cosine") -> dict:
        qvec = self.embedder.embed(question)
        ranked = rank(qvec, self.vectors, top_k=top_k, metric=metric)
        vec_by_id = dict(self.vectors)
        results = []
        for clause_id, score in ranked:
            clause = self.by_id[clause_id]
            quote = best_snippet(qvec, clause["text"], self.embedder.embed)
            verified = verify_quote(quote, clause["text"])
            results.append({
                "id": clause_id,
                "title": clause["title"],
                "score": round(score, 4),
                "euclidean": round(euclidean_distance(qvec, vec_by_id[clause_id]), 4),
                "quote": quote if verified else None,   # an unverified quote is never shown
                "quote_verified": verified,
            })
        best = results[0]["score"] if results else 0.0
        found = bool(results) and (metric != "cosine" or best >= self.threshold)
        return {"question": question, "metric": metric, "threshold": self.threshold,
                "status": "found" if found else "not_found", "best_score": best, "results": results}


def print_answer(answer: dict, finder: ClauseFinder, explain: bool = False) -> None:
    print(f"\nQuestion : {answer['question']}")
    print(f"Embedder : {finder.embedder.name}")
    if explain:
        found = finder.embedder.concepts_found(answer["question"])
        print("Concepts : (stemmed words -> banking concept) " + (", ".join(f"'{p}' -> {c}" for p, c in found) or "(none recognised)"))
    if answer["status"] == "not_found":
        print(f"\nNOT FOUND - best cosine score {answer['best_score']:.3f} is below the threshold "
              f"{answer['threshold']:.2f}.")
        print("No clause is a reliable match. Check the policy library manually or ask the policy team.")
        if answer["results"]:
            print("(Closest clauses, for information only: "
                  + ", ".join(f"{r['id']} {r['score']:.3f}" for r in answer["results"]) + ")")
        return
    print()
    for n, r in enumerate(answer["results"], 1):
        print(f" #{n}  {r['id']:<6} {r['title']}")
        print(f"      cosine {r['score']:.3f}   (euclidean distance {r['euclidean']:.3f})")
        if r["quote_verified"]:
            print(f"      Quote [verified in {r['id']}]: \"{r['quote']}\"")
        else:
            print("      Quote withheld: it could not be verified against the source clause.")
    print("\nHuman review: read the full clause before replying to the customer; the score shows "
          "similarity, not that the clause answers the question.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find the policy clauses that answer an analyst's question.")
    parser.add_argument("question", nargs="*", help="the question, in any wording")
    parser.add_argument("--top", type=int, default=TOP_K, help="how many clauses to return (default 3)")
    parser.add_argument("--threshold", type=float, default=THRESHOLD, help="'not found' below this cosine")
    parser.add_argument("--explain", action="store_true", help="show the banking concepts recognised")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    parser.add_argument("--interactive", action="store_true", help="ask questions until an empty line")
    args = parser.parse_args(argv)

    finder = ClauseFinder(threshold=args.threshold)
    questions = [" ".join(args.question)] if args.question else []
    if args.interactive:
        print("Policy Clause Finder - type a question, or press Enter on an empty line to stop.")
        while True:
            try:
                q = input("\n> ").strip()
            except EOFError:
                break
            if not q:
                break
            print_answer(finder.search(q, top_k=args.top), finder, args.explain)
        return 0
    if not questions or not questions[0].strip():
        parser.error("give a question, for example: python finder.py \"I cannot pay my EMI\"")
    answer = finder.search(questions[0], top_k=args.top)
    if args.json:
        print(json.dumps(answer, indent=2))
    else:
        print_answer(answer, finder, args.explain)
    return 0


if __name__ == "__main__":
    sys.exit(main())
