import hashlib
import json
from datetime import date, datetime, timezone

import pytest

from tprm_evidence import build_manifest, sha256_file


def test_manifest_is_metadata_only_and_review_starts_pending(tmp_path):
    evidence = tmp_path / "synthetic-evidence.txt"
    evidence.write_bytes(b"synthetic supplier evidence, not real data")

    manifest = build_manifest(
        supplier_ref="SUP-001",
        evidence_type="security-questionnaire",
        source_channel="secure-portal",
        received_at=datetime(2026, 10, 18, 5, 0, tzinfo=timezone.utc),
        content_sha256=sha256_file(evidence),
        control_refs=["CTRL-002", "CTRL-001", "CTRL-001"],
        valid_until=date(2027, 10, 18),
    )

    serialized = json.dumps(manifest)
    assert "synthetic supplier evidence" not in serialized
    assert manifest["review"] == {
        "status": "pending",
        "reviewer_ref": None,
        "reviewed_at": None,
    }
    assert manifest["control_refs"] == ["CTRL-001", "CTRL-002"]
    assert manifest["received_at"] == "2026-10-18T05:00:00Z"
    assert len(manifest["manifest_sha256"]) == 64

    unsigned = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    expected = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    assert manifest["manifest_sha256"] == expected


def test_file_digest_changes_when_evidence_bytes_change(tmp_path):
    evidence = tmp_path / "synthetic-evidence.txt"
    evidence.write_bytes(b"version one")
    first = sha256_file(evidence)
    evidence.write_bytes(b"version two")
    second = sha256_file(evidence)

    assert first == hashlib.sha256(b"version one").hexdigest()
    assert second == hashlib.sha256(b"version two").hexdigest()
    assert first != second


@pytest.mark.parametrize("supplier_ref", ["", "Faith Wright", "vendor@example.com", "../supplier"])
def test_rejects_non_opaque_supplier_references(supplier_ref):
    with pytest.raises(ValueError, match="opaque reference"):
        build_manifest(
            supplier_ref=supplier_ref,
            evidence_type="policy",
            source_channel="portal",
            received_at=datetime(2026, 10, 18, tzinfo=timezone.utc),
            content_sha256="a" * 64,
            control_refs=["CTRL-001"],
        )


def test_rejects_naive_timestamp_and_bad_digest():
    with pytest.raises(ValueError, match="timezone"):
        build_manifest(
            supplier_ref="SUP-001",
            evidence_type="policy",
            source_channel="portal",
            received_at=datetime(2026, 10, 18),
            content_sha256="a" * 64,
            control_refs=["CTRL-001"],
        )

    with pytest.raises(ValueError, match="SHA-256"):
        build_manifest(
            supplier_ref="SUP-001",
            evidence_type="policy",
            source_channel="portal",
            received_at=datetime(2026, 10, 18, tzinfo=timezone.utc),
            content_sha256="not-a-digest",
            control_refs=["CTRL-001"],
        )


def test_requires_control_mapping():
    with pytest.raises(ValueError, match="at least one control_ref"):
        build_manifest(
            supplier_ref="SUP-001",
            evidence_type="policy",
            source_channel="portal",
            received_at=datetime(2026, 10, 18, tzinfo=timezone.utc),
            content_sha256="a" * 64,
        )
