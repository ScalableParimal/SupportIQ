# Repository Baseline Setup Prompt

Read and follow `docs/ai/guidelines/REPOSITORY_BASELINE_SETUP_GUIDELINES.md`
and the invocation's `docs/ai/request/REPOSITORY_BASELINE_SETUP_REQUEST.md`
under the three Masters.

Establish the exact target, phase, reserved Work ID, adopted product root and
Master baseline, authorized actor and record scope, fresh stage-start and
applicable Portability, Requirement, Plan and prior baseline evidence. Stop
when a required input, authority or capability is missing.

Inspect authorized evidence without executing project scripts. Interactively
present each applicable candidate and its evidence to the authorized human.
Record applicability, requiredness, protected rules and must-track paths, and
every actual human decision. Do not decide for the human or infer approval.

For each applicable file, present exact proposed bytes, path, diff, base
fingerprint or absence and worktree SHA-256. Obtain a separate explicit
attributable decision. Apply independently approved changes only after each
base preflight, then verify readback. For an already-correct file, obtain its
own exact-content approval, validate its current fingerprint and behavior,
and record `VERIFIED UNCHANGED` without rewriting it. Record deferrals,
failures and partial outcomes; stop on mismatch or error. Never turn deferral
into a waiver.

Run only authorized checks described by the Guideline. Secret-indicator
checks require explicit human authorization each run; never output values or
excerpts. Identify unperformed and unverified checks. Preserve existing
content, tracked files, private records and Git history. Do not run project
scripts, hooks or external clean/smudge filters.

Publish only approved target files and this actor's own permitted records.
Do not modify project instructions or governance, invoke another Agent, stage,
commit, push, change remote settings, or install/configure/migrate LFS.
Report per-item outcomes and phase satisfaction; stop at the handoff.
