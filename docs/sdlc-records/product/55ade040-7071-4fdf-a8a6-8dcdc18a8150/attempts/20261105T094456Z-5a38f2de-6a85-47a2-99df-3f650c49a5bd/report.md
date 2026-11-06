# Requirement Analysis

## Source and execution identity

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261105T094456Z-5a38f2de-6a85-47a2-99df-3f650c49a5bd`
- **Authoritative source:** `docs/requirement/SupportIQ_Product_Requirement_v1.3.md`
- **Source version:** SupportIQ Product Requirement v1.3; 95,458 bytes; SHA-256 `AC40CB29AF795253B5C1C11AA200757C04CE460650FDC5799E69B9276491C496`
- **Source status:** Draft Updated Requirement; unapproved.
- **Analysis approach:** Fresh analysis of v1.3. Prior v1.2 analysis findings were not used as evidence. The v1.3 update evidence was used only to trace the human decisions embodied in the source.
- **Predecessor:** Material-change Portability Assessment completed with `COMPATIBILITY WITH IDENTIFIED ADAPTATION`; no portability blocker was recommended.
- **Boundaries:** Read-only analysis. No source Requirement, implementation, tests, configuration, or plan was modified. No build, test, or runtime action was performed.

## 1. Understanding

SupportIQ is a learning-oriented, demonstrable B2B customer-support portal for fictional CloudDesk. The first release is intended to help authenticated internal support roles use approved knowledge, manage tenant/team-scoped tickets, and use bounded AI assistance. It does not claim production readiness.

**Actors:** Platform Admin; Tenant Admin; Support Manager; Support Agent. Based on the Human decision recorded during this analysis, the first-release AI Customer Assistant is for those four internal roles only; external CloudDesk customers are not assistant users.

**Main functionality:** local account administration and recovery; tenant/team RBAC; version-approved knowledge and RAG; ticket lifecycle and AI assistance; read-only typed AI tools and predefined analytics; persisted background jobs with cancellation; a restricted transactional-email allowlist; audit, evaluation, quality, and Azure deployment controls.

## 2. Explicit Requirements

### Functional requirements and business rules

- Tenant, user, team, permission-matrix, and operational administration use four predefined roles, centralized default-deny backend authorization, tenant/team/resource scope, and independent second-admin approval for privileged Platform Admin changes (Sections 3, 5.9, 5.13; FR-ID-01 through FR-ID-15; FR-TEAM-01 through FR-TEAM-06).
- Knowledge ingestion/reprocessing creates versioned state; only the exact current processed version approved by a Tenant Admin is retrievable. Failed, stale, pending, rejected, or deleted content is unavailable to RAG/search (Section 5.2; FR-KB-01 through FR-KB-12).
- AI assistance is grounded, cites sources, abstains on insufficient evidence, validates structured output, treats retrieved content as untrusted, and does not autonomously send messages or mutate business data (Sections 5.1-5.8, 11).
- Ticket actions are tenant/team/role/resource scoped. Agents directly edit only Subject and Description on authorized tickets; Category/Priority actions use distinct permissions, with Agent correction requests and authorized Manager/Tenant Admin decisions. Cancellation uses a persisted Agent request and authorized approval, with pending ticket state unchanged and cancellation terminal (Section 5.10; FR-TM-01 through FR-TM-14).
- Long-running work is persisted, returns HTTP 202 and a Job ID, revalidates status/result authorization, and supports authorized idempotent queued or cooperative processing cancellation without exposing partial results or overwriting committed completion (Section 5.14; FR-OP-09).
- Transactional email is restricted to the specified identity and ticket/knowledge/account/privileged-change events and recipients, with authorization, privacy, deduplication, bounded retries, and truthful delivery status (Section 5.15).
- Security, audit, retention, test, evaluation, deployment, and acceptance criteria are defined across Sections 5.8, 5.11-5.12, 10-16, and 18. Evaluation percentages are non-gating; mandatory authorization failures remain acceptance failures.

### Constraints

The first release uses React/TypeScript, .NET 8/ASP.NET Core Identity, Azure model endpoints, Azure AI Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, and GitHub Actions. Entra ID/SSO, external ticketing/CRM/messaging integrations, arbitrary text-to-SQL, autonomous multi-agent workflows, AI write tools, and automatic customer communications are out of scope. Use synthetic data only.

## 3. Scope

### In Scope

The mandatory first demonstrable release in Section 4.1: tenant/user/team administration; default-deny permissions; approved knowledge/RAG; ticket lifecycle and new request workflows; read-only tools/analytics; persisted cancellable jobs; allowlisted transactional email; audit, tests/evaluation, CI, documentation, and Azure deployment expectations.

### Out of Scope

Section 4.2 exclusions, including external ticketing/CRM/messaging integration, advanced natural-language analytics/text-to-SQL, enterprise SSO, internal notes, custom roles/tenant permission overrides, autonomous AI writes, and SLA indicators until definitions exist.

### Deferred / Undecided

The Requirement explicitly defers exact Azure AI model/deployment and region; model-specific token limits and monthly cost budget; selection of email provider/sender configuration; provider-bounded per-operation job timeouts/retries; and validation of proposed retention defaults for legal/business suitability before production. These are not new business decisions made by this analysis.

## 4. Ambiguities and Human Decisions

| ID | Requirement | Ambiguity and impact | Human decision received / disposition |
|---|---|---|---|
| RA-A-01 | Sections 3, 4.1, and 5.1: "AI Customer Assistant"; FR-CA-01 says "Users" can start a conversation. | The document's role list contains only internal roles but the feature title could imply external customer access. This affects authentication, tenant linkage, retrieval scope, privacy, and testing. | Human decided first release is **internal roles only** (the four listed roles); no external CloudDesk customer access. v1.3 must be updated to state this explicitly. |
| RA-A-02 | Sections 5.5-5.6 and FR-ID permission catalogue: analytics `ReadTenant`, `ReadTeam`, `ReadOwn`. | The document explicitly gives Managers assigned-team analytics but does not map Tenant Admin, Support Agent, and Platform Admin scopes consistently for both dashboard and AI-invoked analytics. This affects tenant isolation and tool authorization. | Human decided: Tenant Admin tenant-scoped; Support Manager assigned-team; Support Agent only own authorized-ticket data; Platform Admin aggregate-only without tenant business records. v1.3 must be updated with this role mapping. |
| RA-A-03 | FR-ID-11 through FR-ID-14 and Section 5.15. | The text says password reset does not reactivate a deactivated account but leaves reset eligibility and required confirmation-email behavior while inactive unclear. This affects account recovery and email eligibility. | Human decided a deactivated account **cannot reset its password until reactivated**. v1.3 must be updated to state eligibility; the existing generic reset response remains applicable. |

These Human decisions were supplied in the current conversation and are authoritative for the analysis context. They are not yet incorporated into v1.3 and do not authorize a Requirement Update.

## 5. Conflicts

No unresolved contradiction was identified in the reviewed source after applying the supplied human decisions. An apparent tension between FR-TK-06 (Agents may edit/override AI suggestions) and FR-TM-13/14 (Agent direct ticket edits are restricted) is resolved by the explicit existing human decision and v1.3's specific field/action rules: editing a suggestion does not directly mutate Category/Priority; those changes use the separate correction-request workflow. Preserve this distinction in the Requirement Update and tests.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance | Impact / handling |
|---|---|---|---|
| RA-M-01 | The three new decisions above are not yet stated in v1.3. | Blocking before verification | Run a separately authorized Requirement Update to create a new immutable version; then refresh Requirement Analysis before independent verification. |
| RA-M-02 | Exact Azure AI generation/embedding deployment, region, quotas, model compatibility, and token/cost budgets. | Important; explicitly deferred | Confirm before provider-dependent implementation and cost commitments; do not invent values. |
| RA-M-03 | Email provider, sender identity/domain, and environment allowlists. | Important; explicitly deferred to implementation | Decide and verify before real email is enabled; maintain safe failure and secret controls. |
| RA-M-04 | Per-operation background timeout/retry values and observed latency bounds. | Important; explicitly deferred | Choose during implementation against provider constraints; keep distinct from the 30-second API timeout and avoid duplicate effects. |
| RA-M-05 | Legal/business validation of proposed retention and deletion defaults. | Important before production | Validate before production use; the Requirement labels these proposed, configurable defaults, not legal commitments. |

## 7. Assumptions

| ID | Assumption | Impact | Confirmation required |
|---|---|---|---|
| RA-AS-01 | CloudDesk and all example customer/ticket data are fictional/synthetic. | Data, fixtures, prompts, logs, and screenshots must not contain real customer records or secrets. | Already explicit in Sections 12 and 17; preserve. |
| RA-AS-02 | Azure AI model/search resources will be available in a suitable region. | Model, search, quota, cost, and regional support remain unverified. | Confirm before model/provider-dependent implementation; already called out as an open assumption. |

No new implementation or business assumptions were introduced by this analysis.

## 8. Technical Impact

- **API:** Expose only internal-role assistant routes; enforce clarified analytics role scopes and account-status eligibility; retain typed contracts and authorization for cancellation/correction requests and jobs.
- **Application/service layer:** Keep AI output distinct from authoritative ticket data; route Agent Category/Priority proposals through correction requests; keep disabled accounts out of reset eligibility until reactivation.
- **Domain:** Apply explicit user-role, analytics scope, ticket transition, request/approval, job-state, and email-event rules.
- **Infrastructure/data:** Persist ticket requests, jobs, audit, and email delivery status; use the approved tenant-scoped storage/search boundaries. No new infrastructure is mandated by this analysis.
- **Frontend:** Limit assistant entry points to the four internal roles; reflect tenant/team/own analytics scope and recovery eligibility; keep request/approval UI separate from direct ticket edits.
- **Integration:** Exact Azure model/region and email provider/sender remain deferred. Validate approved knowledge version and provider failure semantics at integration boundaries.
- **Testing:** Add negative authorization tests for each analytics scope and internal-only assistant access; test deactivated-account reset denial, ticket request state/concurrency, job cancellation races/idempotency, and notification recipient rules.
- **Security/privacy:** Enforce default-deny backend authorization, tenant/team/own scope, no customer access in the assistant, no reset for inactive accounts, data minimization, and safe email/error behavior.
- **Performance/scalability:** Preserve bounded synchronous calls and persisted async jobs; finalize operation-specific timeouts/retries after provider constraints are known.

These are traceability impacts, not additional approved requirements or an implementation plan.

## 9. Questions Requiring Human Decision

The three questions discovered in this analysis were asked interactively and answered:

1. Who may use the first-release AI Customer Assistant? **Answered:** the four internal roles only; no external customers.
2. Which roles may use analytics? **Answered:** Tenant Admin tenant scope; Manager assigned-team; Agent own authorized-ticket scope; Platform Admin aggregate-only, without tenant business records.
3. May deactivated users reset passwords? **Answered:** no; they must be reactivated first.

**Pending human decisions:** None from these questions. The remaining items in Section 6 are explicitly deferred technical/production decisions already identified by the Requirement.

## 10. Analysis Conclusion

- **Outcome:** Analysis complete with human clarifications; Requirement Update required.
- **Ready for Requirement Analysis Verification:** **No.** The three answers must first be incorporated in a new immutable Requirement version, followed by a fresh post-update analysis/refresh. Independent Requirement Analysis Verification remains a separate process.
- **Blocking decisions:** None pending; the answers were received. The resulting Requirement Update is a required next process, not authorized by these answers.
- **Next step:** Obtain separate Human Process Initiation Approval and record-scope authorization for Requirement Update. Do not modify v1.3 in this analysis.
- **Requirement Approval / implementation:** Not performed or authorized.
