# Requirement Analysis

- **Attempt:** `20261105T073747Z-e68be8ab-2c65-4a76-a8a9-57fb75b90425`
- **Authoritative input:** `docs/requirement/SupportIQ_Product_Requirement_v1.2.md`
- **Source identity:** `SupportIQ Product Requirement v1.2@sha256:D206C95AD75E0D7E1B1169144B29ADE219F3C42299FE5C3ED3C20F75DD8D99AA` (77,893 bytes; unapproved Draft Updated Requirement)
- **Analysis evidence:** `evidence/analysis-evidence.json`
- **Analysis outcome:** Clarifications resolved; Requirement Update is required before verification.

This is a fresh analysis of v1.2. Prior Requirement Analysis results were not consulted or reused. The user's responses in this analysis are recorded as human decisions for a separate Requirement Update; they have not changed v1.2 and do not constitute Human Requirement Approval. Analysis was read-only; no code, tests, configuration, implementation plan, or source Requirement was changed.

## 1. Understanding

SupportIQ is an internal, multi-tenant support workspace for managing tickets and approved knowledge, with constrained AI-assisted retrieval, summaries, classification, reply drafts, and predefined analytics. The system also provides role-scoped administration, persisted background work, auditable ticket workflows, and transactional email. AI capabilities must not bypass backend authorization or directly mutate authoritative business data or send customer-facing communications.

Actors include Customers (as ticket subjects/records), Support Agents, Support Managers, Tenant Admins, Platform Admins, application services and workers, the AI/model provider, and an email provider. The first release uses synthetic ticket/customer data and does not connect external customer or ticketing systems.

## 2. Explicit Requirements

### Source Requirement

- Knowledge content is versioned, reviewed/approved, tenant-authorized, indexed, and retrievable with source references. Ticket operations are scoped by tenant, team, role, and assignment; undefined transitions and unauthorized actions are denied. History and audit records are retained.
- The AI tool boundary is read-only and explicitly allowlisted; FR-WF-03/04 prohibit arbitrary SQL, shell, unrestricted network requests, and AI-invoked write tools. FR-AN-03 defines a small set of predefined natural-language analytics functions. The five-item list under “First-Release Tool Allowlist” omits analytics despite FR-WF-01 naming it. “Advanced natural-language analytics” and arbitrary text-to-SQL remain out of scope; the approved clarification includes only the predefined analytics in §5.5/FR-AN-03.
- Ticket lifecycle, statuses, categories, priorities, transitions, cancellation eligibility, actor boundaries, escalation, retention, and audit requirements are defined in §5.10. FR-TM-07 leaves Agent “work permitted fields” unspecified. FR-TM-09 says an Agent may request cancellation but does not define the persisted request/decision lifecycle.
- §5.14 defines persisted asynchronous jobs and lists `Cancelled` as a state, but does not define an operation, authority, timing, or cancellation/result race behavior.
- §5.15 defines secure provider integration and password recovery plus “other approved transactional notifications,” without enumerating those events. Provider choice is explicitly an implementation-time decision among the permitted options.

### Human Decisions Supplied for Requirement Update

1. **Analytics:** Include the predefined, read-only, tenant-scoped analytics functions in the first-release AI-invoked allowlist. No advanced natural-language analytics or text-to-SQL is authorized.
2. **Agent ticket edits:** Agents may edit Subject and Description on tickets they are authorized to access. They cannot assign/reassign tickets or edit system-managed fields; status follows §5.10. Unspecified fields/actions are denied. Category/Priority are not generic edits.
3. **Category/Priority actions:** Tenant Admins may change these values for tickets in their tenant; Managers may do so only for tickets in assigned teams, including team-queued/unassigned-to-Agent tickets. Agents cannot directly change them; Platform Admins have no routine tenant-ticket modification permission. Changes are allowed only in New, Open, In Progress, or Pending Customer; values must use the defined taxonomy and priority set; changes retain before/after values and actor/tenant/ticket/time/correlation audit history.
4. **Agent Category/Priority correction requests:** Add a separate persisted workflow with Pending Approval, Approved, and Rejected states. Store tenant/ticket, field, current/proposed values, mandatory reason, requester/time, decision/approver/time/reason. Agents submit for accessible tickets; Managers decide for assigned teams; Tenant Admins decide in-tenant; Agents cannot decide. The original value remains while pending; apply only on approval after authorization and state revalidation; reject duplicate pending requests for the same ticket/field; disallow changes for Resolved, Closed, or Cancelled tickets; audit and handle concurrent changes safely. Include request/review UI, APIs, persistence, history, and automated tests.
5. **Job cancellation:** Include user-initiated cancellation in the first release. Tenant Admins may cancel tenant jobs; Managers may cancel jobs associated with their assigned teams subject to resource authorization; Agents may cancel jobs they initiated while still authorized for the associated resource; Platform Admins have no routine unrestricted tenant-job cancellation. Queued jobs cancel immediately; Processing jobs stop cooperatively at a safe checkpoint and must not persist/expose partial results; already committed completion remains Completed. Completed, Failed, Timed Out, or Cancelled jobs cannot be cancelled. Enforce backend reauthorization, idempotency, concurrency safety, audit/correlation, clear UI/error behavior, and unit, integration, API, security, and end-to-end tests.
6. **Ticket cancellation requests:** Add a separate persisted Agent request and Manager/Tenant Admin approval workflow with Pending Approval, Approved, and Rejected states. Record ticket/requester, allowed cancellation reason, mandatory notes, timestamps, and decision details. Agents may request only for accessible tickets and cannot finalize; Tenant Admins decide tenant-wide and Managers decide for their teams, including team-assigned tickets without an Agent. Keep ticket state/assignment unchanged while pending; approval cancels only from New, Open, In Progress, or Pending Customer; rejection leaves the ticket unchanged and records a reason. Prevent duplicate active pending requests and audit/authorize the full workflow. Include UI, APIs, persistence, and automated tests.
7. **Transactional email:** In addition to password recovery and successful password-change confirmation, include exactly these approved first-release events: ticket cancellation request submitted (assigned active team Manager, else authorized Tenant Admin); cancellation approved/rejected (requesting Agent, rejection reason where appropriate); ticket assigned/reassigned (new Agent); ticket escalated (receiving team Manager); ticket reopened (current Agent); knowledge version approved/rejected (uploader, rejection reason where appropriate); account activated/deactivated (affected registered user, including the specified deactivation security-notice exception); Platform Admin privileged permission change pending approval (independent authorized second Platform Admin); and that change approved/rejected (initiating Platform Admin). Resolve recipients from current authorization data, send only to eligible registered users, avoid duplicate recipients, minimize sensitive content, use configurable safe templates, bounded transient retries, and auditable safe delivery metadata. Provider submission is not guaranteed inbox delivery and must not be reported as such. No emails for every status/job update or chat message; no AI-generated customer-facing messages.
8. **Cross-cutting controls:** Default-deny authorization; revalidate tenant/team/role/resource/action permissions on relevant APIs and worker operations. Audit cancellations, edits/decisions, analytics access, admin actions, and email outcomes. Cancellation and request workflows are idempotent and safe under concurrent transitions. Preserve v1.2 security, privacy, retention, operational, and testing requirements. No arbitrary SQL, unrestricted AI write tools, external customer/ticketing integration, or unapproved notification events. No functional deferrals were requested for these approved additions.

These are human decisions, not statements already present in v1.2. A new immutable Requirement version is necessary to make them traceable in the source of truth.

## 3. Scope

### In Scope

The v1.2 first-release scope plus the human decisions above, once incorporated through Requirement Update: internal ticket and knowledge workflows; constrained read-only AI; predefined analytics; explicit Agent field permissions; tracked Category/Priority correction requests; separate job and ticket cancellation workflows; and the enumerated transactional email events.

### Out of Scope

External customer/ticketing integrations, arbitrary text-to-SQL, unrestricted AI write tools, automatic AI business-data mutation or customer communication, unapproved email events, and the advanced analytics/SLA items explicitly deferred by v1.2.

### Deferred / Undecided

No additional product-functionality deferrals were requested in the human decisions. The Requirement Update itself is not yet authorized; therefore these decisions are not incorporated into a new source version. Email provider selection remains explicitly delegated to implementation-time evaluation as stated in v1.2.

## 4. Ambiguities

| ID | Requirement | Ambiguity | Impact / disposition |
|---|---|---|---|
| RA-G-01 | FR-TM-07: Agent may “work permitted fields” | Agent editable-field allowlist was absent. | Resolved: Subject/Description only; other fields default-deny; status and Category/Priority use separate rules. |
| RA-G-02 | §5.14 job state includes `Cancelled` | No cancellation command, actor, timing, terminal-state behavior, or race rules. | Resolved: first-release job cancellation behavior and role scopes are specified in the human decision. |
| RA-G-03 | FR-TM-09 Agent may request ticket cancellation | Request persistence, decision states, authority, and pending/decision behavior were absent. | Resolved: separate persisted Agent request/approval workflow with three states and defined roles/eligibility. |
| RA-G-04 | §5.15 “other approved transactional notifications” | Events and recipients beyond password recovery were unspecified. | Resolved: explicit event/recipient allowlist; additional events require explicit approval. |
| RA-G-05 | Category/Priority corrections | Agent could not directly change these, but the permitted action/request handling was unclear. | Resolved: Tenant Admin/Manager direct actions under defined scope; Agents use a separately persisted approval workflow. |

## 5. Conflicts

| ID | Statements | Conflict | Impact / disposition |
|---|---|---|---|
| RA-C-01 | §5.5 FR-WF-01 allows analytics functions; §5.5 “First-Release Tool Allowlist” says the only tools are five named tools and omits analytics; FR-AN-03 requires predefined natural-language analytics. | The complete allowlist disagrees on whether analytics is available as an AI-invoked first-release tool. This is distinct from the explicit deferral of advanced analytics/text-to-SQL. | Resolved by human decision: include only the predefined read-only analytics functions from §5.5/FR-AN-03; update the enumerated list for consistency. |
| RA-C-02 | Initial human clarification described Managers as cancelling jobs they initiated; a later field described jobs associated with assigned teams. | Two different Manager scopes were proposed. | Resolved by explicit follow-up: Managers may cancel jobs associated with their assigned teams, subject to resource authorization. |

## 6. Missing / Incomplete Information

| ID | Missing Information | Importance | Impact / disposition |
|---|---|---|---|
| RA-M-01 | Exact Agent ticket-edit fields and handling of protected fields/actions. | Blocking | Resolved by the explicit Subject/Description allowlist, separate Category/Priority workflow, §5.10 status rules, no assignment, and default-deny. |
| RA-M-02 | Job-cancellation API/worker behavior, authorization, race/result semantics, and tests. | Blocking | Resolved by the detailed first-release cancellation decision; the implementation plan must map each constraint to tests. |
| RA-M-03 | Ticket cancellation request/approval state and audit behavior. | Blocking | Resolved by the detailed persisted request workflow and role/eligibility rules. |
| RA-M-04 | Category/Priority correction request handling and authorization. | Blocking | Resolved by the detailed separate request workflow and direct-action permissions. |
| RA-M-05 | Approved transactional email event list, recipients, privacy, retries, and failure semantics. | Important | Resolved by the event-specific human decision and cross-cutting delivery controls. |

No unresolved product decision was identified after the user's clarifications. The requirement still needs an authorized version update before verification.

## 7. Assumptions

No unresolved business assumption is used to settle the questions above. The default-deny rule is applied as expressly directed. The predefined analytics boundary comes from §5.5/FR-AN-03; it does not authorize advanced analytics or text-to-SQL. Provider selection remains an explicit implementation-time choice, not an assumption made by this analysis.

## 8. Technical Impact

- **API / authorization:** Add separately authorized Category/Priority change and request/decision operations; job cancellation; ticket cancellation request/decision; and narrowly scoped notifications. Revalidate tenant, team, role, assignment/resource access, ticket/job state, and field/action permissions server-side on every relevant request.
- **Application / domain:** Keep Category/Priority requests distinct from ticket edits, and ticket cancellation distinct from background-job cancellation. Define guarded, auditable state transitions; preserve original values while requests are pending; prevent duplicate pending requests; ensure idempotent decisions and safe concurrent updates.
- **Persistence / audit:** Persist request records independently with requester, requested/current values or cancellation reason/notes, decision, actor, timestamps, tenant/resource identifiers, and correlation IDs. Preserve history and avoid exposing partial job results as completed results.
- **Workers / integrations:** Cooperative cancellation checkpoints must stop subsequent work and result persistence unless completion already committed. Analytics remain predefined/read-only. Email dispatch needs recipient revalidation, duplicate prevention, safe templates, bounded eligible retries, and truthful submission/failure status.
- **Frontend:** Add request and authorized review surfaces for both correction and ticket-cancellation workflows, plus job cancellation/status feedback and safe errors. Do not expose unauthorized actions.
- **Security / privacy:** Enforce tenant/team isolation and default-deny at API and worker boundaries; prevent unauthorized state transitions and data disclosure; minimize sensitive email content; never convert AI output into an automatic write or customer message.
- **Testing:** The human decisions explicitly require unit, integration, API, security, and end-to-end tests for new workflows. Cover authorization matrices, tenant/team boundaries, duplicate/idempotent requests, concurrent state changes, job cancellation checkpoints/races, no partial-result exposure, audit completeness, and email recipient/failure behavior. No tests or builds were run because this was a read-only Requirement Analysis.
- **Performance / operations:** Preserve the existing timeout, retry, retention, and operational limits. Cancellation checkpoints and bounded email retries must fit those controls; no new performance target was introduced.

## 9. Questions Requiring Human Decision

No unresolved product decisions remain from this analysis. A separate process-initiation authorization is still required before changing v1.2 through Requirement Update; the user's answers expressly require separate authorization for that change.

## 10. Analysis Conclusion

- **Requirement analysis outcome:** `ANALYSIS_COMPLETE_WITH_CLARIFICATIONS; REQUIREMENT_UPDATE_REQUIRED`.
- **Human decisions incorporated into this analysis:** Analytics tool scope; Agent ticket-edit allowlist; direct Category/Priority authority and correction-request workflow; job cancellation; ticket cancellation request/approval; transactional email events and delivery controls; default-deny/audit/testing constraints.
- **Unresolved blocking product decisions:** None.
- **Requirement ready for finalization:** No. Human decisions are not yet represented in an immutable Requirement version.
- **Ready for Requirement Analysis Verification:** No. First obtain explicit authorization for Requirement Update, create and validate a new version, then perform the required post-update Requirement Analysis/refresh before independent Requirement Analysis Verification.
- **Next permitted process:** Requirement Update, only after separate explicit human initiation/authorization. This analysis does not approve the Requirement, authorize implementation, or authorize a plan.