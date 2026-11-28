---
name: project-instructions-setup
description: Executes the governed Project Instructions Setup process that interactively generates, and after explicit human approval writes, the target project's .github/copilot-instructions.md during onboarding (Phase 1) and before first Implementation (Phase 2).
---

# Project Instructions Setup Skill

## Purpose and governing artifacts

Run the Project Instructions Setup defined by its current Guideline, Prompt, and Request, under the three Master Governance documents. This Skill supplies the execution mechanics. It creates no new authority.

## Preconditions

Before inspecting any inputs, resolve the following from the Request:
- the phase
- the Work ID
- the target identity and revision
- the adopted Master baseline and product root
- the Portability report
- the applicable Repository Baseline Setup phase result, current per-item
  waivers and refresh evidence under its Guideline
- for Phase 2, the approved Requirement and Plan; for REFRESH, these only when the trigger or the affected sections depend on them (otherwise record NOT APPLICABLE with the reason)
- the verified instructions-file base state: PRESENT with path and SHA-256, or ABSENT
- the authorized human
- the record scope

Stop with `CANNOT COMPLETE` if any of them is missing. A Request is not approval.

## Execution

1. Verify the phase entry conditions from Guideline §3. For a REFRESH, name the trigger and the affected sections. Reuse unchanged sections only when their input fingerprints still match.
2. Inventory evidence read-only within authorized paths:
   - the repository tree
   - project and package manifests
   - CI definitions
   - test configuration
   - the Portability report
   - the approved Requirement and Plan, in Phase 2 or when a REFRESH depends on them
   - the existing instructions

   Fingerprint each source. Do not execute project scripts or tests.
3. Run questionnaire topics Q0–Q8 in order. Use one interactive structured question form per topic, with prefilled answers and cited sources. Record each human answer verbatim with its source.
   - Never answer for the human.
   - In Phase 1, record Plan-dependent topics as `PENDING PHASE 2: <topic>`.
   - In Phase 2, resolve every marker and list Plan conflicts. The Plan wins, except over a designated mandatory team rule, which a Plan may tighten but not weaken (Guideline §2). The human decides whether instruction text changes; report a Plan that weakens a mandatory rule as a finding.
4. Compose the file using the Guideline §5 structure, then run the Guideline §6 self-check.
5. Present the following:
   - the full content
   - its SHA-256
   - the diff against the existing file
   - the answer sources
   - the pending markers
   - the conflicts
   - the self-check results

   Request explicit Human Instructions Approval of that exact fingerprint. If the content is edited, regenerate it and request approval again. If approval is absent, publish `PENDING HUMAN APPROVAL` and stop without writing.
6. After approval, confirm the base fingerprint for PRESENT or confirm the file remains ABSENT, and write only the approved bytes to `.github/copilot-instructions.md`. Read the file back and verify the hash. On a mismatch, stop with `CANNOT COMPLETE` and preserve the evidence.
7. For a human waiver, record it verbatim with the phase or refresh it covers, the preconditions it covers, its rationale, its lapse condition, and the observed file fingerprint (or absent), then publish `WAIVED` (Guideline §3.4).
8. Publish only this actor's own records, following `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §30.1. Return the outcome, the record references, and the next permitted process. Then stop.

## Boundaries

This Skill must not:
- write any file other than `.github/copilot-instructions.md` and its own records
- commit or push
- automatically invoke another Agent or the Orchestrator
- self-approve, or claim approval of a Requirement, Review, Plan, Acceptance, or Process Initiation
- modify governance artifacts
- start any product process
