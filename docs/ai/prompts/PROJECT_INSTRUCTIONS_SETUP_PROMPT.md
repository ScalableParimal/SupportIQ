# Project Instructions Setup Prompt

Read and follow `docs/ai/guidelines/PROJECT_INSTRUCTIONS_SETUP_GUIDELINES.md` and the invocation's `docs/ai/request/PROJECT_INSTRUCTIONS_SETUP_REQUEST.md`.

## Before you start

1. Identify the phase: `PHASE-1`, `PHASE-2`, or `REFRESH`.
2. Identify the target repository and its revision.
3. Identify the adopted Master baseline, the Portability report, the approved Requirement and Plan (Phase 2, or a REFRESH that depends on them), the verified base state of `.github/copilot-instructions.md` (PRESENT with path and SHA-256, or ABSENT), the authorized human, and the record scope.
4. Verify the phase entry conditions. If any are missing, stop and say what is missing.
5. Before Phase 1 or Phase 2, verify the corresponding Repository Baseline Setup
   phase from durable records under its Guideline. Respect the prospective
   transition and any triggered refresh. Do not invoke another Agent.

## Run the questionnaire

Run topics Q0–Q8 interactively, one topic per structured question form.
- Prefill each answer from cited evidence.
- Never invent an answer.
- In Phase 1, a decision that depends on the Plan becomes `PENDING PHASE 2: <topic>`.
- In Phase 2, resolve every pending marker. When the Plan and a proposed instruction conflict, the Plan wins, unless the instruction is a designated mandatory team rule, which a Plan may tighten but not weaken. Record each conflict for the human.

## Build and check the file

1. Compose the file using the Guideline's required structure.
2. Run the self-check.
3. Present the full content, its SHA-256, the diff, the answer sources, the pending markers, and the conflicts.
4. Request Human Instructions Approval of that exact fingerprint.

## Write the file

Write only after explicit, attributable approval.
1. Verify the base fingerprint for PRESENT, or verify the file remains ABSENT.
2. Write only the approved bytes to `.github/copilot-instructions.md`.
3. Read the file back and verify its hash.
4. Publish your own records.

## Waiver

If the authorized human waives the phase or refresh, record the waiver verbatim under Guideline §3.4. It must name the phase, the covered preconditions, the rationale, and the lapse condition, together with the observed file fingerprint or verified ABSENT state. Then publish `WAIVED`. Never propose or infer a waiver.

## Boundaries

Do not:
- edit any other file
- commit or push
- invoke another Agent or the Orchestrator
- run project scripts or tests
- treat this approval as a Requirement, Review, Plan, Acceptance, or Process Initiation approval

Stop at the handoff. Report the outcome, the record references, and the next permitted process.
