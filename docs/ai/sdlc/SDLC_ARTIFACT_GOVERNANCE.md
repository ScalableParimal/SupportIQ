# SDLC Artifact Governance

## 1. Purpose

This document defines the governance model for the artifacts used by the AI-assisted SDLC.

It establishes:

- the purpose of each governed artifact,
- the source of truth for each artifact,
- the relationship between artifacts,
- who or what may create each artifact,
- who or what may verify each artifact,
- where human approval or acceptance is required,
- which artifacts are read-only verification or investigation outputs,
- the authority and limitations of AI-generated artifacts.

This document complements:

`docs/ai/sdlc/SDLC_GOVERNANCE.md`

The lifecycle and sequencing rules are defined by `SDLC_GOVERNANCE.md`.

The detailed execution rules remain in the applicable guideline documents.

---

## 2. Artifact Governance Principles

The following principles apply to all governed SDLC artifacts:

1. Every governed artifact must have a defined purpose.
2. Every governed artifact must have an identifiable source of truth.
3. A downstream artifact must use the current approved upstream artifact where approval is applicable.
4. AI-generated artifacts do not automatically become approved artifacts.
5. AI verification does not constitute human approval.
6. AI review does not constitute human acceptance.
7. Human approval and acceptance must be explicit.
8. Verification artifacts must not silently modify the artifact being verified.
9. Investigation artifacts must not directly implement corrective changes.
10. Corrective decisions must not bypass the applicable human approval gate.
11. An artifact must not silently redefine the authority of another governed artifact.
12. Superseded artifacts must not be treated as current approved artifacts.
13. Traceability must be maintained between related governed artifacts.
14. When a material upstream artifact changes, downstream artifacts must be evaluated for impact.

---

## 3. Governed Artifact Categories

The SDLC uses the following major governed artifact categories:

### 3.1 SDLC Execution Artifacts

1. Requirement
2. Requirement Analysis
3. Requirement Analysis Verification
4. Approved Requirement
5. Implementation Plan
6. Implementation Plan Verification
7. Approved Implementation Plan
8. Implementation
9. Implementation Self-Check
10. Implementation Verification
11. Implementation Review
12. Finding
13. Finding Investigation
14. Corrective Change Decision & Plan Update
15. Human Approval / Acceptance
16. Commit / Push Evidence

### 3.2 SDLC Governance Execution Artifacts

The SDLC Governance Framework also governs the reusable execution mechanisms used to perform the controlled SDLC activities:

17. SDLC Process Skill
18. SDLC Process Agent

SDLC Process Skills and SDLC Process Agents are governance framework artifacts. They define and execute the controlled AI execution boundary for governed SDLC activities but do not replace the underlying Guidelines, Prompts, Requests, or Master Governance documents.

The current SDLC Process Skill set consists of:

1. Requirement Analysis Skill
2. Requirement Analysis Verification Skill
3. Implementation Planning Skill
4. Requirement Update Skill
5. Implementation Plan Verification Skill
6. Implementation Skill
7. Implementation Verification Skill
8. Implementation Review Skill
9. Finding Investigation Skill
10. Corrective Change Decision & Plan Update Skill

1. Requirement Analysis Agent
2. Requirement Analysis Verification Agent
3. Implementation Planning Agent
4. Implementation Plan Verification Agent
5. Implementation Agent
6. Implementation Verification Agent
7. Implementation Review Agent
8. Finding Investigation Agent
9. Corrective Change Decision Agent

Requirement Update is currently Skill-only and does not have a dedicated SDLC Process Agent.

The two Governance Agents:

- `sdlc-governance-audit`
- `sdlc-governance-remediation`

are Governance Control Agents. They govern and remediate the SDLC Governance Framework itself and are separate from the SDLC Process Agents that execute normal product SDLC activities.

These artifacts may be represented by documents, reports, source code, tests, repository state, configuration, Skills, Agents, or other governed records as applicable.

### 3.3 SDLC Process Orchestration Mechanism

The SDLC Process Orchestrator is a governed coordination mechanism under this same SDLC Governance Framework and the authority of the three Master Governance documents. It coordinates the sequence and invocation of existing governed SDLC processes; it does not create governance authority.

The Orchestrator is functionally distinct from the 52 core SDLC process artifacts/mechanisms and is not included in or added to that numerical catalog. The SDLC Governance Audit and SDLC Governance Remediation mechanisms are Governance Control mechanisms under the same framework and the same three Masters; they are functionally distinct from both the 52 core catalog and the Orchestrator. These mechanism categories do not establish separate frameworks, hierarchies, or sources of authority.

---

### 3.4 SDLC Portability Assessment Mechanism

The SDLC Portability Assessment is a separately reported, same-framework governance mechanism for assessing applicability of this framework to an identified target project. It is not a separate framework, is not added to the 52-core catalog, and does not create a product requirement, implementation plan, or parallel approval lifecycle.

Its connected artifacts are the Portability Assessment Guideline, Prompt, Request, Skill, and Agent listed in section 24 of `SDLC_GOVERNANCE.md`. The Agent is its explicit entry point and follows its Skill; the Skill uses the Prompt and Request under the Guideline.

An assessment distinguishes the source-framework baseline from the target-project baseline and evidence. It is read-only with respect to both. It may recommend compatibility, adaptations, incompatibilities/possible blockers, evidence gaps, or not-applicable dimensions. The responsible human for the target project decides whether an assessment-recommended possible blocker applies. The Agent must not automatically invoke other Agents, change either repository, approve a requirement/plan, or initiate implementation.

The entry timing, reassessment conditions, evidence standards, routing, persistence, and report requirements are governed by the dedicated Guideline and by the three Masters. Portability assessment findings about framework governance are not Governance Audit findings merely by being reported. Governance Audit assesses this mechanism and its integration separately from the 52 core; Governance Remediation may act only on actual findings within its approved finding-led scope.

---

### 3.5 Governance Amendment Assurance Mechanisms

Governance Amendment Application, Independent Governance Verification, and Independent Governance Review are separately reported, same-framework mechanisms under the three Masters. Each comprises exactly five artifacts—Guideline, Prompt, Request, Skill, and Agent—as listed in `SDLC_GOVERNANCE.md` §24. They are outside the 52-core SDLC Process catalog and do not create a separate framework or authority.

The Application Agent is the sole standing process actor authorized to apply a governance amendment only after the applicable Human Approval and exact scope are established. Until this mechanism is effective, the approval record must designate a qualified one-time initial application actor.

For this initial route, “qualified” means designated by Human Approval for the one-time Application; it does not require a separate pre-existing runtime qualification record. Human Approval and actor designation do not establish or waive capability. After a fresh Application stage-start and before any source write, the designated actor must establish, publish, and integrity-check current-environment identity, permissions, publication route, and all role-specific capability evidence in its own Application attempt, including every Application check listed below. Missing or uncertain evidence blocks source writes with `CANNOT COMPLETE`. The designated actor must be distinct from the proposal preparer, SDLC Process Orchestrator, any Governance Remediation actor barred from self-edit in its active cycle, verifier, and reviewer. This clarification does not relax the universal current-invocation evidence requirement in section 33.1 or the role-specific capability, independence, fresh stage-start, or read-only boundary for any other actor. The actor must verify every base fingerprint before writing, apply only approved bytes to approved paths, and record exact before/after fingerprints, changed-path list, applied content binding, and any partial outcome. It must stop on mismatch or error and may not commit or push.

The Verification Agent independently and read-only checks approval-to-application identity, exact paths and bytes, base/after fingerprints, absence of unauthorized changes, and cross-artifact consistency. The Review Agent independently and read-only evaluates governance correctness, authority, scope, lifecycle, human gates, and assurance adequacy. The actors must be distinct from the proposal preparer and applier and from each other. Each publishes a separate evidence-bound result; neither approves, applies, or accepts a change.

No role gains authority from its name, Skill, Agent capability, or successful output. Only explicit Human Approval authorizes the exact application. A governance amendment becomes effective only after authorized application, passing independent Verification and Review, and a complete Audit that reports `CONSISTENT`, all required counts at zero, and all seven mechanism groups assessed without unresolved issues. A Master change additionally requires separate prospective-baseline adoption after those gates.

Runtime capability and actor-boundary contract: an Agent definition, name, Skill, or available tool does not establish effective authority or executable capability. Before each role invocation, its actor must inspect the current runtime tool declarations and permission context and record the capability evidence in its own attempt. Application requires repository reads, SHA-256 computation, path/status and exact-content checks, exact writes to only the approval-bound target paths, post-write reads and hashes, and publication to its own authorized record scope. Verification and Review require repository/evidence reads, SHA-256 computation, their specified read-only check execution, and publication to their own authorized record scopes. All three roles must confirm that the Work ID scope and record output location are authorized and that publication is available before proceeding. Confirmation may use only non-mutating read/hash/check operations and the authorized record publisher. Record declared and observed capabilities separately. If any required capability, identity, permission, or publication path is unavailable or cannot be verified, return `CANNOT COMPLETE` before source action; no success result or effectiveness claim is permitted. Application must preflight every base before the first write and read back every target afterward, confirming exact file identity and expected-after hash. Verification and Review must independently publish their own integrity-bound reports and evidence. Each stage is separately and freshly human-initiated; exact patch approval is not stage initiation, and no role may automatically initiate another stage.

## 4. Artifact Authority Model

The following authority model applies:

| Artifact | Primary Authority |
|---|---|
| Requirement | Business / Human |
| Requirement Analysis | AI analysis |
| Requirement Analysis Verification | Independent AI verification |
| Approved Requirement | Human approval |
| Implementation Plan | AI-generated technical plan |
| Implementation Plan Verification | Independent AI verification |
| Approved Implementation Plan | Human approval |
| Implementation | Repository implementation |
| Implementation Self-Check | AI implementation validation |
| Implementation Verification | Independent AI verification |
| Implementation Review | Independent AI engineering review |
| Finding | Verification / Review / Engineering evidence |
| Finding Investigation | AI investigation |
| Corrective Change Decision & Plan Update | Governed AI recommendation subject to required Human Approval |
| Human Approval | Human authority |
| Human Acceptance | Human authority |
| Commit / Push | Repository change evidence after required acceptance |
| SDLC Process Skill | Governed reusable AI execution procedure |
| SDLC Process Agent | Governed AI execution boundary and process entry point |

### 4.1 Skill Authority

A SDLC Process Skill defines the reusable execution procedure for a governed SDLC activity.

A Skill:

- operates under the authority of the applicable Master Governance documents,
- must comply with the applicable Guideline,
- uses the applicable Prompt and Request as controlled inputs,
- must not redefine governance authority,
- must not silently change the governing Guideline, Prompt, Request, Requirement, or Implementation Plan,
- must respect the read/write and approval boundaries defined by the governed process.

A Skill does not constitute human approval or acceptance.

### 4.2 Agent Authority

A SDLC Process Agent provides the controlled execution boundary for a governed SDLC process.

An Agent:

- invokes or follows its designated Skill,
- operates within the authority and permissions defined for that process,
- must respect the applicable Master Governance, Guideline, Prompt, Request, and Skill,
- must not silently redefine the governed process,
- must not acquire authority that is not explicitly granted by the applicable governance framework,
- must not claim Human Approval or Human Acceptance.

An Agent does not become authoritative over the underlying Requirement, Implementation Plan, or other governed artifact merely because it is capable of modifying or evaluating it.

### 4.3 Governance Control Agents

The SDLC Governance Audit Agent and SDLC Governance Remediation Agent are Governance Control Agents.

They operate exclusively on the SDLC Governance Framework and are separate from SDLC Process Agents.

They must not execute or remediate product-specific SDLC work.

AI must not elevate any Skill or Agent output to a human-authorized status.

### 4.4 SDLC Process Orchestrator Authority

The SDLC Process Orchestrator is a coordination mechanism subordinate to the three Master Governance documents and the applicable governed process definitions. It may determine the next process permitted by the approved lifecycle, coordinate the invocation of the designated Process Agent or Requirement Update Skill, validate process preconditions and postconditions, preserve its own execution state and traceability, stop when authority or evidence is missing, and route findings through the established corrective lifecycle.

The Orchestrator must not define or override governance policy; change an approved Requirement or Implementation Plan except through its governed change process; perform or approve another process's work; publish another process actor's report, result, or substantive human decision as its own; or bypass verification, review, Human Approval, Human Acceptance, or corrective controls. It may reference and assess the applicability of the owning process actor's published result but must not replace or re-author that result. It does not become a Governance Control Agent. Process Initiation Approval is an Orchestrator-specific execution interlock, not a formal Human Approval or authorization to perform an otherwise unauthorized action.

Before every Orchestrator-invoked process start, retry, and transition into a process, a fresh explicit Process Initiation response for that exact invocation is mandatory; no exception, inferred response, or reused response is permitted. This response authorizes only initiation of that invocation. It is not a formal Human Approval, does not satisfy any formal Human Gate, and does not authorize an action that is otherwise unauthorized.

---

## 5. Requirement

### 5.1 Purpose

The Requirement defines the business need and expected behavior of the feature or change.

It may define:

- business objectives,
- functional requirements,
- non-functional requirements,
- scope,
- constraints,
- business rules,
- acceptance expectations,
- required decisions.

### 5.2 Source of Truth

The Requirement is the authoritative business source of truth.

### 5.3 Created By

The Requirement may be created or maintained through a human-led process with AI assistance where appropriate.

### 5.4 Verified By

The Requirement itself is not approved by AI verification.

Requirement Analysis Verification verifies the analysis and resulting requirement state before Human Requirement Approval.

### 5.5 Approved By

Human Requirement Approval.

### 5.6 Authority

The approved Requirement controls the business scope and expected behavior.

The Requirement must not be silently redefined by an Implementation Plan or source code.

---

## 6. Requirement Analysis

### 6.1 Purpose

Requirement Analysis examines the Requirement to identify:

- ambiguities,
- missing information,
- conflicts,
- assumptions,
- business rules,
- scope boundaries,
- dependencies,
- relevant technical impact,
- decisions requiring human input.

### 6.2 Source of Truth

The current Requirement and explicitly supplied human decisions.

### 6.3 Created By

AI.

### 6.4 Verified By

Requirement Analysis Verification.

### 6.5 Human Approval

Requirement Analysis itself does not constitute Human Requirement Approval.

### 6.6 Authority

Requirement Analysis may identify issues and recommend decisions.

It must not silently make unresolved human business decisions.

---

## 7. Requirement Analysis Verification

### 7.1 Purpose

Requirement Analysis Verification independently verifies the complete current Requirement Analysis and resulting updated Requirement against the applicable source material and decisions.

### 7.2 Source of Truth

- current Requirement,
- current Requirement Analysis,
- applicable human decisions,
- applicable governance guidelines.

### 7.3 Created By

AI.

### 7.4 Modification Authority

The verification process is read-only.

It must not directly modify the Requirement or Requirement Analysis.

### 7.5 Human Approval

Verification does not constitute Human Requirement Approval.

### 7.6 Authority

The verification report provides evidence, findings, gaps, and recommended next processes.

It does not authorize implementation planning.

---

## 8. Approved Requirement

### 8.1 Definition

An Approved Requirement is the Requirement that has completed the required analysis, verification, resolution of material findings and decisions, and Human Requirement Approval.

### 8.2 Authority

The Approved Requirement is the business source of truth for downstream implementation planning and implementation.

### 8.3 Supersession

When a new Requirement version is approved, the previous approved version becomes superseded.

Downstream artifacts must be evaluated for impact.

---

## 9. Implementation Plan

### 9.1 Purpose

The Implementation Plan translates the Approved Requirement into an actionable technical implementation approach.

It may define:

- implementation tasks,
- architecture alignment,
- components,
- dependencies,
- sequencing,
- interfaces,
- persistence design,
- validation,
- testing,
- acceptance criteria,
- technical assumptions,
- implementation constraints.

### 9.2 Source of Truth

The current Approved Requirement and applicable technical context.

### 9.3 Created By

AI.

### 9.4 Verified By

Implementation Plan Verification.

### 9.5 Approved By

Human Plan Approval.

### 9.6 Authority

The Approved Implementation Plan is the implementation source of truth.

Implementation must not silently redefine the plan.

---

## 10. Implementation Plan Verification

### 10.1 Purpose

Implementation Plan Verification independently verifies the complete current Implementation Plan against the current Approved Requirement and applicable technical constraints.

### 10.2 Source of Truth

- current Approved Requirement,
- current Implementation Plan,
- applicable architecture,
- engineering guidelines,
- repository constraints,
- technical evidence.

### 10.3 Created By

AI.

### 10.4 Modification Authority

Read-only.

It may recommend plan changes but must not apply them.

### 10.5 Human Approval

Verification does not constitute Human Plan Approval.

### 10.6 Authority

The verification report determines whether the plan is ready for the applicable human approval gate or whether findings must be resolved.

---

## 11. Approved Implementation Plan

### 11.1 Definition

An Approved Implementation Plan is the Implementation Plan that has completed:

- Implementation Plan Verification,
- required finding and decision resolution,
- Human Review Approval,
- Human Plan Approval.

### 11.2 Authority

The Approved Implementation Plan is the implementation source of truth.

### 11.3 Corrective Changes

If the plan changes materially, the changed plan must pass through the applicable governed plan update, verification, and approval process before it becomes the current Approved Implementation Plan.

---

## 12. Implementation

### 12.1 Purpose

Implementation is the actual repository change required to satisfy the Approved Requirement using the Approved Implementation Plan.

### 12.2 Source of Truth

- current Approved Requirement,
- current Approved Implementation Plan,
- actual repository state.

### 12.3 Created By

AI may implement the approved work under the governed implementation process.

### 12.4 Authority

Implementation is not authoritative over the Requirement or Implementation Plan.

If implementation reveals a material conflict, the applicable governed corrective process must be followed.

### 12.5 Human Acceptance

Implementation becomes accepted only after the applicable verification, review, and Human Acceptance gates are completed.

---

## 13. Implementation Self-Check

### 13.1 Purpose

Implementation Self-Check provides immediate implementation-level validation after implementation.

It may include:

- build,
- tests,
- architecture checks,
- traceability checks,
- diff inspection,
- repository consistency checks.

### 13.2 Source of Truth

- current Approved Requirement,
- current Approved Implementation Plan,
- actual repository.

### 13.3 Created By

AI or the implementation process.

### 13.4 Authority

Implementation Self-Check is not formal Implementation Verification.

It does not constitute Human Acceptance.

---

## 14. Implementation Verification

### 14.1 Purpose

Implementation Verification independently verifies the complete current implementation against the current Approved Requirement and current Approved Implementation Plan.

### 14.2 Source of Truth

- current Approved Requirement,
- current Approved Implementation Plan,
- actual repository,
- applicable architecture,
- engineering guidelines,
- available evidence.

### 14.3 Created By

AI.

### 14.4 Modification Authority

Read-only.

It must not apply corrections.

### 14.5 Human Approval

Implementation Verification does not constitute Human Acceptance.

### 14.6 Authority

The verification report determines whether the implementation is verified, has gaps, requires changes, or cannot be fully verified.

---

## 15. Implementation Review

### 15.1 Purpose

Implementation Review evaluates the complete current implementation from an engineering and quality perspective.

It may evaluate:

- architecture,
- design quality,
- code quality,
- error handling,
- validation,
- data integrity,
- security,
- performance,
- testing,
- configuration,
- operational concerns,
- repository consistency.

### 15.2 Source of Truth

- current Approved Requirement,
- current Approved Implementation Plan,
- current implementation,
- Implementation Verification results,
- applicable engineering guidelines.

### 15.3 Created By

AI.

### 15.4 Modification Authority

Read-only.

The review must not directly apply corrections.

### 15.5 Human Acceptance

Implementation Review does not constitute Human Acceptance.

---

## 16. Finding

### 16.1 Purpose

A Finding identifies a potential or confirmed issue discovered during a governed activity.

Findings may originate from:

- Requirement Analysis Verification,
- Implementation Plan Verification,
- Implementation Verification,
- Implementation Review,
- testing,
- other governed engineering activities.

### 16.2 Authority

A Finding is evidence or an identified issue.

A Finding is not itself a corrective authorization.

### 16.3 Required Handling

Material findings must follow the Finding Investigation and Corrective Change Decision & Plan Update process.

---

## 17. Finding Investigation

### 17.1 Purpose

Finding Investigation determines whether a finding is valid and, where possible:

- validates the finding,
- determines root cause,
- identifies affected artifacts,
- evaluates impact,
- evaluates corrective options,
- determines whether human decision or approval is required.

### 17.2 Source of Truth

The source depends on the affected artifact.

Investigation must inspect the applicable approved source documents and actual repository state.

### 17.3 Created By

AI.

### 17.4 Modification Authority

Read-only.

Finding Investigation must not directly implement corrections.

### 17.5 Authority

The investigation produces evidence and recommendations.

It does not itself authorize corrective implementation.

---

## 18. Corrective Change Decision & Plan Update

### 18.1 Purpose

This artifact determines:

- whether a finding is accepted or rejected,
- the corrective direction,
- the affected governed artifact,
- whether the current Implementation Plan remains valid,
- whether a plan update is required,
- whether human approval is required,
- the appropriate next process.

### 18.2 Source of Truth

Applicable:

- Finding Source,
- Affected Artifact,
- Approved Requirement,
- Current Approved Implementation Plan,
- Finding Investigation,
- repository state,
- evidence,
- applicable guidelines.

### 18.3 Created By

AI.

### 18.4 Modification Authority

The decision artifact does not itself apply the correction.

### 18.5 Human Approval

Required where the corrective decision materially changes an approved governed artifact or otherwise requires human authority.

### 18.6 Authority

A corrective decision must not bypass the applicable human approval and verification process.

---

## 19. Human Requirement Approval

### 19.1 Purpose

Human Requirement Approval establishes that the human has accepted the current Requirement as the business source of truth.

### 19.2 Authority

Human Requirement Approval authorizes the Requirement to proceed to the implementation planning stage.

### 19.3 AI Boundary

AI may recommend readiness for approval.

AI must not claim Human Requirement Approval.

---

## 20. Human Plan Approval

### 20.1 Purpose

Human Plan Approval establishes that the human has accepted the current Implementation Plan as the implementation source of truth.

### 20.2 Authority

Human Plan Approval authorizes implementation against that approved plan.

### 20.3 AI Boundary

AI may recommend readiness for approval.

AI must not claim Human Plan Approval.

### 20.4 Distinction from Human Review Approval

Human Review Approval is a separate, required manual human gate that precedes Human Plan Approval.

It authorizes only progression to Human Plan Approval.

It is not Human Plan Approval, does not approve the plan, and does not authorize implementation.

---

## 21. Human Acceptance

### 21.1 Purpose

Human Acceptance establishes that the human accepts the implemented result after the applicable verification and review activities.

### 21.2 Authority

Human Acceptance is the final human gate before the implementation proceeds to Commit / Push.

### 21.3 AI Boundary

AI may provide evidence and recommend readiness.

AI must not claim Human Acceptance.

---

## 22. Commit / Push Evidence

### 22.1 Purpose

Commit / Push provides repository history evidence of the accepted implementation state.

### 22.2 Preconditions

Commit / Push occur only after the required Human Acceptance gate.

### 22.3 Authority

A commit does not retroactively constitute Requirement Approval, Plan Approval, Verification, Review, or Human Acceptance.

Repository history is evidence of the change, not a replacement for governance gates.

---

## 23. SDLC Process Skill

### 23.1 Purpose

An SDLC Process Skill is the reusable AI execution procedure for a governed SDLC activity.

The Skill translates the applicable governance framework, Guideline, Prompt, and Request into a controlled execution flow without redefining their authority.

### 23.2 Source of Authority

A Skill operates under:

- the three Master Governance documents,
- the applicable Guideline,
- the applicable Prompt,
- the applicable Request,
- the current approved upstream governed artifacts where required.

The Skill itself is not a replacement for any of these sources.

### 23.3 Created By

AI-assisted development may create or maintain Skills under the governed Governance Framework change process.

### 23.4 Modification Authority

A Skill is a governed Governance Framework artifact.

It must not be materially modified outside the applicable Governance change process.

A Skill change must be evaluated for impact on:

- its associated Guideline,
- Prompt,
- Request,
- Agent,
- governed SDLC activity,
- downstream artifacts,
- traceability,
- authority boundaries.

### 23.5 Authority

A Skill may define execution mechanics within its authorized process boundary.

It must not:

- redefine governance policy,
- override a Master Governance rule,
- override an applicable Guideline,
- bypass required human approval,
- bypass required verification,
- silently change an approved Requirement or Implementation Plan,
- directly perform a corrective change outside the governed corrective process.

### 23.6 Verification

A Skill is subject to Governance Audit for consistency with the applicable Master Governance documents and related Guidelines, Prompts, Requests, and Agents.

### 23.7 Human Approval

A Skill does not constitute Human Approval or Human Acceptance.

Material changes to governance policy, lifecycle, authority, scope, or human gates require the applicable human governance decision and approval.

---

## 24. SDLC Process Agent

### 24.1 Purpose

An SDLC Process Agent is the controlled execution entry point for a governed SDLC process.

It provides the process-specific execution boundary and uses the designated SDLC Process Skill.

### 24.2 Source of Authority

An Agent operates under:

- the three Master Governance documents,
- the applicable Guideline,
- the applicable Prompt,
- the applicable Request,
- the designated SDLC Process Skill,
- the current approved upstream governed artifacts where required.

### 24.3 Created By

AI-assisted development may create or maintain SDLC Process Agents under the governed Governance Framework change process.

### 24.4 Modification Authority

An Agent is a governed Governance Framework artifact.

It must not be materially modified outside the applicable Governance change process.

An Agent change must be evaluated for impact on:

- its designated Skill,
- applicable Guideline,
- Prompt,
- Request,
- governed SDLC activity,
- authority and write boundaries,
- downstream artifacts,
- traceability.

### 24.5 Authority

An Agent may execute only within its explicitly defined process boundary.

An Agent must not:

- redefine the governed process,
- bypass its designated Skill,
- bypass required human approval,
- perform activities assigned to another governed process,
- silently modify governed upstream artifacts,
- claim Human Approval,
- claim Human Acceptance,
- perform corrective implementation when its process does not authorize it.

### 24.6 Verification

An Agent is subject to Governance Audit for:

- existence,
- correct Skill reference,
- correct process identity,
- authority alignment,
- read/write boundary,
- approval boundary,
- process boundary,
- consistency with the applicable Guideline, Prompt, Request, and Skill.

### 24.7 Human Approval

An Agent does not constitute Human Approval or Human Acceptance.

The Agent must stop when its process requires a human decision or approval that has not been provided.

---

## 25. Artifact Lifecycle Relationship

The primary artifact relationship is:

    Requirement
       ↓
    Requirement Analysis
       ↓
    Requirement Analysis Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Requirement Approval
       ↓
    Implementation Plan
       ↓
    Implementation Plan Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Implementation
       ↓
    Implementation Self-Check
       ↓
    Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance
       ↓
    Commit / Push

The approved artifacts are the authoritative downstream inputs:

    Approved Requirement
            ↓
    Approved Implementation Plan
            ↓
    Accepted Implementation

---

## 26. Finding Artifact Relationship

When a material finding occurs:

    Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision & Plan Update
       ↓
    Required Human Approval
       ↓
    Approved Change
       ↓
    Required Verification
       ↓
    Required Review
       ↓
    Human Acceptance where applicable

The finding process must not bypass the governing artifact lifecycle.

---

## 27. Artifact Status Model

The following conceptual statuses may be used where applicable:

- Not Started
- In Progress
- Verification Pending
- Verification Passed
- Verification With Gaps
- Changes Required
- Blocked
- Human Approval Pending
- Human Acceptance Pending
- Accepted
- Superseded

`Accepted` and `Human Acceptance` must not be used by AI to represent an actual human decision unless the human decision has occurred.

---

## 28. Approved vs Verified vs Accepted

These terms have distinct meanings.

### Verified

The applicable AI verification activity has completed according to its guideline.

Verification does not mean human approval.

### Approved

The required human approval has been explicitly provided.

AI must not infer approval from successful verification.

### Accepted

The required Human Acceptance has been explicitly provided.

AI must not infer acceptance from successful implementation, verification, review, or tests.

---

## 29. Current vs Superseded Artifacts

An artifact is current when it is the version applicable to the active governed process.

An approved artifact becomes superseded when a newer approved version replaces it.

Examples include:

- a new Approved Requirement,
- a new Approved Implementation Plan,
- a corrective change that replaces an accepted implementation state.

Downstream processes must use the current applicable approved artifact.

Superseded artifacts may remain available for traceability but must not be treated as current authority.

---

## 30. Artifact Modification Rules

Each artifact has a controlled modification boundary.

| Artifact | May Be Modified Directly During Verification? | Corrective Process Required for Material Change? |
|---|---|---|
| Requirement | No | Yes |
| Requirement Analysis | No | Yes where governed change is required |
| Implementation Plan | No | Yes |
| Implementation | No during verification/review | Yes where material governed change is required |
| Tests | No during verification/review | Yes where governed change is required |
| Configuration | No during verification/review | Yes where governed change is required |
| Documentation | No during verification/review | Yes where governed change is required |

Verification and review activities identify and route changes.

They do not directly apply those changes.

---

## 31. Task IDs and Artifact Scope

Task IDs may be used to:

- identify implementation work,
- identify implementation context,
- identify related findings,
- provide traceability.

Task IDs must not automatically redefine the scope of:

- complete Implementation Plan Verification,
- complete Implementation Verification,
- complete Implementation Review,
- Finding Investigation where broader affected-artifact context is required.

A task ID is context unless the applicable governance document explicitly defines it as the complete scope.

---

## 32. Traceability Requirements

Where applicable, the following relationships must be traceable:

| Downstream Artifact | Must Trace To |
|---|---|
| Requirement Analysis | Requirement |
| Requirement Analysis Verification | Requirement + Requirement Analysis |
| Approved Requirement | Requirement + Verification + Human Approval |
| Implementation Plan | Approved Requirement |
| Implementation Plan Verification | Approved Requirement + Implementation Plan |
| Approved Implementation Plan | Plan + Verification + Human Approval |
| Implementation | Approved Requirement + Approved Implementation Plan |
| Implementation Self-Check | Implementation + Approved Requirement + Approved Plan |
| Implementation Verification | Approved Requirement + Approved Plan + Implementation |
| Implementation Review | Approved Requirement + Approved Plan + Implementation + Verification |
| Finding Investigation | Finding + Affected Artifact |
| Corrective Change Decision | Finding Investigation + Affected Artifact + Applicable Approved Artifacts |
| Human Acceptance | Implementation + Verification + Review |
| Commit / Push | Accepted Implementation |
| SDLC Process Skill | Applicable Master Governance + Guideline + Prompt + Request + Governed SDLC Process |
| SDLC Process Agent | Applicable Master Governance + Guideline + Prompt + Request + SDLC Process Skill + Governed SDLC Process |

---

## 33. Artifact Independence

Each governed artifact must maintain its own purpose and authority.

For example:

- Requirement defines business intent.
- Requirement Analysis identifies requirement issues.
- Implementation Plan defines technical execution.
- Implementation contains the actual code and tests.
- Verification determines conformity.
- Review evaluates engineering quality.
- Human Approval establishes authorization.
- Human Acceptance establishes final acceptance.
- SDLC Process Skill defines reusable AI execution mechanics for a governed process.
- SDLC Process Agent defines the controlled AI execution boundary for a governed process.

One artifact must not silently replace another artifact's responsibility.

A Skill must not replace a Guideline, Prompt, or Request.

An Agent must not replace its designated Skill or the governing Guideline.

A Skill or Agent must not acquire authority that is not explicitly granted by the applicable Governance Framework.

### 33.1 Publication of Existing Governed Process Records

Execution records are durable representations and metadata of existing governed requests, reports, evidence, and human decisions. They are not a new governed artifact category or an independent source of substantive authority.

A process actor may publish its own invocation metadata, checkpoints, required output report, result bindings, and evidence within the explicitly designated record scope, following section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. This permission does not authorize modification of a source or evaluated artifact, another process's records, governance definitions, or approved upstream artifacts.

#### Universal current-invocation qualification and first publication

For every governed AI process actor and every invocation, before consequential work the actor must establish and record: the canonical repository and exact source state; the applicable adopted persistence root (or the narrowly authorized first-use governance-root bootstrap under section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md); stable Work ID; actor identity; authorized process/stage and output scope; current effective identity, permissions, and role-specific capabilities; and all required Human authorization, fresh stage-start, and predecessor gates. Capability evidence must be specific to the current environment and invocation, obtained through non-mutating checks, and include the permitted publication route for the actor's own records. A role/name, declared tool, prior successful invocation, or another actor's evidence is not sufficient. Prior same-actor success is not required when current evidence establishes capability, and historical evidence alone never establishes current capability.

Before consequential work, the actor must publish its own invocation attempt record within the authorized scope using the applicable no-overwrite publication contract, then read back and integrity-check it. A collision, mismatch, missing capability/authorization, or publication/validation failure stops the invocation before consequential work; do not overwrite, perform source actions, or publish a success result. This rule grants no standing authority, Human Approval, stage-start, predecessor result, or effectiveness, and does not relax role-specific read/write, independence, or approval boundaries.

#### First-use bootstrap publication boundary

For a first-use governance-root bootstrap authorized under section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md, the designated process actor may publish its own permitted invocation records, checkpoints, reports, result bindings, and necessary evidence only after validating the independently resolvable Human governance decision and the exact repository, root, Work ID, actor identity, and record scope named by that decision.

The actor's publication authority is limited to its own records and the expressly authorized scope. It does not authorize the actor to create, alter, infer, or transcribe a Human decision that was not actually supplied or explicitly authorized for transcription; publish another actor's records; modify the evaluated governance source files; approve a governance amendment; declare a Governance Audit result; or adopt a Master baseline.

The first bootstrap attempt must reference the actual Human decision evidence by resolvable source identity and location, with sufficient integrity information to detect a change. For a GitHub-hosted repository, this means the canonical issue or pull-request URL and exact comment/review permalink, author identity, timestamp, authorized commit SHA, and the three Master fingerprints specified by section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. The attempt record documents the authorization it relies upon; it does not create that authorization. If the decision cannot be resolved, its scope does not match, or the repository state differs from the authorized state, publication and execution must stop. The candidate Work ID must be collision-checked against both persistence roots before authorization and rechecked immediately before publication; the first successful no-overwrite attempt publication reserves it. Do not create a separate bootstrap-state file or treat a copied decision as the authoritative source.

This provision clarifies the application of the existing publication boundary to the first-use condition. It creates no new record category, persistence root, process actor, lifecycle stage, approval authority, or general exception to this section. All ordinary publication, immutability, evidence, and actor-separation requirements remain in force.

A process actor may publish a request for an existing required human gate associated with its own handoff. AI may persist a human response only when explicitly supplied or explicitly authorized for transcription, preserving its actual wording, attributable source, subject, scope, conditions, and original evidence. AI must not create, revise, infer, or substitute a substantive human decision.

When authorized under the same Governance Framework, the SDLC Process Orchestrator may publish only its own orchestration invocation metadata, checkpoints, report, result bindings, evidence, and Process Initiation interlock request/response within its designated attempt scope and the existing section 30.1 persistence contract. The interlock request and actual supplied response are invocation-authorization metadata for that Orchestrator attempt, not a formal human-gate request or decision; they must not be recorded as Human Requirement Approval, Human Review Approval, Human Plan Approval, Corrective Change Approval, or Human Acceptance. Formal human-gate requests and decisions remain in the existing human-gates records and retain their existing meanings. The Orchestrator may link to, but must not publish, substitute, or alter, another process actor's report/result or a substantive human decision. Any response transcription must preserve the actual supplied wording, attributable source, subject, scope, conditions, and available time. This clarification creates no new record category or persistence convention.

Published final records must not be modified in place. Draft preparation is limited to the actor's own designated unpublished output. Subsequent corrections or supersession must use linked new records under the applicable governed process.

Read-only processes remain read-only with respect to their inputs, evaluated artifacts, and corrective changes. Their permitted output publication is limited to this section and must be explicitly reflected in any otherwise exclusive Skill or Agent write boundary.

Existing authority remains unchanged: approved sources define authorized work; the repository establishes actual implementation; the applicable independent reports establish verification and review conclusions; and actual human decisions establish approval and acceptance. Recording execution position establishes none of those conclusions.

A consolidated execution view is a derived projection. It must not override its sources and may be regenerated from them.

For Governance Audit and Governance Remediation, concise human-facing summaries and downstream handoffs are non-authoritative presentations of process-owned reports and linked evidence. They must identify their sources and must not replace, alter, or independently establish findings, verification conclusions, human decisions, or completion.

The Governance Audit actor may publish only its own invocation metadata, checkpoints, required report, result bindings, and necessary evidence within its explicitly designated record scope. The Governance Remediation actor may publish its own corresponding coordination records and permitted human-gate records, but must link to rather than publish, replace, or alter another actor's report or result. These permissions follow section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md and require explicit alignment of the applicable Skill and Agent boundaries.

Publication permission does not authorize Commit or Push or the creation of a separate Execution State artifact.

---

## 34. AI-Generated Artifact Boundary

AI-generated artifacts are recommendations, analyses, plans, implementations, verification results, investigations, reviews, Skills, or Agents according to their defined purpose.

AI-generated artifacts do not become human-authorized merely because:

- they are complete,
- they contain no findings,
- tests pass,
- verification passes,
- review passes,
- the repository builds successfully,
- a Skill executes successfully,
- an Agent executes successfully.

Skills and Agents are governed execution artifacts, not sources of human authority.

Human authority must be explicitly exercised where required.

---

## 35. Artifact Change Propagation

When an approved governed artifact changes, downstream impact must be evaluated.

Examples:

### Requirement Change

    Requirement Change
       ↓
    Requirement Analysis
       ↓
    Requirement Analysis Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Requirement Approval
       ↓
    Plan Impact Evaluation
       ↓
    Plan Verification / Approval as Required
       ↓
    Implementation

### Plan Change

    Plan Change
       ↓
    Human Approval
       ↓
    Complete Plan Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Implementation

### Implementation Change

    Implementation Change
       ↓
    Complete Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

---

## 36. Artifact Governance Conflict

If two governed artifacts appear to conflict:

1. Identify the conflicting artifacts.
2. Identify their authority levels.
3. Determine whether the conflict is a requirement, plan, implementation, verification, or process conflict.
4. Do not silently resolve the conflict.
5. Route the conflict through the applicable governed decision process.
6. Obtain required human approval before applying a material change.

AI must not resolve a material governance conflict by silently modifying an approved artifact.

---

## 37. Detailed Governance References

The overall lifecycle is defined by:

`docs/ai/sdlc/SDLC_GOVERNANCE.md`

The complete set of execution guidelines is maintained at:

- `docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`
- `docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md`
- `docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_VERIFICATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md`
- `docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md`
- `docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md`

The corresponding controlled Prompts are maintained under:

`docs/ai/prompts/`

The corresponding execution Requests are maintained under:

`docs/ai/request/`

The reusable SDLC Process Skills are maintained under:

`.github/skills/`

The SDLC Process Agents are maintained under:

`.github/agents/`

The SDLC Governance Control Skill and Governance Control Agents are maintained separately and operate exclusively on the SDLC Governance Framework.

---

## 38. Final Artifact Governance Principle

Every governed artifact must have:

- a defined purpose,
- a defined source of truth,
- a defined authority boundary,
- a defined verification relationship where applicable,
- a defined human approval or acceptance boundary where applicable,
- traceability to its upstream artifacts,
- controlled handling when it changes.

This includes SDLC Process Skills and SDLC Process Agents.

The fundamental rule is:

> An AI-generated artifact may provide analysis, evidence, recommendations, plans, implementation, verification, investigation, review, or governed execution mechanics, but it must never silently acquire human approval or acceptance authority.