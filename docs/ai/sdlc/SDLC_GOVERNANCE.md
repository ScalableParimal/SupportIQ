# SDLC Governance

## 1. Purpose

This document defines the governed AI-assisted Software Development Life Cycle (SDLC) used by this repository.

It establishes:

- the overall development lifecycle,
- the relationship between requirements, analysis, planning, implementation, verification, review, and acceptance,
- the human approval gates,
- the role of AI at each stage,
- the controlled process for handling findings and corrective changes,
- the required sequencing between governed activities,
- the relationship between SDLC lifecycle stages and their governed execution mechanisms.

This document defines the overall lifecycle and governance relationships only.

Detailed normative rules for individual activities are defined by the applicable guideline documents under:

`docs/ai/guidelines/`

Reusable AI execution procedures are defined by the applicable Skills under:

`.github/skills/`

Controlled AI execution entry points are defined by the applicable SDLC Process Agents under:

`.github/agents/`

The Skills and Agents must operate within the authority established by this document and the other master governance documents. They must not redefine lifecycle authority, human approval authority, or governed artifact authority.

---

## 2. Governance Principles

The SDLC follows these principles:

1. The approved Requirement is the business source of truth.
2. The approved Implementation Plan is the implementation source of truth.
3. The actual repository is the technical source of truth for existing implementation.
4. AI may analyse, verify, plan, implement, investigate, and review within the applicable governed process.
5. AI must not claim Human Approval or Human Acceptance.
6. Human decisions and approvals are explicit governance gates.
7. Verification is independent of the activity being verified.
8. Findings must follow the governed Finding Investigation and Corrective Change process.
9. Corrective implementation must always use the current approved Implementation Plan.
10. A task ID, recently changed file, or reported finding must not unnecessarily restrict a complete verification or review.
11. A downstream activity must use the current approved output of the applicable upstream stage.
12. When a governed artifact changes, the applicable downstream verification and approval process must be reconsidered.
13. SDLC Process Skills define reusable AI execution procedures and must not redefine governance authority.
14. SDLC Process Agents provide controlled execution boundaries and must not bypass Skills, governed processes, or human approval and acceptance gates.
15. Skills and Agents are execution mechanisms for the governed lifecycle; they are not additional lifecycle stages or human authority.
16. Implementation work that may overlap across tasks or features is governed by mandatory concurrency controls. Relevant task/feature dependencies, shared change surfaces, and repository/checkout/worktree context must be assessed; an absent dependency declaration does not establish independence or concurrency safety. If relevant information or safety is unknown or unassessed, the affected work must be sequenced or serialized until assessed. Implementation writes in one shared checkout must be serialized and coordinated by one Orchestrator; no second write may be dispatched there while a write is active or exclusive coordination cannot be established. Concurrent implementation writes may proceed only in isolated worktrees and require an explicit integration/reconciliation step before the work is combined and verified. Read-only analysis/planning may overlap only where existing process boundaries and distinct output scopes permit. Applicable Planning, Plan Verification, Implementation, and Orchestrator artifacts define the detailed execution of these controls. This principle does not authorize a lock, reservation, scheduler, persistence/state mechanism, new Skill, Agent, or core artifact.

---

## 3. Governed SDLC Lifecycle

### Fresh-repository governance initialization

A repository that has not yet established its governance persistence root or prospective Master baseline must not be required to produce historical governance records that cannot yet exist. Before the first governance-process invocation, follow the one-time first-use route in `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §30.1 and the publication boundary in `SDLC_ARTIFACT_GOVERNANCE.md` §33.1. The default lightweight evidence route for a GitHub-hosted repository is an attributable authorization comment or review in the canonical repository, validated against the exact repository commit, Master fingerprints, record root, Work ID, actor, and limited initial stage.

The bootstrap authorization permits only the first actor-owned invocation publication and the explicitly authorized complete Governance Audit. It does not authorize remediation or source changes, waive ordinary audit criteria, adopt a product persistence root, or adopt a Master baseline. Findings proceed through the normal governed investigation, decision, approval, application, independent verification, review, and re-audit lifecycle. A separate explicit Human decision must adopt the product persistence root before any product-process record or Portability Assessment. Inherited Master files remain candidate text until the target-repository audit and required assurance pass and a separate Human decision adopts the exact three-file baseline. Governance-root bootstrap/Audit is not product-root or baseline adoption. An interrupted or established repository must be reconciled against its existing records; it must not be declared fresh to bypass missing evidence.


### Portability Assessment entry and reassessment

Before a new target project begins its first SDLC activity under this framework, the Portability Assessment mechanism defined in `SDLC_ARTIFACT_GOVERNANCE.md` §3.4 must complete an assessment against identified source-framework and target-project baselines. The assessment is advisory: it reports evidence, classifications, adaptations, uncertainties, and any recommended possible blocking condition. A human authorized for that project must explicitly decide whether each recommended possible blocking condition applies to that project. The Assessment Agent must neither make that decision nor automatically enforce a block. Record the human decision and rationale with assessment evidence; do not label it Human Requirement Approval or Human Acceptance. Until the human decision about a recommended possible blocker is recorded, the first SDLC activity (or, on reassessment, the next affected SDLC activity) does not start. This decision does not approve a product Requirement or Implementation Plan.

Reassess on an explicit human request and after a material change that can affect prior assessment applicability. Material changes include applicable Master/Governance Assessment artifacts or invocation/approval/traceability rules; target-project requirements or scope; architecture, technology stack, repositories/workspace boundaries or project instructions; integrations, security/access controls, CI/test/deployment/operational context; or other declared assessment inputs. The assessment Guideline defines evidence-based reuse and affected-dimension reassessment. Record changed source/target identity and fingerprints; do not reuse a prior conclusion where its scope, inputs, or applicability changed. Do not create unconditional repeated execution or automatic Agent invocation.

This entry control is part of the existing lifecycle, not a parallel lifecycle. Ordinary lifecycle stages and approval authorities remain unchanged.

The standard lifecycle is:

    Source Requirement
            ↓
    Requirement Analysis
            ↓
    Requirement Analysis Verification
            ↓
    Resolve Verification Findings / Decisions
            ↓
    Human Requirement Approval
            ↓
    Implementation Planning
            ↓
    Implementation Plan Verification
            ↓
    Resolve Plan Verification Findings / Decisions
            ↓
    Human Review Package
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

Each stage must use the current approved output of the applicable upstream stage.

---

## 4. Requirement Stage

### 4.1 Source Requirement

The Requirement defines the business need, expected behavior, scope, constraints, and acceptance expectations.

The Requirement is the authoritative business source of truth.

AI must not silently redefine the Requirement.

### 4.2 Requirement Analysis

Requirement Analysis is performed by AI using the Requirement as its source of truth.

The analysis identifies:

- missing information,
- ambiguities,
- conflicts,
- assumptions,
- business rules,
- scope boundaries,
- dependencies,
- relevant technical impact,
- decisions requiring human input.

Requirement Analysis does not approve the Requirement.

Requirement Analysis does not create an implementation plan.

### 4.3 Requirement Analysis Verification

Requirement Analysis Verification independently verifies the complete current Requirement Analysis and resulting updated Requirement against the source Requirement and applicable decisions.

Verification must consider the complete current artifact, not only recently changed sections.

AI verification does not constitute Human Requirement Approval.

### 4.4 Human Requirement Approval

Human Requirement Approval is the formal business approval gate.

The Requirement must not proceed to implementation planning as an approved Requirement until the required verification findings and decisions have been resolved and the human approval has been obtained.

---

## 5. Implementation Planning Stage

### 5.1 Implementation Planning

Implementation Planning creates the Implementation Plan from:

- the current approved Requirement,
- applicable architecture,
- engineering guidelines,
- repository constraints,
- relevant technical evidence.

The Implementation Plan must not redefine the business Requirement.

### 5.2 Implementation Plan Verification

Implementation Plan Verification independently verifies the complete current Implementation Plan against:

- the current approved Requirement,
- applicable architecture,
- engineering guidelines,
- repository constraints,
- technical feasibility,
- testing and acceptance needs.

The verification must cover the complete current plan.

Task IDs and recently changed tasks are context only and must not restrict complete plan verification.

AI verification does not constitute Human Plan Approval.

### 5.3 Human Review Approval

Human Review Approval is a required manual human gate that occurs after complete Implementation Plan Verification and resolution of all required verification findings and decisions.

Human Review Approval authorizes only progression to separate Human Plan Approval.

It does not approve the plan, authorize implementation, waive unresolved required findings, or replace any Human Approval required before applying a corrective change.

### 5.4 Human Plan Approval

Human Plan Approval is the formal approval gate for the Implementation Plan.

Implementation must use the current approved Implementation Plan.

Implementation must not proceed against an unapproved or superseded plan.

---

## 6. Implementation Stage

### 6.1 Implementation

Implementation is performed against:

- the current approved Requirement,
- the current approved Implementation Plan,
- the actual repository.

Implementation must remain within the approved scope.

If a material conflict or deviation is discovered, implementation must stop at the affected point and follow the governed finding/corrective-change process.

### 6.2 Implementation Self-Check

The Implementation Self-Check is performed after implementation.

It may include:

- build validation,
- automated tests,
- architecture checks,
- traceability checks,
- repository consistency checks,
- diff inspection,
- implementation-specific validation.

Implementation Self-Check is an implementation activity.

It does not replace formal Implementation Verification.

It does not constitute Human Acceptance.

---

## 7. Implementation Verification

Implementation Verification independently verifies the complete current implementation against:

- the current approved Requirement,
- the current approved Implementation Plan,
- applicable architecture,
- engineering guidelines,
- repository constraints,
- available evidence.

Verification must cover the complete current implementation.

Task IDs, recently changed files, findings, and corrective changes are context only and must not unnecessarily restrict verification scope.

Implementation Verification is read-only.

Implementation Verification does not perform corrections.

Implementation Verification does not constitute Human Acceptance.

---

## 8. Implementation Review

Implementation Review evaluates the complete current implementation from a broader engineering and quality perspective.

The review may cover:

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

Implementation Review does not directly apply corrections.

Material findings follow the governed finding and corrective-change process.

Implementation Review does not constitute Human Acceptance.

---

## 9. Human Acceptance

Human Acceptance is the final human gate before the implementation is considered accepted.

Human Acceptance occurs after the applicable:

- Implementation Verification,
- Implementation Review,
- finding resolution,
- corrective implementation,
- re-verification,
- re-review

have been completed.

AI must not claim Human Acceptance.

---

## 10. Commit and Push

Commit and Push occur only after the required Human Acceptance gate has been satisfied.

The committed implementation must correspond to the accepted implementation state.

---

## 11. Finding and Corrective Change Lifecycle

Findings may originate from:

- Requirement Analysis Verification,
- Implementation Plan Verification,
- Implementation Verification,
- Implementation Review,
- testing,
- other governed engineering activities.

The standard corrective path is:

    Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision & Plan Update
       ↓
    Required Human Approval
       ↓
    Apply Approved Change
       ↓
    Required Verification
       ↓
    Required Review
       ↓
    Human Acceptance where applicable

A finding must not be corrected informally outside the applicable governed process when the correction materially affects a governed artifact.

---

## 12. Requirement Change Path

If a finding requires a Requirement change:

    Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision
       ↓
    Requirement Update
       ↓
    Requirement Analysis
       ↓
    Complete Requirement Analysis Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Requirement Approval
       ↓
    Plan Evaluation
       ↓
    Implementation Planning / Plan Update as Required
       ↓
    Implementation Plan Verification as Required
       ↓
    Resolve Findings / Decisions as Required
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Implementation

A Requirement change must not be introduced directly through implementation.

---

## 13. Implementation Plan Change Path

If a finding requires an Implementation Plan change:

    Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision
       ↓
    Proposed Plan Update
       ↓
    Required Human Approval
       ↓
    Apply Approved Plan Update
       ↓
    Complete Implementation Plan Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Implementation

Implementation must always use the current approved Implementation Plan.

---

## 14. Implementation Finding Path

If Implementation Verification or Implementation Review identifies a material implementation finding:

    Implementation Finding
            ↓
    Finding Investigation
            ↓
    Corrective Change Decision & Plan Update
            ↓
    Human Approval where required
            ↓
    Update Requirement / Plan where required
            ↓
    Implement Corrective Change
            ↓
    Complete Implementation Verification
            ↓
    Implementation Review
            ↓
    Human Acceptance

The corrective implementation must not bypass the applicable approval or verification gates.

---

## 15. No Direct Corrective Implementation from a Finding

The following shortcut is not permitted:

    Finding
       ↓
    Direct Code Change

The governed path must be used:

    Finding
       ↓
    Investigation
       ↓
    Corrective Decision
       ↓
    Required Approval
       ↓
    Implementation
       ↓
    Verification
       ↓
    Review

---

## 16. Current Approved Artifact Principle

At every downstream stage, use the latest approved version of the applicable upstream artifact.

Examples:

    Source / Updated Requirement
            ↓
    Requirement Analysis

    Current Approved Requirement
            ↓
    Implementation Planning

    Current Approved Requirement
            +
    Current Approved Implementation Plan
            ↓
    Implementation

If an upstream artifact changes, downstream artifacts must be evaluated for impact.

No downstream process may continue using a superseded artifact as though it were current.

---

## 17. Verification and Approval Separation

The following distinctions are mandatory:

| Activity | Meaning |
|---|---|
| Requirement Analysis | AI analysis of the requirement |
| Requirement Analysis Verification | Independent AI verification |
| Human Requirement Approval | Human business approval |
| Implementation Planning | AI creation of implementation plan |
| Implementation Plan Verification | Independent AI verification |
| Human Review Approval | Required manual human gate authorizing only progression to Human Plan Approval; not plan approval or implementation authority |
| Human Plan Approval | Human approval of implementation plan |
| Implementation Self-Check | AI implementation-level validation |
| Implementation Verification | Independent AI verification of complete implementation |
| Implementation Review | Independent engineering/quality review |
| Human Acceptance | Human acceptance of implementation |

AI must not treat one activity as another.

---

## 18. AI Authority Boundary

AI may:

- analyse,
- identify issues,
- ask questions,
- recommend decisions,
- create plans,
- implement approved work,
- verify,
- investigate findings,
- recommend corrective actions,
- review implementations.

AI must not:

- silently change an approved Requirement,
- silently change an approved Implementation Plan,
- make an unresolved human business decision,
- claim Human Requirement Approval,
- claim Human Plan Approval,
- claim Human Acceptance,
- bypass required verification,
- bypass required corrective-change governance.

---

## 19. Scope Principle

A request may identify:

- task IDs,
- changed files,
- components,
- findings,
- implementation slices,
- specific verification objectives.

These are execution context unless the applicable governed process explicitly defines them as the complete scope.

For complete verification and review activities:

> Task IDs and recently changed artifacts are context, not a substitute for complete-scope verification or review.

---

## 20. Read-Only Governance Activities

The following activities must not directly modify governed artifacts:

- Requirement Analysis Verification
- Implementation Plan Verification
- Implementation Verification
- Implementation Review
- Finding Investigation
- Corrective Change Decision & Plan Update

These activities may recommend changes and route findings, but the applicable governed change process must be used to apply them.

---

## 21. Standard Human Approval Gates

The standard human gates are:

### Gate 1 — Human Requirement Approval

Occurs after:

    Requirement
    → Requirement Analysis
    → Requirement Analysis Verification
    → Finding / Decision Resolution

### Gate 2 — Human Review Approval

Occurs after:

    Approved Requirement
    → Implementation Planning
    → Implementation Plan Verification
    → Finding / Decision Resolution
    → Human Review Package

Authorizes only progression to Human Plan Approval.

### Gate 3 — Human Plan Approval

Occurs after:

    Approved Requirement
    → Implementation Planning
    → Implementation Plan Verification
    → Finding / Decision Resolution
    → Human Review Approval

### Gate 4 — Human Acceptance

Occurs after:

    Implementation
    → Implementation Self-Check
    → Implementation Verification
    → Implementation Review
    → Finding / Corrective Resolution where required

Only the human can satisfy these gates.

---

## 22. Standard Lifecycle Status

The governed lifecycle may use the following conceptual statuses:

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

AI-generated verification statuses must not be represented as Human Approval or Human Acceptance.

Execution position must distinguish the governed process, its invocation attempt, attempt progress or termination, the process outcome, and any pending human gate. Starting a process does not establish its completion. Completing an attempt does not establish a successful outcome or authorize progression.

Durable execution recording and recovery must follow section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. Execution metadata does not introduce a lifecycle stage or replace an existing artifact, verification result, approval, or acceptance decision.

---

## 23. Required Traceability

The lifecycle must maintain traceability between:

    Requirement
       ↓
    Requirement Analysis
       ↓
    Approved Requirement
       ↓
    Implementation Plan
       ↓
    Approved Implementation Plan
       ↓
    Implementation
       ↓
    Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

Where findings occur, traceability must additionally capture:

    Finding
       ↓
    Investigation
       ↓
    Corrective Decision
       ↓
    Affected Artifact
       ↓
    Approved Change
       ↓
    Re-verification
       ↓
    Re-review

---

## 24. Detailed Governance Documents

The detailed governance rules for each governed activity are maintained separately.

The complete set of guideline documents is:

- `docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`
- `docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md`
- `docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_VERIFICATION_GUIDELINES.md`
- `docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md`
- `docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md`
- `docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md`

The corresponding prompts are maintained under:

`docs/ai/prompts/`

The corresponding request templates are maintained under:

`docs/ai/request/`

The reusable SDLC Process Skills are maintained under:

`.github/skills/`

The controlled SDLC Process Agents are maintained under:

`.github/agents/`

The Skills provide reusable execution procedures for the governed processes. The Agents provide controlled execution boundaries for those procedures.

This document defines the lifecycle relationship between these governance artifacts; the individual Guidelines, Prompts, Requests, Skills, and Agents define their respective responsibilities within the authority established by the master governance documents.

Governance Control Skills and Agents used to audit or remediate the SDLC governance framework are separate from the normal SDLC Process Skills and Agents.

### Separately Reported Portability Assessment Mechanism

This mechanism is outside—not an addition to—the 52-core catalog:
- Guideline: `docs/ai/guidelines/PORTABILITY_ASSESSMENT_GUIDELINES.md`
- Prompt: `docs/ai/prompts/PORTABILITY_ASSESSMENT_PROMPT.md`
- Request: `docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md`
- Skill: `.github/skills/portability-assessment/SKILL.md`
- Agent/entry point: `.github/agents/portability-assessment.agent.md`

These references connect the entry point to its governing procedure and invocation inputs. The separate mechanism is governed by section 3.4 of `SDLC_ARTIFACT_GOVERNANCE.md`; the fixed 52-core counts above are unchanged.

---

### First-use governance bootstrap

The operational first-use authorization, record-publication, Work ID reservation, recovery, and evidence requirements are defined by `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §30.1 and `SDLC_ARTIFACT_GOVERNANCE.md` §33.1. These requirements establish only the permitted first invocation and do not replace the ordinary Human gates or the separate prospective Master-baseline adoption required by section 42 of the traceability document.

### Governance Amendment Assurance Mechanisms

Governance Amendment Application, Independent Governance Verification, and Independent Governance Review are three separately reported mechanisms under the same three Master Governance documents. Each has its own Guideline, Prompt, Request, Skill, and Agent under `docs/ai/` and `.github/`. They are outside, and do not change, the 52-core catalog.

The Application bundle is `docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md`, `docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md`, `docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md`, `.github/skills/governance-amendment-application/SKILL.md`, and `.github/agents/governance-amendment-application.agent.md`. The Verification bundle is `docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md`, `docs/ai/prompts/INDEPENDENT_GOVERNANCE_VERIFICATION_PROMPT.md`, `docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md`, `.github/skills/independent-governance-verification/SKILL.md`, and `.github/agents/independent-governance-verification.agent.md`. The Review bundle is `docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md`, `docs/ai/prompts/INDEPENDENT_GOVERNANCE_REVIEW_PROMPT.md`, `docs/ai/request/INDEPENDENT_GOVERNANCE_REVIEW_REQUEST.md`, `.github/skills/independent-governance-review/SKILL.md`, and `.github/agents/independent-governance-review.agent.md`.

Application may apply only the exact governance change explicitly approved for the exact target paths and base/expected-after SHA-256 fingerprints. A Human Approval must identify the application actor and route; the first application that establishes this role requires a separately designated qualified one-time actor. The Application Agent creates durable per-target before/after evidence and stops on any mismatch or partial failure.

Verification and Review are read-only, independent of one another and of proposal preparation and application. Each produces its own evidence-bound result. Neither result is Human Approval. Governance changes are effective only after explicit approval, authorized exact application, passing independent Verification, passing independent Review, and the full Audit's `CONSISTENT` result with every required finding/count zero and every mechanism group assessed without unresolved issues. A change to a Master additionally requires a separate prospective-baseline adoption decision after those gates; a non-Master change does not require Master-baseline adoption.

---

## 25. Governance Conflict Rule

If this document conflicts with a detailed guideline, the conflict must be identified and resolved through the governed document-maintenance process.

AI must not silently choose one interpretation and modify the other document.

Until the conflict is resolved, the affected process must be treated as requiring human decision.

---

## 26. Final Governance Principle

The governed SDLC follows this fundamental sequence:

> AI analyses and prepares.  
> AI independently verifies.  
> Human decides and approves.  
> AI implements.  
> AI independently verifies the complete implementation.  
> AI reviews.  
> Human accepts.

For findings:

> Finding → Investigation → Corrective Decision → Required Human Approval → Approved Change → Complete Verification → Review → Human Acceptance.

No stage may silently bypass the applicable verification, approval, or acceptance gate.