"""Send one math question to the jev model via the TypeSafe SDK.

The SDK default model is already "jev-latest" (typesafe_sdk.constants.DEFAULT_MODEL),
so no model override is needed. The client reads TYPESAFE_API_KEY from the
environment, but this project keeps the key in .env as JEV_API_KEY, so it is
loaded here and passed explicitly.

Question + options go into the system_one state, and the answer is a Choice
question with criteria A/B/C/D mapped to the option texts. The response gives
.choice (label), .confidence, and .probabilities.

Input: parsed-data/questions.json (produced by parse_questions.py)
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from typesafe_sdk import Choice, TypeSafeClient

load_dotenv()  # read .env file into os.environ
ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "parsed-data" / "questions.json"


def ask_question(question: dict, api_key: str) -> tuple[str, float]:
    """Ask the jev model one multiple-choice math question.

    Returns (predicted label, confidence).
    """
    state = {
        "question_number": question["number"],
        "stem": question["stem"],
        "options": question["options"],
    }
    with TypeSafeClient(api_key=api_key) as client:
        response = client.system_one(
            state=state,
            questions={
                "answer": Choice(
                    instructions="Solve the math problem and select the correct option.",
                    criteria={label: question["options"][label] for label in "ABCD"},
                )
            },
        )
    answer = response.choices["answer"]
    return answer.choice, answer.confidence


def main() -> None:
    api_key = os.environ["JEV_API_KEY"]
    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))

    question = questions[0]  # smoke test: just one question
    predicted, confidence = ask_question(question, api_key)
    expected = question["answer"]

    mark = "PASS" if predicted == expected else "FAIL"
    print(f"Q{question['number']}: predicted={predicted} (confidence {confidence:.2f})")
    print(f"        expected={expected} -> {mark}")


if __name__ == "__main__":
    sys.exit(main())
