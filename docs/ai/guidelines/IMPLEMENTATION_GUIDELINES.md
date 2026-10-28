# Implementation Guidelines

## 1. Purpose

These guidelines define the standard process for implementing an approved implementation plan using AI assistance.

The purpose is to ensure that AI implementation remains:
- traceable to the approved requirement,
- aligned with the approved implementation plan,
- consistent with the existing repository architecture,
- limited to approved scope,
- testable and verifiable,
- subject to human approval at defined gates.

These guidelines govern implementation execution. They do not redefine business requirements or create the implementation plan.

---

## 2. Required Inputs

Before implementation begins, the following must be available:

1. Approved requirement document.
2. Approved implementation plan.
3. Any explicitly approved technical decisions or constraints.
4. The actual repository and its current state.

If any required input is missing or its approval status is unclear, do not assume approval.

---

## 3. Source of Truth and Decision Authority

Use the following order of authority:

1. Approved requirement.
2. Approved implementation plan.
3. Explicitly approved technical decisions or constraints.
4. Existing repository architecture, conventions, and patterns.
5. AI recommendations.

AI recommendations must never silently override an approved requirement, approved plan, or explicit human decision.

If sources conflict, stop at the affected point and request a human decision when the conflict cannot be resolved from the approved sources.

The implementation phase must not redefine the requirement or implementation plan.

Any material change required to the approved requirement or implementation plan must go through the applicable governed change process before implementation continues.

---

## 4. Implementation Scope

Implement only the tasks or implementation slice explicitly requested by the user.

Do not:
- implement future plan tasks,
- add helpful but unapproved features,
- expand the data model without approval,
- introduce new frameworks or libraries without justification and approval where required,
- refactor unrelated code,
- change existing behavior unrelated to the requested slice.

A task may require small supporting changes in dependent code. Such changes are allowed only when they are necessary to complete the requested task and remain within the approved scope.

---

## 5. Implementation Slice

For non-trivial features, implementation should be executed in small, coherent slices.

A slice should normally contain:
- a logical group of plan tasks,
- the required implementation changes,
- related tests,
- verification of the resulting behavior.

Example:

```text
Implementation Plan
    ↓
T005–T007  → Domain slice
T008–T012  → Application slice
T013–T021  → Infrastructure slice
T022–T027  → API slice
T028–T034  → Frontend slice
```

Do not automatically implement the entire plan when a smaller slice has been requested.

---

## 6. Repository Inspection Before Coding

Before modifying code, inspect the relevant repository areas.

At minimum, determine:
- solution/project structure,
- project references and dependency direction,
- existing patterns in the affected layer,
- existing interfaces and abstractions,
- existing test structure,
- configuration conventions,
- database/data-access conventions where relevant,
- build and test commands,
- related existing features.

Do not invent repository conventions when the repository can be inspected.

---

## 7. Architecture and Layer Boundaries

Implementation must preserve the approved architecture and dependency direction.

For example, if the approved architecture is:

```text
API → Application → Domain
Infrastructure → Application → Domain
```

then implementation must not introduce prohibited dependencies such as:

```text
API → Infrastructure
Application → Infrastructure
Domain → Application
Domain → Infrastructure
```

unless the architecture is explicitly changed and approved.

Do not introduce additional architectural layers, patterns, frameworks, or abstractions merely because they are familiar or convenient.

---

## 8. Implement Against the Approved Plan

For every requested plan task:

1. Identify the requirement(s) covered by the task.
2. Identify the intended project/layer.
3. Inspect the existing code.
4. Implement the smallest appropriate change.
5. Add or update the relevant tests.
6. Verify the task.
7. Record the result.

The implementation must remain traceable:

```text
Requirement
    ↓
Business Rule / Contract
    ↓
Implementation Plan Task
    ↓
Code Change
    ↓
Test
    ↓
Verification Evidence
```

Before implementation writes begin, establish the execution mode specified by the current approved Plan and the current Orchestrator coordination. Only one implementation write may be active in a shared checkout, coordinated by one Orchestrator. Do not begin or continue a write when another writer may be modifying that checkout or exclusive Orchestrator coordination cannot be established. Concurrent implementation is permitted only in isolated worktrees when the approved Plan identifies the assessed concurrency and explicit integration/reconciliation step. Reconcile/integrate the work before treating it as combined or starting verification against the combined result. If relevant dependencies, shared surfaces, or checkout state are unknown, stop and sequence/serialize until they are assessed. An unplanned material conflict continues through the existing Finding → Investigation → Corrective Change process.

---

## 9. Business Rules and Domain Behavior

Business rules must be implemented in the layer defined by the approved architecture.

Do not duplicate business rules across layers unless duplication is explicitly required for a separate concern such as input validation or persistence enforcement.

If the approved plan assigns a rule to the Domain layer, do not move it into API or Infrastructure for convenience.

---

## 10. Contracts and Interfaces

Respect approved ownership of contracts and abstractions.

For example, if the approved plan states that an application-owned persistence abstraction is required, do not move that abstraction into Infrastructure.

Interfaces should remain in the layer that owns the corresponding abstraction according to the approved architecture and plan.

Do not create generic abstractions solely to reduce the number of concrete interfaces.

---

## 11. Tests Are Part of Implementation

Implementation is incomplete without appropriate verification.

Depending on the task, tests may include:
- unit tests,
- integration tests,
- API/endpoint tests,
- database tests,
- frontend/component tests,
- end-to-end tests.

Tests should verify behavior and important boundaries, not merely increase coverage numbers.

When an existing test suite is available:
- run relevant tests after changes,
- add tests for new behavior,
- update tests only when approved behavior has intentionally changed.

Do not weaken or delete meaningful tests merely to make the implementation pass.

---

## 12. Verification Gate

After each implementation slice, perform the implementation checks appropriate to the changed code.

Typical implementation checks include:

```text
Build
  ↓
Relevant tests
  ↓
Full test suite where practical
  ↓
Architecture/dependency check
  ↓
Requirement traceability check
  ↓
Implementation-plan traceability check
  ↓
Diff review
```
Use the repository's actual build and test commands.

Do not report implementation verification success based only on code inspection if automated verification can be executed.

These implementation checks are part of implementation execution and do not replace the separate Implementation Verification process.

The complete current implementation must subsequently be evaluated by the formal Implementation Verification process against the complete current approved requirement and approved implementation plan.

Do not treat implementation checks, AI self-checks, or implementation reports as human approval.
---

## 13. Handling Failures

When tests or builds fail:

1. Identify the failure.
2. Determine whether it is caused by the current change.
3. Fix the implementation if the fix is within the approved scope.
4. Re-run the affected verification.
5. Report remaining failures honestly.

Do not:
- hide failures,
- skip failing tests without justification,
- change tests only to remove evidence of a defect,
- claim completion when required verification has not passed.

---

## 14. Handling Plan or Requirement Deviations

During implementation, AI may discover that:

- the requirement is ambiguous,
- the implementation plan is incomplete,
- the repository conflicts with the plan,
- a technical dependency was missed,
- an approved architectural decision is insufficient.

Do not silently resolve a material deviation.

Instead report:

```text
Deviation detected
    ↓
What was planned
    ↓
What was discovered
    ↓
Why it matters
    ↓
Impact
    ↓
Decision required
```

If the deviation requires changing the requirement or approved implementation plan, pause the affected work until the applicable governed change process is completed and the required human decision is made.

Do not modify the requirement or approved implementation plan informally during implementation.

---

## 15. Plan Updates During Implementation

The implementation plan is not to be silently rewritten during coding.

If a plan change becomes necessary:

1. Stop at the affected task.
2. Explain the reason and impact.
3. Identify whether the requirement or implementation plan is affected.
4. Route the finding through the applicable governed corrective-change process.
5. Obtain the required human decision and the specific Human Approval required before applying the corrective plan change.
6. Apply the approved plan update through the governed process.
7. Complete Implementation Plan Verification again.
8. Resolve all required findings and decisions.
9. Obtain Human Review Approval, which authorizes only progression to Human Plan Approval.
10. Obtain separate Human Plan Approval.
11. Resume implementation using the current approved plan.

This preserves:

```text
Approved Requirement
        ↓
Approved Implementation Plan
        ↓
Implementation
```

rather than allowing implementation to redefine the requirement or plan.
---

## 16. Configuration and Secrets

Follow repository configuration conventions.

Do not:
- hardcode credentials,
- commit secrets,
- embed environment-specific connection strings,
- expose sensitive configuration in source code,
- introduce configuration mechanisms unrelated to the repository's established approach.

If required configuration is missing, identify it explicitly rather than inventing secrets or environment values.

---

## 17. Code Quality and Maintainability

Implementation should:
- follow existing repository coding conventions,
- use clear names,
- keep responsibilities focused,
- avoid unnecessary duplication,
- avoid speculative abstractions,
- preserve readability,
- use asynchronous patterns consistently where the existing architecture requires them,
- avoid unrelated refactoring.

Prefer the smallest maintainable change that satisfies the approved requirement and plan.

---

## 18. Review Before Completion

Before declaring an implementation slice complete, review:

### Requirement
- Is every requested behavior implemented?
- Were any requirements unintentionally changed?

### Plan
- Are all requested tasks implemented?
- Were any tasks skipped?
- Were any unapproved tasks added?

### Architecture
- Are dependency directions preserved?
- Were layer boundaries preserved?
- Were unnecessary abstractions introduced?

### Tests
- Are relevant tests present?
- Are tests passing?
- Are important edge cases covered?

### Repository
- Are only relevant files changed?
- Are there generated files or accidental changes?
- Is configuration safe?

### Verification
- Does the solution build?
- Do required tests pass?
- Are remaining failures documented?

---

## 19. Completion Status

Use explicit status rather than a generic “done”.

Recommended implementation statuses:

- `Not Started`
- `In Progress`
- `Blocked`
- `Implemented – Implementation Verification Pending`
- `Implemented – Implementation Verification Passed`
- `Implementation Verification Required`
- `Implementation Review Required`
- `Human Acceptance Pending`
- `Accepted`

AI must not mark the implementation as human-approved or accepted.

Implementation Verification, Implementation Review, and Human Acceptance are separate controlled stages and must not be represented by a single implementation status.

---

## 20. Implementation Report

After each implementation slice, report at minimum:

```text
Implementation Slice:
Tasks:
Requirement Traceability:
Files/Projects Changed:
Tests Added/Updated:
Verification Performed:
Build Result:
Test Result:
Architecture Check:
Plan Deviations:
Open Issues:
Completion Status:
```

Keep the report factual and concise.

Bind the report to the exact approved Requirement, approved Plan, and identifiable repository state under the common execution contract. For each requested task, record implemented, partial, not-started, or blocked work, the criteria addressed, implementation and self-check evidence, remaining work, and dependencies or findings preventing continuation.

Publish checkpoints at meaningful safe boundaries when execution remains incomplete. Record partial repository effects and failed checks without claiming task completion. Before resuming after interruption or source change, reconcile those effects and the applicable task-impact dispositions; continue only against the current approved sources.

Formal verification, review, and Human Acceptance remain separate. Implementation reports and checkpoints must not assert those outcomes on the implementation actor's own authority.

---

## 21. Human Approval Gates

Human approval is required at the defined decision and acceptance points.

The implementation lifecycle is:

```text
Approved Requirement
        ↓
Approved Implementation Plan
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
```

Implementation Self-Check is part of implementation execution and does not constitute formal verification or human approval.

Implementation Verification independently verifies the complete current implementation against the complete current approved requirement and implementation plan.

Implementation Review provides a separate technical quality assessment before human acceptance.

Human Acceptance is the final human decision that the implementation is accepted.

AI must not claim human acceptance or approval.
---

## 22. Prohibited AI Behaviors

AI must not:

- silently change approved requirements,
- silently change the approved implementation plan,
- make material business decisions,
- bypass architectural boundaries,
- expand scope,
- introduce unnecessary frameworks or patterns,
- weaken tests to obtain a passing result,
- hide build/test failures,
- commit secrets,
- claim human approval,
- claim verification that was not actually performed.

---

## 23. Standard Implementation Workflow

Use this workflow for each implementation slice:

```text
1. Read approved requirement
        ↓
2. Read approved implementation plan
        ↓
3. Identify requested implementation slice
        ↓
4. Inspect relevant repository code
        ↓
5. Confirm architecture and dependencies
        ↓
6. Implement requested tasks
        ↓
7. Add/update tests
        ↓
8. Build and run relevant tests
        ↓
9. Review requirement and plan traceability
        ↓
10. Check architecture and scope
        ↓
11. Review diff
        ↓
12. Perform implementation self-check
        ↓
13. Report implementation results and deviations
        ↓
14. Implementation Verification
        ↓
15. Implementation Review
        ↓
16. Human Acceptance
        ↓
17. Commit/push
```

If a material conflict, finding, or decision is discovered during implementation or subsequent verification/review, pause at the affected step and use the applicable governed corrective-change process before continuing.

---

## 24. Final Principle

The implementation phase translates an approved implementation plan into working, tested code.

AI should optimize for:

**traceability + correctness + architectural consistency + verification + controlled scope**

not simply for producing code quickly.

The approved requirement defines **what the system must do**.

The approved implementation plan defines **how the work is organized and where it should be implemented**.

The implementation phase produces **working code and implementation evidence**.

Implementation Verification independently verifies the complete current implementation against the complete current approved requirement and implementation plan.

Implementation Review assesses the technical quality and readiness of the complete current implementation.

Human Acceptance remains the final human gate before the implementation is considered accepted.

Human acceptance does not replace verification or review, and verification or review does not constitute human acceptance.