"""Tests for the StudySprint command-line workflows."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class TestMain(unittest.TestCase):
    def test_quiz_saves_score_history(self):
        data = {
            "deck_name": "Test deck",
            "cards": [{"id": 1, "question": "Question?", "answer": "yes", "category": "general"}],
            "history": [],
        }
        with patch("main.storage.load_data", return_value=data), \
                patch("main.storage.save_data") as save_data, \
                patch("builtins.input", side_effect=["1", "yes", "0"]), \
                patch("builtins.print"):
            main.main()
        self.assertEqual(data["history"], [1])
        save_data.assert_called_once_with(data)

    def test_lightning_round_reports_elapsed_time(self):
        data = {"deck_name": "Empty", "cards": [], "history": []}
        with patch("main.storage.load_data", return_value=data), \
                patch("main.storage.save_data"), \
                patch("main.time.perf_counter", side_effect=[10.0, 12.345]), \
                patch("builtins.input", side_effect=["9", "0"]), \
                patch("builtins.print") as output:
            main.main()
        printed = [call.args[0] for call in output.call_args_list if call.args]
        self.assertIn("Time: 2.35 seconds.", printed)

    def test_csv_import_saves_cards_and_bad_path_is_reported(self):
        data = {"deck_name": "Test", "cards": [], "history": []}
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "cards.csv"
            csv_path.write_text("question,answer,category\nImported?,yes,science\n", encoding="utf-8")
            missing_path = str(Path(directory) / "missing.csv")
            with patch("main.storage.load_data", return_value=data), \
                    patch("main.storage.save_data") as save_data, \
                    patch("builtins.input", side_effect=["10", str(csv_path), "10", missing_path, "0"]), \
                    patch("builtins.print") as output:
                main.main()
        self.assertEqual(data["cards"][0]["question"], "Imported?")
        self.assertEqual(data["cards"][0]["id"], 1)
        self.assertEqual(save_data.call_count, 1)
        printed = [call.args[0] for call in output.call_args_list if call.args]
        self.assertTrue(any("Could not import cards:" in line for line in printed))

    def test_empty_deck_last_card_option_does_not_crash(self):
        data = {"deck_name": "Empty", "cards": [], "history": []}
        with patch("main.storage.load_data", return_value=data), \
                patch("builtins.input", side_effect=["5", "0"]), \
                patch("builtins.print") as output:
            main.main()
        printed = [call.args[0] for call in output.call_args_list if call.args]
        self.assertIn("The deck has no cards yet.", printed)


if __name__ == "__main__":
    unittest.main()