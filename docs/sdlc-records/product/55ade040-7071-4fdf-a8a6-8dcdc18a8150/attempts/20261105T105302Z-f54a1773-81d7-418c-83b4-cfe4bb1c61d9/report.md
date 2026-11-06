# Requirement Analysis

**Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`  
**Attempt ID:** `20261105T105302Z-f54a1773-81d7-418c-83b4-cfe4bb1c61d9`  
**Authoritative source:** `docs/requirement/SupportIQ_Product_Requirement_v1.5.md`  
**Source version:** SupportIQ Product Requirement v1.5; 99,261 bytes; SHA-256 `FD2DCCF97D6B6A9D3F8E72F58AA162409163C4557BFF9D90F6F9FB7A8C7AEE82`  
**Source status:** Draft Updated Requirement; unapproved.  
**Analysis approach:** Fresh review of v1.5. The previous v1.4 analysis was not reused as analysis evidence. The two attributable human decisions were considered as approved context.

## 1. Understanding

SupportIQ is a fictional B2B SaaS support portal for CloudDesk and a 30-day demonstrable learning release, not a production-readiness commitment. It helps internal support staff find Tenant Admin-approved knowledge, manage synthetic tenant/team-scoped tickets, and use bounded AI assistance while retaining human control of customer-facing decisions and business changes.

**Actors:** Platform Admin, Tenant Admin, Support Manager, and Support Agent. External CloudDesk customers are excluded from the assistant.

**Main functionality:** local identity and tenant/team administration; default-deny role/resource/action authorization; approved, versioned knowledge and RAG; ticket lifecycle and AI assistance; read-only allowlisted tools and role-scoped analytics; persisted cancellable background jobs; allowlisted transactional email; audit, evaluation, operational limits, retention/deletion, CI, and Azure deployment.

## 2. Explicit Requirements

### Functional requirements and business rules

- Four predefined roles use centralized, default-deny, backend-enforced resource/action permissions with tenant/team/resource scope. Privileged Platform Admin changes require approval by an independent second Platform Admin; self-approval and self-elevation are prohibited (Sections 3, 5.9, 5.13; FR-ID-01 through FR-ID-15; FR-TEAM-01 through FR-TEAM-06).
- The assistant is for the four internal roles only. Tenant Admin, Support Manager, and Support Agent retrieval uses current document versions approved by a Tenant Admin in the user's authorized scope. Platform Admin assistant retrieval must not access tenant business content. Responses cite retrieved sources, abstain when evidence is insufficient, and may use at most the most recent 10 turns without crossing access boundaries (Section 5.1; FR-CA-01 through FR-CA-08).
- Each user may read only their own conversation history, regardless of role. The permission catalogue includes `Conversations (ReadOwnHistory)` with owner scope; the illustrative history API contract is addressed in Ambiguity RA15-A-01.
- Knowledge upload, processing, approval, reprocessing, and deletion are versioned. Only the exact current processed version approved by a Tenant Admin is searchable/retrievable; failed, pending, rejected, stale, or deleted content is unavailable (Section 5.2; FR-KB-01 through FR-KB-12).
- AI ticket and copilot outputs are structured, validated, provisional, and human-reviewed. Read-only AI tools are allowlisted; arbitrary SQL, shell, unrestricted network requests, AI write tools, and automatic customer messages are prohibited (Sections 5.3-5.5 and 11).
- Analytics are predefined and read-only. Tenant Admin scope is tenant; Support Manager scope is assigned teams; Support Agent scope is own authorized-ticket data; Platform Admin scope is aggregate-only for one explicitly selected authorized tenant, with no cross-tenant view or underlying business-record access (FR-AN-01 through FR-AN-06).
- Ticket lifecycle, assignment, field edits, Category/Priority corrections, escalation, cancellation, and closure/reopen transitions have role-, team-, tenant-, and state-specific rules. Pending requests do not change authoritative ticket values (Section 5.10; FR-TM-01 through FR-TM-14).
- Long-running AI/RAG/ticket/knowledge operations persist tenant/requester-scoped jobs, return HTTP 202 and a Job ID, revalidate status/result authorization, and support authorized cancellation with safe handling of races and partial results (Section 5.14; FR-OP-09).
- Transactional email is restricted to the listed account, ticket, knowledge, and privileged-change events/recipients, with safe failure, bounded retries, privacy, deduplication, and audit (Section 5.15).
- Security, audit, retention, synthetic data, test, evaluation, deployment, and acceptance controls are defined across Sections 5.8, 5.11-5.12, and 10-18. Evaluation percentages are non-gating; authorization failures remain acceptance failures.

### Constraints

The stated baseline is React/TypeScript, .NET 8 / ASP.NET Core Identity, Azure AI model endpoints, Azure AI Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, and GitHub Actions. The release is demonstrable and learning-oriented. External ticketing/CRM/messaging integrations, enterprise SSO, arbitrary custom roles or tenant overrides, autonomous business-data writes, internal notes, advanced text-to-SQL, and undefined SLA indicators are deferred or out of scope.

## 3. Scope

### In Scope

The mandatory first-release scope in Section 4.1: local identity/recovery; four-role RBAC; tenant/team administration; operational configuration; version-approved knowledge/RAG; synthetic ticket lifecycle and tracked request workflows; ticket AI and copilot; read-only tools/analytics; persisted cancellable jobs; restricted transactional email; audit/monitoring; evaluation/testing; CI, documentation, and Azure deployment.

### Out of Scope

Section 4.2 exclusions, including external ticketing/CRM/messaging integrations, billing, multi-region disaster recovery, compliance certifications, large-scale benchmarking, custom fine-tuning, automated model selection, Entra ID/SSO, MFA/passwordless recovery, internal notes, AI-invoked write tools, custom roles/tenant permission overrides, SLA indicators before definitions exist, and automated approval of privileged Platform Admin changes.

### Deferred / Undecided

Section 17 explicitly defers exact Azure AI model/deployment/region, model-specific token limits and monthly cost budget, email provider/sender/deployment configuration, and bounded per-operation background timeout/retry settings. Retention defaults are configurable proposals, not legal or regulatory commitments; legal/business validation is required before production.

## 4. Ambiguities

| ID | Requirement | Ambiguity | Impact |
|---|---|---|---|
| RA15-A-01 | FR-CA-07; Section 5.9 `Conversations (ReadOwnHistory)`; Section 9 History API (`GET /api/conversations/{id}`) | FR-CA-07 and the permission catalogue specify owner-only history, regardless of role, but the API note says only “Enforce ownership/role and tenant access.” It does not state that role/tenant permissions can never broaden access beyond the conversation owner, or clarify whether they may further restrict an owner's access. | The API authorization contract could be interpreted differently from the explicit owner-only decision. This affects privacy and backend authorization. The existing decision RA-A-01 resolves the intended scope; update the API wording to preserve that scope before verification. |

## 5. Conflicts

No direct contradiction was identified between the assistant audience and retrieval restriction: FR-CA-01 permits internal roles to start conversations, FR-CA-02 restricts Platform Admin tenant-business retrieval, and FR-CA-04 requires abstention when evidence is insufficient. The unresolved wording about history authorization is recorded as ambiguity RA15-A-01 rather than treated as a confirmed policy conflict.

## 6. Missing / Incomplete Information

| ID | Missing Information | Importance | Impact |
|---|---|---|---|
| RA15-M-01 | The illustrative History API contract does not explicitly state owner-only enforcement and non-overridable ownership; see RA15-A-01. | Blocking before verification | Propagate the existing owner-only decision to the Section 9 API contract through a separately authorized Requirement Update, then refresh analysis. |
| RA15-M-02 | Feedback submission is specified, but feedback-read/review access and its permission mapping are not. | Minor; non-blocking under default-deny | Do not add a feedback-reading surface without a separate requirement and authorization decision. |
| RA15-M-03 | Exact Azure AI generation/embedding deployment, region, quotas, model token limits, and monthly cost budget. | Important; explicitly deferred | Validate after model/subscription selection and before provider-dependent implementation or cost commitment; do not invent values. |
| RA15-M-04 | Email provider, sender identity, and deployment/environment configuration. | Important; explicitly deferred | Decide and verify before real email is enabled; retain secret, sender-domain, allowlist, and safe-failure controls. |
| RA15-M-05 | Per-operation background timeout/retry values and observed latency bounds. | Important; explicitly deferred | Set against provider constraints and observed latency; keep independent from the general API and proposed model timeout defaults. |
| RA15-M-06 | Legal/business suitability of proposed retention and deletion defaults. | Important before production | Validate before production use; the source marks these as configurable proposals, not legal commitments. |

## 7. Assumptions

| ID | Assumption | Impact | Confirmation Required |
|---|---|---|---|
| RA15-AS-01 | Azure AI model and Search resources will be available in a suitable region. | Model availability, compatibility, quota, and cost are unverified. | Confirm before provider-dependent implementation; this is already identified in Section 17. |
| RA15-AS-02 | Proposed retention and deletion defaults will be suitable for the learning release. | Defaults are configurable proposals and may not meet legal/business requirements. | Validate before production use as Section 17 requires. |
| RA15-AS-03 | CloudDesk and example organizations, users, tickets, and knowledge data are fictional/synthetic. | Fixtures, prompts, logs, and screenshots must not include real customer records or secrets. | Preserve the explicit synthetic-data constraint in Sections 12 and 17. |

No new business or implementation assumption was introduced. The two human access decisions are present in v1.5 and are treated as decisions, not AI assumptions or Human Requirement Approval.

## 8. Technical Impact

- **API:** The conversation-history endpoint must enforce the authenticated conversation owner's access; role or tenant permissions must not grant access to another user's history. Clarify any additional checks without weakening owner scope.
- **Application/service layer:** Apply the owner check on every history read, including direct-ID requests. Platform Admin assistant retrieval must not access tenant business content; preserve the no-answer path when authorized evidence is unavailable.
- **Domain/data:** Conversation and message records identify a user and tenant. Enforce owner-only reads and tenant boundaries consistently with the user identity and role/resource permission catalogue.
- **Infrastructure:** Continue approval-aware search, tenant-scoped storage, persisted jobs, configurable cleanup, and audit. No additional infrastructure is mandated by this analysis.
- **Frontend:** Expose only the authenticated user's own conversation history; do not rely on UI filtering as the authorization boundary.
- **Testing/security:** Add or retain direct API authorization cases for owner, non-owner same-role, non-owner privileged-role, and cross-tenant history access. Test that Platform Admin assistant retrieval cannot return tenant business content.
- **Performance/operations:** Preserve bounded synchronous APIs, persisted long-running jobs, configurable model/job timeouts, rate limits, and safe provider failure handling.

## 9. Questions Requiring Human Decision

No new business decision is required to resolve RA15-A-01: the existing human decision RA-A-01 specifies owner-only history. The requirement/API contract needs a consistency update through the separate Requirement Update process. The model, provider, cost, timeout/retry, and production-retention decisions remain explicitly deferred in Section 17 and are not silently resolved here.

## 10. Analysis Conclusion

- **Requirement analysis outcome:** `ANALYSIS_COMPLETE; REQUIREMENT_UPDATE_REQUIRED`.
- **Human decisions incorporated:** RA-A-01 (owner-only conversation history) and RA-A-02 (no Platform Admin tenant-business retrieval), both preserved in v1.5.
- **Blocking decisions:** None newly required. A requirement consistency update is required for the Section 9 History API wording identified as RA15-A-01.
- **Ready for Requirement Analysis Verification:** No. First perform a separately initiated Requirement Update to align the History API contract with the existing owner-only decision, then perform a fresh Requirement Analysis against the resulting version. Complete independent verification and resolve any findings before separate Human Requirement Approval.

This analysis does not approve or verify v1.5, authorize planning or implementation, or start a downstream process.
