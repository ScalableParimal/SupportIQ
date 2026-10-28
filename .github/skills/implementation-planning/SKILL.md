---
name: implementation-planning
description: Executes the governed Implementation Planning process using the repository Implementation Planning Guideline, Prompt, and Request.
---

# Implementation Planning Skill

## 1. Purpose

Execute the repository's governed Implementation Planning process.

This Skill provides the reusable execution procedure for creating a candidate Implementation Plan. It does not replace or duplicate the normative rules defined by the Implementation Planning Guideline.

## 2. Governing Artifacts

Before execution, load and follow:

- `docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md`
- `docs/ai/prompts/IMPLEMENTATION_PLANNING_PROMPT.md`
- `docs/ai/request/IMPLEMENTATION_PLANNING_REQUEST.md`

The Guideline is the normative authority for the planning process.

The Prompt defines the controlled invocation requirements.

The Request supplies run-specific inputs.

Do not duplicate, reinterpret, or override their instructions in this Skill.

## 3. Execution Preconditions

Before planning:

1. Load the governing Guideline, Prompt, and Request.
2. Resolve the Current Approved Requirement identified by the Request.
3. Confirm its approval status and approval evidence.
4. Resolve applicable approved technical decisions and constraints.
5. Inspect the actual repository relevant to the feature.
6. Establish the repository architecture, conventions, dependencies, and testing context required for planning.
7. If a required approval, decision, artifact, or repository context cannot be established, stop and report the limitation.

Do not proceed from an unapproved or superseded Requirement.

## 4. Execution Procedure

Execute the following sequence:

1. Establish the authoritative planning inputs.
2. Inspect the relevant repository and existing implementation context.
3. Design implementation work consistent with the approved Requirement and repository context.
4. Decompose the work into traceable implementation tasks.
5. Establish task dependencies and appropriate implementation ordering.
6. Identify affected projects, layers, contracts, persistence, API, frontend, and tests where applicable.
7. Establish the required testing and verification coverage.
8. Identify risks, dependencies, open technical decisions, and scope boundaries.
9. Maintain requirement-to-task-to-verification traceability.
10. Perform the plan validation required by the governing Guideline.
11. Produce the candidate Implementation Plan.
12. Stop at the Implementation Planning process boundary.

The detailed planning criteria and validation rules remain defined by the Guideline.

## 5. Repository Inspection

Use the actual repository as implementation context.

Inspect only the repository areas relevant to producing the plan and establishing architectural fit.

Do not assume repository patterns, dependencies, conventions, or test infrastructure without evidence from the actual repository.

Record relevant repository observations as planning context rather than silently changing the approved Requirement.

## 6. Decision Handling

Preserve the distinction between:

- approved Requirement;
- approved technical decisions or constraints;
- existing repository conventions;
- required technical consequences;
- AI recommendations;
- unresolved decisions.

Do not silently convert an AI recommendation or unresolved decision into an approved requirement or technical decision.

If a material decision is required before implementation can safely proceed, identify it as an open decision and stop at the appropriate planning boundary.

## 7. Artifact Handling

The primary output of this Skill is a candidate Implementation Plan.

The Skill may create or update the designated planning artifact when the execution context explicitly authorizes creation of that artifact.

It must not modify:

- the approved Requirement;
- product source code;
- tests;
- database schema;
- migrations;
- configuration;
- other implementation artifacts.

Planning does not constitute implementation.

## 8. Traceability

Maintain traceability between:

- approved Requirement;
- relevant business rules or contracts;
- implementation tasks;
- verification/testing coverage.

Use the traceability structure required by the governing Guideline.

Do not create new business requirements through plan task identifiers or task descriptions.

## 9. Approval Boundary

The output is a candidate Implementation Plan.

Plan creation and plan validation do not constitute:

- Implementation Plan Verification;
- Human Review Approval;
- Human Plan Approval;
- authorization to implement.

After the candidate plan is produced, the governed sequence continues through independent Implementation Plan Verification and the required human gates defined by the SDLC governance framework.

## 10. Process Boundary

This Skill performs Implementation Planning only.

It does not:

- perform Requirement Analysis;
- perform Requirement Analysis Verification;
- update requirements;
- perform Implementation Plan Verification;
- implement product changes;
- perform Implementation Verification;
- perform Implementation Review;
- investigate findings;
- decide corrective changes;
- perform Human Review Approval;
- perform Human Plan Approval;
- perform Human Acceptance;
- commit or push changes.

## 11. Read/Write Boundary

Implementation Planning is read/analyze/design activity with respect to product implementation artifacts.

Do not implement planned tasks.

Do not create migrations, change database schema, modify application behavior, or modify frontend/backend source code as part of planning.

The designated planning artifact may be produced or updated only when explicitly authorized by the execution context. The process may additionally publish its own governed output records under section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. This does not authorize modification of approved upstream artifacts, another process's records, or substantive human decisions, and does not permit editing published final records in place.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 12. Completion

Return the complete candidate Implementation Plan and the required planning output defined by the governing Guideline and Prompt.

The completion output must identify the resulting plan status and the governed next process.

Do not mark the plan as Human Plan Approved.

The Skill ends with the candidate Implementation Plan and handoff to independent Implementation Plan Verification.