# Candidate Implementation Plan — SupportIQ Product Requirement v1.11

## 1. Status and Scope

- **Plan identity/version:** `supportiq-product-implementation-plan` / `0.2` (candidate; plan-local task IDs are stable within this identity/version).
- **Status:** **Draft Candidate — self-validation complete; independent Implementation Plan Verification not performed.** Not Ready for Human Review Approval, not Human Plan Approved, and not authorized for implementation.
- **Feature / Work ID:** SupportIQ Product Requirement v1.11 / `55ade040-7071-4fdf-a8a6-8dcdc18a8150`.
- **Planning attempt:** `20261111T080022Z-6bcfff1e-cee4-4d86-ac38-a9cec718008c`.
- **Amendment basis:** IPV-01 (Plan Verification attempt `20261107T133205Z-58d4f444-0acf-4ebf-b31b-d66dedca6e75`), Finding Investigation `20261111T052943Z-22085ae6-3b40-4731-b8c3-a4c14bdebc78`, Corrective Change Decision `20261111T072125Z-4ca95993-a4f2-4313-8c2c-06572696b017`, and Human Approval [issue comment 6790246131](https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6790246131) of the exact Option A amendment (SHA-256 `8FCC73D5DA66661180ECEDCAF7596687D584D80EC28C73E81A44A8A5C668E2C6`).
- **Source Requirement:** `docs/requirement/SupportIQ_Product_Requirement_v1.11.md`, 135,602 bytes, SHA-256 `56C9DC9CE23E73C7D23FB1EF52046C3DB007801F3589E7D7029C294D5F79ABBE`.
- **Approval:** Exact bytes approved by repository OWNER `ScalableParimal`; decision `6685628908`, record `docs/sdlc-records/product/55ade040-7071-4fdf-a8a6-8dcdc18a8150/human-gates/human-requirement-approval-v1.11/decisions/6685628908.json`; source permalink: <https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6685628908>.
- **Approval/document-control reconciliation:** The PRD's own control table and version lineage still say “Draft Updated Requirement; unapproved”. The exact hash-bound Human Requirement Approval record and its original OWNER response approve those exact bytes. That approval controls the source status for this plan; the stale text is recorded as a source-document inconsistency and is not edited here.
- **Historical verification:** Requirement Analysis Verification attempt `20261106T094118Z-b0606cb8-b2bf-4d1c-b6c1-3eed10deb74d` remains historically `ANALYSIS VERIFIED WITH GAPS`. RAV-01's decision-provenance limitation was resolved by the subsequent direct, verbatim approval evidence; this does not rewrite the historical result.
- **Approved v1.11 decision set carried into planning:** Critical/High/Medium/Low urgency remains separate from Ticket.Priority with no mapping; Support Agent/Support Manager/Tenant Admin scopes and Platform Admin denial are as stated in the approval; accept/override updates only ReviewedUrgency and review metadata, preserves SuggestedUrgency, and never changes Ticket.Priority. Priority changes use FR-TM-14.
- **In scope:** The complete approved v1.11 first demonstrable release in §4.1 and the 14 modules in §16: identity/access, tenant/team administration, operational settings and tenant lifecycle, knowledge/version approval, ticket lifecycle and requests, Customer/Feedback access, AI ticket intelligence/Copilot, internal-role Customer Assistant, allowlisted read-only tools/analytics, persisted cancellable jobs, audit/monitoring, evaluation/QA, CI/documentation and Azure deployment. The plan includes all applicable §5 functional requirements, §6 workflows, §§7–14 architecture/contracts/NFRs/tests, and §18 Definition of Done.
- **Out of scope:** Preserve §4.2 and explicit exclusions: external ticketing/CRM/messaging integrations; billing, multi-region DR and compliance certification; large-scale benchmarking, custom fine-tuning, automated model selection; Entra ID/enterprise SSO, MFA/passwordless and recovery beyond configured local Identity; internal notes; exceptional Platform Admin access to individual Customer records; AI-invoked write tools/autonomous business-data modifications; custom roles/tenant permission overrides; SLA indicators; and automated approval of privileged Platform Admin changes. No feature or scope is added by this plan.
- **Planning boundary:** This file is a candidate plan only. No product source, tests, configuration, schema, migrations, deployment, or runtime changes are made by this process. Implementation requires the full governed sequence and separate Human Plan Approval.

## 2. Repository and Architecture Context

### Observed repository state

- Canonical repository: `ScalableParimal/SupportIQ`; working copy `C:/PARIMAL_SHERE/SCALABLE_SOLUTIONS/SupportIQ`; branch `SupportIQ-Requirement-Analysis`; HEAD `d9dd1685bbdc6d8a4ce21d2b21ee0bae491d6ef0`.
- The working tree was clean before this attempt. After invocation publication, the only observed untracked paths are this attempt's own governed records; no product changes are present.
- Tracked top level consists of `README.md`, `.github/`, and `docs/`. The README is a product description only. The repository has governance/SDLC customization, requirements, and governed records, but **no product application source, solution/project/package manifests, product tests, or product CI/deployment files** were found. There is no existing application architecture, build/test command, framework/package choice, API pattern, migration convention, or frontend component convention to reuse.
- Accordingly, the following are **PRD-defined target layers**, not claims about existing projects or file paths: React + TypeScript frontend; .NET 8 ASP.NET Core Web API and local Identity; relational persistence in Azure SQL; Blob Storage; Azure AI Search; Azure AI model endpoint; persisted background worker/Azure Functions; transactional email; Key Vault/Application Insights; GitHub Actions. A future implementation must establish the concrete solution/project layout and test tools without assuming that any already exists.

### Architecture boundaries and contract handling

- The browser is presentation-only and receives no provider keys or unrestricted service credentials. The API owns validation, authentication/authorization, tenant/team/resource scope, orchestration, contracts, job submission and persistence.
- Domain/application rules remain independent from infrastructure-specific types. API/presentation must not own persistence, worker, Azure, provider, or secret-management concerns. Keep Azure/provider adapters behind the minimum interfaces required by the approved boundaries; do not add generic repositories, CQRS/MediatR, extra layers, caches, packages, or services without demonstrated need.
- §8 entities are illustrative logical entities, not a finalized schema. Define the necessary fields, foreign keys, tenant-aware uniqueness, indexes, retention and migrations during implementation from the approved rules; do not infer unspecified data or add speculative indexes.
- §9 routes and values marked illustrative are not fixed contracts. Final request/response schemas, validation, status/error behavior, idempotency where required, and OpenAPI documentation must preserve the approved behavior and be reconciled before consumers are built; ownership, deliverables and readiness checks for this reconciliation are assigned to IP-19A.

## 3. Decisions, Constraints, and Prerequisites

### Approved requirement and constraints

- The v1.11 source and approval binding above is authoritative for product behavior. The exact urgency clarifications in the approval record are explicit human decisions. Existing PRD technology statements (React/TypeScript, .NET 8/ASP.NET Core Identity, Azure services, GitHub Actions) are approved requirement content; Azure provider options stated as alternatives remain alternatives, not a selected provider.
- Apply default-deny authorization on every API, data, retrieval, tool, job, and result path. Revalidate current user, tenant, team, ticket, assignment and workflow-state relationships at each read/write/decision. Preserve separate workflow requests, audit/activity history and immutable source suggestions where required.
- Proposed configurable defaults in §5.11 (for example 30-second general API timeout, 60-second initial model timeout, rate/concurrency/upload/context limits and retention periods) are proposed operational defaults, not legal or non-configurable commitments. Implement their configurability and validation; do not silently make them fixed policy.
- §5.7 evaluation percentages are explicitly measurement targets, **not release gates**. Role/tenant/team authorization denial and the approved acceptance criteria remain mandatory.

### Deferred decisions — do not decide in this Plan

| ID | Open decision from approved Requirement §17 | Classification and implementation gate |
|---|---|---|
| D-01 | Exact Azure AI generation/embedding model deployments and region, including model/search compatibility, quota and availability. | **Blocking** for selecting deployments, embedding dimensions/index configuration, model-specific integration and deployment. Keep identifiers/configuration versioned and configurable until decided. |
| D-02 | Exact model-specific token limits and monthly monetary cost budget. | **Blocking** for enabling production/demo model calls and cost-limit configuration; decide only after D-01, pricing and subscription quota are checked. Do not invent numeric budgets. |
| D-03 | Email provider, sender identity/domain and deployment configuration (ACS Email or SendGrid are permitted alternatives). | **Blocking** for real email integration/enabling delivery. Do not select provider, sender or credentials in this Plan. |
| D-04 | Bounded per-operation background timeout/retry settings based on provider constraints and observed latency. | **Blocking** for final worker/provider configuration and retry behavior. Keep independent of the general API timeout; do not invent values. |

Additional implementation-time design points, not human decisions made here: the PRD permits a background worker or Azure Functions; hosting choice must be assessed against the approved deployment context before it is fixed. Exact schema/API/test project layout and the minimal test frameworks are not existing repository conventions and must be designed from the PRD once the solution scaffold exists. Keep these choices small, evidence-based and reviewable; elevate any material architecture/cost/security/scope choice for human decision.

## 4. Implementation Phases and Tasks

Task IDs are stable and Plan-local. References are qualified as `supportiq-product-implementation-plan@0.2/IP-xx`; they are execution tracking identifiers, not business requirements. Dependencies below are minimum logical prerequisites. All work remains subject to D-01–D-04 where specified and to the approved-plan and Orchestrator gates.

### Phase 0 — Establish a real implementation baseline

**IP-01 — Create the minimum solution, configuration, and quality baseline**  
**Target:** new React/TypeScript frontend and .NET 8 API solution areas; repository documentation and GitHub Actions. **Requirements:** PRD §§4.1, 7, 10, 15, 16, 18; FR-OP-08. **Prerequisites:** implementation is authorized against the current Human Plan Approved Plan; use only the approved stack. **Completion:** a new developer can follow documented local setup; frontend/API have reproducible build and test entry points; configuration separates local and Azure environments; no secrets are committed; PR CI builds and runs the established automated suite. Select no unnecessary packages/layers; record actual project layout and commands as implementation evidence.

**IP-02 — Define the minimal tenant-aware domain and persistence contracts**  
**Target:** .NET domain/application contracts and persistence boundary; Azure SQL schema and migrations. **Requirements:** PRD §§8–9, FR-OP-01/10 and all entity-backed modules. **Prerequisites:** IP-01. **Completion:** logical Tenant/User/Team/Permission/Approval, Knowledge/Version/Chunk, Conversation/Message/Citation, Customer, Ticket/Activity/CorrectionRequest/CancellationRequest/TicketAIResult, Feedback, Job, Setting/Retention, Audit, EvaluationRun and EmailDelivery needs are represented only as required; constraints and tenant-aware keys prevent cross-tenant association; migrations can be applied/replayed; indexes are justified by specified lookups; no speculative fields or schema changes are added.

**IP-03 — Establish protected audit, correlation, and telemetry foundations**  
**Target:** API, persistence and worker cross-cutting infrastructure. **Requirements:** FR-ID-07, FR-TM-04, FR-OP-04/05, §5.12 and §10. **Prerequisites:** IP-02. **Completion:** distinct application/security/administrative/ticket-activity records capture required actor, tenant, resource, action, timestamp, outcome and correlation data; access to audit records is protected and audited; secrets, reset tokens/URLs, full email, Feedback `reason`, deleted content and unnecessary sensitive prompts are excluded; trace/correlation spans can link UI/API/worker/model/search operations without excess personal data.

**IP-04 — Implement the centralized versioned default-deny authorization catalogue**  
**Target:** .NET authorization/application/data-access boundaries. **Requirements:** FR-ID-04/05/06/09/16/17, FR-OP-01/02/10, FR-TM-03/07/13, FR-TEAM-03/06, FR-AN-06 and FR-TK-09. **Prerequisites:** IP-02, IP-03. **Completion:** predefined roles/resources/actions and tenant/team/ticket/owner scopes are explicit, versioned and default-deny; every applicable read, write, direct-ID, search, tool, job and result path revalidates current authorization; Platform Admin has no prohibited tenant business/individual Customer/Feedback/TicketAIResult access; tests demonstrate positive and negative role/scope combinations and no grant mechanism beyond the Requirement.

**IP-05 — Implement local Identity, tenant and user administration**  
**Target:** .NET API, Identity persistence and administrative contracts. **Requirements:** FR-ID-01–15, FR-OP-02, workflow §6.4/6.7. **Prerequisites:** IP-02, IP-03, IP-04. **Completion:** local ASP.NET Core Identity only; self-registration disabled; tenant/user lifecycle and permitted predefined role assignment are tenant-scoped; reset/change, generic reset response, single-use protected time-limited link, proposed configurable password/lockout defaults, deactivated-account reset denial, scoped administrative recovery and audit are tested; Platform Admin permission changes require an independent second approver and cannot self-approve/elevate.

**IP-06 — Implement tenant-scoped support teams and membership rules**  
**Target:** .NET application/API, persistence, authorization. **Requirements:** FR-TEAM-01–06; workflow §6.6; relevant §5.9/5.10. **Prerequisites:** IP-04, IP-05. **Completion:** Tenant Admin creates/manages teams only in tenant; each team has one primary Manager; Managers can belong to multiple teams; each Agent has exactly one primary team; Manager membership is view-only; lifecycle/membership operations are validated and audited; deactivating a team preserves history and triggers assignment review. Primary-team change must be blocked until affected ticket assignments are validly dispositioned (completed in IP-11).

**IP-07 — Implement persisted background jobs and safe cancellation**  
**Target:** API, job persistence, selected worker boundary. **Requirements:** FR-OP-09, workflows §6.3/6.9, §5.14 and §9 async-job contracts. **Prerequisites:** IP-02, IP-03, IP-04; D-04 before final operation/provider settings. **Completion:** submission persists tenant/requester/operation context and returns HTTP 202 + Job ID/status endpoint; states are Queued/Processing/Completed/Failed/Timed Out/Cancelled; polling never resubmits; status/result/cancel rechecks scope; queued cancellation prevents execution, processing cancellation stops at a safe checkpoint without partial result, committed completion wins races, terminal states reject cancel, and cancellation is idempotent/audited. Retries are bounded and only for eligible transient failures; no duplicate work/effects.

**IP-08 — Implement validated operational settings, retention, cleanup, and tenant lifecycle**  
**Target:** API, admin settings, persistence/cleanup worker, Blob/Search deletion boundaries. **Requirements:** FR-OP-03/06/07/08/10, §§5.8/5.11/5.12, workflows §6.8 and §10. **Prerequisites:** IP-02, IP-03, IP-04, IP-05, IP-07. **Completion:** global settings and retention policies are validated, versioned, audited and role-scoped; configurable §5.11 defaults and independent API/model/job limits are represented; Customer-with-no-ticket retention starts from `Customer.CreatedAt`, associations suspend eligibility, no active related ticket can be purged, and all-terminal transitions restart the period from the latest terminal timestamp; relationship/eligibility is revalidated immediately before cleanup. Tenant deactivation blocks access/processing while retaining data; deletion uses the 30-day grace period and independent second approval; reversal requires two independent approvals; deletion purges required primary/derived/backup data and preserves only the exact irreversibly pseudonymized allowlist for no longer than the existing audit expiry. Verify no additional deleted-tenant data survives.

**IP-09 — Integrate the approved transactional email event allowlist**  
**Target:** API/Identity and worker email adapter; secured environment configuration. **Requirements:** FR-ID-11/12/13, §5.15, workflows §6.7 and §9. **Prerequisites:** IP-03, IP-05; D-03, D-04 before real delivery. **Completion:** one Human-selected provider behind a small configuration/service boundary; environment-specific verified sender and managed secrets; controlled test-account allowlist; generic reset semantics; only explicitly listed password and notification events/recipients; current recipient role/team/tenant/assignment resolved immediately before send; de-duplication, rate limits, bounded eligible retries, safe failures and status/correlation records; no tokens, URLs, credentials or unnecessary customer data in logs. Provider submission is not reported as inbox delivery.

### Phase 1 — Core business workflows and protected data access

**IP-10 — Implement the tenant/team-scoped ticket lifecycle**  
**Target:** .NET domain/application/API and SQL persistence. **Requirements:** FR-TM-01–08/10–13; workflows §6.5; Ticket/Activity entities in §8. **Prerequisites:** IP-02, IP-03, IP-04, IP-05, IP-06. **Completion:** create/list/detail/edit/search/filter/sort/page; initial statuses/categories/priorities and category-based queue recommendations; separate AssignedTeamId/AssignedAgentId; explicit New/Open/In Progress/Pending Customer/Resolved/Closed/Cancelled transitions and scope rules; Tenant Admin central triage only within tenant; Managers assigned-team only; Agents limited to permitted fields/actions; Platform Admin denied routine tenant ticket work; resolve/close/reopen/escalation rules and append-only history are validated server-side and audited. No permanent ticket deletion.

**IP-11 — Implement ticket correction/cancellation and assignment-change workflows**  
**Target:** .NET API/domain, persistence, audit and notifications. **Requirements:** FR-TM-04/07/09/11/13/14, FR-TEAM-03/05/06, §5.13, workflows §6.6/6.10/6.11 and §9. **Prerequisites:** IP-06, IP-09, IP-10. **Completion:** separate persisted field-correction and cancellation requests; mandatory reason/notes; duplicate active request protection; pending requests never change authoritative values; only allowed Manager/Tenant Admin decides eligible requests after revalidation; cancellation is terminal and not resolution/closure; category/priority changes only in eligible states. Agent primary-team change remains blocked until each assigned ticket is reassigned to an eligible Agent in its current team or only AssignedAgentId is cleared while AssignedTeamId is preserved; only Tenant Admin or Manager of that ticket's current team can dispose it. All outcomes audited; only listed notifications sent.

**IP-12 — Implement role-scoped Customer Search/Read and Feedback Read**  
**Target:** API, query/persistence boundary and audit. **Requirements:** FR-ID-16/17, Customer/Feedback clauses in §5.5, workflows §6.12/6.13, §8–9. **Prerequisites:** IP-02, IP-03, IP-04, IP-10. **Completion:** exact Customer ID and partial case-insensitive name/company matching, status/date filters, allowed sorting, validated configurable page limit, authorization/filter-before-pagination, total count and metadata; no email search. Direct-ID/search scope revalidated; permitted fields only; Tenant Admin tenant scope, Manager assigned-team scope incl. team-queued tickets, Agent currently-assigned-ticket scope and immediate revocation; Platform Admin has no individual Customer access. Email masked everywhere except authorized own-tenant Tenant Admin detail, with each unmask audited. Feedback returns only allowed fields including canonical `reason`, never conversation content/history; scoped read is audited without copying `reason` into audit.

**IP-13 — Persist and review AI urgency independently of Ticket.Priority**  
**Target:** .NET model/API, persistence, authorization and audit. **Requirements:** FR-TK-08/09, TicketAIResult §8/9, workflow §6.14, §13/14/18. **Prerequisites:** IP-02, IP-03, IP-04, IP-07, IP-10. **Completion:** SuggestedUrgency uses only Critical/High/Medium/Low and is stored separately from nullable ReviewedUrgency with model/deployment reference, creation and nullable reviewer/time; accept copies suggestion, override stores selected valid urgency, suggestion remains unchanged; every access/review revalidates exact Agent/current assignment, Manager/current team or Tenant Admin/tenant scope; Platform Admin denied; review never modifies Ticket.Priority; existing 90-day retention applied. Generation is integrated in IP-18.

### Phase 2 — Versioned knowledge and retrieval substrate

**IP-14 — Implement knowledge-document lifecycle and version approval**  
**Target:** API, persistence, Blob Storage boundary, admin contracts. **Requirements:** FR-KB-01–03/05–10/12, workflow §6.2, §8–9. **Prerequisites:** IP-02, IP-03, IP-04, IP-07, IP-09 for listed document-decision notifications. **Completion:** PDF/DOCX/TXT upload; actual type/content/size/processing validation (configurable initial 20 MB); tenant/uploader/version/state records; processing state separate from approval; exact-version Tenant Admin approve/reject; replacement/reprocess invalidates approval and stale content immediately; authorized delete immediately removes availability; no pending/rejected/failed/stale version is eligible for retrieval; safe errors and audit recorded.

**IP-15 — Build the bounded document processing and approval-aware search index**  
**Target:** worker, Blob, Azure AI Search and API adapters. **Requirements:** FR-KB-04/06/10–12; §7–9/11/14. **Prerequisites:** IP-07, IP-14; D-01 and D-04. **Completion:** extraction/normalization/chunking/embedding/indexing and authorized bulk indexing handle exact document versions; state and failures are observable; indexing is tenant-scoped; approved-version filter is applied before retrieval; update/reprocess/reject/delete makes prior chunks unavailable immediately and physically purges per approved policy; citations identify source version and page/section where feasible; retries are bounded and safe.

### Phase 3 — AI services, tools, assistant, ticket intelligence, analytics

**IP-16 — Implement the model/search adapters and read-only typed tool registry**  
**Target:** .NET application/API integration boundary. **Requirements:** FR-WF-01–06, FR-OP-03/04/06/07, §§5.5/5.8/7/9/11. **Prerequisites:** IP-03, IP-04, IP-07, IP-15; D-01, D-02, D-04. **Completion:** only approved configured model/search services are accessed server-side; provider keys never reach browser; only the six named allowlisted read-only tools exist with typed input/output, backend scope checks, validation, timeouts/rate limits, safe errors and audit; no arbitrary SQL, shell, unrestricted network or write tools. Model/deployment/token/cost metadata is versioned/configurable; invalid structured output cannot be persisted or corrupt business values.

**IP-17 — Implement the internal-role Customer Assistant and grounded RAG conversations**  
**Target:** API, conversation persistence and retrieval integration. **Requirements:** FR-CA-01–08, FR-KB-11/12, workflows §6.1, §8–9/11/13. **Prerequisites:** IP-07, IP-15, IP-16. **Completion:** authenticated internal roles only; no external customer access. Tenant Admin, Manager and Agent retrieval uses only current approved knowledge within scope; the Platform Admin assistant is limited to the authorized single-selected-tenant aggregate-analytics path and cannot retrieve knowledge documents or underlying tenant business records. Responses are source-backed with clear abstention for insufficient/conflicting/stale evidence and citations; at most 10 recent turns are used within scope; only the conversation owner can read history; feedback submission remains separate from Feedback Read; no email/customer mutation. UI is covered in IP-22.

**IP-18 — Implement ticket intelligence and non-sending Copilot workflows**  
**Target:** .NET API/model jobs; Copilot UI is in IP-22. **Requirements:** FR-TK-01–09, FR-AC-01–07, workflows §6.3/6.14, §8–9/11/13. **Prerequisites:** IP-07, IP-10, IP-13, IP-15, IP-16; D-01, D-02, D-04. **Completion:** authorized summary/classification, sentiment/urgency suggestions, queue/escalation recommendations, knowledge recommendations and editable grounded reply drafts execute through persisted jobs as needed; structured output validated; suggestions remain non-authoritative; agents can edit/copy/discard/regenerate; human review required; no customer-facing send and no AI ticket mutation. Urgency storage/review follows IP-13 exactly.

**IP-19 — Implement scoped predefined analytics and read-only analytics tools**  
**Target:** API/query and tool boundary. **Requirements:** FR-AN-01–06, FR-WF-01/02/05, §5.5/6 and §9. **Prerequisites:** IP-04, IP-10, IP-16. **Completion:** status/category/priority counts and 7-/30-day trends; only predefined read-only questions/functions (no text-to-SQL); Tenant Admin tenant, Manager assigned-team, Agent own authorized-ticket data; Platform Admin one explicitly selected authorized tenant aggregate only and no underlying business-record access; result declares data scope and time range; audit and tests cover both allow/deny paths.

### Phase 4 — User-facing workflows

**IP-19A — Establish per-slice API contract baselines and consumer readiness**  
**Target:** API presentation layer OpenAPI/contract artifacts and API contract test project(s). **Requirements:** §9 and its final-contract rule (schemas, validation, status codes, error responses, idempotency where needed, OpenAPI documentation); FR families of each slice below; §§13–14. **Prerequisites (per slice; each slice may become ready independently):** S1 identity, tenant, user, team, permission, settings/retention, tenant lifecycle and notification contracts — IP-05, IP-06, IP-08, IP-09; S2 ticket lifecycle, requests, assignment and urgency review — IP-10, IP-11, IP-13; S3 knowledge, indexing status, chat/citations and Copilot — IP-14, IP-15, IP-17, IP-18; S4 Customer Search/Read/unmask and Feedback Read — IP-12; S5 analytics — IP-19. Where a slice exposes asynchronous work, IP-07 is also a prerequisite for that slice. **Completion (per slice):** a versioned, reproducible OpenAPI description of exactly the operations consumed by the slice's UI task, generated from or checked against the producing API; it covers request/response schemas, validation rules, authorization/role scope, status codes and error responses, pagination/filter/sort where applicable, and 202/Job ID/status/result/cancellation and idempotency where required. API contract tests for those operations pass against the producer implementation. A slice readiness record names the slice, its contract version, its producer tasks and its consumer task. No route, field or value is added beyond the approved Requirement, and illustrative names are carried forward only where the design confirms them. D-01 through D-04 are not resolved by this task. **Task completion:** all slices S1–S5 are ready. **Change rule:** any change to a slice contract after readiness re-runs that slice's contract tests and reconciles the affected consumer task before that consumer proceeds.

**IP-20 — Build authentication, tenant/user/team, permission and configuration UI**  
**Target:** React + TypeScript. **Requirements:** FR-ID-01–15, FR-TEAM-01–06, FR-OP-02, workflows §6.4/6.6/6.7/6.8. **Prerequisites:** IP-05, IP-06, IP-08, IP-09 and IP-19A slice S1 ready. **Completion:** UI exposes only role-authorized actions; tenant/user/team lifecycle, permission view, privileged approval, settings/retention, account recovery and team membership flows; field/status constraints mirror but never replace server enforcement; accessible keyboard/label/contrast/loading/error behavior.

**IP-21 — Build ticket lifecycle and request/review UI**  
**Target:** React + TypeScript. **Requirements:** FR-TM-01–14, FR-TEAM-03, FR-TK-01/08/09, workflows §6.5/6.10/6.11/6.14. **Prerequisites:** IP-10, IP-11, IP-13, IP-20, IP-19A slice S2 ready. **Completion:** ticket lists/details, role-appropriate edits/actions, assignment/central triage boundaries, correction/cancellation request and decision views, urgency review, state visibility and audit-relevant reasons; no Agent direct Category/Priority changes, no Platform Admin tenant ticket view, no urgency-to-priority mapping.

**IP-22 — Build knowledge administration, chat, citations and Copilot UI**  
**Target:** React + TypeScript. **Requirements:** FR-KB-01–12, FR-CA-01–08, FR-AC-01–07, workflows §6.1–6.3. **Prerequisites:** IP-14, IP-15, IP-17, IP-18, IP-20, IP-19A slice S3 ready. **Completion:** upload/version/process/approval/delete states; exact-version decisions; grounded citations/abstention; owner-only conversation history; job status; editable non-sending reply drafts; safe errors and accessible interactions.

**IP-23 — Build Customer Search/Read, unmask, and Feedback UI**  
**Target:** React + TypeScript. **Requirements:** FR-ID-16/17, workflows §6.12/6.13, §§5.5/9/13. **Prerequisites:** IP-12, IP-20, IP-19A slice S4 ready. **Completion:** exact supported query/filter/sort/page behavior and visible role scope; masked email by default; only authorized Tenant Admin detail action can unmask; limited Feedback fields only, no conversation/message view; backend remains authoritative.

**IP-24 — Build role-scoped analytics dashboard UI**  
**Target:** React + TypeScript. **Requirements:** FR-AN-01–06 and §13. **Prerequisites:** IP-19, IP-20, IP-19A slice S5 ready. **Completion:** displays only authorized aggregate/ticket data with scope/time range and clear loading/error/empty states; no cross-tenant or underlying record drill-down for Platform Admin.

### Phase 5 — Quality, evaluation, release evidence

**IP-25 — Create deterministic synthetic fixtures and repeatable AI evaluation assets**  
**Target:** test/evaluation projects and non-production seed tooling. **Requirements:** FR-EV-01–06; §12, §5.7, §13–14. **Prerequisites:** IP-07, IP-10, IP-12, IP-13, IP-14, IP-15, IP-16, IP-17, IP-18, IP-19. **Completion:** deterministic seed data (20 fictional knowledge articles; 100 synthetic tickets across five fictional tenants, tenant-scoped teams and ten fictional agents, plus synthetic role users); versioned 50 question/source pairs, 10 no-answer cases and 10 prompt-injection cases; ticket structured-output scenarios; evaluation report includes dataset/run/model/deployment/prompt versions, numerators/denominators, per-case failures and baseline comparison. No real data/secrets. Proposed numerical evaluation targets remain non-gating; authorization failures are always release failures.

**IP-26 — Execute integrated acceptance, security, and operational verification**  
**Target:** unit, integration, API, UI/component, end-to-end, security and operational test projects. **Requirements:** §§13–14/18; all FR families; all workflows §6. **Prerequisites:** completion of every task IP-01 through IP-25, including IP-19A. **Completion:** all mandatory acceptance criteria pass across roles and negative cases; specifically test cross-tenant/team/direct-ID enumeration, conversation ownership, current authorization after reassignment, two-person approval, default-deny scopes, Customer filters before pagination, email masking/unmask audit, limited Feedback/no `reason` logging, ticket transitions/requests, urgency values and no Priority mutation, primary-team disposition, queued/processing cancellation races/partial-result prevention, approval-aware RAG, retention/deletion exact metadata boundary, approved notification events, secret/sensitive-data minimization and retry/error behavior. Record executed evidence and limitations; no percentage evaluation target is silently converted into a release gate.

**IP-27 — Complete developer documentation, CI release path, and deployment verification**  
**Target:** README, GitHub Actions, deployment/configuration artifacts and runbooks. **Requirements:** FR-OP-03/08, §7/10/15/18 and reproducibility criterion. **Prerequisites:** IP-01, IP-25, IP-26 and D-01, D-02, D-03, D-04; worker hosting decision resolved. **Completion:** documented setup, tests, environment configuration, secret handling, deployment, health checks, monitoring, cost/teardown and known limitations; each bounded task has an issue with acceptance/test expectations; PRs link issues, include design/test/migration/configuration evidence, and pass CI plus required human review; deployment workflow uses approved Azure resources and reports only observed smoke-test outcomes. No live provisioning/deployment is authorized by this planning process; any such action requires its own applicable approval.

## 5. Dependency and Concurrency Assessment

### Dependency ordering

The dependency chain is: **IP-01 → IP-02 → IP-03/IP-04 → IP-05/IP-06/IP-07 → IP-08/IP-09/IP-10/IP-14 → IP-11/IP-12/IP-13/IP-15 → IP-16 → IP-17/IP-18/IP-19 → IP-19A (per slice) → IP-20–IP-24 → IP-25 → IP-26 → IP-27**, subject to the per-task prerequisites and D-01–D-04 above. Cross-cutting authorization, audit and persistence contracts precede their consumers. Knowledge version approval precedes indexing/retrieval. Ticket, team and permission contracts precede workflows/UI. Final acceptance follows integration, not isolated module claims. Each IP-19A slice depends only on its own producer tasks, so a UI task may start as soon as its own slice is ready and its other prerequisites are complete.

### Related work, shared surfaces and execution mode

- **Observed:** one repository and one checkout/worktree; no other active worktrees/attempts or Orchestrator coordination was established. The prior Requirement Analysis/Verification/Approval records are completed predecessor records, not concurrent implementation tasks. Other active features or external work are **UNKNOWN/UNASSESSED**. No safety is inferred from absence of a dependency declaration.
- **Shared surfaces:** solution/project manifests, domain contracts, permission catalogue, migrations and tenant keys, API/OpenAPI contracts, React route/components/types, worker/job state, model/search configuration, audit/retention, CI/deployment files and common test fixtures will be shared across modules. Most tasks modify multiple linked surfaces; parallel work is not established as safe.
- **Execution mode:** read-only planning may overlap only where process boundaries and distinct output scopes permit. **All implementation writes in the current shared checkout must be serialized by one SDLC Process Orchestrator.** No task-level parallel implementation is approved by this Plan. If an Orchestrator later proposes concurrency, it must first assess exact tasks/files/contracts/schema/config/shared surfaces and related work; concurrent writes require isolated worktrees, explicit ownership, and an integration/reconciliation step before combined verification. Merging isolated work does not waive rebase/conflict resolution, migration/API compatibility review, or full post-integration tests.
- **Integration:** at each phase boundary reconcile domain/API/schema changes; re-run impacted contract, authorization and migration tests; a contract change after an IP-19A slice is ready follows the IP-19A change rule; after all modules are combined, perform IP-26 against the integrated checkout. Any implementation-plan changes follow governed corrective change control; do not alter approved task definitions informally.

## 6. Affected Projects and Layers

No projects currently exist. The planned logical targets (not existing project names) are:

1. **React + TypeScript presentation:** internal chat, knowledge/admin, tickets, customer/feedback, analytics and configuration.
2. **.NET 8 ASP.NET Core Web API/application:** Identity, API contracts, validation, authorization, orchestration, read-only tools, configuration and job submission.
3. **Domain/application and persistence boundary:** tenant-aware rules, SQL entities/migrations, activity/requests, permissions, jobs, evaluation metadata.
4. **Background worker/Azure Functions boundary (choice open):** persisted AI/RAG/ticket/knowledge work, retries, timeout/cancellation and cleanup.
5. **Azure integrations:** Azure SQL, Blob Storage, AI Search, selected AI model endpoint, Key Vault and Application Insights; no credentials in browser/source.
6. **Transactional email adapter:** only approved event/recipient list; provider remains unselected pending D-03.
7. **Quality/release/docs:** unit/integration/API/security/E2E/evaluation projects, GitHub Actions, README and Azure deployment/runbook.

## 7. Testing and Verification Strategy

Use the eventual repository's adopted minimal test conventions; none exist today, so no current test framework or command is assumed.

- **Unit:** permission matrix/default-deny, tenant/team/ticket filters, state transitions and requests, upload validation/chunking, email-recipient resolution, structured output validation, Feedback/Customer field minimization, urgency accept/override invariants, Customer retention clocks, tenant-deletion allowlist, job cancellation races/idempotency and retry classification.
- **Persistence/integration:** migrations, tenant-aware uniqueness, SQL repositories and filtering-before-pagination/counts; Blob upload/delete; exact-version approval/index invalidation; Azure Search approved-version filtering; job persistence/worker restart/cancel; email adapter safe status; audit and cleanup/backup reapplication.
- **API/security:** every role/resource/action positive and negative combination; cross-tenant/team direct ID and enumeration; Agent assignment/scope revocation; Manager team and unassigned-ticket denial; Platform Admin restrictions; two-admin approval; reset genericity/deactivated denial; Customer masking and Tenant Admin-only detail unmask; Feedback scope/field limits; async job status/result/cancel authorization; allowlisted tools and safe errors.
- **UI/component/accessibility:** role-appropriate controls, hidden/disabled actions backed by server denial, keyboard navigation, labels/contrast, loading/error/empty states and no sensitive-field leakage.
- **End-to-end:** all §6.1–6.14 workflows including knowledge upload→processing→exact-version approval→RAG/citation, reprocess invalidation, ticket lifecycle/corrections/cancellation, teams and primary-team reassignment, Customer/Feedback, urgency review, account recovery, notifications, analytics and jobs/cancellation.
- **AI evaluation:** versioned synthetic datasets, retrieval Recall@5, claim grounding, citation precision and coverage, abstention, structured-output validity, prompt-injection cases; report denominators, limitations, per-case failures and baseline. The PRD's proposed thresholds remain non-gating unless separately approved; any successful unauthorized access fails mandatory acceptance.
- **Operational:** configured rate/concurrency/upload/context/timeouts, health/telemetry correlation, safe retry/error paths, retention and tenant deletion, secret scanning, deployment smoke tests and teardown. No build/test execution was possible or attempted during planning because the repository contains no product implementation or test projects.

## 8. Requirement-to-Task-to-Verification Traceability

Task references in this table mean `supportiq-product-implementation-plan@0.2/<task-id>`.

| Approved requirement / contract | Implementation tasks | Planned verification evidence |
|---|---|---|
| §4.1 mandatory release and §16 modules (identity/access; teams; configuration/tenant lifecycle; knowledge; tickets; Customer/Feedback; AI; tools/analytics; jobs; audit; evaluation; CI/docs/deploy) | IP-01–IP-27 (including IP-19A), by module descriptions above | IP-25 synthetic/evaluation evidence; IP-26 complete acceptance/security/E2E suite; IP-27 CI and approved-environment smoke evidence |
| §4.2 deferred/optional; FR-AC-06/07; FR-WF-04 | Excluded from all tasks; boundaries in IP-16–IP-18/IP-27 | Negative scope review in IP-26; verify no auto-send/write tool, custom role, internal notes or excluded integration |
| FR-ID-01–17; §5.9 permission catalogue; §6.4/6.7 | IP-03–IP-05, IP-08–IP-09, IP-12, IP-20, IP-26 | Identity/RBAC/lockout/recovery/privileged-approval API and security cases; scoped UI/E2E; audit and email evidence |
| FR-TEAM-01–06; §5.13; §6.6 | IP-06, IP-10–IP-11, IP-20–IP-21, IP-26 | Team/membership/primary-team blocked-change and assignment disposition unit/API/security/E2E cases |
| FR-TM-01–14; §6.5/6.10/6.11; Ticket, activity, correction and cancellation contracts | IP-02–IP-03, IP-10–IP-11, IP-21, IP-25–IP-26 | State/role/field tests; correction/cancellation pending and decision tests; history/audit and integrated ticket workflows |
| FR-TK-01–09; §6.3/6.14; TicketAIResult contract | IP-10, IP-13, IP-18, IP-21–IP-22, IP-25–IP-26 | Schema/safe-output tests, role scope and revocation tests, urgency accept/override and no-Priority-mutation assertions, E2E |
| FR-KB-01–12; §6.2; Knowledge/Approval/Chunk contracts | IP-07–IP-09, IP-14–IP-15, IP-22, IP-25–IP-26 | Upload/type/size, exact-version approval, reprocess/delete invalidation, tenant isolation, job/index/citation integration and E2E |
| FR-CA-01–08; §6.1; conversation ownership/citation contracts | IP-16–IP-17, IP-22, IP-25–IP-26 | Internal-role access/external denial; approved evidence/citations/abstention; 10-turn scope and owner-only history tests |
| FR-AC-01–07; §6.3; draft reply contract | IP-16–IP-18, IP-22, IP-25–IP-26 | Authorized context, editable draft controls, no auto-send and no AI mutation tests |
| FR-WF-01–06; §5.5 allowlist; §9 tool contracts | IP-16–IP-19, IP-25–IP-26 | Tool allowlist, typed-contract, role/tenant scope, timeout/safe error, audit, no SQL/shell/network/write tool tests |
| FR-AN-01–06; §5.5 analytics allowlist | IP-16, IP-19, IP-24–IP-26 | Scope/time-range assertions for Tenant Admin, Manager, Agent and selected-tenant aggregate-only Platform Admin; no text-to-SQL |
| FR-EV-01–06; §5.7; §12 | IP-25–IP-26 | Dataset manifest, versioned run output, metric numerator/denominator, baselines, limitations and non-gating target handling |
| FR-OP-01–10; §§5.8/5.11/5.12; §10 | IP-02–IP-09, IP-14–IP-16, IP-26–IP-27 | Tenant isolation, secrets/logging, rate/time limits, cost usage, job state, retention/deletion, audit/telemetry, CI/deploy tests |
| §5.11 retention/deletion including Customer no-ticket start and deleted-tenant audit boundary; §6.8 | IP-03, IP-07–IP-08, IP-26–IP-27 | Clock/state boundary tests, race revalidation, exact retained-field allowlist/pseudonymization/access/expiry, cleanup/recovery tests |
| §5.12 administrative/security/ticket audit | IP-03, IP-05–IP-15, IP-26 | Per-event record fields, access controls, sensitive-data exclusion and correlation coverage |
| §5.14/§6.9/§9 persisted jobs and cancellation | IP-07, IP-14–IP-18, IP-26 | 202/Job ID/status/result/cancel contracts; cancellation/race/idempotency/no partial-result tests |
| §5.15 approved notification events, recipients and email security | IP-09, IP-11, IP-14, IP-20, IP-26 | Event/recipient allowlist, active/scope resolution, duplicate prevention, test allowlist, delivery failure/retry/security tests |
| §§7–9 approved architecture, illustrative entities and API contracts | IP-01–IP-24 (including IP-19A); IP-26 | Project/API/schema design review, contract tests, IP-19A per-slice OpenAPI contract and readiness evidence, architecture boundary checks; no invented route/entity treated as required |
| §§10–11 NFR and AI guardrails | IP-03–IP-09, IP-14–IP-19, IP-22–IP-27 | Auth, privacy, reliability, accessibility, latency/limits, prompt-injection, grounding/citation and operational verification |
| §13 acceptance criteria; §14 test strategy; §18 Definition of Done | IP-25–IP-27 | All specified unit/integration/API/security/E2E/evaluation/operational checks and recorded results |

No approved functional requirement is intentionally left without task and verification coverage. The complete task-to-requirement and task-to-evidence binding must be maintained in the implementation execution records when work begins; task IDs must not be used to expand product scope.

## 9. Risks, Dependencies, and Open Decisions

### Risks

| Risk | Level | Planned handling |
|---|---|---|
| No application code, project structure, test setup, CI or deployment artifacts exist; detailed project conventions cannot be inferred. | Important | Begin with IP-01; record concrete files/tools selected; keep minimal and within PRD stack. Do not claim existing architecture. |
| Cross-tenant/team exposure through list filters, direct IDs, cache/index, worker context, tools, or stale assignments. | Blocking security risk | Centralize default-deny authorization; revalidate at every boundary; mandatory negative API/integration/E2E tests; no release acceptance with any unauthorized success. |
| Job cancellation/completion races and partial AI/index results. | Important | Persist explicit state transitions, idempotency and safe checkpoints; test concurrent commit/cancel and no partial result exposure. |
| Exact-version knowledge approval can be bypassed by stale index or reprocessing/deletion races. | Important | Version-bound state and approval; immediate retrieval exclusion; integration verification on index/storage paths. |
| Customer retention clock, tenant deletion and exhaustive audit metadata boundary are complex and safety-sensitive. | Important | Implement as explicit state/clock logic; revalidate before purge; test exact allowlist, pseudonymization, access, expiry and recovery reapplication. |
| Model quality, prompt injection, quotas and cloud costs. | Important | Synthetic data, grounding/abstention, allowlist, rate/token/time limits and measurement reporting; settle D-01/D-02 before enabling model-backed work. |
| Real email delivery and recipient resolution may disclose sensitive data or report false success. | Important | D-03 gate; strict event/recipient allowlist, verified sender, safe metadata, controlled test accounts, no secrets/tokens in logs. |
| PRD's 30-day boundary is a target, not a schedule/capacity commitment; feature set is broad. | Important | Sequence by dependencies and prioritize security/admin/core ticket/knowledge/AI/mandatory acceptance as PRD directs; explicitly defer only already-approved optional scope. No dates/capacity promised. |

### Dependencies

- Human Plan Approval plus implementation-stage initiation/Orchestrator authorization before any task execution.
- D-01 through D-04 before the implementation areas identified in §3; Azure region/resource availability, quota, pricing and secured environment configuration must be established before deployment/provider use.
- Target project scaffold, SQL migration path, authz/audit contracts and synthetic fixtures are foundational dependencies; specific APIs and schemas remain design-time contracts.
- No external ticketing/CRM/messaging integration is a dependency; those are explicitly excluded.

## 10. Explicitly Out of Scope

The exclusions in §1 are binding. In addition, this Plan does not select or approve a model, embedding, region, token/cost budget, email provider, sender, job timeout/retry value, worker hosting choice, package/test framework, schema/index, or exact API route where the PRD leaves it open/illustrative. No production readiness, legal/compliance commitment, real customer data, live cloud provisioning, implementation, or testing result is claimed.

## 11. Plan Validation

Self-validation against `IMPLEMENTATION_PLANNING_GUIDELINES.md` §19:

- [x] Exact source requirement and explicit human approval evidence bound; source document's contradictory draft label reconciled without editing it.
- [x] Actual repository inspected; no app/test/project conventions invented; architecture claims distinguished from PRD target architecture.
- [x] Functional scope comes from the approved v1.11 PRD; full mandatory scope and explicit exclusions retained.
- [x] All requirement families and cross-cutting sections map to implementation tasks and verification coverage.
- [x] No new business requirement, provider choice, model choice, operational target, or unapproved functionality introduced.
- [x] Tasks are actionable, Plan-local, layer-assigned, dependency-ordered and have observable completion criteria.
- [x] Dependencies identify external decision gates; absence of other-work information is not treated as independence.
- [x] Data/API/persistence changes remain within PRD logical contracts; schema and illustrative routes are not silently finalized.
- [x] Testing strategy covers all affected layers and security-critical negative cases using a future minimal test convention.
- [x] Risks, D-01–D-04, repository limitations, scope exclusions and implementation authorization boundaries are explicit.
- [x] No implementation code or test/build results are included.
- [x] Plan and Requirement exact versions/fingerprints are present; task IDs unique and prerequisite references explicit; v0.1 disposition recorded: superseded draft candidate; tasks IP-01–IP-27 carried forward unchanged except IP-20–IP-24 prerequisites and the IP-26 prerequisite clause; IP-19A added.

**Result:** Self-validation **PASS WITH EXPLICIT DECISION GATES AND REPOSITORY LIMITATIONS**. This is the planning actor's validation only; it is not independent Implementation Plan Verification. The four approved-Requirement §17 decisions remain open and block only their dependent implementation tasks. Concurrency safety is not established, so implementation is serialized. Because independent verification and all later human gates have not occurred, status remains **Draft Candidate**.

## 12. Approval Status and Handoff

- **Candidate plan status:** Draft Candidate v0.2; candidate v0.1 remains preserved as a superseded draft.
- **Independent Implementation Plan Verification:** Complete verification of candidate v0.2 has not been performed; required next process.
- **Human Review Approval:** Not requested or obtained.
- **Human Plan Approval:** Not requested or obtained.
- **Implementation authorization:** None. No implementation may begin from this candidate.
- **Governed next sequence:** Complete independent Implementation Plan Verification of candidate v0.2 → resolve verification findings and required decisions → complete current-plan Human Review package → Human Review Approval (progression only) → separate Human Plan Approval → Implementation using only the current approved Plan, under required Orchestrator coordination.
