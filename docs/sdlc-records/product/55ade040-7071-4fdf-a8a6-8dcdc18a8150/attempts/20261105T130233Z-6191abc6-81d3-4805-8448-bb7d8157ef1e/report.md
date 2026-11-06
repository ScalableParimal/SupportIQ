# Requirement Update Report

**Outcome:** Requirement updated; remains unapproved  
**Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`  
**Attempt ID:** `20261105T130233Z-6191abc6-81d3-4805-8448-bb7d8157ef1e`  
**Context:** Initial Analysis Clarification (pre-approval)

## Source, Decisions, and Result

- **Immutable source:** `docs/requirement/SupportIQ_Product_Requirement_v1.6.md`, 99,368 bytes, SHA-256 `2CD66B9C6A20949E3983B37D5DCD91D122F768E55BF63E0C6A85C5B519B4A73F`; Draft Updated Requirement, unapproved.
- **Source status evidence:** The prior Requirement Update result binds v1.6 as unapproved; the fresh Requirement Analysis result also records the exact source fingerprint, `source_modified: false`, and `human_requirement_approved: false`.
- **Analysis basis:** Requirement Analysis attempt `20261105T123811Z-df38a98b-d93e-4dfd-b23a-10173308e9da`, outcome `ANALYSIS_COMPLETE; HUMAN_DECISIONS_REQUIRED; REQUIREMENT_UPDATE_REQUIRED`; questions RA16-Q-01, RA16-Q-02, RA16-Q-03, and RA16-Q-03-followup.
- **Human decisions applied:** RA16-Q-01 permits only FR-AN-06 single-selected-tenant aggregate analytics through the Platform Admin assistant, with no tenant records or documents. RA16-Q-02 adds Customer Read/Search using existing role scopes and keeps Platform Admin separately restricted. RA16-Q-03 and its follow-up define inactivity by absence of active related tickets and start the 365-day period when the last related ticket becomes terminal, Closed or Cancelled. Decision evidence is linked in `evidence/update-evidence.json`.
- **Updated Requirement:** `docs/requirement/SupportIQ_Product_Requirement_v1.7.md`, 101,677 bytes, SHA-256 `E38812289F69CD4338217EDDC6439B76F8749DE68F054C6707D089324A4093A9`.
- v1.6 and all earlier versions remain unchanged. v1.7 is **Draft Updated Requirement; unapproved**.

## Change Summary

### Added

- Added `Customer (Read, Search)` to the default-deny permission catalogue and specified the existing Tenant Admin, Support Manager, Support Agent, and restricted Platform Admin scopes.
- Added acceptance criteria for Customer Read/Search authorization and Customer-record retention, plus corresponding Definition of Done coverage.

### Modified

- Aligned FR-CA-02, FR-ID-09, Section 5.5 role-based tool access, Section 5.9 permission rules, and the acceptance criteria: the Platform Admin assistant may use only FR-AN-06 aggregate analytics for exactly one explicitly selected authorized tenant; it may not access tenant knowledge documents or underlying tenant business records. The existing FR-AN-06 scope itself was not changed.
- Replaced the Customer-record retention row with the approved inactivity definition and a 365-day period beginning at the last related ticket's terminal transition (Closed or Cancelled); aligned the acceptance criteria and Definition of Done.
- Updated the version label and lineage to bind v1.7 to the exact v1.6 source.

### Removed / Superseded

- The prior blanket prohibition on all Platform Admin assistant access to tenant-derived content is superseded by the explicitly bounded FR-AN-06 aggregate-analytics exception; access to tenant documents and underlying records remains prohibited.
- The prior ambiguous Customer-record retention wording is superseded by the approved inactive/terminal-transition rule.
- No other requirement was removed or superseded.

### Scope

Only the three approved clarifications and their directly related permission, assistant-boundary, retention, acceptance, and Definition of Done statements were changed. All 97 unique functional requirement IDs and all 26 Markdown table blocks were preserved; no new functional requirement ID was introduced. No source code, tests, configuration, implementation plan, or other product artifact was changed.

## Validation

- Re-read v1.7 and confirmed its SHA-256 and byte count match the recorded result identity.
- Confirmed v1.6 remains 99,368 bytes with its original SHA-256 before and after the update.
- Confirmed version lineage, unapproved status, all three decisions and the terminal-status follow-up, and consistent assistant restrictions across related sections.
- Compared source and result: 97 unique functional requirement IDs and 26 Markdown table blocks in both; no IDs added or removed. The bounded diff contains only the authorized changes described above.
- No tests or builds were run; this was a documentation-only Requirement Update.

## Remaining Open Questions

- The 365-day rule does not define a start event for a Customer record that has no related tickets; no new start date was inferred.
- The analysis's unrelated open items remain unchanged, including Customer feedback read/review access and deferred model/provider, token/cost, and background timeout/retry decisions.

## Assumptions

No new material assumption was introduced. The no-related-ticket retention case remains explicitly unresolved rather than being assigned an inferred policy.

## Approval Status and Handoff

v1.7 remains **unapproved**. Requirement Update is not Requirement Analysis, independent Requirement Analysis Verification, or Human Requirement Approval. The next governed stage is a separately initiated fresh Requirement Analysis against v1.7, followed by complete independent verification, resolution of any findings, and separate Human Requirement Approval. None of those stages was started in this attempt.

**Generated at (UTC):** `2026-11-05T13:52:15.539Z`