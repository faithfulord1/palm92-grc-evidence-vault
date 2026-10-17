"""Offline educational evidence triage. No supplier approval or network calls."""
import json
from datetime import date
from pathlib import Path

REQUIRED = ("access_review", "recovery_test", "incident_plan")

def review(case, as_of):
    findings = []
    for control in REQUIRED:
        evidence = case.get("evidence", {}).get(control)
        reasons = []
        if not isinstance(evidence, dict):
            reasons.append("missing evidence")
        else:
            if not evidence.get("source"):
                reasons.append("missing source reference")
            if evidence.get("review_status") != "verified":
                reasons.append("not independently verified")
            try:
                issued = date.fromisoformat(evidence["issued"])
                expires = date.fromisoformat(evidence["expires"])
                if issued > as_of:
                    reasons.append("future-dated evidence")
                if expires < issued:
                    reasons.append("invalid evidence date range")
                if expires < as_of:
                    reasons.append("expired evidence")
            except (KeyError, ValueError, TypeError):
                reasons.append("missing or invalid evidence dates")
        if reasons:
            findings.append({"control": control, "reasons": reasons})
    return {"supplier": case["supplier"], "fictional": True,
            "as_of": as_of.isoformat(), "findings": findings,
            "triage": "gaps_require_review" if findings else "ready_for_human_review",
            "decision": "pending_human_review",
            "limitation": "Metadata checks only; no compliance certification or approval."}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    parser.add_argument("--as-of", type=date.fromisoformat, required=True)
    args = parser.parse_args()
    print(json.dumps(review(json.loads(args.case.read_text()), args.as_of), indent=2))
