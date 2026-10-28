# Corrective Change Decision & Plan Update Guidelines

## 1. Purpose

This guideline defines the process for deciding how to handle a finding and determining whether a governed artifact requires corrective change before the affected downstream process continues.

This process determines how to handle a finding identified during verification or review of an approved requirement, implementation plan, implementation, or other governed artifact.
This process also provides a separate, non-finding route for an explicitly human-requested governance enhancement when its investigation result establishes the request context. The enhancement route does not reclassify or replace any finding, finding disposition, Requirement, or Implementation Plan.

Its responsibility is to:

- evaluate the finding and its source
- determine the corrective direction
- identify which artifact requires correction
- determine whether the approved implementation plan must change
- identify required plan changes
- prepare the proposed artifact or plan changes when required
- establish the human approval gate
- identify the next process

This process does NOT implement code or other corrective changes.

---

## 2. Core Principle

A corrective implementation must always be performed against the current approved implementation plan.

Never implement a corrective change directly from:

- an investigation recommendation
- an AI suggestion
- a review comment
- an informal discussion
- an unapproved plan modification

If the corrective decision changes the approved implementation approach, scope, architecture, task breakdown, acceptance criteria, or other controlled implementation details, the implementation plan must be updated and approved before implementation begins.

---

## 3. Source of Truth

Use the following sources in this order:

1. Approved Requirement
2. Current Approved Implementation Plan
3. Relevant Architecture / Engineering Guidelines
4. Finding Investigation
5. Actual Repository State
6. Verification / Test Evidence
7. Additional context explicitly supplied by the user

The requirement remains the authoritative source for what the feature must do.

The implementation plan defines the currently approved way to implement that requirement.

A finding does not automatically change either one.

---

## 4. Scope

This process covers:

- corrective decision
- plan-impact assessment
- plan amendment
- task changes
- acceptance-criteria changes
- implementation approach changes
- architecture-impact assessment
- human approval determination
- traceability

This process does NOT cover:

- writing production code
- writing corrective tests
- executing implementation
- executing verification
- final implementation review
- final human acceptance

Those activities belong to subsequent processes.

---

## 5. Inputs

Required inputs:

- Finding Source
- Affected Artifact
- Affected Components / Sections
- Approved Requirement, where applicable
- Current Approved Implementation Plan, where applicable
- Finding Investigation
- Relevant Architecture / Engineering Guidelines
For HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING), use the separate request inputs in the Corrective Change Request: stable enhancement request identity if assigned; verbatim human request and attribution; explicit human authorization for the proposal scope; affected governance artifacts; and the Finding Investigation report establishing this non-finding context. Do not invent a Finding Source, Finding ID, finding disposition, approved Requirement, or approved Implementation Plan for this route.

Optional inputs:

- actual implementation state
- test results
- verification results
- additional evidence
- previous corrective decisions
- additional context

If essential information is missing, do not invent it.

Report the missing information and identify what is required.

---

## 6. Finding Source and Affected Artifact

A finding may originate from:

- Requirement Analysis Verification
- Implementation Plan Verification
- Implementation Verification
- Implementation Review
- Other explicitly approved quality-review processes

The corrective process must identify the source of the finding before determining the corrective action.

The process must also identify which governed artifact is affected.

Potential affected artifacts include:

- Requirement
- Requirement Analysis
- Implementation Plan
- Implementation
- Tests
- Configuration
- Documentation
- Other explicitly governed artifacts

The corrective decision must not assume that every finding requires a code change.

Examples:

### Requirement Finding

Requirement Analysis Verification identifies ambiguity or missing information in the requirement.

Corrective path:

Finding
→ Investigation
→ Corrective Change Decision
→ Requirement Update
→ Requirement Analysis
→ Requirement Analysis Verification
→ Human Requirement Approval
→ Implementation Planning

### Plan Verification Finding

Implementation Plan Verification identifies an issue in the implementation plan.

Corrective path:

Finding
→ Investigation
→ Corrective Change Decision & Plan Update
→ Human Approval
→ Apply Approved Plan Update
→ Complete Implementation Plan Verification
→ Resolve Findings / Decisions
→ Human Review Package
→ Human Review Approval
→ Human Plan Approval

### Implementation Verification Finding

Implementation Verification identifies an implementation defect.

Corrective path:

Finding
→ Investigation
→ Corrective Change Decision & Plan Update
→ Human Approval
→ Implementation
→ Implementation Verification
→ Implementation Review

### Implementation Review Finding

Implementation Review identifies a material technical quality issue.

Corrective path:

Finding
→ Investigation
→ Corrective Change Decision & Plan Update
→ Update Plan if required
→ Human Approval
→ Implementation
→ Implementation Verification
→ Implementation Review

---

## 7. Corrective Decision

Evaluate the finding, its source, the affected artifact, and the Finding Investigation result.

Determine one of the following:

### 7.1 Finding Rejected

The finding is not a valid problem.

No corrective implementation or artifact change is required.

### 7.2 Finding Accepted — No Corrective Change Required

The finding is valid, but no change to a governed artifact is required.

Proceed using the applicable current approved artifact.

### 7.3 Finding Accepted — Corrective Change Required

The finding is valid and correcting it requires changing one or more governed artifacts.

Determine the affected artifact and the applicable corrective process.

When the affected artifact is neither the Requirement nor the Implementation Plan, the Decision Status is `FINDING ACCEPTED — OTHER GOVERNED ARTIFACT CHANGE REQUIRED`.

### 7.4 Requirement Change Required

The finding exposes ambiguity, contradiction, missing information, or an incorrect requirement.

Do not modify the implementation plan or implementation until the requirement is updated and approved through the requirement process.

### 7.5 Plan Change Required

The finding is valid and correcting it requires changing the approved implementation plan.

The plan must be amended and approved before implementation proceeds.

### 7.6 Additional Evidence Required

The available evidence is insufficient to make a reliable corrective decision.
HUMAN-REQUESTED ENHANCEMENT — PROPOSAL REQUIRED: Use only when the request is explicitly human-originated, the proposal-preparation authorization and scope are evidenced, and the investigation establishes the non-finding enhancement context. It means a precise governance proposal is prepared or required for Human Approval. It does not mean the enhancement is accepted as policy, approved, applied, or authorized for implementation. Do not assign a finding ID or disposition. HUMAN-REQUESTED ENHANCEMENT — NO CHANGE RECOMMENDED: The separately authorized enhancement was evaluated and no governed change is recommended; this is not a finding disposition and does not imply approval. HUMAN-REQUESTED ENHANCEMENT — NOT ADMITTED: The request lacks attributable human provenance, scope, or authorization required for this route, or is otherwise outside its stated scope. State the specific blocker and do not convert it into a finding. Use ADDITIONAL EVIDENCE REQUIRED where a remediable evidence gap prevents determination.

Do not proceed with corrective implementation or artifact modification.

---

## 8. Determine Whether the Plan Must Change

Assess whether the corrective decision changes any of the following:

- implementation scope
- task breakdown
- task dependencies
- architecture
- project/layer responsibility
- API contract
- database schema
- persistence strategy
- security model
- integration approach
- external dependencies
- performance strategy
- acceptance criteria
- testing strategy
- deployment/infrastructure approach
- files/components explicitly governed by the plan
- constraints or exclusions
- implementation sequence

If none of these change and the correction is already covered by the approved plan:

> Plan Change Required = NO

If one or more change:

> Plan Change Required = YES

Do not change the plan merely for cosmetic reasons.

---

## 9. Plan Amendment Rules

Not every finding requires an implementation plan change.

Determine whether the corrective action affects the currently approved implementation plan.

A plan update is required when the corrective decision changes any controlled implementation detail, including:

- implementation scope
- task breakdown
- task dependencies
- architecture
- project/layer responsibility
- API contract
- database schema/data model
- security
- integrations
- performance strategy
- acceptance criteria
- testing strategy
- deployment/infrastructure approach
- implementation approach
- constraints or exclusions

For findings originating from Implementation Plan Verification, the normal corrective path is to update the plan and then run the complete Implementation Plan Verification process again before Human Plan Approval.

For findings originating after implementation, the plan should be updated when the corrective implementation changes the approved implementation approach or other controlled plan elements.

When a plan change is required, preserve the original approved plan and modify only what is necessary.

The revised plan should explicitly record:

### Finding

What finding triggered the change.

### Investigation Result

What Finding Investigation established.

### Corrective Decision

What decision was made.

### Reason

Why the approved plan is no longer sufficient.

### Changed Tasks

Identify:

- existing task IDs affected
- new task IDs, if required
- removed tasks, if any
- modified task descriptions

Do not renumber existing tasks unnecessarily.

Qualify affected tasks by source and target Plan references. Provide the master-required dispositions for completed, partial, and pending work, including retained implementation with evidence, rework-required work, replaced or removed tasks, dependency effects, and unresolved impact. Distinguish a proposed target Plan from the resulting approved Plan.

### Changed Acceptance Criteria

Document any changed or additional acceptance criteria.

### Changed Architecture / Approach

If applicable, explicitly describe the changed technical approach.

### Changed Scope

Document any change to implementation scope.

### Constraints

Document new constraints or exclusions introduced by the corrective decision.

### Verification Impact

Identify affected previous verification and review reports, their current applicability or unresolved applicability, and the required complete verification and review processes. Retained implementation does not preserve a current verification claim against a changed approved baseline.

---

## 10. Preserve Traceability

The corrective chain must remain traceable:

Requirement
→ Approved Plan
→ Implementation
→ Finding
→ Finding Investigation
→ Corrective Decision
→ Revised Plan
→ Corrective Implementation
→ Verification
→ Review
→ Human Acceptance

Do not overwrite history in a way that loses why the plan changed.

---

## 11. Human Approval Gate

Human approval is required before proceeding when the corrective decision changes a controlled artifact or material decision, including:

- requirement interpretation
- requirement scope
- implementation scope
- implementation plan
- architecture
- API contract
- database schema/data model
- security
- external integrations
- production behavior
- backward compatibility
- infrastructure
- performance strategy
- other material design decisions

When a requirement change is required, follow the requirement update and approval process.

When an implementation plan change is required, follow the plan amendment, verification, and approval process.

For a plan amendment, the required Human Approval before application authorizes only the specifically approved plan change. After the approved amendment is applied, complete Implementation Plan Verification is performed, and findings and decisions are resolved, Human Review Approval is required; it authorizes only progression to separate Human Plan Approval. Separate Human Plan Approval is then required before implementation. These approvals are distinct; neither substitutes for the other, and Human Review Approval does not replace the Human Approval required before applying a corrective change.

For straightforward corrections already covered by the current approved plan, a new plan approval may not be required.

When uncertain whether a decision is material:

> Require human approval.

The AI may recommend a corrective direction but must not represent that recommendation as approved.

---

## 12. Recommendation vs Approval

The AI may:

- recommend a corrective option
- explain trade-offs
- identify risks
- propose plan changes

The AI must not:

- claim human approval
- mark the revised plan as approved
- proceed as though approval was granted
- silently change requirements
- silently expand implementation scope

Approval must come from the human decision-maker.

---

## 13. Corrective Options

When multiple valid corrective approaches exist, document them.

For each option include:

- approach
- affected components
- plan impact
- benefits
- risks
- testing impact
- operational impact
- compatibility impact

Options may be ranked against explicit decision criteria supplied by the user or established by an applicable approved governing source. State the criteria, supporting evidence, assumptions, and relevant trade-offs. Distinguish factual comparisons from value judgments. If the applicable criteria are absent, ambiguous, or conflicting, do not rank the options; describe the options and request the required human decision. Any ranking or recommendation is advisory only. It is not a human decision, approval, or authorization to apply a change.

---

## 14. Read-Only Boundary

During decision analysis, do not:

- modify source code
- modify tests
- modify configuration
- create migrations
- execute corrective implementation
- change the requirement
- modify the implementation plan without explicitly treating it as a proposed amendment

If the process is operating in a proposal-only mode, produce the proposed plan amendment for human approval.
Do not modify the approved Implementation Plan or apply the plan amendment until the required human approval has been explicitly received.

---

## 15. Evidence Classification

Clearly distinguish:

### Executed Evidence

Evidence produced by executing a command or analysis during the current process.

Examples:

- build or test output
- static-analysis output
- dependency-analysis tool output

Reading or inspecting repository files, repository structure, source code, configuration, documentation, or dependency manifests is Source Inspection Evidence, even when performed during the process.

### Source Inspection Evidence

Evidence obtained by inspecting existing files, code, configuration, documentation, repository structure, or dependency manifests.

### Reported Evidence

Evidence supplied by the user or another process.

### Unverified

Information that has not been independently verified.

Do not present reported or unverified evidence as executed evidence.

Classify each evidence item according to how it was obtained. If both source inspection and tool execution contribute evidence, classify the resulting items separately.

---

## 16. Uncertainty

If evidence is incomplete or conflicting:

- identify the conflict
- explain its impact
- do not silently resolve it
- request clarification or additional evidence when necessary

Do not invent missing requirements, implementation decisions, or approval decisions.

---

## 17. Required Decision Report

The final report must contain the fields below with applicability determined by subject type. For FINDING, report the finding fields as finding-specific and the plan fields according to actual plan applicability. For HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING), do not report or imply a finding disposition; identify the enhancement request in the Investigation Result instead of a Finding Summary, and mark Finding Summary as not applicable. Mark Plan Change Required, Plan Impact, and Proposed Plan Amendment not applicable unless an applicable approved Implementation Plan is established; never invent a finding, Requirement, or approved Plan to fill these fields.

### 1. Decision Status

One of:

- FINDING REJECTED
- FINDING ACCEPTED — NO PLAN CHANGE REQUIRED
- FINDING ACCEPTED — PLAN CHANGE REQUIRED
- FINDING ACCEPTED — OTHER GOVERNED ARTIFACT CHANGE REQUIRED
- REQUIREMENT CLARIFICATION REQUIRED
- ADDITIONAL EVIDENCE REQUIRED
- HUMAN-REQUESTED ENHANCEMENT — PROPOSAL REQUIRED
- HUMAN-REQUESTED ENHANCEMENT — NO CHANGE RECOMMENDED
- HUMAN-REQUESTED ENHANCEMENT — NOT ADMITTED

FINDING ACCEPTED — NO PLAN CHANGE REQUIRED means the finding is valid, no governed artifact requires change, and the current approved artifacts remain in force. FINDING ACCEPTED — OTHER GOVERNED ARTIFACT CHANGE REQUIRED means the finding is valid, a governed artifact other than the Requirement or Implementation Plan requires correction, and the current approved plan is unaffected; the Corrective Decision must identify the affected artifact and the proposed correction. FINDING ACCEPTED — PLAN CHANGE REQUIRED remains the status where the approved Implementation Plan must change; any other affected artifact is then identified in the Corrective Decision.

### 2. Finding Summary

Short description of the finding.

### 3. Investigation Result

Summary of the Finding Investigation conclusion.
For an enhancement, identify the separate non-finding investigation result, human request/attribution, authorization scope, and evidence. State No finding asserted and do not use finding-acceptance language.

### 4. Corrective Decision

Clearly describe the proposed corrective direction.

### 5. Plan Change Required

YES / NO

### 6. Plan Impact

Describe affected:

- tasks
- acceptance criteria
- architecture
- scope
- dependencies
- testing
- verification

### 7. Proposed Plan Amendment

If required, provide the exact proposed changes.

### 8. Human Approval Required

YES / NO

Explain why.
A material governance enhancement always requires explicit Human Approval of the exact proposed text/patch, exact target paths and base fingerprints, and scope before application. A proposal-preparation authorization is not that approval. Approval does not itself establish an application actor.

For FINDING ACCEPTED — OTHER GOVERNED ARTIFACT CHANGE REQUIRED, Human Approval is required before the correction is applied.

### 9. Implementation Readiness

One of:

- READY FOR IMPLEMENTATION
- WAITING FOR PLAN APPROVAL
- WAITING FOR REQUIREMENT CLARIFICATION
- WAITING FOR ADDITIONAL EVIDENCE
- WAITING FOR GOVERNANCE CHANGE APPROVAL
- WAITING FOR APPLICATION AUTHORITY DESIGNATION
- WAITING FOR AUTHORIZED APPLICATION
- WAITING FOR INDEPENDENT VERIFICATION
- WAITING FOR COMPLETE GOVERNANCE AUDIT

Implementation readiness and the next-process recommendation must identify the exact outstanding gate, decision, evidence, or source update, together with the safe continuation boundary after it is resolved. Persist links to the original finding, investigation, proposed correction, approval request, and resulting records under the common execution contract. A pending or approved proposal must not be treated as an applied change.

### 10. Next Process

Identify the next process.

Normally:

- Existing Implementation Process
- Requirement Clarification
- Finding Investigation
- Additional Evidence Collection

---

## 18. Next Process Rules

### Finding Rejected

Stop the corrective workflow.

### No Corrective Change Required

Return to the applicable downstream process using the current approved artifacts.

### Other Governed Artifact Change Required

1. Identify the affected artifact and the applicable corrective process.
2. Prepare the exact proposed correction.
3. Obtain the required Human Approval before the correction is applied.
4. Apply only the approved correction through that artifact’s governed process.
5. Perform the applicable verification of the changed artifact.
6. Return to the applicable downstream process using the current approved artifacts.

### Requirement Change Required

1. Route the change through the Requirement Update process.
2. Perform Requirement Analysis / refresh the analysis after the Requirement Update against the resulting updated Requirement.
3. Run complete Requirement Analysis Verification.
4. Resolve any remaining findings or decisions.
5. Obtain Human Requirement Approval.
6. Re-evaluate the implementation plan against the newly approved requirement.
7. Run Implementation Plan Verification when required, and resolve any required findings and decisions.
8. Obtain Human Review Approval where plan verification applies; it authorizes only progression to Human Plan Approval.
9. Obtain separate Human Plan Approval before implementation.

### Plan Change Required

1. Prepare the proposed implementation-plan amendment.
2. Obtain required human approval.
3. Apply the approved plan amendment through the governed plan-update process.
4. Run complete Implementation Plan Verification again.
5. Resolve any remaining findings and decisions.
6. Prepare the Human Review package.
7. Obtain Human Review Approval, which authorizes only progression to Human Plan Approval.
8. Obtain separate Human Plan Approval.
9. Proceed to Implementation.

### Implementation Verification or Implementation Review Finding

If the corrective decision requires implementation changes:

1. Update the implementation plan if required.
2. Obtain required human approval.
3. Implement against the current approved plan.
4. Run complete Implementation Verification again.
5. Run Implementation Review again.
6. Proceed to Human Acceptance when ready.

### Additional Evidence Required

Obtain the required evidence before making the corrective decision.
For a human-requested governance enhancement: (1) preserve it as a non-finding and use only the three enhancement-specific decision statuses; (2) require the Work ID to be reserved under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 30.1 before investigation or invocation; (3) prepare an exact, hash-bound proposal only within the human-authorized scope; (4) obtain explicit interactive Human Approval binding the canonical proposal report, exact content, target paths, base/expected-after SHA-256 fingerprints, scope, exclusions, application route, and all four distinct actor identities (preparer, initial applier, verifier, reviewer); (5) for initial application, require Human Approval to designate an expressly identified one-time applier, but do not require a separate pre-existing runtime qualification record: the fresh Application attempt may be the first qualification-evidence record and must contain integrity-checked current identity, permissions, own-record publication, and role-specific capability evidence for exact-target write, read, hash/check, and readback before any source write; Human Approval or designation alone is not capability evidence, and any missing or uncertain capability requires `CANNOT COMPLETE`; apply the universal current-invocation evidence requirement in SDLC_ARTIFACT_GOVERNANCE.md section 33.1 to every other actor in their own attempt, preserving role-specific capability, independence, fresh stage-start, and read-only constraints; (6) require a fresh human stage-start instruction and separate actor-owned invocation for Application, Verification, Review, and Governance Audit; no stage-start response is patch approval, no patch approval starts a process, and no agent initiates the next stage automatically; (7) stop before source writes on any missing capability or base mismatch, and preserve exact partial-state evidence if an application write fails; (8) require independent read-only Verification and Review by actors distinct from preparer and applier and from each other; (9) run the complete Governance Audit over 52 core artifacts and seven separately reported mechanism groups using the defined evidence matrix; and (10) declare effective only on `CONSISTENT`, zero Critical/High/Medium/Low/Ambiguities/Missing Governance Controls/Unsupported Governance Controls/Broken References, and all seven groups assessed without unresolved issues. For Master changes, separately adopt the exact prospective baseline only after all preceding gates pass. For non-Master changes, effectiveness follows those gates without baseline adoption. The existing product Orchestrator scope and initiation rules remain unchanged. This route authorizes no product change.

---

## 19. Critical Rule

A corrective implementation must always be performed against the current approved implementation plan.

Therefore:

> Never implement a corrective change against an unapproved plan.

If the corrective decision changes the requirement:

> Requirement Update
> → Requirement Analysis
> → Complete Requirement Analysis Verification
> → Resolve Findings / Decisions
> → Human Requirement Approval
> → Plan Evaluation
> → Implementation Planning / Plan Update as required
> → Implementation Plan Verification as required
> → Resolve Findings / Decisions as required
> → Human Review Approval as required
> → Human Plan Approval
> → Implement

If the corrective decision changes the implementation plan:

> Plan Update
> → Human Approval
> → Complete Implementation Plan Verification
> → Resolve Findings / Decisions
> → Human Review Package
> → Human Review Approval
> → Human Plan Approval
> → Implement

If the corrective decision does not change the approved plan:

> Implement using the existing approved plan.

After a corrective implementation:

> Complete Implementation Verification
> → Implementation Review
> → Human Acceptance

The corrective decision process must not bypass the applicable verification or human approval gate.

If another governed artifact is affected, follow the applicable governed process for that artifact before proceeding to the affected downstream process.