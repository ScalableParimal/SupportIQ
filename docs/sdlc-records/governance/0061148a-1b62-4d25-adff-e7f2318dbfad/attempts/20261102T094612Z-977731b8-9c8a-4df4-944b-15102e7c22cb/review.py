"""Reviewer-owned publication/check utility. Never executes upstream scripts."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[6]
OWN = Path(__file__).resolve().parent
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = OWN.name
ROLE = "Independent Governance Review"
BASE = OWN.parent
VER = BASE / "20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1"
APP = BASE / "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd"
PROP = BASE / "20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed"
NAMES = ["review.py", "attempt.json", "evidence/qualification.json",
         "checkpoint-0001.json", "checkpoint-0002.json", "checkpoint-0003.json",
         "evidence/review-evidence.json", "evidence/final-readback.json",
         "report.md", "result.json"]
ALLOWED = {OWN / n for n in NAMES}
EXCLUDED = ALLOWED | {Path(str(p) + ".partial") for p in ALLOWED}
DIR_EXCLUDED = {OWN, OWN / "evidence"}
EVENTS = []
LIMITS = ("PROCEDURAL NON-MUTATION, not enforced read-only or a sandbox. "
          "Shared write-capable OS principal and tools. Actor-visible tool transcript "
          "and instrumented checks/publications only; no exhaustive trusted OS event "
          "stream, continuous observation, lock or coordinated no-edit window. "
          "Matching endpoint fingerprints cannot prove absence of transient writes "
          "or same-principal tampering. Parent message platform IDs/times are not "
          "authenticated/exposed; none invented. Host clock samples describe preparation "
          "or operation observations, not exact filesystem publication times.")
START = ("Yes, initiate Independent Governance Review for the "
         "GOV-AUD-20261102-001 clarification and its passing Verification only")

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def rel(p):
    return Path(p).resolve().relative_to(ROOT).as_posix()

def event(op, args, outcome):
    EVENTS.append(dict(sequence=len(EVENTS)+1, actor=ATTEMPT, operation=op,
                       arguments=args, completion_observed_utc=now(), outcome=outcome))

def binding(p):
    p = Path(p)
    if not p.is_absolute():
        p = ROOT / p
    b = p.read_bytes()
    return dict(path=rel(p), bytes=len(b), sha256=sha(b))

def pairs(xs):
    d = {}
    for k, v in xs:
        if k in d:
            raise ValueError("duplicate key")
        d[k] = v
    return d

def parse(b):
    return json.loads(b, object_pairs_hook=pairs,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))

def native(x):
    if x is None or type(x) in (str, bool, int):
        return
    if type(x) is float:
        import math
        assert math.isfinite(x)
        return
    if type(x) is list:
        for v in x:
            native(v)
        return
    if type(x) is dict:
        assert all(type(k) is str for k in x)
        for v in x.values():
            native(v)
        return
    raise TypeError("not a JSON-native object: " + type(x).__name__)

def encode(x):
    native(x)
    b = (json.dumps(x, ensure_ascii=True, indent=2, allow_nan=False) + "\n").encode()
    assert parse(b) == x
    return b

def selftests():
    sample = {"complete": [None, True, 17, 1.25, {"unicode": "\u00a7 ?"}]}
    assert parse(encode(sample)) == sample
    for x in [("tuple",), {"tuple": (1, 2)}, float("nan")]:
        try:
            encode(x)
        except (TypeError, ValueError, AssertionError):
            pass
        else:
            raise AssertionError("serializer accepted non-native input")
    for b in [b'{"x":1,"x":2}', b'{"x":NaN}']:
        try:
            parse(b)
        except ValueError:
            pass
        else:
            raise AssertionError("strict parse failed")
    return dict(complete_native_roundtrip=True, tuple_rejected=True,
                duplicate_keys_rejected=True, nonfinite_rejected=True,
                full_object_before_every_publication=True)

def command(args):
    c = subprocess.run(args, cwd=ROOT, capture_output=True)
    event("nonmutating subprocess", args, dict(exit_code=c.returncode,
          stdout_sha256=sha(c.stdout), stderr_sha256=sha(c.stderr)))
    assert c.returncode == 0, c.stderr.decode(errors="replace")
    return c.stdout.decode("utf-8", errors="strict").strip()

def snapshot():
    files, dirs = [], []
    for current, ds, fs in os.walk(ROOT):
        ds[:] = sorted(d for d in ds if d != ".git")
        cp = Path(current)
        if cp != ROOT and cp not in DIR_EXCLUDED:
            dirs.append(rel(cp))
        for f in sorted(fs):
            p = cp / f
            if p not in EXCLUDED:
                files.append(binding(p))
    tracked = command(["git", "--no-pager", "ls-files", "--stage"])
    status = command(["git", "--no-pager", "status", "--porcelain=v1", "--untracked-files=all"])
    excluded_rel = {rel(p) for p in EXCLUDED}
    lines = [s for s in status.splitlines()
             if s[3:].replace("\\", "/").strip('"') not in excluded_rel]
    result = dict(files=sorted(files, key=lambda x:x["path"]),
                  directories=sorted(dirs), index=tracked, status=lines,
                  HEAD=command(["git", "--no-pager", "rev-parse", "HEAD"]),
                  branch=command(["git", "--no-pager", "branch", "--show-current"]),
                  origin=command(["git", "--no-pager", "remote", "get-url", "origin"]))
    event("complete non-.git snapshot", dict(files=len(files),
          exact_exclusions=sorted(excluded_rel)), "read/hash/path/index/status complete")
    return result

def record(kind, **kwargs):
    return dict(schema_version="1.0", record_type=kind,
                record_id=ATTEMPT+":"+kind, work_id=WORK, attempt_id=ATTEMPT,
                creator=ATTEMPT, role=ROLE, process=ROLE,
                cycle_id="GOV-REMEDIATION-PROSPECTIVE-001", cycle_number=1,
                finding_id="GOV-AUD-20261102-001", created_at_utc=now(),
                clock_basis="Host UTC record-preparation sample, not publication time",
                **kwargs)

def publish(name, obj):
    p = OWN / name
    assert p in ALLOWED and p.name != "review.py"
    assert os.name == "nt", "Windows rename no-replace semantics required"
    b = obj.encode("utf-8") if type(obj) is str else encode(obj)
    partial = Path(str(p) + ".partial")
    assert not p.exists() and not partial.exists()
    p.parent.mkdir(parents=True, exist_ok=True)
    with partial.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == b
    if type(obj) is not str:
        assert parse(partial.read_bytes()) == obj
    os.rename(partial, p)
    assert p.read_bytes() == b
    event("validated fsync atomic no-overwrite rename and readback",
          dict(final=rel(p), partial=rel(partial), bytes=len(b), sha256=sha(b)), "PASS")
    return binding(p)

def load(p):
    p = Path(p)
    b = p.read_bytes()
    d = parse(b)
    event("strict JSON read", binding(p), "PASS")
    return d

def unchanged():
    q = load(OWN / "evidence/qualification.json")
    s = snapshot()
    assert s == q["baseline"], "Evaluated inputs/path set/index/state changed"
    return dict(outcome="PASS", input_count=len(s["files"]),
                snapshot_sha256=sha(encode(s)), baseline=binding(OWN/"evidence/qualification.json"),
                comparisons="files/bytes/hashes/directories/HEAD/branch/origin/index/status identical",
                expected_absences=q["expected_absences"],
                limits=LIMITS)

def qualify():
    tests = selftests()
    v = load(VER/"result.json")
    assert v["outcome"] == "PASS" and v["execution_status"] == "COMPLETED"
    assert v["unresolved_verification_findings"] == []
    for role, data in v["actor_identity"]["approved_four_role_bindings"].items():
        assert binding(data["definition"]["path"]) == data["definition"], role
    assert len({v["actor_identity"]["approved_four_role_bindings"][r]["definition"]["path"]
                for r in ["preparer", "publisher", "verifier", "reviewer"]}) == 4
    baseline = snapshot()
    expected = [rel(OWN/n) for n in NAMES if n != "review.py"]
    assert all(not (ROOT / p).exists() for p in expected)
    assert baseline["HEAD"] == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    acl = command(["powershell", "-NoProfile", "-Command",
                   "Get-Acl ., .github, docs/ai/sdlc, docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts | Format-List Path,Owner,AccessToString"])
    principal = command(["whoami", "/user"])
    own_identity = dict(role=ROLE, invocation=ATTEMPT,
        runtime_identity_source="Current separately invoked Independent Governance Review agent; no platform session ID exposed",
        definition=binding(".github/agents/independent-governance-review.agent.md"),
        OS_principal=principal, qualification_pid=os.getpid(),
        distinct_from=["Corrective Change Decision preparer", "Governance Amendment Application applier",
                       "Independent Governance Verification verifier", "active Remediation", "Orchestrator"],
        predecessor_actor_bindings=v["actor_identity"]["approved_four_role_bindings"],
        limits="Distinct process role/invocation; not technical isolation from shared OS principal")
    events_before = [
        "Read mandatory Review Skill, Agent, Guideline, Prompt, Request",
        "Located Masters and bounded canonical inputs; read complete Verification report and result eligibility",
        "Read governing sections 3, 33.1 and 30.1; inspected current token/ACL/status",
        "Read-only UnicodeEncodeError in cp1252 output corrected with UTF-8 stdout; no publication occurred",
        "Large combined read output narrowed by ranged/targeted reads; V12 extraction was too broad, then narrowed to locator",
        "github issue_read get_comments ScalableParimal/SupportIQ issue 3 perPage 100 returned OWNER decision id 6522916236",
        "Allocated fresh attempt id; apply_patch created only reviewer-owned review.py publication/check utility",
        "This qualify process: strict PASS gate/role hashes/native serializer/capability/snapshot/ACL checks before invocation"]
    scope = dict(repository="ScalableParimal/SupportIQ", root=str(ROOT),
        output_scope=rel(OWN), authorized_stage=ROLE,
        substantive_subject="Only exact approved GOV-AUD-20261102-001 linked clarification Application and PASS Verification",
        excluded="source edits/fixes/approval/application/replacement Verification/full Audit/effectivity/adoption/product/commit/push",
        task_context="Governance-only; no product Plan or task is applicable")
    q = record("qualification", actor=own_identity, scope=scope, baseline=baseline,
        expected_absences=expected, own_exact_output_exclusions=sorted(rel(p) for p in EXCLUDED),
        directory_exclusions=sorted(rel(p) for p in DIR_EXCLUDED),
        controller=binding(OWN/"review.py"), current_permissions=acl,
        capabilities=dict(read_hash=True, strict_JSON=True, native_selftests=tests,
                          snapshot_path_index_status=True,
                          publication="Runtime write-capable; authorized only own exact outputs; actual no-overwrite publication below"),
        root_decision=dict(url="https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                           author="ScalableParimal", author_association="OWNER",
                           decision_id=6522916236, created_at="2026-10-30T12:31:51Z",
                           updated_at="2026-10-30T12:31:51Z",
                           current_read="github issue_read returned original unedited root adoption; not this Review start",
                           scope="governance root adopted; original Audit-only start not reused"),
        fresh_human_stage_start=dict(actual_wording=START,
            source="Actual Human instruction in current user request after completed PASS Verification",
            platform_message_id=None, authenticated_time=None, not_approval=True),
        ordered_prequalification_operations=events_before,
        operations=EVENTS.copy(), limitations=LIMITS)
    qb = publish("evidence/qualification.json", q)
    inv = record("invocation", actor=own_identity, scope=scope,
        repository_context={k:baseline[k] for k in ["HEAD","branch","origin"]},
        authorization=q["fresh_human_stage_start"], root_decision=q["root_decision"],
        qualification=qb, input_manifest=qb,
        predecessor_report=binding(VER/"report.md"), predecessor_result=binding(VER/"result.json"),
        predecessor_evidence=binding(VER/"evidence/verification-evidence.json"),
        application_report=binding(APP/"report.md"), application_result=binding(APP/"result.json"),
        proposal=binding(PROP/"report.md"),
        approval_request=binding(PROP/"attachments/exact-recovery-approval-request.json"),
        execution_status="QUALIFIED; awaiting separate-process invocation readback before substantive Review",
        outputs=[rel(OWN/n) for n in NAMES], operations=EVENTS.copy(), limitations=LIMITS)
    ib = publish("attempt.json", inv)
    print(json.dumps(dict(qualification=qb, invocation=ib, next="fresh process readback"), indent=2))

def readback():
    inv = load(OWN/"attempt.json")
    q = load(OWN/"evidence/qualification.json")
    assert inv["qualification"] == binding(OWN/"evidence/qualification.json")
    assert inv["actor"]["invocation"] == ATTEMPT
    assert q["controller"] == binding(OWN/"review.py")
    state = unchanged()
    b = publish("checkpoint-0001.json", record("checkpoint", sequence=1,
        last_confirmed_boundary="Separate-process qualification/invocation readback before substantive comparison",
        input_comparison=state, invocation=binding(OWN/"attempt.json"),
        partial_effects="Own qualification/invocation/controller only; no input changes observed",
        unfinished="Substantive Review then final readback/result", blockers=[],
        safe_continuation="Only scoped Independent Governance Review", operations=EVENTS.copy()))
    print(json.dumps(b, indent=2))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    os.chdir(ROOT)
    assert sys.argv[1] in ["qualify", "readback", "check"]
    if sys.argv[1] == "qualify":
        qualify()
    elif sys.argv[1] == "readback":
        readback()
    else:
        print(json.dumps(unchanged(), indent=2))
