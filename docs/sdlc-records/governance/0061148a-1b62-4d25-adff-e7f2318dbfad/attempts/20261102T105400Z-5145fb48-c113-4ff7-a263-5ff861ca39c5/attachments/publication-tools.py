"""Actor-owned publication/evidence helper; no source writes."""
import ctypes
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T105400Z-5145fb48-c113-4ff7-a263-5ff861ca39c5"
BASE = ROOT / "docs/sdlc-records/governance" / WORK / "attempts" / ATTEMPT
ACTOR = "local-corrective-change-decision:" + ATTEMPT
START = "Yes, initiate Corrective Change Decision & Plan Update for GOV-AUD-20261102-002 only under the existing Work ID and Cycle 1 using Investigation attempt 20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff; proposal only, no correction or other stage"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def cmd(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()

def ref(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    b = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest().upper()}

def encoded(obj):
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    assert json.loads(b) == obj, "complete actual object roundtrip mismatch"
    assert b"\\u2014" not in b, "unexpected ASCII escaping"
    return b

def publish(name, obj, raw=False):
    target = BASE / name
    assert target.is_relative_to(BASE)
    assert not target.exists(), "final collision"
    target.parent.mkdir(parents=True, exist_ok=True)
    data = obj if raw else encoded(obj)
    if not raw:
        json.loads(data)
    else:
        data.decode("utf-8", errors="strict")
    partial = Path(str(target) + ".partial")
    with partial.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == data
    move = ctypes.WinDLL("kernel32", use_last_error=True).MoveFileExW
    move.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
    move.restype = ctypes.c_int
    if not move(str(partial), str(target), 0x8):
        raise ctypes.WinError(ctypes.get_last_error())
    assert target.read_bytes() == data
    return ref(target)

def common(kind):
    return {"schema_version": "1.0", "record_type": kind,
            "record_id": ATTEMPT + ":" + kind, "work_id": WORK,
            "attempt_id": ATTEMPT, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
            "cycle": 1, "creator": {"role": "Corrective Change Decision",
            "actor_identity": ACTOR, "runtime_agent_id_observed": "0939dcbe-f104-454a-a8bd-62e36810ccd3",
            "identity_limit": "Runtime roster association, not authenticated platform identity"},
            "created_at_utc": now(),
            "clock_basis": "Host UTC sample during record preparation; not publication timestamp",
            "process": "Corrective Change Decision & Plan Update",
            "subject_type": "FINDING", "finding_id": "GOV-AUD-20261102-002"}

def preflight():
    assert not (BASE / "attempt.json").exists()
    inputs = []
    expected = {
        "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/report.md": "C3E467C0A94CACD0BBC01FB0AAA0820293C715890D239FEEA3ED0C8A3ABF8E65",
        "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/result.json": "95155D44BF54F3FF302021EE8C585838862AD2000B8922DEB73766C03B54BCB5",
        "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/attachments/evidence.json": "9D84E95108116DEBDAA4677BA1FF43D5878E9A2CD8D09CF64EFB19DDB95E2A74",
        "20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f/report.md": "4246B0BAA6A945678034706AE02E26162CD2DB940D8FAC3F2AB7749D76B477A2",
        "20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f/result.json": "3C628AA7BC8ECDF2194EC5FBA13911BB183B45A0BBA4CD57E81CF4B4FBF23231",
        "20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f/evidence/audit-evidence.json": "888ABF5B0E14829F0EC2FF824510DB1E3B8DB3CC1636F29B3DD6E44DF5104AF2",
        "20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/report.md": "0E819BDD31747BA24037C89130D1A25A8E642A7EB0BBF9DF267C34DBD815C768",
        "20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/result.json": "F65D96FC76105E4546CC5318BF7D3E4A8E41784486449BE3CE55726840CE2AD2",
        "20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/attachments/investigation-handoff.md": "59436AEE6D74EC483B89B62F190D6330B85241CB3359D126EFED31EEC43627B3",
    }
    for path, digest in expected.items():
        r = ref(BASE.parent / path)
        assert r["sha256"] == digest, r
        inputs.append(r)
    masters = [
        ("SDLC_GOVERNANCE.md", "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B"),
        ("SDLC_ARTIFACT_GOVERNANCE.md", "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860"),
        ("SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md", "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C")]
    for name, digest in masters:
        assert ref("docs/ai/sdlc/" + name)["sha256"] == digest
    assert cmd("git", "rev-parse", "HEAD") == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert cmd("git", "remote", "get-url", "origin") == "https://github.com/ScalableParimal/SupportIQ.git"
    assert not (ROOT / "docs/sdlc-records/product" / WORK).exists()
    baseline = [ref(p) for top in [ROOT / "docs", ROOT / ".github", ROOT / "README.md"]
                for p in ([top] if top.is_file() else sorted(top.rglob("*")))
                if p.is_file() and not p.is_relative_to(BASE)]
    record = common("invocation")
    record.update({
        "authorization": {"actual_human_start": START,
            "source": "Actual Human instruction supplied in current parent conversation",
            "authenticated_message_id": None, "authenticated_human_time": None,
            "scope": "Proposal-only decision for GOV-AUD-20261102-002; own new records only",
            "not_authorized": ["application", "other stage", "adoption", "commit", "push", "product work"]},
        "repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
            "head": cmd("git", "rev-parse", "HEAD"), "branch": cmd("git", "branch", "--show-current"),
            "remote": cmd("git", "remote", "get-url", "origin"), "status": cmd("git", "status", "--short")},
        "persistence": {"root": "docs/sdlc-records/governance/", "own_scope": BASE.relative_to(ROOT).as_posix(),
            "reservation": ref(BASE.parent / "20261030T123604Z-15be0f40-a028-4166-bb27-fbf5fdefecc4/attempt.json"),
            "root_decision": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                "author": "ScalableParimal", "author_association": "OWNER",
                "created_at": "2026-10-30T12:31:51Z", "updated_at": "2026-10-30T12:31:51Z",
                "current_resolution": "GitHub issue_read get_comments during current invocation; exact HEAD/Masters/root/Work ID matched",
                "scope": "Root adoption retained; one-time initial Audit start NOT reused"},
            "master_status": "Candidate bootstrap comparison sources, not adopted target Master baseline; product root not adopted"},
        "qualification": {"effective_identity": cmd("whoami", "/user"),
            "permissions": "Current Get-Acl on attempts parent: Authenticated Users Modify; Administrators and SYSTEM FullControl",
            "role": ref(".github/agents/corrective-change-decision.agent.md"),
            "current_capabilities": ["Python 3.14.7 available", "Read/hash/strict UTF-8/JSON access demonstrated",
                "Declared apply_patch for actor-owned helper preparation", "MoveFileExW available, fsync available",
                "Atomic no-overwrite write-through publication via same-filesystem .partial and MoveFileExW flag 8",
                "Current read-only git HEAD/branch/remote/status", "Source mutation probe not performed"],
            "json_selftest": "Actual complete invocation object dict/list/scalars roundtrip checked before publication",
            "limits": "Procedural read-only, not sandbox enforced; ACL is eligibility, no source-write probe; same-principal tampering cannot be excluded"},
        "recovery": {"predecessor_attempt": "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff",
            "safe_boundary": "Current explicit Human start after terminal Investigation; no application authorized",
            "liveness": "Current roster sole running Commit Record Clarification Decision matches own runtime ID 0939dcbe-f104-454a-a8bd-62e36810ccd3. Other actors idle. Historical unterminated metadata is not evidence of liveness; no conflicting current writer observed.",
            "limitations": "No exhaustive event log; endpoint baselines do not exclude transient writes"},
        "inputs": inputs, "baseline": baseline,
        "task_context": "N/A governance-only; product Requirement and approved Implementation Plan not applicable",
        "ordering": "Preflight only so far; substantive finding comparison starts only after separate process readback of this record"
    })
    print(json.dumps(publish("attempt.json", record), indent=2))

if __name__ == "__main__":
    preflight()
