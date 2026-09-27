# JEV Math Experiment

## math paper question

## Paper parsing notes

Source: `raw-data/hkdse-2025-math-paper.md` (45 questions, 4 options each) + `raw-data/answer.md` (45 answers, matches).

Parsing strategy: chunk on `^\d+\.` boundaries. Everything inside a chunk before `^[A-D]\.` is the stem. Traps:

## skip questions

if its figure question, skip it. 14, 21, 23, 29

- **Q14** — need to see line L's position relative to the axes to judge p>7, q>7, q>p
- **Q21** — text never says where E is (figure shows E on AB)
- **Q23** — angle text OCR-garbled ("∠ABC + ∠ADC = ∠ACD = ∠BAC = 90°"), need the figure to reconstruct
- **Q29** — data is only in the bar chart image

### figure questions that are still answerable (text self-contained)

Q17, 18, 19, 22, 38 — image is illustration only, all given data is in the text. Keep them in the test.

Result: test 41 of 45 questions in a text-only run.
