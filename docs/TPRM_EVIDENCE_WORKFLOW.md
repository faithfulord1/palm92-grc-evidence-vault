# Palm92 TPRM Evidence Workflow Prototype

## Decision on the Laravel Vault package

The screenshot points to `thetribeofdan/laravel_vault`, an MIT-licensed PHP package for exposing HashiCorp Vault secrets through Laravel configuration. It is not a document store or a third-party-risk evidence workflow. This repository is Python, Terraform, AWS Lambda and S3, so importing that package would add a mismatched runtime without solving the evidence problem.

Keep the two data classes separate:

- **Supplier evidence and its audit metadata:** store in an access-controlled evidence service with explicit retention, provenance, integrity checks and a human review state.
- **Application credentials and API tokens:** keep out of evidence records. The current Lambda uses an AWS execution role and does not need a long-lived Vault token. If a future ingestion integration needs credentials, assess AWS Secrets Manager or Systems Manager Parameter Store with KMS and least-privilege IAM for that workload.

The PHP package can be cited as an example of an application adapter pattern, but it should not be installed in this project.

## Prototype scope

`tprm_evidence.py` creates a metadata-only manifest for a supplier evidence item. It records an opaque supplier reference, evidence type, source channel, received timestamp, mapped control references, optional validity date, content digest and a review state that begins as `pending`.

It does not upload, retain, parse, approve or score supplier files. Use only synthetic data in this public portfolio repository. Do not commit real supplier documents, names, contact details, credentials or evidence hashes. A file hash is an integrity signal, not proof that the supplier's claim is true.

## Intended workflow

1. Receive evidence through an approved, authenticated channel.
2. Store the original file in a private evidence store with access logging and an approved retention policy.
3. Create this manifest from an opaque supplier reference and mapped control IDs.
4. Assign a human reviewer. Record the reviewer, decision, rationale and review time in a later, append-only decision event.
5. Verify the file digest when retrieving it and preserve the original version and provenance.
6. Track expiry and missing evidence. Present findings and uncertainty to a human risk owner; do not turn the manifest into an automated compliance verdict.

## Security architecture learning points

- Separate evidence storage from secrets management.
- Use short-lived workload identity and least-privilege roles instead of embedding cloud credentials.
- Keep metadata minimal and use opaque identifiers in object paths and logs.
- Protect evidence at rest and in transit, restrict access, log retrieval, and define retention before production use.
- Require a human risk owner to accept or reject evidence. Record coverage and provenance, not a guarantee of supplier safety.

## Status and next gate

This is a tested local manifest prototype only. It is not connected to AWS S3, an intake portal, identity provider, approval service or a production retention schedule. Before adding those integrations, specify the data owner, allowed evidence classes, access model, retention and deletion rules, approval roles, and recovery plan. Keep the existing AWS Config collector's production deployment and retention controls separate from this prototype.
