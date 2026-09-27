r"""Parse the HKDSE 2025 math paper and answer key into questions.json.

- paper:   questions start at lines matching ^\d+\.\s
- answers: one letter per line, positional (line i = question i)
"""

import json
import re
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_PATH = ROOT / "raw-data" / "hkdse-2025-math-paper.md"
ANSWER_PATH = ROOT / "raw-data" / "answer.md"
OUTPUT_PATH = ROOT / "parsed-data" / "questions.json"

QUESTION_RE = re.compile(r"^(\d+)\.\s", re.MULTILINE)
OPTION_RE = re.compile(r"^([A-D])\.\s*(.*)$")


def question_chunks(text: str) -> list[str]:
    """Slice the paper text into one chunk per numbered question."""
    starts = [m.start() for m in QUESTION_RE.finditer(text)]
    bounds = starts + [len(text)]
    return [text[begin:end] for begin, end in pairwise(bounds)]


def split_stem_and_options(chunk: str) -> tuple[str, dict[str, str]]:
    """Split a question chunk into its stem and its a–d options.

    Once the first option line appears, every later line is treated as
    option content, so a stray non-option line can't leak into the stem.
    """
    stem_lines: list[str] = []
    options: dict[str, str] = {}
    seen_options = False

    for line in chunk.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        option_match = OPTION_RE.match(stripped)
        if option_match:
            seen_options = True
            options[option_match.group(1)] = option_match.group(2).strip()
        elif not seen_options:
            stem_lines.append(stripped)

    return "\n".join(stem_lines), options


def parse_questions(text: str) -> list[dict]:
    questions = []
    for chunk in question_chunks(text):
        number = int(QUESTION_RE.match(chunk).group(1))
        stem, options = split_stem_and_options(chunk)
        questions.append({"number": number, "stem": stem, "options": options})
    return questions


def parse_answers(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_paper() -> list[dict]:
    questions = parse_questions(PAPER_PATH.read_text(encoding="utf-8"))
    answers = parse_answers(ANSWER_PATH.read_text(encoding="utf-8"))

    for question, answer in zip(questions, answers):
        question["answer"] = answer

    return questions


if __name__ == "__main__":
    questions = parse_paper()
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"parsed {len(questions)} questions -> {OUTPUT_PATH.relative_to(ROOT)}")
