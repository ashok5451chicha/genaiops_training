# Step 4 – what each experiment shows

Full output: `outputs/step4_why_cosine.txt`.

## Experiment 1 – same direction, different length

[3, 4] vs [6, 8]: cosine **1.000**, distance **5.000**. B is just A doubled, so the direction (the "topic") is
identical, but the points are far apart. **Cosine compares direction and ignores size; distance counts size too.**
For text, size mostly reflects length or wordiness rather than meaning. A 2-page and a 20-page policy on the same
topic should match, which is why cosine is the default for text.

## Experiment 2 – ranking sentences for a query

* *"Is this applicant's ID document valid?"*: both metrics pick "Verify identity documents for account opening"
  (cosine 0.968, distance 1.414). When items are similar in size, the metrics agree.
* *"Question about our loans and customer service"*: **they disagree**.
  * Cosine picks the very long annual report (0.998), because it points the same way as the query.
  * Distance picks the short "home loan eligibility" sentence (2.236), because the report's vector is big and so far away.

Neither metric is always right. Cosine can favour a huge, generic document over a precise answer; distance can punish
a relevant document just for being long. That is why retrieval systems cut documents into chunks of similar size
(Day 4) and still show the cited source.

## Experiment 3 – unit-length vectors

After scaling loan and mortgage to length 1: cosine = dot = **0.9718**, and distance² = 2 − 2·cosine = **0.0563**.
On unit vectors the two metrics tell the same story: higher cosine ⇔ smaller distance. Many embedding models already
output unit vectors, so on those the choice of metric changes the scale, not the ranking.

## Experiment 4 – does a library agree?

My functions and numpy give identical results (cosine 0.971825, distance 1.414214). Libraries do the same
arithmetic, only faster and on millions of vectors at once. The value of writing it by hand is knowing what the
number means and checking it, not speed.

## One thing that surprised me

A single long document can beat the best short answer on cosine (experiment 2). A high score means "points the same
way", not "is the best answer". So a score alone should never decide anything that matters.
