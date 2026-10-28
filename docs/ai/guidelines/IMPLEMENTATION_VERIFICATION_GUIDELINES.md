# Implementation Verification Guidelines

## 1. Purpose

Implementation Verification determines whether an implemented change conforms
to the approved requirement and approved implementation plan.

It is an independent verification activity performed after implementation and
before implementation review or human acceptance.

Implementation Verification establishes evidence and identifies gaps.
It does not perform corrections or grant human acceptance.

---

## 2. Source of Truth

Use the following sources when available:

1. Approved requirement — functional source of truth
2. Approved implementation plan — implementation-scope source of truth
3. Approved architecture and engineering guidelines — technical constraints
4. Actual repository — implementation source of truth
5. Test results and other execution results — verification evidence

When the actual repository or approved source documents are available, do not
rely solely on previous AI summaries.

If sources conflict, identify the conflict rather than silently choosing a
different interpretation.

---

## 3. Complete Implementation Verification

Implementation Verification must verify the complete current implementation against:

1. The current approved Requirement
2. The current approved Implementation Plan
3. The current repository implementation
4. The applicable architecture and engineering constraints

Verification must not be limited only to:

- the task that was recently implemented
- files that were recently changed
- the finding that triggered a corrective change
- components identified as "impacted"

When Implementation Verification is run after a corrective implementation or implementation plan update, the complete implementation must be verified again.

This ensures that:

- the corrective change resolves the identified finding
- the complete implementation still satisfies the requirement
- the complete implementation still satisfies the current approved implementation plan
- previously implemented functionality has not regressed
- interactions between changed and unchanged components remain valid
- architecture and engineering constraints continue to be satisfied

The fact that a component was not changed does not exempt it from verification.

The verification target is always:

Current Approved Requirement
+
Current Approved Implementation Plan
+
Current Complete Implementation

--

## 4. Verification Scope

Implementation Verification must verify the complete current implementation of
the feature covered by the current approved requirement and current approved
implementation plan.

The Verification Request may identify a specific implementation slice,
specific task IDs, recently changed files, a feature or implementation area,
or other implementation context.

These items provide verification context and identify areas requiring
particular attention. They do not limit the verification scope.

The verification scope may include:

- all implemented task IDs
- recently implemented task IDs
- feature or implementation area
- approved requirement sections
- approved implementation-plan sections
- relevant architecture constraints
- source code
- project references
- configuration
- tests
- migrations
- infrastructure
- worktree and diff

For example, if the Verification Request identifies specific task IDs such as
T022–T027, those task IDs identify the recently implemented work that should
receive particular attention during verification.

However, verification must also evaluate the interaction between those tasks
and the rest of the current implementation.

Task IDs, recently changed files, implementation slices, or other
implementation context in the Verification Request must not be interpreted as
a restriction on the verification scope.

Therefore:

Verification Context ≠ Verification Scope

The verification scope remains the complete current implementation covered by
the current approved requirement and current approved implementation plan.

Do not expand verification into unrelated features or future implementation
tasks that are outside the approved feature scope.

---

## 5. Verification Activities

### 5.1 Establish the Approved Scope

Determine:

- what is required
- what is explicitly excluded
- what the approved implementation plan expects
- which architecture boundaries apply
- which files or components are expected to be involved
- which acceptance criteria must be satisfied

### 5.2 Inspect the Implementation

Inspect the actual repository and relevant implementation artifacts.

Consider, where applicable:

- source code
- project references
- configuration
- tests
- migrations
- infrastructure
- related existing code
- worktree and diff

### 5.3 Requirement Traceability

For each relevant requirement or task, determine whether it is:

- Implemented
- Partially Implemented
- Not Implemented
- Cannot Be Verified

Provide supporting evidence for the determination.

### 5.4 Implementation-Plan Traceability

Determine whether the implementation follows the approved implementation
plan.

Identify:

- planned items implemented
- planned items missing
- unapproved implementation changes
- architecture deviations
- approved changes to the plan

Do not treat an implementation change as approved merely because it appears
reasonable.

### 5.5 Test Verification

Verify, where applicable, that:

- required tests exist
- tests represent the approved behavior
- important acceptance criteria are covered
- important edge cases are covered
- assertions verify behavior rather than implementation details
- tests do not introduce behavior excluded by the requirement

If tests are executed as part of verification, record the actual command and
observed result.

If tests are not executed, clearly distinguish source-level test inspection
from test execution.

### 5.6 Scope Verification

Inspect the worktree or diff when available.

Identify:

- intended changes
- unrelated changes
- unexpected production changes
- unexpected schema changes
- unexpected API changes
- unexpected dependencies
- unexpected configuration changes
- unexpected documentation changes

---

## 6. Evidence Classification

Every important verification conclusion must be classified as one of the
following.

### Executed Evidence

The verifier actually executed the relevant command, test, build, or other
verification activity and observed the result.

### Source Inspection Evidence

The conclusion was established by inspecting source code, configuration,
project structure, tests, or other repository artifacts without executing the
relevant behavior.

### Reported Evidence

A result was provided by the user or another agent, but the verifier did not
independently reproduce it.

### Unverified

Available evidence is insufficient to establish the conclusion.

Never represent source-inspection or reported evidence as executed evidence.

---

## 7. Finding Classification

Classify findings using one of the following categories.

### Requirement Gap

The implementation does not satisfy the approved requirement.

### Plan Deviation

The implementation differs from the approved implementation plan without an
approved plan change.

### Architecture Deviation

The implementation violates an approved architecture or dependency constraint.

### Test Gap

Required behavior does not have adequate test coverage.

### Test Defect

The test incorrectly represents the approved requirement or expected behavior.

### Scope Deviation

The implementation contains unrelated or unapproved changes.

### Verification Gap

The implementation may be correct, but sufficient verification evidence has
not been obtained.

### Documentation Gap

Required implementation documentation is missing, inconsistent, or incorrect.

---

## 8. Finding Severity

Where applicable, classify findings as:

- Critical
- High
- Medium
- Low

Severity describes the impact of the finding.

Severity must not be used as an acceptance decision.

---

## 9. Read-Only Boundary

Implementation Verification is a read-only activity.

The verifier must not:

- modify source files
- modify tests
- modify requirements
- modify implementation plans
- modify configuration
- modify database state
- fix findings
- redesign the implementation
- commit changes
- push changes

If a correction is required, report the finding for the appropriate corrective
process.

---

## 10. Handling Uncertainty

Do not infer correctness when available evidence is insufficient.

Examples include:

- a build succeeds but required runtime behavior was not verified
- tests exist but their assertions do not establish the requirement
- an AI summary claims a change exists but the repository was not inspected
- a test result was reported but was not independently reproduced
- a required external dependency or environment could not be verified

When evidence is insufficient, explicitly state:

`Cannot be verified from available evidence.`

Do not convert an assumption into a verified fact.

---

## 11. Verification Status

Use one of the following statuses.

### VERIFIED

The complete current implementation conforms to the approved requirement and
approved plan based on the available evidence, with no material verification
gaps.

### VERIFIED WITH GAPS

The complete current implementation appears compliant, but one or more verification gaps remain. This status does not authorize progression to any downstream stage. Resolve every identified verification gap before proceeding to any downstream stage.

### CHANGES REQUIRED

A requirement gap, plan deviation, architecture deviation, material test
defect, scope deviation, or other material issue was identified.

### CANNOT VERIFY

Available evidence is insufficient to establish whether the complete current implementation conforms to the approved requirement and plan.

Do not use `APPROVED` as the verification status.

Human acceptance is a separate decision.

---

## 12. Verification Report

The verification report must contain:

1. Overall verification status
2. Verification scope
3. Verification context
4. Task-by-task verification
5. Requirement traceability
6. Implementation-plan traceability
7. Test verification
8. Scope and deviation findings
9. Evidence classification
10. Remaining verification gaps
11. Recommended next process

The report must clearly distinguish:

- verification scope
- verification context
- verified facts
- findings
- reported evidence
- unresolved uncertainty

Task-by-task verification must not be interpreted as limiting verification to
only the tasks identified in the Verification Request.

Bind the report to the exact approved sources and complete implementation state under the common execution contract. Associate task determinations and findings with their Plan-qualified task references and evidence. Identify any previous result being superseded and the basis for that relationship.

An incomplete or interrupted attempt must preserve available evidence and missing coverage without asserting completed verification. Resume or restart only after reconciling the target state. Historical task verification or retained implementation must not exempt any part of the complete current implementation from required verification.

---

## 13. Recommended Next Process

The recommended next process depends on the verification result:

- `VERIFIED` → proceed to Implementation Review
- `VERIFIED WITH GAPS` → Resolve every remaining verification gap. Do not proceed to any downstream stage until every gap is resolved; do not explicitly accept or waive a gap as a substitute for resolution.
- `CHANGES REQUIRED` → proceed to Finding Investigation
- `CANNOT VERIFY` → Obtain the missing evidence and resolve the associated verification gap before proceeding to any downstream stage.

Implementation Verification itself does not authorize corrective changes or
human acceptance.