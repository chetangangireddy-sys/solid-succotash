"""Reporting helpers for StudySprint."""


def deck_summary(data):
    return data["deck_name"] + ": " + str(len(data["cards"])) + " cards"


def score_summary(data):
    history = data.get("history", [])
    if not history:
        return "Score history: no scores yet"
    recent = history[-5:]
    return "Score history: " + ", ".join(str(score) for score in recent)


def category_report(data):
    report = {}
    for card in data.get("cards", []):
        category = card.get("category", "general")
        report[category] = report.get(category, 0) + 1
    return report
