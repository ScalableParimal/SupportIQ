---
name: requirement-update
description: Executes the governed Requirement Update process using the repository Requirement Update Guideline, Prompt, and Request.
---

# Requirement Update Skill

## 1. Purpose

Execute the repository's governed Requirement Update process.

This Skill provides the reusable execution procedure for applying explicitly approved human decisions to an existing Requirement. It does not replace or duplicate the normative rules defined by the Requirement Update Guideline.

## 2. Governing Artifacts

Before execution, load and follow:

- `docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`
- `docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md`
- `docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md`

The Guideline is the normative authority for the Requirement Update process.

The Prompt defines the controlled invocation requirements.

The Request supplies run-specific inputs.

Do not duplicate, reinterpret, or override their instructions in this Skill.

## 3. Execution Preconditions

Before updating:

1. Load the governing Guideline, Prompt, and Request.
2. Resolve the Requirement document specified by the Request.
3. Resolve the relevant analysis findings/questions.
4. Resolve the explicit human decisions.
5. Resolve recommendations explicitly approved by the human.
6. Confirm that the decisions required for the requested update are sufficiently clear.
7. If a material decision remains unresolved or ambiguous, stop and request clarification.

Only explicitly approved human decisions may drive the Requirement Update.

## 4. Execution Procedure

Execute the following sequence:

1. Establish the current Requirement as the source document to be updated.
2. Establish the analysis findings/questions addressed by the update.
3. Establish the explicit human decisions and approved recommendations.
4. Apply only those approved decisions to the affected Requirement content.
5. Inspect related sections affected by each decision.
6. Preserve valid unrelated Requirement content.
7. Perform the consistency and validation activities required by the governing Guideline.
8. Produce the required change summary.
9. Identify remaining open questions and material assumptions.
10. Clearly state the resulting approval status.
11. Stop at the Requirement Update process boundary.

The detailed rules for applying decisions, preserving requirements, controlling scope, and validating consistency remain defined by the Guideline.

## 5. Artifact Modification Boundary

Requirement Update is the governed process that may modify the specified Requirement document when the execution context explicitly requests the update.

Modify only the designated Requirement document as the subject of the explicitly approved update. Own-output record publication does not authorize additional substantive artifact changes.

Do not modify:

- source code;
- tests;
- implementation plans;
- database schema;
- configuration;
- unrelated documentation;
- AI Guidelines;
- Prompts;
- Requests.

Do not create implementation artifacts as part of Requirement Update.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 6. Decision Boundary

The Skill may apply decisions that have already been explicitly made by the human.

It must not:

- invent requirements;
- make unresolved business decisions;
- silently interpret an ambiguous human decision;
- convert an AI recommendation into a requirement without explicit approval;
- broaden the Requirement;
- introduce unrelated implementation details.

If clarification is required, stop rather than deciding silently.

## 7. Approval Boundary

The output of Requirement Update is an updated Requirement that remains subject to the subsequent governed processes.

Requirement Update does not constitute:

- Requirement Analysis;
- Requirement Analysis Verification;
- Human Requirement Approval;
- Plan Impact Evaluation;
- Implementation Planning;
- Implementation Plan Verification;
- Human Plan Approval;
- implementation authorization.

The updated Requirement becomes the approved source of truth only after the required Human Requirement Approval.

## 8. Downstream Handoff

After Requirement Update, the governed downstream process is:

Requirement Analysis
→ Complete Requirement Analysis Verification
→ Resolve Findings / Decisions
→ Human Requirement Approval

After Human Requirement Approval, follow the applicable Plan Impact Evaluation and implementation-planning path.

Do not perform those downstream processes as part of Requirement Update.

## 9. Completion

Return:

- the updated Requirement;
- the required change summary;
- remaining open questions;
- remaining material assumptions;
- the resulting approval status.

Follow the output requirements defined by the governing Guideline and Prompt.

Do not mark the Requirement as approved.

The Skill ends after the Requirement Update output and handoff to Requirement Analysis.