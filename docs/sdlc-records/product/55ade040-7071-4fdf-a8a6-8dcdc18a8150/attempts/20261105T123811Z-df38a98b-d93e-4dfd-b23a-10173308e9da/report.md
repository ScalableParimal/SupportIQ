# Requirement Analysis

**Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`  
**Attempt ID:** `20261105T123811Z-df38a98b-d93e-4dfd-b23a-10173308e9da`  
**Authoritative source:** `docs/requirement/SupportIQ_Product_Requirement_v1.6.md`  
**Source identity:** SupportIQ Product Requirement v1.6; 99,368 bytes; SHA-256 `2CD66B9C6A20949E3983B37D5DCD91D122F768E55BF63E0C6A85C5B519B4A73F`  
**Lifecycle status:** Draft Updated Requirement; unapproved.  
**Analysis approach:** Fresh review of all 804 lines of v1.6. The v1.5 analysis was not reused as current analysis evidence. Existing human decisions RA-A-01 and RA-A-02 were considered and traced to their decision records.

## 1. Understanding

SupportIQ is a fictional B2B SaaS support portal for CloudDesk and a 30-day demonstrable learning release, not a production-readiness commitment. It supports four internal roles: Platform Admin, Tenant Admin, Support Manager, and Support Agent. Its main functions are tenant/team administration, approved knowledge and grounded AI assistance, synthetic ticket management, read-only tools and scoped analytics, persistent asynchronous jobs, transactional email, audit, testing, and Azure deployment.

## 2. Explicit Requirements

### Functional requirements and business rules

- Four predefined roles use centralized, default-deny, backend-enforced resource/action permissions; tenant, team, resource, action, and owner scopes apply. Privileged Platform Admin changes require a different independent Platform Admin to approve (Sections 3, 5.9; FR-ID-01 through FR-ID-15).
- The assistant is for the four internal roles only. Tenant Admin, Support Manager, and Support Agent retrieval is limited to current Tenant Admin-approved knowledge in authorized scope. The Platform Admin assistant must not access tenant business content. Answers are grounded, cited, and abstain when evidence is insufficient (Section 5.1; FR-CA-01 through FR-CA-08).
- Each user may read only their own conversation history, regardless of role (FR-CA-07, Section 5.9 permission catalogue, Section 9 History API note, acceptance criteria). This aligns with human decision RA-A-01.
- Human-controlled knowledge approval/versioning and ticket workflows are explicit. AI tools are allowlisted, typed, read-only, scoped, and audited; customer-facing messages and business-data changes are not automatic (Sections 5.2-5.5, 5.10-5.15).
- Analytics scopes differ by role. Platform Admin may access aggregate analytics for one selected authorized tenant, with no cross-tenant view or underlying tenant business records (FR-AN-06).
- Long-running work uses persisted jobs with authorized status/result access and cooperative cancellation; email is limited to listed events; retention, audit, and security controls are specified (Sections 5.8, 5.11-5.15).

### Constraints

The stated baseline is React/TypeScript, .NET 8 / ASP.NET Core Identity, Azure AI endpoints/Search, Azure SQL, Blob Storage, App Service, Key Vault, Application Insights, and GitHub Actions. The release is learning-oriented and demonstrable. Entra ID/SSO, external ticketing/CRM/messaging integrations, arbitrary custom roles, AI-invoked write tools, and several other items are out of scope or deferred.

### Human decisions considered

- **RA-A-01:** Each user may read only their own conversation history; roles cannot grant another user access. Evidence: `decision-resolution-001.json`.
- **RA-A-02:** Platform Admin assistant retrieval must not access tenant business content. Evidence: `decision-resolution-002.json`.
- These clarifications are not Human Requirement Approval; v1.6 remains unapproved.

## 3. Scope

### In Scope

The mandatory first-release scope in Section 4.1: local identity/recovery; four-role RBAC; tenant/team administration; operational configuration; version-approved knowledge/RAG; synthetic ticket lifecycle and tracked request workflows; ticket AI and copilot; read-only tools/analytics; persisted cancellable jobs; restricted transactional email; audit/monitoring; evaluation/testing; CI, documentation, and Azure deployment.

### Out of Scope

Section 4.2 exclusions include external service integrations, billing, multi-region disaster recovery, compliance certifications, large-scale benchmarking, custom fine-tuning, automated model selection, Entra ID/SSO, internal notes, AI-invoked write tools, arbitrary custom roles, and SLA indicators before definitions exist.

### Deferred / Undecided

Section 17 defers exact Azure AI models/region, token limits and monthly cost budget, email provider/sender/deployment configuration, and bounded per-operation background timeout/retry settings. Retention values are proposed configurable defaults, not legal or regulatory commitments.

## 4. Ambiguities

| ID | Requirement | Ambiguity | Impact |
|---|---|---|---|
| RA16-A-01 | RA-A-02; FR-WF-01; FR-AN-06; Section 5.5 role-based tool access; Section 5.9 | RA-A-02 bars Platform Admin assistant access to tenant business content, while FR-WF-01 exposes predefined analytics as an assistant tool and FR-AN-06 permits aggregate analytics for one selected tenant. It is unclear whether those tenant-derived aggregates are prohibited content or an explicit exception. | The assistant's tool authorization and tenant-data boundary cannot be consistently enforced without clarifying whether Platform Admin assistant analytics may use the FR-AN-06 aggregate scope. Blocking before verification. |

## 5. Conflicts

No separate direct contradiction was established beyond ambiguity RA16-A-01. It is recorded as an ambiguity because the scope of “tenant business content” relative to aggregate analytics is not defined; neither the prior human decision nor the explicit analytics permission is silently overridden.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance | Impact |
|---|---|---|---|
| RA16-M-01 | The default-deny permission catalogue in Section 5.9 lists no Customer resource or Read/Search action, while Sections 5.5 and FR-WF-01 require Customer Lookup and describe role-specific access. | Blocking for this lookup path | The explicit permission mapping cannot be determined from the catalogue; implementers could either deny the required lookup or infer an unlisted permission. |
| RA16-M-02 | The Customer retention row says records remain while active tickets exist and then refers to “inactive” records, but does not define the inactive condition or when its 365-day clock begins. | Important before cleanup implementation | The destructive retention behavior may differ depending on the meaning; the proposed default is not a legal commitment. |
| RA16-M-03 | Feedback submission, storage, and retention are specified, but no feedback-read/review permission is specified. | Minor / non-blocking | Do not infer read access; keep it default-deny unless a review capability is separately decided. |
| RA16-M-04 | Exact model/deployment/region, model token limits and cost budget, email provider/sender, and per-operation background timeouts/retries remain open. | Deferred | Section 17 expressly defers these decisions; validate before the relevant implementation/deployment choices. |

## 7. Assumptions

| ID | Assumption | Impact | Confirmation required |
|---|---|---|---|
| RA16-AS-01 | CloudDesk and all example organizations, users, tickets, and knowledge are fictional/synthetic. | Controls test data, prompts, logs, and screenshots. | No; explicitly stated. |
| RA16-AS-02 | Azure AI/Search resources are available. | Model, region, quota, compatibility, and cost choices remain unvalidated. | Yes, before selecting deployments. |
| RA16-AS-03 | Retention defaults are proposed/configurable only. | They do not establish legal or regulatory retention obligations. | Validate with business/legal owners before production use. |

No new assumption was converted into a requirement. The unresolved meaning of “inactive” is not assumed in this analysis.

## 8. Technical Impact

- **API / authorization:** Align Platform Admin assistant tool authorization with RA-A-02 and FR-AN-06. Add or clarify an explicit Customer read/search permission and its role/data scopes before enabling Customer Lookup.
- **Application / domain:** Preserve owner-only conversation history; keep knowledge, tickets, and customer results within explicit tenant/team/resource scope. Maintain human approval for ticket and privileged changes.
- **Data / retention:** Define the Customer retention eligibility and clock before automated cleanup. Keep feedback reads denied absent a defined role/action.
- **Infrastructure / integrations:** Use the stated Azure services and real email-provider abstraction; model/region/provider/retry/timeout choices remain deferred.
- **Testing / security:** Cover owner-only history, Platform Admin assistant analytics boundary, Customer lookup allow/deny by role/scope, tenant/team isolation, job cancellation races, and retention cleanup semantics. Evaluation percentages are non-gating; authorization failures remain acceptance failures.
- **Performance / operations:** Enforce proposed request/concurrency/timeout limits and independently bounded job/model timeouts; validate deferred values against provider behavior and cost.

## 9. Questions Requiring Human Decision

1. **RA16-Q-01 - Platform Admin assistant analytics:** Does RA-A-02 prohibit all tenant-derived assistant content, including FR-AN-06 aggregate analytics, or is single-tenant aggregate analytics an explicit exception while underlying tenant documents/records remain inaccessible?
2. **RA16-Q-02 - Customer lookup authorization:** Should the centralized catalogue add an explicit Customer Read/Search resource/action with the role scopes already described in Section 5.5, or should lookup be limited to customer fields reached through an authorized ticket read (with other customer lookup denied)?
3. **RA16-Q-03 - Customer retention:** Is “inactive” intended to mean that no associated active ticket remains, with the 365-day period starting at closure of the last related ticket, or should a different rule apply?

## 10. Analysis Conclusion

- **Ready for requirement finalization:** No.
- **Blocking decisions:** RA16-Q-01 and RA16-Q-02. RA16-Q-03 should be resolved before implementing Customer-record cleanup.
- **Human decisions incorporated:** RA-A-01 and RA-A-02, as recorded; no new decisions were made by the analysis.
- **Requirement Analysis Verification readiness:** No. Resolve the questions through explicit human decisions and a separately authorized Requirement Update if the requirement text changes; then perform fresh analysis against the resulting version before independent Requirement Analysis Verification.
- **Next step:** Obtain the three clarifications; then separately authorize the applicable Requirement Update. No update, verification, approval, planning, or implementation was started in this attempt.

**Source integrity:** v1.6 was read-only throughout; all 97 functional requirement IDs and 26 Markdown table blocks were counted. No source, product artifact, implementation plan, code, tests, or configuration was modified. No tests or builds were run.