Read and follow:
docs/ai/prompts/IMPLEMENTATION_PLANNING_PROMPT.md

Current Approved Requirement (path, version/status, and approval evidence):
Path: [PATH TO CURRENT APPROVED REQUIREMENT]
Version/status: [Current source version and status]
Approval evidence: [Reference to explicit approval evidence]

Additional approved technical decisions:
1. ...
2. ...
3. ...

Execution Context
Feature ID: [Stable feature identifier]
Attempt ID: [Unique invocation identifier]
Record root: [Explicitly approved repository-associated persistence root]
Persistence decision: [Reference to the human governance decision approving the convention/root]
Record scope: [This attempt's designated output scope and requesting actor]
Source bindings: [Exact applicable artifact identities, versions/states, fingerprints, and approval evidence references; distinguish candidate from approved]
Repository binding: [Repository identity, HEAD, branch context, relevant worktree state, and implementation-state manifest where applicable]
Related work/concurrency context: [Known related features or active attempts, shared repository/checkout/worktree context, known dependencies or shared change surfaces, and existing Orchestrator coordination; state UNKNOWN or UNASSESSED where not established]
Related records: [Prior attempt/results, findings, corrective decisions, task-impact assessments, and pending gate references; NONE if none exist]
Resume context: [NEW ATTEMPT, or incomplete attempt/checkpoint reference, unfinished work, blockers, and reconciliation required]
Evidence references: [Durable applicable evidence references and classifications]
Missing context: [Unresolved required information; NONE only when established]

Apply section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. This context does not establish approval, result applicability, or completion. Stop affected execution when required authority or recovery context cannot be reconciled.

Planning Output Context
Candidate Plan identity/version and designated output: [Reference]
Previous approved Plan and task-impact context: [Reference, or NOT APPLICABLE for initial planning]

## Work Item Context (product work)

- Canonical Work Item IDs and types: [IDs/types, or NOT APPLICABLE]
- Parent and related Work Item IDs: [IDs, or NONE established]
- Source Requirement version ID and SHA-256: [identity/fingerprint, or NOT APPLICABLE]
- Existing Requirement IDs, Feature IDs, Plan-local Task IDs, and Finding IDs with mappings: [references, or NOT APPLICABLE]

Use only identities established by the applicable upstream artifact or existing record; identify missing or unresolved mappings rather than inventing IDs. Work Item IDs are traceability context; they do not establish approval or restrict any required complete-scope verification or review. Follow the governing Work Item ID rules.

## Optional Product GitHub Work-Item Reference (not a gate)

- Human-provided GitHub URL(s): [sanitized URL(s), or NOT SUPPLIED; NOT APPLICABLE for governance work]

No URL is required. Do not include secrets or credentials in a URL. The process treats any supplied URL only as an optional opaque reference and does not fetch, poll, or interpret it. Omission does not block any process or gate.

### Portability reassessment gate evidence

Portability reassessment: [NOT APPLICABLE with reason | current assessment report identity/location/SHA-256; trigger and target revision; possible-blocker IDs and stated scopes; affected-stage determination under SDLC_GOVERNANCE.md Section 3; attributable Human decision identity/location/SHA-256 and exact conditions/hold direction for each in-scope blocker]. An unresolved or ambiguous gate blocks consequential work; do not infer a Human decision or automatically invoke Portability Assessment. Governance-only subject: NOT APPLICABLE with reason.

### optional UI prototype planning input

Optional UI prototype: [NOT USED | prototype identity/path/SHA-256; pinned template identity/path/SHA-256; independent Verification report/result identities/location/SHA-256; Human Prototype Approval evidence identity/location/SHA-256 and exact approved Requirement identity/version binding].
