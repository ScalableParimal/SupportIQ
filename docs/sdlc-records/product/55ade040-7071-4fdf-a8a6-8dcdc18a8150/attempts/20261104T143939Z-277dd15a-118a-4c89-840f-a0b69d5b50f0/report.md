# Requirement Analysis — Post-Requirement-Update Refresh

## Record, authority, and outcome

- **Record ID:** `20261104T143939Z-277dd15a-118a-4c89-840f-a0b69d5b50f0:report`
- **Feature:** SupportIQ product requirement
- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt ID:** `20261104T143939Z-277dd15a-118a-4c89-840f-a0b69d5b50f0`
- **Process:** Requirement Analysis
- **Analysis type:** Post-Requirement-Update refresh
- **Creator / role:** AI assistant using Copilot SDK in VS Code / Requirement Analysis process actor
- **Record prepared at:** `2026-11-04T14:44:56.505748+00:00` (Python timezone-aware system UTC; not exact filesystem publication time)
- **Outcome:** `POST_UPDATE_ANALYSIS_COMPLETE_DECISIONS_REQUIRED`
- **Authoritative Requirement:** `docs/requirement/SupportIQ_Product_Requirement_v1.1.md`
- **Version ID:** `SupportIQ Product Requirement v1.1@sha256:E2AA6F67665533ADDD150062F6656DC9B2A9A232B0D5FD96388C9ED335E3CED2`
- **Source status:** Draft; unapproved Initial Analysis Clarification
- **Source modified:** No
- **Human Requirement Approval:** Not claimed
- **Requirement Analysis Verification started:** No
- **Implementation or plan authorized:** No

This refresh analyzes version 1.1 following the authorized Requirement Update. It uses the current v1.0 initial-analysis and v1.1 update chain, the update's human-decision record, and applicable portability/lifecycle context. Older unrelated Requirement Analysis or Requirement Update reports/evidence were excluded. The 15 reviewed inputs and their fingerprints are bound by `checkpoint-0001.json`; the current execution-context and product-root authority are bound by `checkpoint-0002.json`.

No product source, requirement, plan, test, configuration, or governance source was changed. No application, test, build, runtime, deployment, or live integration was executed.

## 1. Understanding

SupportIQ is a fictional CloudDesk B2B SaaS support portal and a learning/portfolio project. The demonstrable first release is intended to provide tenant-aware identity and administration, knowledge management and grounded RAG, internal ticket management, AI ticket assistance, bounded read-only tools and analytics, audit, evaluation, operational controls, CI, and Azure deployment. The stated 30-day boundary is a target, not a guarantee or fixed schedule. The document explicitly does not claim production readiness.

The four roles are Platform Admin, Tenant Admin, Support Manager, and Support Agent. AI output is assistive; people retain responsibility for customer-facing decisions and business-changing actions. The product uses synthetic/fabricated tenant, customer, ticket, and evaluation data only in the first release.

## 2. Explicit requirements and rules

### Functional requirements

- **Identity and administration (FR-ID-01..09):** Local ASP.NET Core Identity; platform tenant/user provisioning; tenant-scoped user administration; four predefined roles; centralized resource/action authorization; permission and administration audit; controlled demo seeding; no self-registration.
- **Knowledge and RAG (FR-KB-01..08, FR-CA-01..08):** PDF/DOCX/TXT upload; configurable 20 MB initial maximum; validate content and size; tenant-scoped processing, status, indexing, update/reprocessing and deletion; authorized search, source references, grounded answers, abstention, 10-turn context, history, and feedback.
- **Tickets and agent assistance (FR-TM-01..08, FR-TK-01..07, FR-AC-01..07):** Full internal synthetic-ticket lifecycle, search/filter/sort/page, configurable statuses/categories/priorities/queues, authorized assignments and transitions, activity history, AI summaries/classification/sentiment/urgency and editable reply drafts. AI does not send customer messages or invoke write tools.
- **Tools and analytics (FR-WF-01..06, FR-AN-01..05):** Explicit typed, tenant-authorized, read-only knowledge/ticket/customer lookup, summary/classification and predefined analytics. Arbitrary SQL/shell/unrestricted networking and arbitrary text-to-SQL are excluded.
- **Evaluation and operations (FR-EV-01..06, FR-OP-01..08):** Versioned evaluation assets and run metadata; grounding, citations, retrieval, abstention, injection and tenant-boundary tests; server-side authorization; secrets protection; telemetry, configurable limits, safe errors, usage/cost monitoring and repeatable deployment.
- **Administration, retention, audit (FR-ID-01..09, FR-OP-04..07, FR-TM-04, sections 5.11–5.12):** Validated, centralized, configurable, versioned and audited operational settings; document deletion/retrieval rules; proposed backup/log/conversation/evaluation retention; minimal audit metadata and protected audit records.

### Explicit business rules and constraints

- Enforce tenant and role authorization on backend APIs and data access; deny cross-tenant access to all relevant data.
- Restrict the first-release AI tool surface to the allowlist. No AI-invoked write tools or automatic customer communications.
- Human review is required for customer-facing drafts and business-changing actions. AI suggestions remain distinct from authoritative ticket/customer data until a permitted human acts.
- Use synthetic/fabricated data only. Do not use real customer records or secrets in prompts, fixtures, logs, or screenshots.
- No Entra ID/enterprise SSO, production external ticketing/CRM/messaging integrations, internal-note workflow, custom roles/tenant permission overrides, SLA indicators, or autonomous business-data modifications in this release.
- Cross-tenant access denial is a mandatory acceptance criterion irrespective of the proposed evaluation percentages.

## 3. Human decisions and scope incorporated

These are decisions authorizing the v1.1 clarification; they do not approve the Requirement itself.

| Decision | Incorporated disposition |
|---|---|
| Identity and authorization | ASP.NET Core Identity with local authentication; Entra/enterprise SSO deferred; four predefined roles; tenant-scoped user administration; explicit testable RBAC; backend enforcement and negative tenant-isolation tests. |
| Knowledge limits and retention | PDF/DOCX/TXT, 20 MB initial limit, validation, configurable policies, immediate retrieval unavailability on deletion, physical purge within 30 days, backups up to 30 days, logs 30 days, conversations and synthetic evaluation data/results 90 days. These values are proposed defaults in the unapproved draft. |
| AI technology direction | Azure AI model endpoints and Azure AI Search retained. Exact model/deployment, embedding, region, token caps and budget are deferred to a technical decision gate before implementation. |
| Tickets and data | Deterministic synthetic seed: 100 fictional tickets, 5 tenants, 10 agents; listed initial fields, statuses, categories, priorities and default queues; no real external ticketing integration. |
| Tools and analytics | Explicitly allowlisted, read-only, tenant-scoped tool/analytics surface; no AI-invoked writes. |
| Scope and delivery | Expanded modules are mandatory first-release scope; 30 days is a target, not a guarantee or weekly plan. |
| Evaluation targets | Recall@5 ≥80%, grounded answer rate ≥90%, citation precision ≥95%, and 100% on initial abstention/structured-output/injection cases are proposals only, not current formal release gates. Cross-tenant denial remains mandatory. |
| Other boundaries | Internal notes, SLA indicators, external integrations, Entra ID, and custom roles remain deferred/out of scope. |

The applicable portability disposition keeps the adopted Master lifecycle controlling and every verification/approval gate intact (PB-01). PB-02 remains a condition at affected future runtime/live-integration/release boundaries, not a blocker to this analysis. This refresh does not claim runtime assurance or waive any gate.

## 4. Scope

### In scope

The mandatory v1.1 first demonstrable release: tenant/user administration and RBAC; configurable operational/retention controls; knowledge-to-RAG; complete internal synthetic-ticket management; ticket intelligence and agent copilot; read-only tools and tenant-scoped analytics; audit, evaluation, tests, CI, documentation, monitoring, and Azure deployment.

### Out of scope

The explicit v1.1 exclusions listed above, including external production integrations, SSO, internal notes, SLA indicators, custom roles/tenant overrides, arbitrary text-to-SQL, autonomous multi-agent behavior, and AI-invoked writes.

### Deferred / undecided

Exact model/deployment/region, model-specific token caps and monetary budget; detailed RBAC assignments; support-team structure; ticket transitions and additional Tenant Admin actions; customer lookup fields; audit access and retention; knowledge approval semantics; retention for ticket/customer/user/feedback/activity/AI-result data; timeout interaction; and evaluation target gate/measurement semantics. Technical model, region, quota and cost choices are explicitly deferred until the pre-implementation technical decision gate.

## 5. Ambiguities and decision-relevant gaps

| ID | Requirement reference | Ambiguity or gap | Importance and impact |
|---|---|---|---|
| A-01 | FR-CA-03, FR-AC-04, tool allowlist; FR-KB-01..08 | Search and suggestions refer to “approved” knowledge, but the knowledge lifecycle only defines Uploaded, Processing, Indexed, Failed, and deletion statuses. No approval owner, transition, or rule states whether authorized upload/indexing itself makes a document approved. | **Blocking.** Retrieval eligibility and the trust boundary for grounded answers cannot be finalized without an explicit approval rule. |
| A-02 | FR-ID-04..06; sections 3, 5.5, 5.9, 5.10 | The Requirement calls for an explicit resource/action permission matrix, but gives role summaries and broad “authorized/permitted” language rather than the complete initial role/resource/action assignments. Platform Admin may edit global mappings while privilege escalation must be prevented; the permitted change surface and protection against self-elevation are unspecified. | **Blocking.** Security behavior, administrative controls, and complete negative authorization tests are not determinable. |
| A-03 | FR-TM-03, FR-TM-07; section 5.5 | Support Manager scope is “team-level,” but no support-team entity, membership assignment, or rule defining which tickets belong to a team is specified. The sample data counts agents but does not define teams. | **Blocking** for team-restricted ticket/analytics capabilities; visibility boundaries cannot be tested as written. |
| A-04 | FR-TM-01, FR-TM-05, FR-TM-07 and the paragraph after FR-TM-08 | Status names are supplied, but allowed transitions, guards, reopen/escalation rules, and the precise actions Tenant Admin may take are intentionally left unresolved. “Authorized” does not define the matrix. | **Blocking** for finalizing the affected lifecycle and permission behavior; do not infer transitions from the status list. |
| A-05 | First-Release Tool Allowlist, Customer Lookup; section 17 | “Only necessary customer information” is not a field-level allowlist. The logical Customer entity says “fabricated display information,” but does not establish which fields can be returned with related ticket history. | **Important / blocking for Customer Lookup contract.** Data minimization and privacy tests require a defined response shape. |
| A-06 | FR-OP-05, FR-OP-07, FR-TM-04, sections 5.11–5.12 | Audit duration and reader permissions are open. Retention defaults do not state a policy for tickets, customer records, user accounts, feedback, ticket activity, or ticket AI results; tenant deactivation/deletion effects are also unspecified. | **Blocking** for complete retention, privacy, and audit behavior; stale or over-retained data and access cannot be assessed. |
| A-07 | Section 5.11 | General API timeout is 30 seconds, while AI model timeout is 60 seconds. If an AI call is synchronous within a normal API request, the outer request may expire first. The requirement does not specify whether AI endpoints have a separate end-to-end budget or are asynchronous. | **Important.** This may be a valid layered configuration, but the user-visible timeout/failure behavior cannot be concluded without clarifying the relationship. |
| A-08 | FR-EV-06 and proposed evaluation-target table; section 17 | The targets are “not formal release gates” in the unapproved draft and require later Human Requirement Approval for formal gate status. It is unclear whether approving v1.1 would itself convert these proposals into gates, despite the supplied decision to include them only as proposals. Measurement denominators and scoring procedures are also incomplete; “100% of outputs accepted by the application are schema-valid” does not by itself state how rejected/retried invalid outputs are measured. | **Important.** Avoids silently promoting proposals to release gates and ensures metrics are meaningful and reproducible. |
| A-09 | FR-ID-08 | “Appropriate local password-reset functionality” does not specify the required account recovery flow or policy constraints. | **Important**, although standard Identity configuration may be selected in technical planning if product behavior is explicitly delegated there. |

## 6. Conflicts

No definite contradictory business rules were identified in the reviewed v1.1 text or supplied decisions. A-07 is a potential operational timing conflict, not a proven contradiction: separate request/model timers could be intentional if the user-visible API behavior is defined.

## 7. Missing / incomplete information

The material omissions are captured in A-01..A-09. In particular:

- The initial RBAC matrix and change-protection rules are not enumerated.
- Team membership and tenant-scoped team data ownership are not defined.
- Ticket workflow transitions and additional Tenant Admin permissions remain open by explicit requirement text.
- Customer lookup fields, knowledge approval, and data-retention coverage beyond the named records are incomplete.
- The target metric gates/measurement and the 30s/60s timeout relationship need explicit semantics.
- Model IDs/region, token caps and monetary budget remain deliberately deferred to a technical decision gate before implementation; this is not reopened as a requirement-analysis blocker.

## 8. Assumptions

No unresolved business rule was silently selected. This analysis treats:

1. version 1.1 and all proposed defaults/targets as an unapproved draft, not an approved source;
2. the supplied update decisions as authorized clarifications for the draft, not Human Requirement Approval;
3. “approved knowledge” as a required eligibility condition without inferring how approval is granted; and
4. an unlisted role/action as restricted until explicitly established, consistent with v1.1.

Each item is an interpretation of the recorded status or explicit wording, not a new product requirement. The technical options in A-07 and A-09 are not selected here.

## 9. Technical and architectural impact

- **API/application:** The backend needs a complete, centrally enforced role/resource/action contract; user-visible authorization denials; bounded AI call behavior; and explicit typed customer lookup responses. No API design or implementation is selected in this analysis.
- **Domain/data:** Knowledge approval, team membership, ticket transitions, Tenant Admin actions, customer field minimization, and retention/deactivation semantics affect domain state and persistence. These cannot be safely filled in by implementation assumptions.
- **AI/search:** Retrieval needs an unambiguous approved-document eligibility rule; evaluation requires reproducible scoring and explicit proposal/gate status. Azure model and region remain a later technical decision.
- **Frontend/admin:** The administration console depends on the agreed permission matrix and safe configuration-change boundaries; status/action controls must match the approved ticket workflow.
- **Security/privacy:** Self-elevation prevention, team/tenant scoping, customer field minimization, audit read access, retention/deletion, account recovery, and denied-path tests require explicit behavior.
- **Testing:** Derive role/action negative tests, team-boundary and cross-tenant tests, transition tests, document approval/retrieval tests, data deletion/retention tests, and evaluation metrics from resolved decisions.
- **Operations/performance:** Reconcile general/API/model timeout behavior and define policy bounds before implementation; numeric model limits/budget remain at the explicitly deferred technical decision gate.

## 10. Questions requiring human decision

1. **Knowledge approval:** Does an authorized upload become eligible for search once indexed, or must a designated person approve it first? If approval is required, who can approve/reject, what is the status flow, and does reprocessing or a new version require re-approval?
2. **RBAC and Platform Admin safeguards:** Please define the initial resource/action permissions for each of the four roles (including Tenant Admin ticket actions and Support Manager team actions). Which Platform Admin permission-matrix changes are permitted, and how should changes that could elevate the acting administrator or alter Platform Admin access be prevented or reviewed?
3. **Support teams:** How are teams created and assigned to agents/managers, who manages membership, and do managers see only tickets assigned to their team or also unassigned tickets?
4. **Ticket workflow:** What status transitions and guards are allowed, including resolution/closure/reopening and escalation? Which ticket actions, if any, may Tenant Admin perform beyond view/oversight?
5. **Customer Lookup:** Which exact customer fields may the tool return, and which related-ticket fields/history are allowed for each role?
6. **Retention and audit:** What retention/deletion rules apply to tickets, customer data, users, feedback, ticket activity, and ticket AI results? How long are audit records retained, which roles may read them, and what should tenant/user deactivation or tenant deletion do to associated data?
7. **Timeouts:** Should AI requests have a separate end-to-end API timeout of at least the 60-second model timeout, or should the model timeout be reduced to fit within the 30-second general API timeout? If neither, should AI work be asynchronous with a separately defined client wait/status behavior?
8. **Evaluation proposals:** Should the listed targets remain non-gating proposals even after Human Requirement Approval unless a separate explicit decision makes them gates? For reproducibility, what denominator/scoring process should define grounded-answer and citation precision, and should schema tests also record invalid raw outputs rejected/retried rather than only accepted outputs?
9. **Local account recovery:** Is ASP.NET Core Identity’s configured reset flow sufficient, or are specific password/reset-token, lockout, and recovery requirements expected for this demonstrable release?

## 11. Analysis conclusion

- **Requirement analysis outcome:** Complete post-update analysis; decisions remain required.
- **Human decisions incorporated:** The update decisions listed in section 3 are reflected as draft clarifications, without claiming Requirement Approval.
- **Blocking decisions:** A-01 through A-06 materially affect access, workflow, privacy, data retention, or security behavior and should be resolved before complete Requirement Analysis Verification. A-07 through A-09 also require resolution or explicit bounded treatment before the affected requirements are finalized.
- **Ready for complete Requirement Analysis Verification:** **No.** Material behavior remains unspecified. Do not start verification against this incomplete decision set.
- **Next step:** Obtain the human decisions above. If they require changing version 1.1, initiate the separate Requirement Update process; then refresh analysis against the resulting version. A separate fresh Requirement Analysis Verification start is required only when the complete analysis and requirement are ready. Human Requirement Approval remains a later, distinct gate.

This analysis is not Requirement Analysis Verification, Requirement Approval, implementation planning, or authorization to implement.
