# Palm92 supplier evidence review lab

Fictional portfolio exercise, created 17 October 2026. AI investigates, humans decide.

## Run without a cloud account or extra packages

From this folder:

```sh
python review.py case.json --as-of 2026-10-17
python -m unittest discover -s . -p 'test_review.py' -v
```

Expected: recovery evidence expired; incident plan unverified; decision pending human review.
`sample-result.json` records this run. Dates and validity windows are fictional exercise policy, not universal requirements.

## Evidence and judgment

| Reference | Evidence | Finding | Next request |
| --- | --- | --- | --- |
| E-01 | Fictional verified access review metadata | No metadata gap | Inspect scope, population, exceptions and reviewer independence in a real assessment |
| E-02 | Fictional recovery test summary | Expired under exercise policy | Obtain current test, results, failed objectives and remediation |
| E-03 | Fictional supplier declaration | Not independently verified | Obtain plan, exercise record and agreed notification arrangements |

Recommended disposition: pause onboarding pending evidence review by the designated risk owner. This recommendation is a worked exercise; no supplier has been assessed or approved.

The checker checks supplied metadata. It does not read certificates, validate authenticity, assess control effectiveness, calculate residual risk or enforce real approvals. A supplier-controlled `verified` flag is not sufficient in a live system. A production system needs authenticated reviewers, provenance, protected evidence, access controls and an auditable decision workflow.

## Framework and audit practice

NIST CSF 2.0 supply chain outcomes provide context: GV.SC-06 for pre-contract due diligence, GV.SC-07 for assessment and monitoring, GV.SC-08 for incident coordination. These are illustrative mappings, not an assurance opinion.
Source: https://www.nist.gov/publications/nist-cybersecurity-framework-20-quick-start-guide-cybersecurity-supply-chain-risk

Audit practice: define criteria, inspect evidence, distinguish assertion from verified evidence, document a finding and obtain an accountable decision. This supports CISA learning; it is not professional experience verification or certification.

## What to show a recruiter

Problem: supplier claims look complete but supporting evidence is weak.
Work: reproducible triage, traceable sources, clear limitations, tests and a human decision boundary.
Proof: this folder, sample output, test record and a short narrated demonstration.

No third-party code, podcast transcript, confidential supplier documents or paid exam questions are included.
