---
name: requirement-analysis
description: Executes the governed Requirement Analysis process using the repository Requirement Analysis Guideline, Prompt, and Request.
---

# Requirement Analysis Skill

## 1. Purpose

Execute the repository's governed Requirement Analysis process.

This Skill provides the reusable execution procedure for Requirement Analysis. It does not replace or duplicate the normative rules defined by the Requirement Analysis Guideline.

## 2. Governing Artifacts

Before execution, load and follow:

- `docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`
- `docs/ai/prompts/REQUIREMENT_ANALYSIS_PROMPT.md`
- `docs/ai/request/REQUIREMENT_ANALYSIS_REQUEST.md`

Authority is determined by the repository SDLC governance framework.

The Guideline is the normative authority for the process.

The Prompt defines the controlled invocation requirements.

The Request supplies run-specific inputs.

Do not duplicate, reinterpret, or override their instructions in this Skill.

## 3. Execution Preconditions

Before starting:

1. Confirm that the Requirement Analysis process has been requested.
2. Load the applicable Request.
3. Resolve the Requirement document identified by the Request.
4. Resolve the applicable human decisions and additional context supplied by the Request.
5. Confirm that the required source artifacts are accessible.
6. If required information is unavailable or cannot be reliably resolved, stop and report the limitation.

## 4. Execution Procedure

Execute the following sequence:

1. Load the governing Guideline, Prompt, and Request.
2. Establish the authoritative Requirement source.
3. Establish the applicable human decisions and contextual inputs.
4. Perform the Requirement Analysis according to the Guideline and Prompt.
5. Maintain traceability between observations and their supporting source/evidence.
6. Distinguish source-supported information from assumptions or other analysis outputs as required by the governing artifacts.
7. Produce the required Requirement Analysis output.
8. Identify the resulting process outcome and any required human decisions.
9. Stop at the Requirement Analysis process boundary.

The Skill must not independently redefine the analysis criteria. Those criteria are maintained by the Guideline.

## 5. Artifact Handling

During normal Requirement Analysis:

- Treat the source Requirement as authoritative input.
- Treat applicable human decisions as authoritative decisions once supplied.
- Treat analysis results as analysis output, not as approved requirements.
- Do not silently modify the source Requirement.
- Do not create or modify an implementation plan.
- Do not modify implementation artifacts.

If a Requirement Update is required, stop and route the work through the separate Requirement Update process defined by the SDLC governance framework.

## 6. Evidence and Traceability

Maintain sufficient traceability to show:

- which authoritative Requirement was analyzed;
- which human decisions were considered;
- which evidence or source information supports material observations;
- which items remain unresolved;
- which decisions are required before progression.

Follow the evidence and traceability requirements defined by the governing Guideline.

## 7. Process Boundary

Requirement Analysis ends when the required analysis output has been produced.

This Skill does not:

- perform Requirement Analysis Verification;
- perform Implementation Planning;
- perform Implementation Plan Verification;
- implement product changes;
- perform Implementation Verification;
- perform Implementation Review;
- investigate findings;
- decide corrective changes;
- perform Human Approval;
- perform Human Acceptance;
- commit or push changes.

The next governed process is Requirement Analysis Verification when the required prerequisites are satisfied.

## 8. Read/Write Boundary

The Requirement Analysis process is read-only with respect to governed source and product artifacts during initial analysis.

Do not modify:

- Requirement artifacts;
- implementation plans;
- source code;
- tests;
- configuration;
- repository governance artifacts.

Any required Requirement modification must use the separately governed Requirement Update process and its required human decision/approval path.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 9. Completion

Return the complete Requirement Analysis output required by the governing Guideline and Prompt.

Do not declare:

- the Requirement approved;
- the Requirement verified;
- the implementation plan approved;
- implementation authorized;
- the feature accepted.

The Skill ends after producing the Requirement Analysis result and identifying the appropriate next governed process.