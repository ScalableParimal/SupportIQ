**SupportIQ** 

AI-Powered Customer Support Knowledge Portal 

**Product Requirements Document (PRD)** 

*Version* *1.9 |* *November 2026 | Learning / portfolio project*

 

**Document Control** ****

| **Item**  | **Description**  |
| --- | --- |
| Product  | SupportIQ  |
| Business context  | A fictional B2B SaaS provider, CloudDesk, uses SupportIQ to help support agents find approved answers and handle customer tickets.  |
| Purpose  | Define product scope, functional and non-functional requirements, workflows, acceptance criteria, and delivery guidance for a 30-day demonstrable learning release.  |
| Audience  | Product owner, developer, AI engineer, QA, and technical reviewer.  |
| Status  | Draft Updated Requirement; unapproved and pending subsequent Requirement Analysis, independent verification, and Human Requirement Approval.  |
| Technology baseline  | React + TypeScript, .NET 8 Web API with ASP.NET Core Identity local authentication, Azure AI model endpoints, Azure AI Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, GitHub Actions.  |

**Version lineage:** This unapproved version 1.9 is an Initial Analysis Clarification of version 1.8 (`SupportIQ_Product_Requirement_v1.8.md`, SHA-256 `E7FB3E982555034B098D42E258CAFBEDB651A0A05B736A99DE987DAB6355AD1B`). Version 1.8 and its version 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, and 1.0 predecessors remain preserved as separate versions. These clarifications do not constitute Human Requirement Approval.
 

**1. Executive Summary** ****

SupportIQ is a learning-oriented, production-minded AI customer support portal. It combines tenant-aware identity and administration, tenant-scoped support teams, an approval-gated knowledge base and retrieval-augmented generation (RAG), complete core ticket management, ticket intelligence, agent assistance, bounded workflow tools, analytics, evaluation, and operational controls.

The system helps agents locate Tenant Admin-approved information, manage team-scoped support tickets, search authorized customer records, read feedback within role scope, draft grounded responses, summarize and classify tickets, and recognize when evidence is insufficient. Knowledge is unavailable to RAG until the current document version is approved; replacement or reprocessing requires approval again. AI outputs are assistive: a human remains responsible for customer-facing decisions and communications. The first release includes tenant and team administration, recoverable local accounts with real transactional email, persisted asynchronous jobs for long-running work, and configurable security, retention, and operational controls. It remains a demonstrable learning release, not a production-readiness commitment.

**2. Goals and Success Measures** ****

- Reduce time spent searching documentation and composing routine replies; measure impact in a later pilot rather than assume improvement. 

- Provide answers with traceable source references and abstain when evidence is insufficient. 

- Demonstrate an end-to-end AI application using .NET, React, Azure services, and GitHub Copilot-assisted development. 

- Establish repeatable tests for retrieval, answer quality, citations, structured outputs, tenant isolation, and core APIs. 

- Deploy a demonstrable application with documented setup, CI checks, monitoring, and cost controls. 

| **Measure**  | **Initial target / evidence**  |
| --- | --- |
| RAG evaluation set  | At least 50 question/source pairs, 10 no-answer questions, and 10 prompt-injection cases.  |
| Knowledge lifecycle  | Upload, process, approve/reject exact versions, retrieve only approved versions, update/reprocess, and delete with visible status.  |
| Ticket intelligence  | Classification and summary return schema-valid output; agents can edit or override.  |
| Grounding  | Assistant responses show sources; unsupported questions trigger a clear no-answer response.  |
| Quality gates  | Automated unit/integration tests and CI checks run on pull requests.  |
| Security  | Tests demonstrate tenant, team, role, and approval isolation for representative API, job, and retrieval paths.  |
| Reproducibility  | A new developer can follow the README to configure, run, test, and deploy.  |
 

**3. Users and Roles** ****

| **Role**  | **Responsibilities**  | **Access summary**  |
| --- | --- | --- |
| Platform Admin  | Manage tenants, global settings, platform-level role mappings, and tightly controlled privileged operations.  | Cross-tenant administration is minimized and audited. Privileged changes require an independent second Platform Admin approval; initiators cannot approve their own changes.  |
| Tenant Admin  | Administer users, support teams, and knowledge for one tenant; approve knowledge versions and oversee tenant tickets, customers, and feedback.  | Tenant-scoped administration, including central triage of completely unassigned tickets in that tenant. Cannot change global role permissions or grant Platform Admin privileges.  |
| Support Manager  | Manage assigned teams, their tickets and escalations, team analytics, and feedback submitted by users in assigned teams.  | Team-scoped access; may belong to multiple teams within one tenant.  |
| Support Agent  | Work tickets currently assigned to them, search approved knowledge, use AI suggestions, and submit feedback.  | Customer access only through currently assigned tickets; cannot manage users, teams, RBAC, or delete knowledge.  |
 

Use ASP.NET Core Identity with local authentication for the first demonstrable release. Microsoft Entra ID and enterprise SSO are deferred. Platform Admin creates tenants and provisions the initial Tenant Admin account. Tenant Admin manages users and teams in their tenant and assigns only predefined permitted roles. Self-registration is disabled; demo users and roles may be seeded through a controlled setup process.

Implement a centralized, default-deny, explicit, testable resource/action permission matrix for the four predefined roles, including tenant, team, resource, action, and data-scope checks. Platform Admin may manage system-wide mappings but may not create arbitrary custom roles or tenant-specific permission overrides. A Platform Admin may initiate a privileged change, but a different Platform Admin must approve it; self-approval and self-elevation are prohibited. Tenant Admin may assign predefined roles and administer teams within their tenant but cannot change global permission definitions or grant Platform Admin privileges. Support Manager and Support Agent cannot manage RBAC configuration. Provide an administrative view of the permission matrix and audit role/permission changes and their approvals. Enforce permissions in backend APIs and data access, prevent privilege escalation, and test denied cross-tenant and cross-team access. Apply the specific role/action rules in sections 5.9 and 5.13; all unlisted combinations are denied.

**4. Scope** ****

**4.1 Mandatory First Demonstrable Release Scope** ****

The 30-day boundary is a target, not a fixed weekly schedule or guarantee. Organize the approved scope into independently implementable and testable modules; implementation order, dependencies, task breakdown, capacity, and milestones are decided separately during Implementation Planning. Prioritize security, administration, core ticket management, knowledge-to-RAG, AI assistance, and mandatory acceptance tests. Defer optional features if necessary to preserve these capabilities.

- Identity and Access Management: local authentication and recovery; tenant and user administration; four predefined roles; centralized resource/action RBAC; independent approval for privileged Platform Admin changes; transactional email.
- Support Team Management: tenant-scoped teams and memberships, one primary team per Support Agent, and multiple team memberships for Support Managers.
- Administrative Configuration: configurable operational limits, retention/deletion policies, system settings, validation, version history, and audit.
- Knowledge Management: supported-file upload (20 MB initial maximum), validation, extraction, chunking, embeddings, indexing, version-specific Tenant Admin approval, reprocessing, lifecycle status, tenant-authorized retrieval, and deletion.
- Ticket Management: tenant/team-scoped create, list, view, edit, assign/reassign, search/filter/sort/page, authorized status/category/priority changes, tracked Category/Priority correction requests, escalation, resolution, closure, reopening through authorized transitions, tracked cancellation requests and approval, and retained activity history.
- Customer and Feedback Access: role-scoped Customer Search and Customer Read, limited Feedback Read, and role-scoped customer-email visibility as defined in sections 5.5 and 5.9.
- AI Ticket Intelligence and Agent Copilot: summaries, category/priority/sentiment/urgency suggestions, knowledge recommendations, troubleshooting suggestions, and editable customer-reply drafts requiring human review.
- AI Customer Assistant for the four internal roles only: RAG chat, authorized retrieval, citations, abstention, 10-turn conversation context, history, and feedback; external CloudDesk customers cannot access it.
- Tools and Analytics: explicitly allowlisted, read-only knowledge/ticket/customer lookup, ticket summary/classification, and predefined analytics with the role-specific scopes in FR-AN-06, including the predefined AI-invoked analytics functions.
- Background Processing: persisted, tenant-scoped asynchronous jobs for long-running AI, RAG, ticket-intelligence, and knowledge operations, with authorized status/result access and user-initiated cancellation.
- Audit and Monitoring: administrative, configuration, approval, ticket, team, security, analytics access, job-cancellation, notification, and tool activity; application telemetry and approximate AI usage/cost monitoring.
- Evaluation and Quality Assurance: unit, integration, API, end-to-end, operational, security, tenant-isolation, prompt-injection, and AI evaluation tests, including ticket request/approval, job-cancellation, notification, Customer Search and scope, Feedback Read, email masking/unmask auditing, retention, and tenant-deletion behavior.
- Repeatable CI, documentation, and Azure deployment for the demonstrable release.

The first-release analytics, ticket field permissions and correction requests, ticket cancellation request/approval, user-initiated background-job cancellation, listed transactional email events, Customer Search, scoped Feedback Read, and customer-email visibility rules are mandatory in the current release and must not be deferred. The pre-existing items listed in section 4.2 remain deferred/out of scope.

**4.2 Deferred / Optional** ****

- Advanced natural-language analytics and arbitrary text-to-SQL. The predefined read-only natural-language analytics in section 5.5 and FR-AN-03 remain in scope.

- Complex autonomous multi-agent orchestration or unsupervised customer communication. 

- Production integrations with external ticketing, CRM, or messaging platforms. 

- Billing, multi-region disaster recovery, and compliance certifications. 

- Large-scale benchmarking, custom fine-tuning, and automated model selection. 
- Microsoft Entra ID and enterprise SSO.
- MFA, passwordless authentication, and advanced recovery methods beyond ASP.NET Core Identity's configured local recovery.
- Internal notes and their visibility/persistence workflows.
- AI-invoked write tools or autonomous business-data modifications.
- Arbitrary custom roles and tenant-specific permission overrides.
- SLA indicators until definitions, business calendars, time zones, and required fields are established.
- Automated approval of Platform Admin privileged changes; the independent second-admin control remains mandatory in the first release.

**5. Product Modules and Functional Requirements** ****

**5.1 AI Customer Assistant** ****

The first-release AI Customer Assistant is available only to authenticated Platform Admin, Tenant Admin, Support Manager, and Support Agent users. External CloudDesk customers cannot access it.

| **ID**  | **Requirement**  |
| --- | --- |
| FR-CA-01  | An authenticated Platform Admin, Tenant Admin, Support Manager, or Support Agent can start a conversation and submit a natural-language question; external CloudDesk customers cannot access the assistant.  |
| FR-CA-02  | For Tenant Admin, Support Manager, and Support Agent users, retrieval returns only the current document versions explicitly approved by a Tenant Admin in the user's tenant and authorized scope. Platform Admin assistant retrieval is limited to FR-AN-06 aggregate analytics for exactly one explicitly selected authorized tenant; it must not retrieve tenant knowledge documents or underlying tenant business records.  |
| FR-CA-03  | Responses are grounded in retrieved, approved content and display source title plus excerpt or section reference where available.  |
| FR-CA-04  | If evidence is insufficient, the assistant states it cannot answer from available knowledge and may suggest escalation.  |
| FR-CA-05  | The most recent 10 conversation turns may be used as context without crossing tenant or access boundaries.  |
| FR-CA-06  | Users can provide positive/negative feedback and an optional reason.  |
| FR-CA-07  | Each user can view only their own conversation history; users cannot read another user's history, regardless of role.  |
| FR-CA-08  | English is supported initially; the design should allow additional languages later.  |
 

**5.2 Knowledge Base Management** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-KB-01  | Authorized users can upload PDF, DOCX, and TXT files up to the configurable 20 MB initial maximum; unsupported, corrupted, or oversized files are rejected clearly.  |
| FR-KB-02  | Validate extension, content type, size, and processing outcome; do not trust filename alone.  |
| FR-KB-03  | Store originals and register tenant, uploader, timestamps, version, and processing status.  |
| FR-KB-04  | Extract and normalize text, split into configurable chunks, generate embeddings, and index chunks.  |
| FR-KB-05  | Track processing state separately from approval state for each version. Show processing status (Uploaded, Processing, Indexed, Failed, and deletion state) separately from approval status (Pending Approval, Approved, Rejected).  |
| FR-KB-06  | Authorized users can update or reprocess a document; each new or reprocessed version invalidates the prior approval and stale index entries immediately become unavailable to retrieval.  |
| FR-KB-07  | Authorized Tenant Admins can approve or reject a specific processed document version in their tenant; approval is required before any of that version's content can be retrieved by RAG or knowledge search.  |
| FR-KB-08  | Authorized users can delete a document and make its content and derived chunks unavailable.  |
| FR-KB-09  | Record approver, decision, document/version, timestamp, and optional reason; approval applies only to the exact content version reviewed.  |
| FR-KB-10  | Reprocessing, replacement, or material content change creates a new version requiring a new Tenant Admin decision; failed, pending, rejected, or stale versions are excluded from retrieval.  |
| FR-KB-11  | Search results and citations identify the approved source document version and, where feasible, page/section.  |
| FR-KB-12  | Pending, rejected, failed, unapproved, or stale versions never appear in search results or AI context.  |
 

**5.3 AI Ticket Management** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-TK-01  | Agents can view a ticket list and detail view using synthetic demo data.  |
| FR-TK-02  | Generate a concise summary from authorized ticket content through a persisted asynchronous job when the operation is long-running.  |
| FR-TK-03  | Classify tickets into configurable categories and priorities using structured output; do not modify authoritative ticket values without an authorized human action.  |
| FR-TK-04  | Sentiment or urgency is labeled as an AI suggestion, not a fact.  |
| FR-TK-05  | Recommend a queue or escalation reason where supported by rules and available information.  |
| FR-TK-06  | Agents can edit/override suggestions; retain the final human-approved value and, where appropriate, the original suggestion.  |
| FR-TK-07  | Invalid model output is handled safely and does not corrupt ticket data.  |
 

**5.4 AI Agent Copilot** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-AC-01  | Agents can request a suggested customer reply for a selected ticket.  |
| FR-AC-02  | Recommend relevant knowledge articles and show their sources.  |
| FR-AC-03  | Summarize customer context only from authorized tenant/team records and allowlisted customer/ticket fields.  |
| FR-AC-04  | Suggest next steps or troubleshooting checks when supported by approved knowledge.  |
| FR-AC-05  | Agents can edit, copy, discard, or regenerate a draft.  |
| FR-AC-06  | The first release must not send customer-facing messages automatically.  |
| FR-AC-07  | Internal notes and their visibility/persistence workflows are out of scope for the first release.  |
 

**5.5 AI Workflow Automation** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-WF-01  | The assistant can invoke only the explicitly allowlisted, read-only knowledge search, ticket lookup, customer lookup, ticket summary, ticket classification, and analytics functions defined in this section and FR-AN-03, subject to the role scopes in FR-AN-06; knowledge tools return approved versions only.  |
| FR-WF-02  | Each tool has typed input/output, authorization checks, timeout, and error handling.  |
| FR-WF-03  | The model cannot execute arbitrary SQL, shell commands, or unrestricted network requests.  |
| FR-WF-04  | The first release exposes no AI-invoked write tools. Any future business-data modification tool requires explicit human confirmation, server-side authorization, validation, and audit logging.  |
| FR-WF-05  | Record tool name, actor, tenant, outcome, timestamp, and correlation identifier in an audit trail.  |
| FR-WF-06  | Tool failures are communicated without exposing secrets or stack traces.  |
 

**First-Release Tool Allowlist** ****

The only AI-invoked tools in the first release are:

1. **Knowledge Search:** Search approved, tenant-authorized knowledge and return source references.
2. **Ticket Lookup:** Read authorized ticket details, status, category, priority, and assignment.
3. **Customer Lookup:** Read only the allowlisted customer fields and authorized related ticket fields from the synthetic demo dataset, after role, tenant, team, and ticket-level authorization.
4. **Ticket Summary:** Generate a summary from authorized ticket content without modifying the ticket.
5. **Ticket Classification:** Suggest category, priority, sentiment, and urgency without modifying the ticket.
6. **Predefined Analytics:** Answer the small set of predefined natural-language analytics questions in FR-AN-03 using only read-only functions within the requesting role's scope defined in FR-AN-06.

All tools are non-mutating and read-only with typed schemas, backend authorization, tenant/team/ticket scope, validation, timeouts, rate limits, safe errors, and audit records. No AI-invoked ticket assignment, status change, customer-data update, knowledge deletion, or customer communication is permitted. Future write tools require a separately governed decision and explicit human confirmation.

**Customer Search, lookup, and access contract:** Customer Search is a first-release capability. Search Customer ID by exact match, Display Name by partial case-insensitive match, and Company/Organization by partial case-insensitive match. Support status and created-date-range filters; sort by Display Name ascending/descending or Created Date newest/oldest; validate a configurable maximum page size; apply authorization and filters before pagination; and return total count and pagination metadata. Email is not searchable. Search results may contain only Customer ID, Customer Display Name, Company/Organization Name, Customer Account Status, Customer Created Date, and masked Email Address. Authorized related-ticket results may contain Ticket ID, Subject, Description only where the requester may read that ticket, Status, Category, Priority, Assigned Team, Assigned Agent, Created Date, Last Updated Date, Escalation Status, and Resolution Summary subject to ticket access. Do not return phone numbers, physical addresses, financial/payment details, credentials, internal notes, confidential staff discussions, unrestricted conversation history, or attachments.

Tenant Admins may search, read, and view related tickets only within their tenant. Support Managers may search/read Customers associated with tickets in their assigned teams, including team-assigned tickets without an Agent; they may not access completely unassigned tickets or other teams' tickets. Support Agents may search/read Customers only when associated with a ticket currently assigned to that Agent; no additional exception, separate grant mechanism, or additional granting authority is available in the first release. Revoke that access immediately on ticket reassignment, loss of team/tenant authorization, or when the ticket leaves the Agent's scope. Platform Admin has no routine Customer Search or unrestricted customer lookup; any separately authorized investigation remains audited and does not permit full-email access. Revalidate current relationships and authorization on every search, lookup, and direct-ID request; deny tenant-wide Agent browsing and prevent identifier enumeration.

Email is masked in Customer Search, lookup, and every response by default. Only a Tenant Admin may see a full registered email address for a Customer in their own tenant through an explicitly authorized Customer-detail operation. Platform Admin, Support Manager, and Support Agent receive masked email only. Enforce these rules server-side across APIs, search, AI tools, and lookup. Audit every full-email access with actor, tenant, Customer ID, timestamp, action, outcome, and correlation ID. Do not expose full email unnecessarily in logs, prompts, indexes, or unauthorized responses.

**First-Release Analytics Allowlist** ****

- Ticket counts grouped by status, category, or priority.
- Ticket-volume trends over predefined 7-day and 30-day ranges.
- Basic dashboards scoped by role as specified in FR-AN-06.
- Analytics are predefined, read-only, scoped by role as specified in FR-AN-06, and identify their data scope and time range. SLA indicators are deferred as stated in FR-AN-02.

**Role-based tool access:** Platform Admin has audited, minimized platform operational access; the Platform Admin assistant may use only the single-selected-tenant aggregate-analytics scope in FR-AN-06, with no access to tenant knowledge documents or underlying tenant records. Tenant Admin can perform read-only customer/ticket lookup and knowledge search within their tenant. Support Manager can use team-level customer/ticket lookup, knowledge search, and authorized team analytics. Support Agent can look up permitted tickets/customers, search knowledge, and request summaries/classifications for authorized tickets. Dashboard and predefined analytics access follows FR-AN-06. Enforce all permissions server-side. The permission matrix is centrally managed by Platform Admin; no custom roles or tenant overrides are supported.

**5.6 AI Support Analytics** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-AN-01  | Provide a basic dashboard for ticket counts by status, category, and priority, scoped according to FR-AN-06.  |
| FR-AN-02  | Show ticket-volume trends for predefined 7-day and 30-day ranges. SLA indicators are deferred until definitions, business calendars, time zones, and required fields are established.  |
| FR-AN-03  | Support a small set of natural-language questions through predefined allowlisted analytics functions, scoped according to FR-AN-06.  |
| FR-AN-04  | Summaries identify their data scope and time range.  |
| FR-AN-05  | Arbitrary text-to-SQL is out of scope; any later exploration requires read-only access, validation, row limits, and tenant scoping.  |
| FR-AN-06  | Apply these scopes to dashboards, ticket-volume trends, and predefined natural-language analytics: Tenant Admins may access ticket data within their tenant; Support Managers may access ticket data for their assigned teams; Support Agents may access only their own authorized-ticket data; Platform Admins may access aggregate analytics for exactly one explicitly selected authorized tenant, with no cross-tenant view and no access through analytics to underlying tenant business records. Enforce these scopes server-side and identify the applicable scope in each result.  |
 

**5.7 AI Evaluation and Testing** ****

| **ID**  | **Requirement**  |
| --- | --- |
| FR-EV-01  | Include a versioned evaluation set with expected source documents and answer characteristics, plus synthetic ticket scenarios for summary, classification, priority, and structured-output evaluation.  |
| FR-EV-02  | Record dataset version, run date/status, total samples, retrieval, answer, citations, latency, model/deployment, prompt version, metric numerators/denominators, individual results, failures, and baseline comparison.  |
| FR-EV-03  | Assess retrieval relevance, grounding, citation correctness, and no-answer behavior.  |
| FR-EV-04  | Compare prompt/model changes against a baseline run.  |
| FR-EV-05  | Include ambiguous questions, missing/conflicting knowledge, prompt injection, and cross-tenant/team access tests.  |
| FR-EV-06  | Treat evaluation results as decision support, not proof of correctness; document thresholds and limitations.  |
 
The following are **proposed initial evaluation targets and measures** for measurement and comparison, not release gates. They remain non-gating after Human Requirement Approval unless a separate, explicit human decision changes their status:

| Evaluation area | Proposed initial target | Measurement / limit |
| --- | --- | --- |
| Retrieval quality | Recall@5 >= 80% | For each query with labeled relevant sources, score relevant sources retrieved in the top five / all labeled relevant sources for that query; report the per-query values, macro-average, and query/source denominators. Report no-answer queries separately. |
| Grounding | Grounded Answer Rate >= 90% | Human reviewers label each factual claim in a non-abstained answer. Score supported factual claims / total evaluated factual claims × 100; unsupported, contradicted, or unverifiable claims are not supported. Evaluate correct abstentions separately. |
| Citation correctness | Citation Precision >= 95% | Score citations that resolve to the correct authorized source and support the associated claim / total citations emitted × 100. Broken, incorrect, irrelevant, or non-supporting citations are incorrect. If none are emitted, report not applicable rather than 100%. |
| Citation coverage | No initial percentage threshold | Score factual claims requiring attribution with at least one correct supporting citation / all factual claims requiring citation × 100. Report separately from citation correctness. |
| Abstention | 100% correct on the initial 10 no-answer cases | Count a case as correct only when missing, conflicting, stale, or insufficient approved evidence produces a clear no-answer response without unsupported claims or fabricated citations; report correct cases / tested no-answer cases. |
| Structured output | Measurement only; no percentage release threshold | Initial invalid output rate = invalid first-attempt outputs / total structured-output attempts. Final unrecoverable invalid rate = outputs still invalid after permitted retries / total attempts. Record both; validate syntax, required fields, types, enums, schema, and business rules. Invalid outputs are rejected or safely retried and must never corrupt persisted data. |
| Prompt-injection handling | 100% safe handling of the initial 10 cases | Report safely handled cases / tested cases; unsafe means unauthorized tool execution, cross-tenant disclosure, secret exposure, or policy bypass. |

Tenant, team, and role authorization is a mandatory acceptance criterion independent of these evaluation percentages: any successful unauthorized access fails acceptance. The initial evaluation sets are small and do not establish production-level accuracy or security assurance. Record dataset version, model/deployment and prompt versions, run date/status, total samples, metric numerators and denominators, initial failures, final outcomes, limitations, and comparisons with the previous baseline; rerun after material model, prompt, retrieval, or configuration changes. Numeric cost budgets and model-specific token limits remain deferred.

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
| FR-OP-09  | Persist asynchronous job state and tenant/requester context; authorize and revalidate cancellation, status, and result access under section 5.14; prevent cancelled or partial results from being persisted or exposed as completed.  |
| FR-OP-10  | Enforce tenant and team authorization on all APIs, retrieval, background execution, and stored results; unlisted access is denied.  |
 

**5.9 Identity and Administrative Management** ****

| ID | Requirement |
| --- | --- |
| FR-ID-01 | Authenticate users locally using ASP.NET Core Identity. Microsoft Entra ID and enterprise SSO are deferred. |
| FR-ID-02 | Platform Admin can create, view, update, activate, and deactivate tenants and provision the initial Tenant Admin account for each tenant. |
| FR-ID-03 | Platform Admin can manage users across tenants. Tenant Admin can create, view, edit, activate, and deactivate users within their tenant and assign/change only permitted predefined roles. Self-registration is disabled. |
| FR-ID-04 | Implement predefined Platform Admin, Tenant Admin, Support Manager, and Support Agent roles through a centralized, explicit, resource/action permission matrix. |
| FR-ID-05 | Platform Admin can manage system-wide mappings for the predefined roles and view the permission matrix. Tenant Admin can view the permission matrix and global operational/retention settings but cannot modify them or grant Platform Admin privileges. Support Manager and Support Agent cannot manage RBAC configuration. |
| FR-ID-06 | Prevent privilege escalation and enforce tenant and role authorization on every relevant backend API and data-access path. |
| FR-ID-07 | Audit tenant administration, user creation/activation/deactivation, role changes, and permission-matrix changes. |
| FR-ID-08 | Use ASP.NET Core Identity built-in local password change and reset; use a configurable minimum password length of 12 characters and an initial proposed reset-token validity of 30 minutes. |
| FR-ID-09 | Minimize and audit Platform Admin access to tenant data; Platform Admin assistant retrieval is limited to FR-AN-06 aggregate analytics for exactly one explicitly selected authorized tenant; it must not retrieve tenant knowledge documents or underlying tenant business records. |
| FR-ID-10 | Use configurable ASP.NET Core Identity lockout defaults of 5 consecutive failed attempts and 15 minutes; apply rate limits, prevent permanent lockout through repeated failures, and audit lockout/unlock events. |
| FR-ID-11 | Return equivalent password-reset responses for existing and non-existing accounts; deliver a protected, single-use HTTPS reset link only to the registered address and never log its token or full URL. |
| FR-ID-12 | Include self-service password recovery and successful password-change confirmation using real transactional email in the first release; on delivery failure, surface a safe failure and allow controlled retry rather than reporting false success. |
| FR-ID-13 | Permit only role-scoped account recovery: Tenant Admin may initiate/reset instructions for users in their tenant but cannot view or set passwords; Platform Admin recovery/unlock is authorized and audited; users may recover their own account. |
| FR-ID-14 | A deactivated user account is not eligible for password reset until a separate authorized reactivation. Password reset must not reactivate a deactivated user or tenant; reactivation requires a separate authorized activation action. |
| FR-ID-15 | Changes to Platform Admin permissions and defined privileged platform access remain pending until an independent second Platform Admin approves; the initiator cannot approve or elevate themselves. |
| FR-ID-16 | Provide explicit Feedback/Read in the centralized versioned default-deny permission catalogue. Tenant Admin may read feedback in their tenant; Support Manager may read feedback submitted by users in assigned teams; Support Agent may read only their own submissions. Platform Admin has no routine access to individual tenant feedback/comments, except already-permitted aggregate analytics. Return only Feedback ID, rating, optional reason, submitting User ID and time, associated conversation/message ID, and Tenant ID; do not grant conversation-history or message-content access. Enforce server-side and audit reads while minimizing sensitive data. |
| FR-ID-17 | Mask Customer email for Platform Admin, Support Manager, and Support Agent. Tenant Admin may view the full registered email only for a Customer in their own tenant through an explicitly authorized Customer-detail operation. Enforce masking in every API, search, AI-tool, and lookup path and audit every full-email access with actor, tenant, Customer ID, timestamp, action, outcome, and correlation ID; do not unnecessarily expose full email in logs, prompts, indexes, or unauthorized responses. |

Maintain a centralized, versioned permission catalogue and default-deny resource/action mappings for Tenant (Create, Read, Update, Activate, Deactivate), User (Create, Read, Update, Activate, Deactivate), Customer (Read, Search), Feedback (Read), Role (Read, Assign), Permission Matrix (Read, Update), Operational Settings (Read, Update), Retention Policies (Read, Update), Knowledge Documents (Create, Read, Update, Approve, Reject, Reprocess, Delete), Tickets (Create, Read, UpdateSubjectDescription, Assign, Reassign, Escalate, ChangeStatus, ChangePriority, ChangeCategory, RequestTicketFieldCorrection, DecideTicketFieldCorrection, RequestTicketCancellation, DecideTicketCancellation), Background Jobs (ReadStatus, ReadResult, Cancel), Conversations (ReadOwnHistory), Teams (Read, ManageMembership, AssignTickets), Analytics (ReadTenant, ReadTeam, ReadOwn), and Audit (ReadPlatform, ReadTenant, ReadTeam, ReadOwn). Enforce each mapping with tenant, team, resource, action, and owner scope at the backend. Conversation history is readable only by its owner, regardless of role. Ticket Update is limited by the explicit field and workflow rules in section 5.10; it is not unrestricted object update. Tenant Admin has tenant-wide ticket management, user/team/knowledge administration, and tenant analytics/audit access, but cannot assign Platform Admin. Support Manager is limited to assigned teams and cannot change membership. Support Agent belongs to one primary team and cannot assign/reassign tickets. Platform Admin has no routine unrestricted access to tenant business content. The Platform Admin assistant is limited to the single-selected-tenant aggregate-analytics scope in FR-AN-06 and cannot retrieve tenant knowledge documents or underlying tenant business records. For changes to Platform Admin permissions or other defined privileged platform access, require a second independent authorized Platform Admin; the initiator cannot approve, and changes remain pending if no independent approver is available. Preserve immutable security controls and protected audit records. Record initiator, approver, reason, and before/after permission values.

Analytics permission mapping: Tenant Admins use Analytics/ReadTenant only for ticket data within their tenant; Support Managers use Analytics/ReadTeam only for assigned teams; Support Agents use Analytics/ReadOwn only for their own authorized-ticket data. Platform Admins use Analytics/ReadTenant only for aggregate analytics of one explicitly selected authorized tenant, never for cross-tenant views or access to underlying tenant business records, as specified in FR-AN-06.

Customer permission mapping: Tenant Admins may use Customer/Read and Customer/Search only within their tenant. Support Managers may use these actions only for Customers associated with tickets in explicitly assigned teams, including team-assigned tickets with no Agent; they may not access completely unassigned tickets or other teams' tickets. Support Agents may use these actions only for Customers associated with tickets currently assigned to them, with no exception or separate grant mechanism; revoke access immediately on reassignment or loss of team/tenant/ticket scope. Platform Admin has no routine Customer Search or unrestricted lookup; separately authorized investigations must be audited and do not provide full-email access. The Platform Admin assistant cannot use Customer/Read or Customer/Search and may use only the FR-AN-06 single-selected-tenant aggregate-analytics scope. Revalidate each action server-side, including direct-ID lookup.

Feedback permission mapping: Tenant Admins may use Feedback/Read only for their tenant; Support Managers may use Feedback/Read only for feedback submitted by users in their assigned teams; Support Agents may use Feedback/Read only for their own submissions. Platform Admin has no routine individual tenant Feedback/Read permission and may access only already-permitted aggregate analytics. Feedback/Read returns only the fields listed in FR-ID-16 and does not authorize reading conversation history or message content. Enforce and audit access server-side.

Customer email access mapping: Search and lookup return masked email for every role. Only Tenant Admin may see a full registered email address in an explicitly authorized Customer-detail operation for that Admin's own tenant. All other roles, including Platform Admin, Support Manager, and Support Agent, receive masked email only. Enforce this boundary across API, search, AI tools, and lookup, and audit every full-email access as specified in FR-ID-17.

Use the built-in ASP.NET Core Identity password and reset-token mechanisms; never store recoverable passwords or use custom reset tokens. Configure the initial minimum password length at 12 characters, reset-token validity at 30 minutes, and lockout at 5 consecutive failures for 15 minutes; keep values configurable. Apply supported password-reuse and compromised-password protections. Use generic reset responses, rate-limit authentication/recovery endpoints, require HTTPS, invalidate used/expired tokens, revoke supported existing sessions after a successful reset, notify the user of a successful change, and require a fresh login. Platform Admin may support authorized recovery/unlock but cannot view passwords or bypass token validation. Tenant Admin may initiate or resend recovery for their own tenant only. Active users may recover their own account; deactivated user accounts are ineligible for reset until separately reactivated. Audit recovery, repeated failures, lockouts, and administrative unlocks without recording credentials or tokens.

**5.10 Core Ticket Management** ****

| ID | Requirement |
| --- | --- |
| FR-TM-01 | Provide a complete internal ticket lifecycle over synthetic demo data: create, list, view details, edit authorized information, assign/reassign, change authorized category/priority/status, escalate, resolve, close, reopen, and cancel through the explicit workflow below. |
| FR-TM-02 | Support search, filtering, sorting, and pagination for ticket lists. |
| FR-TM-03 | Scope ticket ownership, visibility, and actions by tenant, team, role, and individual assignment; enforce permissions at the API. |
| FR-TM-04 | Record ticket activity history and audit creation, edits, Category/Priority correction requests and decisions, assignment/reassignment, status changes, escalation, resolution, closure, reopening, cancellation requests and decisions, and administrative actions. |
| FR-TM-05 | Use initial statuses New, Open, In Progress, Pending Customer, Resolved, Closed, and Cancelled; categories Account & Access, Billing & Payments, Technical Issues, Product Setup, and General Support; and priorities Critical, High, Medium, and Low. Treat escalation as a separate flag, not a status. |
| FR-TM-06 | Use these proposed category-based default queue recommendations: Account & Access to Account & Access Queue; Billing & Payments to Billing Queue; Technical Issues to Technical Support Queue; Product Setup to Product Setup Queue; and General Support to General Support Queue. Queue assignment and escalation are subject to authorization and human review. |
| FR-TM-07 | Platform Admin owns the initial system-wide ticket taxonomy and queues but has no routine tenant ticket-business access. Tenant Admin can view, manage, and route tickets across their tenant, including completely unassigned tickets (neither team nor Agent assigned), and owns central triage within that tenant. Support Manager manages tickets and assignments only within assigned teams, including team-assigned tickets without an Agent; Managers cannot access completely unassigned tickets or other teams' tickets. Support Agent can create tickets, edit Subject and Description on tickets they are authorized to access, request Category/Priority corrections and escalation, and submit ticket-cancellation requests; Agents cannot assign/reassign tickets, directly change Category/Priority, finalize cancellation, or modify the system taxonomy. All unspecified fields and actions are denied by default. |
| FR-TM-08 | Support additional synthetic tickets created through the application; do not connect real external customer or ticketing systems in the first release. |
| FR-TM-09 | Permit ticket cancellation only from New, Open, In Progress, or Pending Customer; require a predefined cancellation reason and mandatory explanatory notes. An Agent may submit a persisted cancellation request but cannot finalize it; an authorized Tenant Admin or Support Manager decides the request under the workflow below. |
| FR-TM-10 | Treat Cancelled as terminal, distinct from Resolved/Closed, not as deletion; exclude cancelled tickets from successful resolution/closure metrics and retain their history under the cancelled-ticket retention period. |
| FR-TM-11 | Require a resolution summary before resolution and valid resolution information before closure; require a reason for reopening; preserve prior values and append activity rather than overwrite history. |
| FR-TM-12 | Do not permit permanent ticket deletion by Tenant Admin, Support Manager, or Support Agent in the first release. |
| FR-TM-13 | Restrict direct Support Agent ticket edits to Subject and Description on tickets the Agent is authorized to access. Agents must not modify TicketId, TenantId, CustomerId, AssignedTeamId, AssignedAgentId, CreatedAt, UpdatedAt, or other system-managed fields; assign/reassign tickets; or directly change Category or Priority. Status, resolution, escalation, reopening, cancellation, and Category/Priority actions use their explicit authorization and workflow rules; unspecified fields and actions are denied by default. |
| FR-TM-14 | Permit direct Category/Priority changes only as separate authorized actions: Tenant Admin for tickets in their tenant and Support Manager for tickets assigned to their teams, including team-assigned tickets without an individual Agent. Agents cannot directly change these values and may submit a tracked correction request. Permit changes only in New, Open, In Progress, or Pending Customer; use only the defined category taxonomy and priority values; preserve prior values and audit each change. |

****Ticket transition and action rules:** New → Open is allowed only for: a Support Agent currently assigned to the ticket who retains valid primary-team and tenant authorization; a Support Manager when the ticket belongs to one of the Manager's currently assigned teams, including a team-assigned ticket without an individual Agent; or a Tenant Admin for any ticket in that Admin's tenant, including a completely unassigned ticket, under the existing tenant-wide ticket management and central-triage authority. Platform Admin cannot perform routine tenant ticket-business status transitions. Ticket creation alone grants no permission to make this transition; a ticket creator must independently satisfy the applicable role, assignment, tenant, and team requirements. Revalidate current user authorization, ticket tenant, team, assignment, and status on every transition; deny unauthorized requests and all undefined transitions by default. Record each successful transition in ticket activity history and audit logs. Open → In Progress is allowed for the assigned Agent or assigned-team Manager. In Progress → Pending Customer, Resolved, or Open and Pending Customer → In Progress or Resolved are allowed for the assigned Agent or assigned-team Manager; Tenant Admin may perform authorized tenant-level status actions. Resolved → Closed is allowed only for a Support Manager in the assigned team or the Tenant Admin. Resolved → Open and Closed → Open (reopen) are allowed only for those same roles and require a reason. Closure is only from Resolved; Open → Closed is prohibited. Require resolution summary/notes before resolution and valid resolution summary before closure. Closed tickets are read-only for normal Agent operations. Escalation preserves underlying status and is auditable; Agents may request it, while authorized Managers may execute it, record a reason, adjust priority only as permitted by the Category/Priority role and state rules below, and route to an appropriate team or higher-level support queue. Tenant Admin can manage tenant tickets, assignments, status actions, escalation, resolution, closure, and reopening subject to the explicit transition rules. Platform Admin has no routine ticket-business action permission.

Cancellation transitions are New → Cancelled, Open → Cancelled, In Progress → Cancelled, and Pending Customer → Cancelled. Tenant Admin may approve or reject cancellation requests for any ticket in their tenant; Support Manager may approve or reject requests for tickets assigned to their teams, including team-queued but unassigned tickets. An Agent may submit a request only for a ticket they are authorized to access and cannot approve, reject, or directly finalize cancellation. Persist each request separately with Pending Approval, Approved, or Rejected status; capture ticket ID, requester, one reason from Customer Withdrawn, Duplicate Ticket, Created in Error, No Longer Required, or Other, mandatory explanatory notes, timestamps, and decision details. The ticket's status, assignment, and other authoritative fields remain unchanged while pending. Approval by an authorized Tenant Admin or Support Manager transitions the ticket to Cancelled; rejection leaves the ticket unchanged and records the rejection reason. Prevent duplicate active pending cancellation requests for the same ticket. Enforce tenant, team, role, ticket, and state authorization at the backend. Preserve requester, approver/rejector, decision, reason, timestamps, previous ticket status, and outcome in the audit trail. Resolved → Cancelled, Closed → Cancelled, and any transition out of Cancelled are prohibited. If support is needed later, create a new linked ticket.

Category/Priority changes are separate authorized actions, not unrestricted ticket edits. Tenant Admin may change either value for any ticket within their tenant; Support Manager may change either value only for tickets in their assigned teams, including team-assigned tickets without an individual Agent; Support Agent may not directly change either value; Platform Admin owns the system-wide taxonomy and queues but has no routine permission to modify tenant business tickets. A direct change is allowed only while the ticket is New, Open, In Progress, or Pending Customer. Category must use the predefined system taxonomy and Priority must be Critical, High, Medium, or Low. Enforce role, tenant, team, state, and value validation at the backend. Preserve the previous and updated value and record actor, tenant, ticket ID, old value, new value, timestamp, and correlation ID in activity/audit history. Reject changes to Resolved, Closed, or Cancelled tickets.

An Agent may submit a Category/Priority correction request only for a ticket they are authorized to access. Persist each request separately with Pending Approval, Approved, or Rejected status; capture ticket ID, tenant ID, requested field, current and proposed values, mandatory correction reason, requesting Agent and submission timestamp, and approval/rejection decision, approver, timestamp, and decision reason. Support Managers may approve or reject requests only for tickets in their assigned teams, including team-assigned tickets without an individual Agent; Tenant Admins may decide requests for tickets in their tenant; Agents cannot approve or reject. The original value remains unchanged while pending. On approval, revalidate the approver's permissions and current ticket state before applying the proposed value; on rejection, retain the original value and record the rejection reason. Reject duplicate active pending requests for the same ticket and field. Requests may be approved only while the ticket is New, Open, In Progress, or Pending Customer; Resolved, Closed, and Cancelled tickets cannot be modified. Preserve prior and updated values, requester, approver, decision, reason, timestamp, tenant, ticket ID, and correlation ID in audit/activity history; enforce tenant, team, role, ticket, and field-level authorization at the backend and handle concurrent requests/state changes safely. Provide Agent submission UI, Manager/Tenant Admin review UI, APIs, persistence, audit history, and automated tests.

Keep ticket assignment as separate AssignedTeamId and AssignedAgentId relationships; a team assignment may exist without an Agent assignment. A Support Agent may be assigned only to a ticket whose AssignedTeamId is that Agent's single current primary support team; no cross-team assignment exception, temporary access mechanism, separate approval authority, or additional permission/grant mechanism exists in the first release. Managers can assign/reassign only within their assigned teams and only to eligible Agents belonging to the ticket's assigned team. Tenant Admin may route tickets across teams within their tenant but may assign an Agent only when that Agent belongs to the ticket's assigned team. The existing Tenant Admin role owns central triage and can view/manage/route tickets that are completely unassigned (neither team nor Agent assigned), only within their tenant. Managers cannot access globally unassigned tickets or other teams' tickets. No new central-triage role, permission, or separate granting authority is introduced. Platform Admin has no routine tenant ticket-business access. Enforce server-side tenant and team-membership validation for every assignment and reassignment; deny and audit unauthorized assignments. Immediately revoke Agent access when the Agent is reassigned, loses primary-team membership, or otherwise loses required tenant, team, or ticket authorization. If a team-membership change results in ticket assignment changes, validate and audit each resulting assignment. The initial ticket fields include TicketId, TenantId, CustomerId, Subject, Description, Status, Category, Priority, AssignedTeamId, AssignedAgentId, CreatedAt, and UpdatedAt.

**5.11 Operational Limits, Retention, and Deletion** ****

The first release provides validated, centralized, configurable operational settings in the administrative console. Platform Admin owns global configuration; Tenant Admin has view-only access. Changes are validated before application, versioned, and audited.

Initial proposed operational defaults:

| Setting | Initial value |
| --- | --- |
| General API rate limit | 60 requests per user per minute |
| AI request limit | 10 requests per user per minute |
| Concurrent AI requests | 2 per user |
| General API timeout | 30 seconds |
| AI model timeout | 60 seconds initial proposed default, configurable independently from the general API timeout |
| Background job timeout | Configurable, bounded by operation type and provider constraints; independent from API/model defaults |
| Maximum document upload | 20 MB per file |
| Conversation context | Most recent 10 turns |

Validate upload extension, MIME/content type, actual content, processing outcome, and size; reject unsupported, corrupted, or oversized files clearly. Enforce configured input/output token limits based on the selected model. Exact model-specific token limits and monthly monetary cost budgets remain deferred until model selection, pricing, quota, and subscription validation.

Initial proposed retention and deletion defaults (configurable; not legal or regulatory commitments):

| Data | Retention / deletion behavior |
| --- | --- |
| Active tickets | While active. |
| Closed tickets | 365 days after closure. |
| Cancelled tickets | 365 days after cancellation, using the same configurable period as closed tickets. |
| Customer records | When a Customer has one or more related tickets, retain it until all are terminal (Closed or Cancelled), then start or reset the configurable 365-day period from the latest related ticket terminal-transition timestamp. When a Customer has no related tickets, start the configurable 365-day period at Customer.CreatedAt. If a ticket becomes associated during a running 365-day period, suspend pending cleanup eligibility. Never purge while any related ticket is active. Once all related tickets are terminal, restart the 365-day period from the latest terminal-transition timestamp. Revalidate current relationships and eligibility immediately before deletion; cleanup remains ineligible until all related tickets are terminal and the applicable period has elapsed. |
| Active users | While the account remains active. |
| Deactivated user records | 365 days after deactivation; preserve historical attribution, except that approved permanent deletion of the tenant after its 30-day grace period and required independent second Platform Admin approval overrides this retention period. |
| User activity records | 365 days. |
| Ticket activity/history and ticket workflow requests | With the associated ticket, subject to ticket retention. |
| Customer feedback | 90 days. |
| Ticket AI results | 90 days. |
| Conversations | 90 days. |
| Application logs | 30 days; no passwords, secrets, or unnecessary sensitive content. |
| Security and administrative audit logs | 365 days, independent of ordinary business-data deletion. |
| Evaluation data and results | 90 days; synthetic data only. |
| Backups | Maximum 30 days; reapply deletion records after restoration. |
| Original knowledge documents and versions | While active; delete under the approved document deletion workflow. |
| Extracted text, chunks, and embeddings | While associated knowledge is active; make unavailable to retrieval immediately on deletion or loss of approval. |
| Deleted knowledge and derived data | Immediately unavailable to search/RAG; physically purge primary storage and indexes within 30 days. |

Platform Admin manages configurable global policies and cleanup operations; Tenant Admin can view applicable policies and delete authorized tenant documents but cannot modify global policies. Support Managers and Agents have no retention administration permissions. Validate, version, and audit policy changes; show pending/completed/failed cleanup. Preserve minimal deletion metadata without retaining deleted content.

**Tenant lifecycle and deletion:** Deactivation immediately blocks authentication, API/application access, RAG/search results, and new tenant processing; safely stop tenant-specific scheduled operations while preserving retained data and audit history. Reactivation requires a separate authorized Platform Admin action. A Tenant Admin may request deletion. Platform Admin reviews it, then a different independent authorized Platform Admin must approve permanent deletion. The tenant enters deactivated/pending-deletion state and all access is revoked during a 30-day grace period. A reversal during that grace period requires approval by two independent Platform Admins before purge begins; self-approval is prohibited. After the required grace period and independent second Platform Admin approval, permanent deletion overrides the 365-day retention period for deactivated-user records in that tenant and purges eligible personal information and business/derived data from primary records, Blob Storage, Search indexes/embeddings, conversations, feedback, and related artifacts. Backups expire within 30 days. Independently of ordinary business-data deletion, preserve only minimum necessary protected security/administrative audit metadata for attribution and accountability under the existing independent audit policy and access controls. This metadata may include the original or irreversibly pseudonymous actor ID, approver, action/resource IDs, relevant permission before/after values, tenant-deletion approval/execution timestamps, outcome, and correlation ID as applicable. Never retain passwords, authentication tokens, personal email addresses, unnecessary personal data, or deleted business/customer content in this metadata. Audit metadata must not restore or reconstruct tenant/business records. If required independent approval is unavailable, deletion or reversal remains pending.

**5.12 Administrative Activity and Audit** ****

Maintain separate application logs, security audit logs, administrative audit logs, and ticket activity history. Record authentication/access-control events; user and tenant lifecycle; role and permission changes; privileged-change initiator/approver and before/after values; retention changes; knowledge upload, approval/rejection, reprocessing, and deletion; ticket edits, Category/Priority correction requests and decisions, transitions, resolution, closure, reopening, cancellation requests and decisions, escalation, and assignments; background-job cancellation actor, tenant, job ID, timestamp, outcome, and correlation ID; analytics access; Customer Search, lookup, detail, and full-email unmasking; Feedback Read; authorized tool execution; email delivery outcomes; and cleanup outcomes. Include actor, tenant, resource identifier, action, timestamp, outcome, and correlation ID where applicable. Audit every full-email access with actor, tenant, Customer ID, timestamp, action, outcome, and correlation ID. Do not log passwords, tokens, secrets, full email unnecessarily, deleted customer/business content, unnecessary personal data, or sensitive prompt data. Protect security/audit records from unauthorized modification/deletion and audit access to audit records.

Audit access is scoped: Platform Admin may read platform security, privileged administration, tenant lifecycle, and platform audit data; Tenant Admin may read their tenant's user, role, knowledge, retention, and ticket audit; Support Manager may read authorized team ticket activity; Support Agent may read their own permitted ticket/personal activity. Enforce these scopes server-side. Retain security and administrative audit logs for a proposed 365 days independently of ordinary business-data deletion.

**5.13 Support Team Management** ****

| ID | Requirement |
| --- | --- |
| FR-TEAM-01 | Tenant Admin can create, view, edit, activate, and deactivate teams only within their tenant; every team belongs to exactly one tenant. |
| FR-TEAM-02 | Tenant Admin manages team membership and assigns one primary Support Manager to each team; a Support Manager may manage one or more teams. |
| FR-TEAM-03 | Each Support Agent belongs to exactly one primary support team in the first release. A Tenant Admin may change an Agent's primary team only through the authorized tenant-scoped team-membership workflow. On a primary-team change, immediately re-evaluate Agent authorization and revoke access outside the Agent's current ticket/team/tenant scope. If any ticket assignments change as a result, validate each assignment server-side against current tenant and team membership and audit it. Multi-team Agent membership and dynamic team hierarchies are deferred. |
| FR-TEAM-04 | Support Managers may view their assigned team membership but cannot create or change team structures or membership. |
| FR-TEAM-05 | Team membership changes, manager assignments, team lifecycle, and ticket assignments are authorized, tenant-scoped, validated server-side against current team membership, and audited. |
| FR-TEAM-06 | Revalidate team membership on access and modification; team deactivation does not delete historical tickets/audit and requires existing assignments to be reviewed and safely reassigned. Platform Admin has oversight but does not routinely manage tenant team membership. |

Support Managers can see all tickets assigned to their teams, including tickets not yet assigned to an individual Agent, and may assign/reassign those tickets to eligible team Agents. They cannot see or modify completely unassigned tickets or other teams' tickets; no separate exception or grant mechanism exists in the first release. Tenant Admin can view, manage, and route all tickets within their tenant and owns central triage for tickets with neither team nor Agent assignment. Platform Admin has no routine tenant ticket-business access. Enforce these boundaries server-side and audit access and routing.

**5.14 Persisted Asynchronous Jobs** ****

Use persisted background jobs for potentially long-running RAG chat/answer generation, ticket summary/classification/priority/sentiment/urgency suggestions, reply drafts, knowledge extraction/chunking/embedding, reprocessing, and bulk indexing. Simple CRUD, authentication, authorization, customer/ticket lookup, and job status queries remain synchronous under a 30-second default general API timeout. Submission validates authorization, stores tenant/requester/operation context, creates a unique job, and returns HTTP 202 Accepted with Job ID and status endpoint; status polling must not rerun work.

Persist job states Queued, Processing, Completed, Failed, Timed Out, and Cancelled. Include authorized user-initiated cancellation in the first release. Tenant Admin may cancel jobs within their tenant. Support Manager may cancel jobs associated with their assigned teams, subject to resource authorization. Support Agent may cancel a job they initiated only while they remain authorized to access its associated ticket, team, or resource. Platform Admin has no routine unrestricted permission to cancel tenant jobs; all unlisted permissions are denied by default. Provide an authorized cancellation endpoint, illustratively `POST /api/jobs/{jobId}/cancel`, and revalidate tenant, role, team, requester, and associated-resource permissions on every request.

Queued jobs must transition to Cancelled immediately without starting execution. A Processing job must accept a cancellation request and stop cooperatively at the next safe checkpoint; workers must not persist cancelled or partially generated results or perform subsequent processing steps. If processing has completed and its result was committed before cancellation takes effect, preserve Completed. Completed, Failed, Timed Out, and already Cancelled jobs cannot be cancelled. Cancellation requests must be idempotent and handle concurrent state changes safely. Persist the cancellation state and audit actor, tenant, job ID, timestamp, outcome, and correlation ID. Display clear cancellation status and safe errors in the UI. Model and background-processing timeouts are independently configurable and bounded; use bounded exponential-backoff retries only for eligible transient errors/throttling. Avoid duplicate jobs or business effects on retry, and do not retry permanent validation/authorization failures. Revalidate authorization for status/result retrieval; prevent cross-tenant access. Log latency/retries/failure with correlation IDs. Streaming, advanced notifications, and distributed orchestration enhancements are deferred.

**5.15 Transactional Email Delivery** ****

Include one real email provider in the first release for password recovery, successful password-change confirmation, and only the explicitly approved transactional notifications listed below. Integrate through SMTP or the provider's supported API behind a configurable service abstraction; Azure Communication Services Email or SendGrid are acceptable, and the final provider is chosen during implementation based on cost, reliability, security, and deployment compatibility. Use environment-specific sender/provider configuration and verified sender domains. Development/testing delivery is restricted to controlled test-account allowlists; demo/production delivery is to registered users. Store credentials in a managed secret store, require HTTPS reset links, rate-limit email-triggering endpoints, and use bounded retries for eligible transient errors. Do not log tokens, complete reset URLs, passwords, or provider secrets. Record safe delivery status, timestamp, message correlation ID, and error metadata; accepted submission is not proof of inbox delivery. On provider failure, return a safe error and permit controlled retry rather than silent success. Enforce RBAC and tenant isolation for every email-triggering operation and audit the outcome.

The approved first-release notification events and recipients are:

1. Ticket cancellation request submitted: notify the active Support Manager assigned to the ticket's team; if no active assigned Manager is available, notify the authorized Tenant Admin.
2. Ticket cancellation approved or rejected: notify the requesting Support Agent; include the rejection reason where appropriate.
3. Ticket assigned or reassigned: notify the newly assigned Support Agent.
4. Ticket escalated: notify the receiving team's assigned Support Manager.
5. Ticket reopened: notify the currently assigned Support Agent.
6. Knowledge document version approved or rejected: notify the uploader; include the rejection reason where appropriate.
7. User account activated or deactivated: notify the affected registered user. A security notification about deactivation may be delivered to the affected user even though the account is no longer active.
8. Platform Admin privileged permission change pending approval: notify the independent authorized second Platform Admin.
9. Platform Admin privileged permission change approved or rejected: notify the initiating Platform Admin.

Password recovery and successful password-change confirmation remain mandatory identity-related email events. Resolve recipients using current tenant, team, role, assignment, and authorization information. Send only to eligible active users with registered email addresses, except for the specified deactivation security notification; prevent duplicate emails to users with multiple eligible roles. Do not expose unnecessary customer-sensitive information. Use configurable templates and record safe delivery status, timestamp, correlation ID, and failure metadata; apply bounded retries for eligible transient failures. Email provider submission is not guaranteed inbox delivery and must not be reported as such. Customer-facing messages must never be sent automatically by AI. Do not send emails for every ticket status change, AI job status update, or individual chat message. Any notification event not listed here requires explicit approval.
 
**6. Key User Workflows** ****

**6.1 Ask a Knowledge-Grounded Question** ****

1. User signs in and selects the appropriate workspace. 

2. API validates identity, role, tenant, request limits, and conversation context. 

3. Retrieval searches only the current, Tenant Admin-approved document versions that the user is authorized to access and returns ranked source references. 

4. The model receives the question and retrieved evidence under a grounding-focused prompt. 

5. The UI displays the answer and source references, or a clear no-answer response. 

6. User may submit feedback; relevant metadata is recorded for evaluation. 

**6.2 Ingest or Update a Knowledge Document** ****

7. Authorized user uploads a supported PDF, DOCX, or TXT document of no more than the configured 20 MB initial maximum and receives validation feedback and a persisted job ID when processing is accepted. 

8. API stores the file and creates a tenant-scoped document record and version. 

9. A persisted background job extracts text, chunks it, creates embeddings, and indexes the new version. 

10. The processed version remains unavailable to retrieval pending Tenant Admin approval; show its version and Pending Approval or Failed status with a safe error summary if needed. 

11. Tenant Admin approves or rejects the exact processed version. On replacement, reprocessing, or deletion, prior approval is invalidated and old/stale chunks are immediately unavailable to retrieval. 

**6.3 Generate a Ticket Reply** ****

12. Agent opens an authorized ticket. 

13. Agent requests a summary, classification, or suggested reply; the API returns HTTP 202 and a job ID for long-running work. 

14. System retrieves relevant knowledge and authorized ticket context. 

15. The authorized user polls or receives job status; the model result is validated, persisted, and returned through an authorized job result endpoint, labeled AI-generated. 

16. Agent reviews, edits, accepts, or discards the suggestion. 

17. No customer message is sent without a separate explicit human action; AI never performs ticket mutations. 
 
**6.4 Administer a Tenant and Users** ****

1. Platform Admin creates or updates a tenant and provisions its initial Tenant Admin.
2. Tenant Admin creates and manages users within that tenant and assigns only permitted predefined roles.
3. The application enforces the centralized resource/action permission matrix on the backend and records administrative changes.
4. Self-registration is unavailable. Platform Admin manages global role mappings and configuration; privileged Platform Admin permission changes require independent second-admin approval. Tenant Admin cannot change global settings.

**6.5 Manage a Support Ticket** ****

1. An authorized user creates or opens a ticket with separate team and agent assignments.
2. The system enforces tenant, team, role, and individual assignment permissions for edits, assignment, category/priority/status changes, escalation, resolution, closure, reopening, and cancellation.
3. Tenant Admin manages tickets and routing across their tenant, including completely unassigned tickets (neither team nor Agent assigned) as the existing central-triage role. Support Manager acts only within assigned teams, including team-assigned tickets without an Agent, and cannot access completely unassigned or other-team tickets. Support Agent may edit only Subject and Description on authorized tickets, cannot assign/reassign or directly change Category/Priority, and uses the correction and cancellation request workflows below.
4. Category/Priority direct changes are limited to Tenant Admin within their tenant and Support Manager within assigned teams, for tickets in New, Open, In Progress, or Pending Customer. Agents submit a separate correction request; the existing value remains until an authorized approval.
5. Resolution requires a summary; closure is only from Resolved; reopening requires a reason; cancellation requires a reason and notes and is terminal. An Agent's cancellation request does not change the ticket while pending.
6. The system records ticket activity and audit metadata. AI suggestions remain separate from authoritative values until an authorized human acts.

**6.6 Administer Support Teams** ****

1. Tenant Admin creates a tenant-scoped team and assigns one primary Support Manager.
2. Tenant Admin assigns eligible Support Agents to exactly one primary team and can change membership.
3. Support Manager views assigned team membership but cannot modify it; Support Agent cannot access other team data.
4. Ticket and team membership changes are revalidated server-side and audited. Deactivating a team preserves history and requires assignment review.

**6.7 Recover a Local Account** ****

1. User requests a password reset by email and receives the same generic response whether the account exists or not.
2. Deactivated user accounts are ineligible for password reset until separately reactivated and receive no reset link. For an eligible active account, ASP.NET Core Identity sends a single-use HTTPS reset link to the registered address using the configured real email provider; responses remain generic as required by FR-ID-11.
3. The user resets the password with a valid token within the configured initial 30-minute lifetime; used/expired tokens are rejected and a fresh login is required.
4. Send a successful password-change confirmation to the user's registered email address.
5. Provider failure is surfaced safely and can be retried; no token, reset URL, password, or provider secret is logged. Password reset never reactivates a deactivated account.

**6.8 Deactivate or Delete a Tenant** ****

1. Authorized Platform Admin deactivation blocks tenant authentication, API, retrieval, and new processing while preserving retained data.
2. Tenant Admin may request deletion; Platform Admin reviews and a second independent Platform Admin approves permanent deletion.
3. Access is revoked during the 30-day grace period. Reversal requires two independent Platform Admin approvals before purge begins.
4. After the grace period and required independent second Platform Admin approval, cleanup purges eligible primary and derived tenant data, including deactivated-user records before their ordinary 365-day period expires, and is observable/retryable; backup copies expire within 30 days. Preserve only minimum necessary protected security/administrative audit metadata under the existing independent audit policy and access controls; it must not contain passwords, tokens, personal email addresses, unnecessary personal data, or deleted business/customer content, and must not restore tenant/business records.

**6.9 Submit and Retrieve a Long-Running Job** ****

1. The API validates the request and authorization, persists the tenant/requester/operation context, and enqueues one job.
2. It immediately returns HTTP 202 Accepted with Job ID and a status endpoint.
3. A worker processes the job and persists a validated result or safe failure under Queued, Processing, Completed, Failed, Timed Out, or Cancelled.
4. The client polls status without resubmitting work; every status/result request revalidates tenant and role authorization.
5. An authorized Tenant Admin, assigned-team Support Manager, or still-authorized initiating Support Agent may request cancellation under section 5.14. A Queued job is cancelled immediately; a Processing job stops at the next safe checkpoint without persisting or exposing partial results.
6. If processing and result commit complete before cancellation takes effect, preserve Completed. Reject cancellation for Completed, Failed, Timed Out, and Cancelled jobs; audit the cancellation outcome and show the final status.

**6.10 Request a Category/Priority Correction** ****

1. An authorized Support Agent selects Category or Priority on a ticket they may access, supplies the proposed value and mandatory correction reason, and submits a request.
2. The system persists a separate Pending Approval request with the ticket/tenant, field, current/proposed values, requester, reason, and timestamp. The ticket's authoritative value remains unchanged.
3. A Support Manager may approve or reject only for a ticket in an assigned team; a Tenant Admin may decide for any ticket in their tenant. Support Agents cannot decide. The system revalidates authorization and eligible ticket state when applying an approval.
4. Approval applies the proposed value only if the ticket remains eligible; rejection leaves the value unchanged and records the decision reason. Prevent duplicate active pending requests for the same ticket and field.
5. Record the request and decision in ticket activity/audit history with the required actor, tenant, ticket, previous/proposed values, reason, timestamps, outcome, and correlation ID. Provide Agent submission UI, Manager/Tenant Admin review UI, APIs, persistence, and automated tests.

**6.11 Request Ticket Cancellation** ****

1. A Support Agent with access to a ticket in New, Open, In Progress, or Pending Customer submits a cancellation request with one predefined reason and mandatory explanatory notes.
2. The system persists a separate Pending Approval request; the ticket's status, assignment, and other authoritative fields remain unchanged while pending. Prevent duplicate active pending requests for the same ticket.
3. A Tenant Admin may approve or reject any request in their tenant. A Support Manager may decide requests only for tickets in assigned teams, including team-assigned tickets without an individual Agent. Support Agents cannot approve, reject, or directly cancel.
4. Approval changes the eligible ticket to terminal Cancelled; rejection leaves the ticket unchanged and records a rejection reason. Resolved, Closed, and Cancelled tickets cannot be cancelled.
5. Record requester, approver/rejector, decision, reason/notes, timestamps, prior status, outcome, tenant, ticket ID, and correlation ID in audit/activity history. Provide request and approval/rejection UI, APIs, persistence, audit logging, and automated tests.

**6.12 Search and View a Customer** ****

1. An authorized user searches Customer ID by exact match, Display Name by partial case-insensitive match, and Company/Organization by partial case-insensitive match, with status and created-date-range filters.
2. The user may sort by Display Name ascending/descending or Created Date newest/oldest. The system validates the configurable maximum page size, applies authorization and filters before pagination, and returns total count and pagination metadata. Email is not searchable.
3. The server applies role and relationship scope before returning results and revalidates it for every request, including direct-ID lookup: Tenant Admin only within their tenant; Support Manager only Customers associated with tickets in assigned teams, including team-assigned tickets without an Agent; Support Agent only Customers associated with tickets currently assigned to that Agent. Platform Admin has no routine Customer Search.
4. Search and lookup responses return masked email for all roles. Only a Tenant Admin may see full registered email in an explicitly authorized Customer-detail operation for a Customer in that Admin's tenant. Reassignment or loss of applicable authorization immediately revokes Agent access. Every full-email access is audited; unauthorized ID probing, tenant-wide Agent browsing, or out-of-scope results are denied.

**6.13 Read Feedback** ****

1. An authorized reader requests feedback only within their permitted scope: Tenant Admin for their tenant, Support Manager for users in assigned teams, and Support Agent for their own submissions. Platform Admin has no routine access to individual tenant feedback/comments, except already-permitted aggregate analytics.
2. Return only Feedback ID, rating, optional reason, submitting User ID and time, associated conversation/message ID, and Tenant ID. Do not expose conversation history or message content.
3. Enforce scope on every request and audit reads while minimizing sensitive data.

**7. High-Level Architecture** ****

| **Layer**  | **Responsibility**  |
| --- | --- |
| React + TypeScript  | Chat, tenant/user administration, permission/configuration views, knowledge administration, ticket lifecycle, copilot, dashboard, feedback.  |
| .NET 8 Web API  | ASP.NET Core Identity local authentication and recovery; authorization boundary; tenant/team scoping; orchestration; validation; tool registry; administrative configuration; persisted job submission; persistence; API contracts.  |
| Azure AI model endpoint  | Answer generation, ticket summarization/classification, and structured responses.  |
| Azure AI Search  | Vector and/or hybrid retrieval over tenant-scoped, currently approved knowledge chunks only.  |
| Azure Blob Storage  | Original uploaded documents and optional processed artifacts.  |
| Azure SQL  | Tenants, teams/memberships, users/roles/permissions, document versions/approvals, persisted jobs, conversations, tickets/activity and workflow requests, customers, feedback, configuration, audit metadata, and evaluation runs.  |
| Background worker / Azure Functions  | Persisted AI/RAG/ticket/knowledge jobs, document extraction, chunking, embeddings, indexing, retries, status/result management, and cooperative job cancellation.  |
| Transactional email provider  | Real password recovery, successful password-change confirmation, and only the explicitly approved transactional notifications using a configurable provider abstraction and secured per-environment configuration.  |
| Key Vault / Application Insights  | Secret management; logs, traces, metrics, dependencies, and correlation.  |
| Administrative controls  | Centrally managed operational limits, retention/deletion policies, permission mappings, and auditable configuration history.  |
| GitHub Actions  | Build, test, configured security checks, and deployment workflow.  |
 

The API mediates model and search access. The browser must not receive provider keys or unrestricted service credentials. Use configuration abstractions for local and Azure environments. 

**8. Core Data Entities** ****

| **Entity**  | **Illustrative fields**  |
| --- | --- |
| Tenant  | TenantId, Name, Status, CreatedAt  |
| User / Membership  | UserId, TenantId, DisplayName, Role, Status, PrimaryTeamId where role is Support Agent  |
| SupportTeam / TeamMembership  | TeamId, TenantId, Name, Status, PrimaryManagerId; UserId, TeamId, Role, CreatedAt  |
| Role / Permission Mapping / Privileged Approval  | Role, Resource, Action, Permission, UpdatedBy, UpdatedAt; initiator, independent approver, reason, before/after values  |
| KnowledgeDocument / Approval  | DocumentId, TenantId, FileName, BlobUri, Version, Status, UploadedBy, CreatedAt, UpdatedAt; DocumentVersion, ApproverId, Decision, Reason, DecidedAt  |
| KnowledgeChunk  | ChunkId, TenantId, DocumentId, Version, Content, PageOrSection, SearchDocumentId  |
| Conversation / ChatMessage  | ConversationId, TenantId, UserId, Role, Content, CreatedAt, PromptVersion, ModelId  |
| Citation  | CitationId, MessageId, DocumentId, ChunkId, DisplayOrder  |
| Customer  | CustomerId, TenantId, DisplayName, CompanyName, AccountStatus, CreatedAt, Email (masked by default)  |
| Ticket  | TicketId, TenantId, CustomerId, Subject, Description, Status, Category, Priority, AssignedTeamId, AssignedAgentId, resolution/cancellation details, CreatedAt, UpdatedAt  |
| TicketActivity  | ActivityId, TenantId, TicketId, ActorId, Action, before/after values, reason, Timestamp, CorrelationId  |
| TicketFieldCorrectionRequest  | RequestId, TenantId, TicketId, RequestedField, CurrentValue, ProposedValue, Reason, RequesterId, Status, ApproverId, DecisionReason, SubmittedAt, DecidedAt, CorrelationId  |
| TicketCancellationRequest  | RequestId, TenantId, TicketId, RequesterId, CancellationReason, Notes, Status, DecisionActorId, DecisionReason, PreviousTicketStatus, SubmittedAt, DecidedAt, CorrelationId  |
| TicketAIResult  | ResultId, TicketId, Summary, SuggestedCategory, SuggestedPriority, SuggestedSentiment, ModelId, CreatedAt, ReviewedBy  |
| Feedback  | FeedbackId, TenantId, UserId, MessageId, Rating, Comment, CreatedAt  |
| ToolAudit / EvaluationRun  | AuditId, TenantId, ActorId, ToolName, Outcome, CorrelationId; RunId, DatasetVersion, PromptVersion, ModelId, Metrics, Status  |
| OperationalSetting / RetentionPolicy  | Setting/policy name, value, version, updated by/time, audit reference  |
| BackgroundJob  | JobId, TenantId, RequesterId, OperationType, State, CreatedAt, UpdatedAt, CorrelationId, safe result/error reference; cancellation outcome is auditable  |
| EmailDelivery  | MessageId, Recipient reference, Template, State, Timestamp, CorrelationId, safe error metadata  |
 

These are logical entities, not a finalized schema. Define indexes, foreign keys, retention, and tenant-aware uniqueness during implementation. 

**9. API and Integration Requirements** ****

| **Area**  | **Illustrative contract**  | **Notes**  |
| --- | --- | --- |
| Chat  | POST /api/chat/messages  | Accept question and optional conversation ID; long-running work returns HTTP 202 and Job ID, with authorized status/result retrieval.  |
| History  | GET /api/conversations/{id}  | Only the conversation owner may read the history; enforce tenant access and do not let role permissions grant access to another user's history.  |
| Knowledge  | POST /api/knowledge/documents  | Multipart upload; validate, create a version-scoped processing job, and return HTTP 202 with Job ID when accepted.  |
| Knowledge status  | GET /api/knowledge/documents/{id}  | Return processing and approval state by version with safe error details.  |
| Lifecycle  | POST /api/knowledge/documents/{id}/reindex; DELETE /api/knowledge/documents/{id}  | Authorized reindex/delete.  |
| Tickets  | GET /api/tickets; GET /api/tickets/{id}  | Tenant-scoped, paginated, filterable.  |
| Ticket lifecycle  | Ticket create/update/assignment/status operations  | Enforce role and tenant permissions; record activity/audit; exact routes are design-time contracts.  |
| Ticket field correction  | Submit, retrieve, approve, or reject Category/Priority correction requests  | Persist requests separately; enforce ticket/team/tenant role scope and eligible states; audit decisions.  |
| Ticket cancellation  | Submit, retrieve, approve, or reject ticket cancellation requests  | Persist requests separately; enforce the cancellation workflow, eligible states, tenant/team role scope, and audit decisions.  |
| Ticket AI  | POST /api/tickets/{id}/ai-summary; POST /api/tickets/{id}/classify  | Long-running work returns HTTP 202 and Job ID; retrieve authorized typed, validated result.  |
| Reply draft  | POST /api/tickets/{id}/draft-reply  | Long-running work returns HTTP 202 and Job ID; retrieve authorized draft and citations; do not send.  |
| Feedback  | POST /api/feedback; GET /api/feedback  | Submission associates with tenant, user, and message. Read returns only the fields in FR-ID-16 within the role scope in sections 5.9 and 6.13; it does not return conversation history or message content.  |
| Health  | GET /health  | Expose only non-sensitive health information.  |
| Administration  | Tenant, user, permission-matrix, operational-setting, and retention-policy operations  | Enforce Platform Admin/Tenant Admin scopes; validate, version, and audit changes.  |
| Knowledge approval  | POST /api/knowledge/documents/{id}/versions/{version}/approve or /reject  | Tenant Admin only; bind decision to exact version; invalidate on reprocess/update.  |
| Teams  | Team and membership administration operations  | Tenant Admin scope; managers can read assigned membership only.  |
| Customer Search  | Read-only search by Customer ID, Display Name, or Company/Organization; status/date filters; sort and page  | Exact ID or partial case-insensitive name/company matching; validated configurable max page size; filtering before pagination; total count and metadata; email is not searchable. Enforce role/relationship scope before search and direct-ID access.  |
| Customer detail / lookup  | Read-only Customer and related-ticket lookup/detail  | Enforce allowlisted fields and role/team/ticket scope before lookup. Mask email for all roles except an explicitly authorized Tenant Admin Customer-detail operation in that Admin's own tenant; audit every full-email access.  |
| Async jobs  | POST operation-specific request; GET /api/jobs/{jobId}; POST /api/jobs/{jobId}/cancel  | Long-running submissions return 202 + Job ID; status/result/cancellation access is authorized, tenant-scoped, and auditable.  |
| Account recovery / email  | ASP.NET Core Identity reset/change workflows and approved transactional notifications  | Generic responses, single-use time-limited tokens, real provider, approved event/recipient allowlist, and safe failure semantics.  |
 

Endpoint names are examples. Final contracts should define schemas, validation, status codes, error responses, idempotency where needed, and OpenAPI documentation. 

**10. Non-Functional Requirements** ****

| **Category**  | **Requirement**  |
| --- | --- |
| Security  | HTTPS; secret protection; input validation; default-deny server-side tenant, team, role, resource, action, and ticket authorization; least privilege and independent approval of privileged changes.  |
| Privacy  | Use synthetic data; allowlist and minimize customer fields; mask email in every path by default, with full registered email available only to a Tenant Admin in an explicitly authorized own-tenant Customer-detail operation; minimize logged content; document retention and deletion behavior.  |
| Reliability  | Handle timeouts, throttling, transient errors, and partial processing failures; persist job state; use safe, bounded retries.  |
| Performance  | Use pagination; return promptly from long-running job submissions; keep synchronous APIs within the 30-second default and configure model/background timeouts separately.  |
| Scalability  | Keep long-running work asynchronous and services loosely coupled; persist job state and avoid reliance on in-memory state.  |
| Maintainability  | Layered boundaries, dependency injection, typed contracts, structured logging, documented configuration.  |
| Accessibility  | Keyboard-operable controls, labels, readable contrast, and clear loading/error states.  |
| Observability  | Correlate UI/API/worker/model/search operations; record latency and failure rates without excess personal data.  |
| Cost  | Use budgets/alerts where available; cap input/output; document model/search usage and teardown.  |
| Portability  | Keep provider-specific code behind interfaces where practical; document cloud dependencies.  |
| Operational controls  | Apply configurable initial API/AI request, concurrency, timeout, upload, and conversation-context limits and independently configurable bounded model/job timeouts from section 5.11.  |
| Retention  | Apply configurable ticket, customer, user, activity, feedback, AI-result, document, log, conversation, evaluation, audit, and backup retention/deletion periods from section 5.11.  |
 

**11. AI-Specific Guardrails** ****

- Ground support answers in approved retrieved knowledge; show sources and do not fabricate citations. 
- Retrieve only the exact current knowledge version approved by a Tenant Admin; a changed, reprocessed, stale, rejected, or pending version is not retrievable.

- Use a no-answer path for missing, conflicting, stale, or insufficient evidence. 

- Treat documents, tickets, and retrieved passages as untrusted data, not model instructions. 

- Prevent unauthorized cross-tenant and cross-team access to documents, tickets, conversations, jobs, results, and embeddings. 

- Constrain tool use to an allowlist with typed schemas and server-side authorization. 

- Require human review for customer-facing drafts and business-changing actions. 

- Validate structured model output before persistence or downstream use. 

- Version prompts and evaluation datasets; rerun regression tests after material changes. 

- Label AI classifications and sentiment as provisional and editable. 
- Do not let AI finalize ticket transitions, cancellation, assignment, approval, tenant deletion, privileged permission changes, or customer communication.

**12. Sample Data and Evaluation Assets** ****

| **Dataset**  | **Suggested volume**  | **Purpose**  |
| --- | --- | --- |
| Knowledge articles / FAQs  | 20  | Product setup, billing, account access, troubleshooting, and policy topics.  |
| Synthetic tickets  | 100 initial tickets across 5 fictional tenants, tenant-scoped teams, and 10 fictional support agents  | Exercise team membership, ticket lifecycle/cancellation, summaries, categories, priorities, assignment, tenant/team isolation, and reply drafting; generate repeatably with a deterministic seed script.  |
| Fictional organizations  | 5  | Validate tenant isolation.  |
| Support agents and managers  | 10 agents plus synthetic Tenant Admins and Support Managers  | Exercise role, team membership, assignment, and access boundaries.  |
| Question/source pairs  | 50  | Measure retrieval, grounding, and citation behavior.  |
| Knowledge approval cases  | Include pending, approved, rejected, updated, and reprocessed versions  | Verify that only the exact currently approved version can be retrieved.  |
| No-answer questions  | 10  | Check abstention when knowledge is missing.  |
| Prompt-injection cases  | 10  | Test resistance to instructions embedded in content.  |
 

Use fabricated names and content only. Do not import real customer records or secrets into prompts, logs, fixtures, or screenshots. 

**13. Acceptance Criteria** ****

- An authorized user uploads a supported file and sees status through indexing or a safe failure state. 

- A processed document version is not retrievable until a Tenant Admin approves that exact version; an approved version can be cited, and update/reprocessing invalidates prior approval immediately. 

- A question without supporting content receives a clear no-answer response, not an invented answer. 
- Answers do not present unsupported factual claims as grounded and do not fabricate citations; correct abstention is handled separately from grounded-answer scoring.

- Users cannot access unauthorized tenant/team documents, chunks, tickets, conversations, feedback, jobs, or results, including through direct API calls or identifier enumeration; conversation history is readable only by its owner, and the Platform Admin assistant is limited to FR-AN-06 aggregate analytics for exactly one explicitly selected authorized tenant, with no access to tenant documents or underlying tenant business records.

- Ticket summary/classification conforms to a documented schema; invalid output is rejected or safely retried. 

- An agent can edit/discard a suggested reply; the system does not send it automatically. 
- The AI Customer Assistant is available only to authenticated Platform Admin, Tenant Admin, Support Manager, and Support Agent users; external CloudDesk customers cannot access it.
- Dashboards and predefined natural-language analytics enforce the role-specific tenant, assigned-team, own-authorized-ticket, and single-selected-tenant aggregate scopes in FR-AN-06.
- Customer Search supports the defined fields, filters, sorting, validated configurable maximum page size, total count, and pagination metadata; email is not searchable. Filtering and role scope are applied before pagination, and direct-ID access is revalidated server-side.
- Tenant Admin Customer Search/Read is limited to their tenant; Support Manager scope is limited to assigned-team Customers, including team-assigned tickets without an Agent; Support Agent scope is limited to Customers associated with tickets currently assigned to that Agent, with no exception/grant mechanism and immediate revocation on reassignment or loss of scope. Platform Admin has no routine Customer Search; the Platform Admin assistant cannot retrieve Customer records.
- Search and lookup mask email for every role. Only Tenant Admin may see full registered email through an explicitly authorized Customer-detail operation for their own tenant; each full-email access is audited with the required identifiers and outcome, and full addresses are not unnecessarily exposed in logs, prompts, indexes, or unauthorized responses.
- Feedback Read is available only to Tenant Admins for their tenant, Support Managers for users in assigned teams, and Support Agents for their own submissions; Platform Admin has no routine individual feedback/comment access. Results contain only the fields listed in FR-ID-16 and do not expose conversation history or message content; access is server-side scoped and audited.
- When a Customer has no related tickets, the configurable 365-day retention period starts at Customer.CreatedAt. A newly associated ticket suspends pending cleanup eligibility; no Customer is purged while any related ticket is active; after all related tickets are terminal (Closed or Cancelled), the 365-day period restarts from the latest terminal-transition timestamp. Revalidate relationships and eligibility immediately before deletion.

- Tool calls are allowlisted, authorized, bounded by timeout, and represented in an audit record. 

- CI runs build and automated tests on pull requests; failures block the normal merge path. 

- Setup and deployment are documented, and secrets are absent from the repository. 

- A repeatable evaluation run records results and model/prompt identifiers. 
- Platform Admin can manage tenants, the predefined-role permission matrix, and global operational/retention settings; Tenant Admin user management is tenant-scoped.
- Privileged Platform Admin permission changes cannot take effect without approval by a second independent Platform Admin; self-approval and self-elevation are denied and audited.
- Unauthorized role/resource actions and cross-tenant access are denied through direct backend requests as well as the UI.
- Tenant Admins can manage users, teams, primary team managers, and Agent memberships only in their tenant; each Agent has exactly one primary team and Managers can belong to multiple teams.
- Authorized users can create and manage synthetic tickets through the tenant/team-scoped workflow; closure is only from Resolved, cancellation has mandatory reason/notes and is terminal, and cancellation is not counted as successful resolution/closure.
- Managers cannot access other teams' or completely unassigned tickets; Agents cannot assign/reassign tickets; the existing Tenant Admin role owns central triage and can view/manage/route tickets that have neither team nor Agent assignment only within that Admin's tenant. Platform Admin has no routine tenant ticket-business access.
- Ticket queue recommendations follow the configured category defaults and remain subject to authorization and human review.
- Operational settings are validated, centralized, versioned, and auditable; the initial values are in section 5.11.
- Deleted knowledge is unavailable to retrieval immediately and is physically purged from primary storage/indexes within 30 days; backups expire within 30 days and deletion records are reapplied after restoration.
- Tenant deactivation blocks access and retrieval without deleting retained data; deletion has a 30-day grace period and dual-admin approval, and reversal requires two independent Platform Admin approvals before purge.
- After the 30-day grace period and independent second Platform Admin approval, permanent tenant deletion overrides the 365-day deactivated-user retention period and purges eligible personal and business records; only minimum necessary protected security/administrative audit metadata remains under the existing independent audit policy/access controls, contains none of the prohibited secrets or deleted content, and cannot restore tenant/business records.
- Closed and Cancelled tickets use the configurable 365-day retention period; application logs are retained 30 days, and feedback, Ticket AI results, conversations, and evaluation data/results are retained 90 days as specified.
- Audit records include the applicable actor, tenant, action/outcome, timestamp, and correlation ID without unnecessary sensitive content.
- Password recovery uses ASP.NET Core Identity and a real configured email provider, generic reset responses, time-limited single-use tokens, safe delivery failures, and role-scoped administrative recovery.
- Deactivated user accounts cannot reset passwords until separately reactivated; this restriction does not disclose account status through a non-generic reset response.
- Long-running AI/RAG/ticket/knowledge operations persist a job, return HTTP 202 and a Job ID, and expose authorized status/results without rerunning work on poll.
- Predefined natural-language analytics use only the read-only functions and role scopes in sections 5.5 and FR-AN-06; advanced analytics and arbitrary text-to-SQL remain out of scope.
- Support Agents can edit only Subject and Description on authorized tickets and cannot assign/reassign or directly change Category/Priority. Direct Category/Priority changes follow FR-TM-14; correction requests are separately persisted and decided by authorized Managers or Tenant Admins.
- Category/Priority correction requests retain the existing ticket value while pending, enforce role/team/tenant and eligible-state rules, reject duplicate active requests for the same ticket/field, and audit request and decision data.
- Ticket cancellation requests are separately persisted; pending requests do not change authoritative ticket fields. Only authorized Tenant Admins or assigned-team Support Managers can approve/reject; approval cancels only eligible tickets, rejection preserves the ticket, and history is audited.
- Authorized actors can cancel Queued or Processing background jobs under section 5.14; queued cancellation prevents execution, processing cancellation stops at a safe checkpoint, partial results are not exposed, and concurrent completion preserves a committed Completed state.
- Only the password, ticket, knowledge, account, and Platform Admin permission-change email events explicitly listed in section 5.15 are sent; recipient authorization, deduplication, privacy, audit, and safe delivery-failure behavior are enforced.
- Proposed evaluation percentages remain non-gating; runs report defined numerators, denominators, model/prompt versions, limitations, and failures.

- Support Agents can be assigned only to tickets in their single current primary team, with no cross-team exception or separate grant; Tenant Admins may route across their tenant but may assign an Agent only when that Agent belongs to the ticket's assigned team. Managers may assign/reassign only within their assigned teams. Server-side tenant/team validation is required for every assignment and reassignment; unauthorized assignments are denied and audited. Primary-team changes use the authorized Tenant Admin workflow, immediately revoke out-of-scope Agent access, and validate/audit any resulting ticket assignment changes.
- New → Open is permitted only for a currently assigned and authorized Support Agent, a Support Manager for a ticket in an assigned team (including a team-queued ticket without an individual Agent), or a Tenant Admin for any ticket in their own tenant including completely unassigned tickets. Platform Admin and ticket creation alone do not grant this permission. The server revalidates current authorization, ticket tenant, team, assignment, and status on every transition; unauthorized and undefined transitions are denied, and successful transitions are recorded in activity history and audit logs.

**14. Test Strategy** ****

| **Test level**  | **Coverage examples**  |
| --- | --- |
| Unit  | Chunking, 20 MB file validation, tenant/team filter construction, default-deny permission mapping including Feedback/Read, independent approval checks, retention/configuration validation including Customer.CreatedAt and ticket-terminal timer resets, Customer Search filters/sorting/page-size validation, DTO validation, output parsing, ticket field permissions and request/state transitions, and queued/processing job cancellation including state races.  |
| Integration  | SQL repositories, Customer Search with filtering before pagination and total-count metadata, ticket correction/cancellation request persistence, Feedback Read role scoping and field minimization, Customer email masking/unmask audit, blob operations, approval-aware search indexing/retrieval, model adapter, tool registry, persisted background workers/jobs and cooperative cancellation, approved email triggers/provider behavior, tenant-deletion override and protected audit metadata, configuration, retention cleanup, and audit history.  |
| API  | Identity recovery/lockout including reset denial for deactivated accounts until reactivation, tenant/user/team administration, two-person privilege safeguards, RBAC, Feedback Read scopes and limited fields, Customer Search field/match/filter/sort/pagination contracts, direct-ID access and role scopes, email masking across API/search/AI tools/lookup and Tenant Admin detail-only unmasking, assistant-role access, role-scoped dashboard and predefined analytics, ticket lifecycle/assignment and central-triage rules, correction/cancellation request permissions, job 202/status/result/cancel contracts, tenant/team isolation, and safe email/error handling.  |
| AI evaluation  | Recall@5, claim-level grounding, citation precision, abstention, structured output validity, prompt injection, and explicit numerator/denominator reporting.  |
| Security  | Default-deny authorization for ticket field edits and approvals, job cancellation, assistant access, each role-specific analytics and Customer/Feedback scope, Agent access revocation after reassignment or authorization loss, no global unassigned-ticket access for Managers, deactivated-account reset denial, tenant/team boundaries, direct-ID enumeration, stale or concurrent requests, partial-result protection, email masking and full-email audit for every access path, tenant-deletion metadata minimization/access controls, notification recipient resolution, and sensitive-data minimization.  |
| End-to-end  | Tenant/user/team setup → permission checks; internal-role assistant access and external-customer denial; role-scoped analytics; upload → process → pending approval → approve → ask/cite; update/reprocess → retrieval invalidation; Customer Search with exact/partial matching, filters, sorting, pagination, roles, direct-ID checks, and email masking; Tenant Admin detail-only unmask with audit; Feedback Read role scopes and field limits without conversation access; ticket create/assign/resolve/close/reopen including central triage boundaries; Category/Priority correction request approval/rejection; ticket cancellation request approval/rejection; active-account password reset/change confirmation and deactivated-account reset denial; async job submission/status/result and queued/processing cancellation.  |
| Operational  | Health checks, telemetry correlation, audit events, tenant deactivation/deletion/reversal including early deactivated-user purge and protected minimal audit metadata, Customer no-ticket retention from CreatedAt and reset after terminal ticket transitions, retries, configured throttling/timeouts, approved notification events and email delivery failures, configuration validation, and deployment smoke test.  |
 

Required assignment and status-transition coverage must test successful and denied role/scope combinations, including cross-team Agent assignment denial, Tenant Admin routing with Agent/team validation, primary-team change and immediate access revocation, unauthorized assignment audit, all specified New → Open role conditions, creator-only denial, Platform Admin denial, current-authorization/status revalidation, and successful transition history/audit.

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
2. Support Team Management.
3. Administrative Configuration and Tenant Lifecycle.
4. Knowledge Management and Version Approval.
5. Ticket Management and Cancellation.
6. Persisted Asynchronous Jobs.
7. Transactional Email and Account Recovery.
8. AI Ticket Intelligence.
9. AI Customer Assistant.
10. Agent Copilot.
11. Analytics and Reporting.
12. Audit and Monitoring.
13. Evaluation and Quality Assurance.
14. Customer Search and Feedback Access.

For each module, define acceptance criteria, dependencies, and integration contracts; include relevant unit/API/integration/security tests; verify role, tenant, team, and approval controls; and maintain required documentation/audit coverage. Decide implementation order, task breakdown, dependency sequencing, resource allocation, and milestones separately during Implementation Planning based on technical dependencies and available capacity.
 

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
| Open question  | Which email provider, sender identity, and deployment configuration will be selected?  | Select Azure Communication Services Email or SendGrid during implementation; verify sender-domain, environment allowlist, secrets, and delivery configuration before enabling real email.  |
| Open question  | What bounded background timeout and retry settings are appropriate for each operation/provider?  | Configure independently from the 30-second general API timeout; validate against provider constraints and observed latency.  |
| Proposed evaluation target  | Recall@5 >= 80%, Grounded Answer Rate >= 90%, Citation Precision >= 95%, and 100% on the initial no-answer/structured-output/prompt-injection cases.  | These are measurement targets only, not release gates, and remain non-gating after Human Requirement Approval unless separately changed by an explicit human decision. Tenant, team, and role authorization denial remains mandatory.  |
 

**18. Definition of Done** ****

- Requirement is implemented or explicitly deferred. 

- Acceptance criteria are met and relevant tests are committed. 

- Tenant, team, role, resource/action, Customer Read/Search, and Feedback Read scope checks are applied and tested for affected data paths; privileged Platform Admin changes enforce independent approval.
- Tenant/user/team administration, version-specific knowledge approval, ticket lifecycle/cancellation, async job access, account recovery/email, and relevant audit events are covered by tests.
- AI Customer Assistant access is limited to the four internal roles; external customers are denied. Dashboard and predefined analytics enforce FR-AN-06, and deactivated accounts cannot reset passwords until separately reactivated.
- Agent ticket field restrictions, Category/Priority correction requests, ticket-cancellation requests, and explicitly approved email event/recipient rules are covered by their relevant automated tests.
- Background-job cancellation is covered by unit, integration, API, security, and end-to-end tests, including authorization, queued and processing cancellation, safe checkpoints, concurrent completion, idempotency, and prevention of partial-result exposure.
- Customer Search uses the specified fields, filters, sorts, validated configurable maximum page size, filter-before-pagination behavior, total count, and metadata; scope is enforced server-side for search and direct IDs.
- Feedback Read enforces the defined role scopes, returns only the permitted feedback fields, does not expose conversation history/message content, and is audited.
- Customer email is masked for Platform Admin, Support Manager, and Support Agent across API, search, AI tools, and lookup; only Tenant Admin may unmask through an explicitly authorized own-tenant Customer-detail operation, with every full-email access audited.
- Tenant Admin central triage, assigned-team Manager access, single-primary-team Agent assignment with no exception, immediate Agent access revocation after assignment/team/scope loss, explicit New → Open role/condition rules, server-side validation, denial/audit behavior, and Platform Admin's lack of routine tenant ticket-business access are enforced and tested.
- Configured request/rate/concurrency/time/upload/context limits, independent model/job timeouts, Customer no-ticket retention from Customer.CreatedAt, retention timer resets after all related tickets become terminal, revalidation before deletion, tenant deactivation/deletion/reversal, and cleanup behaviors are validated.
- Approved tenant deletion after the 30-day grace period and independent second Platform Admin approval overrides the 365-day deactivated-user retention period; only minimum necessary protected audit metadata remains under the existing independent policy/access controls and cannot restore tenant/business records.
- Real email delivery and safe failure/retry behavior are validated in controlled test environments without exposing secrets or reset tokens.

- Errors, loading, and empty states are handled. 

- Telemetry is useful without exposing secrets or unnecessary customer content. 

- Documentation covers setup, configuration, tests, deployment, and known limitations. 

- PR is linked to an issue and passes CI and human review. 

**Appendix A. Recommended Initial Backlog** ****

| **Epic**  | **Example issues**  |
| --- | --- |
| Foundation  | Configure React/.NET and local Identity recovery; define tenants/users/default-deny RBAC and two-person privileged approval; add admin console, operational settings, and CI.  |
| Support teams  | Tenant-scoped team CRUD and membership; primary Manager and Agent team rules; audit and access tests.  |
| Ticket management  | Deterministic synthetic seed data; explicit ticket transitions/cancellation; tracked Category/Priority correction and cancellation requests; team assignment; role permissions; audit/activity; categories and queues.  |
| Knowledge  | Upload API; 20 MB validation; version-specific approval; retention/deletion controls; extraction; chunking; embeddings; approval-aware index lifecycle and status UI.  |
| Async jobs and email  | Persisted job APIs/workers; 202/status/result/cancellation; bounded retries/timeouts; real provider abstraction; password recovery/change confirmation and approved notifications with safe delivery.  |
| Assistant  | Chat API; retrieval; prompt versioning; citation DTO; abstention; conversation UI; feedback submission and scoped Feedback Read.  |
| Customer access  | Role-scoped Customer Search, lookup/detail, email masking and authorized unmask audit; customer retention and tenant-deletion coverage.  |
| Ticket copilot  | Ticket summary/classification schema; reply draft; human edit flow; read-only lookup tools.  |
| Quality & operations  | Tenant/team/RBAC/approval tests; non-gating evaluation runner; prompt-injection tests; audit/telemetry; configurable limits; retention and deletion; deployment; demo runbook.  |
 

**Appendix B. Glossary** ****

| **Term**  | **Meaning**  |
| --- | --- |
| RAG  | Retrieval-augmented generation: retrieve relevant content and provide it to a model as evidence.  |
| Embedding  | Numerical representation of text used for semantic similarity search.  |
| Chunk  | A segment of a source document indexed and retrieved independently.  |
| Grounded answer  | A response supported by available evidence, ideally with traceable citations.  |
| Abstention  | Declining to provide a substantive answer when evidence is insufficient.  |
| Tenant isolation  | Controls preventing one organization from accessing another organization's data.  |
| Support team  | Tenant-owned group with assigned Support Manager and Agents; controls the team scope for ticket visibility and actions.  |
| Approved knowledge version  | Exact processed document version approved by a Tenant Admin and eligible for authorized retrieval until changed, reprocessed, rejected, or deleted.  |
| Background job  | Persisted, tenant-scoped record of a long-running operation with authorized status/result access.  |
| Category/Priority correction request  | A persisted Agent request to change a ticket's Category or Priority, decided by an authorized Manager or Tenant Admin without changing the ticket while pending.  |
| Ticket cancellation request  | A persisted Agent request for an authorized Tenant Admin or assigned-team Support Manager to cancel an eligible ticket.  |
| Background job cancellation  | An authorized request to stop a queued or processing job without exposing partial results or overwriting a completion already committed.  |
| Cancelled ticket  | Terminal ticket outcome distinct from resolution or closure; retained, not physically deleted, and excluded from successful resolution/closure metrics.  |
| Customer Search  | Server-side, role-scoped Customer search with defined match fields, filters, sorting, pagination, and email masking.  |
| Feedback Read  | Permission-scoped access to limited feedback metadata that does not grant conversation-history or message-content access.  |
| Central triage  | The existing Tenant Admin's within-tenant authority to view, manage, and route tickets with neither team nor Agent assignment.  |
| Human-in-the-loop  | A workflow where a person reviews or approves AI-generated content or actions.  |
 
