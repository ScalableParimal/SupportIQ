import ctypes
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[7]
os.chdir(ROOT)
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff"
BASE = Path("docs/sdlc-records/governance") / WORK / "attempts"
OWN = BASE / ATTEMPT
COORD = BASE / "20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565"
AUDIT = BASE / "20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def ref(path, identity=None):
    p = Path(path)
    b = p.read_bytes()
    d = {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest().upper()}
    if identity:
        d["identity"] = identity
    return d

def load(p):
    return json.loads(Path(p).read_bytes())

def checked_json(obj):
    raw = (json.dumps(obj, ensure_ascii=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    assert json.loads(raw) == obj, "complete native-object serialization mismatch"
    assert b"`n" not in raw
    return raw

def publish(p, obj, markdown=False):
    p = Path(p)
    assert p.is_relative_to(OWN), "outside own scope"
    assert not p.exists(), "final already exists"
    raw = obj.encode("utf-8") if markdown else checked_json(obj)
    assert b"`n" not in raw and b"\xef\xbf\xbd" not in raw
    p.parent.mkdir(parents=True, exist_ok=True)
    partial = p.with_name(p.name + ".partial")
    with partial.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == raw
    if not markdown:
        assert load(partial) == obj
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    move = kernel.MoveFileExW
    move.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
    move.restype = ctypes.c_int
    if not move(str(partial.resolve()), str(p.resolve()), 8):
        raise ctypes.WinError(ctypes.get_last_error())
    assert p.read_bytes() == raw
    return ref(p)

def cmd(*args):
    return subprocess.check_output(args, text=True, encoding="utf-8").strip()

def sources():
    return sorted([p for root in [Path(".github"), Path("docs/ai")] for p in root.rglob("*") if p.is_file()])

def prior():
    return sorted(p for p in Path("docs/sdlc-records").rglob("*") if p.is_file() and not p.is_relative_to(OWN))

def bindings(obj, location="$"):
    found = []
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            actual = ref(obj["path"])
            assert actual["sha256"].lower() == obj["sha256"].lower(), (location, obj["path"])
            if "bytes" in obj:
                assert actual["bytes"] == obj["bytes"], (location, "bytes")
            found.append({"location": location, "binding": actual})
        for k, v in obj.items():
            found += bindings(v, location + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += bindings(v, location + "[" + str(i) + "]")
    return found

def common(kind):
    return {"schema_version": "1.0", "record_type": kind, "record_id": ATTEMPT + ":" + kind,
            "work_id": WORK, "attempt_id": ATTEMPT, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
            "cycle": 1, "creator": {"role": "Finding Investigation",
            "actor_identity": "local-finding-investigation:" + ATTEMPT,
            "runtime_label": "Commit Record Ambiguity Investigation",
            "runtime_agent_id_observed": "b7ff5557-b3f4-44b4-87e4-7c6f5cdfc705",
            "identity_limit": "Runtime roster association, not independently authenticated platform principal"},
            "created_at_utc": now(), "clock_basis": "Host UTC sample during record preparation; not publication time",
            "process": "Finding Investigation", "subject_type": "FINDING", "finding_id": "GOV-AUD-20261102-002"}

def prepare():
    assert ROOT == Path("C:/PARIMAL_SHERE/SCALABLE_SOLUTIONS/SupportIQ")
    assert not (OWN / "attempt.json").exists()
    assert cmd("git", "rev-parse", "HEAD") == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert os.access(BASE, os.R_OK | os.W_OK | os.X_OK)
    assert hasattr(os, "fsync") and ctypes.windll.kernel32.MoveFileExW
    a = load(COORD / "attempt.json")
    assert a["work_id"] == WORK
    assert not (Path("docs/sdlc-records/product") / WORK).exists()
    reservation = BASE / "20261030T123604Z-15be0f40-a028-4166-bb27-fbf5fdefecc4/attempt.json"
    reserved = load(reservation)
    assert WORK in json.dumps(reserved)
    inputs = []
    expected = [
        (COORD / "report.md", 19130, "0E819BDD31747BA24037C89130D1A25A8E642A7EB0BBF9DF267C34DBD815C768"),
        (COORD / "result.json", 7103, "F65D96FC76105E4546CC5318BF7D3E4A8E41784486449BE3CE55726840CE2AD2"),
        (COORD / "attachments/investigation-handoff.md", 7361, "59436AEE6D74EC483B89B62F190D6330B85241CB3359D126EFED31EEC43627B3"),
        (AUDIT / "report.md", 55902, "4246B0BAA6A945678034706AE02E26162CD2DB940D8FAC3F2AB7749D76B477A2"),
        (AUDIT / "result.json", 27489, "3C628AA7BC8ECDF2194EC5FBA13911BB183B45A0BBA4CD57E81CF4B4FBF23231"),
        (AUDIT / "evidence/audit-evidence.json", 4819789, "888ABF5B0E14829F0EC2FF824510DB1E3B8DB3CC1636F29B3DD6E44DF5104AF2")]
    for p, size, sha in expected:
        r = ref(p)
        assert r["bytes"] == size and r["sha256"] == sha
        inputs.append(r)
    current_sources = [ref(p) for p in sources()]
    current_prior = [ref(p) for p in prior()]
    # Hash-only pre-execution reconciliation, not affected-source comparison.
    historical_binding_checks = bindings(a["baseline"])
    result_binding_checks = bindings(load(COORD / "result.json")) + bindings(load(AUDIT / "result.json"))
    d = common("invocation")
    d.update({"repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
        "head": cmd("git", "rev-parse", "HEAD"), "branch": cmd("git", "branch", "--show-current"),
        "remote": cmd("git", "remote", "get-url", "origin"), "status": cmd("git", "status", "--porcelain=v1")},
        "authorization": {"actual_human_start": "Yes, initiate Finding Investigation for GOV-AUD-20261102-002 only under the existing Work ID and Cycle 1 using the validated handoff from attempt 20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565; no correction or other stage",
        "source": "Actual Human instruction relayed in current parent conversation",
        "authenticated_message_id": None, "authenticated_human_time": None,
        "scope": "Focused read-only governance finding investigation, own new actor records only",
        "non_goals": ["correction", "exact patch or application approval", "Corrective Change Decision",
        "other stage", "commit", "push", "adoption", "product work", "broad re-audit"]},
        "persistence": {"root": "docs/sdlc-records/governance/", "own_scope": OWN.as_posix(),
        "existing_reservation": ref(reservation), "collision_check": "Existing same-work reservation retained; no matching product-root directory",
        "root_decision": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
        "author": "ScalableParimal", "author_association": "OWNER", "created_at": "2026-10-30T12:31:51Z",
        "updated_at": "2026-10-30T12:31:51Z", "live_resolved_current_invocation": True,
        "scope": "Governance-root adoption only; initial Audit start not reused as current start"},
        "masters": [ref(p) for p in Path("docs/ai/sdlc").glob("SDLC_*.md")],
        "master_status": "Bootstrap comparison authority; target Master baseline and product root not adopted"},
        "qualification": {"effective_identity": cmd("whoami", "/user"),
        "acl_observed": "Current Get-Acl: authenticated Users Modify; Administrators and SYSTEM FullControl",
        "read_access": True, "own_parent_write_eligibility": True, "source_write_probe": False,
        "capability": "Current Python can read/hash/parse sources and JSON; Windows MoveFileExW available, os.fsync available; no-overwrite write-through publication route",
        "serializer_selftest": "Complete actual invocation object JSON roundtrip equality required before publication",
        "limitations": "Procedural nonmutation, not sandbox enforced; shared writable principal"},
        "recovery": {"predecessor": ref(COORD / "result.json"),
        "safe_boundary": "Coordinator completed; new Finding Investigation not previously started for this finding",
        "known_stale_unterminated_attempts": a["recovery"]["stale_unterminated_attempts"],
        "reconciliation": "Retain historical attempts; coordinator validated no corrective payload on failed Application. Native roster shows this investigation as the sole running finding actor; matching own runtime agent ID is not a competing writer; idle actors/stale starts do not establish live writers. No conflicting current write observed; no exhaustive event log.",
        "same_work_historical_baseline_checks": len(historical_binding_checks),
        "upstream_result_binding_checks": len(result_binding_checks)},
        "inputs": inputs, "baseline": {"sources": current_sources, "prior_records": current_prior},
        "helper": ref(Path(__file__).relative_to(ROOT)),
        "designated_outputs": ["attempt.json", "checkpoint-0001.json", "report.md", "result.json",
        "attachments/investigation.py", "attachments/evidence.json", "checkpoint-0002.json"],
        "ordering": "Invocation publication, then independent separate-operation readback, then substantive affected-source analysis"})
    assert checked_json(d)
    print(json.dumps({"published": publish(OWN / "attempt.json", d), "sources": len(current_sources),
                      "prior_records": len(current_prior), "bound_input_checks": len(result_binding_checks)}, indent=2))

def readback():
    d = load(OWN / "attempt.json")
    assert d["attempt_id"] == ATTEMPT and d["work_id"] == WORK
    checks = bindings(d)
    assert set(r["path"] for r in d["baseline"]["sources"]) == set(p.as_posix() for p in sources())
    assert set(r["path"] for r in d["baseline"]["prior_records"]) == set(p.as_posix() for p in prior())
    cp = common("checkpoint")
    cp.update({"sequence": 1, "boundary": "Fresh separate-operation invocation readback passed before substantive source comparison",
        "invocation": ref(OWN / "attempt.json", ATTEMPT + ":invocation"), "binding_checks": len(checks),
        "partial_effects": "Own helper and invocation only; no source/upstream changes",
        "unfinished": "Substantive focused investigation and terminal report",
        "blockers": [], "next": "Read actual affected wording and relevant authority/prior art only"})
    print(json.dumps(publish(OWN / "checkpoint-0001.json", cp), indent=2))

if __name__ == "__main__":
    {"prepare": prepare, "readback": readback}[sys.argv[1]]()
