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

Both commands work from the root of this repo with no setup and no installs.

## Features

- Run a standard or timed lightning-round quiz with a progress bar.
- Add cards, study by category, and import cards from CSV files with
  `question`, `answer`, and `category` columns.
- Review missed answers, track the best correct-answer streak, and generate
  shuffled multiple-choice options.
- View category counts, deck details, and recent scores.
- Save cards and score history to `data/studysprint.json` between sessions.

## What is in here

| Path | What it does |
|---|---|
| `main.py` | The menu loop you interact with |
| `storage.py` | Loads and saves the JSON data file |
| `features/core.py` | The deck, the quiz loop, and small helpers |
| `features/reports.py` | Deck, category, and score reports |
| `data/studysprint.json` | The card deck and score history |
| `tests/` | Unit and command-line workflow tests |
| `tickets/` | Feature specifications and acceptance criteria |
| `docs/README.md` | Product guide and team list |
| `CONTRIBUTING.md` | The Definition of Done and the branch naming rules |

## Before you open a pull request

Read **[CONTRIBUTING.md](CONTRIBUTING.md)**. A pull request is done only when
all five are true: the ticket is linked, it runs, a squadmate reviewed it, a
test covers it, and the docs reflect the change. Never commit straight to
`main` - it is what a new teammate clones and what the demo runs from.

## CSV format

CSV imports need a header row containing `question`, `answer`, and `category`.
Questions and answers must not be blank. Imported cards receive IDs that
continue after the current deck's highest ID.
