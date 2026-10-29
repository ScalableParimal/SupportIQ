# Requirement Update Report

## Work and process

- Work/feature: `supportiq-product-baseline`
- Process: Requirement Update
- Attempt: `20261028T181320Z-81942fff-346a-461f-94af-4d58630d48cd`
- Predecessor: Requirement Analysis attempt `20261028T173927Z-caec8459-e14b-46bf-a687-c557e521e419`, outcome `REQUIREMENT_ANALYSIS_COMPLETE_BLOCKING_DECISIONS`.
- Updated Requirement: `docs/requirement/SupportIQ_Product_Requirements_Document.docx`
- Source SHA-256 before update: `EE752A1B0541EAC55027A3A61CB5485996CB3BD5484E4CE4348B8829DE5CF7FA`
- Updated Requirement SHA-256: `14AF65ACC24885C2378D47313EF41C6B0573283602913F812B7D9E36746709B5`

## Change summary

### Added

- SQL-backed local SupportIQ application accounts (not end-user SQL credentials), salted password hashes, restricted account creation, sign-in rate limiting, a separate protected least-privilege app database service identity, and explicit least-privilege tenant-scoped permissions.
- Versioned knowledge lifecycle states: draft -> review -> approved/current -> superseded, expired, or rejected. Only approved/current content is searchable, submitters cannot approve their own versions, and stale/conflicting content requires abstention and human-review flagging rather than silent source selection.
- A 25 MiB per-file limit, re-review at 180 days, active approved originals retained while current, immediate retrieval block on deletion, 24-hour purge of originals/extracted text/chunks/indexes/caches, encrypted backups aging out within 30 days, content-free deletion/audit metadata retained for 365 days, and failed/rejected uploads purged within 24 hours.
- Tenant-configurable ticket categories/priorities owned by the tenant Support Manager; AI may suggest a queue/escalation but cannot autonomously escalate.
- Human approval of numeric quality thresholds before release, without inventing threshold values.
- Deterministic synthetic ticket seed data.

### Modified

- Tenant Admin, Support Agent, Support Manager, and Platform Admin responsibilities and access summaries to reflect the approved tenant boundaries, least privilege, and exceptional time-limited, reasoned, audited Platform Admin access.
- First-release integration tools are read-only; drafts may be edited in SupportIQ, but ticket/customer write-back through integrations and customer-message sending are not allowed.
- Azure AI remains in the architecture; exact model/deployment/region selection is deferred until availability, quota, cost, and embedding/index compatibility are validated.
- Listed evaluation/sample volumes are initial targets, not hard minimums.
- Related workflows, guardrails, acceptance criteria, security/privacy requirements, test coverage, and the risks/assumptions/open-questions table were aligned with these decisions.

### Removed / superseded

- Replaced the unresolved PRD questions about authentication provider, file-size/retention rules, and ticket-population method with the approved decisions.
- Replaced the prior “at least” evaluation-set language and optional first-release integration write behavior with the approved targets and read-only boundary.

### Scope

- Only the designated PRD was modified as the source Requirement. Only this Requirement Update actor's records were published in this attempt directory.
- No source code, tests, plans, configuration, other documentation, governance artifacts, other actor records, or human-gates were changed. No commit or push occurred.

## Remaining open questions

- Exact Azure AI model/deployment/region, pending availability, quota, cost, and embedding/index compatibility validation.
- Numeric evaluation quality-threshold values, which must receive explicit human approval before release. No values were invented.

## Assumptions

- No material business decision was inferred beyond the explicit decisions supplied. The Azure AI deployment remains unselected, and evaluation threshold values remain unset.

## Validation and approval status

- DOCX ZIP integrity and all XML/relationship parts: PASS.
- Updated text extraction, affected-section consistency, accepted-decision coverage, and scan for superseded statements: PASS.
- Master Governance fingerprints remain unchanged. The only modified tracked file is the authorized PRD.
- No native Word/LibreOffice rendering was performed; validation was structural and text-based.
- **Status: Draft Updated; not an Approved Requirement. Human Requirement Approval has not been granted.**
- Requirement Analysis refresh, Requirement Analysis Verification, and all downstream processes were not invoked. Stop at the Requirement Update boundary as requested.
