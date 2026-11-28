Read and follow:
docs/ai/prompts/IMPLEMENTATION_VERIFICATION_PROMPT.md

Feature / Implementation
[Feature name]

Task IDs
[List implemented task IDs, if applicable. These are verification context only and must not restrict verification scope.]

Current Approved Requirement (path, version/status, and approval evidence)
[PATH / VERSION / STATUS / APPROVAL EVIDENCE]

Current Approved Implementation Plan (path, version/status, and approval evidence)
[PATH / VERSION / STATUS / APPROVAL EVIDENCE]

Relevant Architecture / Engineering Guidelines
[List relevant guidelines]

Implementation Scope / Repository Context
[Relevant projects, layers, components, files, existing implementation, or repository conventions]

Verification Objective
[Optional specific verification focus. This must not restrict complete implementation verification.]

Reported Evidence
[Any test, build, review, or other evidence supplied by the user or previous process]

Previous Verification / Review Results
[If applicable]

Additional Context
[Any additional information]

Execution Context
Feature ID: [Stable feature identifier]
Attempt ID: [Unique invocation identifier]
Record root: [Explicitly approved repository-associated persistence root]
Persistence decision: [Reference to the human governance decision approving the convention/root]
Record scope: [This attempt's designated output scope and requesting actor]
Source bindings: [Exact applicable artifact identities, versions/states, fingerprints, and approval evidence references; distinguish candidate from approved]
Repository binding: [Repository identity, HEAD, branch context, relevant worktree state, and implementation-state manifest where applicable]
Related records: [Prior attempt/results, findings, corrective decisions, task-impact assessments, and pending gate references; NONE if none exist]
Resume context: [NEW ATTEMPT, or incomplete attempt/checkpoint reference, unfinished work, blockers, and reconciliation required]
Evidence references: [Durable applicable evidence references and classifications]
Missing context: [Unresolved required information; NONE only when established]

Apply section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. This context does not establish approval, result applicability, or completion. Stop affected execution when required authority or recovery context cannot be reconciled.

Implementation Verification Target Binding
Complete implementation-state manifest: [Exact target reference]
Previous verification/review target bindings: [References and known applicability limitations, or NONE]

## Work Item Context (product work)

- Canonical Work Item IDs and types: [IDs/types, or NOT APPLICABLE]
- Parent and related Work Item IDs: [IDs, or NONE established]
- Source Requirement version ID and SHA-256: [identity/fingerprint, or NOT APPLICABLE]
- Existing Requirement IDs, Feature IDs, Plan-local Task IDs, and Finding IDs with mappings: [references, or NOT APPLICABLE]

Use only identities established by the applicable upstream artifact or existing record; identify missing or unresolved mappings rather than inventing IDs. Work Item IDs are traceability context; they do not establish approval or restrict any required complete-scope verification or review. Follow the governing Work Item ID rules.

### Portability reassessment gate evidence

Portability reassessment: [NOT APPLICABLE with reason | current assessment report identity/location/SHA-256; trigger and target revision; possible-blocker IDs and stated scopes; affected-stage determination under SDLC_GOVERNANCE.md Section 3; attributable Human decision identity/location/SHA-256 and exact conditions/hold direction for each in-scope blocker]. An unresolved or ambiguous gate blocks consequential work; do not infer a Human decision or automatically invoke Portability Assessment. Governance-only subject: NOT APPLICABLE with reason.

### optional UI prototype Implementation Verification input

Prototype used by implementation: [NOT USED | approved Plan task/section and prototype identity/path/SHA-256; pinned template identity/path/SHA-256; Plan-bound independent Verification report/result identities/location/SHA-256; Human Prototype Approval evidence identity/location/SHA-256 and exact Requirement binding].

### instructions and Setup evidence binding

For each applicable record, bind `.github/copilot-instructions.md` exact path+SHA-256 and the satisfying Project Instructions Setup result identity/location/SHA-256 OR applicable recorded waiver identity/location/SHA-256. Missing/unresolvable evidence: [identify; do not infer].
