---
name: implementation-review
description: Executes the governed Implementation Review process using the repository Implementation Review Guideline, Prompt, and Request.
---

# Implementation Review Skill

## 1. Purpose

Execute the governed Implementation Review process defined by the repository Implementation Review Guideline, Prompt, and Request.

This Skill provides reusable execution mechanics for the technical review.

The governing rules, review areas, finding classifications, evidence classifications, review outcomes, and report requirements remain owned by the referenced Governance artifacts.

Do not duplicate or redefine those rules in this Skill.

## 2. Governing Artifacts

Read and follow:

- `docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md`
- `docs/ai/prompts/IMPLEMENTATION_REVIEW_PROMPT.md`
- `docs/ai/request/IMPLEMENTATION_REVIEW_REQUEST.md`

Use the current repository versions of these artifacts.

## 3. Execution Preconditions

Before beginning the review:

1. Read the Implementation Review Guideline.
2. Read the Implementation Review Prompt.
3. Read the Implementation Review Request.
4. Identify the current approved Requirement.
5. Identify the current approved Implementation Plan.
6. Identify applicable architecture and engineering guidelines.
7. Obtain the current implementation and relevant repository context.
8. Obtain available Implementation Verification results.
9. Obtain applicable finding-investigation or corrective-change information.
10. Obtain available test and build evidence.

If required evidence is unavailable, record the limitation rather than assuming the missing information.

## 4. Execution Procedure

Execute the review using this sequence:

1. Establish the current approved Requirement and Plan as the authoritative baseline.
2. Establish the complete implementation review scope.
3. Treat task IDs, recently changed files, findings, and corrective changes as review context only.
4. Inspect the complete implementation within the approved scope.
5. Review the implementation against applicable architecture and repository boundaries.
6. Evaluate applicable technical-quality areas defined by the governing Guideline.
7. Use existing Implementation Verification results as evidence without duplicating verification unnecessarily.
8. Inspect available tests, builds, configuration, and operational evidence as applicable.
9. Identify material technical findings and non-blocking observations.
10. Classify evidence and uncertainty.
11. Determine the governed review outcome.
12. Assess readiness for Human Acceptance.
13. Produce the complete review report required by the governing Guideline.
14. Determine the recommended next process.

## 5. Complete-Scope Review

Review the complete current implementation within the approved feature scope.

Do not restrict review to:

- recently changed files
- the latest task
- a finding
- a corrective change
- an implementation slice

Consider relevant interactions between changed and unchanged components.

Do not expand the review into unrelated features or future work outside the approved scope.

## 6. Technical Review Handling

Evaluate only the technical concerns applicable to the implementation and defined by the governing Guideline.

Focus on material concerns affecting:

- technical soundness
- maintainability
- architecture
- correctness
- security
- performance
- testing
- operational readiness
- repository consistency

Do not introduce new requirements.

Do not report subjective preferences as defects unless supported by an approved requirement, architecture constraint, engineering guideline, or established repository convention.

Avoid speculative defects and unnecessary refactoring recommendations.

## 7. Verification Relationship

Use Implementation Verification results as supporting evidence where applicable.

Do not treat successful Implementation Verification as automatic completion of Implementation Review.

Do not unnecessarily repeat verification activities already established by reliable evidence.

If a material verification failure or new material concern is discovered during review, record it and route it through the applicable governed finding process.

Do not reopen resolved findings without new evidence.

## 8. Finding and Investigation Boundary

For each material finding:

1. Record the affected component or file.
2. Record supporting evidence.
3. Identify expected and actual behavior or applicable technical principle.
4. Record impact, severity, and confidence.
5. Distinguish confirmed facts from assumptions.
6. Determine the appropriate next governed process.

If a potentially material issue cannot be reliably determined from available evidence, do not declare it a confirmed defect.

Record the uncertainty and recommend Finding Investigation.

## 9. Read/Write Boundary

Implementation Review is read-only.

Do not modify:

- source code
- tests
- configuration
- migrations
- requirements
- implementation plans
- database state
- other product artifacts

Do not:

- implement fixes
- redesign the implementation
- refactor code
- commit changes
- push changes

Corrections must proceed through the governed corrective process.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 10. Evidence Handling

Maintain explicit evidence classification throughout the review.

Distinguish:

- executed evidence
- source inspection evidence
- reported evidence
- unverified information
- facts
- assumptions
- recommendations

Do not represent reported or unverified information as independently executed evidence.

When evidence is incomplete, state:

- what is unknown
- why it matters
- what evidence would resolve it

## 11. Human Acceptance Boundary

Implementation Review provides an AI technical readiness assessment only.

It may conclude that the implementation is:

`READY FOR HUMAN ACCEPTANCE`

or otherwise state the appropriate readiness condition defined by the governing Guideline.

It must never grant or imply:

- Human Acceptance
- Human Approval
- production approval
- release approval

unless an explicitly supplied human decision is being reported as evidence.

## 12. Process Boundary

This Skill performs only Implementation Review.

It must not perform:

- Requirement Analysis
- Requirement Analysis Verification
- Requirement Update
- Implementation Planning
- Implementation Plan Verification
- Implementation
- Implementation Verification
- Finding Investigation
- Corrective Change Decision & Plan Update
- Human Requirement Approval
- Human Review Approval
- Human Plan Approval
- Human Acceptance
- Commit or Push

If another process is required, report it as the recommended next process rather than executing it within this Skill.

## 13. Completion

Complete the process only after the review activities and reporting requirements defined by the governing Guideline have been performed.

Return the complete Implementation Review report defined by the Guideline.

The report must clearly distinguish:

- review status
- scope reviewed
- Requirement/Plan alignment
- architecture observations
- technical-quality observations
- material findings
- non-blocking observations
- evidence classification
- uncertainty
- Human Acceptance readiness
- recommended next process

The Skill ends with the review report.