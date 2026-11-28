---
name: repository-baseline-setup
description: Interactively assesses and applies individually human-approved repository baseline files under the governed Repository Baseline Setup mechanism.
---

# Repository Baseline Setup Skill

Read and follow the current Repository Baseline Setup Guideline, Prompt and
Request under the three Masters. This Skill creates no authority.

## Preconditions

Establish the phase, reserved Work ID, exact target and current state, adopted
product root and Master baseline, current actor identity/capabilities and
authorized record scope, fresh human initiation and applicable predecessor
records. Before consequential work publish and integrity-check this actor's
own attempt under section 30.1. A missing or conflicting prerequisite stops
the run; a Request is not file approval.

## Execution

1. Inspect authorized source and target evidence, keeping it distinct.
   Identify platform, effective Git configuration, current files and tracked
   paths without executing project scripts or hooks. Bind source fingerprints.
2. With the human, classify each candidate, confirm supported owners,
   protected rules and representative must-ignore/must-track paths. Keep
   unresolved classification blocking until the human decides it.
3. Perform the Guideline's safe checks, including nested rule, negation,
   tracked-file and attributes checks. Obtain separate per-run secret-scan
   authorization before any secret-indicator check. Report redacted results,
   unperformed checks and LFS/remote uncertainty accurately.
4. Present each applicable file's exact bytes, path, diff, base fingerprint
   or absence, and proposed SHA-256. Obtain and preserve a separate explicit
   attributable human decision for each. An approved file may be applied even
   when another is deferred, only after its individual preflight; verify
   readback.
   For an already-correct file, bind the separate approval of its exact
   existing bytes, recheck its fingerprint and applicable validation, and
   record `VERIFIED UNCHANGED` without rewriting it.
5. On mismatch or error stop and record exact partial effects. Record any
   actual scoped waiver without inferring one; enforce its named required
   items, phase, conditions and maximum 90-day expiry.
6. Publish only this actor's permitted report, evidence, result and other
   records. Report classifications, decisions, per-file outcomes, evidence,
   fingerprint bindings, unperformed checks, partial effects, phase
   satisfaction and next action. Do not claim completion where required items
   or classifications remain unresolved. Stop at the handoff.

## Boundaries

Write only specifically approved baseline files and this actor's own
authorized records. Do not change project instructions, governance or other
product files, run project scripts or hooks, invoke another Agent, stage,
commit, push, change remote settings, install/configure LFS, migrate files or
rewrite history. Approval of a file is not process initiation or any product
approval. Follow the separately authorized baseline-only commit route without
performing that commit in this Skill.
