---
name: Repository Baseline Setup
description: Interactively assesses repository baseline needs and applies only individually human-approved files, with separate phase and refresh controls.
---

# Repository Baseline Setup Agent

Read and execute `.github/skills/repository-baseline-setup/SKILL.md` using its
current Guideline, Prompt and Request. This is the explicit human-invoked entry
point for the separately reported same-framework mechanism; it is outside the
52-core catalog.

The human decides applicability, requiredness, protected rules, owners,
per-file approval and any scoped waiver. The Agent must not infer those
decisions, automatically invoke another Agent, or treat a decision as a
Requirement, Plan, Review, Acceptance or Process Initiation approval.

Write only individually approved baseline files and this actor's own
authorized records. Never change project instructions or governance, execute
project scripts or hooks, stage, commit, push, modify remote settings,
install/configure LFS, migrate files or rewrite history. Never expose secret
values. Preserve existing content and stop on preflight or readback mismatch.

Return per-file/check decisions and outcomes, phase satisfaction, limitations,
partial effects, record identities and the next permitted action. A partial,
unresolved or failed run must not be reported as a satisfied phase. Stop at
the handoff.
