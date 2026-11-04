**SupportIQ** 

AI-Powered Customer Support Knowledge Portal 

**Product Requirements Document (PRD)** 

*Version* *1.0  |*  *September* *2026  |*  *Learning / portfolio project* 

 

**Document Control** ****

| **Item**  | **Description**  |
| --- | --- |
| Product  | SupportIQ  |
| Business context  | A fictional B2B SaaS provider, CloudDesk, uses SupportIQ to help support agents find approved answers and handle customer tickets.  |
| Purpose  | Define product scope, functional and non-functional requirements, workflows, acceptance criteria, and delivery guidance for an intensive 30-day build.  |
| Audience  | Product owner, developer, AI engineer, QA, and technical reviewer.  |
| Status  | Draft baseline; assumptions should be validated before implementation.  |
| Technology baseline  | React + TypeScript, .NET 8 Web API, Azure AI model endpoint, Azure AI Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, GitHub Actions.  |
 

**1. Executive Summary** ****

SupportIQ is a learning-oriented, production-minded AI customer support portal. It combines a tenant-aware knowledge base, retrieval-augmented generation (RAG), ticket intelligence, agent assistance, lightweight workflow automation, and evaluation/operations capabilities. 

The system helps agents locate approved information, draft grounded responses, summarize and classify tickets, and recognize when evidence is insufficient. AI outputs are assistive: a human remains responsible for customer-facing decisions and communications. 

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
| Tenant Admin  | Manage organization settings, users, and knowledge sources.  | Manage tenant users and content.  |
| Support Agent  | Search knowledge, view tickets, use AI suggestions, submit feedback.  | Access permitted tickets and knowledge; approve/edit drafts.  |
| Support Manager  | Review queues, escalations, quality metrics, and team analytics.  | Read team data; manage assignments where authorized.  |
| Platform Admin  | Operate the application and investigate platform issues.  | Privileged operational access; access audited and minimized.  |
 

Authorization must be enforced by the API, not merely by hiding UI controls. Roles may be seeded for the demo, but the model must be explicit and testable. 

**4. Scope** ****

**4.1 In Scope for the First Demonstrable Release** ****

- Authentication-ready structure and tenant-aware authorization boundaries. 

- Knowledge upload, extraction, chunking, embedding, indexing, status, reindex, and deletion. 

- RAG chat with conversation context, citations, no-answer behavior, and feedback. 

- Ticket list/detail with AI classification and summarization. 

- Agent copilot for suggested replies and knowledge recommendations, with human review. 

- Read-only customer/ticket lookup tools and auditable tool execution. 

- Automated tests, GitHub issue/PR workflow, CI, telemetry, and Azure deployment. 

**4.2 Deferred / Optional** ****

- Advanced natural-language analytics and arbitrary text-to-SQL. 

- Complex autonomous multi-agent orchestration or unsupervised customer communication. 

- Production integrations with external ticketing, CRM, email, or messaging platforms. 

- Enterprise SSO, billing, multi-region disaster recovery, and compliance certifications. 

- Large-scale benchmarking, custom fine-tuning, and automated model selection. 

**5. Product Modules and Functional Requirements** ****

**5.1 AI Customer Assistant** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-CA-01  | Users can start a conversation and submit a natural-language question.  |
| FR-CA-02  | Retrieval returns only knowledge the current user is authorized to access.  |
| FR-CA-03  | Responses are grounded in retrieved content and display source title plus excerpt or section reference where available.  |
| FR-CA-04  | If evidence is insufficient, the assistant states it cannot answer from available knowledge and may suggest escalation.  |
| FR-CA-05  | Recent conversation turns may be used as context without crossing tenant or access boundaries.  |
| FR-CA-06  | Users can provide positive/negative feedback and an optional reason.  |
| FR-CA-07  | Users can view only conversation history permitted by their role.  |
| FR-CA-08  | English is supported initially; the design should allow additional languages later.  |
 

**5.2 Knowledge Base Management** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-KB-01  | Authorized users can upload PDF, DOCX, and TXT files; unsupported or oversized files are rejected clearly.  |
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
| FR-AC-07  | Distinguish internal notes from customer-facing draft content.  |
 

**5.5 AI Workflow Automation** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-WF-01  | The assistant can invoke a small allowlisted set of tools, such as knowledge search and read-only ticket/customer lookup.  |
| FR-WF-02  | Each tool has typed input/output, authorization checks, timeout, and error handling.  |
| FR-WF-03  | The model cannot execute arbitrary SQL, shell commands, or unrestricted network requests.  |
| FR-WF-04  | Business-data changes require explicit human confirmation; write actions may be deferred.  |
| FR-WF-05  | Record tool calls, outcomes, actor, tenant, and correlation identifiers in an audit trail.  |
| FR-WF-06  | Tool failures are communicated without exposing secrets or stack traces.  |
 

**5.6 AI Support Analytics** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-AN-01  | Provide a basic dashboard for ticket counts by status, category, and priority, scoped to authorized data.  |
| FR-AN-02  | Show simple trends and SLA indicators when the sample data contains the required fields.  |
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
 

**6. Key User Workflows** ****

**6.1 Ask a Knowledge-Grounded Question** ****

1. User signs in and selects the appropriate workspace. 

2. API validates identity, role, tenant, request limits, and conversation context. 

3. Retrieval searches authorized indexed chunks and returns ranked source references. 

4. The model receives the question and retrieved evidence under a grounding-focused prompt. 

5. The UI displays the answer and source references, or a clear no-answer response. 

6. User may submit feedback; relevant metadata is recorded for evaluation. 

**6.2 Ingest or Update a Knowledge Document** ****

7. Authorized user uploads a supported document and receives validation feedback. 

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

**7. High-Level Architecture** ****

| **Layer**  | **Responsibility**  |
| --- | --- |
| React + TypeScript  | Chat, knowledge administration, ticket views, copilot, dashboard, feedback.  |
| .NET 8 Web API  | Authentication/authorization boundary, tenant scoping, orchestration, validation, tool registry, persistence, API contracts.  |
| Azure AI model endpoint  | Answer generation, ticket summarization/classification, and structured responses.  |
| Azure AI Search  | Vector and/or hybrid retrieval over tenant-scoped knowledge chunks.  |
| Azure Blob Storage  | Original uploaded documents and optional processed artifacts.  |
| Azure SQL  | Tenants, users/roles, documents, conversations, tickets, feedback, audit metadata, evaluation runs.  |
| Background worker / Azure Functions  | Document extraction, chunking, embeddings, indexing, retries, and status management.  |
| Key Vault / Application Insights  | Secret management; logs, traces, metrics, dependencies, and correlation.  |
| GitHub Actions  | Build, test, configured security checks, and deployment workflow.  |
 

The API mediates model and search access. The browser must not receive provider keys or unrestricted service credentials. Use configuration abstractions for local and Azure environments. 

**8. Core Data Entities** ****

| **Entity**  | **Illustrative fields**  |
| --- | --- |
| Tenant  | TenantId, Name, Status, CreatedAt  |
| User / Membership  | UserId, TenantId, DisplayName, Role, Status  |
| KnowledgeDocument  | DocumentId, TenantId, FileName, BlobUri, Version, Status, UploadedBy, CreatedAt, UpdatedAt  |
| KnowledgeChunk  | ChunkId, TenantId, DocumentId, Version, Content, PageOrSection, SearchDocumentId  |
| Conversation / ChatMessage  | ConversationId, TenantId, UserId, Role, Content, CreatedAt, PromptVersion, ModelId  |
| Citation  | CitationId, MessageId, DocumentId, ChunkId, DisplayOrder  |
| Ticket  | TicketId, TenantId, CustomerId, Subject, Description, Status, Category, Priority, AssignedTo, CreatedAt  |
| TicketAIResult  | ResultId, TicketId, Summary, SuggestedCategory, SuggestedPriority, SuggestedSentiment, ModelId, CreatedAt, ReviewedBy  |
| Feedback  | FeedbackId, TenantId, UserId, MessageId, Rating, Comment, CreatedAt  |
| ToolAudit / EvaluationRun  | AuditId, TenantId, ActorId, ToolName, Outcome, CorrelationId; RunId, DatasetVersion, PromptVersion, ModelId, Metrics, Status  |
 

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
| Ticket AI  | POST /api/tickets/{id}/ai-summary; POST /api/tickets/{id}/classify  | Return typed, validated structured output.  |
| Reply draft  | POST /api/tickets/{id}/draft-reply  | Return draft and citations; do not send.  |
| Feedback  | POST /api/feedback  | Associate with tenant, user, and message.  |
| Health  | GET /health  | Expose only non-sensitive health information.  |
 

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
| Synthetic tickets  | 100  | Exercise summaries, categories, priorities, assignment, and reply drafting.  |
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

**14. Test Strategy** ****

| **Test level**  | **Coverage examples**  |
| --- | --- |
| Unit  | Chunking, file validation, tenant filter construction, DTO validation, prompt formatting, output parsing.  |
| Integration  | SQL repositories, blob operations, search indexing/retrieval, model adapter, tool registry, background worker.  |
| API  | Authentication/authorization, validation, pagination, status codes, tenant isolation, error handling.  |
| AI evaluation  | Retrieval relevance, grounding, citation correctness, abstention, structured output validity, prompt injection.  |
| End-to-end  | Upload → index → ask → inspect citations → feedback; ticket → summary/classification → edit draft.  |
| Operational  | Health checks, telemetry correlation, retries, throttling, configuration validation, deployment smoke test.  |
 

**15. GitHub and Copilot Delivery Workflow** ****

18. Create a GitHub issue for each bounded task with acceptance criteria and test expectations. 

19. Ask Copilot in VS Code to analyze the issue and propose a plan; review it before implementation. 

20. Implement one small change at a time; the developer owns architecture and security decisions. 

21. Use Copilot to draft tests, then inspect and add negative/security cases. 

22. Run formatting, build, unit/integration tests, and relevant AI evaluation locally. 

23. Open a PR linked to the issue with design notes, test evidence, and migration/configuration details. 

24. Use CI as a quality gate; require human review and never blindly merge AI-generated code. 

25. Maintain repository instructions covering conventions, security, test commands, and AI-code boundaries. 

**16. Suggested 30-Day Delivery Boundary** ****

| **Week**  | **Focus**  | **Expected outcome**  |
| --- | --- | --- |
| Week 1  | Foundation, domain model, repo, UI skeleton, tenant boundaries, CI  | Runnable skeleton, backlog, core entities, build/test pipeline.  |
| Week 2  | Knowledge ingestion, lifecycle, embeddings, search  | Upload-to-index workflow and retrieval tests.  |
| Week 3  | RAG assistant, citations, abstention, ticket AI, agent draft  | End-to-end assistant and ticket copilot using synthetic data.  |
| Week 4  | Security tests, evaluation, telemetry, resilience, deployment, demo  | Deployed demo, setup guide, evaluation report, known limitations.  |
 

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
| Open question  | Which authentication provider is used for the demo?  | Choose local auth or Microsoft Entra ID and document trade-offs.  |
| Open question  | What are file-size limits and retention periods?  | Set explicit limits before upload/deletion implementation.  |
| Open question  | Which model and embedding deployment will be used?  | Confirm availability, dimensions, pricing, and index compatibility.  |
| Open question  | How will tickets be populated?  | Prefer a deterministic synthetic seed script for release one.  |
 

**18. Definition of Done** ****

- Requirement is implemented or explicitly deferred. 

- Acceptance criteria are met and relevant tests are committed. 

- Tenant and role checks are applied and tested for affected data paths. 

- Errors, loading, and empty states are handled. 

- Telemetry is useful without exposing secrets or unnecessary customer content. 

- Documentation covers setup, configuration, tests, deployment, and known limitations. 

- PR is linked to an issue and passes CI and human review. 

**Appendix A. Recommended Initial Backlog** ****

| **Epic**  | **Example issues**  |
| --- | --- |
| Foundation  | Create solution structure; configure React/.NET; define tenant/user models; add CI; add repository instructions.  |
| Knowledge  | Upload API; validation; blob adapter; extraction; chunking; embeddings; index lifecycle; status UI.  |
| Assistant  | Chat API; retrieval; prompt versioning; citation DTO; abstention; conversation UI; feedback.  |
| Ticket copilot  | Seed dataset; list/detail; summary; classification schema; reply draft; human edit flow.  |
| Quality & operations  | Tenant tests; evaluation runner; prompt-injection tests; telemetry; rate limits; deployment; demo runbook.  |
 

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
 


