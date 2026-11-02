import os
import sys
import json
import hashlib
import pathlib
import subprocess
import datetime

ROOT = pathlib.Path(__file__).resolve().parents[6]
OWN = pathlib.Path(__file__).resolve().parent
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = OWN.name
PREFIX = OWN.relative_to(ROOT).as_posix()
OUTPUTS = [
    "verification.py", "attempt.json", "checkpoint-0001.json",
    "checkpoint-0002.json", "report.md", "result.json",
    "evidence/qualification.json", "evidence/verification-evidence.json",
    "evidence/final-readback.json",
]
EXCLUDED = {PREFIX + "/" + n for n in OUTPUTS}
EXCLUDED.update({p + ".partial" for p in list(EXCLUDED)})
OWN_DIRS = {PREFIX, PREFIX + "/evidence"}
START = "Yes, initiate Independent Governance Verification for the GOV-AUD-20261102-001 clarification Application only"
LIMITS = (
    "Procedural non-mutation; shared write-capable OS principal and tools, not "
    "enforced read-only. Actor-visible tool transcript and script events only; "
    "no exhaustive trusted OS event stream, lock, coordinated no-edit window, "
    "or continuous observation. Matching endpoint fingerprints cannot prove "
    "absence of transient writes or same-principal tampering. Terminal old "
    "attempts are not evidence of live competing writers. No authenticated "
    "parent message IDs/times are exposed; none invented."
)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def rel(p):
    return pathlib.Path(p).relative_to(ROOT).as_posix()

def fp(p):
    p = pathlib.Path(p)
    if not p.is_absolute():
        p = ROOT / p
    b = p.read_bytes()
    return {"path": rel(p), "bytes": len(b), "sha256": sha(b)}

def pairs(items):
    d = {}
    for k, v in items:
        if k in d:
            raise ValueError("duplicate JSON key: " + k)
        d[k] = v
    return d

def strict(b):
    return json.loads(b, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def native(v):
    if v is None or type(v) in (str, bool, int):
        return
    if type(v) is list:
        for x in v:
            native(x)
        return
    if type(v) is dict:
        assert all(type(k) is str for k in v)
        for x in v.values():
            native(x)
        return
    raise TypeError("Non JSON-native type " + str(type(v)))

def encode(v):
    native(v)
    b = (json.dumps(v, ensure_ascii=True, indent=2, allow_nan=False) + "\n").encode("ascii")
    assert strict(b) == v
    return b

def selftest():
    actual = {"nested": [{"unicode": "\u003f\u00a7\u2019", "null": None,
                         "boolean": True, "integer": 3438}], "empty": []}
    assert strict(encode(actual)) == actual
    for bad in [b'{"x":1,"x":2}', b'{"x":NaN}']:
        try:
            strict(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("strict rejection failed")
    try:
        encode({"tuple": (1, 2)})
    except TypeError:
        pass
    else:
        raise AssertionError("tuple self-test failed")
    return {"complete_actual_objects": "strict native equality before every publication",
            "duplicate_keys": "rejected", "NaN": "rejected",
            "non_native_tuple": "rejected", "Unicode_roundtrip": "PASS"}

def command(args):
    return subprocess.check_output(args, cwd=ROOT, stderr=subprocess.STDOUT).decode("utf-8").strip()

def state():
    raw = subprocess.check_output(
        ["git", "--no-pager", "status", "--porcelain=v1", "--untracked-files=all", "-z"],
        cwd=ROOT)
    fields = raw.decode("utf-8").split("\0")
    external = []
    i = 0
    while i < len(fields):
        f = fields[i]
        i += 1
        if not f:
            continue
        path = f[3:].replace("\\", "/")
        entry = {"status": f[:2], "path": path}
        if "R" in f[:2] or "C" in f[:2]:
            entry["original_path"] = fields[i]
            i += 1
        if path not in EXCLUDED:
            external.append(entry)
    index = ROOT / ".git/index"
    return {"head": command(["git", "rev-parse", "HEAD"]),
            "branch": command(["git", "branch", "--show-current"]),
            "origin": command(["git", "remote", "get-url", "origin"]),
            "index_sha256": sha(index.read_bytes()) if index.exists() else None,
            "external_status": external,
            "raw_status_sha256": sha(raw)}

def snapshot():
    files = []
    dirs = []
    for base, ds, names in os.walk(ROOT):
        if pathlib.Path(base) == ROOT:
            ds[:] = [d for d in ds if d != ".git"]
        for d in ds:
            p = pathlib.Path(base) / d
            assert not p.is_symlink(), "symlink directory: " + str(p)
            rp = rel(p)
            if rp not in OWN_DIRS:
                dirs.append(rp)
        for n in names:
            p = pathlib.Path(base) / n
            rp = rel(p)
            assert not p.is_symlink(), "symlink file: " + str(p)
            if rp not in EXCLUDED:
                files.append(fp(p))
    return {"files": sorted(files, key=lambda x: x["path"]),
            "directories": sorted(dirs), "repository": state(),
            "exact_exclusions": sorted(EXCLUDED),
            "excluded_own_directories": sorted(OWN_DIRS)}

def comparable(s):
    r = dict(s["repository"])
    r.pop("raw_status_sha256")
    return {"files": s["files"], "directories": s["directories"], "repository": r}

def publish(name, obj=None, data=None):
    dest = OWN / name
    assert name in OUTPUTS, "undeclared output"
    assert not os.path.lexists(dest), "no-overwrite collision"
    part = dest.with_name(dest.name + ".partial")
    assert not os.path.lexists(part), "partial collision"
    b = encode(obj) if obj is not None else data
    assert isinstance(b, bytes)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with part.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert part.read_bytes() == b
    if obj is not None:
        assert strict(part.read_bytes()) == obj
    os.rename(part, dest)  # Windows atomic rename fails when destination exists.
    assert dest.read_bytes() == b
    if obj is not None:
        assert strict(dest.read_bytes()) == obj
    return fp(dest)

def load(name):
    return strict((OWN / name).read_bytes())

def initial():
    assert ROOT == pathlib.Path.cwd().resolve()
    assert os.environ.get("COPILOT_AGENT_SESSION_ID") == "923a55cc-499e-4d83-8923-11f097bbcb71"
    test = selftest()
    s = snapshot()
    governing = [
        ".github/agents/independent-governance-verification.agent.md",
        ".github/skills/independent-governance-verification/SKILL.md",
        "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md",
        "docs/ai/prompts/INDEPENDENT_GOVERNANCE_VERIFICATION_PROMPT.md",
        "docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md",
        "docs/ai/sdlc/SDLC_GOVERNANCE.md",
        "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
        "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md",
    ]
    base = ROOT / "docs/sdlc-records/governance" / WORK / "attempts"
    app = base / "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd"
    package = base / "20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed"
    request = strict((package / "attachments/exact-recovery-approval-request.json").read_bytes())
    roles = request["scope"]["roles"]
    assert fp(ROOT / roles["verifier"]["definition"]["path"]) == roles["verifier"]["definition"]
    assert len({v["definition"]["path"] for v in roles.values()}) == 4
    predecessor = fp(app / "result.json")
    assert predecessor["sha256"] == "8F9AEF423A96167C8A6247266F26989A22AB331FB033D7280AB8C46127359CD9"
    appresult = strict((app / "result.json").read_bytes())
    token = command(["whoami", "/user"])
    permissions = command(["powershell", "-NoProfile", "-Command",
        "Get-Acl -LiteralPath '" + str(OWN.parent) + "' | Format-List Owner,AccessToString"])
    qualification = {
        "schema_version": "1.0", "record_type": "qualification",
        "work_id": WORK, "attempt_id": ATTEMPT, "created_at_utc": now(),
        "evaluated_input_set": "All repository non-.git files and path sets, not HEAD-only; exact own output exclusions only",
        "snapshot_before_substantive_checks": s,
        "permissions": permissions, "effective_token": token,
        "capabilities_observed": {
            "read": "Current role, skill, guideline, prompt, request, Masters publication clauses and predecessor qualification records read",
            "SHA256": fp(app / "result.json"),
            "nonmutating_checks": "Python byte/hash/path enumeration and strict JSON parse; git read-only state commands",
            "publication": "Own scoped create-new partial/flush/fsync/atomic no-overwrite Windows rename/readback route; actual first publication below",
        },
        "operation_evidence": [
            {"sequence": 1, "tool": "functions.powershell", "operation": "Read skill, discover/read role and stage contract", "outcome": "PASS; large output retrieved by view"},
            {"sequence": 2, "tool": "functions.powershell", "operation": "whoami, Get-Command, Get-Acl, selected runtime environment, UTC", "outcome": "PASS except Get-Date -AsUTC unsupported; replaced with DateTime.UtcNow, no publication or input mutation"},
            {"sequence": 3, "tool": "functions.rg/functions.view", "operation": "Locate/read Master publication and handoff clauses; completed Application report", "outcome": "qualification only; no substantive comparison"},
            {"sequence": 4, "tool": "functions.powershell", "operation": "Resolve actor/authority bindings and generate UUID attempt; large output narrowed", "outcome": "PASS; no input writes"},
            {"sequence": 5, "tool": "functions.apply_patch", "operation": "Create only this verifier-owned script at exact fresh scope", "outcome": "PASS"},
            {"sequence": 6, "tool": "verification.py initial", "operation": "Snapshot all non-.git input files/path sets/status/index; identity, permissions and selftests; publish qualification then invocation", "start_utc": now(), "outcome": "Pending subsequent fresh-process readback"}
        ],
        "concurrency": "No coordinated no-edit interval or repository lock; terminal prior attempts not presumed live writers; external changes detected by full bounded snapshots",
        "limitations": LIMITS, "serializer_self_tests": test,
    }
    qfp = publish("evidence/qualification.json", qualification)
    invocation = {
        "schema_version": "1.0", "record_type": "invocation",
        "record_id": ATTEMPT + ":invocation", "work_id": WORK,
        "attempt_id": ATTEMPT, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
        "cycle_number": 1, "finding_id": "GOV-AUD-20261102-001",
        "process": "Independent Governance Verification",
        "actor_identity": {
            "role": "Independent Governance Verification",
            "definition": fp(ROOT / ".github/agents/independent-governance-verification.agent.md"),
            "runtime_session": os.environ.get("COPILOT_AGENT_SESSION_ID"),
            "runtime_agent": os.environ.get("AI_AGENT"),
            "invocation_identity": ATTEMPT, "OS_token": token, "pid_at_qualification": os.getpid(),
            "independence": "Distinct current verifier definition/invocation; not preparer, publisher or planned reviewer. Shared OS principal not claimed isolated.",
            "approved_four_role_bindings": roles,
        },
        "created_at_utc": now(), "clock_basis": "Current runtime UTC samples; no parent message timestamps inferred",
        "repository": s["repository"], "governing": [fp(ROOT / p) for p in governing],
        "human_stage_start": {
            "wording": START, "source": "Actual Human current conversation user instruction, supplied 2026-11-02; message ID/time not authenticated or exposed",
            "scope": "Completed GOV-AUD-20261102-001 linked clarification Application only",
            "not_substantive_approval": True,
        },
        "predecessor_complete_result": predecessor,
        "predecessor_report": fp(app / "report.md"),
        "approval_package": fp(package / "report.md"),
        "approval_request": fp(package / "attachments/exact-recovery-approval-request.json"),
        "publication_scope": PREFIX, "permitted_exact_outputs": OUTPUTS,
        "expected_absences": [PREFIX + "/" + n for n in OUTPUTS if n != "verification.py"],
        "qualification": qfp,
        "nonmutation": "No source, evaluated input, upstream record or historical write. Publication only owned records.",
        "limitations": LIMITS,
        "status": "QUALIFIED_PENDING_FRESH_PROCESS_INVOCATION_READBACK",
        "selftests": test,
    }
    print(json.dumps({"qualification": qfp, "invocation": publish("attempt.json", invocation),
                      "input_files": len(s["files"]), "predecessor_status_fields": {k:v for k,v in appresult.items() if k in ("status","outcome","completion")}}, indent=2))

def evaluate():
    import re
    selftest()
    inv = load("attempt.json")
    qualification = load("evidence/qualification.json")
    assert fp(OWN / "evidence/qualification.json") == inv["qualification"]
    assert load("checkpoint-0001.json")["invocation"] == fp(OWN / "attempt.json")
    baseline = qualification["snapshot_before_substantive_checks"]
    current = snapshot()
    assert comparable(baseline) == comparable(current), "evaluated-input drift"
    base = ROOT / "docs/sdlc-records/governance" / WORK / "attempts"
    app = base / "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd"
    package = base / "20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed"
    old = base / "20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31"
    affected = base / "20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0"
    audit = base / "20261102T082552Z-6dfe39f3-18aa-40b8-88be-56850b13b291"
    appresult = strict((app / "result.json").read_bytes())
    appinv = strict((app / "attempt.json").read_bytes())
    appev = strict((app / "evidence/application-evidence.json").read_bytes())
    preflight = strict((app / "evidence/preflight-evidence.json").read_bytes())
    request = strict((package / "attachments/exact-recovery-approval-request.json").read_bytes())
    scope = request["scope"]
    packagebody = (package / "report.md").read_text(encoding="utf-8")
    appbody = (app / "report.md").read_text(encoding="utf-8")
    criteria = []

    def check(cid, title, condition, evidence):
        assert condition, cid + ": " + title
        criteria.append({"criterion": cid, "title": title, "outcome": "PASS", "evidence": evidence})

    check("V01", "Current independent verifier identity, capability and first publication",
          inv["actor_identity"]["definition"] == scope["roles"]["verifier"]["definition"]
          and inv["actor_identity"]["invocation_identity"] not in (app.name, package.name)
          and len({v["definition"]["path"] for v in scope["roles"].values()}) == 4,
          {"invocation": fp(OWN / "attempt.json"),
           "qualification": inv["qualification"],
           "record_first_readback": fp(OWN / "checkpoint-0001.json"),
           "roles": scope["roles"],
           "OS_boundary": "Shared principal explicitly disclosed, process actors distinct; future reviewer still planned only"})
    check("V02", "Fresh actual Human Verification initiation after complete Application",
          inv["human_stage_start"]["wording"] == START
          and appresult["execution_status"] == "COMPLETED"
          and appresult["substantive_application_completed"] is True
          and appresult["substantive_application_started"] is True
          and appresult["outcome"] == "APPLIED EXACT APPROVED BYTES",
          {"stage_start": inv["human_stage_start"], "predecessor": fp(app / "result.json"),
           "scope": "Only completed clarification Application; no previous failed result used as success"})
    human = appresult["actual_approval_and_separate_stage_start"]
    approval = "I explicitly redesignate the proposed one-time publisher and approve the identified recovery package, complete section 4 and all bindings above; do not start Application"
    appstart = "Yes, initiate only this scoped Application retry under the approved recovery package"
    check("V03", "Exact package approval, one-time redesignation and separate Application start",
          human["actual_combined_designation_approval"] == approval
          and human["actual_separate_stage_start"] == appstart
          and human["approved_request_full"] == request
          and human["approved_request_binding"] == fp(package / "attachments/exact-recovery-approval-request.json")
          and appresult["approved_scope_complete"] == scope
          and preflight["approved_scope_complete"] == scope
          and appev["approved_scope_complete"] == scope
          and appinv["authorization"] == human
          and approval in appbody and appstart in appbody
          and human["platform_message_id"] is None and human["decision_time"] is None,
          {"actual_combined_designation_approval": approval, "actual_separate_application_start": appstart,
           "approval_source": "Actual Human current request explicitly supplies these exact decisions and their presentation bindings; Application records retain same wording. Parent message IDs/times not authenticated/exposed.",
           "package": fp(package / "report.md"), "request": fp(package / "attachments/exact-recovery-approval-request.json"),
           "complete_scope": scope, "no_extra_risk_acceptance_gate": True,
           "no_reused_old_authority": True})
    expected_hashes = {
        rel(package / "report.md"): "F96D1A37D0F9CE9C5D423C86B84531D80E7C27D945C52FE559586792491D196F",
        rel(package / "result.json"): "9BAB54540B85A71567FACA3A3EBE1917C99367FC67EE58A9716DA2A637B8084E",
        rel(package / "attachments/exact-recovery-approval-request.json"): "4938CCC6829B21AF4281CFB94D32DCBB4FC1F50D2C1AC16630B4D8C1A2C46097",
        rel(app / "report.md"): "26EEC34BAB50AD8A67FEBDAC262D9A723700807C5BA27FBD932668CE16AB2B88",
        rel(app / "result.json"): "8F9AEF423A96167C8A6247266F26989A22AB331FB033D7280AB8C46127359CD9",
        rel(affected / "report.md"): "CE975EE00E642B93AF50EF8FF0FF418101CE821F2E94121D43E0B260A012BF6B",
        rel(audit / "report-revision-0001.md"): "A1A19F188ADFEED3CA9D9602880FD71F599A1141F0BF6DBF2D538F93AA682EE8",
    }
    fixed = [fp(ROOT / p) for p in expected_hashes]
    check("V04", "All caller-bound canonical input identities and fingerprints",
          all(f["sha256"] == expected_hashes[f["path"]] for f in fixed)
          and fp(app / "report.md")["bytes"] == 6380
          and fp(app / "result.json")["bytes"] == 33474,
          fixed)

    # Validate every actual structured fingerprint, including nested complete
    # request/scope, all preflight bindings, current source manifests and role refs.
    seen = []
    cache = {}
    absent_records = []
    def walk(v, location):
        if isinstance(v, dict):
            p, h, count = v.get("path"), v.get("sha256"), v.get("bytes")
            if isinstance(p, str) and isinstance(h, str) and re.fullmatch(r"[a-fA-F0-9]{64}", h) and type(count) is int:
                rp = p.replace("\\", "/")
                if pathlib.Path(p).is_absolute():
                    rp = rel(pathlib.Path(p))
                if rp not in cache:
                    cache[rp] = fp(ROOT / rp)
                actual = cache[rp]
                assert actual["sha256"] == h.upper() and actual["bytes"] == count, "reference mismatch: " + location + " " + rp
                seen.append({"location": location, "actual": actual, "outcome": "PASS"})
            if isinstance(p, str) and v.get("presence") == "ABSENT":
                absent_records.append({"location": location, "path": p,
                                       "qualification": "Historical base observation, not current absence of the now-applied target"})
            for k, item in v.items():
                walk(item, location + "/" + k)
        elif isinstance(v, list):
            for i, item in enumerate(v):
                walk(item, location + "/" + str(i))
    docs = [
        app / "attempt.json", app / "result.json",
        app / "checkpoint-0001.json", app / "checkpoint-0002.json", app / "checkpoint-0003.json",
        app / "evidence/preflight-evidence.json", app / "evidence/application-evidence.json",
        package / "attempt.json", package / "result.json",
        package / "attachments/exact-recovery-approval-request.json",
        package / "evidence/recovery-decision-evidence.json",
        affected / "result.json", affected / "evidence/investigation-evidence.json",
        old / "result.json", old / "evidence/failure-evidence.json",
    ]
    for p in docs:
        walk(strict(p.read_bytes()), rel(p))
    check("V05", "Complete structured input fingerprint bindings independently recomputed",
          len(seen) > 2010 and all(x["status"] == "PASS" for x in preflight["all_machine_derived_bindings"]),
          {"structured_bindings_checked": len(seen), "unique_fingerprinted_paths": len(cache),
           "source_records": [fp(p) for p in docs], "historical_absence_contexts": absent_records,
           "detail_location": "verification-evidence.json / independently_recomputed_bindings"})
    target = ROOT / scope["one_substantive_target"]
    source = ROOT / scope["payload_source"]["path"]
    payload = target.read_bytes()
    expected = "8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
    check("V06", "Exact target path, immutable source bytes, expected after hash and encoding",
          payload == source.read_bytes() and len(payload) == 3438 and sha(payload) == expected
          and not payload.startswith(b"\xef\xbb\xbf") and max(payload) < 128
          and b"\r" not in payload and payload.endswith(b"\n") and not payload.endswith(b"\n\n")
          and b"`n" not in payload and b"{ev" not in payload
          and appresult["after"] == fp(target)
          and appresult["actual_substantive_path_list"] == [rel(target)]
          and appresult["approved_substantive_path_list"] == [rel(target)],
          {"target": fp(target), "source": fp(source),
           "encoding": "ASCII subset of UTF-8, no BOM, LF only, exactly one final LF; byte equality includes complete headers/body/newlines",
           "path_list": [rel(target)], "no_template_substitution": True})
    historicalbase = appresult["before"]
    check("V07", "ABSENT base, new-attempt/no-overwrite route and complete Application ordering",
          historicalbase == {"path": rel(target), "presence": "ABSENT", "bytes": None, "sha256": None}
          and scope["base_condition"]["presence"] == "ABSENT"
          and scope["base_condition"]["attempt_presence"] == "ABSENT"
          and appinv["actor_identity"]["definition"] == scope["roles"]["publisher"]["definition"]
          and appinv["actor_identity"]["invocation"] == rel(app / "attempt.json")
          and preflight["actual_substantive_paths"] == []
          and appev["actual_substantive_paths"] == [rel(target)]
          and appev["substantive_application_completed"] is True
          and "no-overwrite" in " ".join(appev["tool_outcomes"]),
          {"base": historicalbase, "approval_base": scope["base_condition"],
           "invocation": fp(app / "attempt.json"), "record_first": fp(app / "checkpoint-0001.json"),
           "preflight_readback": fp(app / "checkpoint-0002.json"),
           "completion_readback": fp(app / "checkpoint-0003.json"),
           "tool_outcomes": appev["tool_outcomes"],
           "limits": "Historical ABSENT and ordering are corroborated durable records, not a contemporaneous observation by this verifier or trusted OS event replay"})
    originalfiles = appinv["repository"]["manifest"]
    currentmap = {f["path"]: f for f in current["files"]}
    originalpaths = {f["path"] for f in originalfiles}
    appfiles = sorted(rel(p) for p in app.rglob("*") if p.is_file())
    allowedapp = sorted(rel(app / p) for p in [
        "attempt.json", "checkpoint-0001.json", "checkpoint-0002.json", "checkpoint-0003.json",
        "report.md", "result.json", "attachments/GOV-AUD-20261102-001-linked-clarification.md",
        "evidence/preflight-evidence.json", "evidence/application-evidence.json"])
    added = sorted(set(currentmap) - originalpaths)
    removed = sorted(originalpaths - set(currentmap))
    check("V08", "Complete actual change set and all 302 preexisting files preserved",
          len(originalfiles) == 302 and all(currentmap.get(f["path"]) == f for f in originalfiles)
          and not removed and appfiles == allowedapp and added == allowedapp
          and len(currentmap) == 311
          and current["repository"]["head"] == appinv["repository"]["head"]
          and current["repository"]["branch"] == appinv["repository"]["branch"],
          {"base_manifest": fp(app / "attempt.json"), "preexisting_files": 302,
           "all_before_file_bytes_and_paths_match": True, "actual_added_paths": added,
           "removed": removed, "unauthorized_added_paths": [],
           "all_verifier_inputs": len(currentmap), "index_and_status": "Verifier baseline/checkpoint equality; historical Application reports same HEAD/branch/status"})
    oldtarget = old / "attachments/GOV-AUD-20261102-001-linked-clarification.md"
    oldresult = strict((old / "result.json").read_bytes())
    check("V09", "Failed predecessor remains terminal, unchanged and ineligible; no tooling/payload conflation",
          not os.path.lexists(oldtarget) and oldresult.get("substantive_application_started") is False
          and all(currentmap.get(f["path"]) == f for f in originalfiles if f["path"].startswith(rel(old) + "/")),
          {"failed_result": fp(old / "result.json"), "failed_report": fp(old / "report.md"),
           "old_target": {"path": rel(oldtarget), "presence": "ABSENT"},
           "failure": "Internal Python tuple to JSON list complete-object equality failure before payload publication; not payload drift or a new substantive finding",
           "preserved": [f for f in originalfiles if f["path"].startswith(rel(old) + "/")]})
    originalbody = (affected / "report.md").read_text(encoding="utf-8")
    lines = originalbody.splitlines()
    evpath = affected / "evidence/investigation-evidence.json"
    evfp = fp(evpath)
    aresult = strict((affected / "result.json").read_bytes())
    # Source strings are independently extracted, not accepted from applier comparison.
    contextp = base / "20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55/evidence/approval-context.json"
    originalresponse = strict(contextp.read_bytes())["exact_approval_verbatim"]
    attributedp = base / "20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694/attachments/IGV-FIND-001-approval-transcription-correction.md"
    attributedbody = attributedp.read_text(encoding="utf-8")
    attributed = [line[2:] for line in attributedbody.splitlines() if line.startswith("> I approve")][0]
    differences = [{"offset": i, "original": "U+%04X" % ord(x), "attributed": "U+%04X" % ord(y)}
                   for i, (x, y) in enumerate(zip(originalresponse, attributed)) if x != y]
    check("V10", "Linked correction addresses only original line 15 metadata and line 27 codepoint distinction",
          all(marker in lines[14] for marker in ["{evrel}", "{ev['bytes']}", "{ev['sha256']}"])
          and "IGV-FIND-001" in lines[26]
          and evfp["bytes"] == 22254 and evfp["sha256"] == "8D008604EFEC599AC751EB1B457FD72750E3B4ECB7E0B5071087E64F1A67F977"
          and len(originalresponse) == len(attributed) == 133
          and differences == [{"offset": 27, "original": "U+003F", "attributed": "U+00A7"},
                              {"offset": 42, "original": "U+003F", "attributed": "U+00A7"}]
          and sha(originalresponse.encode("utf-8")) == "B56EFD8E79335C945F829E267E977398B0E685347B86019A18ABE3A48573DE19"
          and sha(attributed.encode("utf-8")) == "F64D83824A1A31FA470FAC6FC36631F5687B468F6EC9DA777C2EFD0253ECF085",
          {"affected_report": fp(affected / "report.md"), "line15_metadata": evfp,
           "terminal_result": fp(affected / "result.json"),
           "original_response_source": fp(contextp), "attributed_source": fp(attributedp),
           "differences": differences, "Unicode_codepoints_each": 133,
           "original_utf8_bytes": len(originalresponse.encode("utf-8")),
           "attributed_utf8_bytes": len(attributed.encode("utf-8")),
           "qualification": "Attributed parent response is not newly authenticated approval; no original message ID/time or transport-cause inference",
           "scope": "No wholesale invalidity, GOV-001/GOV-002 reopening, P1-P5 reapplication or broad punctuation normalization"})
    masterpaths = ["docs/ai/sdlc/SDLC_GOVERNANCE.md", "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
                   "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md"]
    masterhashes = ["79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
                    "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
                    "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C"]
    mastertext = [(ROOT / p).read_text(encoding="utf-8") for p in masterpaths]
    auditbody = (audit / "report-revision-0001.md").read_text(encoding="utf-8")
    check("V11", "Cross-document authority, seven mechanisms, 52-core and Master/non-Master boundaries unchanged",
          all(fp(ROOT / p)["sha256"] == h for p, h in zip(masterpaths, masterhashes))
          and "all seven" in mastertext[1] and "52-core" in mastertext[1]
          and "non-Master change does not require Master-baseline adoption" in mastertext[0]
          and "CONSISTENT WITH MINOR FINDINGS" in auditbody
          and "not a new approval" in attributedbody
          and "standing authority" in payload.decode("ascii")
          and "transient" in scope["risks"] and "not a new approval-validity condition" in scope["risks"],
          {"Masters": [fp(ROOT / p) for p in masterpaths],
           "mechanisms": ["Governance Audit", "Governance Remediation", "SDLC Process Orchestration",
                          "SDLC Portability Assessment", "Governance Amendment Application",
                          "Independent Governance Verification", "Independent Governance Review"],
           "52_core": "Unchanged boundary; no catalog expansion or new Audit performed",
           "cross_links": "Linked payload resolves exact immutable report/evidence/result and two historical response sources; no governance definition is edited",
           "effectiveness": "Non-Master record clarification still requires passing independent Review and a new complete qualifying Audit; no Master adoption required for this correction",
           "latest_full_Audit": fp(audit / "report-revision-0001.md"),
           "latest_full_Audit_status": "COMPLETED / CONSISTENT WITH MINOR FINDINGS; one Low; Governance Remediation FAIL, other six PASS; not adoption/effectiveness qualifying",
           "adoption": "Masters remain candidate/unadopted; no adoption or product readiness claimed"})
    check("V12", "Current repository/root/Work ID and scope authority",
          current["repository"]["head"] == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
          and current["repository"]["branch"] == "sdlc-framework-onboarding"
          and "ScalableParimal/SupportIQ" in current["repository"]["origin"]
          and request["work_id"] == WORK and inv["work_id"] == WORK,
          {"repository": current["repository"],
           "root": "docs/sdlc-records/governance/", "work_id": WORK,
           "root_decision": {
               "url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
               "author": "ScalableParimal", "author_id": 226102895, "association": "OWNER",
               "created_at": "2026-10-30T12:31:51Z", "updated_at": "2026-10-30T12:31:51Z",
               "current_resolution": "github-mcp-server issue_read get_comments issue 3 page 1 perPage 100 independently reopened this invocation; exact HEAD/three Master hashes/root/Work ID matched",
               "authority_limit": "Original Audit-only bootstrap stage not reused; only root adoption relied upon; current Human Verification start is separate"},
           "publication": PREFIX,
           "prohibitions": "No fixes, source/history/upstream writes, Review, Audit, adoption, commit, push or product work"})
    final = snapshot()
    check("V13", "Meaningful-boundary and prepublication procedural non-mutation checkpoint",
          comparable(final) == comparable(baseline),
          {"input_files": len(final["files"]), "baseline": inv["qualification"],
           "all_bytes_paths_directories_index_external_status_HEAD_branch_unchanged": True,
           "snapshot_digest": sha(encode(comparable(final))),
           "concurrency": "No observed evaluated-input/path-set changes; only exact own designated output paths excluded",
           "limitations": LIMITS})
    evidence = {
        "schema_version": "1.0", "record_type": "independent_governance_verification_evidence",
        "record_id": ATTEMPT + ":verification-evidence", "work_id": WORK,
        "attempt_id": ATTEMPT, "cycle_id": inv["cycle_id"], "cycle_number": 1,
        "finding_id": "GOV-AUD-20261102-001", "created_at_utc": now(),
        "actor": inv["actor_identity"], "outcome": "PASS",
        "assurance_mode": "PROCEDURAL NON-MUTATION", "criteria": criteria,
        "independently_recomputed_bindings": seen,
        "all_structured_sources": [fp(p) for p in docs],
        "complete_current_input_snapshot": final,
        "baseline_binding": inv["qualification"], "invocation": fp(OWN / "attempt.json"),
        "record_first_readback": fp(OWN / "checkpoint-0001.json"),
        "serializer_self_tests": selftest(),
        "ordered_operations": [
            {"sequence": 7, "tool": "functions.powershell / verification.py initial", "outcome": "qualification and invocation no-overwrite publication PASS, hashes returned in transcript"},
            {"sequence": 8, "tool": "functions.powershell fresh Python -B import", "outcome": "strict parse/hash/readback plus complete snapshot checkpoint PASS before substantive comparison"},
            {"sequence": 9, "tool": "functions.view, functions.powershell, functions.rg", "operation": "Read exact package section 4/full scope, payload, Application structured evidence/authority/checkpoints, affected report, historical response source, latest full Audit scope/status, governing Master and Application contracts", "outcome": "PASS; one mistyped historical attachment date read failed nonmutating then exact 20261030 path successfully read; large outputs narrowed/ranged, no input writes; parallel operations have no invented within-group order"},
            {"sequence": 10, "tool": "tool_search then github-mcp-server issue_read", "arguments": {"method": "get_comments", "owner": "ScalableParimal", "repo": "SupportIQ", "issue_number": 3, "page": 1, "perPage": 100}, "outcome": "OWNER root decision independently resolved; not current stage authorization"},
            {"sequence": 11, "tool": "functions.apply_patch", "operation": "Extend only own unpublished verification helper, not evaluated input or final record", "outcome": "PASS"},
            {"sequence": 12, "tool": "functions.powershell Python verification.py evaluate", "integrity_bound_arguments": fp(OWN / "verification.py"), "operation": "Strict parse all actual evidence, independent current hashes, entire manifests/path-set comparison, codepoint extraction, scope/cross-document checks, meaningful/final snapshot and own checkpoint/evidence/report publication", "outcome": "PASS if this evidence is successfully published/read back; canonical result follows fresh-process validation"}
        ],
        "operation_coverage": "Actor-visible ordered tool transcript plus own checks; no complete OS event stream or exact per-file operation times. Script binds arguments for machine checks.",
        "limitations": LIMITS, "unresolved": [],
        "next_gate": "Separate fresh actual Human initiation of Independent Governance Review matching approved planned reviewer, after this completed PASS; no automatic start",
        "effectiveness": False,
    }
    c = {
        "schema_version": "1.0", "record_type": "checkpoint", "work_id": WORK,
        "attempt_id": ATTEMPT, "sequence": 2, "created_at_utc": now(),
        "boundary": "Substantive verification complete; all evaluated inputs unchanged immediately before evidence/report publication",
        "baseline": inv["qualification"], "invocation": fp(OWN / "attempt.json"),
        "input_count": len(final["files"]), "input_path_and_state_digest": sha(encode(comparable(final))),
        "criteria": [{"id": x["criterion"], "outcome": x["outcome"]} for x in criteria],
        "limitations": LIMITS,
    }
    cfp = publish("checkpoint-0002.json", c)
    evidence["completion_checkpoint"] = cfp
    efp = publish("evidence/verification-evidence.json", evidence)
    report = build_report(evidence, efp, cfp)
    rfp = publish("report.md", data=report.encode("ascii"))
    print(json.dumps({"outcome": "PASS_PENDING_TERMINAL_READBACK_RESULT",
                      "criteria": len(criteria), "bindings": len(seen), "unique_paths": len(cache),
                      "evidence": efp, "report": rfp, "checkpoint": cfp}, indent=2))

def build_report(e, efp, cfp):
    rows = "\n".join("| " + c["criterion"] + " | " + c["title"] + " | PASS |" for c in e["criteria"])
    def binding(f):
        return "`" + f["path"] + "` (" + str(f["bytes"]) + " bytes; SHA-256 `" + f["sha256"] + "`)"
    c = {v["criterion"]: v["evidence"] for v in e["criteria"]}
    return (
        "# Independent Governance Verification - GOV-AUD-20261102-001\n\n"
        "## Outcome and bounded subject\n\n"
        "**PASS - procedural non-mutation assurance.** Only the completed linked clarification "
        "Application is verified. This is not Review, a Governance Audit, Human Approval, "
        "effectiveness, Master adoption, product readiness or acceptance. Terminal completion "
        "requires the later integrity-bound result.json after fresh-process readback.\n\n"
        "Work ID: `" + WORK + "`; cycle GOV-REMEDIATION-PROSPECTIVE-001, Cycle 1.\n"
        "Verifier attempt: `" + ATTEMPT + "`; runtime session "
        "`923a55cc-499e-4d83-8923-11f097bbcb71`.\n"
        "Repository: ScalableParimal/SupportIQ; local root C:\\PARIMAL_SHERE\\SCALABLE_SOLUTIONS\\SupportIQ; "
        "HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`; branch `sdlc-framework-onboarding`.\n\n"
        "## Fresh initiation, identity, qualification and record-first order\n\n"
        "Actual Human Verification initiation supplied in current request:\n\n"
        "> " + START + "\n\n"
        "This followed the completed successful Application result. It starts only Verification, "
        "not a downstream stage or substantive approval. Parent message IDs/times are not "
        "authenticated/exposed; none are invented.\n\n"
        "Current verifier definition: " + binding(e["actor"]["definition"]) + ".\n"
        "Current actor is distinct from the Corrective Change Decision recovery preparer "
        "(attempt 20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed), the Governance Amendment "
        "Application publisher (attempt 20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd), "
        "and the planned independent Review definition. The exact four approval-bound "
        "definition paths/hashes are retained in V01/V03 evidence. Reviewer remains planned "
        "only; no future runtime/attempt is fabricated. Shared OS principal "
        "`int-scl-010\\parimal`, SID S-1-5-21-2809803128-1021655904-3966773769-1002, "
        "does not establish process-actor identity or technical isolation.\n\n"
        "Nonmutating current reads, SHA-256, strict JSON, path/status/index checks and "
        "permission inspection established capability. Writable ACLs/tools are disclosed, "
        "not treated as authority to modify inputs. Publication authority is confined to "
        "this fresh own attempt under the existing Work ID. Full 311-file non-.git "
        "manifest includes untracked records and directories, byte counts/hashes, index, "
        "HEAD, branch and external status; it is not HEAD-only coverage. Exact own "
        "designated outputs alone are excluded, never an upstream attempt/root.\n\n"
        "Order: governing/identity/authority/qualification reads -> baseline snapshot -> "
        "qualification/attempt atomic no-overwrite publication -> fresh-process strict "
        "parse/hash/snapshot readback -> checkpoint-0001 -> substantive comparisons -> "
        "meaningful-boundary/final snapshot comparison -> checkpoint-0002 -> evidence "
        "and report -> separate fresh-process readback and final snapshot -> result last. "
        "Complete native dict/list/scalar objects are strict-serialized/parsed for equality "
        "before corresponding publication; duplicate keys, NaN and tuple coercion are "
        "rejected by self-tests. Own .partial files are create-new, validated, flushed, "
        "fsynced, Windows atomically renamed without overwrite, then read back/hashed.\n\n"
        "Invocation: " + binding(e["invocation"]) + ".\n"
        "Qualification/initial full manifest: " + binding(e["baseline_binding"]) + ".\n"
        "Precomparison fresh-process checkpoint: " + binding(e["record_first_readback"]) + ".\n"
        "Completed comparison checkpoint: " + binding(cfp) + ".\n\n"
        "## Actual authority trail and complete approval binding\n\n"
        "The actual supplied combined redesignation/approval is:\n\n> "
        + c["V03"]["actual_combined_designation_approval"] + "\n\n"
        "Separate actual Application initiation:\n\n> "
        + c["V03"]["actual_separate_application_start"] + "\n\n"
        "Package: " + binding(c["V03"]["package"]) + ".\n"
        "Exact request: " + binding(c["V03"]["request"]) + ".\n"
        "The Human's current instruction explicitly supplies these decisions and the "
        "presentation binding to complete section 4, exact package hash, designated new "
        "publisher/attempt, target/base, encoding, roles, scope, route, exclusions, "
        "tooling/self-tests and residual-risk disclosures. Application records retain "
        "the same actual wording and complete native approval request/scope objects. "
        "Copy-ready proposed wording is not substituted for the actual decision. "
        "Designation/exact approval is distinct from stage initiation; failed-attempt "
        "authority/start is not silently reused. Residual-risk disclosure is retained, "
        "not an additional approval-validity gate.\n\n"
        "The OWNER root decision was independently reopened using GitHub issue_read "
        "get_comments: https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236 "
        "(ScalableParimal, user ID 226102895, OWNER; created/updated 2026-10-30T12:31:51Z). "
        "Repository, HEAD, root, Work ID and three Master hashes match. Its original "
        "Audit-only start is not generalized; current Verification authority is the "
        "fresh actual instruction above. Masters remain candidate/unadopted.\n\n"
        "## Criterion-by-criterion verification\n\n"
        "| ID | Required criterion | Outcome |\n| --- | --- | --- |\n" + rows + "\n\n"
        "Every row has actual paths/fingerprints, comparisons and qualifications in "
        "the canonical evidence. All " + str(len(e["independently_recomputed_bindings"])) +
        " structured fingerprint occurrences were independently rehashed, not accepted "
        "from the applier's conclusion. Full scope objects match the approved request "
        "without lossy reconstruction. This includes nested role/input/output/base/after "
        "bindings, application checkpoints, preflight bindings, recovery/failure "
        "records and original investigation/result/evidence references.\n\n"
        "## Exact application, base and preservation\n\n"
        "Current target: " + binding(c["V06"]["target"]) + ".\n"
        "Original approved payload: " + binding(c["V06"]["source"]) + ".\n"
        "These complete binary files are equal: 3438 bytes, SHA-256 "
        "`8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA`; "
        "ASCII UTF-8/no BOM/LF only/exactly one final LF. No content/header/footer/"
        "signature/newline change or unresolved payload template. Approved and actual "
        "substantive path lists contain exactly this target.\n\n"
        "Base was ABSENT, null byte count/hash (not empty-file identity). Recovery "
        "proposal, qualified Application invocation, preflight/checkpoint and operation "
        "records corroborate the new attempt/destination and no-overwrite route. "
        "This verifier did not witness the historical base or replay a trusted OS "
        "event stream; those are explicitly historical durable observations. Complete "
        "Application ordering/readback evidence and current resulting bytes agree.\n\n"
        "All 302 files in the Application preexisting manifest match current bytes/hashes "
        "and paths. The only nine additional files are its own attempt, three checkpoints, "
        "report/result, two evidence files and exact approved attachment. No missing or "
        "unauthorized added path; all 311 evaluated inputs remain unchanged at this "
        "verifier's observed boundaries. Original Investigation report SHA-256 "
        "`CE975EE00E642B93AF50EF8FF0FF418101CE821F2E94121D43E0B260A012BF6B`, "
        "source evidence/result, historical records and failed script are preserved. "
        "HEAD/branch match; verifier index/external status/path sets remain unchanged.\n\n"
        "The failed terminal attempt 20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31 "
        "remains unchanged and FAILED/CANNOT COMPLETE; its old target remains absent. "
        "Its pre-publication tuple-to-JSON-list strict equality failure is execution "
        "tooling failure, not evidence of payload drift or a new substantive finding. "
        "No failed preflight/result was relabelled as successful.\n\n"
        "## Linked clarification semantics and cross-document effects\n\n"
        "Original line 15 retains three literal expressions; linked metadata resolves "
        "the actual evidence path, 22254 bytes and SHA-256 "
        "`8D008604EFEC599AC751EB1B457FD72750E3B4ECB7E0B5071087E64F1A67F977`, "
        "consistent with the immutable terminal result. Original line 27's historical "
        "response distinction is independently derived from actual original JSON and "
        "attributed qualification text: 133 Unicode code points each; offsets 27 and 42 "
        "are U+003F QUESTION MARK versus U+00A7 SECTION SIGN. UTF-8 response lengths are "
        "133 versus 135 bytes; both response hashes match the clarification. No lossy "
        "Unicode quotation, new authentication, parent message time/ID or precise "
        "transport cause is asserted.\n\n"
        "The payload links rather than overwrites or wholesale supersedes its original; "
        "it does not reopen GOV-001/GOV-002, reapprove/reapply P1-P5, normalize other "
        "punctuation, create standing authority or alter any prior Audit/Review/"
        "Verification conclusion. All three Masters and governance definitions are "
        "unchanged. Authority and read/write boundaries, fresh Human gates, all seven "
        "separately reported mechanisms and the fixed 52-core boundary are retained.\n\n"
        "Latest full Audit: " + binding(c["V11"]["latest_full_Audit"]) + ". "
        "It remains completed CONSISTENT WITH MINOR FINDINGS, one Low, Governance "
        "Remediation FAIL/other six mechanisms PASS. This Verification does not revise "
        "that Audit, close its finding by fiat, or make it effectiveness/adoption qualifying. "
        "This is a non-Master record clarification: no Master adoption is required "
        "for it, but independent Review and a new complete qualifying Audit still are. "
        "Master baseline adoption, if later pursued, remains separate and prospective.\n\n"
        "## Operation evidence, concurrency and material limitations\n\n"
        + LIMITS + "\n\n"
        "Ordered actor-visible events, script argument integrity binding, current "
        "permission/token evidence, full snapshots and exact exclusion list are "
        "retained in qualification/evidence. Read-only diagnostics include unsupported "
        "PowerShell UTC option (replaced), large/truncated output narrowed/ranged, "
        "and one mistyped historical attachment date (corrected read only). None "
        "was an input write or concealed publication failure. Parallel read groups "
        "have no invented internal order or exact per-read times. Host samples "
        "are not authenticated parent decision or exact publication timestamps. "
        "A changed evaluated input would invalidate affected conclusions; none "
        "was observed. No write probe, source/other-actor edit, fix, rollback, nested "
        "agent, Review, Audit, adoption, commit/push or product work occurred.\n\n"
        "## Canonical evidence, result and next permitted gate\n\n"
        "Canonical evidence: " + binding(efp) + ".\n"
        "Canonical result is `" + PREFIX + "/result.json`, published last only after "
        "independent readback and an immediate final unchanged-input comparison. "
        "The result binds this report and evidence; no circular self-hash is claimed. "
        "Final result/report fingerprints are returned in the invocation response "
        "and own final-readback evidence.\n\n"
        "Unresolved Verification findings: none. Pending gates: separate fresh actual "
        "Human initiation of Independent Governance Review matching its approved "
        "planned definition, then only after PASS a separately initiated complete "
        "Governance Audit. Effectiveness requires exact CONSISTENT, every required "
        "count zero and all seven groups without unresolved issues. Stop here; "
        "no downstream stage is initiated.\n"
    )

if __name__ == "__main__":
    if sys.argv[1:] == ["initial"]:
        initial()
    elif sys.argv[1:] == ["evaluate"]:
        evaluate()
