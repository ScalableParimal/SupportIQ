# Requirement Analysis Verification Guidelines

## 1. Purpose

This guideline defines the process for independently verifying a requirement analysis before Human Requirement Approval.

Requirement Analysis Verification determines whether the complete current requirement analysis accurately and sufficiently represents the source requirement and provides a clear basis for implementation planning.

The verification identifies:

- missing requirements
- incorrect interpretations
- ambiguities
- contradictions
- unsupported assumptions
- scope gaps
- scope creep
- missing decisions
- incomplete acceptance criteria
- unclear dependencies
- non-testable requirements

This process does NOT approve the requirement.

This process does NOT create the implementation plan.

This process does NOT implement the feature.

---

## 2. Core Principle

Requirement Analysis identifies and interprets what the requirement means.

Requirement Analysis Verification independently evaluates whether that analysis is complete, accurate, internally consistent, and sufficiently clear for Human Requirement Approval.

The verification question is:

> Does the complete current requirement analysis accurately represent the complete current source requirement, clearly distinguish confirmed requirements from assumptions and decisions, and provide a sufficiently clear and testable basis for implementation planning?

The complete requirement analysis must be verified.

Do not verify only:

- recently changed requirements
- individual requirements
- individual acceptance criteria
- one business rule
- one feature area

Review the relationships and dependencies across the complete analysis.

---

## 3. Current-State Verification

Requirement Analysis Verification always uses:

1. Source Requirement
2. Resulting Updated Requirement, where a Requirement Update has occurred
3. Complete current Requirement Analysis
4. Applicable approved business/architecture constraints
5. Applicable human decisions, distinguishing decisions explicitly approved by the human
6. Additional evidence supplied for verification

If the requirement or requirement analysis changes, verify the complete current analysis again.

Do not verify only the changed section.

The verification target is always:

Source Requirement
+
Resulting Updated Requirement, where applicable
+
Complete Current Requirement Analysis
+
Applicable Approved Constraints and Human Decisions

The resulting Updated Requirement is an explicit verification target when a Requirement Update has occurred. It must not be treated as implicit in the Requirement Analysis.

---

## 4. Source of Truth

Use the following priority:

1. Current source requirement
2. Explicitly approved business decisions
3. Applicable approved constraints
4. Resulting Updated Requirement, where applicable
5. Current requirement analysis
6. Supporting documentation
7. Additional supplied evidence

The source requirement defines WHAT is requested.

The requirement analysis interprets and structures that requirement.

The analysis must not silently introduce new requirements.

---

## 5. Scope

Review the complete requirement analysis, including where applicable:

- functional requirements
- non-functional requirements
- business rules
- data requirements
- validation rules
- error scenarios
- user interactions
- acceptance criteria
- dependencies
- assumptions
- constraints
- exclusions
- edge cases
- integration requirements
- performance expectations
- security requirements
- compatibility requirements
- open questions
- decisions required

Review only areas relevant to the source requirement.

Do not introduce requirements that are not supported by the source requirement or approved decisions.

When a Requirement Update has occurred, also review the complete resulting Updated Requirement against the Source Requirement and applicable approved human decisions. Verify that the approved decisions were incorporated accurately and that no unsupported or unapproved changes were introduced.

---

## 6. Verification Areas

### 6.1 Requirement Coverage

Determine whether every meaningful part of the source requirement is represented in the analysis.

Identify:

- missing requirements
- partially analyzed requirements
- duplicated requirements
- requirements represented incorrectly
- requirements with insufficient detail

Each significant source requirement should be traceable to the corresponding analysis.

---

### 6.2 Interpretation Accuracy

Verify that the analysis accurately represents what the source requirement states.

Identify:

- incorrect interpretations
- unsupported conclusions
- changed meaning
- assumptions presented as requirements
- technical implementation decisions incorrectly presented as business requirements

Do not replace ambiguous source wording with an assumed interpretation.

---

### 6.3 Scope Alignment

Verify that the analysis:

- preserves the requested scope
- does not omit approved scope
- does not introduce unrequested functionality
- respects explicit exclusions
- clearly identifies boundaries

Identify both:

- scope gaps
- scope creep

---

### 6.4 Functional Requirement Completeness

Verify that applicable functional behavior is clearly represented.

Consider:

- inputs
- outputs
- actions
- workflows
- business behavior
- success conditions
- failure conditions
- state changes
- edge cases

The analysis should provide enough clarity for implementation planning without prematurely prescribing implementation details.

---

### 6.5 Business Rules

Identify and verify:

- business rules
- validation rules
- uniqueness rules
- conditional behavior
- required/optional behavior
- limits and boundaries
- exception conditions

Distinguish business rules from technical implementation choices.

---

### 6.6 Non-Functional Requirements

Where applicable, verify coverage of:

- performance
- scalability
- availability
- security
- reliability
- usability
- compatibility
- observability
- operational constraints

Do not invent non-functional requirements that are not supported by the source requirement or approved constraints.

---

### 6.7 Acceptance Criteria

Verify that important requirements have observable and testable acceptance criteria.

Acceptance criteria should be:

- clear
- observable
- testable
- unambiguous
- traceable to the requirement

Avoid criteria that describe implementation rather than expected behavior unless implementation detail is explicitly required.

---

### 6.8 Ambiguities

Identify statements that can reasonably have multiple interpretations.

For each material ambiguity, document:

- ambiguous requirement
- possible interpretations
- affected behavior
- affected scope
- consequence of choosing each interpretation
- decision required

Do not silently select an interpretation for material business behavior.

---

### 6.9 Contradictions and Consistency

Check the complete analysis for conflicts between:

- requirements
- business rules
- acceptance criteria
- exclusions
- constraints
- dependencies

Also identify contradictions between the analysis and the source requirement.

---

### 6.10 Assumptions

Identify assumptions explicitly.

Classify them as:

- confirmed
- reasonable but unconfirmed
- material assumption requiring human decision

Never present an assumption as a confirmed requirement.

---

### 6.11 Dependencies

Identify relevant dependencies such as:

- external systems
- data sources
- upstream/downstream processes
- business approvals
- infrastructure prerequisites
- other features
- contractual or compatibility constraints

Distinguish confirmed dependencies from assumptions.

---

### 6.12 Decisions Required

Identify decisions that must be made before the requirement can be considered sufficiently defined.

Examples:

- business behavior
- scope interpretation
- uniqueness semantics
- compatibility expectations
- security expectations
- performance targets
- integration behavior
- error behavior

AI may analyze options and consequences.

AI must not claim that a human decision has been made unless explicitly supplied as evidence.

---

### 6.13 Implementation-Neutrality

Requirement Analysis should describe expected behavior rather than prematurely prescribe implementation.

Identify when the analysis unnecessarily dictates:

- specific classes
- specific database tables
- specific frameworks
- specific code structures
- specific implementation patterns

unless those technical constraints are explicitly part of the approved requirement or architecture.

The purpose of requirement analysis is to establish WHAT is required.

Implementation Planning determines HOW it will be implemented.

---

## 7. Finding Classification

Classify identified issues as:

### Requirement Coverage Gap

A source requirement is missing or inadequately represented.

### Interpretation Error

The analysis incorrectly represents the source requirement.

### Ambiguity

The requirement has multiple reasonable interpretations requiring clarification.

### Contradiction

Requirements or analysis elements conflict with each other.

### Scope Issue

The analysis omits approved scope or introduces unapproved scope.

### Missing Decision

A material decision is required before proceeding.

### Unsupported Assumption

An assumption is presented as fact or materially affects interpretation.

### Acceptance Criteria Gap

Required behavior does not have sufficiently clear acceptance criteria.

### Dependency Gap

A relevant dependency is missing or unclear.

### Non-Functional Gap

An applicable non-functional requirement is missing or insufficiently defined.

### Implementation Leakage

The analysis prematurely prescribes implementation details without requirement or architectural justification.

### Informational Observation

An observation that does not require correction.

---

## 8. Severity

Use:

### Critical

The requirement cannot safely proceed to planning without resolution.

### High

A significant issue that should normally be resolved before Human Requirement Approval.

### Medium

A meaningful issue that may require clarification or analysis adjustment.

### Low

A minor issue that does not normally block approval.

### Informational

Observation or improvement suggestion.

Severity must be based on impact, not personal preference.

---

## 9. Human Decision Requirements

Human decision is normally required when the issue involves:

- business intent
- requirement interpretation
- scope
- business rules
- externally visible behavior
- compatibility expectations
- security expectations
- material performance expectations
- other decisions that cannot be determined from the source requirement

AI may:

- identify the decision
- explain ambiguity
- present reasonable interpretations
- explain consequences
- recommend clarification

AI must not silently choose the business requirement.

---

## 10. Recommended Corrections

When changes are required, provide precise recommendations.

For each recommendation include:

- affected requirement/analysis section
- current issue
- proposed clarification or correction
- reason
- source requirement basis
- affected acceptance criteria
- affected downstream planning considerations

Requirement Analysis Verification is read-only in all cases. Do not modify the Requirement or Requirement Analysis during verification. If a change is required, route it through the separate Requirement Update process; do not combine verification and Requirement Update in one operation.

Material findings affecting governed artifacts must be routed through Finding Investigation and Corrective Change Decision & Plan Update. The verification activity must not apply the correction.

---

## 11. Read-Only Boundary

Requirement Analysis Verification is read-only in every invocation. Requirement Update is a separate process and must not be combined with verification.

Do not:

- modify the source requirement
- modify the requirement analysis
- create an implementation plan
- implement code
- modify tests
- make unapproved business decisions
- silently expand or reduce scope

The output is a verification report and, where necessary, recommended corrections or decisions.

Actual requirement changes belong to the requirement update/approval process.

---

## 12. Evidence Classification

Classify evidence as:

### Executed Evidence

Evidence directly produced during the current verification.

### Source Inspection Evidence

Evidence obtained by inspecting:

- source requirement
- requirement analysis
- approved constraints
- supporting documentation

### Reported Evidence

Evidence supplied by the user or another process.

### Unverified

Information that has not been independently confirmed.

Do not present reported or unverified information as independently verified evidence.

---

## 13. Uncertainty

If information is incomplete or conflicting:

- identify the uncertainty
- explain its impact
- do not silently resolve it
- identify the required clarification or evidence

Do not invent business intent.

---

## 14. Verification Outcome

Use one of the following:

### ANALYSIS VERIFIED

The complete requirement analysis accurately and sufficiently represents the source requirement.

No material gaps were identified.

### ANALYSIS VERIFIED WITH GAPS

The analysis is generally usable, but non-blocking gaps or observations exist.

### CHANGES REQUIRED

One or more material analysis issues must be resolved before Human Requirement Approval.

### DECISION REQUIRED

One or more material human/business decisions are required.

### EVIDENCE REQUIRED

Required information is missing.

### CANNOT VERIFY

The available information is insufficient for reliable verification.

---

## 15. Required Verification Report

The report must contain:

### 1. Verification Status

One of the defined outcomes.

### 2. Scope Verified

Identify:

- source requirement
- requirement analysis
- applicable constraints

### 3. Requirement Coverage

Summarize coverage and identify gaps.

### 4. Interpretation Verification

Identify interpretation issues.

### 5. Scope Verification

Identify scope gaps or scope creep.

### 6. Functional and Business Rule Verification

Summarize relevant findings.

### 7. Non-Functional Requirement Verification

Cover applicable areas.

### 8. Acceptance Criteria Verification

Identify gaps in testability or clarity.

### 9. Ambiguities and Contradictions

Identify unresolved issues.

### 10. Assumptions and Dependencies

Identify material assumptions and dependencies.

### 11. Decisions Required

List material unresolved decisions.

### 12. Findings

For each finding:

- classification
- severity
- affected section
- evidence
- impact
- confidence
- recommended action

### 13. Recommended Corrections

Provide precise changes where applicable.

### 14. Evidence Classification

Identify evidence used.

### 15. Uncertainty

Identify unresolved uncertainty.

### 16. Human Requirement Approval Readiness

State:

- READY FOR HUMAN REQUIREMENT APPROVAL
- NOT READY FOR HUMAN REQUIREMENT APPROVAL

This is a readiness assessment only.

It is NOT Human Requirement Approval.

### 17. Recommended Next Process

Normally:

- Human Requirement Approval
- Requirement Update / Clarification
- Corrective Change Decision & Plan Update
- Additional Evidence Collection

When a material verification finding affects a governed artifact, route it through Finding Investigation → Corrective Change Decision & Plan Update → required Human Approval before applying an approved change. Then perform the required verification. Do not apply corrections during Requirement Analysis Verification.

---

## 16. Verification Discipline

The verifier must:

- verify the complete current requirement analysis
- preserve source requirement traceability
- distinguish requirements from assumptions
- distinguish requirements from implementation decisions
- identify material ambiguities
- identify missing decisions
- avoid inventing business intent
- avoid introducing unsupported requirements
- avoid making human decisions
- preserve scope boundaries
- remain read-only

The objective is to determine whether the requirement analysis is sufficiently complete and reliable for Human Requirement Approval and subsequent implementation planning.

---

## 17. Critical Rule

Implementation Planning must not begin merely because a requirement analysis exists.

The expected sequence is:

Source Requirement
→ Requirement Analysis
→ Requirement Analysis Verification
→ Resolve Findings / Decisions
→ Human Requirement Approval
→ Implementation Planning