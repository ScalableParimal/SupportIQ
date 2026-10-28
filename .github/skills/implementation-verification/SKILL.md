---
name: implementation-verification
description: Executes the governed Implementation Verification process using the repository Implementation Verification Guideline, Prompt, and Request.
---

# Implementation Verification Skill

## 1. Purpose

Execute the governed Implementation Verification process defined by the repository Implementation Verification Guideline, Prompt, and Request.

This Skill provides the reusable execution mechanics for Implementation Verification.

The governing rules, verification criteria, evidence classifications, finding classifications, status definitions, and required report content remain owned by the referenced Governance artifacts.

## 2. Governing Artifacts

Read and follow:

- `docs/ai/guidelines/IMPLEMENTATION_VERIFICATION_GUIDELINES.md`
- `docs/ai/prompts/IMPLEMENTATION_VERIFICATION_PROMPT.md`
- `docs/ai/request/IMPLEMENTATION_VERIFICATION_REQUEST.md`

Use the current repository versions of these artifacts.

Do not duplicate or redefine their normative requirements in this Skill.

## 3. Execution Preconditions

Before verification:

1. Read the applicable Implementation Verification Guideline.
2. Read the Implementation Verification Prompt.
3. Read the Verification Request.
4. Identify the current approved Requirement.
5. Identify the current approved Implementation Plan.
6. Identify applicable architecture and engineering constraints.
7. Inspect the actual repository and relevant implementation artifacts.
8. Confirm that the required source artifacts are available.

If the required approved sources cannot be established, do not assume their content or status.

Record the resulting evidence limitation in the verification report.

## 4. Execution Procedure

Execute the verification using this sequence:

1. Establish the current approved verification baseline.
2. Establish the complete implementation verification scope.
3. Treat task IDs, recently changed files, findings, corrective changes, and other request-specific information as verification context only.
4. Inspect the actual repository implementation.
5. Compare the complete implementation against the approved Requirement.
6. Compare the complete implementation against the approved Implementation Plan.
7. Verify applicable architecture and engineering constraints.
8. Inspect relevant tests and available execution evidence.
9. Inspect worktree or diff information when available.
10. Establish requirement and plan traceability.
11. Classify evidence according to the governing Guideline.
12. Record findings and verification gaps according to the governing Guideline.
13. Determine the governed verification status.
14. Produce the complete verification report.
15. Determine the recommended next process from the verification result.

Do not narrow the verification to the implementation slice identified in the Request.

Do not expand the verification into unrelated features or future work outside the approved feature scope.

## 5. Complete-Scope Handling

The verification target is the complete current implementation covered by the current approved Requirement and current approved Implementation Plan.

Use Request-specific task IDs, changed files, implementation slices, or verification objectives to prioritize attention where appropriate.

Do not treat them as a scope restriction.

When verification follows corrective implementation or an approved implementation-plan change, perform complete implementation verification again.

## 6. Repository and Evidence Handling

Use the actual repository and approved source artifacts as the primary sources of verification.

Do not rely solely on previous AI summaries.

When commands, tests, builds, or other verification activities are executed, record the actual command and observed result.

When behavior is established through source inspection without execution, classify it accordingly.

When evidence is supplied by another person or process but is not independently reproduced, classify it accordingly.

When available evidence is insufficient, explicitly record the verification limitation rather than inferring correctness.

## 7. Finding and Decision Boundary

Do not resolve, correct, redesign, or otherwise apply findings during Implementation Verification.

For a finding requiring correction:

1. Record the finding and supporting evidence.
2. Identify the applicable finding category and severity.
3. Identify the affected implementation or governed artifact.
4. Route the finding to the governed Finding Investigation process.
5. Follow the subsequent Corrective Change Decision & Plan Update process where required.

Implementation Verification does not authorize corrective implementation.

## 8. Read/Write Boundary

Implementation Verification is read-only.

The Skill must not modify:

- source files
- tests
- requirements
- implementation plans
- configuration
- migrations
- database state
- other product artifacts

The Skill must not:

- fix findings
- redesign implementation
- apply corrective changes
- commit changes
- push changes

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 9. Independence Boundary

Perform verification independently from the implementation activity being verified.

Do not treat implementation-agent reports, self-checks, previous AI conclusions, or reported test results as independently verified facts unless the applicable evidence is independently established.

Maintain a clear distinction between:

- verification conclusions
- reported evidence
- source inspection evidence
- executed evidence
- unresolved uncertainty

## 10. Traceability

Maintain traceability between:

- approved Requirement
- approved Implementation Plan
- implemented behavior
- implementation tasks
- tests
- verification evidence
- findings
- recommended next process

Task-by-task reporting is required where defined by the governing Guideline, but task-level reporting must not restrict complete implementation verification.

## 11. Process Boundary

This Skill performs only Implementation Verification.

It must not perform:

- Requirement Analysis
- Requirement Analysis Verification
- Requirement Update
- Implementation Planning
- Implementation Plan Verification
- Implementation
- Finding Investigation
- Corrective Change Decision & Plan Update
- Human Requirement Approval
- Human Review Approval
- Human Plan Approval
- Human Acceptance
- Commit or Push

If another process is required, report the appropriate next process rather than executing it as part of Implementation Verification.

## 12. Approval Boundary

Implementation Verification does not grant:

- Requirement Approval
- Plan Approval
- Review Approval
- Human Acceptance
- implementation authorization

A verification status is not a human acceptance decision.

Do not use `APPROVED` as the verification status.

## 13. Completion

Complete the process only after the required verification activities and reporting defined by the governing Guideline have been performed.

The final verification report must follow the report structure required by the governing Guideline and Prompt.

The Skill must clearly state:

- overall verification status
- verification scope
- verification context
- requirement traceability
- implementation-plan traceability
- test verification
- material findings
- evidence classification
- remaining verification gaps
- recommended next process

The Skill ends with the verification report.

It does not authorize downstream execution.