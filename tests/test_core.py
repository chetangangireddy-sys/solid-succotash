"""Example tests for StudySprint. Two small tests to copy from in Lesson 12."""

import unittest

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


if __name__ == "__main__":
    unittest.main()
