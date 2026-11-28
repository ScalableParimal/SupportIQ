# Request: Repository Baseline Setup

Read and follow `docs/ai/prompts/REPOSITORY_BASELINE_SETUP_PROMPT.md` and
`docs/ai/guidelines/REPOSITORY_BASELINE_SETUP_GUIDELINES.md`.

## Work ID

- Work ID: [reserved `repository-baseline-<uuid-v4>` or draft-only unassigned]

Follow `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` section 30.1. Continue an
authorized same-run reservation unchanged. For a new run, generate and
collision-check the ID against both persistence roots before invocation;
the first authorized no-overwrite attempt publication reserves it. An
unassigned ID blocks execution and publication.

## Request fields

- Phase and trigger: [PHASE-1 / PHASE-2 / REFRESH; changed inputs and affected scope]
- Target: [canonical repository, authorized root, branch, commit and relevant worktree state]
- Adopted Master baseline: [identity and three fingerprints]
- Adopted product persistence root and actor-owned output scope: [paths and authorization]
- Applicable Portability report and human blocker dispositions: [identities, locations and hashes]
- Phase 2 Requirement, Plan and approvals: [identities and hashes; otherwise not applicable with reason]
- Prior baseline results, waivers and additive addenda: [identities, paths, hashes or none]
- Candidate files/checks, existing rules and source evidence: [inventory]
- Human authorized for classification, approval and waiver: [identity/role and evidence]
- Protected rules and must-track/must-ignore paths: [actual human designations or unresolved]
- Platform and remote checks: [identified platform, read authorization and limits]
- Secret-indicator check: [explicit per-run authorization and scope or not authorized]
- Git LFS: [applicability, readiness evidence and limitations or unresolved]
- Read scope and current capability evidence: [paths, identity, permissions and publication route]
- Existing content and fingerprints: [path and SHA-256 or verified absence]
- Known privacy, concurrent-writer and other limitations: [state]

The request does not approve any file, waive a requirement, authorize a scan,
start another stage, permit broader writes, or authorize commit or push.
