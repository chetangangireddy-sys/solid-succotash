"""Example tests for StudySprint. Two small tests to copy from in Lesson 12."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from features import core, reports


class TestCore(unittest.TestCase):
    def test_check_answer_is_case_insensitive(self):
        card = {"id": 1, "question": "Capital of France?", "answer": "Paris", "category": "geo"}
        self.assertTrue(core.check_answer(card, "paris"))
        self.assertFalse(core.check_answer(card, "London"))

    def test_add_card_gives_a_new_id(self):
        data = {"cards": [{"id": 1, "question": "q", "answer": "a", "category": "general"}]}
        card = core.add_card(data, "New question?", "yes")
        self.assertEqual(card["id"], 2)
        self.assertEqual(len(data["cards"]), 2)

    def test_record_score_appends_to_history(self):
        data = {"history": [4, 5]}
        result = core.record_score(data, 6)
        self.assertEqual(result, [4, 5, 6])
        self.assertEqual(data["history"], [4, 5, 6])

    def test_score_summary_shows_recent_scores(self):
        data = {"history": [5, 8, 3, 7, 10, 6]}
        summary = reports.score_summary(data)
        self.assertIn("10", summary)
        self.assertIn("6", summary)
        self.assertIn("Score history", summary)

    def test_review_missed_returns_cards_with_false_results(self):
        cards = [{"question": "one"}, {"question": "two"}, {"question": "three"}]
        self.assertEqual(core.review_missed(cards, [True, False, False]), cards[1:])
        self.assertEqual(core.review_missed(cards, [True, True, True]), [])

    def test_best_streak_handles_mixed_and_empty_results(self):
        self.assertEqual(core.best_streak([True, True, False, True, True, True]), 3)
        self.assertEqual(core.best_streak([]), 0)
        self.assertEqual(core.best_streak([False, False]), 0)
        self.assertEqual(core.best_streak([True, True]), 2)

    def test_progress_bar_has_a_fixed_width(self):
        self.assertEqual(core.progress_bar(3, 8), "[###-------] 3/8")
        self.assertEqual(core.progress_bar(8, 8), "[##########] 8/8")
        self.assertEqual(core.progress_bar(0, 0), "[----------] 0/0")

    def test_run_quiz_shows_progress_before_each_question(self):
        cards = [
            {"question": "First?", "answer": "yes"},
            {"question": "Second?", "answer": "no"},
        ]
        output = []
        score = core.run_quiz(cards, ask=lambda prompt: "yes", show=output.append)
        self.assertEqual(score, 1)
        self.assertEqual(output[0], "[#####-----] 1/2")
        self.assertEqual(output[2], "[##########] 2/2")

    def test_import_cards_from_csv_assigns_unique_ids(self):
        existing = [{"id": 4, "question": "old", "answer": "old", "category": "general"}]
        csv_text = "question,answer,category\nNew question?,yes,science\nAnother?,no,history\n"
        with TemporaryDirectory() as directory:
            path = Path(directory) / "cards.csv"
            path.write_text(csv_text, encoding="utf-8")
            cards = core.import_cards_from_csv(path, existing)
        self.assertEqual([card["id"] for card in cards], [5, 6])
        self.assertEqual(cards[0]["category"], "science")

    def test_import_cards_from_csv_rejects_missing_columns(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "cards.csv"
            path.write_text("question,answer\nQ,A\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                core.import_cards_from_csv(path, [])

    def test_import_cards_from_csv_normalizes_headers_and_rejects_extra_values(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "cards.csv"
            path.write_text(" question , answer , category \nQ,A,science\n", encoding="utf-8")
            self.assertEqual(core.import_cards_from_csv(path, [])[0]["question"], "Q")
            path.write_text("question,answer,category\nQ,A,science,extra\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "more values than columns"):
                core.import_cards_from_csv(path, [])

    def test_multiple_choice_options_include_correct_answer_and_are_unique(self):
        cards = [{"answer": answer} for answer in ("a", "b", "c", "d", "e")]
        options = core.generate_multiple_choice(cards[0], cards)
        self.assertEqual(len(options), 4)
        self.assertEqual(len(set(options)), 4)
        self.assertIn("a", options)

    def test_multiple_choice_uses_available_answers_on_short_deck(self):
        cards = [{"answer": "a"}, {"answer": "b"}]
        options = core.generate_multiple_choice(cards[0], cards)
        self.assertEqual(set(options), {"a", "b"})

    def test_category_report_counts_cards_and_handles_empty_deck(self):
        data = {"cards": [
            {"category": "syntax"},
            {"category": "syntax"},
            {"category": "types"},
        ]}
        self.assertEqual(reports.category_report(data), {"syntax": 2, "types": 1})
        self.assertEqual(reports.category_report({"cards": []}), {})


if __name__ == "__main__":
    unittest.main()
