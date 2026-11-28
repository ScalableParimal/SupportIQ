# Request: Project Instructions Setup

Read and follow `docs/ai/prompts/PROJECT_INSTRUCTIONS_SETUP_PROMPT.md` and `docs/ai/guidelines/PROJECT_INSTRUCTIONS_SETUP_GUIDELINES.md`.

## Work ID

- Work ID / request identity: [stable repository-unique Work ID; 'not assigned' is draft-only]

An executable request needs a reserved, stable Work ID under the Project Instructions Setup Work ID allocation in `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §30.1. The format is `instructions-setup-<uuid-v4>`, with one Work ID per Setup run, owned by the target-project scope, under the adopted product root `docs/sdlc-records/product/`.
- If this continues an existing authorized same-run reservation, keep that Work ID unchanged.
- For a new run, allocate the ID and check it for collisions against both persistence roots before invocation. The first authorized no-overwrite `docs/sdlc-records/product/<work-id>/attempts/<attempt-id>/attempt.json` publication reserves the ID.
- 'not assigned' is draft-only. It blocks invocation and record publication.

## Request fields

- Phase: [PHASE-1 baseline (onboarding) / PHASE-2 engineering finalization (pre-Implementation) / REFRESH]
- Trigger and changed inputs: [initial onboarding / Plan approved / named refresh trigger; identify the prior Setup result (Work ID, location, fingerprint) if one exists]
- Target project: [repository/workspace identity, authorized root, branch/commit or immutable revision]
- Adopted Master baseline: [baseline identity and the three Master fingerprints]
- Adopted product persistence root: [path and adoption evidence]
- Portability Assessment report and blocker dispositions: [path/identity/fingerprint]
- Repository Baseline Setup applicable phase result, per-item waiver and refresh evidence: [identities, paths, SHA-256; unresolved if absent]
- Approved Requirement (required for Phase 2; for REFRESH only when the trigger or affected sections depend on it): [path, version, approval evidence; otherwise NOT APPLICABLE with reason]
- Approved Implementation Plan (required for Phase 2; for REFRESH only when the trigger or affected sections depend on it): [path, version, Human Plan Approval evidence; otherwise NOT APPLICABLE with reason]
- Existing instructions file: [absent / path and SHA-256]
- Read permission: [explicit target paths]
- Write permission: the instruction file plus this actor's own records. That is `.github/copilot-instructions.md` (only after Human Instructions Approval) plus this actor's own records within the actor-owned output-record scope below.
- Team-level decisions already made: [verbatim, with source; otherwise none]
- Human authorized to answer the questionnaire and approve the instructions: [identity/role]
- Actor-owned output-record scope: [exact scope or not authorized]
- Known constraints/security/privacy limits: [state]
- Additional context: [state]

A Request does not grant approval, any broader write access, runtime execution, or authority to invoke another Agent.
