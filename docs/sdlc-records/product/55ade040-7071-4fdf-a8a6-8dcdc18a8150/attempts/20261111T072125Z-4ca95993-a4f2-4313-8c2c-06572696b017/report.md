# Corrective Change Decision & Plan Update Report — IPV-01

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Attempt:** `20261111T072125Z-4ca95993-a4f2-4313-8c2c-06572696b017` ([attempt.json](attempt.json), [evidence](evidence/decision-evidence.json), [proposed amendment](attachments/proposed-plan-amendment-ipv-01.md))
- **Actor:** Corrective Change Decision Agent (`.github/agents/corrective-change-decision.agent.md` with its Skill), operated by `INT-SCL-010\Parimal`
- **Repository:** `ScalableParimal/SupportIQ` at HEAD `d9dd1685bbdc6d8a4ce21d2b21ee0bae491d6ef0`. There are no tracked changes and the six pre-existing untracked attempt folders were preserved.
- **Initiation:** the repository owner gave interactive approval to start, with no option preference and no ranking criteria.

## 1. Decision Status

**FINDING ACCEPTED — PLAN CHANGE REQUIRED**

This status applies to the **draft candidate** Implementation Plan `supportiq-product-implementation-plan` / `0.1`. There is currently **no approved Implementation Plan**.

**Interpretation disclosure (Portability C-02):**
- The Corrective Change Guideline's status and §17 wording refer to an "approved Implementation Plan".
- Guideline §§6/9 and the Master lifecycle send Implementation Plan Verification findings to a plan update *before* Human Plan Approval.
- This decision therefore treats the draft candidate v0.1 as the affected plan.
- **The human must confirm this interpretation** when approving the decision.

## 2. Finding Summary

- **IPV-01**, from Implementation Plan Verification `20261107T133205Z-58d4f444-…` (outcome CHANGES REQUIRED).
- IP-20 has the prerequisite "finalized API contracts", and IP-21–IP-24 inherit it through IP-20. No task, deliverable or completion check owns that prerequisite.
- §2 line 32 requires final schemas, validation, status/error, idempotency and OpenAPI to be "reconciled before consumers are built" without naming an owner.
- Evidence: E-01–E-06.

## 3. Investigation Result

Finding Investigation `20261111T052943Z-22085ae6-…` concluded **CORRECTIVE DIRECTION IDENTIFIED**:
- The finding is confirmed, and its root cause is in the implementation plan.
- The formal finding classification is **Cannot Determine**. This decision does not depend on resolving it, because the gap is observable in the Plan text either way.
- No requirement, architecture, schema, migration or configuration change was identified.
- **Option A** (an owned, per-slice contract-readiness task) is the advisory recommendation. **Option B** (contract deliverables added to the producer tasks) is acceptable. **Option C** (rely on phase reconciliation and IP-26 only) is not recommended.

## 4. Corrective Decision

**Accept IPV-01.** Correct the candidate Plan before Human Plan Approval.

- **Plan validity:** v0.1 cannot proceed to Human Review or Plan Approval unchanged.
- **Option selection:** the user gave no ranking criteria, and no approved governing source supplies any (Guideline §13). This process therefore **does not select an option on its own authority**. Both viable options are presented with exact amendment text. **Option A** is presented first because it is the investigation's advisory recommendation, for these documented reasons:
  - it gives the cross-cutting contracts (error envelope, pagination, job status) a single owner;
  - it gives a readiness check that can be observed before each UI task;
  - per-slice readiness avoids a system-wide freeze.
- **Trade-offs:**
  - Option B avoids a new task but spreads ownership across many tasks, and its only control for shared contracts is a consistency check at line 162.
  - Option A adds one task ID and five slice milestones.
- **Option C** is rejected as a sole response because IP-26 runs after the UI work.

## 5. Plan Change Required

**YES**. The change affects task breakdown, task dependencies and acceptance/completion criteria (Guideline §8).

## 6. Plan Impact

| Area | Impact |
| --- | --- |
| Tasks | **Option A:** add IP-19A (no renumbering); change the prerequisites of IP-20–IP-24; clarify the IP-26 prerequisite. **Option B:** extend the Completion of IP-05–IP-15 and IP-17–IP-19 (IP-16 excluded); qualify the prerequisites of IP-20–IP-24. |
| Dependencies | Line 155 chain and line 162 integration rule updated. Under Option A, each slice depends only on its own producer tasks. |
| Acceptance / completion | Adds a versioned OpenAPI description plus passing API contract tests, with a readiness record per slice or per producer task. |
| Traceability | Rows at lines 194 and 211 updated. |
| Testing | Adds API contract tests before UI consumers. IP-26 is unchanged. |
| Architecture / scope / requirement | **No change.** The React/API and authorization boundaries are preserved. No route, field, vendor, package or schema is selected. Requirement v1.11 line 630 already requires final contracts. |
| Data / schema / migration / operations | No change. D-01–D-04 remain open and are not resolved. |
| Version | The candidate becomes **v0.2**. v0.1 is recorded as a superseded draft, and a task disposition is recorded. |

## 7. Proposed Plan Amendment

The exact replacement text is in [attachments/proposed-plan-amendment-ipv-01.md](attachments/proposed-plan-amendment-ipv-01.md). Every v0.1 line number and quoted string in it was matched against the Plan file before publication.

The attachment covers:
- **Part 1, Option A:**
  - A1: the IP-19A task text;
  - A2: the IP-20–IP-24 prerequisites;
  - A3: edits to lines 32, 146, 155, 162, 194 and 211;
  - A4: the v0.2 version, status, self-validation and disposition edits;
  - A5: what stays explicitly unchanged.
- **Part 2:** the Option B variant and its residual risk.
- **Part 3:** why Option C is not proposed.

Record for the §9 amendment:
- **Finding:** IPV-01.
- **Investigation Result:** see §3.
- **Corrective Decision:** see §4.
- **Reason:** the UI prerequisite has no owner or check.
- **Changed Tasks / Acceptance Criteria:** as in the attachment.
- **Changed Architecture / Approach:** none.
- **Changed Scope:** none.
- **Constraints:**
  - no invented routes or fields;
  - D-01–D-04 untouched;
  - serialized execution unchanged.
- **Verification Impact:** a complete new Implementation Plan Verification of v0.2 is required.

## 8. Human Approval Required

**YES** (Guideline §11). This gate covers a plan and API-contract governance change. The human must:
1. accept or reject the decision status, and confirm the draft-candidate interpretation (C-02);
2. select Option A or Option B, or request changes;
3. approve the exact amendment text for the selected option;
4. **designate the application route (Portability C-03).** This process proposes a governed **Implementation Planning revision**. That revision would:
   - produce candidate v0.2 as a new planning attempt;
   - apply only the approved text;
   - leave the v0.1 record untouched.

**This gate is not Human Review Approval and not Human Plan Approval.** Those remain separate, later gates.

## 9. Implementation Readiness

**WAITING FOR PLAN APPROVAL**. No implementation is authorized.

## 10. Next Process

The remaining sequence, in order:
1. Human Approval of this decision, the selected option, the exact amendment and the application route.
2. Application through the designated governed plan-update route, producing candidate v0.2.
3. A **complete** Implementation Plan Verification of v0.2.
4. Resolution of any findings.
5. The Human Review package.
6. Human Review Approval.
7. Human Plan Approval.
8. Implementation under Orchestrator coordination.

If the human rejects the decision or asks for changes, a new Corrective Change Decision attempt is required. This record is not edited.

## Remaining uncertainties

- The formal classification is still Cannot Determine (inherited).
- OpenAPI tooling, the contract test framework and the exact operation lists per slice are deferred to Implementation within the approved architecture.
- Interaction with other concurrent work is unknown and unassessed.
- All evidence is from source inspection or reports. Nothing was executed.
