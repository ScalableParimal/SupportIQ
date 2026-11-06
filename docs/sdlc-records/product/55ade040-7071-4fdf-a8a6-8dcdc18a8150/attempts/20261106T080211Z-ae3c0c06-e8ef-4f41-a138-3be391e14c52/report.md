# Requirement Analysis — SupportIQ v1.9

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261106T080211Z-ae3c0c06-e8ef-4f41-a138-3be391e14c52`
- **Outcome:** `ANALYSIS_COMPLETE; RA18-Q-01/Q-02_RESOLVED; OTHER_DECISIONS_REMAIN; GOVERNANCE_ORDERING_CAVEAT`
- **Authoritative Requirement:** `docs/requirement/SupportIQ_Product_Requirement_v1.9.md`
- **Version/status:** v1.9; Draft Updated Requirement; unapproved
- **Source binding:** 121,036 bytes; SHA-256 `67C94027044E31E12EBB91E34145A2BB48FAC1ED96D934C07E2339A9EFD862A2`

## Source, process, and decision lineage

The Request `docs/ai/request/REQUIREMENT_ANALYSIS_REQUEST.md` remains an unpopulated template. The current conversation supplies the target and explicit authorization for one fresh v1.9 Requirement Analysis; this is process initiation, not Human Requirement Approval or a product decision.

The preceding v1.8 Requirement Analysis attempt `20261106T072405Z-9c32b0cf-d339-444e-9435-852e206a61d5` completed with unresolved blocking questions RA18-Q-01/Q-02 (result SHA-256 `119A9EFB68197585E06F4C0F4B4FA985D89D5C339BD2F7873E610333B7700EE7`). The Requirement Update attempt `20261106T075001Z-e269fde8-1ef3-4fef-a653-05058d8fe3d9` completed as `REQUIREMENT_UPDATED; DRAFT_UPDATED_UNAPPROVED` (result SHA-256 `48DF55B138D2C6C2B39884F8E4D8504834D43812939B8364E673B26C5920B39C`). It records v1.8 at SHA-256 `E7FB3E982555034B098D42E258CAFBEDB651A0A05B736A99DE987DAB6355AD1B` and v1.9 at the source hash above. The update's `attempt.json` contains the exact human answers, and its `evidence/human-decisions.json` links the answers for RA18-Q-01 and RA18-Q-02. This analysis checked both answers against the resulting v1.9 text. The new version remains unapproved.

### Human decisions incorporated (not approval)

1. **RA18-Q-01 — Agent assignment outside primary team:** No cross-team Agent assignment, exception, temporary access, separate approval authority, or added grant in the first release. An Agent may be assigned only within their single primary team. Tenant Admin routing is tenant-bounded and an Agent must belong to the ticket's assigned team. Team changes use the authorized workflow; authorization loss revokes access immediately. Assignments require server-side tenant/team validation and audit; unauthorized assignment is denied and audited.
2. **RA18-Q-02 — New → Open:** Permitted to (a) the currently assigned Agent who retains team/tenant authorization, (b) a Manager for a ticket in an assigned team, including team-queued tickets, and (c) a Tenant Admin for any ticket in their own tenant, including completely unassigned tickets. Platform Admin and ticket creation alone confer no such permission. Every transition revalidates current authorization, tenant, team, assignment, and status; undefined/unauthorized transitions are denied by default; successful transitions are recorded in activity history and audit logs.

These answers are now reflected in §5.10, §5.13 and related acceptance/test/Definition-of-Done clauses. They are the only human decisions supplied for this refresh. RA18-Q-03/Q-04/Q-05 and §17 questions remain open as listed below.

### Prior Requirement Update source pre-read disclosure

The Update invocation and its report/evidence disclose that v1.8 was read during input qualification/preflight before that Update's own `attempt.json` was published; they also state that no source modification or decision application occurred before publication. This does not change v1.8/v1.9 fingerprints, the recorded human answers, or their content lineage, and this analysis does not alter predecessor records. Under SDLC_ARTIFACT_GOVERNANCE §33.1 and SDLC_TRACEABILITY_AND_CHANGE_CONTROL §30.1, the evidence supports a bounded non-mutating preflight explanation, but it does not establish strict invocation-publication-before-any-source-review ordering. Treat this as a process-ordering caveat for independent assessment; do not infer retroactive compliance or invalidate the product source solely from the pre-read.

This fresh attempt likewise inspected source and predecessor records during input preflight before its own invocation publication. Checkpoint 0001's broad assertion that execution started only after invocation read-back was inaccurate; immutable checkpoint 0003 corrects and links that assertion. The final report and evidence were prepared after the invocation publication, and no product source was changed. The ordering caveat is preserved rather than hidden.

## 1. Understanding

- **Business objective:** Define a demonstrable, learning-oriented but production-minded SupportIQ portal for fictional B2B SaaS provider CloudDesk. The target release combines tenant-aware administration, approved-knowledge RAG, internal ticket operations, AI assistance, scoped customer/feedback access, analytics, and operational safeguards. The 30-day target is not a schedule or guarantee; the document disclaims a production-readiness commitment.
- **Actors:** Platform Admin, Tenant Admin, Support Manager, Support Agent; external CloudDesk customers cannot use the AI Customer Assistant.
- **Main behavior:** Internal users work tenant/team-scoped tickets and permitted customer records; search only approved current knowledge; receive grounded/cited or abstaining AI assistance; and use auditable administrative, retention, job, and notification workflows. Human agents retain responsibility for customer-facing decisions and communications.
- **Source hierarchy:** v1.9 is the current analysis input, but remains unapproved. The Update result/evidence establishes its lineage and the two incorporated answers. The template Request supplies no additional product decisions. Analysis recommendations and process-initiation statements are not requirements.

## 2. Explicit Requirements

### Functional and business rules

- **Identity, permissions, and administration (§3, §5.9):** Local ASP.NET Core Identity; four predefined roles; centralized, versioned resource/action permission catalogue; default-deny tenant/team/resource/action/owner checks; no self-registration, custom roles, tenant overrides, privilege escalation, or self-approval. A second independent Platform Admin approves defined privileged Platform Admin changes. User/team administration is tenant-scoped.
- **Teams and tickets (§5.10, §5.13):** Each Agent has one primary team; Managers can manage assigned teams. Tenant Admin has tenant-wide central triage, including fully unassigned tickets; Managers are confined to assigned teams, including team-queued tickets; Agents' ticket/customer access depends on current assignment and authorized scope. Ticket states, transitions, taxonomy, priority, editable fields, correction and cancellation requests, escalation, resolution/closure/reopening, audit, and retention are specified. The New → Open and Agent assignment rules are now explicitly bounded by RA18-Q-01/Q-02. Undefined actions are denied.
- **Knowledge, AI, and tools (§5.1–5.5, §5.8, §11):** Only exact currently approved knowledge versions may be retrieved; approval is invalidated on reprocessing/replacement. RAG and tools are tenant/role scoped, read-only and allowlisted; no arbitrary SQL, shell/network, AI write actions, autonomous business changes, or unsupervised customer communication. Outputs require grounding/citations or abstention, structured validation, safe failure handling, and human review where applicable.
- **Customer, feedback, analytics (§5.5–5.7, §5.9):** Customer Search supports specified exact/partial matching, filters, sorts, pagination and returned fields; applies role/ticket scope and direct-ID revalidation. Email is masked by default; only own-tenant Tenant Admin detail view may unmask, with audit. Feedback Read is role-scoped and field-limited, not conversation/message access. Analytics are predefined, read-only, scoped per FR-AN-06, and label scope/time range. Proposed AI evaluation targets are measures, not release gates; tenant/team/role authorization remains mandatory.
- **Retention, deletion, audit (§5.11–5.12):** Configurable proposed retention defaults; Customer retention depends on related ticket state and specified timer/reset behavior. Tenant deletion uses a 30-day grace period and independent dual-admin control; it overrides deactivated-user retention but preserves protected minimal audit metadata while excluding secrets, personal email, unnecessary personal data, and deleted business content. Security/admin audit is retained separately.
- **Jobs, email, quality, and delivery (§5.14–5.15, §§7–14, §18):** Persisted asynchronous jobs carry tenant/requester context and authorize status/result/cancellation; cancellation must not expose partial completed results. Real transactional email is required for password recovery/change confirmation and enumerated notices. Test, evaluation, monitoring, CI, deployment, documentation, and Definition-of-Done obligations are stated.

### Constraints and decision distinctions

- **Human decisions:** Only RA18-Q-01 and RA18-Q-02 are newly incorporated in v1.9. Their exact answers are bound in the Requirement Update attempt; they are not approvals.
- **Derived observations:** The New → Open role list and single-team assignment rule are consistent with default deny and current team scopes. A primary-team change must revoke Agent access outside the new valid scope; disposition of existing ticket assignments is not specified (RA19-A01 below).
- **Recommendations, not requirements:** Keep the listed initial targets/defaults configurable, and decide provider/schema/API/implementation details in the applicable later stage. No recommendation in this analysis changes the source.

## 3. Scope

### In Scope

The mandatory first demonstrable release in §4.1: local identity/recovery; tenants, users, roles/RBAC and privileged-change approval; support teams; configurable administration; approval-gated knowledge lifecycle/RAG; full tenant/team ticket operations and correction/cancellation workflows; Customer Search/Read, scoped Feedback Read and email visibility; AI ticket intelligence and internal-role copilot; allowlisted read-only tools and analytics; persisted jobs and user cancellation; audit/monitoring; evaluation/testing; CI, documentation and Azure deployment. Customer Search, Feedback Read, email visibility, ticket correction/cancellation, listed email events, and user-initiated job cancellation are expressly mandatory and must not be deferred.

### Out of Scope

§4.2 defers enterprise SSO/Entra, MFA/passwordless, internal notes, external ticketing/CRM/messaging integrations, arbitrary SQL/text-to-SQL, autonomous multi-agent/customer communications, AI write tools, custom roles/tenant permission overrides, SLA indicators, billing, multi-region DR, compliance certifications, large-scale benchmarking, custom fine-tuning, automated model selection, and automated privileged-change approval.

### Deferred / Undecided

§17 leaves model deployments and region, model-specific token limits and monthly cost budget, email provider/sender/deployment configuration, and bounded per-operation background timeout/retry settings open. The document's proposed retention/evaluation values are not legal commitments or release gates as stated. Exact schemas, indexes, API contracts, implementation order, task breakdown, capacity, and milestones are later design/planning matters; illustrative §8–9 entities/routes are not final contracts.

## 4. Ambiguities

| ID | Requirement reference | Ambiguity | Impact / status |
|---|---|---|---|
| RA18-A01 / RA18-Q-01 | §§5.10, 5.13 | Whether Agent may be assigned outside their primary team, and exception authority. | **Resolved by human decision and v1.9:** no cross-team assignment/exception; Agent eligibility, Tenant Admin routing, validation, audit, and access revocation are stated. |
| RA18-A02 / RA18-Q-02 | §5.10 | Which roles may transition New → Open and under what scope. | **Resolved by human decision and v1.9:** Agent, assigned-team Manager, and own-tenant Tenant Admin scopes are explicit; creator-only and routine Platform Admin authority are excluded; revalidation/default deny/audit are stated. |
| RA18-A03 / RA18-Q-03 | §5.9, Customer permission mapping | Platform Admin has no routine Customer Search/unrestricted lookup, while “separately authorized investigations” are contemplated without defining whether that capability is in release or its authorization/scope. | **Important, unresolved:** could create exceptional access to customer data; requires a scope and authorization decision or explicit exclusion. |
| RA18-A04 / RA18-Q-04 | §5.11–5.12 | Post-deletion audit metadata is “minimum necessary”; listed examples “may include” fields rather than a closed allowlist. | **Important, unresolved:** affects privacy, deletion, and audit acceptance; decide exact retained fields and any pseudonymization before finalizing. |
| RA18-A05 | §5.9 FR-ID-16; §8 | Feedback's optional `reason` and illustrative entity `Comment` may or may not be the same persisted/API field. | **Minor, unresolved:** may cause inconsistent contract or unnecessary data capture. |
| RA18-A06 | §5.3 FR-TK-04; §8 | Urgency is an AI suggestion, but illustrative `TicketAIResult` fields omit urgency; entity definitions are non-final. | **Minor / traceability concern, unresolved:** persistence/representation is not specified. |
| RA19-A01 | §5.13 FR-TEAM-03, §5.10 assignment rule | On Agent primary-team change, access outside the new scope is revoked, but the requirement does not specify whether existing tickets assigned to that Agent in the former team must be reassigned, unassigned, remain assigned but inaccessible, or be handled through a separate review. “If any ticket assignments change” requires validation/audit but does not define whether/how they change. | **Important; decision needed for a coherent team-change workflow:** avoid stale/ineligible ticket ownership or silently inventing an automatic reassignment policy. |

## 5. Conflicts

No direct contradictory statements were identified in the complete v1.9 review. The two incorporated answers align with the default-deny role matrix, single-primary-team Agent rule, tenant-wide Tenant Admin triage, assigned-team Manager scope, and ticket audit requirements. The Platform Admin “separately authorized investigation” clause and post-deletion “minimum necessary” audit language are underspecified, not direct contradictions. RA19-A01 is an omission, not a proven conflict; do not assume automatic reassignment.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance | Impact |
|---|---|---|---|
| RA18-Q-03 | Whether separately authorized Platform Admin Customer investigations exist in first release; if yes, the approving authority, purpose/scope, data visibility, duration, and audit controls. | Important | Affects exceptional sensitive-data access and default-deny boundaries. |
| RA18-Q-04 | Exact allowlist and handling (including pseudonymization) of security/admin audit fields retained after tenant deletion. | Important | Needed for privacy, deletion, and audit acceptance. |
| RA18-Q-05 | Whether `reason` and `Comment` are one field and whether/how AI urgency suggestions are persisted. | Minor to important | Affects API/data/test traceability; fields/entities are illustrative. |
| RA19-A01 | Ticket-assignment disposition when an Agent's primary team changes and prior assignments fall outside the new team. | Important | Affects membership workflow, assignment validity, access, and tests; no automatic policy inferred. |
| §17-OQ-01 | Exact generation/embedding model deployments and region, after availability, search compatibility, quota, price and support validation. | Important, intentionally deferred | Needed before provider/environment configuration; not an unresolved product behavior if kept explicitly deferred. |
| §17-OQ-02 | Model-specific token limits and monthly monetary cost budget. | Important, deferred | Needed for safe/cost-bounded model configuration. |
| §17-OQ-03 | Transactional email provider, sender identity and deployment configuration. | Important, deferred | Needed before enabling real email; only candidate providers are named. |
| §17-OQ-04 | Bounded timeout and retry settings per background operation/provider. | Important, deferred | Needed for reliable job behavior; must remain independent of general API timeout. |
| RA18-M06 | Final schemas/indexes/foreign keys, API payload/error/status contracts and implementation/task sequencing. | Non-blocking at analysis | Source labels these as design/planning matters; decide later without changing business rules. |

## 7. Assumptions

| ID | Assumption | Impact | Confirmation required |
|---|---|---|---|
| RA19-AS01 | CloudDesk, seed data and evaluation scenarios are fictional/synthetic as specified. | Supports privacy and demo-data boundaries. | No; source-explicit. |
| RA19-AS02 | Azure AI/Search resources and selected model/region will be available subject to quota, pricing and compatibility validation. | May affect provider choice and deployment. | Yes before configuration/deployment; remain open under §17. |
| RA19-AS03 | Proposed retention values/defaults remain configurable proposals, not legal/regulatory commitments; proposed evaluation targets remain non-gating after approval unless a separate explicit decision changes them. | Prevents converting proposals into commitments. | No new decision inferred. |
| RA19-AS04 | The current conversation's process initiation and prior record statements provide process context only; they do not decide product behavior or approve v1.9. | Preserves authority boundary. | No product decision inferred. |
| RA19-AS05 | Whether old Agent ticket assignments are automatically changed on a primary-team transfer is not assumed. | Assignment/access behavior remains open as RA19-A01. | Yes before finalizing that workflow. |

## 8. Technical Impact (not additional requirements)

- **API/service:** Central server-side default-deny permission checks; revalidate tenant/team/assignment/status for every transition and direct-ID operation; explicit correction/cancellation/approval workflows; protected Customer/Feedback access and email unmask operation; persisted job status/result/cancel authorization.
- **Application/domain:** Ticket state machine, team membership and assignment lifecycle, current-authorization loss, knowledge-version approval, retention eligibility and deletion states, audit scopes, and human-vs-AI authority boundaries.
- **Infrastructure/data:** Version-specific knowledge storage/index invalidation; tenant-scoped SQL/Blob/Search; durable job records and cancellation/race handling; retention cleanup and deletion replay after backup restore; restricted audit residue; real email provider and managed secrets. Exact schema/API is not fixed by illustrative entities/routes.
- **Frontend:** Role-scoped tenant/team/ticket/Customer/Feedback workflows; masked email by default; visible AI suggestions, citations, abstentions, job state and safe failures; explicit approval and audit views.
- **Integrations:** Azure AI model/embedding and Search compatibility, Azure SQL/Blob/App Service/Key Vault/Application Insights, GitHub Actions, and a real transactional email service; exact model/region/email settings remain deferred.
- **Testing/quality:** Role, tenant, team and assignment denial; New → Open role/state cases; team-change assignment disposition; exact-version approval and stale index exclusion; Customer/Feedback/email visibility; tenant deletion and retained audit fields; async cancellation and partial-result races; email recovery; evaluation measures and CI/deployment checks.
- **Security/privacy:** Backend enforcement across API, tools, retrieval, asynchronous jobs and stored results; no cross-tenant/team access; controlled privileged changes; least privilege; no unnecessary personal/secret content in prompts/logs; auditable unmask and deletion.
- **Performance/operations:** Configurable upload/rate/concurrency/token/timeout limits, persisted long-running jobs, safe provider failure handling, approximate cost monitoring and bounded retries. Numeric token/cost and per-operation timeout/retry choices remain open.

These are requirement-derived impacts and technical considerations, not observations about implemented code. No implementation or runtime was inspected.

## 9. Questions Requiring Human Decision

RA18-Q-01 and RA18-Q-02 are answered and incorporated; do not ask them again. The following remain open:

1. **RA18-Q-03:** Is separately authorized Platform Admin investigation of Customer data in first-release scope? If yes, who authorizes it, for what purpose/scope/duration, which fields are visible, and what audit/controls apply? If not, should the clause be explicitly excluded? This matters because routine Customer access is denied and exceptional access must not silently broaden it.
2. **RA18-Q-04:** What exact security/administrative audit fields may remain after permanent tenant deletion, and which must be pseudonymized? A closed set is needed to test deletion while preserving only approved accountability metadata.
3. **RA18-Q-05a:** Does Feedback `reason` correspond to the illustrative `Comment` field, or are they distinct? Which field is accepted, returned, retained, and audited?
4. **RA18-Q-05b:** Should an AI urgency suggestion be persisted with ticket AI results, and if so in what form and lifecycle? Do not treat the illustrative entity omission as a decision.
5. **RA19-A01:** When an Agent changes primary team, what should happen to existing tickets assigned to them in the former team: remain assigned but inaccessible, be unassigned, be reassigned by an authorized user, or follow another explicit workflow? Should the team change be blocked until affected assignments are dispositioned? No automatic reassignment is inferred.
6. **§17 configuration decisions (before corresponding configuration/release):** select generation and embedding model deployments/region; set model-specific token limits and monthly cost budget; choose transactional email provider/sender/deployment; and define bounded per-operation timeout/retry settings after provider validation. These are deliberately deferred, not approved by this analysis.

## 10. Analysis Conclusion

- **Analysis outcome:** Complete static reassessment of the full v1.9 requirement. RA18-Q-01 and RA18-Q-02 are resolved by the recorded human answers and reflected in v1.9. RA18-Q-03/Q-04/Q-05, §17 configuration decisions, and the residual primary-team-change assignment question remain unresolved; none has been silently decided.
- **Requirement finalization / approval readiness:** **No.** Important access/deletion/workflow decisions remain, v1.9 is explicitly unapproved, and this analysis is not approval.
- **Requirement Analysis Verification readiness:** **Not unqualified yet.** The post-update analysis exists, but remaining material decisions and the documented invocation-ordering caveat should be assessed under the existing governance before claiming a clean verification handoff. This report does not perform that assessment or start Verification. If the responsible governance process determines the caveat does not block, an independently initiated Requirement Analysis Verification may review the complete package while preserving the open questions; unresolved questions still must be settled before Human Requirement Approval as required.
- **Next permitted action:** Resolve the verification-readiness/order caveat and material decisions through existing governed processes; any further requirement change requires its separate authorized Requirement Update, followed by refresh analysis and independent verification. Each process requires its own initiation approval.
- **Boundary:** No source requirement, previous process record, implementation plan, source code, tests, configuration or other product artifact was modified. No Requirement Analysis Verification, planning, implementation, corrective process, approval, acceptance, build/test, commit or push was performed.

## Limitations and evidence classification

Static source/process-record inspection only. No application source, tests, CI/workflows, deployment/IaC, provider availability, runtime behavior, privacy/legal suitability, or operational controls were independently validated. Prior Requirement Update and Requirement Analysis reports are process records; they do not establish product implementation. Source pre-read timing statements are reported from those records, not inferred beyond their wording. The current attempt's prepublication inspection and checkpoint correction are disclosed above and in the linked execution records.