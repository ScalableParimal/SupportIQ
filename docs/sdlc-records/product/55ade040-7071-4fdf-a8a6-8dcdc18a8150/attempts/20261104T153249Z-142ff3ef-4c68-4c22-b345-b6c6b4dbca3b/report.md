# Requirement Update Report

## 1. Identity and outcome

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261104T153249Z-142ff3ef-4c68-4c22-b345-b6c6b4dbca3b`
- **Update context:** Initial Analysis Clarification (pre-approval).
- **Outcome:** A new immutable Requirement version 1.2 was created from version 1.1 and updated with the explicitly authorized decisions.
- **Approval status:** Draft Updated Requirement. Version 1.2 remains unapproved; this update and the decisions applied do not constitute Human Requirement Approval.

## 2. Source and resulting versions

| Version | Path | Version ID | SHA-256 | Lifecycle status |
|---|---|---|---|---|
| Predecessor | `docs/requirement/SupportIQ_Product_Requirement_v1.1.md` | `SupportIQ Product Requirement v1.1@sha256:E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2` | `E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2` | Draft; unapproved Initial Analysis Clarification |
| Result | `docs/requirement/SupportIQ_Product_Requirement_v1.2.md` | `SupportIQ Product Requirement v1.2@sha256:D206C95AD75E0D7E1B1169144B29ADE219F3C42299FE5C3ED3C20F75DD8D99AA` | `D206C95AD75E0D7E1B1169144B29ADE219F3C42299FE5C3ED3C20F75DD8D99AA` | Draft Updated Requirement; unapproved |

Version 1.2 is an immutable successor/clarification draft of version 1.1. Version 1.1 remains unchanged. Its version 1.0 predecessor also remains unchanged at 26,513 bytes with SHA-256 `ED2C910654FA39BE995D716F063C45BFE4183D8A4E8C6CB5B1C1194F8C17A871`.

## 3. Human authorization and input

The user explicitly authorized a separate Requirement Update to create an unapproved version 1.2 from version 1.1, incorporating the answers to analysis questions A-01 through A-09 and follow-up clarifications for ticket closure/cancellation, first-release real email, cancelled-ticket retention, and tenant-deletion reversal. The exact decision record is `evidence/human-decisions.json`; the analysis basis is the fresh post-update Requirement Analysis attempt `20261104T143939Z-277dd15a-118a-4c89-840f-a0b69d5b50f0`. Older unrelated analysis/update evidence was excluded as instructed.

This authorization does not approve version 1.2, authorize implementation planning or implementation, or authorize a downstream process to start automatically.

## 4. Change summary

### Added

- Tenant Admin approval/rejection of exact processed knowledge versions; processing and approval states are separate, and pending, rejected, failed, unapproved, or stale versions are excluded from search and AI context.
- Default-deny role/resource/action permissions, privileged Platform Admin change approval by an independent second administrator, and tenant-scoped support-team management.
- Explicit team/ticket access boundaries, customer/ticket lookup field allowlists and email masking, and a complete ticket transition model including terminal cancellation.
- Configurable retention for tickets, customers, users, activity, feedback, ticket AI results, audit, conversations, evaluations, documents, and backups; tenant deactivation/deletion and dual-control reversal rules.
- Persisted asynchronous processing, HTTP 202/Job ID submission, authorized status/result retrieval, independent bounded timeouts, and safe retry behavior.
- ASP.NET Core Identity recovery rules and real transactional email in the first release, with final provider selection deferred to implementation.
- Explicit non-gating evaluation governance and scoring definitions for retrieval, grounding, citation correctness/coverage, abstention, structured-output failure rates, and prompt-injection handling.

### Modified

- Updated the version/status lineage, roles, first-release scope, workflows, architecture, entities, API examples, non-functional requirements, test strategy, acceptance criteria, delivery boundary, risks, backlog, and glossary to reflect the approved decisions consistently.
- Resolved the previously open ticket-transition, customer lookup, audit retention/access, and evaluation-target questions in the new version.

### Removed / superseded

- Replaced automatic retrieval of successfully indexed documents with explicit version-specific Tenant Admin approval.
- Replaced the previous ticket statuses/transition ambiguity; closure is only from Resolved, while Cancelled is distinct, terminal, and not deletion.
- Replaced unresolved Customer Lookup fields and audit retention/access questions with explicit data minimization, scope, and retention rules.
- Replaced any implication that evaluation percentages could become gates solely through Requirement Approval; they remain non-gating unless changed by a separate explicit human decision.
- Replaced deferred email integration with in-scope real transactional email; the specific provider remains an implementation-time choice.
- No version 1.0 or 1.1 artifact was modified or removed.

### Scope

The explicitly authorized first-release requirements now include approval-gated knowledge retrieval; tenant/team administration and scoped ticket operations; cancellation; expanded retention and tenant lifecycle; persisted async jobs; local account recovery with real transactional email; and non-gating AI quality measurement. Existing limitations remain, including no automated customer-facing messages, no AI-invoked write tools, no custom roles/tenant permission overrides, no enterprise SSO, and no production external ticketing/CRM/messaging integrations.

### Remaining open questions

- Exact Azure AI generation/embedding deployments, region, quotas, model-specific token caps, and monetary budget remain deferred to the technical decision gate.
- The final email provider, sender identity, and deployment settings will be selected/verified during implementation; Azure Communication Services Email or SendGrid are acceptable candidates.
- Operation-specific bounded background timeout and retry values remain dependent on provider constraints and observed latency.
- Proposed retention defaults must be validated against applicable legal/business obligations before any production use.

These are explicit technical/deployment deferrals, not decisions silently made in this update.

## 5. Validation and preservation

- Version 1.2 was created separately; it is 77,893 bytes with SHA-256 `D206C95AD75E0D7E1B1169144B29ADE219F3C42299FE5C3ED3C20F75DD8D99AA`.
- Read-back verified version 1.2 and its version ID.
- Version 1.1 remains 47,725 bytes with SHA-256 `E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2`; version 1.0 remains 26,513 bytes with SHA-256 `ED2C910654FA39BE995D716F063C45BFE4183D8A4E8C6CB5B1C1194F8C17A871`.
- Structural checks found 94 functional requirement IDs with no duplicate definitions, all expected top-level sections 1–18, and 26 Markdown table blocks with consistent column counts.
- Decision-focused checks confirmed the version remains unapproved, approval gating and retrieval restrictions are stated, ticket closure/cancellation and retention rules are present, tenant-deletion dual control is present, long-running work returns HTTP 202 with authorized jobs, evaluation metrics remain non-gating, and customer/email privacy constraints are stated.
- This was a documentation-only Requirement Update. No code, tests, configuration, implementation plan, build, runtime, or live integration was changed or exercised.

## 6. Handoff and process boundary

The next process is a separately initiated fresh Requirement Analysis against version 1.2, followed by complete independent Requirement Analysis Verification and resolution of any findings/decisions. Human Requirement Approval remains a separate explicit human decision. This update does not approve the Requirement or authorize planning or implementation.
