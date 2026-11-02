"""Own record-only publication procedure; no product execution or source writes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd().resolve()
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ID = "20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694"
ATTEMPTS = ROOT / "docs/sdlc-records/governance" / WORK / "attempts"
OWN = ATTEMPTS / ID
PRE = ATTEMPTS / "20261030T151526Z-ed894077-40cc-417c-af53-dad64eafac3d"
ORIGINAL = ATTEMPTS / "20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55"
HASH = "4D792552B451BDA23F8FD70AC15C500FF733BD0E5F595806F119445C7F1D91E2"
ALLOWED = {
    "evidence/preflight.json", "evidence/approval-context.json",
    "checkpoint-0001.json", "checkpoint-0002.json",
    "attachments/IGV-FIND-001-approval-transcription-correction.md",
    "evidence/application-evidence.json", "report.md", "result.json",
}


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def relative(p):
    return p.relative_to(ROOT).as_posix()


def ref(p):
    b = p.read_bytes()
    return {"path": relative(p), "sha256": sha(b), "bytes": len(b)}


def load(p):
    return json.loads(p.read_bytes().decode("utf-8"))


def command(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def common(kind, suffix):
    return {
        "schema_version": "1.0", "record_type": kind,
        "record_identity": ID + ":" + suffix,
        "work_id": WORK, "feature_id": WORK, "attempt_id": ID,
        "process": "Governance Amendment Application",
        "creator": "Current separate one-time record-only Governance Amendment Application invocation",
        "role": ".github/agents/governance-amendment-application.agent.md",
        "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "clock_basis": "Current system UTC at record preparation, not exact publication time",
        "exact_publication_time": None,
    }


def encode(d):
    return (json.dumps(d, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


def publish(name, b):
    assert name in ALLOWED and os.name == "nt"
    p = OWN / name
    assert p.resolve().is_relative_to(OWN)
    assert not os.path.lexists(p), "Final path collision: " + name
    q = p.with_name(p.name + ".partial")
    assert not os.path.lexists(q), "Partial path collision: " + name
    p.parent.mkdir(parents=True, exist_ok=True)
    if name.endswith(".json"):
        json.loads(b.decode("utf-8"))
    else:
        b.decode("utf-8")
    with q.open("xb") as f:
        assert f.write(b) == len(b)
        f.flush()
        os.fsync(f.fileno())
    assert q.read_bytes() == b
    # Windows rename is same-filesystem, atomic, and fails if destination exists.
    # Never use replace(), which would overwrite a final record.
    os.rename(q, p)
    actual = p.read_bytes()
    assert actual == b and sha(actual) == sha(b)
    if name.endswith(".json"):
        assert load(p) == json.loads(b.decode("utf-8"))
    print("PUBLISHED_READBACK_OK", json.dumps(ref(p)), flush=True)
    return ref(p)


def publish_json(name, d):
    return publish(name, encode(d))


def snapshot():
    files = []
    for base in (ROOT / ".github", ROOT / "docs/ai", ROOT / "docs/sdlc-records"):
        if base.exists():
            files.extend(p for p in base.rglob("*") if p.is_file() and not p.is_relative_to(OWN))
    files.append(ROOT / "README.md")
    assert all(not p.is_symlink() for p in files)
    return {relative(p): ref(p) for p in sorted(set(files))}


def validate_references(refs):
    for d in refs:
        p = ROOT / d["path"]
        actual = ref(p)
        assert actual == d, (actual, d)


def unicode_details(s):
    return {
        "decoded_text": s, "codepoint_count": len(s),
        "utf8_bytes_without_newline": len(s.encode("utf-8")),
        "sha256_without_newline": sha(s.encode("utf-8")),
        "section_sign_offsets_zero_based": [i for i, c in enumerate(s) if ord(c) == 167],
        "decoded_codepoints": [ord(c) for c in s],
    }


def validate_inputs():
    expected = {
        "report.md": "8E299D41A613D9CBDDB2F6F4D7072BF2017A5EE58BD3A712FC881AE1267501F3",
        "result.json": "9FA47FDDB6087960B727676570BB54123F2FF9CF39FAE153FB65B28A6AFF6AD1",
        "evidence/proposal-finalization-evidence.json": "CC72221338982971970C43F333F4BF7785C136B9103E447BF6AF12FF61CB88D6",
        "evidence/proposed-correction.md": HASH,
    }
    refs = []
    for name, h in expected.items():
        d = ref(PRE / name)
        assert d["sha256"] == h
        refs.append(d)
    predecessor = load(PRE / "evidence/proposal-finalization-evidence.json")
    for p, d in predecessor["integrity_anchors"].items():
        actual = ref(ATTEMPTS / p)
        assert actual["sha256"] == d["sha256"]
        refs.append(actual)
    original = load(ORIGINAL / "evidence/approval-context.json")
    for op in original["exact_subject"]["operations"]:
        actual = ref(ROOT / op["target_path"])
        assert actual["sha256"] == op["expected_after_sha256"]
        assert actual["bytes"] == op["expected_after_bytes"]
        refs.append(actual)
    a = load(OWN / "attempt.json")
    assert ref(OWN / "attempt.json")["sha256"] == "A94DEBE86515D4CE18E98491E92AF3AAB885EC61BA2CF3C1856B84C814C699EE"
    role = ROOT / a["actor"]["definition_path"]
    assert ref(role)["sha256"] == a["actor"]["definition_sha256"]
    refs.append(ref(role))
    for key in ("preparer", "planned_verifier", "planned_reviewer"):
        role = a["identity_bindings"][key]
        actual = ref(ROOT / role["definition_path"])
        assert actual["sha256"] == role["definition_sha256"]
        refs.append(actual)
    for role in a["identity_bindings"]["excluded_applier_roles"]:
        actual = ref(ROOT / role["path"])
        assert actual["sha256"] == role["sha256"]
        refs.append(actual)
    preparer = ROOT / a["identity_bindings"]["preparer"]["actor_owned_attempt"]
    pd = load(preparer)
    assert pd["work_id"] == WORK and pd["attempt_id"] == PRE.name
    assert "corrective-change-decision.agent.md" in json.dumps(pd)
    refs.append(ref(preparer))
    for path, h in {
        "docs/ai/sdlc/SDLC_GOVERNANCE.md": "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
        "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md": "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
        "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C",
    }.items():
        actual = ref(ROOT / path)
        assert actual["sha256"] == h
        refs.append(actual)
    assert command("git", "rev-parse", "HEAD") == a["repository"]["head"]
    assert command("git", "remote", "get-url", "origin") == a["repository"]["origin"]
    assert command("git", "branch", "--show-current") == a["repository"]["branch"]
    assert set(command("git", "diff", "--name-only").splitlines()) == {
        op["target_path"] for op in original["exact_subject"]["operations"]
    }
    assert load(ATTEMPTS / "20261030T144048Z-ea52b7a2-e67b-4579-b22c-20dc3bb09c25/result.json")["outcome"] == "FINDINGS"
    assert load(ATTEMPTS / "20261030T123604Z-15be0f40-a028-4166-bb27-fbf5fdefecc4/result.json")["audit_outcome"] == "CANNOT COMPLETE AUDIT"
    for p in ATTEMPTS.glob("*/attempt.json"):
        if p.parent != OWN:
            assert (p.parent / "result.json").is_file(), "Unresolved competing attempt"
            assert load(p).get("work_id") == WORK
    assert not (ROOT / "docs/sdlc-records/product" / WORK).exists()
    payload = (PRE / "evidence/proposed-correction.md").read_bytes()
    s = a["authorization"]["original_approval_attributed_response"]
    assert unicode_details(s)["section_sign_offsets_zero_based"] == [27, 42]
    assert len(s) == 133 and len(s.encode("utf-8")) == 135
    assert sha(s.encode("utf-8")) == "F64D83824A1A31FA470FAC6FC36631F5687B468F6EC9DA777C2EFD0253ECF085"
    assert original["exact_approval_verbatim"] == s.replace(chr(167), "?")
    assert original["exact_approval_verbatim"] in (ORIGINAL / "report.md").read_text("utf-8")
    assert s in payload.decode("utf-8") and payload.decode("utf-8").count(chr(167)) == 2
    assert len(payload) == 4212 and sha(payload) == HASH
    assert not payload.startswith(b"\xef\xbb\xbf") and b"\r" not in payload
    assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
    return a, refs, payload, original["exact_subject"]["operations"]


def apply():
    a, inputs, payload, operations = validate_inputs()
    assert sorted(relative(p) for p in OWN.rglob("*") if p.is_file()) == sorted([
        relative(OWN / "attempt.json"), relative(OWN / "evidence/publication-procedure.py")])
    target_name = "attachments/IGV-FIND-001-approval-transcription-correction.md"
    assert relative(OWN / target_name) == a["target"]["path"]
    assert not os.path.lexists(OWN / target_name)
    protected = snapshot()
    preflight = common("sdlc_process_evidence", "preflight")
    preflight.update({
        "attempt_binding": ref(OWN / "attempt.json"),
        "capability": a["current_capability_preflight"],
        "runtime_identity": a["actor"], "actor_separation": a["identity_bindings"],
        "repository": a["repository"],
        "git_status_porcelain": command("git", "--no-pager", "status", "--porcelain=v1", "--untracked-files=all"),
        "root_authority": a["root_authority"],
        "validated_inputs": inputs, "protected_state_manifest": protected,
        "absence": {"attempt_was_absent_before_own_partial_preparation": True,
                    "attachment_still_absent_after_own_attempt_readback": True,
                    "base_sha256": None, "no_overwrite": True},
        "publication_procedure": ref(OWN / "evidence/publication-procedure.py"),
        "continuation": "Existing authorized same Work ID; all ten preceding attempts terminal, no conflicting incomplete/partial attempt or product Work ID collision observed.",
        "residual_limits": a["current_capability_preflight"]["limitations"],
    })
    pf = publish_json("evidence/preflight.json", preflight)
    approval = common("sdlc_process_evidence", "approval-context")
    approval.update({
        "attribution": a["authorization"], "proposal_report": ref(PRE / "report.md"),
        "proposal_result": ref(PRE / "result.json"), "proposal_evidence": ref(PRE / "evidence/proposal-finalization-evidence.json"),
        "exact_subject": a["target"], "publisher": a["actor"],
        "current_decision_unicode_checks": {
            k: unicode_details(a["authorization"][k]) for k in (
                "exact_approval_verbatim", "separate_fresh_stage_start_verbatim",
                "original_approval_attributed_response")},
        "provenance": "Actual user-supplied parent-conversation responses, explicitly permitted verbatim retention. No external authentication or decision-event timestamp inferred. Bootstrap comment supports root adoption only.",
    })
    ac = publish_json("evidence/approval-context.json", approval)
    cp = common("sdlc_process_checkpoint", "checkpoint-0001")
    cp.update({
        "sequence": 1, "last_confirmed_boundary": "Own attempt and preflight/approval evidence durable and readback/hash validated; correction still absent.",
        "bindings": [ref(OWN / "attempt.json"), pf, ac],
        "effects": "Only own invocation/evidence records; no correction or source write yet",
        "unfinished_work": "Recheck full protected state and target absence, copy exact approved payload, readback, publish final evidence/report/result",
        "blockers": [], "finding_refs": ["IGV-FIND-001"], "pending_gate": "Independent Verification not started",
        "safe_continuation_prerequisites": "All inputs, source hashes and protected manifest unchanged; exact destination absent; stop on mismatch or failure",
    })
    publish_json("checkpoint-0001.json", cp)
    validate_references(inputs)
    assert snapshot() == protected
    assert not os.path.lexists(OWN / target_name)
    # Consequential publication occurs only after invocation and preflight readbacks.
    correction = publish(target_name, payload)
    actual_payload = (OWN / target_name).read_bytes()
    assert actual_payload == payload and sha(actual_payload) == HASH
    assert len(actual_payload) == 4212
    assert a["authorization"]["original_approval_attributed_response"] in actual_payload.decode("utf-8")
    validate_references(inputs)
    assert snapshot() == protected
    evidence = common("sdlc_process_evidence", "application-evidence")
    evidence.update({
        "preflight": pf, "approval_context": ac,
        "invocation": ref(OWN / "attempt.json"),
        "checkpoint_before_correction": ref(OWN / "checkpoint-0001.json"),
        "actual_correction": correction,
        "before": {"state": "ABSENT", "sha256": None, "bytes": None},
        "after": correction,
        "approved_payload": ref(PRE / "evidence/proposed-correction.md"),
        "exact_byte_equality_after_readback": True,
        "format": "UTF-8 without BOM; LF only; exactly one final LF",
        "unicode_original_response": unicode_details(a["authorization"]["original_approval_attributed_response"]),
        "input_hashes_recomputed_after_correction": inputs,
        "all_protected_source_and_original_record_hashes_unchanged": True,
        "protected_file_count": len(protected),
        "five_original_source_targets_unchanged": [ref(ROOT / op["target_path"]) for op in operations],
        "source_write_count": 0,
        "ordered_operations": [
            "Current nonmutating capability, identity, approval and all-base checks",
            "Own .partial invocation prepared; validated/flushed/atomic no-overwrite publication; separate readback",
            "Procedure evidence published; inputs rechecked; protected-state manifest captured",
            "Preflight/approval evidence and checkpoint-0001 durably published and read back",
            "Full inputs/protected-state/attachment-absence rechecked",
            "Approved bytes copied into own .partial; validated/fsync; same-filesystem Windows no-overwrite rename",
            "Attachment exact bytes/hash/UTF-8/Unicode readback validated",
            "All original/input/source fingerprints and complete protected manifest rechecked unchanged",
        ],
        "tool_outcomes": "Every publication through this point returned successfully with exact readback/hash; any assertion/OS exception stops without rollback.",
        "publication_time_limitation": "Ordered actual operation results are retained; exact filesystem publication timestamps were not captured.",
        "preserved_outcomes": {"original_verification": "FINDINGS", "original_audit": "CANNOT COMPLETE AUDIT"},
        "meaning": "Limited linked qualification only, not whole-result supersession, approval invalidation/reissue, original-result replacement, P1-P5 reapproval/reapplication, resolution or effectiveness.",
        "unresolved": ["Precise technical lossy-transcription cause unknown",
                       "Parent-message IDs and independently authenticated approval-event timestamps unavailable",
                       "Separate independent Verification, Review and Audit gates remain pending"],
        "residual_risk": "Endpoint hashes cannot prove no transient writes or same-principal tampering; no independent OS isolation or continuous filesystem attestation asserted.",
    })
    ev = publish_json("evidence/application-evidence.json", evidence)
    cp2 = common("sdlc_process_checkpoint", "checkpoint-0002")
    cp2.update({
        "sequence": 2, "last_confirmed_boundary": "Exact approved attachment published and byte/hash/Unicode checked; original records and sources unchanged",
        "bindings": [correction, ev],
        "effects": "One approved correction attachment plus own records only; no source write",
        "unfinished_work": "Canonical report and separate terminal readback validation/result publication",
        "blockers": [], "finding_refs": ["IGV-FIND-001"],
        "safe_continuation_prerequisites": "All bound records/protected inputs unchanged; no overwrite; next independent stage requires separate fresh human start",
    })
    cp2ref = publish_json("checkpoint-0002.json", cp2)
    refs = [ref(OWN / "attempt.json"), ref(OWN / "evidence/publication-procedure.py"),
            pf, ac, ref(OWN / "checkpoint-0001.json"), correction, ev, cp2ref]
    rows = "\n".join("| `" + d["path"] + "` | " + str(d["bytes"]) + " | `" + d["sha256"] + "` |" for d in refs)
    source_rows = "\n".join("| `" + op["target_path"] + "` | `" + op["expected_after_sha256"] + "` | unchanged |" for op in operations)
    original_rows = "\n".join("| `" + d["path"] + "` | " + str(d["bytes"]) + " | `" + d["sha256"] + "` |" for d in inputs)
    report = f"""# IGV-FIND-001 - one-time record-only Application

Work ID: `{WORK}`  
Attempt: `{ID}`  
Process/creator: current separate one-time record-only Governance Amendment Application invocation.

## Outcome and exact scope

**APPLIED - EXACT APPROVED RECORD-ONLY CORRECTION.** One attachment was published at the exact approved destination, previously ABSENT (no base bytes/hash), with no overwrite. Readback equals the approved static payload byte-for-byte: {correction['bytes']} bytes; SHA-256 `{HASH}`; UTF-8 without BOM, LF only, exactly one final LF. U+00A7 at original-response offsets 27/42 is retained. The payload was copied as bytes, not regenerated.

Destination: `{correction['path']}`.

This is a linked qualification of the original approval-response transcription and inaccurate unqualified verbatim-retention claim only. It does not supersede the entire original Application result, invalidate/reissue the underlying approval, approve/reapply P1-P5, repair original metadata, or resolve the finding. Original Verification remains **FINDINGS** and original Audit **CANNOT COMPLETE AUDIT**. No effectiveness, Review, Human Acceptance or baseline adoption is established.

## Approval, fresh stage-start and provenance

The actual current user supplied the following human responses from the current parent conversation and explicitly permitted their verbatim retention:

> {a['authorization']['exact_approval_verbatim']}

Separate fresh Application start:

> {a['authorization']['separate_fresh_stage_start_verbatim']}

The current user states the parent question bound this exact canonical finalization report, payload/path/count/encoding/hash, absent/no-overwrite destination, original anchors, designated role hash and own-record-only exclusions. The exact subject, decoded codepoints and UTF-8 hashes of both responses are in `evidence/approval-context.json`. The subject is the finalized report `{relative(PRE / 'report.md')}`, SHA-256 `{ref(PRE / 'report.md')['sha256']}`, and its result/evidence/payload bound below. Historical NOT-APPROVED status records remain immutable; these later actual human responses supply current approval/start, not a rewrite of history.

Original response retained as attributed evidence, not newly approved or externally authenticated:

> {a['authorization']['original_approval_attributed_response']}

Its 133 codepoints / 135 UTF-8 bytes without newline have SHA-256 `F64D83824A1A31FA470FAC6FC36631F5687B468F6EC9DA777C2EFD0253ECF085`. U+00A7 occurs at zero-based offsets 27/42. The original report/approval-context instead retain U+003F. Exact technical lossy-transcription cause remains unknown. No original parent-message ID or independently authenticated decision timestamp was supplied; none is invented. Current record creation times are system UTC preparation samples, not decision or exact publication timestamps. Attempt timestamp is the approved proposal allocation identity, not current invocation/publication time.

## Current identity, authority, capability and continuation

Current actor definition: `{a['actor']['definition_path']}`, SHA-256 `{a['actor']['definition_sha256']}`; unique own invocation `{ID}`. WindowsIdentity observed `INT-SCL-010\\Parimal`, SID `{a['actor']['sid']}`; this OS principal is not an externally authenticated AI identity. Active role-bound invocation and exact current human designation bind process identity. It is separate from the preparer and prior Application/Verification invocations and does not reuse their attempts.

Preparer definition/own finalization attempt, current applier, planned Verification and planned Review definition path/hash bindings are retained in `attempt.json` and preflight. All four roles are distinct; Orchestrator and Governance Remediation excluded-applier roles are separately fingerprinted. Planned Verification/Review bindings are identities only, not future attempts, current capabilities or stage starts. No future attempt was created.

Current read/hash/status/path checks succeeded before publication. Token S-1-5-11 and inherited Authenticated Users Modify/Synchronize ACL on attempts parent support exact own-scope write/readback; no deny observed and no write probe made. Current Python/PowerShell primitives support exclusive .partial creation, flush/fsync and same-filesystem atomic no-overwrite publication. Own invocation was published/read back/hash-validated before consequential correction work; preflight capability/state evidence and checkpoint were durable before attachment publication. Every final publication was independently read back. Nonmutating capability evidence is not inferred from a role or previous actor success.

The existing authorized Work ID is continued unchanged: ten predecessor attempts have terminal results; no incomplete/partial/conflicting attempt or product-root Work ID collision was observed. Exact candidate attempt and target were absent before own preparation; target remained absent after own invocation publication and immediately before correction publication. Complete protected file manifests before/after match ({len(protected)} files); no other actor record changed.

Governance-root adoption was currently resolved through GitHub issue 3 comment `https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236`, author ScalableParimal, association OWNER, created/updated 2026-10-30T12:31:51Z. Its root adoption/original Audit authorization is not current correction approval/start. Three current Master hashes match that decision. SDLC_GOVERNANCE section 3 explicitly permits normal correction lifecycle after bootstrap; non-Master amendment does not require Master-baseline adoption. Masters remain candidate/unadopted; no product root or baseline adopted.

Repository: ScalableParimal/SupportIQ; local `{ROOT.as_posix()}`; HEAD `{a['repository']['head']}`; branch `{a['repository']['branch']}`. Initial tracked modifications were exactly the five previously applied amendments; untracked governance records were expected. Complete initial status and protected manifest are in preflight. No source was written, no P1-P5 reapplication, product work/tests/build/runtime, other agent/stage, rollback, commit or push occurred.

## Five source targets preserved

| Path | Current SHA-256 before/after | State |
|---|---|---|
{source_rows}

## Original and approved input anchors recomputed and preserved

| Path | Actual bytes | SHA-256 |
|---|---:|---|
{original_rows}

All entries were independently recomputed in this invocation, including the twelve original predecessor anchors, finalization report/result/evidence/payload, original Application report/result/approval-context, Verification chain and original proposal. Original Application result is context only, unchanged, not superseded.

## Durable output integrity

| Path | Actual bytes | SHA-256 |
|---|---:|---|
{rows}

This is the single canonical report body. The later terminal `result.json` must bind its final bytes/hash and required evidence after separate readback. This report does not self-assert its own or its future result hash. Ordered operation evidence establishes invocation-before-correction publication; exact publication timestamps were not captured.

## Evidence classes, residual limits and next gate

Executed: current nonmutating identity/ACL/Git/file/hash/Unicode checks; own no-overwrite durable publication and exact readbacks; protected-state preservation. Source inspection: governing Skill/Guideline/Prompt/Request, applicable Master clauses and actual finalization report/payload/original evidence. Reported: actual human wording supplied from parent conversation, without external authentication/message IDs. Future/unverified: independent assurance, finding resolution, effectiveness, adoption.

Endpoint hashes cannot prove absence of transient writes or same-principal tampering. No exclusive OS isolation, continuous filesystem attestation or external approval authentication is claimed. Unknown exact transcription cause remains. Local durable publication is not remote backup or Git commit.

**Next permitted process: separately initiated independent Governance Verification**, only after a complete successful bound Application result and its own fresh human stage-start. The planned role fingerprint must match at invocation and the actor must establish its own current capabilities/attempt. Review then Audit remain later separately gated. No next stage is invoked.
"""
    publish("report.md", report.encode("utf-8"))
    print("APPLICATION_AND_REPORT_PUBLISHED; terminal result withheld pending separate readback validation", flush=True)


def finalize():
    a, inputs, payload, operations = validate_inputs()
    pf = load(OWN / "evidence/preflight.json")
    assert snapshot() == pf["protected_state_manifest"]
    validate_references(pf["validated_inputs"])
    evidence = load(OWN / "evidence/application-evidence.json")
    validate_references([evidence["preflight"], evidence["approval_context"], evidence["invocation"],
                         evidence["actual_correction"], evidence["approved_payload"],
                         evidence["checkpoint_before_correction"]])
    approval = load(OWN / "evidence/approval-context.json")
    assert approval["attribution"] == a["authorization"]
    for k, d in approval["current_decision_unicode_checks"].items():
        assert d == unicode_details(a["authorization"][k])
    target = ROOT / a["target"]["path"]
    assert target.read_bytes() == payload
    assert not list(OWN.rglob("*.partial"))
    report = OWN / "report.md"
    text = report.read_bytes().decode("utf-8")
    assert a["authorization"]["exact_approval_verbatim"] in text
    assert a["authorization"]["separate_fresh_stage_start_verbatim"] in text
    assert a["authorization"]["original_approval_attributed_response"] in text
    refs = [ref(p) for p in sorted(OWN.rglob("*")) if p.is_file() and p.name != "result.json"]
    validate_references(refs)
    result = common("sdlc_process_result", "result")
    result.update({
        "execution_termination": "COMPLETED",
        "application_outcome": "APPLIED - EXACT APPROVED RECORD-ONLY CORRECTION",
        "completion_meaning": "Only exact authorized attachment publication and own evidence/report completed; not independent assurance or finding resolution.",
        "repository": a["repository"], "actor": a["actor"],
        "canonical_report": {**ref(report), "identity": ID + ":report"},
        "required_evidence_and_records": refs,
        "approved_target": a["target"], "actual_correction": ref(target),
        "approval_context": ref(OWN / "evidence/approval-context.json"),
        "predecessor_report": ref(PRE / "report.md"), "predecessor_result": ref(PRE / "result.json"),
        "preterminal_separate_readback": "Separate command/process reloaded and rehashed report, every bound evidence/output, approved bytes and all protected inputs; exact decoded decisions checked against supplied values before terminal publication.",
        "exact_evaluated_state": {"protected_manifest": ref(OWN / "evidence/preflight.json"),
                                  "protected_state_unchanged": True, "source_writes": 0},
        "original_verification_outcome_unchanged": "FINDINGS",
        "original_audit_outcome_unchanged": "CANNOT COMPLETE AUDIT",
        "unresolved_items": evidence["unresolved"],
        "residual_risks": evidence["residual_risk"],
        "planned_independent_verifier": a["identity_bindings"]["planned_verifier"],
        "planned_independent_reviewer": a["identity_bindings"]["planned_reviewer"],
        "next_permitted_process": "Independent Governance Verification only after separate fresh human stage-start and new independent current qualification/attempt; not invoked",
        "not_claimed": ["Finding resolution", "Whole-result supersession", "New underlying approval",
                        "P1-P5 reapplication", "Review", "Audit", "Effectiveness",
                        "Master/product-root adoption", "Human Acceptance", "Commit", "Push"],
    })
    publish_json("result.json", result)


if __name__ == "__main__":
    assert ROOT.as_posix().lower() == "c:/parimal_shere/scalable_solutions/supportiq"
    assert sys.argv[1:] in (["apply"], ["finalize"])
    if sys.argv[1] == "apply":
        apply()
    else:
        finalize()
