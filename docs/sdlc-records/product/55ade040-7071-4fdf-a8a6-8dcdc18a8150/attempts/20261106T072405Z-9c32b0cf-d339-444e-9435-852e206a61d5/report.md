# Requirement Analysis

**Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`  
**Attempt ID:** `20261106T072405Z-9c32b0cf-d339-444e-9435-852e206a61d5`  
**Outcome:** `ANALYSIS_COMPLETE; HUMAN_DECISIONS_REQUIRED; NOT_READY_FOR_REQUIREMENT_ANALYSIS_VERIFICATION`  
**Authoritative source:** `docs/requirement/SupportIQ_Product_Requirement_v1.8.md`  
**Source status:** Draft Updated Requirement; unapproved.

### Invocation context (not product decisions)

The user explicitly authorized one fresh Requirement Analysis in this conversation (`initiate_requirement_analysis=true`) and clarified that the later empty attempt directory `20261106T063721Z-68f9bc3e-09c9-417d-9f2f-aef2a5b4e3cb` is abandoned. These statements authorize/contextualize this process only. Neither is treated as a product requirement, product decision, Human Requirement Approval, or acceptance. The abandoned directory was left unchanged.

### Source and evidence identity

v1.8 was analyzed at 117,136 bytes, SHA-256 `E7FB3E982555034B098D42E258CAFBEDB651A0A05B736A99DE987DAB6355AD1B`. Its lineage names v1.7 SHA-256 `E38812289F69CD4338217EDDC6439B76F8749DE68F054C6707D089324A4093A9`. The latest Requirement Update is attempt `20261106T060433Z-73c4408d-8c23-4b9f-a8e5-3cb02f65a086` (`REQUIREMENT_UPDATED; DRAFT_UPDATED_UNAPPROVED`); the latest material-change Portability Assessment is attempt `20261106T062000Z-33c74d75-caae-4eaf-9dc9-9b07744b7e20` (`COMPATIBILITY WITH IDENTIFIED ADAPTATION`, no recommended possible blockers). Their bound evidence and relevant prior Analysis result are listed in `evidence/analysis-evidence.json`. The Portability Assessment is advisory and historical: it records a different HEAD from this invocation and is not substituted for current invocation validation.

## 1. Understanding

- **Business objective:** Deliver a 30-day-target, demonstrable learning/portfolio AI support portal for fictional CloudDesk, with tenant-aware administration, approval-controlled RAG, internal ticket handling, AI assistance, Customer/Feedback access, and operational controls. The requirement explicitly disclaims production-readiness commitment.
- **Actors:** Platform Admin, Tenant Admin, Support Manager, Support Agent; external CloudDesk customers are excluded from the assistant.
- **Main behavior:** Authorized internal users work tenant/team-scoped tickets and customers, search only currently approved knowledge, receive grounded/cited or abstaining AI assistance, and use auditable administrative, job, retention, and email workflows.
- **Source hierarchy:** v1.8 is the sole current product source for this analysis. The Update report/result resolve v1.8 provenance and incorporated decisions; the Request document remains a template. The latest Portability Assessment contributes process/adaptation context, not product requirements or a blocker decision.

## 2. Explicit Requirements

- **Identity/RBAC (§3, §5.9):** Local ASP.NET Core Identity; four predefined roles; centralized versioned default-deny resource/action authorization; tenant/team/owner scope; no self-registration, custom roles, tenant overrides, privilege escalation, or self-approval. Two-person independent approval is required for defined privileged Platform Admin changes.
- **Teams/tickets (§5.10, §5.13):** Tenant Admin manages tenant teams and owns within-tenant central triage, including completely unassigned tickets. Managers are limited to assigned teams (including team-assigned tickets without an Agent); Agents have one primary team and work only authorized assigned tickets. Ticket statuses, taxonomy, priority values, transitions, field edit permissions, correction requests, escalation, cancellation, terminal-state behavior, audit, and retention are specified; unspecified actions are denied.
- **Knowledge/AI (§5.1–5.5, §5.8, §11):** Only exact currently approved document versions are retrievable. Retrieval is tenant/scope authorized; AI has a read-only typed allowlist, no arbitrary SQL/shell/network or write tools, no automatic customer messages, and no authority to make business changes. Outputs require grounding, citations or abstention, validation, human review where applicable, safe error handling, and versioned evaluation.
- **Customer, feedback, analytics (§5.5–5.6, §5.9):** Customer Search match/filter/sort/page contract, role/ticket relationship scope, direct-ID revalidation, email masking and Tenant Admin own-tenant detail-only unmask with audit are explicit. Feedback Read is role-scoped and field-limited, without conversation/message-content access. Analytics are predefined, read-only, scope-labeled, and limited by FR-AN-06.
- **Retention, deletion, audit (§5.11–5.12):** Configurable proposed retention defaults; Customer timer starts at `Customer.CreatedAt` when no related tickets, pauses eligibility for new/active related tickets, and resets after all related tickets are terminal. Tenant deletion has a 30-day grace period and dual-admin control; it overrides deactivated-user retention but preserves only minimum protected audit metadata, excluding personal email, secrets, and deleted business content. Security/admin audit is retained independently.
- **Jobs/email/quality (§5.14–5.15, §7–14, §18):** Persisted asynchronous jobs return 202 and authorized status/results; cancellation is role-scoped, cooperative, and race-aware. A real email provider is required for reset/change confirmation and enumerated notifications only. The requirement defines tests, safety, deployment, documentation, and Definition-of-Done expectations.
- **Constraints/boundaries:** React + TypeScript, .NET 8, Azure services, synthetic data, 20 MB initial upload limit, API/AI limits, proposed retention values, and 30-day target. Logical entities and API routes are illustrative, not finalized schema/contracts.

### Human decisions incorporated from the latest Requirement Update (not approvals)

The current v1.8 text and Update records incorporate seven decision groups: (1) no-related-ticket Customer retention starts at `Customer.CreatedAt`, with active-ticket protection, timer reset at latest terminal transition, and pre-delete revalidation; (2) Agent Customer access only through currently assigned tickets, immediately revoked on assignment/scope loss, with no separate grant; (3) existing Tenant Admin owns central triage, Managers remain assigned-team-scoped, no new role/permission/grant, and Platform Admin has no routine ticket-business access; (4) approved permanent tenant deletion after grace and independent second-admin approval overrides deactivated-user retention, leaving only minimum protected audit metadata; (5) Customer Search matching, filters, ordering, pagination, returned fields, scopes, and direct-ID enforcement; (6) Feedback Read role scopes and field/content limits; and (7) Customer email masking across roles/paths, with Tenant Admin own-tenant detail-only unmask and audit. See Update report/result and the prior decision-linked Analysis result in the evidence record. These are incorporated human decisions in the draft; they do not approve v1.8.

## 3. Scope

### In Scope

The mandatory first demonstrable release in §4.1: local identity/recovery, tenants/users/RBAC, teams, administrative configuration, approval-gated knowledge/RAG, tenant/team ticket lifecycle, Customer Search/Read, Feedback Read, AI ticket intelligence/copilot, internal-role assistant, read-only tools/analytics, persisted jobs and cancellation, audit/monitoring, tests/evaluation, CI/documentation, and Azure deployment. Customer Search, Feedback Read, email visibility, ticket correction/cancellation workflows, listed email events, and job cancellation are expressly mandatory and not optional.

### Out of Scope

§4.2 explicitly defers external SSO, MFA/passwordless, internal notes, external ticketing/CRM/messaging integrations, arbitrary SQL/text-to-SQL, autonomous multi-agent/customer communication, AI write tools, custom roles/tenant overrides, SLA indicators, billing, multi-region DR, compliance certifications, large-scale benchmarking, custom fine-tuning, automated model selection, and automated privileged approvals.

### Deferred / Undecided

Exact model deployments/region, token limits/monthly budget, email provider/sender/deployment, and per-operation timeout/retry settings remain open in §17. Retention and evaluation numbers are proposed/configurable or explicitly non-gating, not legal or release commitments. Implementation order, schema, exact API contracts, staffing/capacity, and milestones belong to later planning.

## 4. Ambiguities

| ID | Requirement reference | Ambiguity | Impact / importance |
|---|---|---|---|
| RA18-A01 | §5.10 Agent assignment; §5.13 one primary Agent team | “Unless an explicitly approved exception exists” allows possible assignment outside an Agent’s primary team but defines no exception authority, criteria, scope, duration, or revocation; team membership remains single-primary. | **Blocking** for access control and assignment behavior; could broaden ticket/customer visibility. |
| RA18-A02 | §5.10 New → Open; §5.9 default-deny matrix | New → Open is allowed for an “authorized user,” without naming eligible roles or conditions. Other transitions are role-specific and unlisted actions default-deny. | **Blocking** for the ticket state machine and authorization tests. |
| RA18-A03 | §5.9 Customer access | Platform Admin has no routine Customer Search, but “separately authorized investigations” are contemplated without a defined first-release scope or authorization path. | **Important/conditional** security boundary; clarify whether this capability exists, and if so who authorizes what and with which audit/limits. |
| RA18-A04 | §5.11 tenant deletion | Remaining audit metadata is “minimum necessary”; example fields are introduced as “may include,” not a closed allowlist. | **Important** privacy/deletion boundary; exact fields retained after purge should be settled before implementation. |
| RA18-A05 | §5.9 FR-ID-16; §8 Feedback entity | Read output calls the optional text “reason,” while the illustrative entity calls it `Comment`; the requirement does not explicitly say whether these are the same field. | **Minor** contract/terminology mismatch; avoid extra or inconsistent feedback fields. |
| RA18-A06 | §5.3 FR-TK-04; §8 TicketAIResult | AI urgency is an explicit suggestion, but the illustrative TicketAIResult fields list summary/category/priority/sentiment and omit urgency. Entities are explicitly non-final. | **Minor/important for traceability**; decide persistence/representation during planning, or explicitly leave urgency transient. |

## 5. Conflicts

No direct contradictory statements were identified in the current v1.8 text. The prior v1.7 ambiguities about Customer retention without tickets, Agent Customer-access grants, central triage/Manager access, and tenant-deletion precedence are resolved in v1.8. RA18-A01–A06 are omissions/underspecifications, not silently resolved conflicts.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance | Impact |
|---|---|---|---|
| RA18-M01 | Resolution of RA18-A01 and RA18-A02. | **Blocking** | Permission behavior and lifecycle acceptance tests cannot be completed without inventing authorized actors/exception policy. |
| RA18-M02 | Whether Platform Admin investigations are in first-release scope and, if so, the authorization workflow and limits. | **Important; conditional** | Could create privileged Customer access inconsistent with the default-deny/no-routine-access boundary. |
| RA18-M03 | Closed allowlist of retained audit fields after permanent tenant deletion. | **Important** | Deletion acceptance and privacy tests cannot prove the “minimum necessary” requirement without a bounded field policy. |
| RA18-M04 | Provider/model/region, per-model token/cost limits, email sender/provider configuration, and bounded operation-specific timeout/retry values (explicit §17 open questions). | **Important, intentionally deferred** | These block final environment/provider configuration, but are expressly reserved for model/subscription/implementation validation and do not change the stated business scope. |
| RA18-M05 | Feedback `reason`/`Comment` mapping and whether/how AI urgency is persisted (RA18-A05/A06). | **Minor to important** | API/data traceability and tests may diverge if the terms or persisted outputs are assumed. |
| RA18-M06 | Exact implementation schemas, indexes, foreign keys, API schemas/status/error contracts, and final queue assignment mechanics. | **Non-blocking at analysis** | §8–9 explicitly label data/API contracts illustrative/design-time; decide in planning without changing business rules. |

## 7. Assumptions

| ID | Assumption | Impact | Confirmation required |
|---|---|---|---|
| RA18-AS01 | CloudDesk and all seed/evaluation content are fictional/synthetic, as explicitly stated. | Prevents use of real customer data and supports privacy boundaries. | No; source-explicit. |
| RA18-AS02 | Azure AI/search resources are available, subject to region/quota/pricing validation. | Availability and cost can affect deployment and model choice. | Yes before corresponding configuration/deployment; already recorded as an open assumption. |
| RA18-AS03 | “Proposed” retention and evaluation values remain configurable defaults/non-gating as stated, not regulatory commitments or approved release thresholds. | Avoids converting suggestions into business commitments. | No change inferred; retain stated status. |
| RA18-AS04 | The current conversation authorization and abandoned-attempt clarification govern process execution only. | No product behavior derives from process metadata. | No product decision is inferred. |

## 8. Technical Impact

- **API/service/domain:** Central default-deny policy enforcement, tenant/team/owner scope on each operation, explicit ticket transition and request/approval workflows, role-limited Customer/Feedback access, and tenant lifecycle/deletion rules.
- **Data/index/storage:** Version-specific knowledge approval and stale-index invalidation; persisted jobs/results; ticket activity/request history; retention timers and relationship revalidation; tenant deletion, backup/deletion replay, and restricted audit residue. Illustrative entities are not schema authorization.
- **Frontend:** Role-scoped administration, ticket/approval/job/Customer/Feedback workflows, masked email, safe failure states, and displayed AI suggestions/citations/status.
- **AI/integrations:** Read-only tool allowlist, approved-source retrieval, typed and validated outputs, human-review boundary, model/search provider configuration, rate/timeout/retry controls, real email and recipient validation.
- **Security/privacy:** Server-side authorization on direct-ID and async paths, no identifier enumeration, no secrets or unneeded personal data in prompts/logs, audited unmasking/privileged changes, protected deletion metadata, and safe email recovery.
- **Testing/operations:** Unit/integration/API/security/end-to-end and evaluation coverage required by §13–14/§18; CI, telemetry, cost caps/alerts, reproducible deployment, synthetic data, and documented limitations. No implementation/code/test/repository architecture was evaluated in this analysis; these are impacts of the written requirement, not observed implementation facts.

## 9. Questions Requiring Human Decision

**Blocking before the requirement can be finalized for complete verification:**

1. **RA18-Q-01 (RA18-A01):** Should the first release permit assigning an Agent to a ticket outside that Agent’s single primary team? If yes, who approves the exception, what eligibility/scope/duration applies, and how is it revoked and audited? If no, confirm that the exception clause is not supported in the first release.
2. **RA18-Q-02 (RA18-A02):** Which roles and conditions may transition a `New` ticket to `Open` (for example, ticket creator/assigned Agent, assigned-team Manager, Tenant Admin)? Do not infer this from “authorized user.”

**Important boundary decisions before the affected capability is implemented or retained in scope:**

3. **RA18-Q-03 (RA18-A03):** Is separately authorized Platform Admin Customer investigation included in the first release? If yes, specify the authorizer, purpose/scope, approval/expiry or revalidation controls, permitted fields/actions, and audit expectations; otherwise explicitly defer/exclude it.
4. **RA18-Q-04 (RA18-A04):** Which exact audit fields may remain after permanent tenant deletion? Confirm a minimal allowlist consistent with the stated exclusion of personal email, secrets, unnecessary personal data, and deleted business/customer content.

**Non-blocking terminology/model clarification:**

5. **RA18-Q-05 (RA18-A05/A06):** Is Feedback `reason` the same value as illustrative `Feedback.Comment`, and must AI urgency suggestions be persisted or may they remain transient? These can be resolved during authorized Requirement Update/planning if they affect the approved contract.

**Explicitly deferred §17 configuration decisions (not newly resolved here):** exact Azure AI generation/embedding deployments and region; token limits and monthly cost budget; email provider/sender/deployment; and bounded per-operation background timeouts/retries. Resolve them through the appropriate later decision/configuration work, not by assumption.

## 10. Analysis Conclusion

- **Requirement Analysis outcome:** Complete static analysis of v1.8; human decisions required for identified product questions.
- **Human decisions incorporated:** The seven decision groups listed in §2, traced to the latest Requirement Update and prior decision-linked Analysis records. The current invocation approval/abandoned-directory clarification are not included as product decisions.
- **Blocking decisions:** RA18-Q-01 and RA18-Q-02. RA18-Q-03/Q-04 are important conditional security/privacy decisions; RA18-Q-05 is a lower-priority contract clarification.
- **Ready for Requirement Analysis Verification:** **No—not for the complete lifecycle handoff while the blocking questions remain unresolved.** Resolve decisions using the separately governed Requirement Update process if v1.8 must change, then perform fresh Requirement Analysis/refresh and independent Verification. This report does not verify itself.
- **Next step:** Human answers the questions above. No Requirement Update, Verification, approval, planning, implementation, or acceptance was performed or authorized by this report.
- **Approval status:** v1.8 remains a Draft Updated Requirement; unapproved. No human approval/acceptance or implementation authorization is claimed.

### Limitations and preservation

Analysis was read-only against v1.8 and supporting records. Current invocation was bound to repository `ScalableParimal/SupportIQ`, branch `SupportIQ-Requirement-Analysis`, HEAD `6e82033850ade3c8e621b5cac5aa26f1c62f7ba2`, with a clean tree at invocation. The source hash remained unchanged after analysis. The portability assessment reported a prior HEAD (`1146170be88c1f8dbb88f428efccba56bdf7c7a3`); it was used only as historical advisory/provenance evidence. No code, tests, configuration, implementation plan, Requirement, or upstream/prior process record was changed; no tests/builds, Requirement Analysis Verification, external service check, commit, or push was performed. Process records published are limited to this attempt scope.
