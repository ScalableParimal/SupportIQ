---
name: implementation
description: Executes the governed Implementation process using the repository Implementation Guideline, Prompt, and Request.
---

# Implementation Skill

## 1. Purpose

Execute the repository's governed Implementation process.

This Skill provides the reusable execution procedure for implementing an approved Implementation Plan. It does not replace or duplicate the normative rules defined by the Implementation Guideline.

## 2. Governing Artifacts

Before execution, load and follow:

- `docs/ai/guidelines/IMPLEMENTATION_GUIDELINES.md`
- `docs/ai/prompts/IMPLEMENTATION_PROMPT.md`
- `docs/ai/request/IMPLEMENTATION_REQUEST.md`

The Guideline is the normative authority for implementation.

The Prompt defines the controlled invocation requirements.

The Request supplies run-specific inputs.

Do not duplicate, reinterpret, or override their instructions in this Skill.

## 3. Execution Preconditions

Before modifying the repository:

1. Load the governing Guideline, Prompt, and Request.
2. Resolve the Current Approved Requirement.
3. Confirm its approval status and approval evidence.
4. Resolve the Current Approved Implementation Plan.
5. Confirm its approval status and required human approval evidence.
6. Resolve the implementation slice requested by the user.
7. Inspect the relevant current repository state.
8. Confirm that the required implementation inputs are available.

Do not begin implementation if required approval or authoritative artifacts cannot be established.

## 4. Execution Procedure

Execute the following sequence:

1. Establish the current approved Requirement as the business source of truth.
2. Establish the current approved Implementation Plan as the implementation source of truth.
3. Establish the requested implementation slice.
4. Inspect the relevant repository code, architecture, dependencies, and tests.
5. Map the requested work to the applicable approved plan tasks.
6. Implement the requested slice.
7. Add or update appropriate tests.
8. Execute the implementation checks required by the governing Guideline.
9. Review requirement and plan traceability.
10. Review the resulting repository changes and implementation scope.
11. Perform the required implementation self-check.
12. Record implementation evidence, deviations, and unresolved issues.
13. Produce the implementation report.
14. Stop at the Implementation process boundary.

The detailed implementation rules remain defined by the Guideline.

## 5. Implementation Scope

Implement only the requested implementation slice.

Task IDs and the requested slice are execution context. They do not replace or override the complete current approved Requirement or current approved Implementation Plan.

Small supporting changes are permitted only when necessary to complete the requested task and remain within approved scope.

Do not implement future or unrelated plan work.

## 6. Repository Handling

Use the actual repository as the technical context.

Before coding, inspect the relevant:

- projects and dependencies;
- architecture and layer boundaries;
- existing implementation patterns;
- interfaces and abstractions;
- tests;
- configuration;
- data-access conventions;
- related features.

Do not invent repository conventions where the repository can provide evidence.

## 7. Implementation Boundary

The Skill may modify product implementation artifacts required by the approved plan and requested implementation slice.

It may:

- modify application source code;
- modify frontend source code;
- modify backend source code;
- add or update appropriate tests;
- make other implementation changes explicitly required by the approved plan.

It must not modify the approved Requirement or approved Implementation Plan as an informal part of implementation.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 8. Traceability

Maintain traceability through the implementation:

Requirement
→ applicable business rule/contract
→ approved Implementation Plan task
→ code change
→ test
→ implementation verification evidence

Record sufficient information to establish which approved requirements and plan tasks are addressed by the implementation slice.

## 9. Implementation Self-Check

After implementation, execute the self-check required by the governing Guideline.

Use actual build, test, repository, architecture, scope, and diff evidence where available.

The self-check is part of Implementation and does not replace the separate Implementation Verification process.

## 10. Failure Handling

When an implementation check fails:

1. Identify the failure.
2. Determine whether the current implementation caused it.
3. Fix it when the correction remains within the approved scope.
4. Re-run the affected checks.
5. Report remaining failures honestly.

Do not hide failures, weaken meaningful tests, or claim successful completion without the required evidence.

## 11. Deviation Handling

If implementation reveals a material conflict or deviation involving:

- the Requirement;
- the approved Implementation Plan;
- architecture;
- technical dependencies;
- repository constraints;

stop at the affected point.

Record:

- what was approved;
- what was discovered;
- why it matters;
- affected implementation;
- impact;
- decision required.

Do not silently resolve a material deviation.

Route material deviations through the applicable Finding Investigation and Corrective Change Decision & Plan Update process.

## 12. Plan and Requirement Change Boundary

The Skill must not informally modify the approved Requirement or approved Implementation Plan.

If a material change is required:

1. Pause the affected implementation work.
2. Record the deviation.
3. Route it through the applicable governed corrective-change process.
4. Wait for the required human decision and approval.
5. Resume only against the resulting current approved artifacts.

Do not continue implementation against a superseded or invalidated plan.

## 13. Evidence and Traceability

Distinguish:

- implementation evidence;
- reported evidence;
- deviations;
- unresolved issues.

Use actual execution results wherever available.

Do not claim a build, test, verification, or implementation result that was not actually established.

## 14. Process Boundary

This Skill performs Implementation only.

It does not:

- perform Requirement Analysis;
- perform Requirement Analysis Verification;
- update requirements;
- perform Implementation Planning;
- perform Implementation Plan Verification;
- perform formal Implementation Verification;
- perform Implementation Review;
- investigate findings;
- decide corrective changes;
- perform Human Review Approval;
- perform Human Plan Approval;
- perform Human Acceptance;
- commit or push changes.

Formal Implementation Verification, Implementation Review, and Human Acceptance remain separate governed stages.

## 15. Completion

Return the implementation result required by the governing Guideline and Prompt, including:

- implemented tasks;
- files/projects changed;
- tests added or updated;
- build/test results;
- requirement traceability;
- plan traceability;
- deviations;
- unresolved issues;
- implementation self-check status.

Clearly state the implementation completion status.

Do not mark the implementation approved or accepted.

The Skill ends with the implementation report and handoff to formal Implementation Verification.