"""Send one math question to the jev model via the TypeSafe SDK.

Question + options go into the system_one state, and the answer is a Choice
question with criteria A/B/C/D mapped to the option texts. The response gives
.choice (label), .confidence, and .probabilities.

Input: parsed-data/questions.json (produced by parse_questions.py)
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from typesafe_sdk import AsyncTypeSafeClient, Choice, TypeSafeClient

load_dotenv()  # read .env file into os.environ
ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "parsed-data" / "questions.json"
DEFAULT_CONCURRENCY = 8


def _build_request(question: dict) -> tuple[dict, dict]:
    """Build the (state, questions) pair shared by the sync and async askers."""
    state = {
        "question_number": question["number"],
        "stem": question["stem"],
        "options": question["options"],
    }
    questions = {
        "answer": Choice(
            instructions="Solve the math problem and select the correct option.",
            criteria={label: question["options"][label] for label in "ABCD"},
        )
    }
    return state, questions


def ask_question(question: dict, api_key: str) -> tuple[str, float]:
    """Ask the jev model one multiple-choice math question.

    Returns (predicted label, confidence).
    """
    state, questions = _build_request(question)
    with TypeSafeClient(api_key=api_key) as client:
        response = client.system_one(state=state, questions=questions)
    answer = response.choices["answer"]
    return answer.choice, answer.confidence


async def ask_questions_parallel(
    questions: list[dict], api_key: str, max_concurrency: int = DEFAULT_CONCURRENCY
) -> list[tuple[str, float]]:
    """Ask the jev model many questions concurrently over one shared client.

    A semaphore caps how many requests are in flight at once. Results come
    back in the same order as the input, each as (predicted label, confidence).
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def ask_one(client: AsyncTypeSafeClient, question: dict) -> tuple[str, float]:
        state, request = _build_request(question)
        async with semaphore:
            response = await client.system_one(state=state, questions=request)
        answer = response.choices["answer"]
        return answer.choice, answer.confidence

    async with AsyncTypeSafeClient(api_key=api_key) as client:
        return list(await asyncio.gather(*(ask_one(client, q) for q in questions)))


def main() -> None:
    """Smoke test: ask the first question synchronously, ignore the rest.

    The full parallel run lives in main.py.
    """
    api_key = os.environ["JEV_API_KEY"]
    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))

    question = questions[0]
    predicted, confidence = ask_question(question, api_key)
    expected = question["answer"]

    mark = "PASS" if predicted == expected else "FAIL"
    print(f"Q{question['number']}: predicted={predicted} (confidence {confidence:.2f})")
    print(f"        expected={expected} -> {mark}")


if __name__ == "__main__":
    sys.exit(main())
