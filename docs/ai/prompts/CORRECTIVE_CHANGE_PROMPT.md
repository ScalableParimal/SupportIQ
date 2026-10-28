# Corrective Change Decision & Plan Update Prompt

Read and follow:

`docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md`

Use the supplied Finding Source, Affected Artifact, Current Approved Requirement and Current Approved Implementation Plan where applicable, including evidence identifying their current version and approval status, Finding Investigation, repository state, and evidence as the source of truth. If current version, status, or approval cannot be established, identify the uncertainty rather than silently selecting a source.
The request identifies exactly one subject type: FINDING or HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING). For the latter, require the attributed human wording, explicit proposal-preparation authorization and scope, and investigation result. Keep the enhancement separate from every finding; do not invent a finding ID or use a finding disposition. Use only the enhancement-specific statuses in the Guideline, and treat a proposal as unapproved until explicit Human Approval binds the exact per-file content or unambiguous diff in the canonical process-owned report, exact target paths and base/expected-after SHA-256 fingerprints, scope, exclusions, application route, and distinct identities for the proposal preparer, one-time initial applier, verifier, and reviewer. Human Approval must designate the one-time initial applier, but must not require a separate pre-existing runtime-qualification record or treat designation as capability evidence. The applier must publish and integrity-check its own current-invocation identity, permissions, publication route, and role-specific capability evidence in its Application attempt before any source write; missing or uncertain evidence requires `CANNOT COMPLETE`. For every other actor, require its own current-invocation evidence under SDLC_ARTIFACT_GOVERNANCE.md section 33.1 while preserving role-specific capability, independence, fresh stage-start, and read-only requirements. A standalone patch file is not required. Human Approval does not initiate a process stage; each Application, Verification, Review, and Audit invocation requires its own fresh explicit human stage-start instruction and actor-owned attempt record.

Determine:

1. For a FINDING, whether it should be accepted or rejected. For a HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING), do not determine finding acceptance or rejection; determine only its separate enhancement disposition under the Guideline.
2. The appropriate corrective decision.
3. Which governed artifact is affected.
4. Whether the current implementation plan remains valid.
5. Whether a plan update is required.
6. What specific artifact or plan changes are required, if any.
7. Whether human approval is required before proceeding.
8. What the next process should be.
For an enhancement, determine whether it is admitted for proposal, no-change-recommended, or not admitted; state explicitly that this is not finding acceptance/rejection and is not approval or authority to apply.

If a plan update is required, produce a precise proposed amendment to the approved implementation plan.

If another governed artifact requires correction, identify the affected artifact and the applicable corrective process. Do not perform the correction.

Do not implement the corrective change.

Do not modify source code, tests, configuration, migrations, or other implementation artifacts.

Do not claim human approval.

Do not silently change the requirement or implementation scope.

Clearly distinguish executed evidence, source inspection evidence, reported evidence, and unverified information.

If required information is missing or conflicting, identify it rather than inventing an answer.

Return the required decision report defined by:

`docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md`