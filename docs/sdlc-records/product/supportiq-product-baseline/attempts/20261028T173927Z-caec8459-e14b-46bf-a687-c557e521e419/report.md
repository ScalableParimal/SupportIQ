# Requirement Analysis — SupportIQ Product Baseline

- **Work ID:** `supportiq-product-baseline`
- **Attempt:** `20261028T173927Z-caec8459-e14b-46bf-a687-c557e521e419`
- **Outcome:** Analysis complete; material human decisions remain unresolved.
- **Authority:** Requirement Analysis only. This report is not Requirement Approval, Requirement Analysis Verification, implementation authorization, or Acceptance.

## Source, invocation, and traceability basis

The complete authoritative source analyzed was `docs/requirement/SupportIQ_Product_Requirements_Document.docx` (SHA-256 `EE752A1B0541EAC55027A3A61CB5485996CB3BD5484E4CE4348B8829DE5CF7FA`). The DOCX body (136 paragraphs, 21 tables), header, and footer were read. It contains Document Control, sections 1–18, and Appendices A–B. There are no supplied human product/business decisions. The source itself labels its status “Draft baseline; assumptions should be validated before implementation.”

**Page traceability limitation:** The DOCX has one explicit page break after the title/cover and no saved rendered-page-break markers. Therefore actual page numbers beyond the cover cannot reliably be recovered from this source in this environment. To avoid inventing page numbers, findings cite the PRD section/subsection, heading, requirement/table ID, and a short text anchor; “page unavailable” means the source file does not establish a reliable printed page number.

Process-initiation record: the actual wording `initiate_exact_scope`, reported as the initiating human’s separate interactive response in the current request, available at `2026-10-28T23:09:55.119+05:30` (`2026-10-28T17:39:55.119Z`). Its scope is Process Initiation only and it is not a formal Human Approval. Record-scope authorization is limited to this actor’s records under this attempt directory. Neither is a product decision. The adopted product records root and predecessor applicability are bound in `attempt.json` and `result.json`.

### 1. Understanding

**Business objective.** SupportIQ is a learning-oriented, production-minded support portal for fictional B2B SaaS provider CloudDesk. It aims to help agents find approved information, draft grounded responses, summarize/classify tickets, and detect insufficient evidence while leaving customer-facing decisions and communications to humans (PRD §1, “AI outputs are assistive”). The described build is a learning/portfolio project, not a commitment to production readiness (§16).

**Actors.** Tenant Admin, Support Agent, Support Manager, and Platform Admin (PRD §3). Authorization is enforced by APIs, not only UI controls; demo roles may be seeded but the role model must be explicit and testable.

**Main functionality.** Tenant-aware knowledge ingestion/lifecycle and search; RAG chat with citations, abstention and feedback; ticket summary/classification; human-reviewed agent drafts; constrained tool use; basic scoped analytics; evaluation/operations; tests, CI, telemetry, documentation and Azure deployment (PRD §§2, 4–14).

### 2. Explicit requirements

The following are source requirements, not analysis recommendations:

- **Objectives and evidence (§2):** reduce search/reply effort with impact measured in a later pilot; provide source-traceable answers and abstain when evidence is insufficient; demonstrate the stated .NET/React/Azure stack; establish tests for retrieval, answer quality, citations, structured outputs, tenant isolation and APIs; deploy a demonstrable app with setup, CI, monitoring and cost controls. Initial evaluation targets are at least 50 question/source pairs, 10 no-answer questions and 10 prompt-injection cases. Lifecycle, ticket, grounding, quality, security and reproducibility measures are also listed in the “Initial target / evidence” table.
- **Knowledge assistant (FR-CA-01–08, §5.1):** natural-language conversations; retrieval restricted to knowledge the current user may access; grounded responses with source title and excerpt/section where available; clear no-answer response for insufficient evidence (escalation may be suggested); recent context without tenant/access crossover; positive/negative feedback with optional reason; role-permitted history; English initially with later-language extensibility.
- **Knowledge management (FR-KB-01–08, §5.2):** PDF/DOCX/TXT upload; reject unsupported or oversized content clearly; validate extension, content type, size and processing outcome; register tenant/uploader/timestamps/version/status; extract, normalize, chunk (configurable), embed and index; display Uploaded/Processing/Indexed/Failed and deletion statuses; authorize update/reprocess and prevent stale index results; deletion makes content and derived chunks unavailable; identify source and, where feasible, page/section in results/citations.
- **Ticket intelligence (FR-TK-01–07, §5.3):** synthetic-data ticket list/detail; concise summaries; configurable categories/priorities with structured output; sentiment/urgency presented as AI suggestions; supported queue/escalation suggestions; agent edit/override with final human-approved value and original suggestion retained where appropriate; safely handle invalid model output.
- **Agent copilot (FR-AC-01–07, §5.4):** suggested replies for selected tickets, sourced knowledge recommendations, authorized customer context, supported next-step suggestions, editable/copyable/discardable/regenerable draft, no automatic customer message in release one, and distinction between internal notes and customer-facing draft.
- **Workflow tools (FR-WF-01–06, §5.5):** small allowlist (examples: knowledge search and read-only ticket/customer lookup); typed I/O, authorization, timeout and error handling; no arbitrary SQL, shell or unrestricted network execution; explicit human confirmation for business-data changes (write actions may be deferred); auditable calls/outcomes/actor/tenant/correlation IDs; safe tool-failure messages.
- **Analytics (FR-AN-01–05, §5.6):** authorized counts by ticket status/category/priority; trends/SLA indicators only where sample fields permit; limited natural-language questions mapped to predefined allowlisted analytics; state data scope and time range; arbitrary text-to-SQL is out of scope, and any later exploration is constrained as specified.
- **Evaluation/operations (FR-EV-01–06, §5.7; FR-OP-01–08, §5.8):** versioned evaluation data and expected sources/answer traits; record retrieval/answer/citation/latency/model/deployment/prompt data; assess relevance, grounding, citation correctness and abstention; compare changes to a baseline; test ambiguous/missing/conflicting knowledge, prompt injection and cross-tenant access; results are decision support, not proof, and thresholds/limitations are documented. Enforce tenant and role boundaries, managed secrets/no committed secrets, useful but minimized/configurable logs, limits/rates/timeouts/graceful failures, approximate usage/cost tracking where provider metadata allows, and repeatable CI/CD deployment/configuration.
- **Workflows (§6):** sign-in/workspace selection through validated, tenant-scoped retrieval and grounded answer/feedback; authorized upload through processing/indexing/failure with stale chunks disabled on replacement/deletion; agent review of ticket AI results/drafts, with a separate explicit human action before any customer message is sent.
- **Architecture/data/API (§§7–9):** stated React + TypeScript, .NET 8 API, Azure model endpoint/Search/Blob/SQL, background worker or Functions, Key Vault, Application Insights and GitHub Actions baseline. API mediates model/search access; browser receives no provider keys/unrestricted credentials. Listed entities and endpoint names are illustrative, not finalized schemas/contracts. The PRD says final contracts should define schemas, validation, status/error responses, idempotency where needed and OpenAPI documentation.
- **Non-functional and guardrails (§§10–11):** HTTPS, server-side authorization/least privilege, synthetic data, documented retention/deletion, resilient retries, pagination/asynchronous ingestion, accessibility, correlated observability with privacy minimization, budget/usage caps and teardown documentation, practical provider abstraction; ground in approved knowledge, cite rather than fabricate, abstain for missing/conflicting/stale/insufficient evidence, treat source content as untrusted data, constrain tools, require human review for drafts/actions, validate structured output, version prompts/evaluations and label AI outputs provisional/editable.
- **Dataset, acceptance and test strategy (§§12–14):** suggested seed volumes include 20 knowledge articles, 100 synthetic tickets, 5 fictional organizations, 10 agents, 50 question/source pairs, 10 no-answer questions and 10 injection cases. Fabricated content only; no real customer data or secrets in prompts/logs/fixtures/screenshots. The acceptance criteria require lifecycle/status, citation/no-answer, direct-API tenant isolation, schema-safe ticket outputs, editable non-sending drafts, constrained/audited tools, PR CI, secret-free documented setup/deployment and repeatable evaluation runs. Tests span unit, integration, API, AI evaluation, end-to-end and operational cases.
- **Delivery and completion (§§15–18; appendices):** issue/PR-linked small changes, developer ownership of architecture/security, tests and human review; suggested 30-day weekly delivery outcomes, not a production-readiness commitment; Definition of Done checklist; Appendix A is recommended backlog, Appendix B glossary.

### 3. Business rules and constraints

**Explicit rules:** tenant boundaries apply on every data path; API-side authorization is required; responses must be grounded and source-traceable, and abstain when evidence is insufficient/missing/conflicting/stale; AI classifications/sentiment are provisional and editable; model-provided source content is untrusted data; only allowlisted, authorized, bounded tools may run; arbitrary SQL/shell/unrestricted networking is prohibited; customer messages are never automatically sent in release one; business-data changes require explicit human confirmation; invalid structured output must not corrupt data; deletion must make source content and derived chunks unavailable; data and demo fixtures are synthetic; secrets are protected and not committed; evaluation results are decision support rather than proof.

**Explicit technical constraints/baseline:** React/TypeScript, .NET 8, named Azure service categories, API mediation of AI/search credentials, CI/PR checks and documented configuration/deployment. These source choices are not inferred recommendations. Latency guarantees are expressly deferred until baselines are established (PRD §10).

### 4. Scope

**In scope:** first demonstrable release features in PRD §4.1; listed functional modules, roles, synthetic data, test strategy, CI/telemetry, and demonstrable Azure deployment.

**Explicitly out of scope/deferred (§4.2, §5.6):** advanced natural-language analytics/arbitrary text-to-SQL; autonomous multi-agent orchestration or unsupervised customer communication; production external ticketing/CRM/email/messaging integrations; enterprise SSO, billing, multi-region DR and compliance certifications; large-scale benchmarking, custom fine-tuning, automated model selection; arbitrary text-to-SQL. Production readiness is not promised (§16).

**Undecided/deferred:** authentication provider; exact role/resource/action permissions; knowledge approval/currentness and retention/deletion policy; upload size limits; model/embedding deployment; ticket taxonomy and routing; evaluation pass thresholds and status of sample counts as acceptance minima; whether release-one tools may include write actions; ticket population method. These are not silently included or resolved here.

### 5. Ambiguities and important gaps

All locations are in the PRD; printed page is unavailable as explained above.

| ID / importance | Traceable PRD anchor | Ambiguity / impact |
|---|---|---|
| A-01 **Blocking** | §3 (“Authentication-ready structure”; API-enforced roles); §17 open question “Which authentication provider is used for the demo?” | Local auth vs Microsoft Entra ID is unresolved. Identity affects tenant membership, API authorization, setup, testing and deployment; no provider will be selected by this analysis. |
| A-02 **Blocking** | §3 role access summary; FR-OP-02; FR-KB-01/06/07; FR-CA-07; §17 | “Permitted,” “where authorized,” and “privileged operational access” do not define role-to-action/resource boundaries, including Platform Admin’s tenant scope, knowledge management, ticket access/assignment, history and feedback. Missing authorization policy is a direct safety/security gap. |
| A-03 **Blocking for safe knowledge behavior** | FR-CA-03/04; FR-KB-05/06/08; §11 (“approved retrieved knowledge”; stale/conflicting evidence) | Lifecycle statuses do not include an explicit approval/currentness state or define who approves, what is searchable, how “stale” is determined, or how conflicts are adjudicated. The core grounding/abstention rule therefore lacks an operational business condition. |
| A-04 **Blocking for lifecycle requirements** | FR-KB-01/02/06/07; §10 Privacy; §17 open question “file-size limits and retention periods” | No maximum size or retention duration. “Deletion statuses” and “make content and derived chunks unavailable” do not define treatment of originals, chunks/index records, backups, logs, failed processing or deletion confirmation. Upload acceptance and privacy/deletion behavior cannot be finalized without a decision. |
| A-05 **Important** | FR-TK-03/05; §3 Support Manager; §17 | “Configurable” categories/priorities and queue/escalation recommendations lack values, configuration authority, rules and fallback. This affects classification, routing, UI and acceptance tests. |
| A-06 **Important** | Document Control technology baseline; §§7, 17 (“Which model and embedding deployment...”) | Azure model/embedding deployment, region/availability, dimensions, quotas, pricing and index compatibility are not selected/confirmed. This affects feasibility, cost and integration-specific contracts. |
| A-07 **Important** | §2 “Initial target / evidence”; FR-EV-01/03/04/06; §12 “Suggested volume”; §13 | Counts and targets are listed, but the relation between target and suggested volume is unclear; no quality/pass thresholds are specified despite FR-EV-06 requiring documented thresholds. Without confirmation, evaluation is measurable but not a pass/fail acceptance gate. |
| A-08 **Important for workflow scope** | §4.1 read-only lookup tools; FR-WF-04; FR-AC-06; §6.3 | Read-only tools are examples/current scope, while FR-WF-04 permits business-data changes after confirmation and says write actions “may be deferred.” It is unclear whether any write action belongs in release one; no write action is added here. |
| A-09 **Minor / useful** | §17 “How will tickets be populated?” | A deterministic synthetic seed script is preferred, not decided. This affects reproducibility and fixtures, but does not block unrelated requirement clarification. |

### 6. Conflicts

No direct contradictory statements were found in the complete PRD. The following are gaps/tensions, not asserted conflicts: “approved knowledge” is required but its approval state/workflow is absent (A-03); a read-only tool emphasis coexists with optional confirmed writes without defining release-one scope (A-08); and test/evaluation targets are present without pass thresholds (A-07). The rule that drafts remain human reviewed and are not automatically sent is consistent across §§1, 5.4, 6.3 and 11.

### 7. Missing or incomplete information

- Authentication and role/action policy (A-01/A-02).
- Knowledge approval/currentness, conflict/staleness handling, file limits, retention and deletion coverage (A-03/A-04).
- Ticket category/priority values and queue/escalation logic (A-05).
- Model and embedding deployment/capacity/cost selection (A-06).
- Evaluation acceptance thresholds and whether volumes are mandatory minima (A-07).
- First-release write-tool scope (A-08); synthetic seed approach (A-09).
- API contracts intentionally remain illustrative; schemas, validation, status/error behavior, idempotency and OpenAPI are still needed as PRD §9 states. This is an implementation-contract detail, not a contradiction.
- PRD §10 deliberately supplies no latency guarantee; it requires baselines before guarantees. This is a stated deferral, not an unrecognized commitment.

### 8. Assumptions

**PRD-stated assumptions (§17):** CloudDesk is fictional and demo data synthetic; Azure AI model and Search resources are available. The latter is not verified. The PRD’s stated risks—model error/overconfidence, cross-tenant leakage, complex parsing/indexing failures and cloud-cost overruns—are risks, not approved assumptions.

**Analysis assumptions:** None adopted. No unresolved identity, role, content-approval, retention, model, taxonomy, threshold or write-scope choice has been filled in.

### 9. Technical impact (analysis, not additional requirements)

- **API/service:** identity, tenant/role enforcement, upload/status/lifecycle, chat/citations/feedback, ticket AI, typed allowlisted tools, safe errors and illustrative endpoints require concrete contracts after decisions.
- **Application/UI:** role-appropriate administration, ingestion status, source citations/no-answer, ticket views, provisional AI labels, editable drafts, internal/customer-facing distinction, feedback and dashboards.
- **Domain/data:** tenant/user memberships, documents/versions/chunks, conversations/messages/citations, tickets/AI suggestions, feedback, tool audit and evaluation entities are logical candidates only; PRD §8 explicitly says they are not a finalized schema.
- **Infrastructure/integration:** storage, search/embeddings, model endpoint, background ingestion, SQL, secret management, observability and CI/CD are named in the baseline. Model/auth/region/quotas and deletion semantics remain dependencies.
- **Testing/security:** direct API tenant isolation, role matrix, invalid uploads/model outputs, stale/deleted indexes, no-answer/citations, prompt injection, tool restrictions, audit privacy, failures/retries and repeatable evaluation are needed to demonstrate stated criteria.
- **Performance/reliability/privacy:** pagination, asynchronous ingestion, safe retries/timeouts/throttling, correlation, content minimization, retention/deletion, budgets and teardown matter; no quantitative latency guarantee is currently specified.

No existing application source or runtime was evaluated; technical impacts above are derived only from the Requirement.

### 10. Questions requiring human decision

1. **Identity and authorization (blocking):** For the demo, choose local authentication or Microsoft Entra ID. For each of Tenant Admin, Support Agent, Support Manager and Platform Admin, specify permitted tenant/resource/actions (including user/content management, ticket/assignment, conversation/history, feedback and platform-wide access) and any cross-tenant operational access.
2. **Knowledge lifecycle and privacy (blocking):** Who can approve/publish knowledge, what makes it current/searchable, and how should conflicting or stale content be treated? Set accepted upload-size limits and retention periods; specify deletion coverage and expected completion/status for originals, extracted content, chunks/index, backups and logs.
3. **Ticket business rules (important):** What categories and priority values apply, who may configure them, and what queues/escalation reasons/rules should be suggested? If these remain demo-configurable, identify the allowed initial values and decision owner.
4. **AI deployment (important):** Which model and embedding deployments/regions are intended? Confirm availability, embedding dimensions/index compatibility, quotas and cost constraints, or explicitly leave deployment selection to a later governed technical decision.
5. **Evaluation acceptance (important):** Are §2 counts hard minimums or initial targets, and what thresholds/criteria determine a satisfactory evaluation for grounding, citations, abstention and retrieval? If not a release gate, state that explicitly.
6. **Tool write scope (important):** Are any business-data write tools in the first release, or are all first-release tools read-only? If writes are included, identify actions and confirmation/authorization rules; otherwise explicitly defer them.
7. **Ticket data (minor):** Confirm whether release-one ticket data should be generated by a deterministic synthetic seed script (the PRD’s preference) or another synthetic mechanism.

These questions are not answered by the process-initiation response. That response authorizes the process only and is not a product decision.

### 11. Analysis conclusion and handoff

- **Outcome:** Requirement Analysis completed against the complete PRD; source remains a draft baseline with unresolved items.
- **Human product/business decisions incorporated:** None.
- **Blocking decisions:** A-01 through A-04 / Questions 1–2. Important decisions remain A-05 through A-08 / Questions 3–6; A-09 / Question 7 is minor.
- **Ready for requirement finalization:** No, pending material decisions and resolution through the separately governed Requirement Update process.
- **Source ready for Requirement Analysis Verification:** **No—not as the finalized, decision-resolved requirement for the approval sequence.** The Guideline calls for the decisions, authorized Requirement Update and post-update analysis refresh before complete Requirement Analysis Verification. This analysis is the initial analysis output and may not be treated as verification.
- **Next governed path:** Human resolves the questions; only on a separate authorized request, Requirement Update applies decisions; Requirement Analysis is refreshed against the changed source; then independently initiated Requirement Analysis Verification may follow. Stop here.
- No Requirement Approval, Verification, implementation authorization, Acceptance, human-gate record, source update, plan, product code/test/configuration change, commit or push was created or claimed.
