**SupportIQ** 

AI-Powered Customer Support Knowledge Portal 

**Product Requirements Document (PRD)** 

*Version* *1.1 |* *November 2026 | Learning / portfolio project*

 

**Document Control** ****

| **Item**  | **Description**  |
| --- | --- |
| Product  | SupportIQ  |
| Business context  | A fictional B2B SaaS provider, CloudDesk, uses SupportIQ to help support agents find approved answers and handle customer tickets.  |
| Purpose  | Define product scope, functional and non-functional requirements, workflows, acceptance criteria, and delivery guidance for a 30-day demonstrable learning release.  |
| Audience  | Product owner, developer, AI engineer, QA, and technical reviewer.  |
| Status  | Updated draft; unapproved and pending subsequent Requirement Analysis, independent verification, and Human Requirement Approval.  |
| Technology baseline  | React + TypeScript, .NET 8 Web API with ASP.NET Core Identity local authentication, Azure AI model endpoints, Azure AI Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, GitHub Actions.  |

**Version lineage:** This unapproved version 1.1 is an Initial Analysis Clarification of the version 1.0 draft at `SupportIQ_Product_Requirement.md` (SHA-256 `ED2C910654FA39BE995D716F063C45BFE4183D8A4E8C6CB5B1C1194F8C17A871`). Version 1.0 remains preserved and unchanged. Clarification decisions do not constitute Human Requirement Approval.
 

**1. Executive Summary** ****

SupportIQ is a learning-oriented, production-minded AI customer support portal. It combines tenant-aware identity and administration, a knowledge base, retrieval-augmented generation (RAG), complete core ticket management, ticket intelligence, agent assistance, bounded workflow tools, analytics, evaluation, and operational controls.

The system helps agents locate approved information, manage support tickets, draft grounded responses, summarize and classify tickets, and recognize when evidence is insufficient. AI outputs are assistive: a human remains responsible for customer-facing decisions and communications. The first release includes a tenant/user administration console and configurable security, retention, and operational controls. It remains a demonstrable learning release, not a production-readiness commitment.

**2. Goals and Success Measures** ****

- Reduce time spent searching documentation and composing routine replies; measure impact in a later pilot rather than assume improvement. 

- Provide answers with traceable source references and abstain when evidence is insufficient. 

- Demonstrate an end-to-end AI application using .NET, React, Azure services, and GitHub Copilot-assisted development. 

- Establish repeatable tests for retrieval, answer quality, citations, structured outputs, tenant isolation, and core APIs. 

- Deploy a demonstrable application with documented setup, CI checks, monitoring, and cost controls. 

| **Measure**  | **Initial target / evidence**  |
| --- | --- |
| RAG evaluation set  | At least 50 question/source pairs, 10 no-answer questions, and 10 prompt-injection cases.  |
| Knowledge lifecycle  | Upload, process, index, search, update/reindex, and delete a document with visible status.  |
| Ticket intelligence  | Classification and summary return schema-valid output; agents can edit or override.  |
| Grounding  | Assistant responses show sources; unsupported questions trigger a clear no-answer response.  |
| Quality gates  | Automated unit/integration tests and CI checks run on pull requests.  |
| Security  | Tests demonstrate tenant isolation for representative API and retrieval paths.  |
| Reproducibility  | A new developer can follow the README to configure, run, test, and deploy.  |
 

**3. Users and Roles** ****

| **Role**  | **Responsibilities**  | **Access summary**  |
| --- | --- | --- |
| Tenant Admin  | Manage users and knowledge sources for their tenant; oversee tenant tickets.  | Manage tenant users and content; view authorized tenant ticket data.  |
| Support Agent  | Create and work permitted tickets; search knowledge; use AI suggestions; submit feedback.  | Perform authorized ticket actions and review or edit AI suggestions; cannot manage users, grant administrative roles, or delete knowledge documents.  |
| Support Manager  | Manage team tickets, assignments, escalations, and team analytics.  | Perform authorized team-level ticket and analytics actions within their tenant.  |
| Platform Admin  | Manage tenants and users across tenants, initial tenant administrators, global permissions/configuration, and platform operations.  | Privileged access is minimized, least-privilege, and audited.  |
 

Use ASP.NET Core Identity with local authentication for the first demonstrable release. Microsoft Entra ID and enterprise SSO are deferred. Platform Admin creates tenants and provisions the initial Tenant Admin account. Tenant Admin manages users in their tenant and assigns only predefined permitted roles. Self-registration is disabled; demo users and roles may be seeded through a controlled setup process.

Implement a centralized, explicit, testable resource/action permission matrix for the four predefined roles. Platform Admin may manage system-wide mappings but may not create arbitrary custom roles or tenant-specific permission overrides. Tenant Admin may assign predefined roles but cannot change global permission definitions or grant additional administrative privileges. Support Manager and Support Agent cannot manage RBAC configuration. Provide an administrative view of the permission matrix and audit role/permission changes. Enforce all permissions in backend APIs and data access, prevent privilege escalation, and test denied cross-tenant access. Tenant Admin ticket oversight and any action not explicitly assigned in this document remain subject to the permission matrix and must be resolved before the affected capability is finalized.

**4. Scope** ****

**4.1 Mandatory First Demonstrable Release Scope** ****

The 30-day boundary is a target, not a fixed weekly schedule or guarantee. Organize the approved scope into independently implementable and testable modules; implementation order, dependencies, task breakdown, capacity, and milestones are decided separately during Implementation Planning. Prioritize security, administration, core ticket management, knowledge-to-RAG, AI assistance, and mandatory acceptance tests. Defer optional features if necessary to preserve these capabilities.

- Identity and Access Management: local authentication; tenant and user administration; four predefined roles; centralized resource/action RBAC and audit.
- Administrative Configuration: configurable operational limits, retention/deletion policies, system settings, validation, version history, and audit.
- Knowledge Management: supported-file upload (20 MB initial maximum), validation, extraction, chunking, embeddings, indexing, reprocessing, lifecycle status, tenant-authorized retrieval, and deletion.
- Ticket Management: create, list, view, edit, assign/reassign, search/filter/sort/page, change authorized status/category/priority, escalate, resolve, close, reopen through authorized transitions, and retain activity history.
- AI Ticket Intelligence and Agent Copilot: summaries, category/priority/sentiment/urgency suggestions, knowledge recommendations, troubleshooting suggestions, and editable customer-reply drafts requiring human review.
- AI Customer Assistant: RAG chat, authorized retrieval, citations, abstention, 10-turn conversation context, history, and feedback.
- Tools and Analytics: explicitly allowlisted, read-only knowledge/ticket/customer lookup, ticket summary/classification, and predefined tenant-scoped analytics.
- Audit and Monitoring: administrative, configuration, ticket, and tool activity; application telemetry and approximate AI usage/cost monitoring.
- Evaluation and Quality Assurance: unit, integration, API, end-to-end, operational, security, tenant-isolation, prompt-injection, and AI evaluation tests.
- Repeatable CI, documentation, and Azure deployment for the demonstrable release.

**4.2 Deferred / Optional** ****

- Advanced natural-language analytics and arbitrary text-to-SQL. 

- Complex autonomous multi-agent orchestration or unsupervised customer communication. 

- Production integrations with external ticketing, CRM, email, or messaging platforms. 

- Billing, multi-region disaster recovery, and compliance certifications. 

- Large-scale benchmarking, custom fine-tuning, and automated model selection. 
- Microsoft Entra ID and enterprise SSO.
- Internal notes and their visibility/persistence workflows.
- AI-invoked write tools or autonomous business-data modifications.
- Arbitrary custom roles and tenant-specific permission overrides.
- SLA indicators until definitions, business calendars, time zones, and required fields are established.

**5. Product Modules and Functional Requirements** ****

**5.1 AI Customer Assistant** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-CA-01  | Users can start a conversation and submit a natural-language question.  |
| FR-CA-02  | Retrieval returns only knowledge the current user is authorized to access.  |
| FR-CA-03  | Responses are grounded in retrieved content and display source title plus excerpt or section reference where available.  |
| FR-CA-04  | If evidence is insufficient, the assistant states it cannot answer from available knowledge and may suggest escalation.  |
| FR-CA-05  | The most recent 10 conversation turns may be used as context without crossing tenant or access boundaries.  |
| FR-CA-06  | Users can provide positive/negative feedback and an optional reason.  |
| FR-CA-07  | Users can view only conversation history permitted by their role.  |
| FR-CA-08  | English is supported initially; the design should allow additional languages later.  |
 

**5.2 Knowledge Base Management** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-KB-01  | Authorized users can upload PDF, DOCX, and TXT files up to the configurable 20 MB initial maximum; unsupported, corrupted, or oversized files are rejected clearly.  |
| FR-KB-02  | Validate extension, content type, size, and processing outcome; do not trust filename alone.  |
| FR-KB-03  | Store originals and register tenant, uploader, timestamps, version, and processing status.  |
| FR-KB-04  | Extract and normalize text, split into configurable chunks, generate embeddings, and index chunks.  |
| FR-KB-05  | Show Uploaded, Processing, Indexed, Failed, and deletion statuses.  |
| FR-KB-06  | Authorized users can update or reprocess a document; stale index entries must not remain searchable.  |
| FR-KB-07  | Authorized users can delete a document and make its content and derived chunks unavailable.  |
| FR-KB-08  | Search results and citations identify the source document and, where feasible, page/section.  |
 

**5.3 AI Ticket Management** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-TK-01  | Agents can view a ticket list and detail view using synthetic demo data.  |
| FR-TK-02  | Generate a concise summary from ticket content.  |
| FR-TK-03  | Classify tickets into configurable categories and priorities using structured output.  |
| FR-TK-04  | Sentiment or urgency is labeled as an AI suggestion, not a fact.  |
| FR-TK-05  | Recommend a queue or escalation reason where supported by rules and available information.  |
| FR-TK-06  | Agents can edit/override suggestions; retain the final human-approved value and, where appropriate, the original suggestion.  |
| FR-TK-07  | Invalid model output is handled safely and does not corrupt ticket data.  |
 

**5.4 AI Agent Copilot** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-AC-01  | Agents can request a suggested customer reply for a selected ticket.  |
| FR-AC-02  | Recommend relevant knowledge articles and show their sources.  |
| FR-AC-03  | Summarize customer context from authorized available records.  |
| FR-AC-04  | Suggest next steps or troubleshooting checks when supported by approved knowledge.  |
| FR-AC-05  | Agents can edit, copy, discard, or regenerate a draft.  |
| FR-AC-06  | The first release must not send customer-facing messages automatically.  |
| FR-AC-07  | Internal notes and their visibility/persistence workflows are out of scope for the first release.  |
 

**5.5 AI Workflow Automation** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-WF-01  | The assistant can invoke only the explicitly allowlisted, read-only knowledge search, ticket lookup, customer lookup, ticket summary, ticket classification, and analytics functions defined in this section and FR-AN-03.  |
| FR-WF-02  | Each tool has typed input/output, authorization checks, timeout, and error handling.  |
| FR-WF-03  | The model cannot execute arbitrary SQL, shell commands, or unrestricted network requests.  |
| FR-WF-04  | The first release exposes no AI-invoked write tools. Any future business-data modification tool requires explicit human confirmation, server-side authorization, validation, and audit logging.  |
| FR-WF-05  | Record tool name, actor, tenant, outcome, timestamp, and correlation identifier in an audit trail.  |
| FR-WF-06  | Tool failures are communicated without exposing secrets or stack traces.  |
 

**First-Release Tool Allowlist** ****

The only AI-invoked tools in the first release are:

1. **Knowledge Search:** Search approved, tenant-authorized knowledge and return source references.
2. **Ticket Lookup:** Read authorized ticket details, status, category, priority, and assignment.
3. **Customer Lookup:** Read only necessary customer information and authorized related ticket history from the synthetic demo dataset.
4. **Ticket Summary:** Generate a summary from authorized ticket content without modifying the ticket.
5. **Ticket Classification:** Suggest category, priority, sentiment, and urgency without modifying the ticket.

All tools are non-mutating and read-only with typed schemas, backend authorization, tenant scope, validation, timeouts, rate limits, safe errors, and audit records. No AI-invoked ticket assignment, status change, customer-data update, knowledge deletion, or customer communication is permitted. Future write tools require a separately governed decision and explicit human confirmation.

**First-Release Analytics Allowlist** ****

- Ticket counts grouped by status, category, or priority.
- Ticket-volume trends over predefined 7-day and 30-day ranges.
- Basic dashboards scoped by tenant and role.
- Analytics are predefined, read-only, tenant-scoped, and identify their data scope and time range. SLA indicators are deferred as stated in FR-AN-02.

**Role-based tool access:** Platform Admin has audited, minimized platform operational access. Tenant Admin can perform read-only customer/ticket lookup and knowledge search within their tenant. Support Manager can use team-level customer/ticket lookup, knowledge search, and authorized team analytics. Support Agent can look up permitted tickets/customers, search knowledge, and request summaries/classifications for authorized tickets. Enforce all permissions server-side. The permission matrix is centrally managed by Platform Admin; no custom roles or tenant overrides are supported.

**5.6 AI Support Analytics** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-AN-01  | Provide a basic dashboard for ticket counts by status, category, and priority, scoped to authorized data.  |
| FR-AN-02  | Show ticket-volume trends for predefined 7-day and 30-day ranges. SLA indicators are deferred until definitions, business calendars, time zones, and required fields are established.  |
| FR-AN-03  | Support a small set of natural-language questions through predefined allowlisted analytics functions.  |
| FR-AN-04  | Summaries identify their data scope and time range.  |
| FR-AN-05  | Arbitrary text-to-SQL is out of scope; any later exploration requires read-only access, validation, row limits, and tenant scoping.  |
 

**5.7 AI Evaluation and Testing** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-EV-01  | Include a versioned evaluation set with expected source documents and answer characteristics.  |
| FR-EV-02  | Record retrieval, answer, citations, latency, model/deployment, and prompt version for each run.  |
| FR-EV-03  | Assess retrieval relevance, grounding, citation correctness, and no-answer behavior.  |
| FR-EV-04  | Compare prompt/model changes against a baseline run.  |
| FR-EV-05  | Include ambiguous questions, missing/conflicting knowledge, prompt injection, and cross-tenant access tests.  |
| FR-EV-06  | Treat evaluation results as decision support, not proof of correctness; document thresholds and limitations.  |
 
The following are **proposed initial evaluation targets**, not formal release gates in this unapproved draft. They must not be treated as formal release gates until the Requirement receives subsequent Human Requirement Approval:

| Evaluation area | Proposed initial target | Measurement / limit |
| --- | --- | --- |
| Retrieval quality | Recall@5 >= 80% | At least 80% of expected relevant source documents appear in the top five results. |
| Grounding | Grounded Answer Rate >= 90% | Substantive factual claims are supported by retrieved, authorized knowledge; unsupported claims are not stated as facts. |
| Citation correctness | Citation Precision >= 95% | Citations refer to valid retrieved sources and relevant content; fabricated citations are prohibited. |
| Abstention | 100% correct on the initial 10 no-answer cases | Missing, conflicting, stale, or insufficient evidence produces a clear no-answer response without fabricated citations. |
| Structured output | 100% of outputs accepted by the application are schema-valid | Invalid output is rejected or safely retried and cannot corrupt persisted data. |
| Prompt-injection handling | 100% safe handling of the initial 10 cases | No unauthorized tool execution, cross-tenant disclosure, secret exposure, or policy bypass. |

Cross-tenant access denial is a mandatory acceptance criterion independent of the proposed percentages: any successful unauthorized cross-tenant access fails acceptance. The initial evaluation sets are small and do not establish production-level accuracy or security assurance. Record baseline runs, model/deployment and prompt versions, results, limitations, and failures; rerun after material model, prompt, retrieval, or configuration changes. Numeric cost budgets and model-specific token limits remain deferred.

**5.8 Security and AI Operations** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-OP-01  | Associate application data with a tenant and enforce tenant scope on every read/write path.  |
| FR-OP-02  | Enforce role-based access on APIs and relevant UI actions.  |
| FR-OP-03  | Store secrets in a managed secret store; never commit them to source control.  |
| FR-OP-04  | Record errors, latency, model usage where available, and correlation IDs.  |
| FR-OP-05  | Avoid unnecessary sensitive content in logs; make retention/redaction configurable.  |
| FR-OP-06  | Apply request limits, rate limits, timeouts, and graceful handling of model/search failures.  |
| FR-OP-07  | Track approximate AI usage/cost by feature or tenant where provider metadata permits.  |
| FR-OP-08  | Document repeatable deployment and configuration through CI/CD.  |
 

**5.9 Identity and Administrative Management** ****

| ID | Requirement |
| --- | --- |
| FR-ID-01 | Authenticate users locally using ASP.NET Core Identity. Microsoft Entra ID and enterprise SSO are deferred. |
| FR-ID-02 | Platform Admin can create, view, update, activate, and deactivate tenants and provision the initial Tenant Admin account for each tenant. |
| FR-ID-03 | Platform Admin can manage users across tenants. Tenant Admin can create, view, edit, activate, and deactivate users within their tenant and assign/change only permitted predefined roles. Self-registration is disabled. |
| FR-ID-04 | Implement predefined Platform Admin, Tenant Admin, Support Manager, and Support Agent roles through a centralized, explicit, resource/action permission matrix. |
| FR-ID-05 | Platform Admin can manage system-wide mappings for the predefined roles and view the permission matrix. Tenant Admin cannot modify global permissions or grant additional administrative privileges. Support Manager and Support Agent cannot manage RBAC configuration. |
| FR-ID-06 | Prevent privilege escalation and enforce tenant and role authorization on every relevant backend API and data-access path. |
| FR-ID-07 | Audit tenant administration, user creation/activation/deactivation, role changes, and permission-matrix changes. |
| FR-ID-08 | Provide appropriate local password-reset functionality and a controlled setup path for seeded demo users and roles. |
| FR-ID-09 | Minimize and audit Platform Admin access to tenant data. |

Tenant Admin manages knowledge documents in their own tenant and has tenant-level ticket visibility/administrative oversight subject to the permission matrix. Support Manager can manage authorized team tickets, assignments, and escalations. Support Agent can work permitted tickets, use knowledge/RAG, submit feedback, and create/edit AI suggestions, but cannot manage users, assign administrative roles, or delete knowledge documents. Any unlisted role/action combination must be explicitly restricted until its permission is established.

**5.10 Core Ticket Management** ****

| ID | Requirement |
| --- | --- |
| FR-TM-01 | Provide a complete internal ticket lifecycle over synthetic demo data: create, list, view details, edit authorized ticket information, assign/reassign, update authorized status/category/priority, escalate, resolve, close, and reopen through authorized workflow transitions. |
| FR-TM-02 | Support search, filtering, sorting, and pagination for ticket lists. |
| FR-TM-03 | Scope ticket ownership, visibility, and actions by tenant and role; enforce permissions at the API. |
| FR-TM-04 | Record ticket activity history and audit creation, assignment/reassignment, status changes, and administrative actions. |
| FR-TM-05 | Use configurable proposed initial statuses Open, In Progress, Pending, Resolved, and Closed; categories Account & Access, Billing & Payments, Technical Issues, Product Setup, and General Support; and priorities Critical, High, Medium, and Low. |
| FR-TM-06 | Use these proposed category-based default queue recommendations: Account & Access to Account & Access Queue; Billing & Payments to Billing Queue; Technical Issues to Technical Support Queue; Product Setup to Product Setup Queue; and General Support to General Support Queue. Queue assignment and escalation are subject to authorization and human review. |
| FR-TM-07 | Platform Admin owns the initial system-wide ticket taxonomy and queues. Support Manager manages authorized team assignments/escalations and overrides. Support Agent can create tickets, work permitted ticket information, change authorized statuses, and request escalation, but cannot modify the system taxonomy. |
| FR-TM-08 | Support additional synthetic tickets created through the application; do not connect real external customer or ticketing systems in the first release. |

The initial ticket fields are TicketId, TenantId, CustomerId, Subject, Description, Status, Category, Priority, AssignedTo, and CreatedAt. The dataset and fields remain tenant-scoped. Exact allowed status-transition rules and any additional Tenant Admin ticket actions must be resolved before those behaviors are finalized; do not infer them from the status list.

**5.11 Operational Limits, Retention, and Deletion** ****

The first release provides validated, centralized, configurable operational settings in the administrative console. Platform Admin owns global configuration; Tenant Admin has view-only access. Changes are validated before application, versioned, and audited.

Initial proposed operational defaults:

| Setting | Initial value |
| --- | --- |
| General API rate limit | 60 requests per user per minute |
| AI request limit | 10 requests per user per minute |
| Concurrent AI requests | 2 per user |
| General API timeout | 30 seconds |
| AI model timeout | 60 seconds |
| Maximum document upload | 20 MB per file |
| Conversation context | Most recent 10 turns |

Validate upload extension, MIME/content type, actual content, processing outcome, and size; reject unsupported, corrupted, or oversized files clearly. Enforce configured input/output token limits based on the selected model. Exact model-specific token limits and monthly monetary cost budgets remain deferred until model selection, pricing, quota, and subscription validation.

Initial proposed retention and deletion defaults:

| Data | Retention / deletion behavior |
| --- | --- |
| Original documents and previous versions | Retain while the parent document is active; delete when it is deleted. |
| Extracted text, chunks, and embeddings | Retain while the associated document is active; immediately make unavailable for retrieval upon deletion. |
| Deleted documents and derived data | Stop returning from search/retrieval immediately; physically purge from primary storage and indexes within 30 days of the deletion request. |
| Backups | Maximum 30 days. Reapply deletion records after restoration. |
| Application logs | 30 days; do not store document content, passwords, secrets, or unnecessary sensitive data. |
| Conversations | 90 days, then automatically delete. |
| Evaluation data and results | 90 days; synthetic data only. |

Retention settings are configurable, not hardcoded. Platform Admin manages global policies; Tenant Admin can delete authorized documents in their own tenant but cannot modify global policies. The administrative console displays document deletion/cleanup status and allows authorized cleanup operations. Validate policy changes before applying them. Maintain minimal deletion/retention audit metadata without retaining deleted document content. Audit-record retention duration remains to be defined.

**5.12 Administrative Activity and Audit** ****

Record user creation, activation/deactivation and role changes; permission-matrix and tenant administration; operational-configuration and retention-policy changes; document deletion/cleanup; ticket creation, assignment/reassignment and status changes; tool execution; actor, tenant, outcome, timestamp, and correlation ID where applicable. Protect audit records from unauthorized modification and avoid unnecessary sensitive content. Audit retention and access rules must be defined without weakening least privilege.

**6. Key User Workflows** ****

**6.1 Ask a Knowledge-Grounded Question** ****

1. User signs in and selects the appropriate workspace. 

2. API validates identity, role, tenant, request limits, and conversation context. 

3. Retrieval searches authorized indexed chunks and returns ranked source references. 

4. The model receives the question and retrieved evidence under a grounding-focused prompt. 

5. The UI displays the answer and source references, or a clear no-answer response. 

6. User may submit feedback; relevant metadata is recorded for evaluation. 

**6.2 Ingest or Update a Knowledge Document** ****

7. Authorized user uploads a supported PDF, DOCX, or TXT document of no more than the configured 20 MB initial maximum and receives validation feedback. 

8. API stores the file and creates a tenant-scoped document record and version. 

9. A worker extracts text, chunks it, creates embeddings, and indexes the chunks. 

10. Document status becomes Indexed or Failed, with a safe error summary if needed. 

11. On replacement or deletion, old chunks are removed or disabled from retrieval. 

**6.3 Generate a Ticket Reply** ****

12. Agent opens an authorized ticket. 

13. Agent requests a summary, classification, or suggested reply. 

14. System retrieves relevant knowledge and authorized ticket context. 

15. Model returns a structured result or draft; UI labels it AI-generated. 

16. Agent reviews, edits, accepts, or discards the suggestion. 

17. No customer message is sent without a separate explicit human action. 
 
**6.4 Administer a Tenant and Users** ****

1. Platform Admin creates or updates a tenant and provisions its initial Tenant Admin.
2. Tenant Admin creates and manages users within that tenant and assigns only permitted predefined roles.
3. The application enforces the centralized resource/action permission matrix on the backend and records administrative changes.
4. Self-registration is unavailable. Platform Admin manages global role mappings and configuration; Tenant Admin cannot change global settings.

**6.5 Manage a Support Ticket** ****

1. An authorized user creates or opens a tenant-scoped ticket.
2. The system enforces role permissions for ticket edits, assignment, status/category/priority changes, escalation, resolution, closure, and reopening.
3. Support Manager performs authorized team assignment and escalation actions; Support Agent may update permitted ticket fields and request escalation.
4. The system records ticket activity and audit metadata. AI suggestions remain separate from authoritative values until an authorized human acts.

**7. High-Level Architecture** ****

| **Layer**  | **Responsibility**  |
| --- | --- |
| React + TypeScript  | Chat, tenant/user administration, permission/configuration views, knowledge administration, ticket lifecycle, copilot, dashboard, feedback.  |
| .NET 8 Web API  | ASP.NET Core Identity local authentication; authorization boundary; tenant scoping; orchestration; validation; tool registry; administrative configuration; persistence; API contracts.  |
| Azure AI model endpoint  | Answer generation, ticket summarization/classification, and structured responses.  |
| Azure AI Search  | Vector and/or hybrid retrieval over tenant-scoped knowledge chunks.  |
| Azure Blob Storage  | Original uploaded documents and optional processed artifacts.  |
| Azure SQL  | Tenants, users/roles/permissions, documents, conversations, tickets/activity, customers, feedback, configuration, audit metadata, evaluation runs.  |
| Background worker / Azure Functions  | Document extraction, chunking, embeddings, indexing, retries, and status management.  |
| Key Vault / Application Insights  | Secret management; logs, traces, metrics, dependencies, and correlation.  |
| Administrative controls  | Centrally managed operational limits, retention/deletion policies, permission mappings, and auditable configuration history.  |
| GitHub Actions  | Build, test, configured security checks, and deployment workflow.  |
 

The API mediates model and search access. The browser must not receive provider keys or unrestricted service credentials. Use configuration abstractions for local and Azure environments. 

**8. Core Data Entities** ****

| **Entity**  | **Illustrative fields**  |
| --- | --- |
| Tenant  | TenantId, Name, Status, CreatedAt  |
| User / Membership  | UserId, TenantId, DisplayName, Role, Status  |
| Role / Permission Mapping  | Role, Resource, Action, Permission, UpdatedBy, UpdatedAt  |
| KnowledgeDocument  | DocumentId, TenantId, FileName, BlobUri, Version, Status, UploadedBy, CreatedAt, UpdatedAt  |
| KnowledgeChunk  | ChunkId, TenantId, DocumentId, Version, Content, PageOrSection, SearchDocumentId  |
| Conversation / ChatMessage  | ConversationId, TenantId, UserId, Role, Content, CreatedAt, PromptVersion, ModelId  |
| Citation  | CitationId, MessageId, DocumentId, ChunkId, DisplayOrder  |
| Customer  | CustomerId, TenantId, fabricated display information and related ticket references  |
| Ticket  | TicketId, TenantId, CustomerId, Subject, Description, Status, Category, Priority, AssignedTo, CreatedAt  |
| TicketActivity  | ActivityId, TenantId, TicketId, ActorId, Action, Timestamp, CorrelationId  |
| TicketAIResult  | ResultId, TicketId, Summary, SuggestedCategory, SuggestedPriority, SuggestedSentiment, ModelId, CreatedAt, ReviewedBy  |
| Feedback  | FeedbackId, TenantId, UserId, MessageId, Rating, Comment, CreatedAt  |
| ToolAudit / EvaluationRun  | AuditId, TenantId, ActorId, ToolName, Outcome, CorrelationId; RunId, DatasetVersion, PromptVersion, ModelId, Metrics, Status  |
| OperationalSetting / RetentionPolicy  | Setting/policy name, value, version, updated by/time, audit reference  |
 

These are logical entities, not a finalized schema. Define indexes, foreign keys, retention, and tenant-aware uniqueness during implementation. 

**9. API and Integration Requirements** ****

| **Area**  | **Illustrative contract**  | **Notes**  |
| --- | --- | --- |
| Chat  | POST /api/chat/messages  | Accept question and optional conversation ID; return answer, citations, and trace metadata.  |
| History  | GET /api/conversations/{id}  | Enforce ownership/role and tenant access.  |
| Knowledge  | POST /api/knowledge/documents  | Multipart upload; validate and create processing record.  |
| Knowledge status  | GET /api/knowledge/documents/{id}  | Return status and safe error details.  |
| Lifecycle  | POST /api/knowledge/documents/{id}/reindex; DELETE /api/knowledge/documents/{id}  | Authorized reindex/delete.  |
| Tickets  | GET /api/tickets; GET /api/tickets/{id}  | Tenant-scoped, paginated, filterable.  |
| Ticket lifecycle  | Ticket create/update/assignment/status operations  | Enforce role and tenant permissions; record activity/audit; exact routes are design-time contracts.  |
| Ticket AI  | POST /api/tickets/{id}/ai-summary; POST /api/tickets/{id}/classify  | Return typed, validated structured output.  |
| Reply draft  | POST /api/tickets/{id}/draft-reply  | Return draft and citations; do not send.  |
| Feedback  | POST /api/feedback  | Associate with tenant, user, and message.  |
| Health  | GET /health  | Expose only non-sensitive health information.  |
| Administration  | Tenant, user, permission-matrix, operational-setting, and retention-policy operations  | Enforce Platform Admin/Tenant Admin scopes; validate, version, and audit changes.  |
 

Endpoint names are examples. Final contracts should define schemas, validation, status codes, error responses, idempotency where needed, and OpenAPI documentation. 

**10. Non-Functional Requirements** ****

| **Category**  | **Requirement**  |
| --- | --- |
| Security  | HTTPS; secret protection; input validation; server-side tenant and role authorization; least privilege.  |
| Privacy  | Use synthetic data; minimize logged content; document retention and deletion behavior.  |
| Reliability  | Handle timeouts, throttling, transient errors, and partial ingestion failures; make retries safe.  |
| Performance  | Use pagination and asynchronous ingestion; establish latency baselines before setting guarantees.  |
| Scalability  | Keep ingestion asynchronous and services loosely coupled; avoid reliance on in-memory state.  |
| Maintainability  | Layered boundaries, dependency injection, typed contracts, structured logging, documented configuration.  |
| Accessibility  | Keyboard-operable controls, labels, readable contrast, and clear loading/error states.  |
| Observability  | Correlate UI/API/worker/model/search operations; record latency and failure rates without excess personal data.  |
| Cost  | Use budgets/alerts where available; cap input/output; document model/search usage and teardown.  |
| Portability  | Keep provider-specific code behind interfaces where practical; document cloud dependencies.  |
| Operational controls  | Apply configurable initial API/AI request, concurrency, timeout, upload, and conversation-context limits from section 5.11.  |
| Retention  | Apply configurable document, log, conversation, evaluation, and backup retention/deletion periods from section 5.11.  |
 

**11. AI-Specific Guardrails** ****

- Ground support answers in approved retrieved knowledge; show sources and do not fabricate citations. 

- Use a no-answer path for missing, conflicting, stale, or insufficient evidence. 

- Treat documents, tickets, and retrieved passages as untrusted data, not model instructions. 

- Prevent cross-tenant access to documents, tickets, conversations, and embeddings. 

- Constrain tool use to an allowlist with typed schemas and server-side authorization. 

- Require human review for customer-facing drafts and business-changing actions. 

- Validate structured model output before persistence or downstream use. 

- Version prompts and evaluation datasets; rerun regression tests after material changes. 

- Label AI classifications and sentiment as provisional and editable. 

**12. Sample Data and Evaluation Assets** ****

| **Dataset**  | **Suggested volume**  | **Purpose**  |
| --- | --- | --- |
| Knowledge articles / FAQs  | 20  | Product setup, billing, account access, troubleshooting, and policy topics.  |
| Synthetic tickets  | 100 initial tickets across 5 fictional tenants and 10 fictional support agents  | Exercise ticket lifecycle, summaries, categories, priorities, assignment, tenant isolation, and reply drafting; generate repeatably with a deterministic seed script.  |
| Fictional organizations  | 5  | Validate tenant isolation.  |
| Support agents  | 10  | Exercise roles, assignment, and access boundaries.  |
| Question/source pairs  | 50  | Measure retrieval, grounding, and citation behavior.  |
| No-answer questions  | 10  | Check abstention when knowledge is missing.  |
| Prompt-injection cases  | 10  | Test resistance to instructions embedded in content.  |
 

Use fabricated names and content only. Do not import real customer records or secrets into prompts, logs, fixtures, or screenshots. 

**13. Acceptance Criteria** ****

- An authorized user uploads a supported file and sees status through indexing or a safe failure state. 

- An indexed document is retrievable and a chat response can cite it. 

- A question without supporting content receives a clear no-answer response, not an invented answer. 

- Users from different tenants cannot access each other's documents, chunks, tickets, conversations, or feedback, including through direct API calls. 

- Ticket summary/classification conforms to a documented schema; invalid output is rejected or safely retried. 

- An agent can edit/discard a suggested reply; the system does not send it automatically. 

- Tool calls are allowlisted, authorized, bounded by timeout, and represented in an audit record. 

- CI runs build and automated tests on pull requests; failures block the normal merge path. 

- Setup and deployment are documented, and secrets are absent from the repository. 

- A repeatable evaluation run records results and model/prompt identifiers. 
- Platform Admin can manage tenants, the predefined-role permission matrix, and global operational/retention settings; Tenant Admin user management is tenant-scoped.
- Unauthorized role/resource actions and cross-tenant access are denied through direct backend requests as well as the UI.
- Authorized users can create and manage synthetic tickets through the ticket lifecycle, with tenant-scoped permissions and auditable activity.
- Ticket queue recommendations follow the configured category defaults and remain subject to authorization and human review.
- Operational settings are validated, centralized, versioned, and auditable; the initial values are in section 5.11.
- Deleted knowledge is unavailable to retrieval immediately and is physically purged from primary storage/indexes within 30 days; backups expire within 30 days and deletion records are reapplied after restoration.
- Conversations are deleted after 90 days; application logs are retained 30 days; evaluation data/results are retained 90 days and use synthetic data only.
- Audit records include the applicable actor, tenant, action/outcome, timestamp, and correlation ID without unnecessary sensitive content.

**14. Test Strategy** ****

| **Test level**  | **Coverage examples**  |
| --- | --- |
| Unit  | Chunking, 20 MB file validation, tenant filter construction, permission mapping, retention/configuration validation, DTO validation, prompt formatting, output parsing, and ticket transitions.  |
| Integration  | SQL repositories, blob operations, search indexing/retrieval, model adapter, tool registry, background worker, configuration, retention cleanup, and audit history.  |
| API  | Local authentication, tenant/user administration, RBAC, ticket lifecycle permissions, validation, pagination, status codes, tenant isolation, and error handling.  |
| AI evaluation  | Retrieval relevance, grounding, citation correctness, abstention, structured output validity, prompt injection.  |
| End-to-end  | Tenant/user setup → permission checks; upload → index → ask → inspect citations → feedback; synthetic ticket create/assign/update/resolve → summary/classification → edit draft.  |
| Operational  | Health checks, telemetry correlation, audit events, retention/deletion, retries, configured throttling/timeouts, configuration validation, and deployment smoke test.  |
 

**15. GitHub and Copilot Delivery Workflow** ****

1. Create a GitHub issue for each bounded task with acceptance criteria and test expectations.
2. Ask Copilot in VS Code to analyze the issue and propose a plan; review it before implementation.
3. Implement small, reviewable changes; the developer owns architecture and security decisions.
4. Use Copilot to draft tests, then inspect and add negative/security cases.
5. Run formatting, build, unit/integration tests, and relevant AI evaluation locally.
6. Open a PR linked to the issue with design notes, test evidence, and migration/configuration details.
7. Use CI as a quality gate; require human review and never blindly merge AI-generated code.
8. Maintain repository instructions covering conventions, security, test commands, and AI-code boundaries.

**16. Suggested 30-Day Delivery Boundary** ****

The mandatory release is the scope in section 4.1. Organize it as small, independently implementable and testable feature modules or vertical slices:

1. Identity and Access Management.
2. Administrative Configuration.
3. Knowledge Management.
4. Ticket Management.
5. AI Ticket Intelligence.
6. AI Customer Assistant.
7. Agent Copilot.
8. Analytics and Reporting.
9. Audit and Monitoring.
10. Evaluation and Quality Assurance.

For each module, define acceptance criteria, dependencies, and integration contracts; include relevant unit/API/integration/security tests; verify role permissions and tenant isolation; and maintain required documentation/audit coverage. Decide implementation order, task breakdown, dependency sequencing, resource allocation, and milestones separately during Implementation Planning based on technical dependencies and available capacity.
 

This is an intensive learning build, not a commitment to production readiness. Prioritize a thin, working vertical slice over optional features. 

**17. Risks, Assumptions, and Open Questions** ****

| **Type**  | **Item**  | **Handling / decision**  |
| --- | --- | --- |
| Assumption  | CloudDesk is fictional; all demo data is synthetic.  | Keep sample content marked fictional.  |
| Assumption  | Azure AI model and search resources are available.  | Confirm region, model availability, quotas, and cost.  |
| Risk  | Model output may be inaccurate or overconfident.  | Ground, abstain, cite, evaluate, and require human review.  |
| Risk  | Cross-tenant leakage through filters or caching.  | Centralize tenant scoping; add negative integration tests.  |
| Risk  | Parsing/indexing can fail on complex files.  | Limit formats/size; expose status; add retries and safe errors.  |
| Risk  | Cloud costs may exceed the learning budget.  | Use small datasets, caps, alerts, and teardown instructions.  |
| Open question  | Which exact Azure AI generation and embedding model deployments and region will be used?  | Verify model availability, Azure AI Search compatibility, quotas, pricing, and regional support before implementation; keep identifiers and dimensions configurable/versioned.  |
| Open question  | What are the exact model-specific token limits and monthly monetary cost budget?  | Decide after the selected model, Azure pricing, and subscription quotas are verified.  |
| Open question  | Which detailed ticket status transitions and any additional Tenant Admin ticket actions are permitted?  | Define and test the transition/permission matrix; do not infer unspecified actions.  |
| Open question  | Which customer fields are necessary for the limited customer lookup?  | Minimize returned data and specify the approved fields before contract finalization.  |
| Open question  | How long are audit records retained and who may read them?  | Define retention and access without retaining unnecessary sensitive content.  |
| Proposed evaluation target  | Recall@5 >= 80%, Grounded Answer Rate >= 90%, Citation Precision >= 95%, and 100% on the initial no-answer/structured-output/prompt-injection cases.  | Proposed only, not formal release gates in this unapproved draft. Formal gate status requires subsequent Human Requirement Approval. Cross-tenant denial remains mandatory.  |
 

**18. Definition of Done** ****

- Requirement is implemented or explicitly deferred. 

- Acceptance criteria are met and relevant tests are committed. 

- Tenant and role checks are applied and tested for affected data paths. 
- Tenant/user administration, permission-matrix changes, operational configuration, ticket lifecycle, and relevant audit events are covered by tests.
- Configured request/rate/concurrency/time/upload/context limits and retention/deletion behaviors are validated.

- Errors, loading, and empty states are handled. 

- Telemetry is useful without exposing secrets or unnecessary customer content. 

- Documentation covers setup, configuration, tests, deployment, and known limitations. 

- PR is linked to an issue and passes CI and human review. 

**Appendix A. Recommended Initial Backlog** ****

| **Epic**  | **Example issues**  |
| --- | --- |
| Foundation  | Configure React/.NET and local identity; define tenants/users/RBAC; add admin console, operational settings, and CI.  |
| Ticket management  | Deterministic synthetic seed data; ticket lifecycle, role permissions, assignment, audit/activity, categories and queues.  |
| Knowledge  | Upload API; 20 MB validation; retention/deletion controls; extraction; chunking; embeddings; index lifecycle; status UI.  |
| Assistant  | Chat API; retrieval; prompt versioning; citation DTO; abstention; conversation UI; feedback.  |
| Ticket copilot  | Ticket summary/classification schema; reply draft; human edit flow; read-only lookup tools.  |
| Quality & operations  | Tenant/RBAC tests; evaluation runner; prompt-injection tests; audit/telemetry; configurable limits; retention; deployment; demo runbook.  |
 

**Appendix B. Glossary** ****

| **Term**  | **Meaning**  |
| --- | --- |
| RAG  | Retrieval-augmented generation: retrieve relevant content and provide it to a model as evidence.  |
| Embedding  | Numerical representation of text used for semantic similarity search.  |
| Chunk  | A segment of a source document indexed and retrieved independently.  |
| Grounded answer  | A response supported by available evidence, ideally with traceable citations.  |
| Abstention  | Declining to provide a substantive answer when evidence is insufficient.  |
| Tenant isolation  | Controls preventing one organization from accessing another organization's data.  |
| Human-in-the-loop  | A workflow where a person reviews or approves AI-generated content or actions.  |
 
