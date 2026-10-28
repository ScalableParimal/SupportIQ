# SDLC Traceability and Change Control

## 1. Purpose

This document defines the traceability and change-control rules for the governed AI-assisted Software Development Life Cycle (SDLC).

It establishes:

- how governed artifacts are connected,
- how requirements are traced through implementation,
- how findings are traced through investigation and corrective action,
- how changes to approved artifacts propagate downstream,
- how the current approved artifact is determined,
- when re-verification is required,
- when re-review is required,
- how corrective changes are controlled,
- how governance shortcuts are prevented.
- how governed SDLC execution mechanisms are traced to their governing artifacts,
- how changes to Skills and SDLC Process Agents are controlled and propagated.

This document complements:

`docs/ai/sdlc/SDLC_GOVERNANCE.md`

and:

`docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md`

The overall lifecycle is defined by `SDLC_GOVERNANCE.md`.

Artifact authority and lifecycle responsibilities are defined by `SDLC_ARTIFACT_GOVERNANCE.md`.

This document defines the traceability and change-control relationships between those artifacts.

---

## 2. Core Traceability Principle

Every downstream governed artifact must be traceable to the applicable current approved upstream artifact.

The fundamental relationship is:

    Requirement
       ↓
    Requirement Analysis
       ↓
    Requirement Analysis Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Requirement Approval
       ↓
    Approved Requirement
       ↓
    Implementation Plan
       ↓
    Implementation Plan Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Approved Implementation Plan
       ↓
    Implementation
       ↓
    Implementation Self-Check
       ↓
    Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance
       ↓
    Commit / Push

Traceability must allow a reviewer to determine:

- where the business requirement originated,
- which requirement version was approved,
- which implementation plan was based on that requirement,
- which implementation was based on that plan,
- which verification and review results apply to that implementation,
- which human approval or acceptance gates were satisfied.

---

## 3. Traceability Does Not Mean Approval

Traceability establishes relationships between artifacts.

Traceability does not itself establish:

- Requirement Approval,
- Plan Approval,
- Verification,
- Review,
- Human Acceptance.

For example:

    Requirement
       ↓
    Implementation Plan

does not mean the Requirement or Plan is approved.

The applicable approval gates must still be satisfied.

---

## 4. Required Upstream Traceability

The following relationships are mandatory.

### 4.1 Requirement Analysis

Requirement Analysis must trace to:

- the Requirement being analysed,
- applicable human decisions,
- relevant requirement context.

### 4.2 Requirement Analysis Verification

Requirement Analysis Verification must trace to:

- the current Requirement,
- the current Requirement Analysis,
- applicable human decisions,
- relevant verification evidence.

### 4.3 Approved Requirement

The Approved Requirement must be traceable to:

- the Requirement,
- the Requirement Analysis,
- Requirement Analysis Verification,
- resolved findings and decisions,
- Human Requirement Approval.

### 4.4 Implementation Plan

The Implementation Plan must trace to:

- the current Approved Requirement,
- applicable architecture,
- applicable engineering guidelines,
- repository constraints,
- relevant technical evidence.

### 4.5 Implementation Plan Verification

Implementation Plan Verification must trace to:

- the current Approved Requirement,
- the complete current Implementation Plan,
- applicable architecture,
- applicable engineering guidelines,
- relevant technical evidence.

### 4.6 Approved Implementation Plan

The Approved Implementation Plan must be traceable to:

- the Implementation Plan,
- Implementation Plan Verification,
- resolved findings and decisions,
- Human Review Approval,
- Human Plan Approval.

The Human Review Approval record must reference the Human Review package that was submitted for that approval. The Human Review package is a review submission, not a separate governed artifact.

### 4.7 Implementation

Implementation must trace to:

- the current Approved Requirement,
- the current Approved Implementation Plan,
- the actual repository state,
- implemented task or component context where applicable.

### 4.8 Implementation Self-Check

Implementation Self-Check must trace to:

- the implementation being checked,
- the current Approved Requirement,
- the current Approved Implementation Plan,
- test/build/validation evidence.

### 4.9 Implementation Verification

Implementation Verification must trace to:

- the current Approved Requirement,
- the current Approved Implementation Plan,
- the complete current implementation,
- verification evidence,
- applicable architecture and engineering guidelines.

### 4.10 Implementation Review

Implementation Review must trace to:

- the current Approved Requirement,
- the current Approved Implementation Plan,
- the complete current implementation,
- Implementation Verification results,
- applicable engineering guidelines,
- review evidence.

### 4.11 Human Acceptance

Human Acceptance must be traceable to:

- the accepted implementation state,
- applicable Implementation Verification results,
- applicable Implementation Review results,
- resolved material findings,
- required corrective changes.

---

## 5. Current Approved Artifact

A downstream activity must always use the current approved version of the applicable upstream artifact.

An artifact is the current approved artifact only when:

1. the applicable artifact exists,
2. required verification has been completed,
3. required findings and decisions have been resolved,
4. the required human approval has been obtained,
5. the artifact has not subsequently been superseded by another approved version.

Examples:

    Current Approved Requirement
            ↓
    Implementation Planning

    Current Approved Requirement
            +
    Current Approved Implementation Plan
            ↓
    Implementation

A previous approved version must not be treated as current after a newer approved version becomes effective.

---

## 6. Determining the Current Approved Artifact

When multiple versions of an artifact exist, determine the current approved artifact using the following order:

1. Identify the latest artifact version.
2. Confirm that the required verification was completed.
3. Confirm that required findings and decisions were resolved.
4. Confirm that required human approval was obtained.
5. Confirm that the artifact has not been superseded.
6. Use that artifact as the current approved source for downstream work.

If these conditions cannot be established, the artifact must not be assumed to be approved.

The uncertainty must be identified and routed through the applicable governance process.

---

## 7. Requirement-to-Implementation Traceability

The complete requirement-to-implementation chain is:

    Business Requirement
       ↓
    Requirement Analysis
       ↓
    Requirement Analysis Verification
       ↓
    Human Requirement Approval
       ↓
    Approved Requirement
       ↓
    Implementation Planning
       ↓
    Implementation Plan Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Approved Implementation Plan
       ↓
    Implementation
       ↓
    Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

Every implementation task should be explainable in terms of:

- which approved requirement it supports,
- which approved plan task defines it,
- which implementation artifact realizes it,
- which verification evidence confirms it.

---

## 8. Requirement Change Control

A material Requirement change must not be introduced directly through implementation.

The governed path is:

    Requirement Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision
       ↓
    Requirement Update
       ↓
    Requirement Analysis
       ↓
    Complete Requirement Analysis Verification
       ↓
    Resolve Findings / Decisions
       ↓
    Human Requirement Approval
       ↓
    Plan Impact Evaluation
       ↓
    Implementation Planning / Plan Update as Required
       ↓
    Implementation Plan Verification as Required
       ↓
    Resolve Findings / Decisions as Required
       ↓
    Human Review Approval where required
       ↓
    Human Plan Approval
       ↓
    Implementation

The new Requirement becomes the current Approved Requirement only after the required approval gate is completed.

---

## 9. Requirement Change Impact

When the Requirement changes, the Implementation Plan must not automatically be assumed to remain valid.

The plan must be evaluated for:

- changed scope,
- changed business rules,
- changed acceptance criteria,
- changed dependencies,
- changed interfaces,
- changed data requirements,
- changed validation requirements,
- changed testing requirements,
- changed architecture implications,
- changed implementation tasks.

If the plan is materially affected, it must be updated through the governed plan-change process.

Record the previous and resulting Requirement references, changed requirement sections, affected Plan tasks and dependencies, implementation retained or requiring rework, affected verification and review results, unresolved impact, and required downstream processes. Bind the assessment to the relevant source and target versions. An unresolved impact must not be treated as compatibility or authorization to continue affected work.

---

## 10. Implementation Plan Change Control

A material Implementation Plan change must not be applied informally during implementation.

The governed path is:

    Plan Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision
       ↓
    Proposed Plan Update
       ↓
    Required Human Approval
       ↓
    Apply Approved Plan Update
       ↓
    Complete Implementation Plan Verification
       ↓
    Resolve Verification Findings / Decisions
       ↓
    Human Review Approval
       ↓
    Human Plan Approval
       ↓
    Implementation

The updated plan becomes the current Approved Implementation Plan only after the required approval gate.

---

## 11. Plan Change Impact

When the Implementation Plan changes, the implementation must be evaluated for impact.

The evaluation must consider:

- completed implementation tasks,
- pending implementation tasks,
- affected components,
- architecture,
- APIs and contracts,
- data and persistence,
- validation,
- testing,
- configuration,
- dependencies,
- acceptance criteria.

If existing implementation no longer conforms to the updated plan, corrective implementation is required through the governed implementation process.

Record a source-Plan-to-target-Plan mapping for completed, partial, and pending tasks. Identify retained work with supporting evidence, rework-required work, added or removed tasks, split or merged task relationships, dependency effects, and unresolved dispositions. Retention of implementation is not retention of current verification. Preserve complete Implementation Verification after an applicable Plan update and the required review process.

---

## 12. Implementation Change Control

Implementation changes may occur during normal implementation or as corrective implementation.

A material corrective implementation must use the current Approved Implementation Plan.

The governed path is:

    Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision & Plan Update
       ↓
    Required Human Approval
       ↓
    Implement Approved Change
       ↓
    Complete Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

Implementation must not be corrected directly from a finding without the applicable governed decision and approval process.

---

## 13. Implementation Verification Change Control

Implementation Verification evaluates the complete current implementation.

If it identifies a material issue:

    Implementation Verification Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision & Plan Update
       ↓
    Required Human Approval
       ↓
    Corrective Implementation
       ↓
    Complete Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

The corrective implementation must be verified as a complete current implementation.

Verification must not be limited only to the corrected lines or files when the governing verification requires complete-scope verification.

---

## 14. Implementation Review Change Control

If Implementation Review identifies a material issue:

    Implementation Review Finding
       ↓
    Finding Investigation
       ↓
    Corrective Change Decision & Plan Update
       ↓
    Required Human Approval
       ↓
    Corrective Implementation
       ↓
    Complete Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

The review finding must not be corrected directly inside the review activity.

---

## 15. Finding Traceability

Every material finding must be traceable to:

- the activity that discovered it,
- the affected artifact,
- the affected component or section,
- the evidence supporting the finding,
- the Finding Investigation,
- the corrective decision,
- any required human approval,
- the implemented correction,
- the resulting verification,
- the resulting review where applicable.

The traceability chain is:

    Finding
       ↓
    Investigation
       ↓
    Corrective Decision
       ↓
    Affected Artifact
       ↓
    Approved Change
       ↓
    Corrective Implementation where applicable
       ↓
    Re-verification
       ↓
    Re-review where applicable
       ↓
    Human Acceptance where applicable

---

## 16. Finding Investigation Scope

Finding Investigation must consider the complete relevant context of the affected governed artifact.

Task IDs, recently changed files, or the location where a finding was detected are context only.

They must not unnecessarily restrict investigation scope.

For example, a finding identified in one implementation file may require investigation of:

- related application services,
- domain rules,
- persistence,
- API contracts,
- tests,
- configuration,
- requirement,
- implementation plan.

The investigation scope must be appropriate to the actual finding.

---

## 17. Corrective Decision Traceability

The Corrective Change Decision & Plan Update must identify:

1. Finding Source
2. Affected Artifact
3. Affected Components / Sections
4. Finding Investigation
5. Applicable Approved Requirement
6. Current Approved Implementation Plan where applicable
7. Whether the finding is accepted or rejected
8. Whether corrective change is required
9. Whether the Requirement changes
10. Whether the Implementation Plan changes
11. Required human approval
12. Required next process

The corrective decision must not silently introduce a new business requirement.

---

## 18. Requirement Change vs Plan Change

The following distinction must be maintained.

### Requirement Change

A Requirement change changes what the system is expected to do.

Examples include changes to:

- business behavior,
- business rules,
- scope,
- acceptance criteria,
- mandatory business constraints.

Requirement changes must follow the Requirement change process.

### Plan Change

A Plan change changes how the approved Requirement will be implemented.

Examples include changes to:

- implementation tasks,
- technical sequencing,
- component allocation,
- persistence approach,
- testing approach,
- technical design,
- implementation dependencies.

A Plan change must not silently change the business Requirement.

---

## 19. Implementation Deviation vs Requirement Change

Not every implementation problem is a Requirement change.

The following distinction must be maintained:

### Implementation Deviation

The implementation does not conform to the current Approved Requirement or Approved Implementation Plan.

The correction should restore conformance unless a governed decision determines that the Requirement or Plan itself must change.

### Requirement Change

The approved business expectation itself must change.

This requires the Requirement change process.

### Plan Change

The business Requirement remains valid, but the approved technical implementation approach must change.

This requires the Plan change process.

---

## 20. Verification After Corrective Change

After a corrective implementation:

> Complete Implementation Verification is required.

Verification must evaluate the complete current implementation against:

- the current Approved Requirement,
- the current Approved Implementation Plan,
- applicable architecture,
- applicable engineering guidelines,
- relevant repository constraints,
- available evidence.

Verification must not assume that the corrective change is correct merely because the changed test passes.

---

## 21. Review After Corrective Change

After corrective implementation and complete Implementation Verification, Implementation Review must be performed when required by the applicable review process.

The review must evaluate the complete current implementation.

The review must not be restricted to:

- the corrected file,
- the corrected method,
- the finding location,
- the changed task.

The correction may have downstream technical or quality effects.

---

## 22. Re-verification Is Not Optional

A previous verification result does not automatically remain valid after a material change.

If a governed artifact or implementation materially changes after verification:

- the affected verification must be repeated,
- the current approved upstream artifacts must be used,
- the verification must consider the complete applicable current scope.

A previous verification report may remain as historical evidence but does not replace current verification.

---

## 23. Re-review Is Not Optional When Required

A previous review result does not automatically remain valid after a material corrective implementation.

Where the applicable review process requires re-review:

- review the complete current implementation,
- use the current Approved Requirement,
- use the current Approved Implementation Plan,
- consider the latest Implementation Verification,
- consider all relevant findings and corrective changes.

---

## 24. No Stale Approval

An approval applies to the artifact version that was approved.

If that artifact materially changes, the previous approval must not be treated as approval of the changed version.

Examples:

    Approved Requirement v1
            ↓
    Requirement changes
            ↓
    v1 approval does not automatically approve v2

    Approved Plan v1
            ↓
    Plan changes
            ↓
    v1 approval does not automatically approve v2

A new approval must be obtained where required.

---

## 25. No Stale Verification

A verification result applies to the artifact state that was verified.

If the verified artifact materially changes, the previous verification must not automatically be treated as verification of the changed state.

The changed current artifact must be verified according to the applicable verification process.

---

## 26. No Direct Finding-to-Code Shortcut

The following process is prohibited:

    Finding
       ↓
    Code Change
       ↓
    Tests Pass

Passing tests does not replace:

- Finding Investigation,
- Corrective Change Decision,
- required Human Approval,
- complete Implementation Verification,
- required Implementation Review,
- Human Acceptance.

The governed process must be followed.

---

## 27. No Direct Plan-to-Code Shortcut for Corrective Work

A corrective change must not be implemented against an unapproved plan.

The required relationship is:

    Corrective Decision
       ↓
    Plan Evaluation
       ↓
    Plan Update if Required
       ↓
    Required Human Approval
       ↓
    Plan Verification
       ↓
    Current Approved Implementation Plan
       ↓
    Corrective Implementation

If the current Approved Implementation Plan remains valid, implementation may proceed using that plan without unnecessary plan modification.

---

## 28. Task ID Traceability

Task IDs provide implementation traceability.

They may identify:

- planned work,
- implemented work,
- affected work,
- related findings,
- verification context.

Task IDs do not replace:

- Requirement traceability,
- Plan traceability,
- verification,
- review,
- human approval,
- human acceptance.

A task marked complete does not by itself mean that the implementation is verified or accepted.

Executed Plan tasks must have unique, stable Plan-local identifiers qualified by Plan identity and version. Preserve task relationships across amendments; do not unnecessarily renumber tasks. Reusing an identifier does not establish unchanged criteria or dependencies. Record replacements, splits, merges, removals, and their impact explicitly.

---

## 29. Complete-Scope Verification Principle

For activities defined as complete-scope verification:

> The complete current governed artifact is the verification target.

Task IDs, recently changed files, or recently corrected components may help focus the investigation but must not unnecessarily restrict the verification target.

This principle applies particularly to:

- Implementation Plan Verification,
- Implementation Verification,
- Implementation Review where complete implementation review is required.

---

## 30. Evidence Traceability

Evidence should be classified where applicable as:

- executed evidence,
- source inspection evidence,
- reported evidence,
- unverified information.

Evidence must not be represented as stronger than its actual source.

For example:

- A reported test result is not the same as an independently executed test.
- A source inspection observation is not the same as runtime evidence.
- An AI assumption is not verified evidence.
- A previous verification result is not current verification after a material change.

### 30.1 Durable Execution Records and Recovery

#### Purpose and applicability

Existing governed process requests, reports, evidence, human-gate records, and their execution metadata must be durably recorded when they are used for execution tracking or recovery. Agent memory, conversation history, session storage, and temporary files must not be the sole recovery source.

These records do not create a new artifact category, lifecycle stage, approval authority, or execution-state authority. Publication permissions are defined by section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md.

#### Approved persistence convention

The fixed repository-relative persistence roots are `docs\sdlc-records\governance\` for governance-subject records and `docs\sdlc-records\product\` for product-subject records. Their adoption requires explicit Human governance decision and approval through governed change control; a suggested directory or process request alone does not approve this convention. Execution context must identify the applicable root, stable feature/work identifier, actor-owned record scope, and resolvable adoption or applicable authorization evidence before invocation publication and execution.

**Root adoption and first-use order.** The first-use governance-root bootstrap in this section is limited to adopting `docs/sdlc-records/governance/` and authorizing the explicitly scoped initial complete Governance Audit. It does not adopt `docs/sdlc-records/product/`, authorize product-process records, or authorize a Portability Assessment. Before any product-process record is published or a Portability Assessment is invoked, the product root must be separately and explicitly adopted by an attributable, independently resolvable Human governance decision bound to the canonical target repository/state, exact product root, purpose and scope, and applicable actor-owned record scope. Product-root adoption is distinct from the process stage-start; both must be established before product-process publication or assessment. A governance-root bootstrap/Audit may proceed without the product root, but it must not create or imply product-root adoption. Existing records are not retroactively invalidated by this rule; new invocations follow the adopted root and current authorization.

For a repository receiving inherited Master files, the copied bytes are candidate text, not an adopted baseline. The target must audit the candidate framework in that target repository and complete the required assurance before a separate Human decision adopts the exact three-file Master set. Source-repository approval, root adoption, audit, or execution history does not transfer.


#### First-use governance-root bootstrap

This subsection defines a limited first-use route for establishing the governance persistence convention when its normal precondition cannot yet be satisfied. It applies only when all of the following are established: the repository identity is known; the applicable governance persistence root has not previously been established as adopted; no valid adoption or authorization evidence is available under that root; and no governance process invocation or record publication has yet occurred for the bootstrap work.

Before any Governance Audit, Governance Remediation, governance investigation, or other governance-process invocation begins, an attributable Human governance decision must explicitly authorize the bootstrap. The decision must identify:

- the canonical repository identity and the repository state to which the authorization applies, including the relevant commit or other resolvable source-state identity;
- the exact persistence root being adopted, which for governance-subject records is `docs\sdlc-records\governance\`;
- the purpose and bounded scope of the bootstrap, including authorization for the initial bootstrap record publication and the explicitly identified process stage, subject to the existing stage-ordering and stage-start requirements;
- the stable governance Work ID, the designated initial process actor, and the exact actor-owned record scope;
- the applicable Master Governance source paths and their SHA-256 fingerprints, where the decision concerns their current applicability;
- the authorized approval-evidence location and the method by which another actor can resolve and validate that evidence; and
- any limitations, conditions, and one-time restrictions on the authorization.

The bootstrap decision must be recorded as an existing Human governance decision or approval through an attributable, independently resolvable approval channel that does not depend on prior publication under the not-yet-adopted governance root. Preserve the actual decision, its source, scope, conditions, and integrity information. The decision evidence must be retained at its authorized source and linked from the first bootstrap attempt record once publication becomes permitted. This provision does not create a new governed artifact category, a second persistence root, or a substitute approval authority.

##### Default lightweight evidence route for GitHub-hosted repositories

To avoid requiring a separate approval platform or protected-branch configuration solely for first-use bootstrap, a GitHub-hosted repository may use an attributable Human authorization comment or review on a GitHub issue or pull request in the canonical repository. Prefer a pull-request review when the authorization is already being handled through a pull request; an issue comment is an acceptable lightweight alternative when no suitable pull request exists. The GitHub record is the external evidence source; copying its text into the governance record root does not create authority. A protected branch is not, by itself, a prerequisite for using this evidence route.

The decision-maker must be the repository owner, an administrator, or another Human whose authority to make this repository's governance decision is independently established. Validate the account and its authority using the GitHub repository interface or an authenticated GitHub CLI session. The existence of a GitHub account, public profile, commit author string, or URL alone does not establish that the author is authorized. If identity or authority cannot be verified, stop.

Before requesting authorization, identify the canonical repository, exact full commit SHA, SHA-256 fingerprints of all three Master Governance files, exact governance persistence root, proposed stable Work ID, designated initial actor, and the limited scope of the first invocation. The repository working tree must be clean when the authorization is issued. Generate the candidate Work ID and collision-check it against both `docs\sdlc-records\governance\` and `docs\sdlc-records\product\` before requesting authorization. This pre-check does not reserve the ID. Recheck for collisions immediately before first publication; the successful no-overwrite publication of the first `attempt.json` reserves the Work ID. If a collision or repository-state mismatch is found, do not publish; issue a new decision bound to the corrected ID or repository state.

The authorization comment or review must explicitly state the decision and include the repository identity, full commit SHA, all three Master file paths and SHA-256 fingerprints, governance record root, stable Work ID, designated actor, authorized initial stage (`complete Governance Audit`), exact permitted initial record publication, output scope, and the one-time limitation. The exact comment/review permalink is captured in the first attempt record after GitHub creates it; do not require a comment to contain a permalink to itself. The decision must explicitly exclude corrective changes, approval of proposed changes, independent verification, independent review, subsequent process starts, and initial Master-baseline adoption. Those activities remain subject to their own existing stage-start, approval, actor-separation, assurance, and adoption controls. Approval of a governance amendment and authorization to bootstrap the first audit are distinct decisions; neither substitutes for the other.

Copy-ready decision text (replace every bracketed field; post it as an authenticated comment or review in the canonical repository):

```text
HUMAN GOVERNANCE DECISION — ONE-TIME FIRST-USE BOOTSTRAP

Decision: I AUTHORIZE the one-time bootstrap and ADOPT the specified governance persistence root for this repository state.
Canonical repository: [owner/repository]
Authorized repository state: [full commit SHA]
Master Governance fingerprints:
- docs/ai/sdlc/SDLC_GOVERNANCE.md: SHA-256 [hash]
- docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md: SHA-256 [hash]
- docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md: SHA-256 [hash]
Governance record root: docs/sdlc-records/governance/
Stable Work ID: [collision-checked ID]
Designated initial actor: [actor identity]
Authorized stage: complete Governance Audit only
Authorized initial publication: the designated actor's own first attempt.json and permitted actor-owned audit records under the governance root, referencing this decision
Scope and limits: one-time authorization for this repository state and Work ID only. This does not authorize remediation, source changes, change approval, verification, review, another process start, or baseline adoption. Any repository-state, Master-fingerprint, actor, root, Work ID, or scope mismatch invalidates this authorization.
```

Retain the canonical URL/permalink to the actual GitHub decision, its author identity and timestamp, and enough source metadata to re-open and validate it. The first attempt record must link to that external source and record the exact commit and Master fingerprints. If the evidence source is unavailable, edited in a way that makes the decision ambiguous, revoked, or otherwise no longer verifiable, stop and reconcile; do not reconstruct the decision from conversation history.

If no such independently resolvable approval evidence can be established, the process must stop. A conversational request, a directory's existence, an empty or populated records directory, a generated Work ID, a commit, a fingerprint, or an agent's assertion does not by itself establish the required Human decision.

The explicit bootstrap decision may adopt the specified governance persistence root for the identified repository and authorize the bounded bootstrap and the explicitly identified record publication; it does not waive any prerequisite for a Governance Audit or any other process stage.

Before publishing the initial invocation, the designated actor must validate the decision evidence, repository identity and state, root, Work ID, actor identity, and record scope against the decision. The actor may then publish only its own invocation metadata and other records permitted by section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md within the expressly authorized scope. The initial audit must assess the applicable governance framework under the ordinary audit criteria; the bootstrap authorization does not relax its assessment scope, evidence requirements, findings criteria, or outcome conditions.

After the initial invocation, all subsequent invocations and publications must follow the normal persistence, authorization, integrity, immutability, recovery, and governed change-control requirements. This bootstrap provision is not a standing exemption, does not authorize an actor to create or infer Human decisions, and does not permit an audit or other process to establish its own prior authorization.

Select the root by the subject of the governed work, not by the executing Skill or Agent. Governance Audit, Governance Remediation, and governance-focused investigations and corrective decisions use the governance root. Product lifecycle processes, product Orchestrator coordination, and product-focused investigations and corrective decisions use the product root. For cross-feature product work, establish one explicitly authorized owning feature scope and reference other affected features without duplicating the canonical report. If ownership or governance/product classification is mixed, ambiguous, or unestablished, stop and obtain a scoped Human decision before invocation publication or execution; do not infer a root.

Within the applicable root, use a stable feature/work identifier and the following relative structure. The `<feature-id>` placeholder also represents the stable governance-work identifier for governance-subject records:

```text
<feature-id>\
    attempts\
        <attempt-id>\
            attempt.json
            checkpoint-<sequence>.json
            report.md
            result.json
            attachments\
    human-gates\
        <gate-id>\
            request.json
            decisions\
                <decision-id>.json
            attachments\
```

Structured metadata uses UTF-8 JSON with an identified schema version. Existing human-readable reports use UTF-8 Markdown. Necessary evidence retains an appropriate native format. A report has one canonical body; metadata references that body rather than creating a second authoritative report.

Feature identifiers are stable repository-unique lowercase kebab-case identifiers. Attempt, gate, and decision identifiers combine a UTC creation timestamp with a UUID. Checkpoints have a zero-padded sequence local to the attempt. Record identity, not timestamp ordering, establishes references. Names must not be changed merely because a feature title or Plan version changes.

Governance work identifiers follow the same stable repository-unique lowercase kebab-case identity rules. Feature or work display names may change without changing identifiers or record locations. Remediation cycle identities remain traceable in the applicable records and reports; directory grouping does not replace them.

This root separation becomes effective for new attempts and new gates after the specifically approved correction is applied, independently verified, and confirmed by the required complete Governance Audit. Attempts and gates established before that effective boundary retain their authorized original locations, including their subsequent checkpoints, results, attachments, and supplied decisions. Published historical records remain immutable and resolvable at their existing paths; new records may reference them. Do not move, rewrite, or duplicate canonical historical records under this correction. Any later physical migration requires a separate Human-approved governed migration and reference-preservation proposal.

Before publishing an invocation, the actor must validate that the designated output location is within its authorized scope under the applicable root and stable identifier, or within an explicitly retained pre-effective attempt or gate scope. Missing, conflicting, or mismatched routing context blocks execution. Existing publication, integrity, recovery, retention, and authority rules remain unchanged. Necessary evidence must be retained within, or resolvably referenced with integrity information from, the applicable attempt or gate records; this directory policy does not relocate authoritative Requirements, Plans, source files, or every transient build output.

#### Governance Work ID allocation and reservation

For a new governance enhancement, allocate its Work ID before investigation or any other process invocation. Unless continuing an already-authorized existing Work ID, generate `gov-enhancement-<uuid-v4>` using a cryptographically secure UUIDv4 source, rendered lowercase with hyphens. This remains a repository-unique lowercase kebab-case identifier. Do not include personal or confidential request text in the identifier.

Before reservation, search `docs/sdlc-records/governance/` and `docs/sdlc-records/product/` for the complete candidate identifier in directory names and structured record `work_id` or feature-identity fields. If it already identifies another work item, discard it and generate a new UUIDv4. Reserve the identifier by atomically publishing the first no-overwrite `attempt.json` at `docs/sdlc-records/governance/<work-id>/attempts/<attempt-id>/attempt.json` under the existing section 30.1 publication contract. If the work directory or attempt record already exists and is not an authorized continuation of this same Work ID, do not overwrite it; generate a new ID and repeat the collision check. The first published attempt record is the reservation; do not create a separate registry or state artifact.

Once reserved, retain the exact Work ID across retries and lifecycle stages. Put it in each attempt, request, report, result, evidence manifest, and human-gate request/decision; every cross-stage handoff must reference the Work ID plus the source record identity, location, and fingerprint. Attempt, gate, and decision IDs remain separately generated timestamp-plus-UUID identities. Never derive a new Work ID from a changed title, branch, or attempt number. The existing Work ID `governance-amendment-applier-verifier-reviewer-readiness` is preserved as an already-established identity and is not regenerated under this prospective allocation rule.

#### Governance amendment stage invocation and handoff

Each governance-amendment stage is a separate actor invocation with its own pre-execution attempt record, explicitly supplied human stage-start instruction, and actor-owned report/result/evidence. Patch approval authorizes only the exact application described by that approval; it does not start the Application, Verification, Review, or Audit process and is not a Process Initiation response. The stages are: proposal preparation; exact Human Approval; Application; independent Verification; independent Review; complete Governance Audit; and, for Master changes only, separate prospective-baseline adoption. A human must explicitly initiate each process stage after reviewing the preceding handoff. Retries and restarts require a fresh stage-start instruction; no response is inferred, reused, or automatically propagated.

The Application invocation requires the exact current Human Approval decision and its own fresh stage-start instruction. Verification may be separately initiated only after a complete Application result exists; Review only after a passing independent Verification result; Audit only after passing Review. Each request must bind the same Work ID, current repository state, predecessor report/result identities and fingerprints, applicable approval and target fingerprints, assigned actor identity, scope, and authorized output location. A missing, stale, failed, or conflicting predecessor blocks the next stage. The receiving actor validates the handoff before execution and publishes only its own records. These direct human-initiated governance stages do not invoke or extend the product SDLC Process Orchestrator; its existing initiation rules and product scope remain unchanged. A stage-start instruction is invocation authorization only, never Human Approval, Review Approval, acceptance, or baseline adoption.


#### Governance Audit and Remediation reporting and handoff

Governance Audit and Governance Remediation must distinguish the complete canonical report, the human-facing summary, and the downstream handoff. This distinction changes presentation, not required assessment scope, evidence, findings, authority, independence, approval gates, or completion criteria.

The canonical report must retain every required report element. Compact tables, coverage matrices, shared explanations, and resolvable evidence references may replace repetitive prose. Passing-artifact assessments must retain identifiable coverage and conclusions. Every material finding must retain its required fields and supporting evidence. Decisions, approvals, corrections, verification results, limitations, unresolved items, and cycle history must remain traceable. Do not duplicate another actor's report body; reference the actor-owned report and evidence needed to support the current conclusion.

The normal human-facing summary must identify the cycle or attempt, assessed scope, required counts, separately assessed mechanisms, actual outcome, all unresolved finding IDs and severities, material limitations, pending human decisions or approvals, next permitted process, and canonical report location. Decision requests must include sufficient evidence, options, exact proposed correction or subject, approval scope, and conditions for an informed decision. Do not apply a fixed length limit that omits material information. Supply additional detail when requested.

A downstream handoff must identify the originating process and actor, cycle or attempt, applicable input versions or fingerprints, canonical report and result references with integrity information, relevant finding dispositions, pending gates or blockers, and next permitted process. Include relevant excerpts only where needed. The receiving actor must resolve the referenced records, establish applicability to the current state, and inspect the evidence required for its assigned process. A summary or upstream assurance is not independent verification.

##### Non-circular Governance Audit-to-Remediation integrity chain

For the final Audit result relied on by a Governance Remediation cycle, preserve this directed chain using only the existing actor-owned invocation, report, evidence, and result records:

1. The Audit report identifies the current attempt, canonical report, result, and evidence records by path and stable identity. It fingerprints source and other records whose final bytes are available before report publication, but does not claim a final fingerprint for its own immutable report or the result that is published later.
2. After the Audit report and evidence are durably published, the Audit result binds the final Audit report by path, identity, and SHA-256, and binds each required evidence record by path, identity, and SHA-256. The result identity and path may be recorded in the earlier report; its future fingerprint is not required there.
3. Before the Remediation cycle is reported complete, the Remediation actor resolves the final Audit report and result, recomputes and validates the stored Audit result's SHA-256, and confirms that the Audit result binds the final Audit report. The canonical final Remediation report records the Audit report path and identity and its result-bound SHA-256, plus the Audit result path, result identity, recomputed SHA-256, and validation outcome. It also records whether the final Audit findings list is empty or identifies the findings; the same binding is mandatory when there are no findings.
4. The Remediation report is a post-Audit terminal handoff anchor, not an input required to publish or determine the earlier Audit result. The Remediation actor then publishes its result after the final report and required evidence are durable; that result binds the final Remediation report by path, identity, and SHA-256. The Remediation report does not claim its own or its later result's fingerprint.

This order avoids self-reference and future-record claims while preserving the existing immutable report-first/result-second rule. It adds no record category, mutable addendum, approval, process stage. The existing Governance Remediation final-report requirements remain applicable, including for an Audit with zero findings.

Use the existing approved persistence convention and publication contract. Where durable recording is required but its scope or permission is missing, obtain the required authorization before execution. If publication is unavailable or fails, explicitly disclose the limitation, retain the required report through an authorized available channel, and stop progression that depends on durable completion. A conversational report does not satisfy a durable-record requirement. Do not claim that an unpublished report is durably available.

Reduce generation as well as repeated context consumption by eliminating redundant report text. Moving unchanged lengthy prose from conversation to a file alone does not reduce the tokens needed to generate it. Do not claim measured savings without measurement.

#### Common metadata and references

Each structured record must identify its schema version, record identity and type, feature, creator and role, creation time in UTC, and applicable process, attempt, gate, and related-record references.

Record-creation metadata, attempt-identity generation time, native execution-event time, and publication time describe distinct events. Record-creation metadata must describe preparation of the record, with its clock source or capture basis identified where needed to interpret the evidence. A clock sample taken while allocating an attempt or preparing a record must not be represented as its publication time.

This contract does not require an exact publication timestamp. If a publication time or observation is recorded, identify what was observed and its evidence source. Native tool request, start, and completion timestamps describe those logged events; they are not automatically the exact time of a filesystem publication operation. Do not infer an exact publication time from record-creation metadata, attempt identifiers, file metadata alone, or an unrelated event timestamp. Where exact publication time was not captured, state that limitation rather than inventing a value.

The required invocation-before-execution ordering must still be established through evidence of publication and subsequent execution, including operation results, final-record validation, and attributable event sequence as applicable. A command failure must be assessed in relation to its partial effects; it does not alone establish that an earlier publication operation failed or succeeded. A missing optional exact publication timestamp is not itself noncompliance, but an unsupported timestamp claim or unestablished mandatory ordering remains subject to finding and corrective governance. All validation, flushing, atomic no-overwrite publication, integrity, and immutable-record requirements remain unchanged.

An artifact reference must identify the artifact, location, version or immutable state identifier, and content fingerprint where needed to detect change. Where approval applies, it must reference actual approval evidence. Candidate and approved artifacts must remain distinguishable. Paths, version labels, timestamps, or fingerprints alone do not establish approval.

Task references must identify the Plan and version together with the Plan-local task identifier. Finding references must identify the originating report and original finding identifier. Related records must be resolvable by identity and location; final report and evidence references must include sufficient integrity information to detect alteration.

Unknown or unavailable information must be explicitly identified. Not-applicable information must be distinguished from missing information. Neither may be replaced by an invented value.

#### Invocation, checkpoint, and result records

The invocation record must identify the governed process, requested scope, input references, applicable task context, repository context, invocation authorization or request, predecessor or retry where applicable, and designated output location. It must be durably published before execution starts.

Checkpoints must identify the attempt and sequence, last confirmed boundary, relevant partial outputs or repository effects, unfinished work, observed evidence, blockers, pending gate or finding references, and the prerequisites for safe continuation. Publish checkpoints at meaningful safe boundaries; every tool call need not be recorded.

A terminal result must distinguish completed execution from observed failure, interruption, or cancellation. A completed result must reference the required final report, exact evaluated or produced state, actual governed outcome, evidence, unresolved items, and next permitted process. A completed attempt may have an unsuccessful outcome. Execution termination must not be represented as successful process completion.

Findings, investigations, corrective decisions, and task-impact assessments remain in their existing governed reports. Metadata must link them; it must not create a competing substantive register.

#### Implementation-state binding

Implementation-related records must identify repository identity, HEAD commit, branch as context, relevant tracked modifications and untracked files, and the relevant implementation scope. They must reference a path-and-content-fingerprint manifest sufficient to identify the implementation state being reported, verified, or reviewed, together with relevant execution environment and test context.

HEAD or branch alone is insufficient for an uncommitted implementation. A fingerprint detects change but does not preserve lost content. Where recovery requires restoration, the actual necessary source, configuration, and evidence must also remain available through an authorized persistence or backup mechanism.

Metadata and record-publication files must not themselves redefine the implementation verification scope or invalidate a result solely because execution bookkeeping changed.

#### Human-gate records

A gate request must identify the existing gate type, exact subject and version or implementation state, requested decision scope, applicable package and evidence, prerequisites, and requesting process or attempt.

A decision record must preserve the actual supplied human response, attributable source, exact subject and scope, conditions, decision time where available, and original decision evidence. It may reference an explicitly superseded decision. Transcription does not create approval or acceptance.

Absence or ambiguity of decision evidence means the gate is not established as satisfied. Human Review Approval, Human Plan Approval, corrective-change approval, and Human Acceptance remain distinct and retain their existing meanings.

#### Publication and incomplete writes

Prepare records under temporary names ending in .partial. Validate and flush their content before publication using a suitable same-filesystem atomic operation. Do not overwrite an existing final record.

Publish result.json for completed execution only after the required report and evidence references are durably available. It must bind the final report by identity and content fingerprint.

Partial files, malformed records, missing references, and mismatched fingerprints must not establish completion or authorize progression. If publication fails, record and surface the limitation where possible and stop progression that depends on the unpublished result.

An attempt without a valid terminal result is incomplete or unresolved. A later observer must not infer successful completion or observed termination merely from the start record.

#### Applicability and recovery

A fresh execution session must validate the records, resolve current approved sources and actual repository state, identify incomplete or competing attempts, reconcile partial effects, evaluate task-impact dispositions and result applicability, resolve human gates and corrective decisions, and determine the last confirmed safe boundary and next process permitted by the existing lifecycle.

Reconcile whether a previous attempt is still executing before starting conflicting work. A start record alone does not establish current liveness.

Distinguish applicable results, historical or superseded results, stale results that do not establish conformity of the current state, and unresolved applicability. Neither an unchanged task identifier nor retained implementation automatically carries verification forward to a new approved baseline.

Explicit supersession must reference the replaced record and its governing basis. A later timestamp, newer branch, or larger version label alone does not establish supersession or authority.

If source authority, approval, version binding, repository state, evidence, result applicability, human decisions, or competing records cannot be reconciled, stop the affected continuation and identify the required evidence or governed decision. Do not choose the newest record as a substitute for reconciliation.

Resuming from a confirmed safe boundary may require restarting an incomplete process. Partial evidence must not be represented as completion of complete-scope verification or review.

#### Git, recovery scope, and retention

Local publication is not a Git commit or remote push. Commit and Push retain their existing Human Acceptance precondition and require the applicable explicit authorization; no automatic publication to Git or a remote is authorized.

Before Human Acceptance, records may persist locally under the approved convention. After Human Acceptance, the necessary records may accompany the accepted implementation through explicitly authorized Commit and Push. Acceptance itself performs neither action.

Local persistence supports recovery in the retained workspace. Another machine or checkout requires the necessary authorized repository history or a separately approved backup or transfer mechanism, including necessary uncommitted implementation and evidence. This convention alone does not guarantee recovery after workspace or machine loss.

Preserve final records, superseded results and decisions, impact assessments, and necessary evidence and recovery checkpoints for the feature's maintained lifetime. Reconcile incomplete attempts before removing temporary publication material. Sensitive data must follow applicable handling constraints and must not be indiscriminately copied or published.

Derived execution views may be regenerated and must not become a separate authority.

---

## 31. SDLC Process Execution Traceability

SDLC Process Skills and SDLC Process Agents are governed execution mechanisms.

They must be traceable to the governance artifacts and governed process they implement.

The required relationship is:

    Master Governance
           ↓
    Guideline
           ↓
    Prompt / Request
           ↓
    SDLC Process Skill
           ↓
    SDLC Process Agent
           ↓
    Governed SDLC Process

The exact upstream relationship depends on the applicable process.

### 31.1 SDLC Process Skill

Each SDLC Process Skill must be traceable to:

- the applicable master governance documents,
- the applicable Guideline,
- the applicable Prompt,
- the applicable Request,
- the governed SDLC process,
- the current approved upstream artifacts required by that process.

A Skill defines reusable AI execution mechanics.

A Skill must not become a replacement for:

- Master Governance,
- Guideline,
- Prompt,
- Request,
- human approval,
- human acceptance,
- the current approved Requirement,
- the current approved Implementation Plan.

### 31.2 SDLC Process Agent

Each SDLC Process Agent must be traceable to:

- the applicable master governance documents,
- the applicable Guideline,
- the applicable Prompt,
- the applicable Request,
- the applicable SDLC Process Skill,
- the governed SDLC process,
- the authority and write boundaries defined for that process.

An Agent is a controlled execution entry point.

An Agent must not become an independent source of:

- governance authority,
- Requirement authority,
- Implementation Plan authority,
- human approval,
- human acceptance,
- corrective-change authorization.

### 31.3 Governance Control Mechanisms

The SDLC Governance Audit and SDLC Governance Remediation mechanisms are governed by the same three Master Governance documents and the same SDLC Governance Framework as the 52 core SDLC process mechanisms. They are a distinct functional category, not a separate governance framework or source of authority. Their governance-control responsibilities remain separate from normal SDLC process execution and from the coordination responsibility of the SDLC Process Orchestrator.

### 31.4 SDLC Process Orchestrator

The SDLC Process Orchestrator is a coordination mechanism under the same three Master Governance documents and governed process definitions. It remains outside the numerical 52-core catalog; this does not place it outside the Governance Framework.

Orchestration traceability must link the feature/work identity, applicable Master Governance and process definitions, current approved upstream artifacts, process invocation, the owning process attempt/report/result, applicable findings and corrective decisions, formal human-gate records, the Orchestrator's own interlock request/response, and the resulting next permitted process. A link or orchestration record does not replace the owning process actor's report/result or establish an approval.

The Process Initiation interlock is recorded as invocation-authorization metadata in the Orchestrator's own attempt under §30.1, with the actual human response, attributable source, exact subject/scope, conditions, and available time. It is not a formal human-gate record. Existing formal human-gate records and approvals remain separate and unchanged. No new record type, schema, persistence root, or execution-state authority is created.

Material Orchestrator or governance-control changes follow this same Governance Framework's Finding Investigation, Corrective Change Decision, required Human Approval, authorized application, independent verification/review, and Governance Audit path. The Orchestrator cannot approve or apply its own governance changes. Audit reporting must retain the exact 52-core count and report these additional mechanism-alignment checks separately.

### 31.5 Skill and Agent Change Traceability

A material change to a Skill or SDLC Process Agent must be traceable to:

- the reason for the change,
- the affected Skill or Agent,
- the applicable Guideline, Prompt, Request, and master governance artifacts,
- the affected governed process,
- the affected authority or execution boundary,
- required verification,
- required downstream impact,
- the resulting approved governance state.

A Skill or Agent change must not silently change the Requirement, Implementation Plan, human approval boundary, verification requirement, or acceptance requirement.

---

## 32. Traceability Matrix

The following matrix defines the primary traceability expectations:

| Artifact | Primary Upstream Source | Verification | Human Gate | Downstream Use |
|---|---|---|---|---|
| Requirement | Business need / source requirement | Requirement Analysis Verification | Human Requirement Approval | Implementation Planning |
| Requirement Analysis | Requirement | Requirement Analysis Verification | Human Requirement Approval applies to Requirement | Requirement refinement |
| Approved Requirement | Requirement + analysis + verification | Completed | Human Requirement Approval | Implementation Plan |
| Implementation Plan | Approved Requirement | Implementation Plan Verification | Human Review Approval, then Human Plan Approval | Implementation after Human Plan Approval |
| Approved Implementation Plan | Plan + verification + resolved findings | Completed | Human Review Approval and Human Plan Approval | Implementation after Human Plan Approval |
| Implementation | Approved Requirement + Approved Plan | Implementation Verification | Human Acceptance | Review / Acceptance |
| Implementation Self-Check | Implementation + approved sources | Self-check | None | Implementation Verification |
| Implementation Verification | Approved Requirement + Approved Plan + Implementation | Verification process | None | Implementation Review |
| Implementation Review | Approved Requirement + Approved Plan + Implementation + Verification | Review process | Human Acceptance follows where applicable | Acceptance |
| Finding | Verification / Review / Engineering activity | Finding Investigation | As required | Corrective Decision |
| Finding Investigation | Finding + affected artifact | Investigation | None | Corrective Decision |
| Corrective Decision | Finding Investigation + approved artifacts | Applicable verification after change | Human approval where required | Corrective implementation |
| SDLC Process Skill | Applicable Master Governance + Guideline + Prompt + Request + Governed SDLC Process | Governance Audit | None | SDLC Process Agent / Governed Process Execution |
| SDLC Process Agent | Applicable Master Governance + Guideline + Prompt + Request + SDLC Process Skill + Governed SDLC Process | Governance Audit | None | Governed SDLC Process Execution |
| Human Acceptance | Current implementation + verification + review | Evidence from prior stages | Human Acceptance | Commit / Push |

---

## 33. Change Propagation Rule

When a governed artifact changes, evaluate downstream artifacts in dependency order.

The dependency order is:

    Requirement
       ↓
    Requirement Analysis
       ↓
    Approved Requirement
       ↓
    Implementation Plan
       ↓
    Approved Implementation Plan
       ↓
    Implementation
       ↓
    Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

A change must propagate through every downstream stage that is materially affected.

The process must not stop merely because the changed artifact is technically valid in isolation.

### Governance Execution Mechanism Changes

Changes to SDLC Process Skills and SDLC Process Agents follow a separate governance dependency.

The relationship is:

    Governing Artifact
           ↓
    SDLC Process Skill
           ↓
    SDLC Process Agent
           ↓
    Governed Process Execution

When a Skill or Agent changes, evaluate whether the change affects:

- the applicable governance rules,
- the governed process,
- execution authority,
- read/write boundaries,
- approval boundaries,
- verification boundaries,
- traceability requirements,
- downstream Skills or Agents,
- the validity of existing governance verification.

A Skill or Agent change must not be treated as a product Requirement, Implementation Plan, or implementation change unless the change actually affects those artifacts.

Where a Skill or Agent change materially affects governance authority or process behavior, the applicable governance change, verification, and remediation process must be followed.

---

## 34. Minimal Required Propagation

Not every change requires restarting the entire SDLC.

The applicable downstream impact must be evaluated.

Examples:

### Documentation-only change

May require only documentation review if no governed behavior, requirement, plan, or implementation is affected.

### Test-only change

May require test verification and relevant implementation verification depending on the nature of the change.

### Implementation change

Normally requires Implementation Verification and may require Implementation Review.

### Plan change

Requires the applicable Plan Verification and Human Plan Approval before implementation continues against the changed plan.

### Requirement change

Requires Requirement Analysis, complete Requirement Analysis Verification, Human Requirement Approval, and downstream plan evaluation.

The required propagation must be determined by the applicable governed process.

---

## 35. Human Decision Boundary

When it is unclear whether a change:

- changes the Requirement,
- changes the Implementation Plan,
- changes the implementation only,
- requires new approval,
- invalidates prior verification,

AI must identify the ambiguity.

AI must not silently choose the governance path when the decision materially affects human authority.

The applicable human decision must be obtained.

---

## 36. Historical Traceability

Superseded artifacts, previous verification reports, previous review reports, and previous approval evidence needed to establish execution history, current applicability, corrective traceability, or human authority must be retained according to section 30.1. Preserve prior facts through linked subsequent records rather than overwriting them.

Historical records are useful for:

- auditability,
- understanding change history,
- investigating findings,
- understanding previous decisions,
- tracing corrective actions.

Historical records must not be treated as the current authority when superseded.

---

## 37. Governance Conflict Handling

If traceability reveals a conflict between artifacts:

1. Identify the conflicting artifacts.
2. Identify the applicable authority of each artifact.
3. Determine whether the conflict is business, technical, implementation, verification, or governance-related.
4. Do not silently resolve a material conflict.
5. Route the conflict through Finding Investigation or the applicable governed decision process.
6. Obtain required human approval before applying a material change.
7. Re-establish traceability after the conflict is resolved.

---

## 38. Required Corrective Traceability

Every material corrective change should be traceable through:

    Original Finding
       ↓
    Investigation
       ↓
    Corrective Decision
       ↓
    Human Approval where required
       ↓
    Approved Change
       ↓
    Corrective Implementation
       ↓
    Complete Implementation Verification
       ↓
    Implementation Review
       ↓
    Human Acceptance

This allows the repository history and governance records to explain:

- why the change was made,
- what authorized it,
- what requirement and plan it followed,
- how it was verified,
- how it was reviewed,
- when it was accepted.

---

## 39. Governance Shortcuts That Are Not Permitted

The following shortcuts are prohibited:

1. Requirement → Implementation without Human Requirement Approval.
2. Implementation Plan → Implementation without Human Review Approval and Human Plan Approval.
3. Finding → Direct Code Change.
4. Plan Change → Implementation without required Plan Verification, Human Review Approval, and Human Plan Approval.
5. Corrective Implementation → Human Acceptance without required Implementation Verification.
6. Verification → Human Approval.
7. Review → Human Acceptance.
8. Passing tests → Human Acceptance.
9. Previous approval → automatic approval of a changed artifact.
10. Previous verification → automatic verification of a changed artifact.
11. Task completion → automatic implementation acceptance.
12. AI recommendation → automatic human decision.

---

## 40. Final Traceability Principle

The governed SDLC must always be able to answer:

> What requirement authorized this behavior?

> Which approved Requirement version was used?

> Which approved Implementation Plan defined the implementation?

> What implementation was produced?

> What verification established conformance?

> What review evaluated the implementation?

> What findings were identified?

> How were those findings investigated and corrected?

> Which human approvals were obtained?

> Which implementation state was finally accepted?

If these relationships cannot be established, the affected process must be treated as having a traceability gap and routed through the applicable governance process.

---

## 41. Final Change-Control Principle

The fundamental change-control rule is:

> Never silently change an approved governed artifact.

The governed sequence is:

    Identify Change
       ↓
    Investigate
       ↓
    Determine Affected Artifact
       ↓
    Determine Corrective Direction
       ↓
    Obtain Required Human Approval
       ↓
    Apply Approved Change
       ↓
    Re-establish Traceability
       ↓
    Complete Required Verification
       ↓
    Complete Required Review
       ↓
    Obtain Human Acceptance where applicable

Every material change must leave an understandable and traceable governance path from the original source to the final accepted state.

## 42. Prospective Master Source Baseline and Change Control

The Master Governance source set for prospective source-baseline status consists of exactly these three files:

- `docs/ai/sdlc/SDLC_GOVERNANCE.md`
- `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md`
- `docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md`

**Candidate bytes are not approval.** Exact paths and SHA-256 fingerprints identify bytes only. A source set remains a candidate unless and until a separate, explicit, attributable Human decision adopts it under this section. Current repository bytes, a path, version label, timestamp, branch, commit, fingerprint, or partial approval lineage does not by itself establish approval, adoption, or an effective boundary. Preserve prior source versions as historical; where authentic evidence does not establish their approval or effective status, record that status as unknown. Do not infer prior approval or supersession.

**Initial adoption of an unchanged inherited Master set.** When a target repository receives the exact three Master files without changing their bytes, the files remain candidate text until a complete Governance Audit in that target repository assesses them. Adoption requires the Audit result `CONSISTENT`, Critical, High, Medium, Low, Ambiguities, Missing Governance Controls, Unsupported Governance Controls, and Broken References each equal to zero, and all seven separately assessed mechanism groups complete with no unresolved issue. Only then may a separate explicit Human decision adopt the exact three paths and SHA-256 fingerprints as that target's prospective baseline, with target identity, baseline identity, scope, effective boundary, predecessor status, and resolvable Audit evidence. This no-change initial adoption does not fabricate an application or amendment record, does not adopt product persistence root, and does not bypass any separate approval or stage-start. If the candidate audit or any required assurance is incomplete or fails, the baseline remains unadopted.

**Approval and exact application of a material Master change.** Each material proposed change to any of the three Master files requires its own explicit Human Approval before application. The approval must bind the exact patch or text, exact target path or paths, each target's base and expected-after SHA-256, scope and exclusions, and the application route. Approval authorizes only that bound change and does not itself establish application authority. If an already-authorized application actor is not demonstrably established, the approval record must explicitly designate a qualified actor and one-time scope. That actor must be distinct from the proposal preparer, the SDLC Process Orchestrator, and any Governance Remediation Agent barred from self-edit during its active cycle. The designated actor may apply only the approved change when every base fingerprint matches; any mismatch, additional change, or target deviation requires stopping and obtaining a new exact proposal and approval. No commit or push is authorized by this section. The standing Governance Amendment Application Agent may be the applier only after the mechanism is effective; it must remain distinct from the preparer, verifier, and reviewer. For this mechanism's initial establishment, the Human Approval record must designate the qualified one-time applier because the new Agent does not yet have effective authority.

**Independent assurance and separate prospective adoption.** After exact authorized application, require independent governance verification and independent review; neither may be performed by the proposal preparer or applier. Then complete the full Governance Audit over all 52 core artifacts and separately assess all seven mandatory same-framework mechanism groups: Governance Audit, Governance Remediation, SDLC Process Orchestration, SDLC Portability Assessment, Governance Amendment Application, Independent Governance Verification, and Independent Governance Review. Do not add mechanism groups to the 52-core count. Effectiveness requires the exact result `CONSISTENT`; Critical, High, Medium, Low, Ambiguities, Missing Governance Controls, Unsupported Governance Controls, and Broken References must each equal zero; all seven groups must be assessed and have no unresolved issue. A failed, incomplete, unavailable, or unresolved gate prevents effectiveness. If any required gate fails or remains unresolved, stop; do not declare the change or a baseline effective. Only after all these gates succeed may a separate, explicit, attributable Human decision adopt the exact then-current paths and SHA-256 fingerprints of all three Master files as a new prospective baseline. The adoption record must bind a baseline identity, the attributable Human Approval, scope, effective boundary, predecessor status, and resolvable references to the exact authorized application, independent verification, independent review, and complete Governance Audit. The adoption decision is distinct from patch approval, application authority, verification, review, and Audit; none substitutes for another. No baseline is adopted by default or retroactively.

**Existing records and historical boundaries.** Record and link proposals, approvals, application evidence, assurance results, and any separate adoption decision using the existing governed process records and human-decision records under section 30.1 of this document and section 33.1 of `SDLC_ARTIFACT_GOVERNANCE.md`. This section creates no artifact category, gate category, schema, persistence root, process, or approval authority and does not replace or relax either publication or change-control requirements. A future baseline decision must not waive, cure, reclassify, or make retroactive claims about the original alarm `CANNOT VERIFY`, missing pre-write bytes, missing pre-write scope manifest, earlier verifier-ordering deviation, the main gap's blocked/inactive/no-further-process decision, or the separate unresolved referral/no-further-work decision. It does not authorize alarm integration, activation, operation, or any product change; those require a distinct later governed request and their own approvals and assurance.

## 43. Optional Centralized Framework Consumption in a Local Multi-Root VS Code Workspace

### 43.1 Scope and preservation of the repository-local route

A product repository may use the SDLC framework from a separate local framework repository only through this optional centralized-consumption route and only after every prerequisite in this section is satisfied. The existing repository-local route remains valid, unchanged, and the default. Centralized consumption does not copy or transfer approval, authority, baseline adoption, audit results, actor identity, records, or permissions between repositories. Failure or ambiguity in the centralized route must stop that route; it must not trigger an automatic fallback, mixed-source invocation, or silent switch to repository-local artifacts.

This route is limited to a validated local multi-root VS Code workspace containing the exact framework and product roots selected for the invocation. Workspace visibility, folder order, the active editor, current working directory, repository parent discovery, or agent-name coincidence does not establish identity, authority, source selection, or permission. Each product root is an independent target and requires its own binding and authorization, even when multiple products share one framework root.

### 43.2 Per-product identity and immutable source binding

Before any product process starts, an attributable Human decision in the product repository must bind, at minimum: the canonical framework repository identity and verified local root; the full immutable framework commit; the SHA-256 manifest of the exact applicable framework artifacts; the canonical product repository identity, verified local root, and exact product source state; the local multi-root workspace used; the permitted actor/process scope; the adopted record roots and destinations; and the conditions and limits of use. Record the decision by reference in the target's existing governed records. Do not create a new persistence root or treat a workspace file alone as authorization.

The applicable framework manifest must identify the three Master Governance files and every Guideline, Prompt, Request, Skill, Agent, and referenced governance document or helper required by the selected process, each by repository-relative path and SHA-256. Resolve each artifact from the bound framework root and verify its bytes before use. The framework root must be at the approved full commit, have no uncommitted changes affecting the manifest, and be readable at every required path. Missing, dirty, changed, unreadable, ambiguous, or unlisted required inputs stop the invocation. The product root must independently match its approved canonical identity, root, and source state. Never combine files from different framework revisions or substitute same-named product-local files without explicit binding.

### 43.3 Onboarding and external baseline adoption

The target must establish its own governance persistence root and, before product records or Portability Assessment, separately adopt its own product persistence root under section 30.1. A target-context Governance Audit must resolve and assess the exact externally bound framework artifacts and all required mechanisms against the target's recorded identity and scope; an audit or baseline decision from the framework repository does not establish target consistency or adoption. The applicable external Master baseline may be adopted only by a separate explicit Human decision after the target-context Audit and all required independent assurance pass. That decision must bind the exact full framework commit, all three Master fingerprints, the applicable artifact-manifest identity and fingerprint, the product identity/root, scope, effective boundary, predecessor status, and the target Audit/assurance records. An external framework baseline is not copied into the product repository by this route.

After the target roots and external baseline are adopted, complete the separately authorized Portability Assessment and resolve its recommendation through the applicable Human decision before entering the product lifecycle. Portability Assessment remains read-only and advisory; it cannot adopt roots or a baseline, approve a product, or authorize implementation. The framework repository's own audit, the external source's approval history, and another product's records do not substitute for any target-specific gate.

### 43.4 Actor discovery, invocation, record ownership, and access boundaries

A process invocation must explicitly select the authorized Agent from the bound framework root and verify the corresponding Skill, Guideline, Prompt, Request, referenced artifacts, and their hashes against the manifest. Validate that the intended VS Code version and selected harness actually discover and invoke those exact files. Do not rely on discovery alone, primary-root precedence, duplicate-name resolution, or a displayed role name. If the intended actor or any required reference cannot be unambiguously resolved and verified, stop before consequential work.

Every actor must bind its own invocation to the framework identity/root/commit/manifest, product identity/root/source state, selected workspace, Work ID, process stage, fresh Human stage-start, predecessor gates, and exact output scope. The framework repository is read-only to product-process actors; product actors may publish only their own permitted records in the adopted target root. Framework-maintenance records remain in the framework repository's adopted governance root; target governance bootstrap, audit, and baseline-adoption records remain in the target governance root; product integration and lifecycle records remain in the target's separately adopted product root. Link cross-repository records using immutable identities, paths, and fingerprints. A product actor must not write framework definitions, another actor's records, another product root, or any location outside its authorized target scope. Workspace access is not authorization. If current capabilities cannot establish these boundaries, do not start or publish a process result.

### 43.5 Revision changes and interrupted-run recovery

A framework upgrade is a new candidate revision, not an in-place refresh of an adopted baseline. It requires a separate target assessment, applicable Audit and assurance, and explicit Human adoption of the exact new commit and manifest before new invocations use it. Existing and interrupted invocations remain pinned to their original framework revision and product source state. Resume only when every bound identity, root, revision, fingerprint, record scope, and required predecessor result still matches. On any mismatch, missing checkpoint, changed root, or unavailable artifact, preserve existing records, stop, and obtain an explicit Human recovery decision; do not combine revisions, silently restart under a different source, or overwrite history.

### 43.6 Runtime validation and fail-closed availability

Before this route is declared available for a particular VS Code version, harness, and workspace configuration, a separately authorized validation must establish root resolution independent of folder order and working directory; exact actor/reference discovery and invocation; rejection of identity, revision, fingerprint, dirty, missing, or unreadable-source mismatches; correct per-repository record destinations; actor-only publication and denial of framework/cross-product writes; pinned upgrades and interrupted-run handling; and unchanged operation of the repository-local route. Static documentation or source inspection is not runtime validation. Until the intended combination has passed that validation and the result is accepted through its governed gates, do not represent centralized consumption as operational or authorize product use.
