---
name: implementation-plan-verification
description: Executes the governed Implementation Plan Verification process using the repository Implementation Plan Verification Guideline, Prompt, and Request.
---

# Implementation Plan Verification Skill

## 1. Purpose

Execute the repository's governed Implementation Plan Verification process.

This Skill provides the reusable execution procedure for independently verifying the complete current candidate Implementation Plan. It does not replace or duplicate the normative rules defined by the Implementation Plan Verification Guideline.

## 2. Governing Artifacts

Before execution, load and follow:

- `docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md`
- `docs/ai/prompts/IMPLEMENTATION_PLAN_VERIFICATION_PROMPT.md`
- `docs/ai/request/IMPLEMENTATION_PLAN_VERIFICATION_REQUEST.md`

The Guideline is the normative authority for the verification process.

The Prompt defines the controlled invocation requirements.

The Request supplies run-specific inputs.

Do not duplicate, reinterpret, or override their instructions in this Skill.

## 3. Execution Preconditions

Before starting:

1. Load the governing Guideline, Prompt, and Request.
2. Resolve the Current Approved Requirement.
3. Resolve the complete current Candidate Implementation Plan under verification.
4. Resolve the applicable architecture and engineering constraints.
5. Resolve relevant repository context and conventions.
6. Resolve available evidence and previous verification/review results.
7. Treat a previously approved Implementation Plan only as a baseline/comparator when supplied.
8. Confirm that the complete verification context is available.
9. If meaningful verification cannot be performed from the available context, stop and report the limitation.

## 4. Execution Procedure

Execute the following sequence:

1. Establish the complete current verification target.
2. Load the authoritative Requirement and applicable constraints.
3. Inspect the candidate Implementation Plan in its entirety.
4. Inspect relevant repository context required to evaluate the plan.
5. Independently evaluate the candidate plan according to the governing Guideline and Prompt.
6. Maintain traceability between verification observations and supporting evidence.
7. Record material findings using the classifications and severity defined by the Guideline.
8. Identify decisions, evidence, or plan changes required for progression.
9. Produce the complete verification report required by the governing artifacts.
10. Determine the applicable verification outcome.
11. Stop at the Implementation Plan Verification boundary.

## 5. Complete-Scope Verification

The verification target is always the complete current candidate Implementation Plan.

Task IDs, recently changed tasks, or a reported problem location may provide verification context but must not restrict the verification scope.

If the candidate plan changes after verification, the complete updated plan must be verified again.

## 6. Artifact Handling

Treat the following as distinct:

- Current Approved Requirement;
- Current Candidate Implementation Plan under verification;
- applicable architecture and engineering constraints;
- repository context;
- supporting evidence;
- previously approved Implementation Plan, when supplied.

Do not treat the candidate plan as an approved source of truth.

Do not silently reconcile conflicts between authoritative inputs.

Do not modify the candidate plan during verification.

## 7. Evidence and Traceability

Maintain sufficient traceability to show:

- what was verified;
- which source or evidence supports the verification;
- what was found;
- the affected task or plan area where applicable;
- impact;
- severity and confidence where required;
- recommended action.

Use the evidence categories defined by the governing Guideline.

Do not present reported or unverified information as independently verified evidence.

## 8. Finding and Decision Boundary

Verification findings are outputs of this process.

When a finding requires a plan change, provide the required recommendation and route it through the applicable governed process.

Do not apply a recommended plan change during verification.

Do not silently make a human decision to resolve a material ambiguity.

## 9. Read/Write Boundary

Implementation Plan Verification is read-only.

The Agent/Skill must not:

- modify the Requirement;
- modify the Implementation Plan;
- implement product changes;
- modify source code;
- modify tests;
- create migrations;
- change architecture;
- apply corrective changes;
- approve human decisions;
- commit or push changes.

The output is the verification result and, where applicable, recommended changes.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 10. Process Boundary

This Skill performs Implementation Plan Verification only.

It does not:

- perform Requirement Analysis;
- perform Requirement Analysis Verification;
- update requirements;
- perform Implementation Planning;
- implement product changes;
- perform Implementation Verification;
- perform Implementation Review;
- investigate findings;
- decide corrective changes;
- perform Human Review Approval;
- perform Human Plan Approval;
- perform Human Acceptance;
- commit or push changes.

## 11. Approval Boundary

Verification may determine readiness for the next human gate.

Verification readiness is not:

- Human Review Approval;
- Human Plan Approval;
- implementation authorization.

The Skill must not declare the Implementation Plan approved.

## 12. Completion

Return the complete Implementation Plan Verification result required by the governing Guideline and Prompt.

Identify the resulting verification outcome and appropriate next governed process.

If the current plan is not ready, identify the findings, decisions, evidence, or recommended changes that prevent progression.

The Skill ends with the verification result and governed handoff.