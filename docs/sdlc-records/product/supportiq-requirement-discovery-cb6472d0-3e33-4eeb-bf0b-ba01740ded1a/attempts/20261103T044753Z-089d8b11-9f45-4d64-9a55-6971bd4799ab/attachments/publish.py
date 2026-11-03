"""Own clarification evidence publication only; no policy choice or later process."""
import pathlib
import hashlib
import json
import re
import os
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path.cwd().resolve()
WORK = "supportiq-requirement-discovery-cb6472d0-3e33-4eeb-bf0b-ba01740ded1a"
ATTEMPT = "20261103T044753Z-089d8b11-9f45-4d64-9a55-6971bd4799ab"
BASE = ROOT / "docs/sdlc-records/product" / WORK
OWN = BASE / "attempts" / ATTEMPT
SOURCE = pathlib.Path(r"C:\Users\Parimal\AppData\Local\Temp\1793681194955-copilot-tool-output-9619f50b5fe5490eb4ab5a053a4ddc88.txt")
CONFIRMATION = "Confirm the dedicated 180-day policy is decided; Q3 deferrals cover only additional criteria, and replacement rules do not waive validity or authorization restrictions"


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
        "attempt_id": ATTEMPT,
        "process": "SDLC Process Orchestrator Q2 confirmation and Q3 recording only",
        "creator": {"identity": "orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff",
                    "role": "SDLC Process Orchestrator; actual supplied response transcriber",
                    "effective_os_identity": "INT-SCL-010\\Parimal",
                    "harness_session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60"},
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "clock_basis": "Python system UTC at preparation, not publication/native Human decision time",
        "gate": {"subject": "Existing Human clarification Q2 confirmation/Q3",
                 "formal_requirement_approval": False, "process_start": False,
                 "remaining": "Q4-Q10 pending"},
        "related_records": [ref(OWN / "attempt.json")],
        "task_context": "No Plan-local task; no new Analysis or later process",
        "state": "REQUIREMENT_DECISION_PENDING", "exact_publication_time": None}


def publish(p, data, is_json):
    data.decode("utf-8", errors="strict")
    if is_json:
        obj = strict(data)
        for key in ["schema_version", "record_type", "record_id", "work_id", "feature",
                    "creator", "created_at_utc", "process", "attempt_id", "gate",
                    "related_records", "task_context"]:
            assert key in obj
        assert obj["work_id"] == WORK and obj["attempt_id"] == ATTEMPT
    final = lp(p)
    partial = lp(p.with_name(p.name + ".partial"))
    assert not final.exists() and not partial.exists()
    with partial.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert partial.read_bytes() == data and not final.exists()
    os.rename(partial, final)  # Windows atomic same-directory rename, fails if destination exists.
    fresh = final.read_bytes()
    assert fresh == data and sha(fresh) == sha(data)
    if is_json:
        assert strict(fresh) == strict(data)
    result = ref(p)
    print("PUBLISHED/READBACK PASS", json.dumps(result))
    return result


def pubjson(p, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    assert strict(data) == value
    return publish(p, data, True)


def inputs():
    def git(*args):
        return subprocess.check_output(["git", "--no-pager", *args], text=True).strip()
    assert git("rev-parse", "HEAD") == "ae355f5d5d538f9751ff6f7919433bd442979b2c"
    assert git("branch", "--show-current") == "sdlc-framework-onboarding"
    assert not git("diff", "--name-only") and not git("diff", "--cached", "--name-only")
    p = ROOT / "docs/sdlc-records/product/55ade040-7071-4fdf-a8a6-8dcdc18a8150/attempts/20261102T180059Z-36b3dfb9-ba84-4787-b9b7-97f8e75cda93/evidence/continuation-evidence.json"
    data = lp(p).read_bytes()
    assert sha(data) == "FE7D8E0B290CAD8587832B05699D449F250C689A8B5D8A88D1C59E3102EB4C49"
    manifest = strict(data)
    for key in ["source_inventory", "target_inventory"]:
        for v in manifest[key]:
            actual = ref(ROOT / v["path"])
            assert actual["sha256"] == v["sha256"] and actual["bytes"] == v["bytes"]
    paths = {p.relative_to(ROOT).as_posix() for folder in [".github", "docs/ai"]
             for p in (ROOT / folder).rglob("*") if p.is_file()}
    assert paths == {v["path"] for v in manifest["source_inventory"]}
    return {"framework": 76, "targets": 2, "hidden_inclusive_path_set": "PASS",
            "head_branch_source_staging": "Unchanged"}


def main():
    assert os.name == "nt"
    assert sha(lp(OWN / "attempt.json").read_bytes()) == "4323D577942D29EBA98236A17EE39A2D23682A54DD0860406D34B17C624919C5"
    prior = BASE / "attempts/20261103T040945Z-db5b9506-5cf3-4fd5-9790-b665f0e2ddd1"
    assert sha(lp(prior / "attachments/q2.json").read_bytes()) == "DB88FEA84D7143237D743745EAE4669733E12F80BAD6BA4A870227B6D0E7BD06"
    before = inputs()
    historical = {str(p): sha(p.read_bytes()) for p in lp(BASE).rglob("*")
                  if p.is_file() and not p.name.endswith(".partial")}
    raw = lp(SOURCE).read_bytes()
    assert len(raw) == 26718 and sha(raw) == "42634BD2A9CDAF72A63FFD1BE394684F5A877424A7DB2E9FC8DCA766723F7522"
    text = raw.decode("utf-8", errors="strict")
    names = ["additional_staleness", "conflict_insufficiency", "review_ownership",
             "unresolved_behavior", "resolution", "rationale"]
    markers = list(re.finditer(r"(additional_staleness|conflict_insufficiency|review_ownership|unresolved_behavior|resolution|rationale)=", text))
    assert [m.group(1) for m in markers] == names and text[:markers[0].start()] == "User responded: "
    fields, slices = {}, {}
    for i, m in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        segment = text[m.end():end]
        delimiter = ", " if i + 1 < len(markers) else ""
        assert not delimiter or segment.endswith(delimiter)
        fields[m.group(1)] = segment[:-len(delimiter)] if delimiter else segment
        slices[m.group(1)] = {"start": m.end(), "end": end,
                             "exact_rendered_segment": segment, "transport_suffix": delimiter}
    rebuilt = text[:markers[0].start()] + "".join(
        n + "=" + fields[n] + slices[n]["transport_suffix"] for n in names)
    assert rebuilt.encode("utf-8") == raw
    assert "Only explicitly established and approved precedence rules may resolve a conflict automatically." in fields["conflict_insufficiency"]
    assert "must never independently approve, resolve, or reinstate previously excluded knowledge." in fields["resolution"]
    assert "A clarification or resolution alone does not constitute a new approval or reset the 180-day review clock." in fields["resolution"]
    for p in [OWN / "attachments/q2-confirm.json", OWN / "attachments/q3.json",
              OWN / "checkpoint-0001.json", OWN / "report.md", OWN / "result.json"]:
        assert not lp(p).exists() and not lp(p.with_name(p.name + ".partial")).exists()
    source_attribution = {
        "channel": "Actual current parent Human conversation",
        "harness_session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
        "available_message_context_time": "2026-11-03T10:17:41.773+05:30",
        "native_authenticated_message_id": None, "native_decision_time": None,
        "limit": "Actual supplied conversation attribution; not cryptographic Human identity or byte-authenticated whitespace"}
    confirmation = common("evidence", "q2-confirmation")
    confirmation.update({
        "actual_confirmation": CONFIRMATION, "source": source_attribution,
        "original_q2_evidence": ref(prior / "attachments/q2.json"),
        "original_q2_result": ref(prior / "result.json"),
        "subject": "Earlier Q2 broad deferral wording versus dedicated 180-day policy",
        "meaning_as_supplied": "Dedicated policy decided; Q3 deferrals only additional criteria; replacement does not waive validity/authorization",
        "preservation": "Original Q2 fields and discrepancy remain immutable; new confirmation linked, not source rewritten",
        "authority_limits": "Clarification only; no Requirement approval/update/verification/start or runtime permission"})
    confref = pubjson(OWN / "attachments/q2-confirm.json", confirmation)
    issue = {
        "subject": "Automatic source-precedence selection versus Human flagged/excluded-content resolution",
        "automatic_rule_source": {"field": "conflict_insufficiency",
                                  "quote": "Only explicitly established and approved precedence rules may resolve a conflict automatically."},
        "human_review_source": {"field": "resolution",
                               "quote": "AI and automated system processes may collect evidence, generate flags, and recommend review actions but must never independently approve, resolve, or reinstate previously excluded knowledge."},
        "observation": "Both statements preserved. A possible distinction is ordinary selection among otherwise eligible sources versus final resolution/reinstatement of flagged/excluded content; this distinction is not adopted as a new policy by Orchestrator.",
        "parent_confirmation_needed": "Before implementing/applying changed source, confirm that approved-rule automatic selection never closes flagged/excluded issues or reinstates excluded knowledge without authorized non-submitter Human review.",
        "response": None, "automatic_reinstatement_authorized_by_orchestrator": False}
    evidence = common("evidence", "q3-clarification")
    evidence.update({
        "source": {**source_attribution, "path": str(SOURCE), "bytes": len(raw), "sha256": sha(raw),
                   "integrity_limit": "Raw file hash/offsets preserve actual transport text only, not authenticated Human whitespace/message ID/time"},
        "raw_tool_response": text, "actual_fields": fields, "field_slices": slices,
        "roundtrip_selftest": "Exact retained UTF-8 reconstruction and native JSON object equality PASS",
        "q2_confirmation": confref, "cross_field_scope_issue": issue,
        "explicit_deferrals": "Q5 deletion/purge/retention/backup; operational response/notification/escalation timings; technical detection algorithms; numeric thresholds; section-level implementation details as supplied",
        "authority_limits": {"clarification_only": True, "requirement_approval": False,
                             "requirement_update": False, "verification": False,
                             "process_start": False, "runtime_implementation": False},
        "related_records": [ref(OWN / "attempt.json"), confref],
        "no_policy_selection": "All actual words preserved; no invented precedence metadata/rules, automatic reinstatement, thresholds or account permissions"})
    evref = pubjson(OWN / "attachments/q3.json", evidence)
    fresh = strict(lp(OWN / "attachments/q3.json").read_bytes())
    assert fresh["raw_tool_response"].encode("utf-8") == raw and fresh["actual_fields"] == fields
    assert strict(lp(OWN / "attachments/q2-confirm.json").read_bytes())["actual_confirmation"] == CONFIRMATION
    for p, h in historical.items():
        assert sha(pathlib.Path(p).read_bytes()) == h
    receipt = common("checkpoint", "checkpoint-0001")
    receipt.update({
        "sequence": 1, "last_confirmed_boundary": "Q2 exact confirmation and Q3 raw/full fields/rationale durably published/readback; no later process",
        "related_records": [ref(OWN / "attempt.json"), ref(OWN / "attachments/publish.py"), confref, evref],
        "selftests": {"common_metadata": "PASS", "strict_utf8_native_json": "PASS",
                      "raw_source_roundtrip": "PASS", "all_field_objects_and_offsets": "PASS",
                      "exact_confirmation": "PASS", "null_native_authentication": "PASS",
                      "no_overwrite_and_fresh_readback": "PASS"},
        "historical_final_manifest": historical,
        "inputs_before": before, "inputs_after": inputs(),
        "cross_field_scope_issue": issue,
        "publication": "Absolute extended Windows paths; exclusive partial preparation, flush/fsync, validated same-directory Windows atomic no-overwrite rename, fresh bytes/hash/object readback"})
    cpref = pubjson(OWN / "checkpoint-0001.json", receipt)
    body = (
        "# Q2 confirmation and Q3 clarification recorded\n\n"
        f"Work `{WORK}`; own Orchestrator attempt `{ATTEMPT}`; actor "
        "`orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff`.\n\n"
        "State **REQUIREMENT_DECISION_PENDING**. Q4-Q10 unanswered. Own invocation "
        "qualified/published/readback first; no source edits or other process.\n\n"
        "## Exact supplied Q2 confirmation\n\n"
        f"> {CONFIRMATION}\n\n"
        "This is linked evidence, not revision of original Q2 fields/history or Requirement Approval. "
        "Q2's earlier wording concern now has an explicit Human clarification; original fields "
        "and pending-history records remain intact.\n\n"
        "## Q3 actual evidence\n\n"
        "All six actual fields and full rationale/deferrals are retained in attachments/q3.json "
        "with raw tool text, field offsets and reconstruction test. This summary is not replacement. "
        "Raw file integrity is not authenticated Human whitespace/message ID/native time; nulls preserved.\n\n"
        "Additional staleness triggers include validity expiry, superseding/withdrawn authority, "
        "product changes and credible human/AI concerns. Potential flags differ from confirmed "
        "lifecycle decisions. Credible/objective concerns exclude affected versions pending "
        "eligible tenant non-submitter review; authorized human inspection remains separate. "
        "AI detects/reports/recommends but does not gain lifecycle/reinstatement authority.\n\n"
        "Conflicts are material contradictions among otherwise eligible applicable sources, "
        "distinguished from valid date/version/tenant differences. Insufficiency means inadequate "
        "direct support/context/citations; no fabricated gap filling or numeric thresholds. "
        "Explicit approved authority/applicability precedence may be used; ranking/upload timestamp "
        "alone is not authority; unresolved contradictions require abstention/review.\n\n"
        "Tenant Admin owns operational acknowledgement/assignment/tracking; explicitly assigned "
        "eligible Primary Knowledge Reviewer owns final decisions. Eligible backup/escalation "
        "required as stated, timings deferred. Support Manager operational follow-up grants no "
        "approval authority; no eligible reviewer means issue open/content excluded/no automatic bypass.\n\n"
        "Retrieval requires indexed/approved-current/currently valid/not unresolved/180-day "
        "current/tenant-user authorization; fail closed including cached/indexed content. Whole "
        "affected version initially excluded; portions require explicit independent review and "
        "traceable controls, implementation details deferred. AI abstains unsupported/conflicting/"
        "ineligible claims, uses eligible references only, no hidden excluded evidence. Human "
        "inspection is restricted; mere KB existence grants Support Agents no excluded-content access.\n\n"
        "Authorized non-submitter reviewer determines resolution. Unfounded flag closure is not "
        "new approval or 180-day reset; all old validity restrictions remain. Corrections require "
        "new full processing/independent approval. Formal explicit re-review approval alone resets "
        "an existing clock; new version starts on first explicit approval. No reinstatement bypasses "
        "overdue review. Full rationale prioritizes safety over availability with targeted exclusion "
        "rather than tenant-wide disablement.\n\n"
        "## Cross-field scope confirmation for parent\n\n"
        "conflict_insufficiency permits approved precedence rules to resolve conflicts automatically; "
        "resolution reserves final decisions about flagged/previously excluded content for Human "
        "review. Preserve both. Parent should confirm scope before applying source/implementation: "
        "approved-rule ordinary source selection must not be interpreted as automatic flag closure "
        "or reinstatement of excluded knowledge. A preflag-selection versus reinstatement "
        "distinction is a clarification option, not a policy chosen here. No automatic reinstatement "
        "or precedence metadata/rules are invented.\n\n"
        "## Bounded Q4 form for parent only\n\n"
        "Actual Analysis section 9 question 4 (RA-A04/RA-M04): account creation/disablement/recovery, "
        "role-operation permissions, exceptional Platform Admin authorizer, maximum duration, "
        "reason/audit fields and revocation. Parent may group as: (1) authorized account provisioning "
        "and tenant assignment; (2) disable/reactivate/recovery actors and constraints; (3) explicit "
        "role-to-operation map, preserving Q2/Q3 knowledge restrictions; (4) exceptional access "
        "grantor/subject/tenant/data scope, time limit, rationale and audit; (5) expiry/revocation "
        "and oversight; (6) rationale/deferrals. No defaults or permissions selected; no Q4 asked "
        "by recording actor. Exceptions must not silently grant knowledge approval/reinstatement "
        "or reviewer independence bypass.\n\n"
        "Q5 deletion/purge/retention/backup, operational timings, detailed detection algorithms, "
        "numeric thresholds and section implementation details remain expressly deferred. "
        "No PRD/Requirement Update/Verification/Analysis/refresh or runtime authorization.\n\n"
        "## Canonical binding references\n\n"
        f"- Q2 confirmation `{confref['path']}`, {confref['bytes']} bytes, SHA-256 `{confref['sha256']}`.\n"
        f"- Q3 full evidence `{evref['path']}`, {evref['bytes']} bytes, SHA-256 `{evref['sha256']}`.\n"
        f"- Receipt `{cpref['path']}`, {cpref['bytes']} bytes, SHA-256 `{cpref['sha256']}`.\n\n"
        "Historical finals and 78 framework/target fingerprints/hidden-inclusive pathset unchanged. "
        "HEAD ae355f5d5d538f9751ff6f7919433bd442979b2c; branch sdlc-framework-onboarding; "
        "no tracked/staged diff. No nested agent, source/project/runtime/deploy/staging/commit/push. "
        "Current administrative record checks are not independent Verification/runtime evidence. "
        "No authenticated native Human ID/time or byte-whitespace claim; local records not remote "
        "backup. All publication used validated partials, flush/fsync, extended Windows paths, "
        "no-overwrite atomic rename and independent readback. Stop after recording.\n"
    ).encode("utf-8")
    rpref = publish(OWN / "report.md", body, False)
    result = common("result", "result")
    result.update({
        "execution_status": "COMPLETED",
        "outcome": "Q2_CONFIRMATION_AND_Q3_RECORDED_WITH_SCOPE_CLARIFICATION_PENDING",
        "completion_scope": "Actual supplied confirmation and Q3 transcription only",
        "report": rpref, "checkpoint": cpref, "invocation": ref(OWN / "attempt.json"),
        "q2_confirmation": confref, "q3_evidence": evref,
        "q2_confirmation_recorded": True, "q3_recorded": True,
        "cross_field_scope_issue": issue, "remaining_questions": "Q4-Q10 pending",
        "q4_asked": False, "requirement_approved": False,
        "source_modified": False, "later_process_started": False,
        "related_records": [confref, evref, ref(prior / "result.json")],
        "current_inputs": inputs(),
        "publication_order": "Own invocation first/readback; exact confirmation; full Q3 evidence; receipt; report; result last",
        "limitations": "Native Human authenticated ID/time unavailable; raw transport integrity not byte-authenticated whitespace; no policy precedence or automatic reinstatement inferred"})
    for v in [confref, evref, cpref, rpref]:
        assert ref(ROOT / v["path"]) == v
    rsref = pubjson(OWN / "result.json", result)
    final = strict(lp(OWN / "result.json").read_bytes())
    for k in ["report", "checkpoint", "invocation", "q2_confirmation", "q3_evidence"]:
        assert ref(ROOT / final[k]["path"]) == final[k]
    for p, h in historical.items():
        assert sha(pathlib.Path(p).read_bytes()) == h
    assert inputs() == before and lp(SOURCE).read_bytes() == raw
    print("FINAL PUBLICATION SUCCESS", json.dumps(rsref))


if __name__ == "__main__":
    main()
