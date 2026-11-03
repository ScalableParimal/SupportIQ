"""Bounded actual Q2 transcription; no policy decisions or process execution."""
import pathlib
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path.cwd().resolve()
WORK = "supportiq-requirement-discovery-cb6472d0-3e33-4eeb-bf0b-ba01740ded1a"
ATTEMPT = "20261103T040945Z-db5b9506-5cf3-4fd5-9790-b665f0e2ddd1"
BASE = ROOT / "docs/sdlc-records/product" / WORK
OWN = BASE / "attempts" / ATTEMPT
SOURCE = pathlib.Path(r"C:\Users\Parimal\AppData\Local\Temp\1793678933628-copilot-tool-output-0597ad6b364149d8890c8624085223ef.txt")
SOURCE_HASH = "3C50A405F0651E326A8C5FB4516A075469FFE1EFE071A07DE304670D07F7BB18"


def lp(p):
    return pathlib.Path("\\\\?\\" + str(p.resolve()))


def sha(d):
    return hashlib.sha256(d).hexdigest().upper()


def strict(d):
    return json.loads(d.decode("utf-8", errors="strict"))


def ref(p):
    d = lp(p).read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(d), "sha256": sha(d)}


def common(kind, suffix):
    return {
        "schema_version": "1.0", "record_type": kind, "record_id": ATTEMPT + ":" + suffix,
        "work_id": WORK, "feature": "SupportIQ draft discovery; not one implementation feature",
        "attempt_id": ATTEMPT, "process": "SDLC Process Orchestrator Q2 clarification recording only",
        "creator": {"identity": "orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff",
                    "role": "SDLC Process Orchestrator; actual response transcriber, not decision-maker",
                    "effective_os_identity": "INT-SCL-010\\Parimal",
                    "harness_session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60"},
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "clock_basis": "Python UTC at preparation; not publication/native Human decision time",
        "gate": {"subject": "Existing Human clarification Q2", "formal_approval": False,
                 "process_initiation": False, "remaining": "Q3-Q10 pending"},
        "related_records": [ref(OWN / "attempt.json")],
        "task_context": "No Plan-local task; no later process execution",
        "state": "REQUIREMENT_DECISION_PENDING", "exact_publication_time": None}


def publish(p, d, is_json):
    d.decode("utf-8", errors="strict")
    if is_json:
        j = strict(d)
        for k in ["schema_version", "record_type", "record_id", "work_id", "feature",
                  "creator", "created_at_utc", "process", "attempt_id", "gate",
                  "related_records", "task_context"]:
            assert k in j
        assert j["work_id"] == WORK and j["attempt_id"] == ATTEMPT
    f = lp(p)
    partial = lp(p.with_name(p.name + ".partial"))
    assert not f.exists() and not partial.exists()
    with partial.open("xb") as s:
        s.write(d)
        s.flush()
        os.fsync(s.fileno())
    assert partial.read_bytes() == d and not f.exists()
    os.rename(partial, f)  # Windows no-overwrite same-directory atomic rename.
    fresh = f.read_bytes()
    assert fresh == d and sha(fresh) == sha(d)
    if is_json:
        assert strict(fresh) == strict(d)
    value = ref(p)
    print("PUBLISHED/READBACK PASS", json.dumps(value))
    return value


def pubjson(p, j):
    d = (json.dumps(j, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    assert strict(d) == j
    return publish(p, d, True)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], text=True).strip()


def inputs():
    assert git("rev-parse", "HEAD") == "ae355f5d5d538f9751ff6f7919433bd442979b2c"
    assert git("branch", "--show-current") == "sdlc-framework-onboarding"
    assert git("diff", "--name-only") == "" and git("diff", "--cached", "--name-only") == ""
    p = ROOT / "docs/sdlc-records/product/55ade040-7071-4fdf-a8a6-8dcdc18a8150/attempts/20261102T180059Z-36b3dfb9-ba84-4787-b9b7-97f8e75cda93/evidence/continuation-evidence.json"
    d = lp(p).read_bytes()
    assert sha(d) == "FE7D8E0B290CAD8587832B05699D449F250C689A8B5D8A88D1C59E3102EB4C49"
    j = strict(d)
    for key in ["source_inventory", "target_inventory"]:
        for v in j[key]:
            z = ref(ROOT / v["path"])
            assert z["bytes"] == v["bytes"] and z["sha256"] == v["sha256"]
    paths = {p.relative_to(ROOT).as_posix() for f in [".github", "docs/ai"]
             for p in (ROOT / f).rglob("*") if p.is_file()}
    assert paths == {v["path"] for v in j["source_inventory"]}
    return {"framework": 76, "targets": 2, "path_set": "PASS", "git_source_staging": "Unchanged"}


def main():
    assert os.name == "nt"
    assert sha(lp(OWN / "attempt.json").read_bytes()) == "0054C1039E1D5F312CBEEF1BC186DB92FB649460C75D01262B23C960EFF2C881"
    before = inputs()
    finals = {str(p): sha(p.read_bytes()) for p in lp(BASE).rglob("*")
              if p.is_file() and not p.name.endswith(".partial")}
    raw = lp(SOURCE).read_bytes()
    assert len(raw) == 15378 and sha(raw) == SOURCE_HASH
    text = raw.decode("utf-8", errors="strict")
    names = ["status_model", "transitions", "authority_matrix",
             "reviewer_eligibility", "rereview_policy", "rationale"]
    markers = list(re.finditer(r"(status_model|transitions|authority_matrix|reviewer_eligibility|rereview_policy|rationale)=", text))
    assert [m.group(1) for m in markers] == names and text[:markers[0].start()] == "User responded: "
    fields, slices = {}, {}
    for i, m in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        chunk = text[m.end():end]
        # Only the known tool transport delimiter is separated, never substantive words.
        delimiter = ", " if i + 1 < len(markers) else ""
        assert not delimiter or chunk.endswith(delimiter)
        fields[m.group(1)] = chunk[:-len(delimiter)] if delimiter else chunk
        slices[m.group(1)] = {"start": m.end(), "end": end,
                             "exact_rendered_segment": chunk, "transport_suffix": delimiter}
    # Exact source reconstruction is a selftest, not authenticated Human whitespace.
    rebuilt = text[:markers[0].start()] + "".join(
        n + "=" + fields[n] + slices[n]["transport_suffix"] for n in names)
    assert rebuilt == text and rebuilt.encode("utf-8") == raw
    assert fields["status_model"] == "Separate processing and approval statuses"
    assert "intentionally deferred to Q3" in fields["transitions"]
    assert "overdue-review and stale/conflicting knowledge rules remain subject to Q3" in fields["authority_matrix"]
    assert "Overdue documents must immediately become ineligible for AI retrieval and citation." in fields["rereview_policy"]
    assert "beyond the agreed 180-day overdue policy" in fields["rationale"]
    discrepancy = {
        "subject": "Q2 cross-field overdue-review deferral wording",
        "earlier_field_provenance": ["transitions", "authority_matrix"],
        "dedicated_policy_provenance": ["rereview_policy", "rationale"],
        "observation": "Earlier fields defer exact overdue-review rules to Q3; dedicated policy and final rationale explicitly decide the 180-day rule and defer other stale/conflicting/insufficient criteria beyond that policy.",
        "treatment": "Both source fields preserved faithfully. Dedicated explicit policy recorded as supplied, not erased or silently overridden. Before applying changed Requirement text, parent should confirm whether earlier deferral wording was intended to reserve only other Q3 criteria.",
        "human_confirmation": None,
        "no_automatic_resolution": True}
    evidence = common("evidence", "q2-clarification")
    evidence.update({
        "source": {"path": str(SOURCE), "bytes": len(raw), "sha256": sha(raw),
                   "attribution": "Actual tool response designated by current parent Human conversation; not authenticated platform message identity",
                   "available_message_context_time": "2026-11-03T09:39:34.792+05:30",
                   "native_authenticated_message_id": None, "native_decision_time": None,
                   "whitespace_limit": "Raw file bytes/hash preserved for integrity and recovery, not authenticated Human whitespace or decision time"},
        "raw_tool_response": text, "actual_fields": fields, "field_slices": slices,
        "source_reconstruction_test": "PASS exact retained UTF-8 text and bytes",
        "cross_field_discrepancy": discrepancy,
        "authority_limits": {"clarification_only": True, "requirement_approval": False,
                             "requirement_update": False, "verification": False,
                             "analysis_refresh": False, "process_start": False,
                             "implementation_runtime_authorization": False},
        "deferrals": "Q3 other stale/conflicting/insufficient criteria and routing/handling beyond dedicated 180-day policy; Q5 deletion/purge/retention; detailed notification/escalation schedules as supplied. Earlier broad Q3 deferrals retained.",
        "no_new_decision": "Transcription only; no role assignments, grace periods, precedence, deletion policy or future connector invented"})
    for p in [OWN / "attachments/q2.json", OWN / "checkpoint-0001.json",
              OWN / "report.md", OWN / "result.json"]:
        assert not lp(p).exists() and not lp(p.with_name(p.name + ".partial")).exists()
    ev = pubjson(OWN / "attachments/q2.json", evidence)
    fresh = strict(lp(OWN / "attachments/q2.json").read_bytes())
    assert fresh["actual_fields"] == fields and fresh["raw_tool_response"].encode("utf-8") == raw
    for p, h in finals.items():
        assert sha(pathlib.Path(p).read_bytes()) == h
    receipt = common("checkpoint", "checkpoint-0001")
    receipt.update({
        "sequence": 1, "last_confirmed_boundary": "Q2 raw/full fields/rationale and discrepancy durably published/read back; no later process",
        "evidence": ev, "related_records": [ref(OWN / "attempt.json"), ev, ref(OWN / "attachments/publish.py")],
        "selftests": {"strict_native_json": "PASS", "source_reconstruction": "PASS",
                      "full_field_object_equality": "PASS", "common_metadata": "PASS",
                      "cross_field_provenance_and_null_authentication": "PASS",
                      "historical_final_hashes": "PASS"},
        "historical_final_manifest": finals, "inputs_before": before, "inputs_after": inputs(),
        "publication": "Absolute extended Windows paths; exclusive .partial write; validation/flush/fsync; atomic Windows no-overwrite rename; independent final reopen byte/hash/object equality"})
    cp = pubjson(OWN / "checkpoint-0001.json", receipt)
    body = (
        "# Q2 clarification recorded — Requirement decisions remain pending\n\n"
        f"Work: `{WORK}`; own Orchestrator attempt `{ATTEMPT}`. "
        "Actor: `orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff`.\n\n"
        "State: **REQUIREMENT_DECISION_PENDING**. Q1 remains recorded; Q2 actual fields/rationale "
        "recorded; Q3-Q10 remain unanswered. No source, approval, update, verification, Analysis, "
        "refresh, nested agent or later stage is performed.\n\n"
        "The own qualified invocation was durably published/read back first. Exact source tool "
        "response is retained as raw UTF-8 text plus all six full field values and source offsets "
        "in attachments/q2.json. No summary replaces the decision or rationale. Source hash "
        "identifies file bytes only; no authenticated Human whitespace/message ID/time claimed. "
        "Native authenticated identifiers/times remain null.\n\n"
        "## Source-supported Q2 clarification summary (not replacement)\n\n"
        "Separate processing and approval states; processing Uploaded -> Processing -> Indexed/Failed "
        "and authorized retry; independent Draft/Pending Review/Approved Current/Rejected/revised "
        "Draft/Superseded/Expired transitions. Indexed never implies approval. Replacement must "
        "complete processing and independent approval before superseding a prior current version; "
        "this does not waive existing validity/overdue/tenant/user restrictions. Only indexed, "
        "approved/current, currently valid and authorized content is retrievable.\n\n"
        "Tenant-scoped explicit roles separate requests, authorization and execution. Tenant Admin "
        "upload/submit/request/monitor; explicitly assigned Knowledge Reviewer independent approval/"
        "rejection/expiry. Support roles alone do not grant maintenance/approval privileges. "
        "Platform Admin has no routine content/approval or review bypass. System executes authorized "
        "processing/policy actions, never independently approves. Submitter cannot self-approve "
        "even with multiple roles. No eligible reviewer means pending/unsearchable, notification, "
        "no automatic approval/self-approval/Platform Admin override; eligible same-tenant backup allowed.\n\n"
        "The dedicated rereview_policy field explicitly starts/resets each version's 180-day period "
        "on explicit approval/reapproval, not upload/index/reprocessing/metadata retry. Tenant Admin "
        "owns assignment and designated reviewer actual review. At deadline without review, Review "
        "Overdue/Pending Re-review immediately excludes AI retrieval/citation; authorized human "
        "review access remains, no automatic extension. Return to eligibility requires explicit "
        "non-submitter review/reapproval and all current eligibility conditions. Audits and notifications "
        "required; schedules/operational escalation may be refined as supplied.\n\n"
        "## Cross-field clarification issue — not silently resolved\n\n"
        "transitions says exact 180-day overdue behavior is deferred to Q3; authority_matrix also "
        "defers overdue-review rules. In contrast rereview_policy and final rationale explicitly "
        "decide that policy and reserve Q3 for other stale/conflicting/insufficient criteria and "
        "routing/handling beyond the agreed policy. All fields are faithfully retained. Do not "
        "claim all 180-day policy undecided, ignore the dedicated policy, or silently rewrite the "
        "earlier fields. Parent should obtain confirmation before reconciling amended source text: "
        "were those earlier deferrals intended to reserve only the other Q3 criteria? No confirmation "
        "or precedence decision is invented here.\n\n"
        "Q5 deletion/purge/retention remains explicitly deferred. No purge/retention or unrelated "
        "permissions are decided by this recording. A transitions reference to 'designated knowledge "
        "manager' is preserved, not promoted into an invented role assignment; explicit role limits remain.\n\n"
        "## Bounded Q3 questions for parent use only\n\n"
        "Source: actual Analysis report section 9 question 3, RA-A03/RA-M03. With dedicated Q2 "
        "180-day statements preserved and the wording issue visible, ask only: (1) additional stale "
        "criteria/triggers beyond the 180-day rule; (2) what constitutes conflicting or insufficient "
        "knowledge and how it is reported/detected; (3) who receives/owns human-review flags, "
        "tenant-scoped routing/backup/escalation; (4) retrieval/citation/abstention and human-review "
        "handling while those other conditions are unresolved; (5) authorized resolution/reinstatement "
        "and rationale or explicit deferrals. Keep deletion/retention for Q5. No defaults/options "
        "are selected, no Q3 is asked by this actor, and no broader detection architecture is planned.\n\n"
        "## Canonical integrity\n\n"
        f"- Evidence `{ev['path']}`, bytes {ev['bytes']}, SHA-256 `{ev['sha256']}`.\n"
        f"- Receipt `{cp['path']}`, bytes {cp['bytes']}, SHA-256 `{cp['sha256']}`.\n\n"
        "All outputs used current absolute Windows extended paths, validated .partial preparation, "
        "flush/fsync, atomic same-directory no-overwrite rename, and fresh readback. Historical "
        "final hashes and 78 source/target fingerprints/hidden-inclusive pathset remain unchanged. "
        "HEAD ae355f5d5d538f9751ff6f7919433bd442979b2c, branch sdlc-framework-onboarding, "
        "no source/staged change. Local administrative publication is not formal Verification, "
        "runtime behavior or remote backup. No PRD/project/runtime/deploy/staging/commit/push. "
        "Report/result timestamps are preparation observations, not publication/native decision time. "
        "Stop after Q2 recording.\n"
    ).encode("utf-8")
    rp = publish(OWN / "report.md", body, False)
    result = common("result", "result")
    result.update({
        "execution_status": "COMPLETED", "completion_scope": "Actual Q2 clarification transcription only",
        "outcome": "Q2_RECORDED_WITH_CROSS_FIELD_WORDING_CONFIRMATION_PENDING",
        "report": rp, "checkpoint": cp, "invocation": ref(OWN / "attempt.json"),
        "evidence": ev, "related_records": [ev, ref(OWN / "attempt.json")],
        "q2_recorded": True, "remaining_questions": "Q3-Q10 pending",
        "cross_field_issue": discrepancy, "q3_presented": False,
        "requirement_approved": False, "requirement_updated": False,
        "later_process_started": False, "source_modified": False,
        "inputs": inputs(), "publication_order": "Own invocation first/readback; evidence; receipt; report; result last",
        "limitations": "Exact raw transport preserved but no authenticated Human whitespace/message ID/native time; no implicit policy selection/precedence; local persistence not remote backup"})
    for v in [rp, cp, ev]:
        assert ref(ROOT / v["path"]) == v
    rs = pubjson(OWN / "result.json", result)
    fresh_result = strict(lp(OWN / "result.json").read_bytes())
    for k in ["report", "checkpoint", "invocation", "evidence"]:
        assert ref(ROOT / fresh_result[k]["path"]) == fresh_result[k]
    for p, h in finals.items():
        assert sha(pathlib.Path(p).read_bytes()) == h
    assert inputs() == before and lp(SOURCE).read_bytes() == raw
    print("FINAL Q2 PUBLICATION SUCCESS", json.dumps(rs))


if __name__ == "__main__":
    main()
