# Implementation Plan Verification Prompt

Read and follow:

`docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md`

Independently verify the complete current candidate Implementation Plan under verification against:

If a previously approved Implementation Plan is supplied, use it only as a baseline/comparator; it is not the verification target.

- the complete current approved Requirement
- the applicable architecture
- applicable engineering guidelines
- relevant repository constraints and conventions
- available technical evidence

Verify:

1. Requirement traceability
2. Scope alignment
3. Architecture alignment
4. Task completeness
5. Task dependencies and sequencing
6. Technical feasibility
7. API and contract completeness where applicable
8. Data and persistence design where applicable
9. Validation and error handling
10. Testing strategy
11. Acceptance criteria
12. Decisions and ambiguities
13. Assumptions and dependencies
14. Implementation sequence

Verify cross-feature dependencies and shared change surfaces, the proposed execution mode, and any required integration/reconciliation. Do not treat an undeclared dependency as evidence of concurrency safety; require sequencing/serialization when relevant information is unassessed.

Identify:

- missing requirements
- incomplete tasks
- architecture conflicts
- missing decisions
- scope issues
- dependency/sequencing problems
- testability gaps
- technical risks
- unsupported assumptions

For every material finding, provide evidence, impact, severity, confidence, and recommended action.

If a human decision is required, identify the decision explicitly and explain why it cannot be safely assumed.

Do not:

- implement code
- modify tests
- modify the requirement
- silently modify the implementation plan
- change architecture
- make unapproved human decisions
- apply corrective changes
- claim Human Plan Approval

If plan changes are required, provide precise recommended changes but do not apply them.

Verify the complete current plan, not only recently changed tasks.

If the plan has previously been modified, verify the complete updated plan again.

Clearly distinguish:

- executed evidence
- source inspection evidence
- reported evidence
- unverified information

Return the complete verification report defined by:

`docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md`