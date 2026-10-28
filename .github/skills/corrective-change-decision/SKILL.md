---
name: corrective-change-decision
description: Executes the governed Corrective Change Decision and Plan Update process using the repository Corrective Change Guideline, Prompt, and Request.
---

# Corrective Change Decision & Plan Update Skill

## 1. Purpose

Execute the governed Corrective Change Decision & Plan Update process defined by the repository Corrective Change Guideline, Prompt, and Request.

This Skill provides reusable execution mechanics for either evaluating an investigated finding or deciding how to handle a separately authorized human-requested governance enhancement as a non-finding, including exact proposal preparation and its Human Approval boundary.

The governing rules, decision statuses, plan-change criteria, approval requirements, evidence classifications, and report requirements remain owned by the referenced Governance artifacts.

Do not duplicate or redefine those rules in this Skill.

## 2. Governing Artifacts

Read and follow:

- `docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md`
- `docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md`
- `docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md`

Use the current repository versions of these artifacts.

## 3. Execution Preconditions

Before beginning the decision process:

1. Read the Corrective Change Guideline.
2. Read the Corrective Change Prompt.
3. Read the Corrective Change Request.
4. Establish whether the request subject is a finding or an explicitly authorized non-finding governance enhancement; preserve its source and scope.
5. Identify the affected governed artifact.
6. Establish the current approved Requirement where applicable.
7. Establish the current approved Implementation Plan where applicable.
8. Establish the applicable Finding Investigation result for the selected subject type.
9. Identify applicable architecture and engineering guidelines.
10. Inspect relevant repository and evidence context.

Confirm the current version, status, and approval evidence of applicable governed artifacts.

If essential information cannot be established, record the uncertainty rather than silently selecting a source.

## 4. Execution Procedure

Execute the decision process using this sequence:

1. Establish the finding or separate human-requested enhancement subject and its source.
2. Establish the affected governed artifact.
3. Establish the applicable approved Requirement and Implementation Plan.
4. Review the Finding Investigation and supporting evidence.
5. For a finding, determine its finding disposition. For an enhancement, use only the separate enhancement decision statuses; never accept/reject a nonexistent finding.
6. Determine the corrective direction.
7. Determine which governed artifact requires correction, if any.
8. Determine whether the current Implementation Plan remains valid.
9. Determine whether a plan update is required.
10. Identify the required artifact or plan changes.
11. Prepare a precise proposed amendment where a plan change is required.
12. Determine whether human approval is required.
13. Establish implementation readiness.
14. Identify the governed next process.
15. Produce the complete decision report.

Do not implement corrective changes during this process.

## 5. Decision Boundary

Evaluate the finding using the applicable approved Requirement, current approved Implementation Plan, Finding Investigation, repository state, and available evidence.

The decision must explicitly establish:

- finding disposition
- or, for an enhancement, its distinct non-finding disposition
- affected artifact
- corrective direction
- plan validity
- plan-change requirement
- required artifact or plan changes
- human approval requirement
- next process

Do not assume that every finding requires a code change.
A human-requested enhancement is not a finding. Proposal-preparation authorization permits preparation only within its stated scope; it never constitutes approval or authority to apply. Any material governance patch remains unapproved until exact Human Approval and explicit scoped application authority; independent verification and the complete Governance Audit remain required.

Do not silently alter the Requirement, Implementation Plan, implementation scope, or architecture.

## 6. Plan Impact Assessment

Determine whether the proposed corrective direction affects the current approved Implementation Plan.

Use the controlled implementation details defined by the governing Guideline as the basis for this assessment.

If the approved plan remains sufficient, preserve it as the current approved plan.

If the plan must change:

1. Identify affected tasks and dependencies.
2. Identify affected acceptance criteria.
3. Identify affected architecture or implementation approach.
4. Identify affected scope and constraints.
5. Identify testing and verification impact.
6. Prepare the precise proposed amendment.
7. Preserve traceability to the finding and investigation.

Do not apply the proposed amendment without the required human approval.

## 7. Proposed Plan Amendment

When a plan update is required, prepare only the minimum necessary amendment.

Preserve the existing approved plan and its history.

The proposed amendment must make the relationship between the finding, investigation, corrective decision, and changed plan elements explicit.

Do not mark the revised plan as approved.

Do not treat the proposed amendment as the current approved Implementation Plan.

## 8. Other Governed Artifact Changes

If the affected artifact is not the Requirement or Implementation Plan:

1. Identify the affected artifact.
2. Identify the applicable governed correction process.
3. Describe the proposed correction where required.
4. Determine the required human approval.
5. Do not apply the correction in this Skill.

The current approved Implementation Plan remains authoritative unless the corrective decision explicitly determines that it must change.

## 9. Requirement Change Boundary

If the corrective decision determines that the Requirement must change:

1. Identify the requirement impact.
2. Do not modify the Requirement in this process.
3. Route the change through the governed Requirement Update process.
4. Identify the resulting downstream Requirement Analysis, Verification, approval, and planning processes required by the governing rules.

Do not implement against an unresolved or unapproved requirement change.

## 10. Human Approval Boundary

Determine whether human approval is required using the governing Guideline.

When the decision affects a controlled artifact or material design decision requiring human authority, explicitly identify the required approval.

When uncertain whether a decision is material, use the human-approval path defined by the governing Guideline.

A recommendation is advisory only.

Do not:

- claim human approval
- mark a proposed plan as approved
- proceed as though approval was granted
- silently expand scope

## 11. Read/Write Boundary

The decision process is read-only with respect to implementation and governed artifacts unless the process is explicitly operating in a proposal-generation context.

Do not:

- modify source code
- modify tests
- modify configuration
- create migrations
- execute corrective implementation
- silently change requirements
- silently modify the approved Implementation Plan

A proposed plan amendment may be produced as an explicit proposal.

Do not apply it to the approved plan until the required human approval has been explicitly received.

The restrictions in this section do not prohibit publication of this process's own governed output records. Follow section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md within the explicitly designated record scope. This limited permission covers the process's own invocation metadata, checkpoints, required report, result bindings, and permitted evidence or gate records; it does not permit changes to approved upstream artifacts, another process's records, or substantive human decisions. Published final records must not be edited in place. Establish required execution context before starting and publish the terminal record only when its recorded termination or completion is established. All other write, process, independence, approval, and acceptance restrictions remain in force.

## 12. Evidence Handling

Maintain explicit distinction between:

- executed evidence
- source inspection evidence
- reported evidence
- unverified information

Do not represent reported or unverified evidence as executed evidence.

If evidence is incomplete or conflicting:

- identify the conflict
- explain its impact
- do not silently resolve it
- request clarification or additional evidence when necessary

## 13. Corrective Implementation Boundary

This Skill does not implement corrective changes.

A corrective implementation may proceed only after the applicable governed artifact changes and required human approvals have been completed.

Corrective implementation must use the current approved Implementation Plan.

Never direct implementation against an unapproved plan or informal corrective recommendation.

## 14. Traceability

Maintain the corrective chain:

Requirement
→ Approved Plan
→ Implementation
→ Finding
→ Finding Investigation
→ Corrective Decision
→ Revised Plan where applicable
→ Corrective Implementation
→ Verification
→ Review
→ Human Acceptance

Preserve the reason and evidence for any approved plan change.

## 15. Process Boundary

This Skill performs only Corrective Change Decision & Plan Update.

It must not perform:

- Requirement Analysis
- Requirement Analysis Verification
- Requirement Update
- Implementation Planning
- Implementation Plan Verification
- Implementation
- Implementation Verification
- Implementation Review
- Finding Investigation
- Human Requirement Approval
- Human Review Approval
- Human Plan Approval
- Human Acceptance
- Commit or Push

If another process is required, identify it as the next governed process rather than executing it within this Skill.

## 16. Completion

Complete the process only after the decision activities and reporting requirements defined by the governing Guideline have been performed.

Return the complete Corrective Change Decision & Plan Update report defined by the Guideline.

The report must clearly identify:

- decision status
- finding summary
- investigation result
- corrective decision
- plan-change requirement
- plan impact
- proposed plan amendment where applicable
- human approval requirement
- implementation readiness
- next process

The Skill ends with the corrective decision report.

It does not authorize or execute corrective implementation.