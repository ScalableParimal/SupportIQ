# Requirement Update Report

## 1. Identity and outcome

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261104T143031Z-e7ca6b97-53ac-4105-9ebb-3bf449ca0b18`
- **Update context:** Initial Analysis Clarification (pre-approval).
- **Outcome:** A new immutable Requirement draft was created from the identified version 1.0 source. The original source remains unchanged.
- **Approval status:** Draft Updated Requirement. It is not approved; clarification decisions do not constitute Human Requirement Approval.

## 2. Source and resulting versions

| Version | Path | Version ID | SHA-256 | Lifecycle status |
|---|---|---|---|---|
| Source | `docs/requirement/SupportIQ_Product_Requirement.md` | `SupportIQ Product Requirement v1.0@sha256:ED2C910654FA39BE995D716F063C45BFE4183D8A4E8C6CB5B1C1194F8C17A871` | `ED2C910654FA39BE995D716F063C45BFE4183D8A4E8C6CB5B1C1194F8C17A871` | Initial unapproved draft baseline |
| Result | `docs/requirement/SupportIQ_Product_Requirement_v1.1.md` | `SupportIQ Product Requirement v1.1@sha256:E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2` | `E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2` | Draft; pending subsequent analysis, independent verification, and separate Human Requirement Approval |

Version 1.1 is the immutable successor/clarification draft of version 1.0. Version 1.0 remains preserved as the original source; it is not marked Approved or Superseded.

## 3. Human authorization and input

The user explicitly authorized an **Initial Analysis Clarification Requirement Update**, confirmed the supplied revised first-release scope as mandatory, and directed that the evaluation percentages be included only as proposed targets, not formal release gates. The complete decision inputs are bound in `evidence/human-decisions.json`.

The update used the current Requirement Analysis report `20261104T133354Z-d37bd154-22f0-4341-bb7b-a0d2faa482bf/report.md`, which was based on the user's designated initial draft and did not use any earlier Requirement Analysis or Requirement Update report/evidence.

## 4. Change summary

### Added

- Local ASP.NET Core Identity authentication; tenant/user provisioning; predefined roles; centralized resource/action RBAC; administrative views and audit rules.
- Administrative controls for validated, versioned operational limits and configurable retention/deletion policies.
- Complete internal ticket lifecycle requirements, initial synthetic dataset, fields, categories, priorities, queues, and role boundaries.
- Explicit read-only AI tool and analytics allowlists, role scopes, and prohibition on AI-invoked write tools in the first release.
- Initial operational defaults: 60 general API requests/user/minute, 10 AI requests/user/minute, two concurrent AI requests/user, 30-second general API timeout, 60-second model timeout, 20 MB file limit, and 10 conversation turns.
- Proposed retention defaults: active-document retention for originals/versions/derived data; immediate retrieval unavailability and physical purge within 30 days; backups up to 30 days; logs 30 days; conversations and synthetic evaluation data/results 90 days.
- Proposed AI evaluation targets for Recall@5, grounded answers, citation precision, abstention, structured outputs, and prompt-injection handling. They are explicitly not formal release gates in this draft; cross-tenant access denial remains a mandatory acceptance criterion.
- A module-based 30-day delivery boundary with no fixed weekly schedule, plus expanded acceptance, test, audit, and administration expectations.

### Modified

- Updated the first-release scope and role descriptions to include the confirmed administrative console and core ticket lifecycle.
- Clarified the 20 MB upload maximum, 10-turn conversation context, 7/30-day ticket trends, synthetic data generation, and human review/AI write boundaries.
- Updated architecture, logical entities, API examples, non-functional requirements, workflows, test strategy, definition of done, and backlog to remain consistent with the clarified scope.

### Removed / superseded

- The former narrow ticket list/detail-only scope and fixed week-by-week delivery table were replaced in version 1.1 by the confirmed ticket lifecycle and module-based planning boundary.
- The previous open questions for authentication provider, file size/retention, ticket seeding, and tool scope were resolved or bounded by the supplied decisions. Exact model deployments, region, token limits, monetary budget, and other listed open items remain unresolved.
- No source file or previously created Requirement version was edited or removed.

### Scope

The user's explicitly confirmed expanded scope is included in version 1.1: tenant/user administration, RBAC and configuration controls, complete core ticket management with synthetic data, knowledge-to-RAG, AI assistance, read-only tools/analytics, audit, evaluation, and operational controls. Internal notes, Entra ID/enterprise SSO, AI-invoked write tools, external production integrations, SLA indicators, custom roles/tenant permission overrides, and other stated optional capabilities remain deferred or out of scope.

## 5. Remaining open questions and assumptions

- Exact Azure AI generation and embedding model deployment identifiers, region, availability/quotas, model-specific token caps, and monthly cost budget remain deferred to a technical decision gate.
- The supplied evaluation percentages remain proposed targets, not formal release gates. Their gate status requires the later Human Requirement Approval process.
- Exact ticket status-transition rules and any additional Tenant Admin ticket actions remain unspecified and must not be inferred.
- The minimal customer fields returned by Customer Lookup remain to be defined.
- Audit-record retention duration and detailed audit-read permissions remain open.
- Exact API contracts, schemas, operational configuration semantics, and implementation sequence remain for their governed downstream design/planning processes.
- The document remains a learning/demo scope; it does not claim production readiness, realized quality, or security assurance.

## 6. Validation and preservation

- The version 1.1 source was copied from the exact version 1.0 bytes and updated as a separate file.
- Read-back verified version 1.1 at 47,725 bytes with SHA-256 `E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2`.
- The original version 1.0 remained at 26,513 bytes with SHA-256 `ED2C910654FA39BE995D716F063C45BFE4183D8A4E8C6CB5B1C1194F8C17A871`.
- Structural validation found 72 defined functional requirement IDs with no duplicate definitions and confirmed the expected sections and key approved decisions.
- No code, tests, configuration, implementation plan, or governance source was modified. No build, test, runtime, or live integration was run.

## 7. Handoff and process boundary

The next eligible process is a fresh Requirement Analysis/analysis refresh against version 1.1, followed by complete independent Requirement Analysis Verification, resolution of any remaining findings/decisions, and separate Human Requirement Approval. This update does not start those processes, approve the Requirement, authorize implementation, or authorize an implementation plan.
