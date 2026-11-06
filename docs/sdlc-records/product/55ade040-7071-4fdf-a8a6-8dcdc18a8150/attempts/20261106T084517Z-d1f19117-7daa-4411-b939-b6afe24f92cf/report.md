# Requirement Analysis

**Feature:** SupportIQ Product Requirement v1.10  
**Attempt:** `20261106T084517Z-d1f19117-7daa-4411-b939-b6afe24f92cf`  
**Authoritative source:** [SupportIQ_Product_Requirement_v1.10.md](../../../../../requirement/SupportIQ_Product_Requirement_v1.10.md)  
**Source binding:** 130,841 bytes; SHA-256 `93DB568F180A4B6BCFB10B1244730007F96EBE087ABDBC176DC41F63854C60F6`; Draft Updated Requirement, unapproved.

This is a Requirement Analysis, not Requirement Approval. The prior complete analysis of v1.9 was used as the baseline for unchanged content; the v1.9-to-v1.10 changes were checked across scope, role permissions, workflows, data/API descriptions, acceptance criteria, tests, and Definition of Done. The five prior human decisions are linked in [human-decisions-verbatim.json](../20261106T082331Z-db49e004-4ef6-4bae-a9aa-b76af9ee37fb/evidence/human-decisions-verbatim.json). No product requirement, code, tests, or configuration was changed.

## 1. Understanding

SupportIQ is a fictional, learning-oriented, multi-tenant customer-support portal for internal support staff. Its first demonstrable release combines local identity and tenant/team administration; approval-gated knowledge ingestion and RAG; ticket lifecycle and support workflows; AI ticket intelligence and agent assistance; authorized Customer Search and Feedback Read; predefined analytics; persisted jobs; transactional email; and audit, retention, privacy, and operational controls. AI assistance is bounded and non-mutating: authoritative business changes require an authorized human action. The document explicitly is not a production-readiness commitment.

Actors are Platform Admin, Tenant Admin, Support Manager, and Support Agent. External CloudDesk customers cannot access the assistant. Platform Admin manages platform configuration and privileged operations but has no direct access to individual Customer records or exceptional Customer investigation in the first release. Tenant, team, ticket, owner, role, and action scopes are enforced server-side with default-deny behavior.

## 2. Explicit Requirements

- Local ASP.NET Core Identity, four predefined roles, centralized default-deny permissions, tenant/team/resource scope enforcement, and independent second-Platform-Admin approval for defined privileged changes.
- Knowledge documents are versioned and unavailable to RAG/search until the exact version is approved; reprocessing, replacement, or deletion invalidates stale retrieval access.
- Tickets use defined status, category, and priority rules; assignment and transition permissions depend on role, tenant, team, and current assignment. Correction and cancellation requests are distinct workflows. Agents cannot assign/reassign or directly change Category/Priority.
- AI tools are explicitly allowlisted, typed, read-only, scoped, bounded, and audited. Long-running operations use persisted jobs. AI suggestions do not automatically alter authoritative ticket fields; customer-facing messages are not sent automatically.
- Customer Search is constrained by role/ticket relationships; email is masked except for the explicitly authorized Tenant Admin detail operation. Feedback Read has role-specific scope and field minimization.
- Retention, cleanup, tenant deactivation/deletion, audit access, and privacy boundaries are explicit. Post-deletion retention is limited to the irreversibly pseudonymized allowlist, protected and purged by the existing audit-retention expiry.

**Previously supplied human decisions, rechecked against v1.10:**

| Decision | Incorporated outcome |
|---|---|
| RA18-Q-03 | No direct or exceptional Platform Admin access to individual Customer records; only scoped platform administration and explicitly permitted single-tenant aggregate analytics. |
| RA18-Q-04 | Exhaustive post-deletion audit metadata allowlist, irreversible pseudonymization, access protection, and 365-day maximum retention. |
| RA18-Q-05a | `reason` is the canonical optional Feedback field; illustrative `Comment` maps to it; free-text reason is not copied into audit logs. |
| RA18-Q-05b | Persist suggested urgency separately from nullable reviewed urgency, preserve the suggestion, capture model/reviewer metadata, apply 90-day retention, and do not auto-update authoritative ticket data. The specific value set and review semantics remain incomplete; see RA20-Q-01. |
| RA19-A01 | Block Agent primary-team changes until every affected ticket is dispositioned within its current team by the Tenant Admin or Manager of that team; reassign within the same team or clear only the Agent assignment. |

## 3. Scope

### In Scope

The first demonstrable release in §4.1 and the functional modules in §5, including identity/RBAC, tenant and team administration, knowledge approval/RAG, ticket management, AI assistance, Customer Search, Feedback Read, analytics, jobs, email recovery, audit, retention, and deletion. The approved scope remains subject to the 30-day delivery target and later Implementation Planning.

### Out of Scope

The document explicitly excludes external ticketing/CRM/messaging integrations; enterprise SSO, MFA, and passwordless authentication; internal notes; exceptional Platform Admin Customer investigation; AI-invoked write tools/autonomous business-data modifications; custom roles and tenant-specific permission overrides; and other listed deferred capabilities such as SLA indicators and advanced model work.

### Deferred / Undecided

Section 17 intentionally defers exact generation/embedding model deployments and region; model-specific token limits and monthly cost budget; transactional email provider/sender/deployment; and per-operation background timeout/retry settings. The document says to resolve these after the specified availability, compatibility, quota, pricing, subscription, and provider checks. They remain open, are not silently decided here, and are not blockers to this analysis finding. Exact database schema, API payload/error contracts, and implementation sequencing are also design/planning matters as stated in the PRD.

## 4. Ambiguities

| ID | Requirement | Ambiguity | Impact |
|---|---|---|---|
| RA20-Q-01 | §5.3 FR-TK-08/09; §5.10 FR-TM-05/07/14; §8 TicketAIResult; §9 Ticket AI urgency review | v1.10 says to use configured urgency values and allows an authorized human to review, accept, or override, but does not enumerate those values or define the reviewer's exact role scope. It also does not say whether `ReviewedUrgency` remains separate review metadata or, after human action, updates authoritative `Ticket.Priority`. The existing priority set is Critical, High, Medium, and Low, but the requirement does not say that it is also the urgency set. | Affects validation/configuration, permission mapping, the human review workflow, authoritative ticket state, audit/history, and tests. Do not equate urgency with priority or infer reviewer roles. **Blocking to completing this requirement and to readiness for Requirement Analysis Verification.** |

The canonical Feedback `reason`/illustrative `Comment` relationship, Customer access restrictions, deleted-tenant audit allowlist, and Agent primary-team disposition are explicit and consistent; they are not re-raised as questions.

## 5. Conflicts

No direct internal contradiction was identified in the complete v1.9 baseline or the v1.10 successor changes reviewed. The new Platform Admin, deletion, Feedback, and team-change clauses align across the role matrix, workflows, permission mapping, acceptance criteria, tests, and Definition of Done. The general audit-retention wording is expressly subordinated to the exhaustive deleted-tenant boundary.

The predecessor Requirement Analysis contains a process-ordering caveat concerning prepublication inspection and a checkpoint correction. The v1.10 Update preserved it. It is not a product-requirement conflict, and this attempt does not claim to resolve it retroactively. This attempt's own invocation was published and integrity-checked before reviewing v1.10.

## 6. Missing / Incomplete Information

| ID | Missing information | Importance | Impact |
|---|---|---|---|
| RA20-Q-01 | Allowed urgency values (including whether they reuse ticket priorities), precise authorized reviewer roles, and whether a human-reviewed value changes authoritative ticket priority or remains separate. | Blocking for completion/verification of the urgency behavior. | Prevents a traceable validation rule, permission/action mapping, and unambiguous acceptance tests for the newly added AI urgency workflow. |
| §17-OQ-01..04 | Model/region, token/cost limits, email provider/sender, and operation-specific timeout/retry choices. | Important but intentionally deferred. | Needed before corresponding provider/environment configuration; the PRD expressly defers these decisions, and the initiation context asked to preserve that deferral. |

## 7. Assumptions

No new business assumption is introduced. The PRD explicitly identifies CloudDesk and demo data as fictional/synthetic, and identifies the learning-release boundary. The analysis does not assume that urgency equals Priority, does not assign reviewer roles, and does not infer a ticket-field update from the review action.

## 8. Technical Impact

- **API:** Expose the urgency suggestion/review lifecycle and validate a resolved allowed-value set; enforce explicit reviewer authorization on write and retrieval. The PRD's API contracts remain illustrative.
- **Application/domain:** Keep AI suggestion, human-reviewed value, and authoritative ticket fields distinct unless the human decision explicitly couples them. Revalidate current ticket/tenant/team authorization at review time.
- **Database:** Persist the separate suggestion and nullable reviewed value with model/deployment and reviewer/time metadata under the existing 90-day Ticket AI retention. Final schema/index design is deferred to implementation.
- **Frontend:** Clearly distinguish AI-suggested and human-reviewed states and show review controls only to the decided roles; do not imply that a suggestion is an authoritative ticket value.
- **Integration:** Preserve model/deployment traceability. Exact Azure model/region selection and budgets remain §17 deferrals.
- **Testing:** Cover allowed/invalid urgency values, preserved original suggestion, accept/override behavior, reviewer-role denial, tenant/team/ticket isolation, retention, and no automatic authoritative-ticket mutation. If a human action updates Priority, test the existing priority state/role rules and ticket history.
- **Security/privacy:** Enforce default-deny scope on AI-result storage and retrieval; preserve the already defined customer, feedback, audit, pseudonymization, and tenant-deletion boundaries.
- **Performance/operations:** Existing async-job, timeout, token, rate, and concurrency controls apply. Provider-specific settings and cost caps remain deferred as documented.

These are requirement-derived impacts, not observations about implemented code. No code or runtime was inspected.

## 9. Questions Requiring Human Decision

Please resolve the following as one decision group so any authorized Requirement Update can incorporate it in one pass:

1. **Allowed urgency values:** Which exact values should `SuggestedUrgency` and `ReviewedUrgency` accept? Should they reuse Ticket.Priority (`Critical`, `High`, `Medium`, `Low`) or use a distinct configured urgency set? If distinct, provide the full set.
2. **Reviewer authority:** Which existing roles may review, accept, or override urgency, and over which tickets (for example, assigned Support Agent only, assigned-team Support Manager, Tenant Admin within tenant, or a specified combination)?
3. **Effect of review:** Does an accepted/overridden `ReviewedUrgency` remain separate AI-review metadata, or update the authoritative `Ticket.Priority`? If it updates Priority, specify applicable roles and eligible ticket states under the existing ticket rules.

The four §17 configuration decisions remain deferred as requested; this analysis does not ask to select them now.

## 10. Analysis Conclusion

- **Requirement analysis outcome:** Complete with one material unresolved decision, RA20-Q-01.
- **Ready for requirement finalization:** No, pending the urgency decision group.
- **Blocking decisions:** RA20-Q-01. The §17 provider/configuration decisions remain explicitly deferred and are not treated as blockers here.
- **Ready for Requirement Analysis Verification:** No. Resolve RA20-Q-01 through the applicable separately authorized Requirement Update, then perform the required post-update Requirement Analysis refresh before independent Requirement Analysis Verification.
- **Human Requirement Approval:** Not given or implied; v1.10 remains draft and unapproved.
- **Next step:** Await the human decisions above. The answers alone do not authorize a Requirement Update or another process; that process requires its own explicit initiation approval. Preserve, without retroactive claims, the predecessor process-ordering caveat.
