Read and follow:
docs/ai/prompts/IMPLEMENTATION_PROMPT.md

Current Approved Requirement (path, version/status, and approval evidence):
Path: [PATH TO CURRENT APPROVED REQUIREMENT]
Version/status: [Current source version and status]
Approval evidence: [Reference to explicit approval evidence]

Current Approved Implementation Plan (path, version/status, and approval evidence):
Path: [PATH TO CURRENT APPROVED IMPLEMENTATION PLAN]
Version/status: [Current source version and status]
Approval evidence: [Reference to explicit approval evidence]
Human Review Approval evidence: [Reference to the Human Review package and explicit Human Review Approval, limited to progression to Human Plan Approval]

Implement:
[TASK IDS OR RANGE TO IMPLEMENT]

Additional Context:
[Optional implementation context, constraints, or evidence]

Project Instructions Setup precondition (PROJECT_INSTRUCTIONS_SETUP_GUIDELINES.md §9):
[First Implementation: the Phase 2 Setup result Work ID, location, and approved `.github/copilot-instructions.md` SHA-256 (`INSTRUCTIONS APPLIED`), or the recorded waiver naming Phase 2 and the current approved Requirement and Plan. Later Implementation: the latest applicable Setup result and approved SHA-256 or unlapsed waiver, and confirmation that no §3.3 refresh trigger is outstanding. Required before invocation.]

Setup record binding: [For the satisfying Setup result or waiver, give its Work ID, record identity, canonical path and record SHA-256. Separately give the instructions-file path and SHA-256 for INSTRUCTIONS APPLIED, or the observed file state/fingerprint or ABSENT for a waiver. The file fingerprint is not the record fingerprint.]

Repository Baseline Setup precondition: [applicable Phase 1/Phase 2 results,
per-item waivers, additive addenda and refresh evidence with identities, paths
and SHA-256; Phase 2 binds the current approved Requirement and Plan].

Execution Context
Feature ID: [Stable feature identifier]
Attempt ID: [Unique invocation identifier]
Record root: [Explicitly approved repository-associated persistence root]
Persistence decision: [Reference to the human governance decision approving the convention/root]
Record scope: [This attempt's designated output scope and requesting actor]
Source bindings: [Exact applicable artifact identities, versions/states, fingerprints, and approval evidence references; distinguish candidate from approved]
Repository binding: [Repository identity, HEAD, branch context, relevant worktree state, and implementation-state manifest where applicable]
Approved concurrency mode and Orchestrator coordination: [Current approved Plan section and mode; shared checkout/worktree identity; current coordination/exclusivity status; state UNKNOWN or UNASSESSED where not established]
Related records: [Prior attempt/results, findings, corrective decisions, task-impact assessments, and pending gate references; NONE if none exist]
Resume context: [NEW ATTEMPT, or incomplete attempt/checkpoint reference, unfinished work, blockers, and reconciliation required]
Evidence references: [Durable applicable evidence references and classifications]
Missing context: [Unresolved required information; NONE only when established]

Apply section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. This context does not establish approval, result applicability, or completion. Stop affected execution when required authority or recovery context cannot be reconciled.

Implementation Task Context
Requested tasks qualified by current approved Plan identity/version: [References]
Applicable retained/rework/partial-task dispositions: [References, or NOT APPLICABLE]

## Work Item Context (product work)

- Canonical Work Item IDs and types: [IDs/types, or NOT APPLICABLE]
- Parent and related Work Item IDs: [IDs, or NONE established]
- Source Requirement version ID and SHA-256: [identity/fingerprint, or NOT APPLICABLE]
- Existing Requirement IDs, Feature IDs, Plan-local Task IDs, and Finding IDs with mappings: [references, or NOT APPLICABLE]

Use only identities established by the applicable upstream artifact or existing record; identify missing or unresolved mappings rather than inventing IDs. Work Item IDs are traceability context; they do not establish approval or restrict any required complete-scope verification or review. Follow the governing Work Item ID rules.

### Portability reassessment gate evidence

Portability reassessment: [NOT APPLICABLE with reason | current assessment report identity/location/SHA-256; trigger and target revision; possible-blocker IDs and stated scopes; affected-stage determination under SDLC_GOVERNANCE.md Section 3; attributable Human decision identity/location/SHA-256 and exact conditions/hold direction for each in-scope blocker]. An unresolved or ambiguous gate blocks consequential work; do not infer a Human decision or automatically invoke Portability Assessment. Governance-only subject: NOT APPLICABLE with reason.
