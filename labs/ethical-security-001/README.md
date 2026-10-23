# Palm92 Ethical Security Lab 001

Completed 23 October 2026. AI-assisted engineering exercise, executed in an offline Python/SQLite in-memory target with three fictional records. No external targets, personal data, listeners or network testing.

## Finding and fix

CWE-89: concatenating an owner lookup into SQL allowed a crafted value to return all three synthetic records. Parameter binding treated the input as data and returned zero records for the identical input. Seven checks passed, covering the baseline, disclosure demonstration, remediation, normal lookup, a legitimate apostrophe, unknown and empty values.

Run with Python standard library only:

```sh
python lab.py > new-evidence.json
```

See evidence.json for the recorded execution and source SHA-256. A hash supports comparison, not independent attestation.

## Boundaries

This original teaching example is not a reproduction of the PHP vulnerabilities, a scan of Palm92 services, an AI vulnerability-discovery benchmark or a production security certification. Real applications also need independent authorization checks. Deliberately vulnerable code must remain isolated.

## Operational lesson

Permission and scope → reproduce → fix → retest → evidence → human review.

Palm92 production PHP exposure remains unverified. Further work: inventory code and deployed runtimes, obtain hosting-provider patch evidence, and map any findings to owners and closure checks.

AI investigates. Humans decide.
