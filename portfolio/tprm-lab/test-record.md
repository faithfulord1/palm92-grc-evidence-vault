# Local verification, 17 October 2026

Python unittest: 4 tests passed, including subcases for future dates, invalid dates, invalid date ranges and missing provenance.

Verified: expired recovery evidence and unverified incident evidence are flagged; missing evidence does not pass; valid metadata still leaves the decision pending human review.

Command: `python -m unittest discover -s . -p 'test_review.py' -v`

Example run: `python review.py case.json --as-of 2026-10-17`

No cloud resources, real supplier records, video rendering or external services were exercised. Tests cover this standalone lab, not the rest of the repository.
