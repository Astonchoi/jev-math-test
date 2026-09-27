# Results Report

Full run output: `output/results.json` (36 answers).

## Scoring scope

Exclude all 9 figure-related questions — Q14, 21, 23, 29 (never tested) and Q17, 18, 19, 22, 38 (tested but not fairly answerable without the image). Scored on the remaining **36 questions**.

## Overall (no confidence filter)

17/36 correct = **47.2%**

## With confidence threshold > 0.5

Jev only answers when its confidence exceeds 0.5:

- Answered: 11 of 36
- Correct: **8/36 = 22.2%**
- Precision among answered: 8/11 = 72.7%
- Correct: Q1, Q2, Q5, Q6, Q9, Q25, Q28, Q41
- Wrong: Q7 (0.59), Q36 (0.70), Q37 (0.57)

Takeaways:

- The confidence filter cuts the error rate among answered questions roughly in half (72.7% vs 47.2%), but coverage is poor — 25 of 36 questions go unanswered, so the raw score is only 22.2%.
- 9 of the 17 correct answers came in below the 0.5 threshold, so most correct answers would be discarded by the filter.
- Q36 was confidently wrong (0.70) — the model's confidence is not calibrated on questions it misunderstands.

## Per-topic breakdown

Scored on the 36 kept questions, grouped by the paper's topic bands:

| Topic | Tested | Correct | Accuracy | Conf > 0.5 | Correct among those |
| --- | --- | --- | --- | --- | --- |
| 1–5 Algebra, factorisation, equations | 5 | 3 | 60% | 3 | 3 |
| 6–9 Bounds, inequalities, functions | 4 | 3 | 75% | 3 | 2 |
| 10–13 Compound interest, variation, sequences | 4 | 1 | 25% | 0 | 0 |
| 14–20 Geometry, mensuration, similarity | 3 | 1 | 33% | 0 | 0 |
| 21–24 Geometry, circles, trig | 1 | 0 | 0% | 0 | 0 |
| 25–27 Coordinate geometry | 3 | 2 | 67% | 1 | 1 |
| 28–30 Probability & statistics | 2 | 1 | 50% | 1 | 1 |
| 31–34 Algebra, logarithms, indices | 4 | 0 | 0% | 0 | 0 |
| 35–37 Functions/inequalities/sequences | 3 | 1 | 33% | 2 | 0 |
| 38–41 Circle geometry, trig, 3-D | 3 | 2 | 67% | 1 | 1 |
| 42–45 Combinations, probability, statistics | 4 | 3 | 75% | 0 | 0 |

Observations:

- Strongest topics: bounds & functions (3/4), combinations & statistics (3/4), coordinate geometry (2/3), circle geometry/trig/3-D (2/3).
- Weakest topics: logarithms & indices (0/4), compound interest/variation/sequences (1/4) — Jev was never confident on any of these (0 answers above threshold).
- All of Jev's high-confidence mistakes concentrate in two bands: bounds/functions (Q7) and functions/inequalities/sequences (Q36, Q37).

## Run-to-run note

Compared to the previous run, the overall score dropped 18/36 → 17/36 (the 38–41 circle geometry band went 3/3 → 2/3) and the wrong-answer confidences shifted (Q7 0.54 → 0.59, Q36 0.66 → 0.70, Q37 0.67 → 0.57). The confidence-filtered picture was stable: same 11 answered, same 8 correct, same 3 wrong.
