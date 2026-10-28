# Finding Investigation Prompt

Read and follow:

`docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md`

Use the Investigation Request above to determine the scope, affected artifact, and context of the investigation.
The request must identify its subject type. For FINDING, follow the finding validation and report rules unchanged. For HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING), verify the attributed human request and explicit authorization to investigate it; keep it distinct from every finding; do not invent a finding ID, defect, finding validation, or finding disposition. Use the enhancement-specific investigation outcome and report fields in the Guideline. The investigation is advisory and read-only; it does not approve or authorize a governance change. For the enhancement route, validate that the candidate Work ID was collision-checked against both persistence roots before authorization. Before investigation execution, recheck for collisions and publish the first actor-owned `attempt.json` without overwrite; that first successful publication reserves the ID. Do not require a prior attempt record to exist before it can be published. If an existing valid reservation for the same work exists, reuse it; if a collision or conflicting record exists, stop and reconcile rather than overwrite. Preserve the Work ID across all linked records. `NOT ASSIGNED`, a placeholder, or an unreserved identifier is invalid input.
For the enhancement route, require a RESERVED STABLE WORK ID (per SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 30.1); NOT ASSIGNED is not valid input.

Inspect the applicable current approved source documents, including evidence identifying their current version and approval status, and the actual repository relevant to the finding. If current status or approval cannot be established, identify that uncertainty rather than silently selecting a source.

Do not rely solely on previous AI summaries.

For a FINDING, validate it, determine root cause where possible, evaluate viable corrective options, assess their impact, and determine whether human decision or approval is required. For a HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING), do not validate a finding or perform expected-versus-observed defect or defect-root-cause analysis; instead establish the authorized request context and assess the intended governance outcome, affected artifacts, constraints, risks, feasible directions, evidence gaps, and human decision/approval needs required by the Guideline.

Consider the complete relevant context of the affected governed artifact. Task IDs, recently changed files, or corrective changes are context only and must not unnecessarily restrict the investigation scope.

Produce the investigation report required by the guideline.

Clearly distinguish executed evidence, source inspection evidence, reported evidence, and unverified information.

Do not modify the implementation or any other governed artifact as part of the investigation.

Do not make or claim human approval.

If a requirement, requirement analysis, implementation plan, implementation, test, configuration, or other governed artifact requires correction, identify the affected artifact and route the finding to the Corrective Change Decision & Plan Update process.

At the end, state:

1. Investigation outcome
2. Affected artifact
3. Whether the finding is confirmed
4. Root cause, if established
5. Recommended corrective direction, if appropriate
6. Whether human decision/approval is required
7. Recommended next process