import unittest
from features import reports

class TestReports(unittest.TestCase):
    def test_average_score_empty(self):
        # Edge case: empty history should return 0.0
        result = reports.average_score({"history": []})
        self.assertEqual(result, 0.0)

    def test_average_score_normal(self):
        # Normal case: calculates correct average
        result = reports.average_score({"history": [5, 6, 4]})
        self.assertEqual(result, 5.0)

if __name__ == "__main__":
    unittest.main()