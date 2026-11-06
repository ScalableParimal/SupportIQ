# Requirement Analysis

## Source and execution identity

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261105T102333Z-8133e154-e109-40eb-a787-e0d3e3100741`
- **Authoritative source:** `docs/requirement/SupportIQ_Product_Requirement_v1.4.md`
- **Source version:** SupportIQ Product Requirement v1.4; 98,684 bytes; SHA-256 `332EEE3EC6C2D2A145EEF6C26BC567D9FD73B95DD118FB86C63DCB848ABFBF5F`
- **Source status:** Draft Updated Requirement; unapproved.
- **Analysis approach:** Fresh analysis against v1.4 only. Prior v1.3 analysis findings were not used as evidence; assertions below were checked against v1.4. The two clarifications below are authoritative human decisions for this analysis, but are not yet in the source requirement.
- **Boundaries:** Read-only with respect to the requirement and product artifacts. No implementation plan, source code, tests, configuration, or other process was modified or run. No build, test, or runtime action was performed.

## 1. Understanding

SupportIQ is a fictional B2B support portal for CloudDesk, intended as a demonstrable learning release rather than a production-readiness commitment. It helps internal support staff find approved knowledge, manage synthetic tenant/team-scoped tickets, and use bounded AI assistance while retaining human control over customer-facing decisions and business changes.

**Actors:** Platform Admin, Tenant Admin, Support Manager, and Support Agent. The AI Customer Assistant is internal-only; external CloudDesk customers are excluded.

**Main functionality:** local identity and tenant/team administration; default-deny role/resource/action authorization; approved, versioned knowledge and RAG; ticket lifecycle and AI assistance; read-only allowlisted tools and role-scoped analytics; persisted cancellable background jobs; allowlisted transactional email; audit, evaluation, operational limits, retention/deletion, CI, and Azure deployment.

## 2. Explicit Requirements

### Functional requirements and business rules

- Four predefined roles use centralized, default-deny, backend-enforced resource/action permissions with tenant/team/resource scope. Privileged Platform Admin changes require an independent second Platform Admin; self-approval and self-elevation are prohibited (Sections 3, 5.9, 5.13; FR-ID-01 through FR-ID-15; FR-TEAM-01 through FR-TEAM-06).
- The assistant is for the four internal roles only. Retrieval uses only current document versions approved by a Tenant Admin in the user's authorized tenant scope; responses cite sources, abstain when evidence is insufficient, use at most the latest 10 turns as context, and do not cross access boundaries (Section 5.1; FR-CA-01 through FR-CA-08).
- Knowledge upload, processing, approval, reprocessing, and deletion are versioned. Only the exact current processed version approved by a Tenant Admin is searchable/retrievable; failed, pending, rejected, stale, or deleted content is unavailable (Section 5.2; FR-KB-01 through FR-KB-12).
- AI ticket and copilot outputs are structured, validated, provisional, and human-reviewed. Read-only AI tools are explicitly allowlisted; arbitrary SQL, shell, unrestricted network requests, AI write tools, and automatic customer messages are prohibited (Sections 5.3-5.5 and 11).
- Analytics are predefined and read-only. Tenant Admin scope is tenant; Support Manager scope is assigned teams; Support Agent scope is own authorized-ticket data; Platform Admin scope is aggregate-only for one explicitly selected authorized tenant, with no cross-tenant view or underlying business-record access (FR-AN-01 through FR-AN-06).
- Ticket lifecycle, assignment, field edits, Category/Priority corrections, escalation, cancellation, and closure/reopen transitions have role-, team-, tenant-, and state-specific rules. Agents cannot assign/reassign or directly change Category/Priority; pending requests do not change authoritative ticket values (Section 5.10; FR-TM-01 through FR-TM-14).
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

The source explicitly defers exact Azure AI model/deployment/region, model-specific token limits and monthly cost budget, email provider/sender/deployment configuration, and bounded per-operation background timeout/retry settings. Retention defaults are configurable proposals, not legal or regulatory commitments; legal/business validation is required before production.

## 4. Ambiguities

| ID | Requirement | Ambiguity and impact | Human decision received / disposition |
|---|---|---|---|
| RA-A-01 | FR-CA-07; Section 9 History API; permission catalogue in Section 5.9 | "History permitted by role" did not say whose history each role may read; the permission catalogue did not map conversation history. This affects privacy and backend authorization. | **Owner-only.** Each user may view their own conversation history; other roles may not read it. This decision is not yet incorporated into v1.4 and requires Requirement Update. |
| RA-A-02 | FR-CA-01/02; FR-ID-09; Sections 5.5 and 5.9 | Platform Admin is listed as an assistant user, but the assistant requires authorized tenant-scoped retrieval and Platform Admin has no routine tenant business-content access. No retrieval scope was stated. | **No tenant-content retrieval** for Platform Admin. This decision resolves the retrieval scope for analysis but is not yet incorporated into v1.4; update the requirement before verification. |

## 5. Conflicts

No unresolved contradiction was identified in the reviewed source after applying the two clarifications. The apparent tension between FR-TK-06 (Agents can edit/override AI suggestions) and FR-TM-13/14 (Agents cannot directly change Category/Priority) is resolved by the specific correction-request workflow: a suggestion can be proposed, but the authoritative value changes only after the authorized decision workflow. The assistant audience and role-specific analytics rules are stated consistently in the corresponding requirements and acceptance criteria.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance | Impact / handling |
|---|---|---|---|
| RA-M-01 | The two access-scope decisions received during this analysis are not stated in v1.4. | Blocking before verification | Start a separately authorized Requirement Update to create a new immutable version; then refresh Requirement Analysis before independent verification. |
| RA-M-02 | Exact Azure AI generation/embedding deployment, region, model compatibility, quotas, model token limits, and monthly cost budget. | Important; explicitly deferred | Validate after model/subscription selection and before provider-dependent implementation or cost commitment; do not invent values. |
| RA-M-03 | Email provider, sender identity, and deployment/environment configuration. | Important; explicitly deferred | Decide and verify before real email is enabled; retain secret, sender-domain, allowlist, and safe-failure controls. |
| RA-M-04 | Per-operation background timeout/retry values and observed latency bounds. | Important; explicitly deferred | Set against provider constraints and observed latency; keep independent from the 30-second general API and proposed 60-second model defaults. |
| RA-M-05 | Legal/business suitability of proposed retention and deletion defaults. | Important before production | Validate before production use; the source marks these as configurable proposals, not legal commitments. |
| RA-M-06 | Feedback read/review access is not defined; the API contract specifies submission only and the permission catalogue has no feedback-read mapping. | Minor; non-blocking under default-deny | Do not add a feedback-reading surface without a separate requirement and authorization decision. No additional human decision is required for the currently specified submission behavior. |

## 7. Assumptions

| ID | Assumption | Impact | Confirmation required |
|---|---|---|---|
| RA-AS-01 | Azure AI model and search resources will be available in a suitable region. | Model availability, compatibility, quota, and cost are unverified. | Confirm before provider-dependent implementation; this is already identified as an assumption/open question in Section 17. |
| RA-AS-02 | CloudDesk and all example organizations, users, tickets, and knowledge data are fictional/synthetic. | Fixtures, prompts, logs, and screenshots must not include real customer records or secrets. | Explicitly required by Sections 12 and 17; preserve. |

No additional business or implementation assumptions were introduced. The two human access decisions are not treated as source requirements until separately updated.

## 8. Technical Impact

- **API:** Enforce conversation-owner reads and deny Platform Admin tenant-content retrieval on every backend/tool path; preserve tenant/team authorization and default-deny behavior. The exact permission mapping should be stated in the updated requirement before implementation planning.
- **Application/service layer:** Keep AI suggestions separate from authoritative ticket data; retain correction/cancellation workflows and account-status eligibility. Platform Admin assistant requests must not retrieve tenant business content.
- **Domain/data:** Conversation records include tenant and user identity; enforce owner-only history and 90-day proposed conversation retention. Feedback submission is specified, but feedback reads are not.
- **Infrastructure:** Persisted jobs, approval-aware search, tenant-scoped storage, configurable cleanup, and audit are required. No new infrastructure is mandated by this analysis.
- **Frontend:** Preserve internal-only assistant access; apply owner-only history behavior. Do not expose tenant knowledge to Platform Admin through assistant retrieval.
- **Integration:** Exact Azure AI deployment/region and email provider/sender remain deferred. Validate provider limits and safe failure behavior at integration boundaries.
- **Testing:** Add negative authorization tests for another user's conversation history and Platform Admin tenant-content retrieval, alongside tenant/team/RBAC, stale-version, job-cancellation, notification, and feedback-read-denial cases.
- **Security/privacy:** Apply default-deny authorization, tenant/team/resource scope, least privilege, minimized Platform Admin access, approved-version retrieval, and sensitive-data minimization.
- **Performance:** Keep long-running work asynchronous; source defaults include 30-second general API and proposed 60-second AI model timeouts, while per-operation job timeouts/retries remain deferred.

These impacts are analysis traceability, not an implementation plan or additional approved requirements.

## 9. Questions Requiring Human Decision

The two material access questions raised during this analysis were answered:

1. **Conversation history visibility (FR-CA-07):** `owner_only` — each user may view only their own conversation history.
2. **Platform Admin assistant retrieval:** `no_tenant_content` — Platform Admin must not retrieve tenant business content through the assistant.

**Pending human decisions:** None from the questions raised in this analysis. The provider, quota/cost, timeout/retry, and production-retention items remain explicitly deferred in the source.

## 10. Analysis Conclusion

- **Outcome:** Analysis complete with human clarifications; Requirement Update required.
- **Ready for Requirement finalization / Requirement Analysis Verification:** **No.** Both answers must first be incorporated in a new immutable Requirement version, followed by a fresh post-update analysis. Independent Requirement Analysis Verification is a separate process.
- **Blocking decisions:** No human answers remain pending. The blocking next action is the separately authorized Requirement Update; the answers do not authorize that process.
- **Next step:** Obtain separate Human Process Initiation Approval and exact record-scope authorization for Requirement Update. Update from v1.4 only with the two recorded decisions, then perform a fresh analysis/refresh before independent Requirement Analysis Verification.
- **Requirement approval / implementation:** Not performed or authorized. v1.4 remains a draft and unapproved.