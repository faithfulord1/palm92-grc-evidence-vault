import copy
import json
import unittest
from datetime import date
from pathlib import Path
from review import review, REQUIRED

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(Path(__file__).with_name("case.json").read_text())
        self.today = date(2026, 10, 17)

    def test_expired_and_self_declared_evidence_flagged(self):
        result = review(self.case, self.today)
        self.assertEqual([x["control"] for x in result["findings"]], ["recovery_test", "incident_plan"])
        self.assertIn("expired evidence", result["findings"][0]["reasons"])
        self.assertEqual(result["decision"], "pending_human_review")

    def test_missing_evidence_never_passes(self):
        self.case["evidence"] = {}
        self.assertEqual(len(review(self.case, self.today)["findings"]), 3)

    def test_valid_metadata_still_requires_human_decision(self):
        item = self.case["evidence"]["access_review"]
        self.case["evidence"] = {key: copy.deepcopy(item) for key in REQUIRED}
        result = review(self.case, self.today)
        self.assertEqual(result["triage"], "ready_for_human_review")
        self.assertEqual(result["decision"], "pending_human_review")

    def test_future_or_invalid_dates_and_missing_source_flagged(self):
        for change in ({"issued": "2027-01-01"}, {"expires": "bad"}, {"expires": "2020-01-01"}, {"source": ""}):
            with self.subTest(change=change):
                case = copy.deepcopy(self.case)
                case["evidence"]["access_review"].update(change)
                self.assertIn("access_review", [x["control"] for x in review(case, self.today)["findings"]])

if __name__ == "__main__":
    unittest.main()
