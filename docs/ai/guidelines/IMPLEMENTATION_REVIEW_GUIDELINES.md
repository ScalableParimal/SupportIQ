# Implementation Review Guidelines

## 1. Purpose

This guideline defines the process for performing a final technical review of an implementation before Human Acceptance.

Implementation Review evaluates the technical quality and readiness of the completed implementation.

It determines whether the implementation is:

- technically sound
- maintainable
- consistent with the approved architecture
- consistent with repository conventions
- appropriately tested
- free from unnecessary complexity
- free from material technical concerns that should block acceptance

Implementation Review is an AI technical assessment.

It does not constitute Human Acceptance.

---

## 2. Core Principle

Implementation Verification and Implementation Review have different responsibilities.

Implementation Verification answers:

> Does the implementation satisfy the current approved Requirement and current approved Implementation Plan?

Implementation Review answers:

> Is the implementation technically sound and ready for Human Acceptance?

Implementation Review must not duplicate Implementation Verification unnecessarily.

However, if a material verification failure is discovered during review, it must be reported as a finding and routed through the established Finding Investigation process.

---

## 3. Source of Truth

Use the following sources:

1. Current approved Requirement
2. Current approved Implementation Plan
3. Current repository implementation
4. Relevant architecture guidelines
5. Relevant engineering guidelines
6. Implementation Verification results
7. Test/build results
8. Finding Investigation results, if applicable
9. Corrective Change Decision / revised plan, if applicable

The current approved Requirement and current approved Implementation Plan remain authoritative.

Do not silently reinterpret or modify them during review.

---

## 4. Scope

Review the complete implementation.

Do not restrict the review only to:

- recently changed files
- the latest task
- the files mentioned in a finding
- the corrective change

Review the implementation as a complete system/component within the approved scope.

The review should consider interactions between changed and unchanged components where relevant.

---

## 5. Review Areas

### 5.1 Architecture

Verify that the implementation respects the approved architecture.

Consider:

- project/layer dependencies
- dependency direction
- separation of concerns
- responsibility boundaries
- interface ownership
- infrastructure isolation
- domain independence
- API/application/infrastructure boundaries
- prohibited dependencies

Do not introduce architectural requirements that are not part of the approved architecture or engineering guidelines.

---

### 5.2 Design Quality

Evaluate whether the implementation:

- has clear responsibilities
- avoids unnecessary coupling
- uses appropriate abstractions
- avoids unnecessary complexity
- avoids premature generalization
- avoids duplicated logic
- follows established repository patterns
- remains understandable and maintainable

The review should identify material design concerns rather than stylistic preferences.

---

### 5.3 Code Quality

Review for:

- readability
- consistency
- naming
- method/class responsibility
- duplication
- unnecessary code
- dead code
- error-prone patterns
- inappropriate magic values
- maintainability concerns

Do not report purely subjective style preferences as defects unless they conflict with an established repository convention or guideline.

---

### 5.4 Error Handling

Evaluate whether:

- expected errors are handled appropriately
- domain/application errors are mapped correctly
- unexpected exceptions are not silently swallowed
- error handling preserves useful diagnostic information
- error behavior is consistent with the approved API/application contract

---

### 5.5 Validation and Data Integrity

Review whether:

- validation occurs at the appropriate layer
- domain invariants are protected
- persistence constraints are appropriate
- duplicate/conflict behavior is handled correctly
- invalid states are prevented where required

---

### 5.6 Security

Review applicable security concerns such as:

- secrets
- credentials
- connection strings
- sensitive information exposure
- unsafe input handling
- injection risks
- inappropriate trust boundaries
- authorization/authentication implications where applicable

Do not invent security requirements outside the approved scope.

If security implications are uncertain or material, report them explicitly.

---

### 5.7 Performance

Review for obvious material performance concerns such as:

- unnecessary database calls
- N+1 queries
- unbounded data retrieval
- inefficient queries
- inappropriate synchronous blocking
- unnecessary allocations
- scalability concerns

Do not optimize speculative problems without evidence.

Distinguish:

- observed performance issue
- obvious code-level risk
- theoretical concern

---

### 5.8 Testing

Review whether tests provide meaningful coverage of the implemented behavior.

Consider:

- unit tests
- integration tests
- API tests
- frontend tests
- end-to-end tests where applicable
- positive cases
- negative cases
- boundary conditions
- error behavior
- regression coverage

Do not equate test count with test quality.

Review whether the tests actually verify behavior rather than implementation details.

---

### 5.9 Configuration and Operational Concerns

Review applicable:

- configuration
- environment variables
- connection configuration
- deployment assumptions
- logging
- migration/deployment requirements
- external dependencies
- operational risks

Do not treat development-only configuration as production configuration unless the implementation indicates that it will be used that way.

---

### 5.10 Repository Consistency

Check whether the implementation is consistent with:

- existing project structure
- naming conventions
- established patterns
- dependency management
- test organization
- configuration conventions
- documentation conventions

Existing repository conventions should be considered evidence, but do not automatically override the approved architecture or requirement.

---

## 6. Review Findings

Classify review findings as:

### Critical

A material issue that creates a significant risk to correctness, security, data integrity, architecture, or production behavior.

### High

A significant issue that should normally be resolved before Human Acceptance.

### Medium

A meaningful technical concern that may require correction depending on context.

### Low

A minor issue or maintainability concern that does not normally block acceptance.

### Informational

Observation or improvement suggestion that does not represent a defect.

Do not use severity merely to express personal preference.

---

## 7. Finding Evidence

Every material finding must include:

- finding
- affected component/file
- evidence
- expected behavior or principle
- actual behavior
- impact
- severity
- confidence

Clearly distinguish observed facts from assumptions.

---

## 8. Verification Relationship

Implementation Review may use Implementation Verification results as evidence.

However, a successful Implementation Verification does not automatically mean the implementation passes Implementation Review.

For example:

Implementation Verification may establish:

> The implementation satisfies the pagination requirement.

Implementation Review may still identify:

> The pagination implementation creates an unnecessary database round trip.

These are different concerns.

Likewise, Implementation Review must not re-open already resolved findings without new evidence.

---

## 9. Findings That Require Further Investigation

If the reviewer identifies a potentially material problem but cannot determine its validity from available evidence:

- do not declare it a confirmed defect
- classify it as requiring investigation
- identify the missing evidence
- recommend Finding Investigation

Do not implement fixes during review.

---

## 10. No Direct Corrections

Implementation Review is read-only.

Do not:

- modify source code
- modify tests
- modify configuration
- modify migrations
- modify requirements
- modify implementation plans
- implement fixes

If a correction is required:

Implementation Review
→ Finding Investigation
→ Corrective Change Decision & Plan Update
→ Human Approval
→ Implementation
→ Implementation Verification
→ Implementation Review

---

## 11. Human Acceptance Boundary

Implementation Review must never state:

- "Human approved"
- "Accepted"
- "Approved for production"
- "Approved for release"

unless that decision was explicitly made by the human and supplied as evidence.

The review may state:

> READY FOR HUMAN ACCEPTANCE

This means only that the AI technical review found no material blocking issues.

Human Acceptance remains a separate decision.

---

## 12. Evidence Classification

Classify evidence as:

### Executed Evidence

Evidence generated by executing a command or verification activity during the current review.

Examples:

- build execution
- test execution
- static analysis execution

### Source Inspection Evidence

Evidence obtained by inspecting code, configuration, documentation, or repository structure.

- repository-content inspection

### Reported Evidence

Evidence supplied by the user or another process.

### Unverified

Information that has not been independently confirmed.

Do not present reported or unverified information as executed evidence.

---

## 13. Uncertainty

When evidence is incomplete:

- state what is unknown
- explain why it matters
- identify what evidence would resolve it
- do not invent assumptions

If a material concern cannot be determined reliably, recommend Finding Investigation rather than declaring the implementation defective.

---

## 14. Review Outcome

The final review must produce one of:

### READY FOR HUMAN ACCEPTANCE

No material technical concerns were identified.

### READY FOR HUMAN ACCEPTANCE WITH NON-BLOCKING OBSERVATIONS

No material blocking issues were identified, but informational or low-impact observations exist.

### CHANGES REQUIRED

One or more material issues should be corrected before Human Acceptance.

### INVESTIGATION REQUIRED

A potentially material concern requires additional investigation before a reliable review conclusion can be reached.

### CANNOT COMPLETE REVIEW

Required evidence is unavailable or insufficient.

---

## 15. Required Review Report

The report must contain:

### 1. Review Status

One of the defined review outcomes.

### 2. Scope Reviewed

Identify:

- feature
- tasks reviewed, if applicable
- projects/components
- complete implementation scope

Task IDs, recently changed files, findings, or corrective changes are context for the review and must not be treated as a restriction on review scope.

The review must cover the complete current implementation within the approved scope.

### 3. Requirement / Plan Alignment

Summarize whether the implementation is consistent with the current approved Requirement and Plan.

Do not duplicate the complete Verification report.

### 4. Architecture Review

Identify material architecture observations.

### 5. Technical Quality Review

Cover relevant:

- design
- code quality
- error handling
- validation
- security
- performance
- testing
- configuration/operations
- repository consistency

### 6. Findings

For each material finding:

- severity
- component
- evidence
- impact
- confidence

### 7. Non-Blocking Observations

List useful but non-blocking observations separately.

### 8. Evidence Classification

Identify the evidence type used.

### 9. Uncertainty

Identify unresolved uncertainties.

### 10. Human Acceptance Readiness

State:

- READY FOR HUMAN ACCEPTANCE
- NOT READY FOR HUMAN ACCEPTANCE

This is a readiness assessment, not Human Acceptance.

### 11. Recommended Next Process

Normally:

- Human Acceptance, when the review is ready for acceptance
- Finding Investigation, when a material or potentially material finding requires investigation
- Corrective Change Decision & Plan Update, when a finding requires a governed corrective decision
- Additional Evidence Collection, when evidence is insufficient
- Implementation Verification, when the implementation has materially changed and complete verification is required

Bind the review to the exact approved sources, implementation state, and applicable verification report under the common execution contract. Establish whether supplied verification applies to the current target before using it as current conformity evidence. Identify interrupted or incomplete review coverage, unresolved applicability, and the exact next-process or human-gate prerequisites.

Report readiness for Human Acceptance separately from any actual Human Acceptance record. Preserve complete-current-implementation review and do not replace missing verification with a review readiness statement.

---

## 16. Review Discipline

The reviewer must:

- remain within the approved scope
- distinguish facts from opinions
- avoid speculative defects
- avoid unnecessary refactoring recommendations
- avoid introducing new requirements
- avoid silently changing architecture
- avoid implementing corrections
- preserve traceability
- focus on material technical quality

The objective is not to find the maximum number of issues.

The objective is to identify issues that materially affect the quality, correctness, maintainability, security, or readiness of the implementation.