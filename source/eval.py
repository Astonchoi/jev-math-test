r"""Evaluate the jev math run from output/results.json.

Scores every answer in results.json the same way readme.md does:
- overall accuracy
- accuracy when jev only answers above a confidence threshold (default 0.5)
- per-topic breakdown using the paper's topic bands.

Which questions get tested is decided in main.py (it skips the
figure/image questions before the run); eval just scores the results.

No API calls, no .env needed — pure offline scoring, so it is safe to rerun.

Usage (from source/): python eval.py [--threshold 0.5]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "output" / "results.json"

# The paper's topic bands (readme.md "math paper question").
TOPIC_BANDS: list[tuple[range, str]] = [
    (range(1, 6), "Algebra, factorisation, equations"),
    (range(6, 10), "Bounds, inequalities, functions/polynomials"),
    (range(10, 14), "Compound interest, variation, sequences"),
    (range(14, 21), "Geometry, mensuration, similarity"),
    (range(21, 25), "Geometry, circles, trigonometry, polar coordinates"),
    (range(25, 28), "Coordinate geometry"),
    (range(28, 31), "Probability & statistics"),
    (range(31, 35), "Algebra, logarithms, indices"),
    (range(35, 38), "Functions/inequalities/sequences"),
    (range(38, 42), "Circle geometry, trigonometry, 3-D geometry"),
    (range(42, 46), "Combinations, probability, statistics"),
]


def topic_for(number: int) -> str:
    for band, topic in TOPIC_BANDS:
        if number in band:
            return topic
    raise ValueError(f"question {number} is outside the paper's topic bands")


def load_results() -> list[dict]:
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def overall(results: list[dict]) -> tuple[int, int]:
    correct = sum(r["correct"] for r in results)
    return correct, len(results)


def thresholded(results: list[dict], threshold: float) -> tuple[list[dict], list[dict]]:
    answered = [r for r in results if r["confidence"] > threshold]
    correct = [r for r in answered if r["correct"]]
    return answered, correct


def per_topic(results: list[dict], threshold: float) -> list[dict]:
    rows: dict[str, dict] = {}
    for r in results:
        topic = topic_for(r["number"])
        row = rows.setdefault(
            topic,
            {
                "topic": topic,
                "tested": 0,
                "correct": 0,
                "answered": 0,
                "answered_correct": 0,
            },
        )
        row["tested"] += 1
        row["correct"] += r["correct"]
        if r["confidence"] > threshold:
            row["answered"] += 1
            row["answered_correct"] += r["correct"]
    return sorted(rows.values(), key=lambda row: row["topic"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="confidence threshold (default: 0.5)",
    )
    args = parser.parse_args()

    scored = load_results()
    print(f"results: {len(scored)} answers")
    print()

    correct, total = overall(scored)
    print(f"Overall: {correct}/{total} ({correct / total:.1%})")
    print()

    answered, answered_correct = thresholded(scored, args.threshold)
    print(f"Confidence > {args.threshold}:")
    print(f"  answered {len(answered)}/{total}")
    print(
        f"  correct   {len(answered_correct)}/{total} "
        f"({len(answered_correct) / total:.1%} of the paper)"
    )
    print(
        f"  precision {len(answered_correct)}/{len(answered)} "
        f"({len(answered_correct) / len(answered):.1%} of answered)"
    )
    wrong = [r for r in answered if not r["correct"]]
    if wrong:
        print(
            "  wrong: "
            + ", ".join(f"Q{r['number']} ({r['confidence']:.2f})" for r in wrong)
        )
    print()

    print(f"Per-topic (confidence > {args.threshold}):")
    print(
        f"  {'Topic':<45} {'Tested':>6} {'Correct':>7} {'Acc':>6} {'Ans':>4} {'OK':>3}"
    )
    for row in per_topic(scored, args.threshold):
        acc = f"{row['correct'] / row['tested']:.0%}"
        print(
            f"  {row['topic']:<45} {row['tested']:>6} {row['correct']:>7} "
            f"{acc:>6} {row['answered']:>4} {row['answered_correct']:>3}"
        )


if __name__ == "__main__":
    sys.exit(main())
