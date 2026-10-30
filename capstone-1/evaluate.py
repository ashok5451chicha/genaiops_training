"""
evaluate.py - run the test questions and report honest counts.

For every question it records the top-3 clauses and whether the expected clause is first ("right first
time") or anywhere in the top 3. It compares three rankings on the same questions:

  1. concept embedder + cosine     (the tool as shipped)
  2. concept embedder + euclidean  (same vectors, different metric: shows why cosine is used)
  2b. euclidean on unit-length vectors (must rank exactly like cosine: d^2 = 2 - 2cos, Day 3)
  3. keyword baseline + cosine     (no synonyms: the "keyword search fails" business problem;
                                    ranking only, no threshold, because its scores sit on a different scale)

It also checks the out-of-scope questions return "not found", and prints the score distribution used to
choose the threshold. Output: the terminal and results/test_results.md.

    python evaluate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from embed import ConceptEmbedder, KeywordEmbedder
from finder import ClauseFinder, load_clauses
from rank import norm

HERE = Path(__file__).resolve().parent
QUESTIONS_FILE = HERE / "data" / "test_questions.json"
RESULTS_FILE = HERE / "results" / "test_results.md"


class UnitConceptEmbedder(ConceptEmbedder):
    """The same concept vectors scaled to length 1 (only used to compare metrics)."""

    name = "concept lexicon, unit length"

    def embed(self, text: str) -> list[float]:
        vec = super().embed(text)
        n = norm(vec)
        return [x / n for x in vec] if n else vec


def run(finder: ClauseFinder, questions: list[dict], metric: str = "cosine") -> list[dict]:
    rows = []
    for q in questions:
        answer = finder.search(q["question"], metric=metric)
        top_ids = [r["id"] for r in answer["results"]]
        rows.append({
            **q,
            "top3": answer["results"],
            "status": answer["status"],
            "best_score": answer["best_score"],
            "first": bool(top_ids) and top_ids[0] == q["expected"] and answer["status"] == "found",
            "in_top3": q["expected"] in top_ids,
            "quotes_verified": all(r["quote_verified"] for r in answer["results"]),
        })
    return rows


def fmt_top3(row: dict, metric: str = "cosine") -> str:
    key = "score" if metric == "cosine" else "euclidean"
    return ", ".join(f"{r['id']} {r[key]:.3f}" for r in row["top3"])


def table(rows: list[dict], metric: str = "cosine") -> list[str]:
    lines = ["| # | Question | Expected | Top 3 (" + ("cosine" if metric == "cosine" else "distance")
             + ") | Right first time | In top 3 |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['id']} | {r['question']} | {r['expected']} | {fmt_top3(r, metric)} | "
                     f"{'yes' if r['first'] else '**no**'} | {'yes' if r['in_top3'] else '**no**'} |")
    return lines


def count(rows: list[dict], key: str) -> str:
    return f"{sum(r[key] for r in rows)}/{len(rows)}"


def main() -> int:
    data = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    main_q, stress_q, oos_q = data["questions"], data.get("stress_set", []), data["out_of_scope"]
    clauses = load_clauses()

    tool = ClauseFinder(clauses)
    unit = ClauseFinder(clauses, embedder=UnitConceptEmbedder())
    keyword = ClauseFinder(clauses, embedder=KeywordEmbedder([c["title"] + ". " + c["text"] for c in clauses]),
                           threshold=0.0)

    main_cos = run(tool, main_q)
    main_euc = run(tool, main_q, metric="euclidean")
    main_unit = run(unit, main_q, metric="euclidean")
    main_kw = run(keyword, main_q)
    stress_cos = run(tool, stress_q)
    oos = run(tool, oos_q)
    oos_ok = sum(r["status"] == "not_found" for r in oos)

    in_scope_best = [r["best_score"] for r in main_cos + stress_cos]
    oos_best = [r["best_score"] for r in oos]

    out = [
        "# Policy Clause Finder - test results",
        "",
        f"Embedder: `{tool.embedder.name}` · threshold for \"not found\": **{tool.threshold:.2f}** (cosine) · "
        f"{len(clauses)} clauses",
        "",
        "## Summary",
        "",
        "| Test set | Ranking | Right first time | In top 3 |",
        "|---|---|---|---|",
        f"| 8 main questions | concept embedder + **cosine** (the tool) | **{count(main_cos, 'first')}** | {count(main_cos, 'in_top3')} |",
        f"| 8 main questions | concept embedder + euclidean | {count(main_euc, 'first')} | {count(main_euc, 'in_top3')} |",
        f"| 8 main questions | concept embedder, unit-length vectors + euclidean | {count(main_unit, 'first')} | {count(main_unit, 'in_top3')} |",
        f"| 8 main questions | keyword baseline + cosine | {count(main_kw, 'first')} | {count(main_kw, 'in_top3')} |",
        f"| 6 stress questions (unknown words, not tuned) | concept embedder + cosine | **{count(stress_cos, 'first')}** | {count(stress_cos, 'in_top3')} |",
        f"| 2 out-of-scope questions | must say \"not found\" | {oos_ok}/{len(oos)} | - |",
        "",
        f"Every quote shown was verified verbatim in its source clause: "
        f"{'yes' if all(r['quotes_verified'] for r in main_cos + stress_cos + oos) else '**NO**'}.",
        "",
        "## 1. Main test set: the tool (concept embedder + cosine)",
        "",
        *table(main_cos),
        "",
        "## 2. Same questions ranked by Euclidean distance",
        "",
        *table(main_euc, "euclidean"),
        "",
        "## 3. Same questions with the keyword baseline (no synonyms)",
        "",
        *table(main_kw),
        "",
        "## 4. Stress set (written after the main set scored, lexicon not changed afterwards)",
        "",
        *table(stress_cos),
        "",
        "## 5. Out-of-scope questions",
        "",
        "| # | Question | Result | Best cosine |",
        "|---|---|---|---|",
        *[f"| {r['id']} | {r['question']} | {r['status'].replace('_', ' ')} | {r['best_score']:.3f} |" for r in oos],
        "",
        "## 6. Score distribution (used to choose the threshold)",
        "",
        f"* Best score of each in-scope question (main + stress): min **{min(in_scope_best):.3f}**, "
        f"max {max(in_scope_best):.3f}",
        f"* Best score of each out-of-scope question: max **{max(oos_best):.3f}**",
        f"* Main-set best scores: min **{min(r['best_score'] for r in main_cos):.3f}**. Threshold "
        f"**{tool.threshold:.2f}** sits between the out-of-scope maximum and the main-set minimum.",
        "* In-scope questions answered \"not found\" (below the threshold; a safe failure, the analyst is sent "
        "to the policy team): " + (", ".join(f"{r['id']} ({r['best_score']:.3f})" for r in main_cos + stress_cos
                                            if r["status"] == "not_found") or "none"),
        "",
    ]
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    RESULTS_FILE.write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    print(f"Saved: {RESULTS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
