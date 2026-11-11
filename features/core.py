"""Core StudySprint logic: the deck, the quiz loop, and small helpers."""

import csv
import random


def get_cards(data):
    return data["cards"]


def check_answer(card, guess):
    return guess.strip().lower() == card["answer"].strip().lower()


def run_quiz(cards, ask=None, show=None):
    ask = ask or input
    show = show or print
    score = 0
    total = len(cards)
    for index, card in enumerate(cards, start=1):
        show(progress_bar(index, total))
        guess = ask(card["question"] + " ")
        if check_answer(card, guess):
            show("Correct!")
            score += 1
        else:
            show("Not quite. The answer was: " + card["answer"])
    return score


def review_missed(cards, results):
    return [card for card, correct in zip(cards, results) if not correct]


def best_streak(results):
    best = current = 0
    for correct in results:
        if correct:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def progress_bar(current, total, width=10):
    total = max(0, total)
    current = min(max(0, current), total)
    filled = width * current // total if total else 0
    return "[" + "#" * filled + "-" * (width - filled) + "] " + str(current) + "/" + str(total)


def import_cards_from_csv(path, existing_cards):
    required = {"question", "answer", "category"}
    next_id = max((card["id"] for card in existing_cards), default=0) + 1
    imported = []
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames is not None:
                reader.fieldnames = [header.strip() for header in reader.fieldnames]
            headers = set(reader.fieldnames or [])
            if not required.issubset(headers):
                raise ValueError("CSV must include question, answer, and category columns.")
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    raise ValueError("CSV row " + str(line_number) + " has more values than columns.")
                if not any((value or "").strip() for value in row.values()):
                    continue
                question = (row.get("question") or "").strip()
                answer = (row.get("answer") or "").strip()
                category = (row.get("category") or "").strip() or "general"
                if not question or not answer:
                    raise ValueError("CSV row " + str(line_number) + " needs a question and answer.")
                imported.append({
                    "id": next_id,
                    "question": question,
                    "answer": answer,
                    "category": category,
                })
                next_id += 1
    except csv.Error as error:
        raise ValueError("Could not read CSV: " + str(error)) from error
    return imported


def generate_multiple_choice(card, cards):
    correct_answer = card["answer"]
    wrong_answers = []
    seen = {correct_answer}
    for candidate in cards:
        answer = candidate["answer"]
        if answer not in seen:
            seen.add(answer)
            wrong_answers.append(answer)
    options = [correct_answer] + random.sample(wrong_answers, min(3, len(wrong_answers)))
    random.shuffle(options)
    return options


def add_card(data, question, answer, category="general"):
    new_id = max((c["id"] for c in data["cards"]), default=0) + 1
    card = {"id": new_id, "question": question, "answer": answer, "category": category}
    data["cards"].append(card)
    return card


def list_cards(cards, show=print):
    for card in cards:
        show(str(card["id"]) + ". " + card["question"])


def cards_by_category(cards, category):
    return [c for c in cards if c["category"] == category]


def count_by_category(cards):
    counts = {}
    for card in cards:
        name = card["category"]
        counts[name] = counts.get(name, 0) + 1
    return counts


def top_card(cards):
    return cards[len(cards) - 1]


def percent_correct(score, total):
    if total == 0:
        return 0
    return round(100 * score / total)


def record_score(data, score):
    if "history" not in data:
        data["history"] = []
    data["history"].append(score)
    return data["history"]
