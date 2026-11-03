"""One authorized own-record recovery; no source/product writes or retry loop."""
import os
import json
import pathlib
import hashlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path.cwd().resolve()
WORK = "supportiq-requirement-discovery-cb6472d0-3e33-4eeb-bf0b-ba01740ded1a"
ATTEMPT = "20261103T035546Z-abfbecb2-c676-4f78-b588-8e1e05c19a9e"
OLD = "20261103T035033Z-c365b679-bee8-40a9-8cad-fc85ff4a59df"
BASE = ROOT / "docs/sdlc-records/product" / WORK
OWN = BASE / "attempts" / ATTEMPT
ORIGINAL = BASE / "attempts" / OLD
HEAD = "ae355f5d5d538f9751ff6f7919433bd442979b2c"


def lp(path):
    return pathlib.Path("\\\\?\\" + str(path.resolve()))


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def ref(path, record_id=None):
    data = lp(path).read_bytes()
    value = {"path": path.relative_to(ROOT).as_posix(),
             "bytes": len(data), "sha256": digest(data)}
    if record_id:
        value["record_id"] = record_id
    return value


def strict(data):
    return json.loads(data.decode("utf-8", errors="strict"))


def common(kind, suffix):
    return {
        "schema_version": "1.0", "record_type": kind,
        "record_id": ATTEMPT + ":" + suffix, "work_id": WORK,
        "feature": "SupportIQ draft requirement discovery; not one implementation feature",
        "attempt_id": ATTEMPT,
        "process": "SDLC Process Orchestrator bounded Q1 publication recovery only",
        "creator": {
            "identity": "orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff",
            "role": "SDLC Process Orchestrator",
            "effective_os_identity": "INT-SCL-010\\Parimal",
            "harness_session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60"},
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "clock_basis": "Python system UTC at record preparation, not exact publication or native decision time",
        "gate": {"subject": "Q1 clarification recording only", "formal_approval": False,
                 "later_process_start": False, "remaining": "Q2-Q10 pending"},
        "task_context": "No Plan-local task; no product process executed",
        "state": "REQUIREMENT_DECISION_PENDING"}


def publish_prepared(path, expected_data, is_json):
    partial = lp(path.with_name(path.name + ".partial"))
    final = lp(path)
    assert partial.parent == final.parent and not final.exists()
    actual = partial.read_bytes()
    assert actual == expected_data
    actual.decode("utf-8", errors="strict")
    if is_json:
        item = strict(actual)
        assert item["work_id"] == WORK and item["record_id"]
    with partial.open("r+b") as stream:
        stream.flush()
        os.fsync(stream.fileno())
    assert not final.exists()
    # Windows os.rename is atomic on the same filesystem and fails if destination exists.
    os.rename(partial, final)
    readback = final.read_bytes()
    assert readback == expected_data and digest(readback) == digest(expected_data)
    if is_json:
        assert strict(readback) == strict(expected_data)
    print("PUBLISHED/READBACK PASS", json.dumps(ref(path)))
    return ref(path)


def publish_json(path, item):
    data = (json.dumps(item, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    assert strict(data) == item
    for key in ["schema_version", "record_type", "record_id", "work_id", "creator",
                "created_at_utc", "process", "attempt_id", "gate", "task_context"]:
        assert key in item
    partial = lp(path.with_name(path.name + ".partial"))
    assert not partial.exists() and not lp(path).exists()
    with partial.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    return publish_prepared(path, data, True)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, text=True).strip()


def validate_inputs():
    assert git("rev-parse", "HEAD") == HEAD
    assert git("branch", "--show-current") == "sdlc-framework-onboarding"
    assert git("diff", "--name-only") == "" and git("diff", "--cached", "--name-only") == ""
    evidence = ROOT / "docs/sdlc-records/product/55ade040-7071-4fdf-a8a6-8dcdc18a8150/attempts/20261102T180059Z-36b3dfb9-ba84-4787-b9b7-97f8e75cda93/evidence/continuation-evidence.json"
    data = evidence.read_bytes()
    assert digest(data) == "FE7D8E0B290CAD8587832B05699D449F250C689A8B5D8A88D1C59E3102EB4C49"
    manifest = strict(data)
    for key in ["source_inventory", "target_inventory"]:
        for v in manifest[key]:
            actual = ref(ROOT / v["path"])
            assert actual["bytes"] == v["bytes"] and actual["sha256"] == v["sha256"]
    paths = {p.relative_to(ROOT).as_posix() for folder in [".github", "docs/ai"]
             for p in (ROOT / folder).rglob("*") if p.is_file()}
    assert paths == {v["path"] for v in manifest["source_inventory"]}
    return {"framework_fingerprints": 76, "target_fingerprints": 2,
            "hidden_inclusive_path_set": "PASS", "head": HEAD,
            "tracked_and_staged_diff": "Empty", "input_manifest": ref(evidence)}


def main():
    assert os.name == "nt"
    assert digest(lp(OWN / "attempt.json").read_bytes()) == "7795D82526147B20F7728E48AF14456C1F6D7C4443F1CC334F08533826F1ECAD"
    assert digest(lp(ORIGINAL / "attempt.json").read_bytes()) == "9CE5F352DAB440D7AD9714E841D0EE84E11C973D908BED102B342062B160041B"
    # Snapshot only existing records in this owning product work, including hidden paths.
    historical = {}
    for p in lp(BASE).rglob("*"):
        if p.is_file() and not p.name.endswith(".partial"):
            historical[str(p)] = digest(p.read_bytes())
    inputs_before = validate_inputs()
    evidence_path = ORIGINAL / "attachments/20261103T035033Z-c055d486-717c-4fc2-b000-e2cc24945089.json"
    report_path = ORIGINAL / "report.md"
    evidence_bytes = lp(evidence_path.with_name(evidence_path.name + ".partial")).read_bytes()
    report_bytes = lp(report_path.with_name(report_path.name + ".partial")).read_bytes()
    assert len(evidence_bytes) == 7603 and digest(evidence_bytes) == "238EB48907DD25EAA0ED310C8784F2E213E984A1AC95247F62DF47888F3708B5"
    assert len(report_bytes) == 6655 and digest(report_bytes) == "08ED668988AAF2C533225163A308811ED969B2F06175D79307B0BB578CA09C8B"
    item = strict(evidence_bytes)
    assert item["attempt_id"] == OLD and item["work_id"] == WORK
    assert item["actual_boundary"] == "Synthetic / local data only; no external connector or live / customer data will be used in the first version. But we may need external connector or live / customer data to be used in future. We will take this later."
    assert "**Customer Lookup:**" in item["actual_allowed_operations_response"]
    assert "**Ticket Lookup:**" in item["actual_allowed_operations_response"]
    assert "**Knowledge Lookup:**" in item["actual_allowed_operations_response"]
    assert "**Ticket Context Retrieval:**" in item["actual_allowed_operations_response"]
    assert item["source"]["native_authenticated_message_id"] is None
    assert item["source"]["native_decision_time"] is None
    assert all(item["authority_limits"][key] is False for key in [
        "requirement_approval", "requirement_update", "verification", "process_start",
        "implementation_runtime_authorization", "acceptance", "later_stage_authorized"])
    # Preflight all intended output absences before any recovery mutation.
    for p in [evidence_path, report_path, OWN / "checkpoint-0001.json", OWN / "report.md", OWN / "result.json"]:
        assert not lp(p).exists()
    evref = publish_prepared(evidence_path, evidence_bytes, True)
    oldreportref = publish_prepared(report_path, report_bytes, False)
    inputs_after = validate_inputs()
    for p, h in historical.items():
        assert digest(pathlib.Path(p).read_bytes()) == h
    receipt = common("checkpoint", "checkpoint-0001")
    receipt.update({
        "sequence": 1,
        "last_confirmed_boundary": "Original unchanged partials recovered to exact intended finals with flush/atomic-no-overwrite/readback; no prior success fabricated",
        "recovery_authorization": strict(lp(OWN / "attempt.json").read_bytes())["authorization"],
        "original_failure_evidence": {
            "original_attempt": ref(ORIGINAL / "attempt.json"),
            "failed_operation": ".NET File.ReadAllBytes normal 282-char path: DirectoryNotFoundException",
            "recovery_diagnosis": "Normal Python read failed; extended absolute Windows prefix read succeeded; GetFileAttributesW normal error 3 versus extended attributes 0x20/error 0. Same bytes confirmed. API normal-path handling limit established; process/registry configuration not asserted.",
            "original_partial_bases": [
                {"path": evref["path"] + ".partial", "bytes": 7603, "sha256": digest(evidence_bytes)},
                {"path": oldreportref["path"] + ".partial", "bytes": 6655, "sha256": digest(report_bytes)}],
            "preservation": "Original final invocation unchanged; failed partial bytes preserved exactly through authorized same-location atomic rename; failure/base evidence retained here, no partial duplicated or original failure erased"},
        "recovered_records": [evref, oldreportref],
        "related_records": [ref(OWN / "attempt.json"), ref(OWN / "attachments/recover.py")],
        "inputs_before": inputs_before, "inputs_after": inputs_after,
        "historical_final_hash_manifest": historical,
        "historical_finals_comparison": "PASS",
        "native_json_selftests": "Strict UTF-8 parse, common metadata, exact base/hash/full object roundtrip, authority limits/null times PASS",
        "readback": "Fresh reopen of each final; bytes/hash identical; JSON object equality for evidence",
        "exact_publication_time": None})
    receipt_ref = publish_json(OWN / "checkpoint-0001.json", receipt)
    body = (
        "# Q1 clarification publication recovery — successful\n\n"
        f"Work ID: `{WORK}`\n\nRecovery attempt: `{ATTEMPT}`; actor: SDLC Process Orchestrator "
        "`orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff`.\n\n"
        "State remains **REQUIREMENT_DECISION_PENDING**. Q2-Q10 remain unanswered. "
        "No question/policy was selected or later process started.\n\n"
        "Actual Human recovery authorization is retained in the own immutable invocation. "
        "Native authenticated message ID/time are null. This is one authorized recovery, not "
        "Requirement Approval, Update, Verification, Analysis or implementation/runtime permission.\n\n"
        "Cause: normal 282-character Windows API path access failed while extended `\\\\?\\` "
        "access read the same existing bytes. Win32 attributes were error 3 on normal path and "
        "0x20/error 0 on extended path. The failure was path handling, not lost/missing evidence. "
        "No claim about exact process/registry long-path settings.\n\n"
        "Original evidence and report partials were validated against exact pre-recovery bases, "
        "flushed with os.fsync and atomically renamed with Windows os.rename (no overwrite) "
        "to their originally intended paths. Fresh readback confirmed byte/hash/object equality. "
        "Original invocation and all historical final records remain unchanged; original partial "
        "bytes and failure evidence are bound in the recovery receipt. No outside relocation, "
        "stable-ID change, replacement or blind retry occurred.\n\n"
        "Actual Q1 boundary, all allowed operations/prohibitions, and full rationale remain in "
        "the unchanged original evidence. Substantive words/markdown preserved; userform "
        "whitespace layout is presentation, not byte-authenticated transport. Synthetic/local "
        "fictional first-release lookups only; external/live/customer data deferred, future scope "
        "requires separate approval/authorization. Recording does not close formal findings "
        "or edit/approve the draft.\n\n"
        "Canonical recovered records:\n\n"
        f"- Evidence: `{evref['path']}`, bytes {evref['bytes']}, SHA-256 `{evref['sha256']}`.\n"
        f"- Original report: `{oldreportref['path']}`, bytes {oldreportref['bytes']}, SHA-256 `{oldreportref['sha256']}`.\n"
        f"- Receipt: `{receipt_ref['path']}`, bytes {receipt_ref['bytes']}, SHA-256 `{receipt_ref['sha256']}`.\n\n"
        "Current 76 hidden-inclusive framework plus two target inputs/path set and Git HEAD "
        "are unchanged; no tracked/staged diff. No source probes, runtime/deploy, nested agent, "
        "Update/Verification/Analysis/other stage, staging/commit/push. Administrative "
        "read/hash/record publication evidence only, not formal Verification/runtime evidence. "
        "Local recovery is not remote backup; timestamps are preparation observations, "
        "not exact publication/native decision time.\n\n"
        "This recovery report/result do not assert original attempt technical success or "
        "rewrite its historical failure. Original report remains a bounded Q2 form for parent "
        "use only, not a new interactive question here. Stop after recovered Q1 publication.\n"
    ).encode("utf-8")
    partial = lp(OWN / "report.md.partial")
    assert not partial.exists()
    with partial.open("xb") as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())
    report_ref = publish_prepared(OWN / "report.md", body, False)
    result = common("result", "result")
    result.update({
        "execution_status": "COMPLETED",
        "completion_scope": "One bounded Q1 publication recovery only",
        "outcome": "Q1_CLARIFICATION_PUBLICATION_RECOVERED",
        "report": report_ref, "checkpoint": receipt_ref,
        "invocation": ref(OWN / "attempt.json"),
        "related_records": [evref, oldreportref, ref(ORIGINAL / "attempt.json")],
        "repository": {"canonical": "ScalableParimal/SupportIQ", "head": HEAD,
                       "branch": "sdlc-framework-onboarding"},
        "current_input_checks": validate_inputs(),
        "remaining_questions": "Q2-Q10 pending; not asked by recovery actor",
        "q1_recorded": True, "requirement_approved": False,
        "source_modified": False, "later_process_started": False,
        "historical_failure_erased": False,
        "limitations": "Native Human authenticated ID/time unavailable; whitespace presentation not byte authentication; endpoint checks not continuous monitoring; no remote backup",
        "publication_order": "Fresh recovery invocation first/readback; original evidence/report finals; recovery receipt; recovery report; result last after all bindings verified",
        "exact_publication_time": None})
    for value in [report_ref, receipt_ref, evref, oldreportref]:
        actual = ref(ROOT / value["path"])
        assert actual["sha256"] == value["sha256"] and actual["bytes"] == value["bytes"]
    result_ref = publish_json(OWN / "result.json", result)
    # Independent final reopening and all machine-derived bindings.
    actual_result = strict(lp(OWN / "result.json").read_bytes())
    assert actual_result == result
    for key in ["report", "checkpoint", "invocation"]:
        v = actual_result[key]
        assert ref(ROOT / v["path"]) == v
    for p, h in historical.items():
        assert digest(pathlib.Path(p).read_bytes()) == h
    assert validate_inputs() == inputs_before
    print("FINAL RECOVERY SUCCESS", json.dumps(result_ref))


if __name__ == "__main__":
    main()
