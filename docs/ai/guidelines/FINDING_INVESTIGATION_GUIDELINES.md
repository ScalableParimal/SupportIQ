# Finding Investigation Guidelines

## 1. Purpose

Finding Investigation determines whether an identified finding is valid, why it exists, what impact it has, and what corrective options are available.

It is an analytical and read-only process performed after a finding has been identified by:

- Requirement Analysis Verification
- Implementation Plan Verification
- Implementation Verification
- Implementation Review
- testing
- another approved engineering activity

Finding Investigation may apply to findings affecting:

- Requirement
- Requirement Analysis
- Implementation Plan
- Implementation
- Tests
- Configuration
- Documentation
- other governed artifacts

Finding Investigation does not implement corrections or modify governed artifacts.
In addition to findings, this process may investigate a separately identified human-requested governance enhancement as a non-finding only when the request explicitly records the human source, verbatim request, and authorization to investigate it. Keep the finding and enhancement tracks separate: an enhancement is not a defect, finding, false positive, or finding-disposition substitute. The finding classifications and outcomes below apply only to the finding track.

Its output provides the information required for the next corrective decision.

---

## 2. Source of Truth

Use the following sources when applicable:

1. Current approved requirement — functional source of truth
2. Current approved implementation plan — implementation-scope source of truth
3. Current approved requirement analysis or verification results — analysis/verification context where applicable
4. Approved architecture and engineering guidelines — technical constraints
5. Actual repository — implementation source of truth
6. Finding evidence — source of the reported problem
7. Relevant test/build/runtime evidence
8. Previous approved decisions related to the affected artifact
9. Current approved corrective decisions or revised plans, if applicable

The applicable source of truth depends on the affected artifact.

When the actual repository or approved source documents are available, do not rely solely on previous AI summaries.

If sources conflict, identify the conflict rather than silently choosing an interpretation.

---

## 3. Investigation Scope

Investigate the finding specified in the request and the complete relevant context of each artifact directly affected by it. Determine investigation scope from the finding’s source and governing process. For an SDLC Governance Audit finding, remain within the defined Governance Audit scope and inspect related Governance artifacts only as needed to establish context, authority, dependencies, and impact. For a product SDLC finding, remain within its applicable approved product scope and inspect related product artifacts only as needed. In either case, task IDs, changed files, and discovery location are context only and must not unnecessarily restrict relevant investigation; do not expand into unrelated work or redesign.

The investigation may include:

- the reported finding
- the affected artifact
- relevant requirement sections
- relevant requirement-analysis sections
- relevant implementation-plan sections
- affected source code
- affected tests
- configuration
- database/schema/infrastructure
- architecture boundaries
- related implementation decisions
- relevant verification or review evidence

Do not expand the investigation into unrelated features or redesign the system beyond what is necessary to understand the finding.

Task IDs, recently changed files, or the location where the finding was discovered are investigation context and must not unnecessarily restrict the investigation scope.

---

## 4. Investigation Objectives

The investigation must establish, where evidence permits:

1. What was observed?
2. What was expected?
3. Is the finding valid?
4. What evidence supports or contradicts the finding?
5. What is the root cause?
6. Is the problem in production code, test code, configuration,
   environment, requirement, plan, or verification?
7. What are the available corrective options?
8. What are the consequences of each option?
9. Does the correction require a human decision?
10. What corrective direction is recommended?

Do not assume that every reported finding is a production-code defect.

---

## 5. Finding Validation
This section applies only when the request subject type is FINDING. For HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING), do not invent an expected-vs-observed defect, assign a finding ID, or use a finding-validation classification. Instead establish the human request and investigative authorization, intended governance outcome, affected governance artifacts, current authority and constraints, material risks, feasible change boundaries, and evidence or uncertainty. The enhancement investigation remains read-only and makes no approval or application decision.

First determine whether the finding is valid.

Classify the finding as one of:

### Valid Implementation Defect

The implementation does not satisfy the approved requirement or plan.

### Test Defect

The implementation is consistent with the requirement, but the test incorrectly
represents expected behavior.

### Requirement Ambiguity

The approved requirement does not provide enough information to determine the
correct behavior.

### Plan Problem

The implementation follows the approved plan, but the plan itself conflicts
with the approved requirement or creates an identified issue.

### Environment or Configuration Problem

The observed behavior is caused by environment, configuration, permissions,
infrastructure, or external dependencies rather than implementation logic.

### Verification Problem

The reported finding is caused by incomplete, incorrect, or insufficient
verification evidence.

### False Positive

Available evidence does not support the finding.

### Cannot Determine

Available evidence is insufficient to classify the finding.

Do not recommend a corrective implementation until the finding has been
validated sufficiently.

---

## 6. Root Cause Analysis

For a valid finding, determine the root cause.

Use the following structure:

### Observed Behavior

What actually happened?

### Expected Behavior

What should happen according to the approved requirement, plan, or other
authoritative source?

### Difference

What specifically differs between actual and expected behavior?

### Root Cause

What implementation, design, configuration, test, requirement, or process
condition caused the difference?

Avoid describing the symptom as the root cause.

For example:

Incorrect:

`ExecuteDeleteAsync deletes too many records.`

Better:

`The integration-test fixture has no test-data ownership boundary and therefore
the cleanup operation cannot distinguish test records from unrelated Customer
records.`

---

## 7. Corrective Options

When a valid finding requires a correction, identify viable options.

For each option describe:

- approach
- affected files/components
- production impact
- test impact
- architecture impact
- requirement impact
- implementation-plan impact
- migration/schema impact, if applicable
- operational impact
- complexity
- risks
- limitations

Do not create unnecessary alternatives.

Only present options that are technically viable for the current repository
and approved architecture.

---

## 8. Human Decision Assessment

Determine whether human decision or approval is required.

### Human Decision Usually Not Required

Examples include:

- straightforward implementation defect explicitly covered by the approved requirement and current approved implementation plan
- obvious missing validation required by the approved contract
- test assertion defect with an unambiguous expected behavior
- formatting or mechanical correction with no design impact

Such cases may proceed to the appropriate corrective process, subject to the project's established approval rules.

### Human Decision Required

Escalate when the correction could change or materially affect:

- approved requirements
- requirement analysis
- implementation plan
- architecture
- API contracts
- database schema
- data model
- security boundaries
- external integrations
- performance strategy
- infrastructure strategy
- scope
- backward compatibility
- production behavior where multiple valid approaches exist

When human decision is required, do not implement the correction.

Route the finding through the established Corrective Change Decision & Plan Update process.

---

## 9. Recommendation

When sufficient evidence exists, provide a recommendation.

The recommendation must state:

- recommended option
- reason
- expected impact
- known risks
- requirement impact
- plan impact
- architecture impact
- whether human approval is required

The recommendation is advisory.

It does not constitute human approval.

---

## 10. Read-Only Boundary

Finding Investigation is a read-only activity.

The investigator must not:

- modify source files
- modify tests
- modify requirements
- modify implementation plans
- modify configuration
- modify database state
- implement the correction
- commit changes
- push changes

If additional evidence requires a command or test, only perform it when the
investigation request explicitly permits execution.

---

## 11. Evidence Classification

Classify important evidence as:

### Executed Evidence

The investigator actually executed the relevant command, test, build, or
other verification activity and observed the result.

### Source Inspection Evidence

The conclusion was established by inspecting source code, configuration,
tests, project structure, or other repository artifacts.

### Reported Evidence

The result was supplied by the user or another agent and was not independently
reproduced.

### Unverified

Available evidence is insufficient to establish the conclusion.

Never present reported or source-inspection evidence as executed evidence.

---

## 12. Handling Uncertainty

Do not invent missing facts.

If the investigation cannot establish the root cause or determine the correct
behavior, explicitly state:

`Cannot be determined from available evidence.`

Identify the specific evidence required to continue.

---

## 13. Investigation Outcome

Use one of the following outcomes:

### FINDING CONFIRMED

The finding is valid and its cause is sufficiently understood.

### FINDING REJECTED

Available evidence does not support the finding.

### TEST DEFECT

The implementation is consistent with the approved behavior and the test is incorrect.

### REQUIREMENT OR PLAN CLARIFICATION REQUIRED

The correct behavior cannot be established without clarification or an approved change.

### EVIDENCE REQUIRED

Additional evidence is required before the finding can be classified.

### CORRECTIVE DIRECTION IDENTIFIED

The finding is confirmed, the corrective approach is sufficiently understood, and the appropriate next corrective decision can begin.
HUMAN-REQUESTED ENHANCEMENT CONTEXT ESTABLISHED: The separately authorized non-finding request, affected governance context, and evidence are sufficiently established for Corrective Change Decision consideration. This outcome does not validate a finding, approve the proposed enhancement, or authorize a policy change.

The investigation outcome is not itself a corrective approval or authorization to implement changes.

---

## 14. Required Investigation Report

The investigation report must contain:

1. Finding summary
2. Finding source
3. Finding validation
4. Evidence
5. Expected behavior
6. Actual behavior
7. Root cause
8. Impact assessment
9. Corrective options
10. Recommended option
11. Human decision requirement
12. Remaining uncertainties
13. Investigation outcome
14. Recommended next process
For the non-finding enhancement subject type, replace finding-specific fields with: stable Work ID allocated under section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md; verbatim human request and attribution; explicit investigation authorization and its scope; affected governance artifacts; current authoritative sources and evidence; intended outcome; constraints and feasible directions; human decision/approval requirements; uncertainties; outcome HUMAN-REQUESTED ENHANCEMENT CONTEXT ESTABLISHED or EVIDENCE REQUIRED; and recommended next process. Generate the candidate Work ID and collision-check it against both persistence roots before requesting authorization. The first successful, no-overwrite `attempt.json` publication reserves the ID before investigation execution; recheck for collisions immediately before publication and stop on any collision. If a valid reservation already exists for the same work, reuse it and preserve its history. Propagate the same Work ID unchanged to every linked invocation, report, result, evidence record, and human gate. A missing, placeholder, unreserved, or conflicting ID blocks this route. State explicitly that no finding is asserted and that the investigation does not approve or authorize a change.


The report must clearly distinguish facts, analysis, recommendations, and
reported evidence.

---

## 15. Recommended Next Process

Based on the investigation outcome:

- `FINDING REJECTED` → return to the originating verification/review process
- `TEST DEFECT` → proceed to the Corrective Change Decision & Plan Update process to determine the governed corrective action
- `FINDING CONFIRMED` → proceed to the Corrective Change Decision & Plan Update process
- `REQUIREMENT OR PLAN CLARIFICATION REQUIRED` → obtain the required human decision through the applicable governed process before implementation
- `EVIDENCE REQUIRED` → obtain the required evidence and repeat the investigation
- `CORRECTIVE DIRECTION IDENTIFIED` → proceed to the Corrective Change Decision & Plan Update process, subject to any required human approval
- `HUMAN-REQUESTED ENHANCEMENT CONTEXT ESTABLISHED` → proceed to Corrective Change Decision & Plan Update using the separate non-finding enhancement subject type; any proposal remains subject to explicit Human Approval and authorized application

Finding Investigation must not bypass the Corrective Change Decision & Plan Update process when a governed artifact requires correction.

The next process must determine whether the requirement, implementation plan, implementation, tests, configuration, or another governed artifact requires change and whether human approval is required.