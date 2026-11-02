import sys
sys.dont_write_bytecode = True
from recovery import *

INV = json.loads((BASE / "attempt.json").read_bytes())
INV_REF = ref(BASE / "attempt.json")
RETRY_ID = "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd"
RETRY = PARENT / RETRY_ID
TARGET = RETRY / "attachments/GOV-AUD-20261102-001-linked-clarification.md"

def absence():
    assert not os.path.lexists(RETRY) and not os.path.lexists(TARGET)
    assert not os.path.lexists(OLD_TARGET)
    return {"path": TARGET.as_posix(), "presence": "ABSENT", "base_sha256": None, "base_bytes": None,
            "attempt_scope": RETRY.as_posix(), "attempt_presence": "ABSENT",
            "method": "Nonmutating os.path.lexists false for proposed attempt and exact target",
            "semantics": "No base bytes; not an empty-file hash; observation not reservation. Recheck before any later approved write."}

def cite(rr):
    return f"`{rr['path']}` ({rr['bytes']} bytes; SHA-256 `{rr['sha256']}`)"

def text_check(s):
    assert s.isascii() and s.endswith("\n") and "\r" not in s and "`n" not in s
    for bad in ["{evrel}", "{ev['bytes']}", "{ev['sha256']}", "[PATH", "[HASH", "TODO", "TBD", "<new"]:
        assert bad not in s

def prepare():
    assert INV_REF["sha256"] == "8EDA2344DB8D5312AF43CBBED844F21D6349798CC62CD6EA739E99E9CF1EDE34"
    preserved = unchanged(INV)
    failure_result = json.loads((FAILED / "result.json").read_bytes())
    failure_evidence = json.loads((FAILED / "evidence/failure-evidence.json").read_bytes())
    failure_inv = json.loads((FAILED / "attempt.json").read_bytes())
    prior_result = json.loads((PRIOR / "result.json").read_bytes())
    prior_ev = json.loads((PRIOR / "evidence/finalized-decision-evidence.json").read_bytes())
    prior_report = (PRIOR / "report.md").read_text(encoding="utf-8")
    failure_report = (FAILED / "report.md").read_text(encoding="utf-8")
    all_checks = []
    for name, obj in [("failed_result", failure_result), ("failed_evidence", failure_evidence),
                      ("failed_invocation", failure_inv), ("prior_result", prior_result),
                      ("prior_evidence", prior_ev)]:
        checks(obj, name, all_checks)
    assert failure_result["execution_status"] == "FAILED"
    assert failure_result["outcome"] == "CANNOT COMPLETE"
    assert not failure_result["substantive_application_started"]
    assert failure_result["actual_substantive_path_list"] == []
    assert failure_result["after"]["presence"] == "ABSENT"
    assert failure_result["after"]["sha256"] is None
    assert failure_result["approved_target"] == OLD_TARGET.as_posix() or failure_result["approved_target"]["path"] == OLD_TARGET.as_posix()
    auth = failure_result["approval_and_stage_start"]
    assert auth["canonical_package"] == ref(PRIOR / "report.md")
    assert auth["approval_verbatim"] == "I approve the identified canonical package and its complete section 4, with all bindings, restrictions and disclosures above; do not start Application"
    assert auth["stage_start_verbatim"] == "Yes, initiate only the scoped Governance Amendment Application under the approved package"
    assert failure_evidence["preservation"]["preexisting_files_compared"] == 288
    assert failure_evidence["preservation"]["all_bytes_paths_match"]
    script = FAILED / "evidence/application-publication.py"
    script_text = script.read_text(encoding="utf-8")
    relevant = [{"line": i, "text": l} for i, l in enumerate(script_text.splitlines(), 1)
                if "diffs =" in l or "response_differences" in l or "Serializer parse-check" in l]
    assert "Serializer parse-check" in script_text and "response_differences" in script_text
    payload_b = PAYLOAD.read_bytes()
    assert len(payload_b) == 3438 and sha(payload_b) == PAYLOAD_HASH
    assert payload_b.isascii() and b"\r" not in payload_b and not payload_b.startswith(b"\xef\xbb\xbf")
    assert payload_b.endswith(b"\n") and not payload_b.endswith(b"\n\n")
    assert prior_report.split("```markdown\n", 1)[1].split("```\n", 1)[0].encode() == payload_b
    original = json.loads(Path(prior_ev["original_response"]["source"]["path"]).read_bytes())["exact_approval_verbatim"]
    attr_text = Path(prior_ev["attributed_response"]["source"]["path"]).read_text(encoding="utf-8")
    attributed = next(l[2:] for l in attr_text.splitlines() if l.startswith("> I approve"))
    native_diffs = [{"offset": i, "original": f"U+{ord(a):04X}", "attributed": f"U+{ord(b):04X}"}
                    for i, (a, b) in enumerate(zip(original, attributed)) if a != b]
    assert native_diffs == [{"offset": 27, "original": "U+003F", "attributed": "U+00A7"},
                            {"offset": 42, "original": "U+003F", "attributed": "U+00A7"}]
    self_test = {"response_differences": native_diffs, "offsets": [27, 42], "pass": True}
    assert json.loads(encode(self_test)) == self_test
    roles = {
        "preparer": {"definition": ref(".github/agents/corrective-change-decision.agent.md"), "attempt": INV_REF,
                     "status": "CURRENT RECOVERY PROPOSAL PREPARER; not retry publisher"},
        "publisher": {"definition": ref(".github/agents/governance-amendment-application.agent.md"),
                      "proposed_attempt_identity": RETRY_ID, "proposed_scope": RETRY.as_posix(),
                      "status": "PROPOSED FRESH ONE-TIME DESIGNATION ONLY; prior one-time approval not transferred"},
        "verifier": {"definition": ref(".github/agents/independent-governance-verification.agent.md"),
                     "status": "PLANNED DEFINITION ONLY; own attempt/current capability after completed Application and fresh Verification start"},
        "reviewer": {"definition": ref(".github/agents/independent-governance-review.agent.md"),
                     "status": "PLANNED DEFINITION ONLY; own attempt/current capability after PASS Verification and fresh Review start"},
    }
    excluded = [ref(".github/agents/sdlc-process-orchestrator.agent.md"), ref(".github/agents/sdlc-governance-remediation.agent.md")]
    assert len({(v["definition"]["path"], v["definition"]["sha256"]) for v in roles.values()}) == 4
    assert roles["publisher"]["definition"] not in excluded
    controls = [ref(p) for p in [
        "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
        ".github/agents/governance-amendment-application.agent.md",
        "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md",
        "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md",
    ]]
    for rr in controls:
        Path(rr["path"]).read_text(encoding="utf-8")
    scope = {
        "status": "RECOVERY PROPOSAL ONLY; NO NEW DESIGNATION/APPROVAL/RETRY START",
        "purpose": "Only recovery from failed Application of GOV-AUD-20261102-001; no new finding",
        "one_substantive_target": TARGET.as_posix(), "base_condition": absence(),
        "payload_source": ref(PAYLOAD), "expected_after_sha256": PAYLOAD_HASH, "expected_after_bytes": 3438,
        "encoding": "UTF-8 without BOM; ASCII-only; LF only; one final LF",
        "roles": roles, "excluded_publisher_definitions": excluded,
        "application_route": "Fresh explicitly Human-redesignated distinct one-time Governance Amendment Application actor publishes exact approved payload in its own new retry attempt; own required execution records only in same new scope",
        "no_reuse": "No new publication in failed attempt, no edits to historical scripts/final records, no silent transfer of designation/approval, no same-identity terminal attempt restart",
        "tooling_direction": "In future fresh actor-owned script use JSON-native dict/list/scalar structures from construction. Self-test complete actual evidence objects with strict serialize/parse structural equality before any corresponding partial/final publication. Preserve exact-byte/hash/parse checks; do not weaken them, coerce away mismatches, edit failed script or claim old failed preflight evidence passed.",
        "exclusions": "No source/historical/other-actor edits; no payload/content/newline change, broad punctuation normalization, GOV-001/GOV-002 reopening, P1-P5 reapplication, product work/alarm integration, standing authority, adoption, commit/push, verification eligibility from failed result or effectiveness claim",
        "next_human_gate": "One combined attributable Human decision explicitly redesignating publisher/new attempt and approving this recovery package's exact target/ABSENT base/payload/roles/scope/route. Do not separately gate designation before exact package approval; both may be explicit in one decision.",
        "later_separate_gate": "After combined designation/exact approval, require a fresh separate Human Application retry stage-start; old start is not reusable",
        "qualification": "Fresh publisher own current nonmutating identity/permissions/capability evidence and no-overwrite invocation publication/readback before substantive work. Its new Application attempt may be first capability record; no pre-existing qualification record required. Missing/uncertain capability/approval/base/identity means CANNOT COMPLETE.",
        "later_assurance": "Completed successful Application then separately Human-started independent Verification; PASS then separately started independent Review; PASS then separately started complete Governance Audit. No Master adoption required for non-Master record clarification.",
        "risks": "Shared write-capable OS principal is not enforced sandbox. Endpoint hashes cannot exclude transient same-principal tampering/unobserved concurrent writes; no exhaustive execution log/no-edit window/continuous observation/repository lock. Disclosure is not a new approval-validity condition.",
    }
    cp = common("publication_boundary_checkpoint")
    cp.update({"sequence": "0001", "invocation": INV_REF,
               "ordering": ["Q1 current governance/identity/ACL/Git/root/input hashes/recovery metadata qualification",
                            "Q2 own invocation parse/flush/fsync/no-overwrite publication",
                            "Q3 separate readback validates 310 invocation bindings and 293 pre-existing file endpoints before substantive comparison",
                            "S1 inspect failed report/result/evidence/script and actual approval/start; inspect current recovery rules",
                            "S2 compare actual payload/response/bindings, JSON-native self-test, and prepare new target proposal only"],
               "last_confirmed_boundary": "Record-first boundary and failure reconciliation established; proposal publication next",
               "effects": "Only own records; failed target absent; no retry directory created",
               "pending_gate": scope["next_human_gate"], "preservation": preserved})
    cp_ref = publish(BASE / "checkpoint-0001.json", encode(cp))
    ev = common("recovery_decision_evidence")
    ev.update({"invocation": INV_REF, "publication_checkpoint": cp_ref,
               "failure_report": ref(FAILED / "report.md"), "failure_result": ref(FAILED / "result.json"),
               "failure_evidence": ref(FAILED / "evidence/failure-evidence.json"), "failed_script": ref(script),
               "source_inspected_serializer_lines": relevant, "actual_prior_authorization": auth,
               "prior_approved_package": ref(PRIOR / "report.md"),
               "all_checked_input_references": all_checks, "input_binding_count": len(all_checks),
               "all_input_bindings_match": True, "serializer_json_native_self_test": self_test,
               "failure_classification": "Reported and source-supported execution-tooling tuple/list equality mismatch; not a new finding or payload/evidence invalidity",
               "prior_288_file_endpoint_claim": failure_evidence["preservation"],
               "current_preservation": preserved, "recovery_proposal": scope,
               "decision_status": STATUS, "readiness": "WAITING FOR GOVERNANCE CHANGE APPROVAL",
               "plan_change_required": False, "requirement_plan": "N/A: governance-only; no adopted product Requirement/Plan",
               "governing": INV["governing"], "application_assurance_controls": controls,
               "publisher_scripts": [ref(BASE / "attachments/recovery.py"), ref(Path(__file__).relative_to(ROOT))],
               "evidence_classes": {
                   "executed": ["Current hashes/JSON/native structure self-test/response codepoint/absence/path-set checks and own publication/readback"],
                   "source_inspection": ["Failure report/result/evidence/script and prior approval/start; current recovery/publication/application rules; unchanged actual payload and historical character sources"],
                   "reported": ["Native tool failure events, prior 288-file endpoints and approval/start attributed in Application records; full historical Audit/Investigation outcomes, not re-executed"],
                   "unverified": ["Original external conversation identity/time, exhaustive failure event log, transient same-principal tampering/unobserved concurrency/product runtime"]},
               "limits": INV["qualification"]["limits"]})
    checks(ev, "recovery_evidence_prepublication", [])
    ev_b = encode(ev)
    ev_path = BASE / "evidence/recovery-decision-evidence.json"
    ev_ref = {"path": ev_path.as_posix(), "bytes": len(ev_b), "sha256": sha(ev_b)}
    role_lines = "\n".join(f"- {k}: {cite(v['definition'])}. {v['status']}." for k, v in roles.items())
    report = f"""# Recovery Corrective Change Decision & Plan Update

Subject: FINDING GOV-AUD-20261102-001 only; bounded recovery from failed Application.
Work ID: `{WORK}`; prospective cycle GOV-REMEDIATION-PROSPECTIVE-001, Cycle 1.
Decision attempt: `{ID}`.
Repository ScalableParimal/SupportIQ; HEAD `{INV['repository']['head']}`;
branch `{INV['repository']['branch']}`. Current exact bytes/path set, not HEAD
alone, are bound in the invocation manifest. Bootstrap pre-Master-adoption.

## 1. Decision Status

**FINDING ACCEPTED -- OTHER GOVERNED ARTIFACT CHANGE REQUIRED**

Original disposition retained; canonical JSON uses U+2014 for the separator.
**Readiness: WAITING FOR GOVERNANCE CHANGE APPROVAL.**
Recovery requires a fresh explicit scoped publisher designation/new-destination
approval. These may be one combined Human decision, followed by a distinct
fresh Application start. This is not a new finding or approval.

## 2. Finding Summary

Original Low report-only traceability defect remains: line 15 evidence metadata
and line 27 U+003F QUESTION MARK versus U+00A7 SECTION SIGN distinction.
All fourteen required affected report fields remain identifiable; wholesale
invalidity unsupported. Not all question-mark-bearing lines are defective.
No historical GOV-001/GOV-002 reopening. This continuation addresses only
recovery of its failed Application, not a new Investigation.

## 3. Investigation Result and failed Application reconciliation

Latest Investigation remains CORRECTIVE DIRECTION IDENTIFIED. Original exact
3438-byte clarification remains sufficient. Full Audit remains COMPLETED,
CONSISTENT WITH MINOR FINDINGS: 52/52 core, 76 source files, one Low finding,
Governance Remediation FAIL and other six mechanisms PASS; nonqualifying for
adoption/effectiveness, not incomplete Audit execution.

Prior approved package: {cite(ref(PRIOR / 'report.md'))}.
Failed Application report: {cite(ref(FAILED / 'report.md'))}.
Failed Application terminal result: {cite(ref(FAILED / 'result.json'))}.
Failure evidence: {cite(ref(FAILED / 'evidence/failure-evidence.json'))}.
Preserved failed execution script: {cite(ref(script))}.

Actual result is FAILED / CANNOT COMPLETE, no substantive application started,
actual substantive path list empty, exact old attachment absent with null
after-byte count/digest. Preflight validate returned; strict serializer equality
then failed because response-difference Python tuples round-trip as JSON lists.
Failed preflight evidence was not published. Source inspection corroborates the
failure explanation; the native historical execution is reported evidence, not
re-executed. No repair, retry or rollback is performed here.

The actual Application record retains these distinct historical Human decisions:
- Exact approval: "{auth['approval_verbatim']}"
- Separate Application start: "{auth['stage_start_verbatim']}"

They bind the prior package and old one-time attempt/destination, not this
proposed retry. Current user confirms that history; source-provenance record
relays actual conversation decisions, with no authenticated external message
ID/time exposed. We do not invalidate or silently renew that original approval.
Earlier package's NOT GIVEN statements describe its preparation-time state;
later supplied Application evidence records the approval and start.

Failure evidence reports 288 pre-existing files unchanged at failure endpoints.
This recovery separately fingerprints {preserved['files']} pre-existing files,
including failed attempt and intervening records; all current bytes/path set and
HEAD/branch/status match recovery invocation. These different snapshots are not
contradictory. Current payload/old attachment state rechecked unchanged/absent.
All {len(all_checks)} actual structured input references checked PASS.
No reported or inspected evidence shows payload/source drift. A tooling mismatch
does not establish a new substantive defect or invalid actual evidence.

## 4. Corrective Decision and exact recovery proposal

### A. Ownership and lawful recovery route

Do not append the payload to the failed terminal attempt in this recovery.
Artifact Governance 33.1 permits own records, not another process actor's
records; Traceability 30.1 preserves final records, requires each invocation's
pre-execution attempt, fresh retry stage-start and reconciliation. The original
approved route additionally required a new actor-owned Application attempt and
ABSENT designated attempt directory. That historical attempt now exists and is
terminal FAILED; its invocation/result cannot be overwritten or silently
reopened. The failed result explicitly stopped and requires fresh direction.

An unoccupied attachment name alone does not grant continuation or cross-actor
authority. A new invocation cannot adopt the historical attempt merely by using
the same role label/OS account. No current authority establishes that a retry
actor owns it or that a new publication there satisfies the approved new-attempt
route. A separate approved exceptional same-attempt route is not presumed or
requested; it would need different explicit governing authority. Keep all failed
records/scripts and the absent old attachment state intact.

Use the ordinary fresh own-attempt route, explicitly redesignated and approved
by the Human. Allocation of a proposed identity below is proposal preparation
only, not designation, reservation, publication or Application initiation.
Current proposal scope authorizes preparing this exact recovery package, so
no preliminary extra Human gate or second decision continuation is needed before
requesting the combined designation/exact approval.

### B. Proposed new one-time scope and exact destination

Proposed future retry attempt identity: `{RETRY_ID}`.
Proposed publisher-owned scope: `{RETRY.as_posix()}`.
One exact substantive destination:

`{TARGET.as_posix()}`

**Base: ABSENT**. Nonmutating lexists checks confirm both proposed directory
and exact attachment absent. Base SHA-256/byte count are N/A (JSON null), not
an empty-file hash. This is a point-in-time observation, not reservation.
No future retry directory or actor-owned record is created here.
Recheck the complete exact target set and all authority/input/base fingerprints
before later application. Collision/drift/missing capability means stop,
not overwrite, alternative destination, normalization or rollback.

Historical target remains ABSENT but is NOT this recovery's approved destination:
`{OLD_TARGET.as_posix()}`.
No one-time designation, prior approval or historical stage-start is transferred.
Human approval of this package must explicitly redesignate the publisher/new
attempt and approve this changed destination/base condition.

### C. Exact unchanged payload

Use only original source {cite(ref(PAYLOAD))}.
Exact expected-after bytes: **3438**.
Exact expected-after SHA-256: **`{PAYLOAD_HASH}`**.
Encoding: UTF-8 without BOM; ASCII-only; LF only; one final LF.
No content/header/footer/signature/newline/codepoint change.
Prior package's exact embedded body was byte-compared with that actual payload;
all source bindings remain valid. No duplicate payload is created here.

Actual historical response sources were re-read and compared: 133 Unicode code
points each; U+003F versus U+00A7 at zero-based offsets 27 and 42 only; no new
authentication or precise original encoding/transport-cause claim. The immutable
affected report and resolved 22254-byte evidence remain bound in the unchanged
payload and prior package/evidence.

### D. Exact actor-definition and independence bindings

{role_lines}

Current preparer invocation: {cite(INV_REF)}.
All four definition path/hash pairs distinct. Publisher additionally excluded
from Orchestrator {cite(excluded[0])} and active barred Remediation actor
{cite(excluded[1])}.
Future publisher identity is proposed only. Verifier/reviewer remain planned
definition-only bindings, no attempts/runtime capability claimed or precreated.
Each eventual actor must match its approval-bound definition identity, establish
current independent invocation/capability and own-record publication. Shared OS
identity/host/repository alone does not defeat process-actor separation; display
name/definition alone does not prove capability.

### E. Bounded fresh execution-tooling direction

Do not modify the failed script or relabel failed preflight evidence as passed.
Future fresh publisher should construct JSON-native dict/list/scalar evidence,
including response differences, and self-test the complete actual object before
any corresponding partial/final durable publication. Retain strict structural
serialize/parse equality, exact bytes/hash checks, flushing, atomic no-overwrite
publication and independent readback. Do not relax checks or coerce mismatches
away just to pass. Current in-memory JSON-native self-test with actual response
differences passed; this administrative check is not execution of Application
and does not prove a future actor's full runtime capability.

The new actor's own transient helper/evidence records may implement that direction
only within its later approved scope and process conduct. No source fix or
separately approved upstream artifact amendment is needed to avoid the internal
tuple/list mismatch. New actor must run all actual preflight checks afresh; a
return from the failed validate call is not a durable successful Application.

### F. Scope, exclusions and exact gate

Only the exact payload attachment plus new publisher's own required execution
records within section 4.B's new scope. Preserve originals, failed scripts and
final reports/results. No edits to old attempts/source/other actors' records,
P1-P5 reapplication, GOV-001/GOV-002 reopening, broad punctuation cleanup,
payload changes, product/alarm integration, requirements/plans/code/tests/
configuration/migrations, standing authority, effectiveness/adoption, commit/push.

Next gate is **one explicit attributable Human decision** both redesignating the
distinct one-time publisher for this new attempt/scope and approving this exact
recovery canonical report (final SHA-256 bound by request/result), section 4
payload/target/base/after-encoding/bytes/hash, four actor bindings, route,
exclusions and preserved-history boundary. No separate initial designation gate
is necessary because this package already fixes the proposed exact destination.

## 5. Plan Change Required

**NO.** Governance-only; current approved product Requirement/Implementation Plan
are N/A, none adopted. No approved product Plan whose validity can be affirmed
or changed, and no new Plan is invented or approved.

## 6. Plan Impact

Tasks, acceptance criteria, architecture, product scope/dependencies/testing/
verification N/A and unchanged. Governance Application must be retried only
after authority gates, with fresh checks and independent assurance afterward.
Failed Application does not make Verification eligible. No retention of a
successful Application/Verification claim is inferred from unchanged payload.

## 7. Proposed Plan Amendment

N/A. No product Plan amendment. Section 4 is the exact other-artifact recovery
proposal; it is not an approved Plan or implementation authority.

## 8. Human Approval Required

**YES; recovery approval/redesignation NOT GIVEN.** Original exact approval and
one-time start remain authentic attributed historical decisions for their scope,
not reusable authority for the changed destination or new actor invocation.
Approve/redesignate in one combined Human decision as section 4.F describes.
An actor-owned exact request metadata record will bind the final report digest
after publication; it is a request, never a supplied Human decision.

After that combined decision require **a separate fresh explicit Application
retry stage-start**, bound to actual approval/package, failure predecessor,
new designated actor/attempt/scope and current repository state. No repeated
Corrective Decision is needed if this exact proposal is approved unchanged.
Old Application initiation is not reused or automatically propagated.

Then publisher establishes current nonmutating identity/permissions/read/hash/
check/exact authorized publication/readback capability; publishes and independently
validates its own new invocation before substantive preflight/application.
The new Application attempt may be its first qualification record; no extra
pre-existing qualification record is required. Missing/uncertain authority,
capability, base or input binding means CANNOT COMPLETE before application.
No source write-probe, broad write or unapproved rollback.

After completed successful Application, separately initiate independent
Governance Verification; after PASS, independent Governance Review; after PASS,
complete Governance Audit. Each requires fresh Human start, proper predecessor
and current actor-owned qualification/readback. No Master file changes:
Master adoption is not required for this record-only correction and not authorized.

## 9. Implementation Readiness

**WAITING FOR GOVERNANCE CHANGE APPROVAL** (including the explicit fresh
one-time publisher/new-scope designation in the same decision).
Not product implementation readiness. Unchanged payload remains unapplied;
new target and retry directory absent; failed target absent. No Verification,
Review or Audit progression is currently eligible.

## 10. Next Process

**Combined Human recovery redesignation and exact-change approval only; STOP.**
After approval, separately fresh Application start; then only qualified designated
publisher may execute the approved own-record route. No additional proposed
investigation, new finding, code change or preliminary designation-only round.
Reject/alter the proposal if the Human wants different scope; do not silently
substitute a target or transfer the earlier one-time decision.

## Execution context, evidence, traceability and limitations

Fresh actual Human recovery start:
> {START}

No authenticated platform message identity/time exposed; current user supplies
the instruction and historical approval/start summary. Existing OWNER root
adoption was re-resolved at
https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236
(created/updated 2026-10-30T12:31:51Z), current HEAD/Master fingerprints match.
Initial Audit-only start not reused; governance-root adoption distinct from
Master/product baseline adoption. SDLC_GOVERNANCE section 3 normal bootstrap
corrective workflow, Artifact Governance 33.1 own-record boundary, Traceability
30.1 invocation/recovery/immutability and stage-start rules apply.
Relevant product architecture/engineering guideline N/A to this record recovery.

Invocation {cite(INV_REF)} was published and independently read back before
substantive comparison; all 310 invocation bindings passed. Boundary checkpoint:
{cite(cp_ref)}. Canonical evidence: {cite(ev_ref)}.
Inputs/actual approval/start/payload/failed result/script/current governing
controls and complete request applicability are bound in those records.
Administrative checks are not a downstream Verification/Audit or Application.

Executed evidence: current identity/ACL/Git, strict hash/JSON/native-structure/
codepoint/absence/path-set tests and own publication/readback.
Source inspection: actual failed records/script, prior exact package, supplied
historical decisions within Application evidence, payload and current controls.
Reported: historical native failure events, 288-file endpoint comparison and
full Audit/Investigation assessments, not re-executed.
Unverified: original external conversation identity/time, exhaustive native
execution history, unobserved concurrency/transient tampering/product runtime.

Shared OS procedure is write-capable, not enforced read-only sandbox. No source
write-probe, no-edit window, repository lock, continuous concurrency monitoring
or exhaustive trusted execution log. Endpoint hashes cannot exclude transient
same-principal tampering/unobserved activity. Historical in_progress is not proof
of live work; this invocation is this actor, not a competitor; no agent dispatched.
Risk disclosure is not a new approval-validity condition or generic risk stage.
Creation times are host preparation samples, not exact filesystem publication
times. Actor-visible ordered operations establish invocation-before-comparison,
not exhaustive ordering of every event. All {preserved['files']} pre-existing
files/path set and HEAD/branch/status are compared, excluding this exact attempt.

No source/corrective/application/downstream work, Finding Investigation, new
finding, adoption, commit/push or substantive Human decision is performed here.
All originals preserved. Canonical recovery report:
`{(BASE / 'report.md').as_posix()}`; terminal result:
`{(BASE / 'result.json').as_posix()}`.
Exact approval request: `{(BASE / 'attachments/exact-recovery-approval-request.json').as_posix()}`.
Report does not claim its own/future result hash. Later request/result bind
durable final report; independent actual content/ALL-binding readback and completion
precede result publication. Stop at combined Human authority/approval gate.
"""
    text_check(report)
    for i, name in enumerate(["Decision Status", "Finding Summary", "Investigation Result",
                              "Corrective Decision", "Plan Change Required", "Plan Impact",
                              "Proposed Plan Amendment", "Human Approval Required",
                              "Implementation Readiness", "Next Process"], 1):
        assert report.count(f"## {i}. {name}") == 1
    unchanged(INV)
    absence()
    assert json.loads(ev_b) == ev
    assert publish(ev_path, ev_b) == ev_ref
    checks(ev, "evidence_before_report", [])
    print(json.dumps({"report": publish(BASE / "report.md", report.encode()),
                      "evidence": ev_ref, "input_references": len(all_checks), "new_base": absence(),
                      "state": "Report/evidence durable; independent actual-content/binding readback required next"}))

if __name__ == "__main__":
    prepare()
