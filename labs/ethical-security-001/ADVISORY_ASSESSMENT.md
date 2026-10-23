# Palm92 security advisory response: verified phase report

Date: 23 October 2026
Owner: Faith Wright / Palm92 Intelligence

## Completed

- Original offline SQL injection exercise, fixed using parameter binding. Seven checks passed. Synthetic data only; no external targets.
- RepoGuard read-only PHP indicator inventory implemented in src/repoguard/php_inventory.py. Five focused regression cases passed through a direct Python runner; pytest was unavailable in the execution environment.
- Four repository snapshots examined: 110 tracked files total. No PHP source/Composer indicators or PHP-related text references found. One binary video skipped. RepoGuard had untracked new inventory implementation/test files during collection; the tracked snapshot was unchanged.
- Published LinkedIn caption and generated Palm92 graphic, verified through successful publication message and live post: https://www.linkedin.com/feed/update/urn:li:share:7519214531009646594/
- Produced a 36-second 1080x1920 H.264 silent captioned motion graphic companion. Representative frames checked. It illustrates recorded lab outcomes; it is not a screen recording or narrated film. Renderer is included in this folder. Video has not been published to LinkedIn.

## Repository inventory

| Repository | Tracked files | Observed stack | PHP source indicators | Hosted infrastructure |
|---|---:|---|---|---|
| jobshield-ai | 5 | HTML/CSS/JavaScript | None found | Unknown |
| palm92-governed-agent-mcp | 32 | Python; Render and Vercel config files | None found | Unknown |
| palm92-repoguard | 66 | Python | None found in captured tracked snapshot | Unknown |
| palm92-verified-request | 7 | Node.js package manifest | None found | Unknown |

Exact commits and exclusions are in php-inventory.json. Results are bounded source observations, not patch verification. Manifest declarations do not prove a live deployment. No PHP changes were made because no matching runtime was established in the inspected source.

## Reproduce inventory

From a checkout of palm92-repoguard:

    PYTHONPATH=src python -m repoguard.php_inventory /path/to/authorised/git/checkout

The checker reads tracked working-tree files and returns source_status and deployment_status separately. PHP references in documentation or the checker itself are review leads, not findings of exposure. No CVE/version exploitability decision is made.

## Remaining production gate

For each live service, obtain its verified deployment identity, current runtime/package build, bundled components and provider advisory response. If PHP exists, compare provider patch/backport evidence to current official PHP/NCSC guidance. Then record owner, action, date, validation and remaining uncertainty. No hosting credentials or provider attestation were available in this source-only phase.

## Small pilot service definition

Deliver an advisory impact review to one consenting community organisation: authorised asset list, source evidence, hosting questions, named action owner and closure checklist. The pilot is not a penetration-testing certification. No client has been contacted, enrolled or charged. Deliver a sample first and establish actual effort before pricing.

## Evidence model

Permission → scope → evidence → reproduce where authorised → fix → retest → human review → closure record.

AI investigates. Humans decide.
