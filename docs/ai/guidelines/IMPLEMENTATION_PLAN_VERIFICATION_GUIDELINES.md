# Implementation Plan Verification Guidelines

## 1. Purpose

This guideline defines the process for independently verifying an implementation plan before Human Plan Approval.

Implementation Plan Verification determines whether the complete current candidate Implementation Plan is sufficiently:

- complete
- traceable
- internally consistent
- architecturally aligned
- technically feasible
- testable
- appropriately scoped
- implementable against the approved requirement

The purpose is to identify gaps, ambiguities, missing decisions, conflicts, risks, and required plan changes before implementation begins.

This process does NOT implement the feature.

This process does NOT grant Human Plan Approval.

---

## 2. Core Principle

Implementation Planning creates the proposed way to implement the approved requirement.

Implementation Plan Verification independently evaluates that plan before implementation begins.

The verification question is:

> Does the complete current candidate Implementation Plan provide a sufficiently complete, consistent, traceable, feasible, and testable path to implement the complete current approved requirement within the approved architecture and scope?

The plan must be evaluated as a complete plan.

Do not verify only:

- the first few tasks
- recently changed tasks
- individual task descriptions
- one technical area
- one project/layer

Review the relationships and dependencies between the complete set of planned tasks.

---

## 3. Current-State Verification

Implementation Plan Verification always uses:

1. Current approved Requirement
2. Current candidate Implementation Plan under verification
3. Current applicable architecture
4. Current engineering guidelines
5. Current repository structure and conventions where relevant
6. Explicit decisions already approved by the human
7. Additional evidence supplied for verification
8. Previously approved Implementation Plan, if one exists, as a baseline/comparator only

If the implementation plan has been updated, verify the complete current plan again.

Do not compare only the changed portion of the plan.

The verification target is always:

Current Approved Requirement
+
Current Complete Candidate Implementation Plan under verification
+
Current Applicable Architecture / Engineering Constraints

A previously approved Implementation Plan, if supplied, is a baseline/comparator and is distinct from the candidate Implementation Plan under verification.

---

## 4. Source of Truth

Use the following priority:

1. Current approved Requirement
2. Current approved Architecture / Engineering Constraints
3. Current candidate Implementation Plan under verification (the object of evaluation, not an approved source of truth)
4. Repository conventions and existing implementation
5. Supporting documentation
6. Additional supplied evidence

The requirement defines WHAT must be implemented.

The candidate Implementation Plan under verification defines HOW the approved requirement is currently proposed to be implemented. A previously approved Plan, if applicable, is a baseline/comparator and is not the verification target.

Architecture and engineering constraints define boundaries within which the plan must operate.

A plan must not silently change the requirement.

---

## 5. Scope

Review the complete implementation plan, including where applicable:

- task breakdown
- task dependencies
- implementation sequence
- architecture
- layer responsibilities
- interfaces and contracts
- data model
- API contracts
- validation
- error handling
- persistence
- configuration
- testing
- deployment/infrastructure
- acceptance criteria
- exclusions
- assumptions
- technical decisions
- external dependencies
- operational considerations

Review only areas relevant to the approved scope.

Do not introduce requirements that are outside the approved requirement or applicable engineering constraints.

---

## 6. Verification Areas

### 6.1 Requirement Traceability

Determine whether every approved requirement is represented in the implementation plan.

Check for:

- missing requirements
- partially covered requirements
- ambiguous coverage
- duplicated coverage
- contradictory tasks
- unnecessary implementation work

Each significant requirement should be traceable to one or more implementation tasks.

Example:

Requirement R001
    ↓
T001
T003
T006

Requirement R002
    ↓
T004
T005

Identify requirements without sufficient implementation coverage.

---

### 6.2 Scope Alignment

Verify that the plan:

- implements the approved scope
- does not silently expand scope
- respects explicit exclusions
- does not introduce unrelated functionality
- does not omit approved functionality

Identify both:

- scope gaps
- scope creep

---

### 6.3 Architecture Alignment

Verify that the proposed implementation respects the approved architecture.

Review:

- project dependencies
- layer responsibilities
- dependency direction
- interface ownership
- domain independence
- application responsibilities
- infrastructure responsibilities
- API responsibilities
- frontend/backend boundaries
- prohibited dependencies

For example, if the approved architecture requires:

API
→ Application
→ Domain

Infrastructure
→ Application
→ Domain

then the plan must not introduce an unapproved dependency such as:

API
→ Infrastructure

unless that architectural decision has been explicitly approved.

---

### 6.4 Task Completeness

Determine whether the task breakdown contains sufficient work to implement the approved requirement.

Consider whether the plan has appropriately covered:

- domain model
- business rules
- application/use cases
- contracts/DTOs
- persistence abstractions
- infrastructure implementation
- API endpoints
- frontend behavior
- validation
- error handling
- tests
- configuration
- migrations
- integration concerns

Do not require every category for every feature.

Determine applicability from the requirement and architecture.

---

### 6.5 Task Dependencies

Verify that task dependencies are logically correct.

Check for:

- missing prerequisites
- circular dependencies
- incorrect implementation sequence
- tasks depending on artifacts that do not yet exist
- tasks that should be split because of dependency boundaries

Example:

Domain contract
    ↓
Application abstraction
    ↓
Infrastructure implementation
    ↓
API integration

The plan should reflect dependencies such as these where applicable.

Verify that relevant cross-feature dependencies and shared change surfaces are assessed, including files/components, APIs/contracts, schemas/migrations, configuration, and integration dependencies. Verify that the plan records an explicit execution mode and that it follows the governing concurrency rule: implementation writes in one shared checkout are serialized by one Orchestrator; parallel implementation requires isolated worktrees and explicit integration/reconciliation before combined verification. Absence of a declared dependency does not establish concurrency safety. Where relevant information is unknown or unassessed, require sequencing/serialization until assessed.

---

### 6.6 Technical Feasibility

Evaluate whether the proposed approach is technically feasible within:

- selected technology
- framework versions
- repository architecture
- known infrastructure
- database capabilities
- external dependencies
- environment constraints
- stated operational constraints

Identify assumptions that require validation.

Do not present uncertain technical assumptions as facts.

---

### 6.7 API and Contract Completeness

Where APIs or other contracts are involved, verify that the plan sufficiently defines:

- operations
- request contracts
- response contracts
- validation
- status/error behavior
- pagination/filtering behavior
- compatibility considerations
- relevant edge cases

The level of detail should be sufficient for implementation without requiring significant unstated decisions.

---

### 6.8 Data and Persistence Design

Where persistence is involved, verify:

- entities
- relationships
- constraints
- indexes justified by requirements/query behavior
- migrations
- repository/persistence responsibilities
- data validation
- uniqueness requirements
- transaction considerations where applicable
- test database/integration-test requirements

Do not introduce database structures without requirement or technical justification.

---

### 6.9 Validation and Error Handling

Verify that the plan identifies:

- applicable validation rules
- ownership of validation
- expected error conditions
- error propagation
- conflict behavior
- not-found behavior
- API error mapping where applicable

Do not duplicate domain rules unnecessarily across layers.

---

### 6.10 Testing Strategy

Verify that the plan provides an appropriate testing strategy.

Consider:

- unit tests
- application/service tests
- infrastructure/integration tests
- API tests
- frontend tests
- end-to-end tests

Verify coverage for:

- normal behavior
- validation
- errors
- boundaries
- important edge cases
- integration behavior
- regression risks

Do not judge test quality solely by test count.

---

### 6.11 Acceptance Criteria

Every significant implementation task should have sufficiently clear completion criteria.

Acceptance criteria should be:

- observable
- testable
- unambiguous
- traceable to the requirement

Avoid vague criteria such as:

"Implement customer functionality."

Prefer criteria that describe observable behavior.

---

### 6.12 Decisions and Ambiguities

Identify decisions that must be made before implementation.

Examples:

- identifier type
- uniqueness semantics
- API response contract
- error contract
- persistence strategy
- integration approach
- configuration strategy
- compatibility behavior

For each unresolved decision, identify:

- decision required
- why it matters
- affected tasks
- available options if known
- consequence of delaying the decision

Do not silently choose a material design decision on behalf of the human.

---

### 6.13 Assumptions and Dependencies

Identify:

- assumptions
- external dependencies
- infrastructure prerequisites
- configuration prerequisites
- unavailable information
- required environment setup

Distinguish confirmed facts from assumptions.

---

### 6.14 Implementation Sequence

Review whether the proposed sequence is practical.

The sequence should allow developers or AI agents to implement tasks without repeatedly blocking on missing contracts, infrastructure, or decisions.

Identify sequencing problems where applicable.

---

## 7. Finding Classification

Classify identified issues as:

### Plan Defect

The plan is incomplete, inconsistent, technically incorrect, or otherwise unsuitable for implementation.

### Requirement Coverage Gap

An approved requirement is not adequately represented in the plan.

### Architecture Conflict

The plan conflicts with the approved architecture or engineering constraints.

### Missing Decision

A material decision is required before implementation can proceed safely.

### Missing Evidence

The plan depends on information that has not yet been established.

### Scope Issue

The plan omits approved scope or introduces unapproved scope.

### Testability Gap

The plan does not provide sufficient means to verify the required behavior.

### Dependency / Sequencing Issue

Task dependencies or implementation order are incorrect or incomplete.

### Technical Risk

The plan is implementable but contains a material technical risk that should be explicitly considered.

### Informational Observation

A useful observation that does not require a plan change.

---

## 8. Severity

Use:

### Critical

The plan cannot safely proceed without resolution.

### High

A significant issue that should normally be resolved before Human Plan Approval.

### Medium

A meaningful issue that may require clarification or plan adjustment.

### Low

A minor issue that does not normally block plan approval.

### Informational

Observation or improvement suggestion.

Severity must be based on impact, not personal preference.

---

## 9. Human Decision Requirements

AI should identify when human decision-making is required.

Human decision is normally required when the plan contains unresolved material decisions involving:

- requirement interpretation
- scope
- architecture
- API contract
- database/data model
- security
- external integrations
- compatibility
- production behavior
- infrastructure
- material performance strategy
- other significant design choices

AI may analyze options and consequences.

AI must not represent its recommendation as an approved decision.

---

## 10. Recommended Plan Changes

When changes are required, provide precise recommendations.

For each recommended change include:

- affected task
- current issue
- proposed change
- reason
- requirement/architecture basis
- dependency impact
- testing impact
- acceptance-criteria impact

Implementation Plan Verification is read-only. Do not modify the Implementation Plan during verification. If a Plan Update is required, identify and recommend it, then route it through the separate Implementation Planning / Corrective Change Decision & Plan Update process. Invoking or requesting a Plan Update does not authorize modification during verification.

---

## 11. Read-Only Boundary

Implementation Plan Verification is read-only.

Do not:

- modify source code
- modify tests
- implement tasks
- modify the requirement
- silently modify the implementation plan
- create migrations
- change architecture
- approve decisions
- apply corrective changes

The output is a verification report and, where necessary, recommended plan changes.

Actual plan modification belongs to the Implementation Planning / Corrective Change Decision & Plan Update process.

If a material finding requires a plan change, route the finding through the Finding Investigation and Corrective Change Decision & Plan Update processes.
---

## 12. Evidence Classification

Classify evidence as:

### Executed Evidence

Evidence produced by executing a command or analysis during the current verification.

Examples:

- build or test output
- static-analysis output
- dependency-analysis tool output

Reading or inspecting repository files, repository structure, source code, configuration, documentation, or dependency manifests is Source Inspection Evidence, even when performed during verification.

### Source Inspection Evidence

Evidence obtained by inspecting:

- requirement
- implementation plan
- architecture documentation
- repository structure
- existing code
- configuration and dependency manifests

### Reported Evidence

Evidence supplied by the user or another process.

### Unverified

Information that has not been independently confirmed.

Do not present reported or unverified information as independently verified evidence.

Classify each evidence item according to how it was obtained. If both source inspection and tool execution contribute evidence, classify the resulting items separately.

---

## 13. Uncertainty

If information is incomplete or conflicting:

- identify the uncertainty
- explain its impact
- do not silently resolve it
- request clarification or evidence where necessary

Do not invent requirements, architectural decisions, technical capabilities, or human approvals.

---

## 14. Verification Outcome

Use one of the following:

### PLAN VERIFIED

The complete current plan is sufficiently complete, consistent, traceable, feasible, and testable.

No material blocking gaps were identified.

### PLAN VERIFIED WITH GAPS

The plan is generally implementable, but non-blocking gaps or observations exist.

### CHANGES REQUIRED

One or more material plan issues must be resolved before Human Plan Approval.

### DECISION REQUIRED

One or more material human decisions are required before the plan can be approved.

### EVIDENCE REQUIRED

Verification cannot be completed reliably because required evidence is missing.

### CANNOT VERIFY

The available information is insufficient to perform meaningful verification.

---

## 15. Required Verification Report

The report must contain:

### 1. Verification Status

One of the defined outcomes.

### 2. Scope Verified

Identify:

- feature
- requirement
- complete current candidate Implementation Plan under verification
- applicable architecture
- applicable engineering constraints

Task IDs or recently changed tasks may be identified as verification context, but they must not limit the verification scope.

### 3. Requirement Traceability

Summarize coverage and identify gaps.

### 4. Architecture Verification

Summarize architecture alignment and conflicts.

### 5. Task and Dependency Verification

Identify completeness, dependencies, and sequencing issues.

### 6. Technical Feasibility

Identify feasibility concerns and assumptions.

### 7. API / Data / Validation / Error Handling Review

Cover applicable areas.

### 8. Testing Strategy Review

Identify coverage and testability gaps.

### 9. Decisions Required

List material unresolved decisions.

### 10. Findings

For each finding:

- classification
- severity
- affected task
- evidence
- impact
- confidence
- recommended action

### 11. Recommended Plan Changes

Provide precise changes where applicable.

### 12. Evidence Classification

Identify the evidence used.

### 13. Uncertainty

Identify unresolved uncertainty.

### 14. Human Review Approval Readiness

State:

- READY FOR HUMAN REVIEW APPROVAL
- NOT READY FOR HUMAN REVIEW APPROVAL

READY requires complete verification of the current plan and resolution of all required findings and decisions.

This is a readiness assessment only.

It is NOT Human Review Approval and NOT Human Plan Approval.

The report must bind its result to the exact candidate Plan and current approved Requirement references using the common execution contract. Task and dependency verification must check unique task identifiers, observable completion criteria, resolvable prerequisites, and any required source-to-target task-impact mapping. Identify the exact outstanding findings, decisions, evidence, or human gate that prevent the next process. These checks do not approve the candidate Plan or narrow complete-Plan verification.

### 15. Recommended Next Process

Normally:

- Human Review package and Human Review Approval, followed by separate Human Plan Approval
- Implementation Planning / Plan Update
- Finding Investigation
- Corrective Change Decision & Plan Update
- Additional Evidence Collection

---

## 16. Verification Discipline

The verifier must:

- verify the complete current plan
- preserve requirement traceability
- respect approved architecture
- distinguish facts from assumptions
- identify material gaps
- avoid speculative requirements
- avoid unnecessary plan complexity
- avoid implementing changes
- avoid silently making human decisions
- preserve scope boundaries

The objective is to determine whether the plan is sufficiently ready for Human Plan Approval and implementation.

---

## 17. Critical Rule

Implementation must not begin merely because an implementation plan exists.

The expected sequence is:

Requirement Approval
→ Implementation Planning
→ Implementation Plan Verification
→ Resolve Findings / Decisions
→ Human Review Approval
→ Human Plan Approval
→ Implementation

If the plan changes materially after verification:

Updated Plan → Complete Implementation Plan Verification → Resolve Findings / Decisions → If a finding or decision requires a plan change, route it through Corrective Change Decision & Plan Update, obtain required human approval, apply only the approved plan update, then repeat Complete Implementation Plan Verification → Resolve Findings / Decisions. When verification is complete and no findings or decisions remain unresolved → Human Review Approval → Human Plan Approval → Implementation. Human approval required before applying any corrective plan change remains separate and is not replaced by Human Review Approval.