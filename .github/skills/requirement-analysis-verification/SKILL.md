---
name: requirement-analysis-verification
description: Executes the governed Requirement Analysis Verification process using the repository Requirement Analysis Verification Guideline, Prompt, and Request.
---

# Requirement Analysis Verification Skill

## 1. Purpose

Execute the repository's governed Requirement Analysis Verification process.

This Skill provides the reusable execution procedure for independently verifying the current Requirement Analysis. It does not replace or duplicate the normative rules defined by the Requirement Analysis Verification Guideline.

## 2. Governing Artifacts

Before execution, load and follow:

- `docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md`
- `docs/ai/prompts/REQUIREMENT_ANALYSIS_VERIFICATION_PROMPT.md`
- `docs/ai/request/REQUIREMENT_ANALYSIS_VERIFICATION_REQUEST.md`

The Guideline is the normative authority for the verification process.

The Prompt defines the controlled invocation requirements.

The Request supplies run-specific inputs.

Do not duplicate, reinterpret, or override their instructions in this Skill.

## 3. Execution Preconditions

Before starting:

1. Load the governing Guideline, Prompt, and Request.
2. Resolve the authoritative Source Requirement.
3. Resolve the current Requirement Analysis to be verified.
4. Resolve the resulting Updated Requirement when applicable.
5. Resolve applicable human decisions and approved constraints.
6. Resolve relevant previous verification/review results and reported evidence when supplied.
7. Confirm that the required artifacts are accessible.
8. If the complete current verification context cannot be established, stop and report the limitation.

## 4. Execution Procedure

Execute the following sequence:

1. Establish the complete current verification scope.
2. Load the authoritative source artifacts and applicable evidence.
3. Independently evaluate the current Requirement Analysis against those sources.
4. Maintain traceability between verification observations and supporting evidence.
5. Record material findings according to the classifications and severity defined by the governing Guideline.
6. Identify required human decisions or additional evidence where applicable.
7. Produce the complete verification report required by the governing Guideline and Prompt.
8. Determine the governed verification outcome.
9. Stop at the Requirement Analysis Verification process boundary.

Verification must cover the complete current Requirement Analysis rather than only recently changed sections.

## 5. Independence

The verification must independently evaluate the current Requirement Analysis.

Do not treat the conclusions of the Requirement Analysis as verified merely because they were produced by the Requirement Analysis process.

Do not modify the analysis while verifying it.

Any correction must be reported as a finding or recommendation and routed through the applicable governed corrective process.

## 6. Artifact Handling

Treat the following as distinct inputs:

- Source Requirement;
- resulting Updated Requirement, when applicable;
- current Requirement Analysis;
- applicable human decisions;
- approved constraints;
- available evidence.

Do not silently reconcile contradictions between these artifacts.

Where a material issue requires a governed change, identify the issue and route it through the applicable finding and corrective-change process.

## 7. Evidence and Traceability

Maintain sufficient traceability to show:

- what was verified;
- which source or evidence supports the verification;
- what was found;
- the affected artifact or area;
- the impact and confidence where required;
- what corrective action or decision is recommended.

Follow the evidence classification and traceability requirements defined by the governing Guideline.

## 8. Read/Write Boundary

Requirement Analysis Verification is read-only.

The Agent/Skill must not:

- modify the Requirement;
- modify the Requirement Analysis;
- create or modify an Implementation Plan;
- modify product source code;
- modify tests or configuration;
- apply corrective changes;
- approve or accept artifacts;
- commit or push changes.

Recommendations are observations for the applicable governed process; they are not authorization to change artifacts.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 9. Process Boundary

This Skill performs Requirement Analysis Verification only.

It does not:

- perform Requirement Analysis;
- update requirements;
- perform Implementation Planning;
- perform Implementation Plan Verification;
- implement product changes;
- perform Implementation Verification;
- perform Implementation Review;
- investigate findings;
- decide corrective changes;
- perform Human Requirement Approval;
- perform Human Plan Approval;
- perform Human Acceptance;
- commit or push changes.

If a material finding requires investigation or corrective action, stop at the verification result and route it through the applicable governed process.

## 10. Completion

Return the complete Requirement Analysis Verification output required by the governing Guideline and Prompt.

The result may identify verification findings, gaps, decisions, evidence requirements, or readiness.

Do not declare the Requirement approved or accepted.

Do not convert verification recommendations directly into Requirement, Plan, or implementation changes.

The Skill ends with the verification result and the appropriate governed handoff.