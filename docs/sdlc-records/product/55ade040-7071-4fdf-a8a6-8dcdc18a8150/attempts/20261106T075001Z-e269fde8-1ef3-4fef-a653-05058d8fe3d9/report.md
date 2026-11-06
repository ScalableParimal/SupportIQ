# Requirement Update — Initial Analysis Clarification

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261106T075001Z-e269fde8-1ef3-4fef-a653-05058d8fe3d9`
- **Outcome:** `REQUIREMENT_UPDATED; DRAFT_UPDATED_UNAPPROVED`
- **Created:** 2026-11-06T07:57:41Z (PowerShell system clock converted to UTC while preparing this report)
- **Update scope:** Incorporate only the human decisions answering RA18-Q-01 and RA18-Q-02 from the Requirement Analysis of v1.8.

## Authorization and decision evidence

The user explicitly approved initiating this one Requirement Update attempt. This process-initiation response is not Human Requirement Approval. The exact answers are preserved in `attempt.json` and linked through `evidence/human-decisions.json`.

1. **RA18-Q-01 — Agent assignment outside primary team:** Rejected for first release. Agents may be assigned only within their single current primary team; no cross-team exception, temporary access mechanism, separate approval authority, or added grant is allowed. Tenant Admin routing is tenant-bounded and an Agent must belong to the ticket's assigned team. Primary-team changes use the authorized workflow; authorization loss revokes access immediately, and assignment changes are validated and audited.
2. **RA18-Q-02 — New → Open:** Permitted for a currently assigned, authorized Agent; a Manager for a ticket in an assigned team, including team-queued tickets without an Agent; and a Tenant Admin for any ticket in their own tenant, including completely unassigned tickets. Platform Admin and ticket creation alone do not confer permission. Each transition revalidates current authorization, tenant, team, assignment, and status; unauthorized/undefined transitions are denied, and successful transitions are recorded in activity history and audit logs.

## Source and result identity

| Artifact | Version | Status | Bytes | SHA-256 |
|---|---|---|---:|---|
| `docs/requirement/SupportIQ_Product_Requirement_v1.8.md` | v1.8 | Draft Updated Requirement; unapproved | 117136 | `E7FB3E982555034B098D42E258CAFBEDB651A0A05B736A99DE987DAB6355AD1B` |
| `docs/requirement/SupportIQ_Product_Requirement_v1.9.md` | v1.9 | Draft Updated Requirement; unapproved | 121036 | `67C94027044E31E12EBB91E34145A2BB48FAC1ED96D934C07E2339A9EFD862A2` |

v1.9 was created as a new sequential version from v1.8 after confirming v1.8 was the latest version and the v1.9 destination was absent. Its lineage binds to v1.8's path and SHA-256. v1.8 and all previous requirement versions remain preserved. No status was written into or used to alter the frozen requirement content.

## Change summary

### Added / modified

- Replaced the undefined “authorized user” New → Open rule with the explicit Agent, assigned-team Manager, and Tenant Admin role/scope conditions; excluded routine Platform Admin status transitions and creator-only authority; added per-transition revalidation, default-deny behavior, and activity/audit recording.
- Removed the undefined Agent cross-team assignment exception. Clarified single-primary-team Agent eligibility, Tenant Admin's within-tenant routing and Agent/team match, and Manager assignment boundaries.
- Required server-side tenant/team-membership validation for assignment and reassignment; unauthorized assignments are denied and audited. Clarified immediate access revocation on reassignment, primary-team loss, or other authorization loss.
- Clarified the authorized Tenant Admin primary-team change workflow; any resulting ticket assignment changes must be revalidated and audited.
- Updated first-release acceptance criteria, API/security/end-to-end test coverage, and Definition of Done for these behaviors.

**Affected requirement references:** §5.10 (including FR-TM-01, FR-TM-03–05, FR-TM-07 and the ticket transition/assignment rules); §5.13 (FR-TEAM-03 and FR-TEAM-05); §§13–14; §18.

### Removed / superseded

The v1.8 statements “New → Open is allowed for an authorized user” and “unless an explicitly approved exception exists” are superseded in v1.9. The source v1.8 text is unchanged.

### Scope

No additional product scope was introduced. Cross-team Agent assignment is explicitly excluded from the first release. No automatic ticket reassignment on primary-team change was inferred; if assignments change, they must be validated and audited.

## Consistency and preservation validation

- v1.8 remained 117136 bytes with its expected SHA-256 before and after the update.
- v1.9 was read back; the recorded 121036-byte result hash matches the file.
- Confirmed v1.9 is the next sequential version, the prior undefined exception and transition language are absent, all decision clauses are present, and no v1.10 destination exists.
- Reviewed the changed source-to-result lines; changes are limited to version lineage, ticket transition and assignment rules, team-membership rules, acceptance criteria, test coverage, and Definition of Done.
- The new version remains unapproved. No implementation plan, source code, tests, CI/deployment, or runtime was changed or inspected; no tests/builds, commit, or push were performed.

## Remaining open questions and assumptions

The update does not resolve other v1.8 analysis questions:

- **RA18-Q-03:** Whether separately authorized Platform Admin Customer investigation is in first-release scope and, if so, its authorization controls.
- **RA18-Q-04:** Exact allowlist of audit fields retained after permanent tenant deletion.
- **RA18-Q-05:** Feedback `reason`/`Comment` mapping and whether/how AI urgency suggestions are persisted.
- **§17 deferred configuration:** Model/deployment and region, token/cost limits, email provider/sender, and operation-specific timeout/retry settings.

No new assumptions were added. Existing configurable/proposed values and assumptions remain unchanged.

## Handoff and limitations

**Next governed process:** a separately initiated fresh Requirement Analysis against v1.9, followed by complete independent Requirement Analysis Verification, resolution of material findings/decisions, and separate Human Requirement Approval. This Requirement Update does not initiate any later process or approve the requirement.

The source was read during input preflight before this attempt's invocation record was published; this is explicitly recorded in `attempt.json`. No source modification or decision application occurred before invocation publication. This was a static requirement/process-record review only; implementation, CI/deployment, and runtime behavior remain unverified.
