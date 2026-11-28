# Repository Baseline Setup Guidelines

## 1. Purpose and authority

Repository Baseline Setup is a separately reported mechanism under the three
Master Governance documents. It is not part of the 52-core catalog, a product
Requirement or Plan, a finding disposition, or an approval authority. It
interactively identifies and, only after individual Human Baseline Approvals,
applies applicable target-repository baseline files. The Guideline, Prompt,
Request, Skill and Agent have distinct roles under the Masters.

The mechanism supports heterogeneous repositories and stacks. It does not
mandate a universal list of required files or automatically invoke any process.
The authorized human decides each candidate's applicability and, if
applicable, whether it is required or optional. The human confirms the target
platform, supported owners, protected rules and must-track paths.

## 2. Scope and prohibitions

Assess root and relevant nested `.gitignore` and `.gitattributes`; `.editorconfig`;
the hosting platform's supported CODEOWNERS or equivalent; platform-appropriate
pull-request and issue templates; tracked-file and secret-indicator reports;
and conditional Git LFS readiness and rules. Recommend `SECURITY.md` where
appropriate but never create or modify it or make its creation a phase gate.
Report remote enforcement, including
code-owner review and secret push protection, as enabled, disabled, or
unverified/not checked with source, scope and timestamp where available; never
change remote settings or make their modification a phase gate.

The actor may write only individually approved baseline target files and its
own authorized product-root records. It must not modify project instructions,
governance definitions, other product files, or another actor's records; run
project scripts, hooks, or unapproved external tools; invoke other Agents;
stage, untrack, delete, commit, push, renormalize, migrate, or rewrite history;
install or configure Git LFS; or self-approve. Existing rules, comments,
exceptions and unrelated content are preserved unless the exact diff is
individually approved. A proposed wholesale replacement needs an explicitly
approved wholesale diff and does not excuse loss of unrelated content.

## 3. Entry, phases and prospective transition

Establish the canonical target repository and root, source commit and relevant
working-tree state, adopted product persistence root, applicable adopted Master
baseline, reserved Work ID, authorized output scope, current actor capabilities,
explicit human stage-start and applicable predecessor results. Record the
Portability Assessment and its recorded human blocker dispositions before
Phase 1. The actor does not perform those processes or infer their decisions.

- **PHASE-1:** after Portability Assessment and recorded blocker dispositions,
  before Project Instructions Setup Phase 1 and the first Requirement Analysis.
- **PHASE-2:** after first Human Plan Approval, before Project Instructions
  Setup Phase 2 and the first Implementation. Bind the current approved
  Requirement and Plan and their approvals.
- **REFRESH:** after a material change to applicable baseline inputs, including
  repository layout, stack, tools, hosting platform, managed files or rules, or
  protected/must-track paths. An authorized additive Implementation change
  under section 10 uses its linked addendum, not an automatic refresh. Reuse an
  earlier conclusion only when scope, identities, applicable inputs and
  fingerprints still match.

For already-onboarded projects, apply the controls prospectively at the next
affected process start after this amendment is effective and the relevant
Master baseline is adopted. Do not invalidate past approvals or completed
stages or interrupt an active invocation. Establish Phase 1 for the project
using its current evidence even if Instructions Setup Phase 1 already occurred;
if a Plan is approved, establish Phase 2 before the next affected Implementation
as applicable. A completed historical stage is not rerun merely because of
this transition. Document the lifecycle position, applicable phases and
evidence; do not infer a waiver or automatically invoke Setup.

## 4. Work identity, classifications and results

Use the `repository-baseline-<uuid-v4>` Work ID and the allocation, collision,
reservation, actor-owned attempt and recovery contract in
`SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` section 30.1. Each phase or refresh
is a separate run unless it is an authorized continuation of that run.
Reference prior results and approved additive addenda by identity, path and
SHA-256. Record exact input identities and fingerprints.

Maintain a candidate inventory with evidence and the actual attributable human
decision for every file and check. Record classification as
`APPLICABLE-REQUIRED`, `APPLICABLE-OPTIONAL`, `NOT APPLICABLE`, `DEFERRED`, or
`UNRESOLVED` and outcome as `APPLIED`, `VERIFIED UNCHANGED`, `CHECKED`,
`PENDING`, `DEFERRED`, `WAIVED`, or `CANNOT COMPLETE`, as applicable.
`CHECKED` applies only to a check actually performed and passed; it is not a
file outcome. `VERIFIED UNCHANGED` is the no-write file outcome in section 5.
A classification of `DEFERRED` does not identify requiredness and therefore
remains unresolved for the phase gate.
The human must first decide required versus optional; only a named required
item can be waived. Record why a candidate is not applicable.

A phase is satisfied only by an integrity-bound result establishing that every
candidate was dispositioned; each required file is `APPLIED` and validated,
`VERIFIED UNCHANGED`, or covered by a current scoped waiver; each required
check is `CHECKED` or covered by a current scoped waiver; and no applicability or requiredness
decision remains unresolved. An explicitly completed all-not-applicable result
can satisfy the phase. Optional items may be deferred without blocking solely
for that reason. `PARTIAL`, `CANNOT COMPLETE`, pending, deferred or unresolved
required items do not satisfy the phase by themselves. Deferral is neither an
approval nor a waiver.

For checks without a target file, record their evidence, applicability and
human decision in the same inventory; do not mark an unperformed or failed
required check as applied or completed. A waived required check remains
unperformed and is not reported as passing.

## 5. Human decisions, approvals and waivers

Obtain a separate explicit attributable human decision for each applicable
file. Before any Human Baseline Approval, present its exact target path, exact
proposed bytes, readable diff, current base SHA-256 or verified absence, and
proposed worktree SHA-256. Bind the decision to those values, the run and scope.
For a file that is deferred, record the actual decision and reason; it is not
an approval. An approved file may be applied while another remains deferred.
No Human Baseline Approval substitutes for process initiation, Requirement
Approval, Review Approval, Plan Approval or Human Acceptance.

For an existing file requiring no change, present its exact current bytes,
target path, zero-change diff, base and proposed SHA-256, and obtain its own
explicit attributable approval. Recheck the approved path and current
fingerprint and complete the applicable validation without rewriting the file.
Only then record `VERIFIED UNCHANGED`, binding that approval, fingerprint and
validation evidence. A file's mere existence, prior approval for different
bytes, or an unperformed or failed check cannot establish this outcome.

A human authorized for the target may issue an explicit attributable waiver
only for named required files or checks and named affected phases. One decision
may list several named required items. Record exact scope, rationale, decision
source, creation time, expiry and lapse conditions, applicable fingerprints
or absence, and the approving authority. The expiry must be no later than 90
days after the decision; a shorter time or earlier condition controls. A
relevant input change lapses the waiver. Do not infer a waiver, waive an
undecided classification, or treat a waiver as file-content approval. A
waiver cannot waive another approval gate or authorize an unapproved write.

## 6. Evidence and platform checks

Distinguish source inspection, executed, reported and unverified evidence.
Identify the actual platform and its supported owner/template paths before
proposing platform-specific files. Confirm owners with the human; do not
invent users, teams, supported syntax or remote enforcement state.

Enumerate the repository root, applicable nested rule files, relevant
`.git/info/exclude`, global excludes, effective Git configuration and
attributes, and existing tracked paths, without exposing sensitive data.
Resolve the effective values and origins of relevant settings, including
`core.excludesFile`, `core.attributesFile` and `core.autocrlf`; report
conflicting or inaccessible configuration and redact unrelated sensitive
values.
Obtain human-designated representative must-ignore and must-track paths,
including relevant governance artifacts, Requirements, records, lockfiles
and intentional configuration where appropriate. Human designation does not
authorize publishing private or local-only records or forcing them into Git.
Report already-tracked matching files separately: adding an ignore rule does
not untrack them.

Use non-mutating `git check-ignore -v --no-index` and `git check-attr` checks,
with representative paths covering nested precedence, negation, tracked files
and must-track paths. Interpret the matched pattern, including a leading `!`,
rather than treating a verbose match or its exit status alone as proof that a
path is ignored; cross-check effective status without verbose output. Capture
relevant sources and actual results; a path that must remain trackable must not
be effectively ignored. Validate the
candidate rules in an isolated, non-production test context before approval
and the approved target after application. Do not stage files or invoke hooks
or arbitrary clean/smudge filters. If safe isolated validation or required
evidence is unavailable, report the limitation and do not claim a pass.
Account for platform support and effective Git configuration when interpreting
results. A check result is not proof of repository or history cleanliness.

The secret-indicator check is local and requires explicit human authorization
for each run and its scope. It must not transmit content externally or copy
matched values, excerpts, credentials or sensitive paths into reports,
records or chat. Report only redacted indicator types/counts and suitably
redacted paths when authorized, and explicitly state performed, not performed,
incomplete or unavailable with limitations. Do not assert clean history or
secret safety without evidence; `.gitignore` is not secret protection.

Before proposing LFS rules, determine applicability, check available local
readiness without installation or configuration, and explain capacity,
collaboration, hosting, tracked-file and migration/history risks. If
readiness is unavailable or unverified, record it; do not assert readiness.
No automatic LFS installation, configuration, file migration or history
rewriting is permitted.

## 7. Per-file application and failure recovery

Before each write, re-resolve the approved path and repository boundary,
ensure it is not redirected through an unapproved link, verify the approved
base fingerprint or absence and the exact approved proposal fingerprint, and
confirm current authority and non-conflicting writer context. Stop before that
write if any check fails. Apply only the approved bytes to the approved path,
then read back and verify the SHA-256. Never overwrite another actor's records.

Record each applied, deferred, waived, failed or pending item and exact
before/after fingerprints or absence, approval references, validation and
errors. Stop on a mismatch or write/readback error; publish an accurate
partial outcome when possible. Never claim rollback, completion or a clean
state without evidence. Preserve prior published records and files; recovery
requires explicit human direction and a new authorized attempt or continuation
under section 30.1. Recheck the base and approvals before any subsequent write.

## 8. Fingerprints and baseline-only commit

An approval and application bind exact working-file bytes and worktree SHA-256.
Separately record the expected committed Git blob SHA-256 and the proposed
transformation. If committed bytes would differ, obtain a separate explicit
attributable human approval of that exact expected blob fingerprint and
transformation before any commit; do not treat working-file approval as blob
approval. Do not run unapproved external filters or write objects merely to
derive a prediction. If the expected blob cannot be determined safely, stop.

After applicable approved files are applied and validated, a separate explicit
human commit authorization may authorize a baseline-only commit. It must bind
the Work ID, exact paths, approved worktree and expected blob fingerprints,
and scope. Only approved baseline files may be included; setup records,
project instructions and product changes are excluded. The Setup actor never
stages, commits or pushes. The authorized committer independently checks the
base, paths, staged content and expected blob hashes before committing, and
verifies committed blobs afterward; stop on mismatch and record any partial
outcome without rewriting history. A push, if desired, needs separate
authorization. This route does not change the instructions-only commit route.

## 9. Lifecycle checks and records

Before dependent phases or directly invoked processes, resolve durable results,
named current waivers, fingerprints, additive addenda and refresh triggers.
Phase 1 precedes Instructions Setup Phase 1 and first Requirement Analysis;
Phase 2 follows first Plan Approval and precedes Instructions Setup Phase 2
and first Implementation. Later affected work requires any triggered refresh.
Before each directly invoked product process, including planning, verification,
review and Requirement Update, determine from its actual scope and the changed
inputs whether it depends on an affected managed file or check. If so, enforce
the applicable prospective transition and refresh before starting; if
applicability cannot be established, stop and ask the human. Do not require
Phase 2 before first Human Plan Approval or merely to create or verify a
candidate Plan. The additive exception in section 10 remains non-circular.
For shared Finding Investigation and Corrective Change Decision processes,
apply this check only to affected product-subject work, never governance-only
work. Investigation or decision work solely to resolve the unmet baseline gate
may proceed without first satisfying that same gate; it neither satisfies
the gate nor starts a dependent process.
If the applicable gate is not established, stop and present the Baseline Setup
Agent as a human-invoked entry point; never invoke it automatically.

Publish only the actor's own invocation, checkpoints, report, result,
permitted evidence and actual human decisions when explicitly supplied or
authorized for transcription, under the adopted product root and section
30.1. Bind target, source state, platform, input and per-file evidence, exact
decisions and approval sources, waiver scopes and lapses, and all before/after
fingerprints. Preserve unverified and not-performed checks, partial effects,
recovery and next permitted action. Final records are immutable. Never copy
secret values or infer a substantive human decision.

## 10. Subsequent change control

Implementation may add `.gitignore` entries only when the current approved
Plan explicitly authorizes that task and normal Implementation controls and
shared-file gates are satisfied. Before the addition, establish the applicable
baseline result and current fingerprint. Verify that additions neither weaken
protected rules nor ignore designated must-track paths under effective and
nested rules. Record an actor-owned addendum or link in the Implementation
evidence binding the prior baseline fingerprint, exact addition, resulting
fingerprint and must-track validation. The addendum advances only the affected
file's baseline reference and does not invalidate the entire baseline or
trigger a circular precondition.

Removal or weakening of protected rules and changes to other managed baseline
files require an explicitly initiated Baseline Setup refresh and individual
approval before application. Plan Verification identifies proposed weakening
and verifies that a Plan introducing generated output specifies appropriate
ignore handling or explicitly justifies why none is needed. A finding follows
the ordinary finding and corrective route; no direct corrective implementation
is authorized.
