# Requirement Analysis Prompt

Read and follow:

`docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`

Using those guidelines, analyse the requirement document specified by the user.

The user will provide:

1. The requirement document to analyse
2. Human decisions, if any, that have already been provided for the requirement

## Instructions

- Treat the specified requirement document as the authoritative source of truth.
- Treat explicitly supplied human decisions as authoritative decisions for the applicable requirement questions.
- Perform analysis only; do not modify source/evaluated artifacts or another process’s records. This restriction does not prohibit publishing this process’s own governed output records within its explicitly designated record scope, as permitted by §33.1 of `SDLC_ARTIFACT_GOVERNANCE.md` and §30.1 of `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md`.
- Do not implement anything.
- Do not create or modify an implementation plan.
- Identify missing information, ambiguities, conflicts, assumptions, business rules, scope boundaries, dependencies, and relevant technical impact.
- Do not silently make unresolved business decisions.
- Clearly identify decisions that require human input.
- Clearly distinguish:
  - explicit requirements
  - human decisions
  - derived observations
  - assumptions
  - technical recommendations
- Do not introduce functionality that is not supported by the requirement or explicitly approved human decisions.
- Keep technical recommendations implementation-neutral unless the requirement or applicable engineering constraints require technical consideration.
- Follow the standard analysis output defined in `docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`.
- Do not treat Requirement Analysis as Requirement Approval.
- Do not claim human approval or acceptance.
- Requirement Analysis Verification and Human Requirement Approval are separate subsequent stages.

At the end, state:

1. Requirement analysis outcome
2. Human decisions incorporated
3. Blocking decisions, if any
4. Whether the requirement is ready for Requirement Analysis Verification