# Requirement Analysis

**Outcome:** `ANALYSIS_COMPLETE; HUMAN_DECISIONS_REQUIRED; REQUIREMENT_UPDATE_OR_REFRESH_REQUIRED`  
**Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`  
**Attempt ID:** `20261105T160827Z-6b0c9a3f-db79-4181-925a-5cceefcf6f25`  
**Authoritative source:** `docs/requirement/SupportIQ_Product_Requirement_v1.7.md` (v1.7; 101,677 bytes; SHA-256 `E38812289F69CD4338217EDDC6439B76F8749DE68F054C6707D089324A4093A9`)  
**Status in source:** Draft Updated Requirement; unapproved.  
**Predecessor:** Portability Assessment attempt `20261105T142403Z-138c401d-bdfa-4688-81e2-3c8d464c959b`; persisted result/report/evidence reconciled. Outcome `COMPATIBILITY WITH IDENTIFIED ADAPTATION`; no possible blocker recommended. It is applicable to the current source/state (same repository, branch, HEAD, v1.7 source hash, and matching adopted Master fingerprints). Its adaptation expressly preserves the unresolved retention event for a Customer with no related tickets.  
**Authorization:** Fresh user-supplied authorization for exactly one new Requirement Analysis attempt, recorded in this attempt's `attempt.json` as invocation-authorization metadata, not as a formal Human Gate. Invocation was published no-overwrite and read back with integrity validation before the Requirement was opened.  
**Analysis basis:** The complete v1.7 Requirement was reviewed read-only against the current Requirement Analysis Guideline, Prompt, Request, Skill, Agent, applicable governance, and relevant persisted predecessor/decision records. No implementation artifacts were inspected or changed.

## 1. Understanding

SupportIQ is a fictional CloudDesk B2B SaaS support portal and a learning-oriented, demonstrable first release, not a production-readiness commitment. Four internal roles (Platform Admin, Tenant Admin, Support Manager, Support Agent) administer tenants/teams and handle synthetic tickets; they use approved knowledge, bounded AI assistance, scoped analytics, persistent asynchronous jobs, and controlled email. The stated stack is React/TypeScript, .NET 8 / ASP.NET Core Identity, Azure AI/Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, and GitHub Actions (Requirement §§1, 3, 7).

The central constraints are server-side default-deny access, tenant/team/resource/action/owner scoping, human control of customer-facing or business-data changes, exact-version knowledge approval, auditable workflows, and retention/deletion controls. The 30-day schedule is a target, not a guarantee (§§2, 4, 16).

## 2. Explicit Requirements and Human Decisions

### Explicit requirements

- Four predefined roles use centralized, versioned, default-deny resource/action permissions; backend/data access enforces tenant, team, ticket, owner, and role scope. Privileged Platform Admin changes require an independent second Platform Admin; self-approval/elevation is denied (§§3, 5.9; FR-ID-01–15).
- Internal-role assistant responses use approved, authorized knowledge, cite sources, abstain when evidence is insufficient, and never send messages automatically. AI tools are allowlisted, typed, read-only, scoped, rate/time bounded, and audited (§§5.1–5.5, 11, 13).
- Tenant Admins, assigned-team Managers, and Agents have distinct ticket/customer access. Customer Read/Search is explicitly in the permission catalogue; Platform Admin assistant access is limited to aggregate analytics for one selected authorized tenant, with no underlying records/documents (§§5.5, 5.6 FR-AN-06, 5.9).
- Ticket statuses, permitted transitions, assignment, escalation, Category/Priority correction requests, cancellation requests, approval, history, and retention are specified; cancellation is terminal and distinct from closure (§5.10; §6.5, §6.10–11).
- Long-running work uses persisted authorized jobs and cooperative cancellation. Retention, tenant lifecycle, audit, approved transactional email events, security, evaluation, and test coverage are defined (§§5.11–15, 13–14).
- Proposed evaluation percentages and several operational values are expressly non-gating/proposed; retention defaults are configurable and are not legal/regulatory commitments (§§5.7, 5.11, 17).

### Previously supplied human decisions incorporated

The v1.7 Update evidence binds these clarifications to earlier Requirement Analysis decision records: **RA16-Q-01** permits only FR-AN-06 aggregate analytics for exactly one selected tenant through the Platform Admin assistant, with no underlying records or documents; **RA16-Q-02** adds Customer Read/Search with the stated role scopes and separately restricted Platform Admin; **RA16-Q-03** defines inactivity as no active related tickets and starts the 365-day period at the last related ticket's terminal transition; its follow-up defines terminal as Closed or Cancelled. The current v1.7 Update report confirms these were applied and v1.7 remains unapproved. The separate v1.6 analysis observation that feedback submission/retention exists without feedback-read permission also remains relevant; no read capability is inferred.

These earlier decisions resolve the former assistant-boundary and missing Customer permission issues. They do **not** answer the currently preserved no-related-ticket retention question. No new human decision was made in this analysis.

## 3. Scope

### In Scope

The mandatory first demonstrable release in §4.1: local identity/recovery; four-role RBAC and tenant/team administration; configurable operations; version-approved knowledge/RAG; synthetic ticket lifecycle and tracked correction/cancellation requests; AI summaries/classification/copilot; read-only scoped tools and analytics; persisted cancellable jobs; listed transactional email; audit/monitoring; evaluation/testing; CI, documentation, and Azure deployment.

### Out of Scope

Section 4.2 exclusions include Entra ID/enterprise SSO, external ticketing/CRM/messaging integrations, billing, multi-region DR, compliance certification, custom fine-tuning/model selection, autonomous multi-agent/customer communications, internal notes, arbitrary custom roles/tenant permission overrides, AI-invoked write tools, and SLA indicators pending definitions.

### Deferred / Undecided

Exact model/deployment/region, token/cost budgets, email provider/sender, and per-operation job timeouts/retries are deferred in §17. The no-related-ticket Customer retention start event remains undecided. Customer feedback review access is not required by the explicit submission-only behavior and remains unprovided; it must stay denied unless separately specified.

## 4. Ambiguities

| ID | Requirement reference | Ambiguity and impact | Importance |
|---|---|---|---|
| RA17-A-01 | §5.11 Customer retention; §13 acceptance criteria; §17 | For a Customer with no related tickets, no ticket can become terminal and the 365-day clock has no defined start event. Different choices (e.g. record creation or a separately recorded inactivity event) change when destructive cleanup occurs. Do not infer a date or behavior. | **Blocking for the no-related-ticket retention path.** |
| RA17-A-02 | §5.5 Customer lookup contract; §5.9 Customer permission mapping | Agent access covers customers related to tickets assigned to them “or otherwise explicitly permitted,” but the additional qualifying relationship, granting authority, and lifecycle/revocation rule are not identified. This affects Customer Read/Search and tool authorization; broad access would conflict with the stated no-tenant-wide-browse boundary. | **Important; resolve before finalizing this access path.** |
| RA17-A-03 | §5.5; §5.10 unassigned-ticket rules; §5.13 | “Separate authorization” for Managers to access globally unassigned tickets and “authorized central-triage function” are not mapped to an existing role or an explicit permission/grant. The requirement otherwise defines four roles and excludes custom roles. This affects visibility and routing of unassigned tickets. | **Important; clarify actor and exact scope.** |
| RA17-A-04 | §5.11 user retention and tenant deletion | Deactivated user records are retained for 365 days, while tenant deletion purges eligible business/derived data after a 30-day grace period. The text does not state whether tenant deletion overrides that user-record period or what attribution must remain. | **Important for deletion/retention implementation.** |
| RA17-A-05 | §5.5 Customer Search; §9 API/integration | Role scopes and fields are bounded, but matching semantics, searchable fields, filters, ordering, and pagination for Customer Search are not specified. This may yield materially different search behavior. | **Minor / clarify before final search acceptance.** |

## 5. Conflicts

No definite internal contradiction was established in v1.7. The earlier Platform Admin assistant ambiguity and missing Customer Read/Search mapping are resolved by the recorded decisions and current text. The four-role/custom-role boundary versus “central triage” is an unresolved scope mapping (RA17-A-03), not enough evidence to declare a direct contradiction. The retention overlap in RA17-A-04 likewise needs precedence clarification rather than an assumed conflict resolution.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance / impact |
|---|---|---|
| RA17-M-01 | Customer-with-no-tickets retention start event (§5.11). | Blocking for safely applying automated Customer cleanup to this case; captured as RA17-A-01. |
| RA17-M-02 | Explicit authorization mapping for Agent “otherwise permitted” customer/ticket relationships and central triage (§§5.5, 5.9, 5.10, 5.13). | Important security/functional acceptance boundary; unspecified access remains denied under default-deny. |
| RA17-M-03 | Precedence between tenant deletion and 365-day deactivated-user retention (§5.11). | Important for purge eligibility, attribution, and testable retention behavior. |
| RA17-M-04 | Feedback read/review permission is absent although submission, storage, and retention are specified (FR-CA-06; §§5.9, 8, 13). | Minor; no feedback-reading feature should be inferred. Add a read scope only if intended. |
| RA17-M-05 | Whether “masked by default” customer email is always masked in the first release or whether a role-controlled unmask path is intended (§5.5). | Minor privacy detail; no unmask capability should be added absent explicit scope. |

## 7. Assumptions

| ID | Assumption / explicit basis | Impact / confirmation |
|---|---|---|
| RA17-AS-01 | All example organizations, users, tickets, documents, and evaluation data are fictional/synthetic (§§1, 12). | Use synthetic data only; source explicitly requires it, so no additional confirmation is needed for this analysis. |
| RA17-AS-02 | Retention values are proposed, configurable defaults and not legal/regulatory commitments (§§5.11, 17). | Business/legal suitability must be confirmed before production use; this is expressly stated, not elevated to an approved policy. |
| RA17-AS-03 | No access beyond an explicit role/resource mapping is authorized. | Derived from default-deny requirements (§§3, 5.9, FR-OP-10); in particular, unresolved Agent/central-triage access is not granted by this report. |

No unresolved business decision was inferred. The implementation state, security enforcement, model availability, cost, and operational behavior have not been independently evaluated.

## 8. Technical Impact

- **API / authorization:** Customer Read/Search and tool endpoints need server-side field and row scoping, direct-ID enumeration protection, and distinct PA/tenant/team/Agent rules. Central-triage and Agent exceptions need an explicit permission mapping before enablement. Ticket transition/correction/cancellation and two-person privileged approval require enforceable state and actor checks.
- **Application / domain:** Customer-to-ticket associations, role-visible search, tenant/team membership changes, ticket terminal/reopen behavior, and cleanup eligibility must remain consistent. The no-ticket Customer state and tenant-deletion/user-retention precedence require decisions before cleanup behavior is finalized.
- **Data / persistence:** Logical entities are illustrative, not a schema (§8). Preserve versioned permissions, ticket/audit history, job state, email delivery metadata, and exact knowledge approvals. The source leaves indexes, foreign keys, tenant-aware uniqueness, and implementation details for later design.
- **Infrastructure / integrations:** Stated Azure AI/Search, SQL, Blob, worker, Key Vault, telemetry, and real transactional-email components are constraints/recommendations in the source; exact model/provider/quota/cost and job retry/timeout values remain deferred. No service availability or deployment feasibility was verified.
- **Frontend:** Role-scoped dashboards, customer search, approval and ticket workflows, safe errors, job status/cancellation, audit/configuration views, and accessibility requirements are indicated; exact Customer Search interaction behavior remains incomplete.
- **Testing / security:** Cover default-deny role/resource boundaries, Customer Read/Search scopes and field minimization, direct-ID/cross-tenant/team denial, Platform Admin aggregate-only access, approval independence, ticket state races, job cancellation races, retention clocks and tenant deletion precedence, email account-enumeration safety, and audit/redaction behavior.
- **Performance / operations:** Apply the configurable rate/concurrency/upload/context limits and separate API/model/job timeouts; evaluate the explicit non-gating AI measures without treating them as proof of correctness. Verify costs, quotas, and production retention suitability separately.

These are requirement impacts, not implementation instructions or proof that the current product meets them. No source code, tests, configuration, CI, deployment, runtime, or external services were inspected or executed.

## 9. Questions Requiring Human Decision

1. **RA17-Q-01 — Customer with no related tickets:** What exact event starts the configurable 365-day Customer-record retention period when the Customer has no related tickets? Please specify the event and any reset behavior. This analysis does not select a date or cleanup rule.
2. **RA17-Q-02 — Agent Customer access:** What precise ticket/customer relationship qualifies as “otherwise explicitly permitted” for Support Agent Customer Read/Search, who grants that authorization, and when is it revoked? If none is intended, confirm assigned-ticket-only access.
3. **RA17-Q-03 — Central triage / globally unassigned tickets:** Is central triage a capability assigned to one of the four existing roles (which role and actions), or an additional separately governed permission? Who may read/route globally unassigned tickets, and under what scope? Do not infer a fifth role or override the no-custom-role constraint.
4. **RA17-Q-04 — Tenant deletion versus user retention:** Does approved tenant deletion after its grace period supersede the 365-day retention for deactivated user records in that tenant? Specify minimum attribution/audit data to preserve if records are purged earlier.

Customer search matching/pagination, feedback review access, and any unmasking of email are lower-priority completeness items. Unless expressly decided otherwise, do not add feedback-reading or email-unmask functionality, and keep search within the stated allowlisted fields and role scopes.

## 10. Analysis Conclusion

- **Analysis outcome:** `ANALYSIS_COMPLETE; HUMAN_DECISIONS_REQUIRED; REQUIREMENT_UPDATE_OR_REFRESH_REQUIRED`.
- **Ready for requirement finalization:** No.
- **Blocking decision:** RA17-Q-01 for Customer cleanup when there are no related tickets. RA17-Q-02 and RA17-Q-03 are important access-boundary decisions; RA17-Q-04 is important for deletion/retention precedence.
- **Human decisions incorporated:** RA16-Q-01, RA16-Q-02, RA16-Q-03 and its terminal-ticket follow-up, as bound by the v1.7 Requirement Update report/evidence and prior decision records. They remain source decisions, not approvals of v1.7.
- **Ready for Requirement Analysis Verification:** **No.** Under the Guideline's sequence, required material decisions must be supplied, any resulting Requirement change must pass through the separate Requirement Update process, and the post-update analysis/refresh must precede independent Requirement Analysis Verification.
- **Exact next governed stage:** No subsequent process is started or authorized by this analysis. First obtain human decisions for the questions above. If the decisions require changing v1.7, the next governed process is a separately initiated **Requirement Update**; after that, perform a fresh Requirement Analysis/refresh, then **Requirement Analysis Verification**. Requirement approval remains a later, separate human gate.
- **Approval/acceptance:** No Requirement approval, verification, implementation authorization, or acceptance is claimed.
- **Read/write boundary:** The source Requirement and prior records remain unchanged. No Requirement Update, Verification, Planning, implementation, tests, builds, or commit/push was performed. The earlier attempt `20261105T155753Z-7019f0b0-f274-4f3f-8c33-89eab08d9621` was preserved and not reused.

### Evidence references

- Invocation record: `docs/sdlc-records/product/55ade040-7071-4fdf-a8a6-8dcdc18a8150/attempts/20261105T160827Z-6b0c9a3f-db79-4181-925a-5cceefcf6f25/attempt.json` (SHA-256 `DDDF5392610A5D36A9CAB0F4F40ACBA13FEC4D5DBED1EC562FBAB51212545D64`).
- Analysis evidence: same attempt directory, `evidence/analysis-evidence.json`.
- Predecessor portability report/result/evidence: attempt `20261105T142403Z-138c401d-bdfa-4688-81e2-3c8d464c959b`.
- Human decision records: attempt `20261105T123811Z-df38a98b-d93e-4dfd-b23a-10173308e9da`, `evidence/human-decisions-001.json` and `human-decisions-002.json`.
- v1.7 Requirement Update report/result/evidence: attempt `20261105T130233Z-6191abc6-81d3-4805-8448-bb7d8157ef1e`.
