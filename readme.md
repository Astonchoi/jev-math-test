# JEV Math Test

## Paper parsing notes

Source: hkdse-2025-math-paper (45 questions, 4 options each) + `raw-data/answer.md` (45 answers, matches).

## skip questions

if its figure question, skip it. 14, 21, 23, 29

- **Q14** — need to see line L's position relative to the axes to judge p>7, q>7, q>p
- **Q21** — text never says where E is (figure shows E on AB)
- **Q23** — angle text OCR-garbled ("∠ABC + ∠ADC = ∠ACD = ∠BAC = 90°"), need the figure to reconstruct
- **Q29** — data is only in the bar chart image

### figure questions that are still answerable (text self-contained)

Q17, 18, 19, 22, 38 — image is illustration only, all given data is in the text. Kept in the test run, but excluded from scoring to be fair to a text-only model.

See [report.md](report.md) for the results.

## How to reproduce

1. **Get the data** — the question paper and answer key of the same year (I used the HKDSE 2025 math paper).
2. **OCR the data into markdown** — I used Paddle OCR on the paper images.
3. **Clean the data** — questions in the format of `raw-data/questions-example.md` (numbered questions, 4 options `A.`–`D.`), answers in the format of `raw-data/answer.md` (one letter per line, in question order).
4. **Point the parser at your files** — update `PAPER_PATH`, `ANSWER_PATH`, `OUTPUT_PATH` in `source/data_parse.py`.
5. **Update the hard-coded config for your paper** — the skip lists in `source/main.py` (`SKIP_FIGURE_QUESTIONS`, `SKIP_IMAGE_ILLUSTRATION_QUESTIONS`, figure questions a text-only model can't answer) and the topic bands in `source/eval.py` (`TOPIC_BANDS`). Both are hard-coded for the 2025 paper.
6. **Get a jev API key** — copy `.env.example` to `.env` and fill in `JEV_API_KEY`.
7. **Set up the environment**:

   ```sh
   # no uv? install it first
   brew install uv                                      # macOS (Homebrew)
   curl -LsSf https://astral.sh/uv/install.sh | sh      # Linux/macOS

   uv sync          # create .venv + install dependencies
                    # (reads requires-python >= 3.11, downloads Python if needed)
   ```

8. **Run**:

   ```sh
   cd source
   ../.venv/bin/python main.py
   ```

9. **Evaluate** — offline, no API calls, safe to rerun:

   ```sh
   cd source
   ../.venv/bin/python eval.py --threshold 0.5
   ```
