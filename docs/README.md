# StudySprint

StudySprint is a terminal flashcard trainer. It loads a JSON deck, runs quizzes,
tracks scores, and saves deck changes and quiz history between sessions.

## Run it

```bash
python main.py
```

## Run the tests

```bash
python -m unittest
```

## Features

- Standard quizzes and timed lightning rounds with a fixed-width progress bar.
- Add cards, study by category, or import a CSV deck with `question`, `answer`,
	and `category` columns.
- Review missed answers, track the best answer streak, and generate shuffled
	multiple-choice options from the deck.
- Category, deck, and recent-score summaries.
- Cards and score history persist in `data/studysprint.json`.

## How it's laid out

| File | What it does |
|---|---|
| `main.py` | The menu loop you interact with |
| `storage.py` | Loads and saves the JSON data file |
| `features/core.py` | The deck, the quiz loop, and small helpers |
| `features/reports.py` | Deck, category, and score reports |
| `data/studysprint.json` | The card deck and score history |
| `tests/` | Unit and command-line workflow tests |

## Team

- Chetan Angireddy (developer)

## CSV format

CSV imports require a header row with `question`, `answer`, and `category`
columns. Questions and answers must not be blank. Imported cards continue the
deck's existing ID sequence.
