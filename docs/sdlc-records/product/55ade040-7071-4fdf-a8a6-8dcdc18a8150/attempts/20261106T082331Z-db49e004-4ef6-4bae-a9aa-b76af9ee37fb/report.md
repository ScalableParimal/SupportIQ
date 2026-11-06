# Requirement Update — Initial Analysis Clarification

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261106T082331Z-db49e004-4ef6-4bae-a9aa-b76af9ee37fb`
- **Outcome:** `REQUIREMENT_UPDATED; DRAFT_UPDATED_UNAPPROVED`
- **Prepared:** 2026-11-06T08:36:28Z (PowerShell system clock while preparing this report; not a publication timestamp)
- **Prepared by / role:** AI assistant using Copilot SDK in VS Code; Requirement Update executor under the recorded process-initiation authority.
- **Update scope:** Apply only the clarification decisions for RA18-Q-03, RA18-Q-04, RA18-Q-05a, RA18-Q-05b, and RA19-A01 to a new version of v1.9.

## Authorization and decision evidence

The user authorized one Requirement Update attempt against unapproved v1.9, limited to the five recorded clarification groups. The authorization is not Human Requirement Approval. The summary decision index and verbatim user answers are preserved in `evidence/human-decisions.json` and `evidence/human-decisions-verbatim.json`; the exact requirements include:

1. **RA18-Q-03 — Platform Admin Customer access:** Exclude routine and exceptional direct access to individual Customer records, including investigation, from the first release. Limit Platform Admin to platform administration, privileged operations with independent second-admin approval, and explicitly permitted aggregate analytics for one authorized, explicitly selected tenant. Customer email remains masked.
2. **RA18-Q-04 — Post-deletion audit retention:** Retain only the explicit allowlist: audit event ID; irreversibly pseudonymized actor, independent approver (where applicable), and tenant reference; action/event type; resource type and non-business audit reference limited to tenant deletion and privileged approval; necessary structured permission before/after values; UTC request/approval/execution timestamps; outcome/status; and correlation ID. Use irreversible pseudonymization without a mapping, exclude all other fields and sensitive/business content, protect the metadata, and permanently purge no later than the existing 365-day audit-retention expiry.
3. **RA18-Q-05a — Feedback field:** `reason` is the canonical optional free-text field in contracts, models, and Feedback Read. Illustrative `Comment` maps to `reason`, not a separate field. Retain under the existing 90-day policy and scope; audit reads but never copy the free-text into audit logs.
4. **RA18-Q-05b — AI urgency:** Persist `SuggestedUrgency` separately from nullable `ReviewedUrgency`, retain the suggestion after any human override, and persist `ModelId`/deployment reference, `CreatedAt`, nullable `ReviewedBy`, and nullable `ReviewedAt`. Validate configured urgency values, allow authorized humans to review/accept/override, enforce tenant/team/ticket/role authorization, retain for 90 days, and never modify authoritative ticket data automatically.
5. **RA19-A01 — Agent primary-team change:** Block the change until each affected ticket is reassigned to an eligible Agent in its current team or has only `AssignedAgentId` cleared while preserving `AssignedTeamId`. Either the Tenant Admin or Manager of that currently assigned team may perform the disposition; no new approval authority is introduced.

## Source and result identity

| Artifact | Version | Status | Bytes | SHA-256 |
|---|---|---|---:|---|
| `docs/requirement/SupportIQ_Product_Requirement_v1.9.md` | v1.9 | Draft Updated Requirement; unapproved | 121036 | `67C94027044E31E12EBB91E34145A2BB48FAC1ED96D934C07E2339A9EFD862A2` |
| `docs/requirement/SupportIQ_Product_Requirement_v1.10.md` | v1.10 | Draft Updated Requirement; unapproved | 130841 | `93DB568F180A4B6BCFB10B1244730007F96EBE087ABDBC176DC41F63854C60F6` |

v1.10 is the next sequential immutable version and its lineage binds to v1.9's path and SHA-256. v1.9 and all earlier versions remain preserved. The new requirement remains unapproved; approving clarification decisions does not constitute Human Requirement Approval.

## Change summary

### Added / modified

- Explicitly excluded exceptional Platform Admin access to individual Customer records in §4.2 and aligned the role, Customer-access, permission, and acceptance rules. The already-permitted single-tenant aggregate-analytics scope and independent approval for privileged operations remain.
- Replaced broad post-deletion audit-retention wording with an exhaustive allowlist in §5.11, with corresponding audit, deletion-workflow, acceptance, test, and Definition-of-Done requirements in §§5.12, 6.8, 13, 14, and 18.
- Defined canonical Feedback `reason`, the illustrative `Comment` mapping, existing 90-day retention and role scope, and the prohibition on logging free-text reason across §§5.9, 6.13, 8, 9, 13, 14, and 18.
- Added FR-TK-08/09 and aligned TicketAIResult, API, acceptance, test, and Definition-of-Done contracts for separate suggested/reviewed urgency, validation, metadata, authorization, retention, and no automatic authoritative-ticket update.
- Added an Agent primary-team disposition gate and aligned team, API, acceptance, test, and Definition-of-Done requirements in §5.13 and §§9, 13, 14, and 18.
- Updated the version header and lineage.

### Removed / superseded

- Any implication that a separately authorized or exceptional Platform Admin Customer investigation is in first-release scope is excluded.
- General post-tenant-deletion audit examples are superseded by the exhaustive, irreversibly pseudonymized allowlist; no other field may remain.
- The illustrative Feedback `Comment` is not a separate logical or persisted field.
- A primary-team change can no longer proceed while affected tickets remain assigned to the Agent.

### Scope

No unrelated product scope was added. The explicit first-release exclusion is Platform Admin exceptional individual-Customer access. Deferred configuration decisions in §17 remain unchanged.

## Consistency and preservation validation

- Verified v1.9 remains 121036 bytes with its expected SHA-256; v1.10 is 130841 bytes and reads back with the recorded result SHA-256.
- Confirmed v1.10 is the latest sequential version and its lineage references the exact v1.9 identity.
- Reviewed the affected requirement, workflow, entity, API, acceptance, test, and Definition-of-Done surfaces. Markdown table rows have consistent pipe counts.
- Confirmed all five approved decision groups are reflected, no unapproved recommendation was introduced, and §17's model/deployment/region, token/cost, email provider/sender, and operation-specific timeout/retry decisions remain open.
- No source code, implementation plan, or tests were changed. No tests/builds, commit, push, or later SDLC process were performed.

## Remaining open questions and assumptions

The following existing §17 configuration decisions remain unresolved:

- Exact Azure AI generation and embedding model deployments and region.
- Model-specific token limits and monthly cost budget.
- Email provider, sender identity, and deployment configuration.
- Bounded per-operation timeout and retry settings.

No new material assumptions were added.

## Process-ordering caveat and handoff

The v1.9 Requirement Analysis report preserves a prior process-ordering caveat: earlier Requirement Update/analysis work included bounded source/predecessor pre-reads before invocation publication. This update's invocation records that v1.9 content was read only after its invocation was published. The earlier caveat is not retroactively cleared; preserve it for the next governed analysis and verification.

**Next process:** Fresh Requirement Analysis against v1.10, only after separate process-initiation approval. Complete independent Requirement Analysis Verification and the required finding/decision resolution must precede separate Human Requirement Approval. This Requirement Update does not start those processes or approve v1.10.
