r"""Orchestrate the full jev math experiment in one run.

Pipeline: parse the paper and answer key (data_parse.parse_paper)
-> ask the remaining questions in parallel (ask_jev.ask_questions_parallel)
-> print per-question results and the final score, save results.json.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from ask_jev import ask_questions_parallel
from data_parse import parse_paper
from dotenv import load_dotenv

load_dotenv()  # read .env file into os.environ
ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "output" / "results.json"

# Figure-only questions: the text alone cannot answer them (see readme.md).
SKIP_FIGURE_QUESTIONS = {14, 21, 23, 29}
SKIP_IMAGE_ILLUSTRATION_QUESTIONS = {17, 18, 19, 22, 38}
SKIP_ALL = SKIP_FIGURE_QUESTIONS | SKIP_IMAGE_ILLUSTRATION_QUESTIONS


def main() -> None:
    api_key = os.environ["JEV_API_KEY"]

    questions = parse_paper()
    testable = [q for q in questions if q["number"] not in SKIP_ALL]
    print(
        f"parsed {len(questions)} questions, "
        f"testing {len(testable)} (skipping figure questions {sorted(SKIP_FIGURE_QUESTIONS)})"
    )

    results = asyncio.run(ask_questions_parallel(testable, api_key))

    correct = 0
    rows = []
    for question, (predicted, confidence) in zip(testable, results):
        expected = question["answer"]
        passed = predicted == expected
        correct += passed
        mark = "PASS" if passed else "FAIL"
        print(
            f"Q{question['number']}: predicted={predicted} (confidence {confidence:.2f})"
        )
        print(f"        expected={expected} -> {mark}")
        rows.append(
            {
                "number": question["number"],
                "predicted": predicted,
                "expected": expected,
                "confidence": confidence,
                "correct": passed,
            }
        )

    score = correct / len(testable)
    print(f"Score: {correct}/{len(testable)} ({score:.0%})")

    RESULTS_PATH.parent.mkdir(exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"results -> {RESULTS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
