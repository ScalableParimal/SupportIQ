# Requirement Update Report

**Outcome:** Requirement updated; remains unapproved  
**Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`  
**Attempt ID:** `20261105T100539Z-d2467ce6-2ee0-44bc-9974-47b2442fc8a0`  
**Completed:** 2026-11-05T10:20:08.102Z  
**Context:** Initial Analysis Clarification (pre-approval)

## Source, Authorization, and Result

- **Immutable source:** [SupportIQ_Product_Requirement_v1.3.md](../../../../../requirement/SupportIQ_Product_Requirement_v1.3.md), 95,458 bytes, SHA-256 `AC40CB29AF795253B5C1C11AA200757C04CE460650FDC5799E69B9276491C496`; Draft Updated Requirement, unapproved.
- **Authorization:** The user separately authorized initiating this Requirement Update and publishing only this attempt's invocation, report, result, and necessary evidence in its designated attempt directory.
- **Analysis basis:** Requirement Analysis attempt `20261105T094456Z-5a38f2de-6a85-47a2-99df-3f650c49a5bd`; its current report revision, result, and decision evidence are bound in the invocation and update evidence.
- **Updated Requirement:** [SupportIQ_Product_Requirement_v1.4.md](../../../../../requirement/SupportIQ_Product_Requirement_v1.4.md), 98,684 bytes, SHA-256 `332EEE3EC6C2D2A145EEF6C26BC567D9FD73B95DD118FB86C63DCB848ABFBF5F`.
- v1.3 and all earlier versions remain preserved unchanged. v1.4 is **Draft Updated Requirement; unapproved**.

## Change Summary

### Added

- `FR-AN-06` specifies dashboard, ticket-trend, and predefined natural-language analytics scopes for Tenant Admin, Support Manager, Support Agent, and Platform Admin. Platform Admin analytics are aggregate-only for one explicitly selected authorized tenant, with no cross-tenant view or underlying tenant business records.
- An explicit first-release restriction that the AI Customer Assistant is available only to the four authenticated internal roles; external CloudDesk customers cannot access it.

### Modified

- Clarified `FR-CA-01`, first-release scope, assistant access criteria, and API/security/end-to-end testing to enforce the internal-only assistant audience.
- Bound the analytics allowlist, dashboard, trends, role/tool permissions, acceptance criteria, test strategy, and Definition of Done to the role scopes in `FR-AN-06`.
- Updated `FR-ID-14`, account recovery rules, and the recovery workflow so deactivated user accounts cannot reset passwords until separately reactivated; generic reset responses remain required.

### Removed / Superseded

- Superseded the ambiguous assistant audience implied by generic “Users” wording and the underspecified tenant-scoped analytics language with explicit, testable role scopes.
- Superseded the incomplete statement that reset did not reactivate a deactivated account with an explicit reset-eligibility rule. No unrelated requirement was removed.

### Scope

Only the three human decisions recorded as `RA-A-01` through `RA-A-03` were applied, with directly related consistency updates. No features, implementation details, or other business decisions were added.

## Validation

- Reviewed the v1.3-to-v1.4 diff; all changes are confined to the approved clarification surfaces.
- All 18 numbered sections were preserved. The document contains 97 unique functional requirement IDs and 26 Markdown table blocks with consistent columns.
- Verified the new version's source lineage, unapproved status, exact analytics scopes, assistant audience, reset eligibility, and preservation of existing open questions and assumptions.
- Published v1.4 under a new path using no-overwrite atomic publication. Final read-back matched the recorded size and SHA-256; v1.3 matched its original SHA-256 before and after publication. No `.partial` file remains.
- No source code, tests, configuration, implementation plan, or unrelated product artifact was changed. No builds or tests were run for this documentation-only Requirement Update.

## Remaining Open Questions

- Select the Azure AI generation and embedding model deployments and region; verify availability, Search compatibility, quotas, pricing, and regional support.
- Set model-specific token limits and monthly cost budget.
- Select the email provider, sender identity, and deployment configuration.
- Set per-operation background timeout and retry values against provider constraints and observed latency.
- Validate the proposed retention and deletion defaults against legal and business requirements before production use.

## Assumptions

No new material assumption was introduced. Existing synthetic-data, Azure resource availability, and proposed retention assumptions remain unchanged.

## Approval Status and Handoff

v1.4 remains **unapproved**. This Requirement Update is not Requirement Analysis, independent Requirement Analysis Verification, Human Requirement Approval, Implementation Planning, or implementation authorization. After separate process initiation, the next governed process is a fresh Requirement Analysis against v1.4, followed by complete independent verification, resolution of any findings, and separate Human Requirement Approval.

**Evidence:** `evidence/update-evidence.json` (fingerprinted in the result record).
