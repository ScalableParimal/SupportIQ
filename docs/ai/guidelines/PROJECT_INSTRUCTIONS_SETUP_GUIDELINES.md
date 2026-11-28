# Project Instructions Setup Guidelines

## 1. Purpose and outcome

Make sure every target project governed by this framework has a current, human-approved repository instruction file at `.github/copilot-instructions.md`. Generate it through an interactive, evidence-prefilled questionnaire, so no team has to write an ad-hoc prompt or remember to create the file.

The file is the project's **approved project engineering instructions**. It is the source of the "approved architecture and engineering guidelines" that Implementation Planning, Implementation, Implementation Verification, and Implementation Review use as technical constraints.

This is a separately reported, same-framework mechanism under the three Master Governance documents (`SDLC_ARTIFACT_GOVERNANCE.md` §3.6). It is not a parallel SDLC, a product Requirement, an Implementation Plan, a Governance Audit, or an approval authority. It does not add to the 52-core catalog.

## 2. Authority and boundaries

- Precedence is: the three Masters, then the current approved Requirement, then the current approved Implementation Plan, then the approved project instructions, then existing repository conventions, then AI recommendations.
- The exception to that order is **mandatory team rules** (`SDLC_ARTIFACT_GOVERNANCE.md` §3.6). These are the instruction rules the Human Instructions Approval explicitly designates as mandatory, such as a coverage threshold, requirement-ID test tagging, and stop gates.
  - A Plan may make them stricter but must not weaken, waive, or omit them.
  - Only a Setup refresh with new approval may change them.
  - They still rank below the Masters and the approved Requirement.
- The instructions must state this precedence and list the designated mandatory team rules. They must never grant, imply, or record approval, verification, or acceptance. They must never weaken or redefine a Master, Guideline, Prompt, Request, Skill, or Agent.
- The Setup actor may write only the instruction file plus its own records:
  1. the target project's `.github/copilot-instructions.md`
  2. its own actor-owned records within the authorized scope under the adopted product root
- The Setup actor writes the instruction file only after **Human Instructions Approval**. Human Instructions Approval is an explicit, attributable human decision bound to:
  - the exact proposed content
  - its SHA-256 fingerprint
  - the target path
  - the phase
  - the scope

  It is a recorded human decision of the same kind as a Portability blocker disposition. It is not Human Requirement Approval, Human Review Approval, Human Plan Approval, or Human Acceptance, and it does not substitute for any of them. It is also not Process Initiation Approval: an Orchestrator interlock response neither approves instruction content nor satisfies a Setup phase.
- The Setup actor must not modify any other file. That includes Masters, Guidelines, Prompts, Requests, Skills, Agents, Requirements, Plans, source code, tests, CI, or configuration.
- The Setup actor must not:
  - commit or push
  - automatically invoke another Agent
  - activate the Orchestrator
  - execute project scripts or tests
  - self-approve
- AI answers, defaults, and repository inferences are proposals until the human confirms them. Never invent a technology choice, ID scheme, coverage threshold, approval, or Work Item ID.

## 3. Phases and entry conditions

The mechanism has two required phases plus a refresh route.

### 3.1 Phase 1: Baseline instructions (onboarding)

Phase 1 runs after the Portability Assessment completes and every recommended possible blocker has its recorded human disposition. It must complete before the target's first Requirement Analysis.

Prerequisites:
- the adopted product persistence root
- the adopted Master baseline (`SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §§30.1, 42, and 43.3)
- the applicable Portability report
- Repository Baseline Setup Phase 1 satisfied for this target under
  `REPOSITORY_BASELINE_SETUP_GUIDELINES.md` §§3–4

Phase 1 produces a complete file with these parts:
- the governance and precedence section
- the repository layout
- the traceability ID rules
- the collaboration and stop gates
- the testing and quality gates the team already knows

Any engineering decision that depends on a not-yet-approved Requirement or Plan is written as an explicit marker `PENDING PHASE 2: <topic>`. Phase 1 must not present a pending marker as a decision.

### 3.2 Phase 2: Engineering finalization (pre-Implementation)

Phase 2 runs after Human Plan Approval of the first approved Implementation Plan and before the first Implementation invocation.
Repository Baseline Setup Phase 2 must be satisfied first for the same target,
approved Requirement and Plan. Verify durable result and waiver evidence, not
file existence. If it is not established, stop and present the explicitly
human-invoked Baseline Setup Agent; do not invoke it automatically.

It does three things:
- resolves every `PENDING PHASE 2` marker
- reconciles each engineering section with the current approved Requirement and Plan
- records any conflict for human decision

If the Plan and a proposed instruction conflict, the Plan wins, unless the instruction is a designated mandatory team rule. Record the difference and let the human decide whether the instruction text is adjusted. Do not change the Plan.

If an approved Plan weakens a mandatory team rule, Plan Verification should have reported it. Report it as a finding for the ordinary finding and corrective path. Do not silently weaken the rule to match the Plan. A Plan change follows Corrective Change control.

### 3.3 Refresh (reassessment)

Refresh the affected sections, or run a complete re-setup, in any of these cases:
- an explicit human request
- a new approved Requirement version that changes ID schemes, scope, roles, or constraints
- an approved Plan or corrective decision that changes architecture, the technology stack, the folder layout, the testing tooling, the deployment target, or shared-file boundaries
- a Master-baseline change that affects precedence or gate wording
- a Portability reassessment that reports instructions as stale

Reuse unchanged sections only when their inputs and fingerprints still match. There is no time-based repetition.

### 3.4 Waiver

A human authorized for the target project may decline a phase or refresh. The waiver must be explicit and attributable, and must name all of the following:
- the phase or refresh it covers
- the specific preconditions it covers
- the rationale
- the lapse condition

A waiver lapses at whichever comes first:
- its stated expiry
- the next §3.3 refresh trigger
- any change to `.github/copilot-instructions.md` after the waiver is recorded

Record the waiver verbatim in the Setup actor's records, together with the observed file fingerprint, or "absent". The Agent must not propose or infer a waiver as its own decision.

A waiver approves no file content. While it applies, any existing file is unapproved guidance and has no mandatory team rules. The file-content conditions in §9 apply only to `INSTRUCTIONS APPLIED`.

A missing file with no recorded waiver is an unmet precondition, not a waiver.

## 4. Interactive questionnaire

Use the host's interactive question facility, such as a structured ask-user form. Ask one topic per form, in the order below.

For every answer:
- Prefill it from evidence: the repository tree, manifests and project files, the existing CI, the Portability report, and the approved Requirement and Plan in Phase 2.
- Show the source of each prefill.
- Let the human accept, change, or mark the topic not applicable.

Skip a topic only when it is demonstrably not applicable, and record why. Do not proceed past an unanswered mandatory topic. In Phase 1, record it as `PENDING PHASE 2`. In Phase 2, stop and ask.

| # | Topic | Must capture |
|---|---|---|
| Q0 | Governance and precedence | The Masters' paths, the current approved Requirement and Plan locations, the exclusions for product work (governance paths not edited), the human-gate wording, and the stop-and-ask rule |
| Q1 | Repository and folder architecture | The exact root layout (backend, frontend, tests, docs), the feature-slice or module convention, folders that must not be created, and the rule that folders are created only when a Plan task needs them |
| Q2 | Requirement traceability | The canonical requirement-ID pattern taken from the approved Requirement (never invented), the backend test tag syntax (for example xUnit `[Trait("Requirement", "<ID>")]`), the frontend test syntax (for example `describe('<ID>: ...')`), Work Item ID tagging, and the developer traceability-view reminder with its path. The view is a non-authoritative developer aid; the governed report stays authoritative |
| Q3 | Backend engineering | The architecture style (for example Minimal APIs and vertical slices, Clean Architecture, controllers, or a mediator), validation, error and problem-details format, async and cancellation rules, security and tenancy, integrations, and logging |
| Q4 | Database | The engine and ORM, the mapping convention (for example no data annotations and per-entity configuration), the read-query rules (for example `AsNoTracking` and projection), pagination, raw-SQL safety, concurrency, and the migration-ownership rule (for example no migrations generated during feature work) |
| Q5 | Frontend engineering | Language strictness, the component model and props typing, server-state and data-fetching library, UI-state rules, the UI or styling library and design tokens, accessibility, and the API client |
| Q6 | Testing and quality gates | Test frameworks and mocking libraries, unit versus integration isolation (no real database, HTTP, or cloud calls in unit tests), the coverage thresholds and enforcement commands, determinism, and the mandatory allowed and denied cases. A threshold must never be lowered to pass |
| Q7 | Deployment and runtime | The hosting target, configuration sources and naming, the secrets policy, build-time versus runtime frontend configuration, file-system and storage rules, statelessness, telemetry, and health |
| Q8 | Collaboration guardrails | The shared files that need explicit developer confirmation before editing, the new-dependency rule, the breaking-change stop gate (published contracts and historical requirement-ID behavior), concurrent-work rules, and the end-of-session summary contents |

Answers to Q3–Q7 that depend on the approved Plan are expected to be `PENDING PHASE 2` in Phase 1 unless the team has already decided them. Record a team-level decision as a human-supplied constraint with its source.

## 5. Required content structure

The generated file must use this structure. Section names may be adapted to the target, but no section may be dropped without a recorded not-applicable rationale.

```text
# <Project> — Copilot Repository Instructions
<one-paragraph product and stack summary>

## 0. Precedence and governance (read first)
   - Masters win; then approved Requirement; then approved Plan; then this file
   - Mandatory team rules a Plan may tighten but not weaken (from Q2, Q6, Q8)
   - This file creates no approval, gate, or governance authority
   - Distinguish product, governance, and informational work; stop-and-ask rule
   - Never claim or infer human gates; never commit before Human Acceptance
   - Finding → Investigation → Corrective Decision route; immutable requirement versions
   - Governance paths (docs/ai/**, .github/agents/**, .github/skills/**) are not edited in product work;
     this file changes only through Project Instructions Setup
## 1. Repository layout                  (Q1)
## 2. Requirement traceability           (Q2)
## 3. Backend standards                  (Q3)
## 4. Database standards                 (Q4)
## 5. Frontend standards                 (Q5)
## 6. Testing and quality gates          (Q6)
## 7. Deployment and runtime             (Q7)
## 8. Team collaboration guardrails      (Q8, including the session summary)
```

Write the content as concrete, checkable instructions with short examples. Avoid vague principles. Keep the file focused, about 25 KB or less. Do not copy Master text; reference it by path.

## 6. Self-check before approval request

Before requesting Human Instructions Approval, confirm all of the following:
1. Every section either exists or has a recorded not-applicable rationale.
2. Every `PENDING PHASE 2` marker is listed. Phase 2 must leave zero markers.
3. No content conflicts with the Masters, or with the current approved Requirement or Plan. Otherwise, list the conflict.
4. No secret, credential, or personal data is present.
5. Every referenced path exists, or is labeled as a target layout to be created by Plan tasks.
6. The requirement-ID pattern matches the approved Requirement, or is `PENDING PHASE 2` when none exists.
7. The mandatory team rules are listed explicitly in §0 as rules a Plan may tighten but not weaken. The approval request names them so that the Human Instructions Approval designates them.

## 7. Approval, write, and readback

1. Present the full proposed content, its SHA-256 fingerprint, a diff against any existing file and its fingerprint, the questionnaire answers with their sources, the pending markers, the conflicts, and the self-check results.
2. Request Human Instructions Approval for that exact content and fingerprint. Accept only an explicit, attributable approval. Any edit invalidates the approval: regenerate the content, recompute the fingerprint, and request approval again.
3. Immediately before writing, confirm the target's current fingerprint equals the base presented for approval, or that the file is absent if it was absent. On a mismatch, stop with `CANNOT COMPLETE`.
4. Write only the approved bytes to `.github/copilot-instructions.md`. Read the file back and confirm the SHA-256 equals the approved fingerprint. On a mismatch or a partial write, stop and preserve the evidence.
5. Never commit or push. After `INSTRUCTIONS APPLIED`, the authorized human commits the file only through the separate, instructions-only commit route in `SDLC_ARTIFACT_GOVERNANCE.md` §3.6:
   - The commit contains only this file and, where authorized, the Setup records.
   - The committed blob matches the approved SHA-256.
   - The commit message references the Work ID and fingerprint.
   - A separate, explicit commit authorization is required.

   The file is never part of a feature change set, and no other process may edit it.

## 8. Records

Publish only actor-owned records under the adopted product persistence root (`docs/sdlc-records/product/`). Follow `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §30.1, including its Project Instructions Setup Work ID allocation (`instructions-setup-<uuid-v4>`, one per run, owned by the target-project scope):
- `attempt.json`
- checkpoints
- the report
- `result.json`

Across the immutable records for this invocation, bind the following as applicable to each stage. The pre-execution attempt records known inputs and marks future or unavailable values PENDING or UNKNOWN, and inapplicable values NOT APPLICABLE with a reason; it must not predict a human answer, approval, waiver, write or readback. Later checkpoints, report and result bind values when actually available and link prior records by identity, path and SHA-256; do not edit earlier final records in place.
- the Work ID and the prior Setup result reference, if any
- the phase (`PHASE-1`, `PHASE-2`, or `REFRESH`)
- the target repository identity and revision
- the Master baseline identity
- the Portability report reference
- the approved Requirement and Plan references for Phase 2
- the questionnaire answers with their sources
- the pending markers
- the conflicts
- the proposed and approved fingerprints
- the verbatim Human Instructions Approval or waiver
- the pre-write base hash
- the post-write readback hash
- the next permitted process

The result outcome is one of the following:

| Outcome | Meaning |
|---|---|
| `INSTRUCTIONS APPLIED` | Approved content was written and the readback matched |
| `WAIVED` | An explicit human waiver was recorded |
| `PENDING HUMAN APPROVAL` | Content is proposed but not yet approved; nothing is written |
| `CANNOT COMPLETE` | Inputs, authority, or capability are missing, or the base or readback did not match |

Only `INSTRUCTIONS APPLIED` or `WAIVED` satisfies the phase precondition.

## 9. Lifecycle preconditions

These preconditions are checked in two places, so that a direct invocation cannot bypass them:
- by the Orchestrator (O16.6)
- by the Requirement Analysis and Implementation processes in their own Skill preconditions and Requests

The Setup Agent does not enforce them itself. Each phase is satisfied by either of these:
- **(a)** an `INSTRUCTIONS APPLIED` result
- **(b)** a recorded waiver under §3.4 that covers that phase and its preconditions and has not lapsed

The file-content conditions below apply only to (a).

- **Before the first Requirement Analysis:** Phase 1 is satisfied for the current target and Master baseline.
- **Before the first Implementation:** Phase 2 is satisfied.
  - For (a), the result is bound to the current approved Requirement and Plan, the file contains no `PENDING PHASE 2` marker, and its current fingerprint equals the last approved fingerprint.
  - For (b), the waiver names Phase 2 and the current approved Requirement and Plan.
- **Before any later Implementation:** no refresh trigger in §3.3 is outstanding.
  - For (a), the current fingerprint must equal the last approved fingerprint. A mismatch means the instructions changed outside this mechanism; report it as a precondition failure for the human to resolve.
  - For (b), a file change lapses the waiver.

When a precondition fails, the next process does not start. Present `.github/agents/project-instructions-setup.agent.md` as the explicit, human-invoked entry point.
