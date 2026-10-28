---
name: finding-investigation
description: Executes the governed Finding Investigation process using the repository Finding Investigation Guideline, Prompt, and Request.
---

# Finding Investigation Skill

## 1. Purpose

Execute the governed Finding Investigation process defined by the repository Finding Investigation Guideline, Prompt, and Request.

This Skill provides reusable execution mechanics for investigating either an identified finding or an explicitly authorized, separately classified human-requested governance enhancement. The applicable Guideline owns the distinct subject types and report outcomes; this Skill does not redefine them.

The governing rules, investigation objectives, finding classifications, corrective-option requirements, evidence classifications, outcomes, and report requirements remain owned by the referenced Governance artifacts.

Do not duplicate or redefine those rules in this Skill.

## 2. Governing Artifacts

Read and follow:

- `docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md`
- `docs/ai/prompts/FINDING_INVESTIGATION_PROMPT.md`
- `docs/ai/request/FINDING_INVESTIGATION_REQUEST.md`

Use the current repository versions of these artifacts.

## 3. Execution Preconditions

Before beginning the investigation:

1. Read the Finding Investigation Guideline.
2. Read the Finding Investigation Prompt.
3. Read the Finding Investigation Request.
4. Identify the request subject type and its source; for an enhancement, preserve the human wording, attribution, and investigation authorization. Before execution, validate the existing Work ID reservation or collision-check the candidate against both persistence roots and publish the first actor-owned attempt record without overwrite to reserve it; do not require a prior attempt record before the first publication, and stop on any collision or authorization mismatch.
5. Identify the affected governed artifact.
6. Establish the applicable current approved source documents and their status.
7. Inspect the actual repository or relevant governed artifacts.
8. Identify available supporting evidence.
9. Establish the relevant architecture and engineering constraints.

If required source status, approval, or evidence cannot be established, record the uncertainty rather than silently selecting an alternative.

## 4. Execution Procedure

Execute the investigation using this sequence:

1. Establish the finding or separately authorized non-finding enhancement request and its source.
2. Establish the affected governed artifact and relevant context.
3. Establish the applicable current approved sources.
4. Inspect the actual affected implementation or governed artifacts.
5. For a finding, validate it under the finding classifications. For an enhancement, establish the authorized request context without manufacturing a finding or finding classification.
Steps 6 through 8 apply only to a FINDING. For an enhancement, instead establish the intended governance outcome and assess the authorized request context, affected governance artifacts, current authority and constraints, material risks, feasible change boundaries, and evidence or uncertainty; do not perform defect comparison, determine a defect difference, or assign a defect root cause.
6. Compare observed behavior with expected behavior.
7. Determine the difference.
8. Determine the root cause where evidence permits.
9. Assess impact.
10. Identify technically viable corrective options where correction is required.
11. Assess requirement, plan, architecture, testing, migration, operational, and other applicable impacts.
12. Determine whether human decision or approval is required.
13. Provide an advisory corrective recommendation where sufficient evidence exists.
14. Classify the outcome using only the subject-type-specific outcomes in the Guideline.
15. Produce the complete investigation report.
16. Determine the recommended next process.

Do not implement a correction during these steps.

## 5. Investigation Scope

Investigate the finding and the complete relevant context of the governed artifacts directly affected by it.

Use the finding source, affected artifact, approved sources, and repository context to determine the relevant scope.

Task IDs, recently changed files, corrective changes, and discovery location are context only.

Do not unnecessarily restrict investigation to those items.

Do not expand the investigation into unrelated work or redesign beyond what is necessary to understand the finding.

## 6. Source and Evidence Handling

Use the applicable approved artifact as the authoritative source for the affected subject.

Inspect actual repository artifacts where relevant.

Do not rely solely on previous AI summaries.

If sources conflict:

- identify the conflict
- preserve the conflicting evidence
- do not silently select an interpretation

Maintain explicit distinction between:

- executed evidence
- source inspection evidence
- reported evidence
- unverified information

If the investigation request explicitly permits execution, commands or tests may be used to obtain additional evidence.

Do not represent source-inspection or reported evidence as executed evidence.

## 7. Finding Validation

Determine whether the finding is supported by available evidence.

Establish:

- observed behavior
- expected behavior
- difference between them
- validity of the finding
- affected artifact
- root cause where possible

Do not assume the finding is a production-code defect.

Do not recommend corrective implementation until the finding has been sufficiently validated.

If the available evidence cannot establish the classification or root cause, record the uncertainty and identify the evidence required to continue.

## 8. Root Cause and Impact

For a valid finding, distinguish the symptom from its underlying cause.

Determine whether the cause resides in, or is materially affected by:

- implementation
- tests
- configuration
- environment
- requirement
- implementation plan
- verification
- another governed artifact or process

Assess the relevant impact without redesigning unrelated parts of the system.

## 9. Corrective Options

Where correction is required, identify only technically viable options for the current repository and approved architecture.

For each meaningful option, assess the applicable impacts defined by the governing Guideline.

Do not create unnecessary alternatives.

Do not select or authorize a corrective option on behalf of the human decision-maker when the applicable process requires human authority.

## 10. Human Decision Boundary

Assess whether the finding or proposed correction requires human decision or approval.

When the correction could materially affect a governed artifact, architecture, contract, schema, security boundary, scope, compatibility, infrastructure strategy, or another area requiring human authority, identify that requirement explicitly.

Do not implement a correction where human decision or approval is required.

Route a finding, or an established human-requested enhancement context, to Corrective Change Decision & Plan Update using its separate subject type. A recommendation remains advisory; no change is approved or authorized.

## 11. Recommendation Boundary

A corrective recommendation is advisory only.

It may identify:

- recommended option
- rationale
- expected impact
- risks
- requirement impact
- plan impact
- architecture impact
- human approval requirement

It does not authorize implementation and does not constitute human approval.

## 12. Read/Write Boundary

Finding Investigation is read-only.

Do not modify:

- source files
- tests
- requirements
- implementation plans
- configuration
- database state
- governed artifacts
- other product artifacts

Do not:

- implement corrections
- commit changes
- push changes

If execution is explicitly permitted by the Investigation Request, execute only the evidence-gathering activities necessary for the investigation.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 13. Process Boundary

This Skill performs only Finding Investigation.

It must not perform:

- Requirement Analysis
- Requirement Analysis Verification
- Requirement Update
- Implementation Planning
- Implementation Plan Verification
- Implementation
- Implementation Verification
- Implementation Review
- Corrective Change Decision & Plan Update
- Human Requirement Approval
- Human Review Approval
- Human Plan Approval
- Human Acceptance
- Commit or Push

If corrective action is required, report the Corrective Change Decision & Plan Update process as the next governed process.

## 14. Completion

Complete the process only after the investigation activities and reporting requirements defined by the governing Guideline have been performed.

Return the complete Finding Investigation report defined by the Guideline.

The report must clearly distinguish:

- finding summary
- finding source
- finding validation
- evidence
- expected behavior
- actual behavior
- root cause
- impact assessment
- corrective options
- recommended option
- human decision requirement
- remaining uncertainties
- investigation outcome
- recommended next process

The Skill ends with the investigation report.

It does not authorize corrective changes.