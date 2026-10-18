"""Create metadata-only manifests for third-party risk evidence.

This module deliberately does not upload, retain, or parse supplier documents.
It produces a manifest that can later be stored beside an access-controlled
evidence object after an approved intake workflow is in place.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable


_OPAQUE_REFERENCE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")
_SHA256 = re.compile(r"^[a-f0-9]{64}$")


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 digest of a file without loading it all into memory."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")

    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(payload: dict) -> str:
    """Serialize a manifest consistently so its digest is reproducible."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _opaque_reference(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not _OPAQUE_REFERENCE.fullmatch(value):
        raise ValueError(
            f"{field_name} must be an opaque reference using 1-80 letters, "
            "numbers, dots, underscores, or hyphens; do not use names or email addresses"
        )
    return value


def _utc_timestamp(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("received_at must include a timezone")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def build_manifest(
    *,
    supplier_ref: str,
    evidence_type: str,
    source_channel: str,
    received_at: datetime,
    content_sha256: str,
    control_refs: Iterable[str] = (),
    valid_until: date | None = None,
) -> dict:
    """Build a TPRM evidence manifest with review pending by default.

    The manifest contains references and hashes only. It must not contain the
    evidence body, a supplier contact's personal details, or credentials.
    """
    supplier_ref = _opaque_reference(supplier_ref, "supplier_ref")
    evidence_type = _opaque_reference(evidence_type, "evidence_type")
    source_channel = _opaque_reference(source_channel, "source_channel")

    if not isinstance(content_sha256, str) or not _SHA256.fullmatch(content_sha256):
        raise ValueError("content_sha256 must be a lowercase SHA-256 hex digest")

    refs = sorted({_opaque_reference(ref, "control_ref") for ref in control_refs})
    if not refs:
        raise ValueError("at least one control_ref is required")
    if valid_until is not None and (
        isinstance(valid_until, datetime) or not isinstance(valid_until, date)
    ):
        raise ValueError("valid_until must be a date or None")

    manifest = {
        "schema_version": "1.0",
        "record_type": "third_party_evidence",
        "supplier_ref": supplier_ref,
        "evidence_type": evidence_type,
        "source_channel": source_channel,
        "received_at": _utc_timestamp(received_at),
        "content_sha256": content_sha256,
        "control_refs": refs,
        "valid_until": valid_until.isoformat() if valid_until else None,
        "review": {
            "status": "pending",
            "reviewer_ref": None,
            "reviewed_at": None,
        },
    }
    manifest["manifest_sha256"] = hashlib.sha256(
        canonical_json(manifest).encode("utf-8")
    ).hexdigest()
    return manifest
