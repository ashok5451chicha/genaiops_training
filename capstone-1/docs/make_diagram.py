"""Draw docs/architecture.png (needs matplotlib, only for regenerating the picture):  python docs/make_diagram.py"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

BOXES = {  # name: (x, y, label, colour)
    "q":      (0.6, 2.2, "Analyst question\n(CLI: finder.py)", "#dbe8f6"),
    "embed":  (2.9, 2.2, "Embed\n(embed.py)\nconcept lexicon", "#dbe8f6"),
    "store":  (2.9, 0.6, "Clause store\n(data/clauses.json)\n19 synthetic clauses", "#fdf1c7"),
    "rank":   (5.2, 2.2, "Rank\n(rank.py)\ncosine by hand, top 3", "#dbe8f6"),
    "verify": (7.5, 2.2, "Verify quote\n(verify.py)\nverbatim in source", "#dbe8f6"),
    "out":    (9.8, 2.2, "Answer: clause ID\n+ score + quote\nor NOT FOUND", "#d9f0dc"),
    "check":  (5.2, 0.6, "Cross-check\n(crosscheck.py)\nnumpy / scikit-learn", "#eeeeee"),
}
W, H = 1.9, 1.0

fig, ax = plt.subplots(figsize=(12, 4))
ax.set_xlim(-0.5, 11.3)
ax.set_ylim(-0.2, 3.3)
ax.axis("off")
ax.set_title("Policy Clause Finder - architecture", fontsize=14)
for x, y, label, colour in BOXES.values():
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.05",
                                fc=colour, ec="#33475b"))
    ax.text(x, y, label, ha="center", va="center", fontsize=9)


def arrow(a, b, style="-", text=None):
    (x1, y1, *_), (x2, y2, *_) = BOXES[a], BOXES[b]
    if y1 == y2:
        start, end = (x1 + W / 2 + 0.05, y1), (x2 - W / 2 - 0.05, y2)
    else:
        start, end = (x1 + (0.4 if x2 > x1 else 0), y1 + H / 2 + 0.05), (x2 - (0.4 if x2 > x1 else 0), y2 - H / 2 - 0.05)
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, color="#33475b", linestyle=style))
    if text:
        ax.text((start[0] + end[0]) / 2 + 0.1, (start[1] + end[1]) / 2, text, fontsize=8, color="#555555")


arrow("q", "embed")
arrow("embed", "rank")
arrow("rank", "verify")
arrow("verify", "out")
arrow("store", "embed", "--", "clauses embedded once")
arrow("check", "rank", "--", "same result to 3 dp")
ax.text(9.8, 1.35, "below threshold 0.40 -> NOT FOUND,\nanalyst asks the policy team (human review)",
        ha="center", fontsize=8, color="#8a3b12")

out = Path(__file__).resolve().parent / "architecture.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("saved", out)
