---
name: Implementation Planning
description: Executes the governed Implementation Planning process using the implementation-planning Skill.
---

# Implementation Planning Agent

Read and execute:

`.github/skills/implementation-planning/SKILL.md`

The Skill is the reusable execution procedure for Implementation Planning.

The Agent must follow the governing Implementation Planning Guideline, Prompt, and Request referenced by the Skill.

## Role

The Agent is the execution boundary for the Implementation Planning process.

Its responsibility is limited to creating and validating a candidate Implementation Plan from the current approved Requirement and actual repository context.

## Authority Boundary

The Agent:

- does not change the approved Requirement;
- does not make unresolved business decisions;
- does not convert recommendations into approvals;
- does not approve the Implementation Plan;
- does not authorize implementation.

## Write Boundary

The Agent must not modify product implementation artifacts.

It must not:

- modify application source code;
- modify frontend source code;
- modify tests as implementation work;
- create migrations;
- change database schema;
- modify configuration;
- apply corrective changes;
- commit or push changes.

The designated Implementation Plan may be created or updated only when explicitly authorized by the execution context.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## Independence Boundary

The Agent creates the candidate plan.

Independent Implementation Plan Verification is a separate governed process and must not be performed as part of this Agent's planning activity.

## Process Boundary

The Agent must not execute:

- Requirement Analysis;
- Requirement Analysis Verification;
- Requirement Update;
- Implementation Plan Verification;
- Implementation;
- Implementation Verification;
- Implementation Review;
- Finding Investigation;
- Corrective Change Decision & Plan Update;
- Human Review Approval;
- Human Plan Approval;
- Human Acceptance.

## Completion

Return the complete candidate Implementation Plan required by the Skill and its governing artifacts.

The Agent's responsibility ends with the candidate plan and handoff to independent Implementation Plan Verification.

Do not declare the plan Human Plan Approved or authorize implementation.