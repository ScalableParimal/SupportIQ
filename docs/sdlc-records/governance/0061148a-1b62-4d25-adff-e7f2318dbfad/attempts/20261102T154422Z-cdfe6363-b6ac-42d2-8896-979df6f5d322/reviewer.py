import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[6]
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T154422Z-cdfe6363-b6ac-42d2-8896-979df6f5d322"
ACTOR = "9b69bce7-c71e-487c-8893-23715797ad44"
ROLE = "Independent Governance Review"
BASE = "docs/sdlc-records/governance/" + WORK + "/attempts/"
OWN = BASE + ATTEMPT + "/"
PREP = BASE + "20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d/"
APP = BASE + "20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494/"
VER = BASE + "20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216/"
INV = BASE + "20261102T141609Z-4e74248e-a440-4617-8c17-61f31f2ff9c9/"
AUDIT = BASE + "20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f/"
START = "Yes, initiate Independent Governance Review for the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 five-file amendment and its fresh passing Verification only"
APPROVAL = "I approve the identified canonical report, exact proposal and patch with all five target fingerprints, scope, actor and assurance bindings; freshly designate the proposed one-time applier under that route; do not start Application"
APPSTART = "Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 under the approved five-file package"
VERSTART = "Yes, initiate one fresh Independent Governance Verification retry for the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 Application only; preserve unsuccessful records and start no later stage"
OUTPUT_NAMES = ["reviewer.py", "attempt.json", "input-manifest.json", "checkpoint-0001.json",
                "checkpoint-0002.json", "checkpoint-final.json", "review-evidence.json", "report.md", "result.json"]
EXCLUDE = {OWN + n for n in OUTPUT_NAMES} | {OWN + n + ".partial" for n in OUTPUT_NAMES}
EVENTS = []
LIMITS = [
    "Procedural non-mutation; sources are not technically write-excluded. Write-capable tools and inherited writable ACLs confer no source-write authority.",
    "Actor-visible tool/operation ordering, not an exhaustive trusted OS event stream. No exact filesystem publication timestamps are claimed.",
    "Matching endpoint fingerprints cannot prove absence of transient writes or same-principal tampering.",
    "No coordinated no-edit lock or exhaustive concurrency visibility; registry and repeated content/path-set/index/HEAD observations are bounded evidence.",
    "Human quotes are supplied by the actual current user with parent-conversation attribution. Authenticated message identifiers and original decision times are unavailable; none invented.",
    "Harness agent registry and current assignment establish invocation attribution, not an external identity/authenticity guarantee. Shared host session title is not role proof.",
    "This is only the five-file amendment Review, not a complete Governance Audit, finding closure, effectiveness declaration, Master adoption or product-root adoption."
]

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def event(op, paths=None, outcome="OK", **extra):
    e = dict(sequence=len(EVENTS)+1, actor=ACTOR, attempt=ATTEMPT,
             observed_at_utc=now(), operation=op, paths=paths or [], outcome=outcome)
    e.update(extra)
    EVENTS.append(e)

def read(path):
    b = (ROOT/path).read_bytes()
    event("read/SHA-256", [path], bytes=len(b), sha256=sha(b))
    return b

def ref(path):
    b = read(path)
    return dict(path=path, bytes=len(b), sha256=sha(b))

def load(path):
    return json.loads(read(path).decode("utf-8-sig"))

def git(*args):
    p = subprocess.run(["git", "--no-pager", *args], cwd=ROOT, capture_output=True, check=True)
    event("git " + " ".join(args), outcome="OK", stdout_bytes=len(p.stdout), stdout_sha256=sha(p.stdout))
    return p.stdout

def common(kind):
    return dict(schema_version="1.0", record_type=kind, record_id=ATTEMPT+":"+kind,
                feature="Governance-only F003/F004; product feature N/A", work_id=WORK,
                cycle_id="GOV-REMEDIATION-PROSPECTIVE-001", cycle=1, process=ROLE,
                attempt_id=ATTEMPT, creator=dict(role=ROLE, runtime_agent_id=ACTOR,
                copilot_agent_session_id=os.environ.get("COPILOT_AGENT_SESSION_ID")),
                created_at_utc=now(), clock_basis="System UTC record preparation, not publication time",
                gate_refs=dict(current="Actual fresh Human Review stage-start in supplied request",
                               predecessor=VER+"result.json", later="Separate complete Governance Audit gate"),
                related_records=[PREP+"result.json", APP+"result.json", VER+"result.json"])

def native(v):
    if type(v) is dict:
        assert all(type(k) is str for k in v), "non-string object key"
        for x in v.values():
            native(x)
    elif type(v) is list:
        for x in v:
            native(x)
    else:
        assert type(v) in (str, int, float, bool, type(None)), "non-native JSON value"
        if type(v) is float:
            assert v == v and abs(v) != float("inf")

def validate(d):
    assert type(d) is dict, "record must be native object, not serialized object string"
    native(d)
    for k in ["schema_version", "record_type", "record_id", "feature", "work_id", "cycle_id",
              "cycle", "process", "attempt_id", "creator", "created_at_utc", "clock_basis",
              "gate_refs", "related_records"]:
        assert k in d and d[k] is not None, "missing common metadata: "+k
    assert d["schema_version"] == "1.0" and d["work_id"] == WORK and d["attempt_id"] == ATTEMPT
    assert d["process"] == ROLE and d["cycle"] == 1
    assert type(d["creator"]) is dict and d["creator"]["runtime_agent_id"] == ACTOR
    assert type(d["gate_refs"]) is dict and type(d["related_records"]) is list
    assert datetime.fromisoformat(d["created_at_utc"]).utcoffset().total_seconds() == 0
    required = {
        "invocation": ["requested_scope", "task_context", "inputs", "repository", "authorization",
                       "predecessor", "output_scope", "runtime", "capabilities", "input_manifest",
                       "operations", "limitations"],
        "input_manifest": ["snapshot"],
        "checkpoint": ["sequence", "last_confirmed_boundary", "repository_effects", "unfinished_work",
                       "observed_evidence", "blockers", "pending_gates", "safe_continuation_prerequisites"],
        "review_evidence": ["outcome", "criteria", "input_manifest", "checkpoints", "operations", "limitations"],
        "result": ["execution_status", "outcome", "report", "evidence", "exact_evaluated_state",
                   "unresolved_items", "next_permitted_process", "limitations"]
    }
    assert d["record_type"] in required
    for k in required[d["record_type"]]:
        assert k in d, "missing process metadata: "+k
    if d["record_type"] == "invocation":
        for k in ["inputs", "repository", "authorization", "predecessor", "runtime", "capabilities", "input_manifest"]:
            assert type(d[k]) is dict, k+" is not native object"
        assert d["predecessor"]["outcome"] == "PASS"
        assert d["predecessor"]["execution_status"] == "COMPLETED"
        assert d["input_manifest"]["files"] and any(x["path"].startswith(".github/") for x in d["input_manifest"]["files"])
        assert d["input_manifest"]["expected_absences"]
    encoded = json.dumps(d, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    parsed = json.loads(encoded)
    assert parsed == d
    assert type(parsed) is dict
    assert b"`n" not in encoded and b"[MUST" not in encoded and b"[STABLE ID]" not in encoded
    return encoded

def selftests():
    a = common("input_manifest")
    a["snapshot"] = dict(native_object=True, quote=START, null=None, values=[1, False, "CRLF\r\n"])
    assert json.loads(validate(a)) == a
    for bad in [json.dumps(a), [], {k:v for k,v in a.items() if k != "feature"},
                dict(a, creator=json.dumps(a["creator"])), dict(a, snapshot={"bad": (1, 2)})]:
        try:
            validate(bad)
        except (AssertionError, TypeError, ValueError):
            continue
        raise AssertionError("invalid JSON/metadata test was accepted")
    event("strict native complete-object metadata/roundtrip positive and negative selftests", outcome="PASS")

def publish(name, obj):
    path = OWN+name
    assert path in EXCLUDE and name != "reviewer.py"
    if name.endswith(".json"):
        data = validate(obj)
    else:
        assert type(obj) is str and "`n" not in obj and "[MUST" not in obj
        data = obj.encode("utf-8")
    dest = ROOT/path
    partial = Path(str(dest)+".partial")
    assert not dest.exists() and not partial.exists(), "publication collision"
    with partial.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    back = partial.read_bytes()
    assert back == data
    if name.endswith(".json"):
        assert validate(json.loads(back)) == data
    event("validated and flushed own unpublished partial", [str(partial.relative_to(ROOT)).replace("\\","/")],
          bytes=len(data), sha256=sha(data))
    assert os.name == "nt", "rename no-overwrite route qualified for Windows only"
    os.rename(partial, dest)
    assert dest.read_bytes() == data
    event("atomic Windows rename no-overwrite and fresh readback", [path], bytes=len(data), sha256=sha(data),
          time_basis="Ordering observed, exact publication instant not captured")
    return dict(path=path, bytes=len(data), sha256=sha(data))

def snapshot():
    tracked = set(git("ls-files", "-z").decode("utf-8").split("\0")) - {""}
    files = []
    dirs = []
    for parent, dn, fn in os.walk(ROOT):
        pp = Path(parent)
        if pp == ROOT:
            dn[:] = [x for x in dn if x != ".git"]
        for n in dn:
            p = (pp/n).relative_to(ROOT).as_posix()
            if p != OWN.rstrip("/"):
                dirs.append(p)
        for n in fn:
            full = pp/n
            p = full.relative_to(ROOT).as_posix()
            if p in EXCLUDE:
                continue
            assert not full.is_symlink(), "unqualified symbolic link: "+p
            b = full.read_bytes()
            files.append(dict(path=p, present=True, bytes=len(b), sha256=sha(b), tracked=p in tracked,
                              readable=os.access(full,os.R_OK), writable_acl_observation=os.access(full,os.W_OK),
                              readonly_attribute=bool(getattr(full.stat(),"st_file_attributes",0)&1)))
    files.sort(key=lambda x:x["path"])
    pathset = [x["path"] for x in files]
    status_raw = git("status", "--porcelain=v1", "-uall").decode("utf-8")
    status_lines = [l for l in status_raw.splitlines() if l[3:] not in EXCLUDE]
    index = ROOT/".git/index"
    if not index.is_file():
        gitdir = git("rev-parse","--git-path","index").decode().strip()
        index = ROOT/gitdir
    absences = ["AGENTS.md", ".github/copilot-instructions.md", "docs/sdlc-records/product"]
    return dict(files=files, directories=sorted(dirs), path_set_sha256=sha("\n".join(pathset).encode()),
                expected_absences=[dict(path=x,present=(ROOT/x).exists()) for x in absences],
                tracked_paths_sha256=sha("\n".join(sorted(tracked)).encode()),
                repository=dict(canonical_repository="ScalableParimal/SupportIQ", root=str(ROOT),
                                head=git("rev-parse","HEAD").decode().strip(),
                                branch=git("branch","--show-current").decode().strip(),
                                index_bytes=index.stat().st_size,index_sha256=sha(index.read_bytes()),
                                refs_sha256=sha(git("show-ref")),
                                status_excluding_exact_own_outputs=status_lines,
                                unstaged_diff_sha256=sha(git("diff","--binary")),
                                staged_diff_sha256=sha(git("diff","--cached","--binary"))),
                coverage="Every filesystem file hidden-inclusive outside .git, except exact designated own output files; .git bound by index/ref/HEAD/status/diff observations",
                excluded_exact_own_outputs=sorted(EXCLUDE),
                permissions_basis="Per-file os.access and readonly attributes; current effective principal and inherited ACL observed separately; no write probe")

def compare(a,b):
    aa = {x["path"]:x for x in a["files"]}
    bb = {x["path"]:x for x in b["files"]}
    delta = dict(added=sorted(bb.keys()-aa.keys()), removed=sorted(aa.keys()-bb.keys()),
                 changed=[p for p in aa.keys() & bb.keys() if aa[p]!=bb[p]],
                 directories_changed=a["directories"]!=b["directories"],
                 repository_changed=a["repository"]!=b["repository"],
                 absences_changed=a["expected_absences"]!=b["expected_absences"])
    assert not any(delta.values()), "unexplained evaluated-input drift: "+str(delta)
    return dict(outcome="UNCHANGED", file_count=len(aa), delta=delta,
                path_set_sha256=b["path_set_sha256"], repository=b["repository"])

EXPECTED = {
    PREP+"report.md": (39577,"A925ECCE1D7593DE1955EC0CA416A1BDFD1AA67A5B1800129BF8FA3C1B685677"),
    PREP+"result.json": (11450,"A4BEE48991E0CA74D414BDDA1957220F0703E1FEF7F62AE50536E9EDB6A725ED"),
    PREP+"attachments/exact-proposal.json": (21495,"086D48C77EC7D6C052615498DC82B380493B2C0610F9AAF070D1FFF08580D29C"),
    PREP+"attachments/minimal.patch": (13651,"DFE0F97EE5EC19D0194E6FFB9FC2C3CD5104F41B9B9DCA908837556E1E99F1DD"),
    APP+"report.md": (9379,"6964F08042A633D53790E52FD6089AAA268C6D9DBC37E5DC88B999383160C6C6"),
    APP+"result.json": (10315,"2B45D3CC36B665D0CCB561D0C0C32DADA35D9260319A62A1AC6B8B36B1B80CF7"),
    APP+"evidence/application-evidence.json": (199421,"9C0C75BD3E2C96655F6F6BB09F73056A1C243B490DBAFB1A687EBB84EE168D4B"),
    APP+"checkpoint-0002.json": (70499,"350100E17EF345D7116C7AE5FD8C1CC52CC367496A970534567014B0DD488F51"),
    VER+"report.md": (29429,"A6760AB96EBA87BBC92EE6E1BA50989594D55C313651934177457591A3B04B82"),
    VER+"result.json": (159760,"9DF69D773325B6271F05E7339743FD9ED2D8BF0B8374D6C384037EBABB7DE6EB"),
    VER+"verification-evidence.json": (1918232,"A62DD58BFB6197081C20BB3F945C4584A4F75ECC260DA5D427710E8F9E03DD09"),
    INV+"report-revision-0002.md": (21951,"1B298794D8AA503E4C18AA3730754FA170D6196B7745160390BB9C68246D1365")
}

def prerequisites():
    refs = {}
    for p,(n,h) in EXPECTED.items():
        r = ref(p)
        assert (r["bytes"],r["sha256"]) == (n,h), "stale supplied binding "+p
        refs[p] = r
    v = load(VER+"result.json")
    assert v["outcome"] == "PASS" and v["execution_status"] == "COMPLETED"
    assert v["work_id"] == WORK and v["creator"]["runtime_agent_id"] == "8e0bf478-bfeb-461b-90ed-64033f60f8d5"
    for k in ["report","evidence","invocation","input_manifest"]:
        r = v[k]
        assert type(r) is dict
        actual = ref(r["path"])
        assert actual["sha256"] == r["sha256"] and actual["bytes"] == r["bytes"]
    app = load(APP+"result.json")
    prep = load(PREP+"result.json")
    identities = [ACTOR,prep["creator"]["runtime_agent_id"],app["creator"]["runtime_agent_id"],v["creator"]["runtime_agent_id"]]
    assert len(set(identities)) == 4
    assert app["record_type"] == "application_result" and app["process"] == "Governance Amendment Application" and app["outcome"] == "COMPLETED"
    assert APPSTART == load(VER+"attempt.json")["authorization"]["separate_application_start_exact_ascii"]
    assert APPROVAL == load(VER+"attempt.json")["authorization"]["approval_exact_ascii"]
    assert VERSTART == load(VER+"attempt.json")["authorization"]["fresh_start_exact_ascii"]
    return refs,v,app

def prepare():
    selftests()
    refs,v,app = prerequisites()
    initial = snapshot()
    assert initial["repository"]["head"] == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert initial["repository"]["branch"] == "sdlc-framework-onboarding"
    assert all(x["readable"] for x in initial["files"])
    assert not any(x["present"] for x in initial["expected_absences"])
    a = common("invocation")
    a.update(requested_scope="ONLY Independent Governance Review GOV-AUD-20261102-003 and GOV-AUD-20261102-004 five-file approved amendment and fresh PASS Verification",
             task_context="N/A: governance-only correction; no approved product Requirement/Plan or product work",
             inputs=refs, repository=initial["repository"], input_manifest=initial,
             authorization=dict(fresh_start_exact_ascii=START,approval_exact_ascii=APPROVAL,
                  separate_application_start_exact_ascii=APPSTART,separate_verification_start_exact_ascii=VERSTART,
                  source="Actual current user supplies parent-conversation Human decisions and Review start; no inferred authority",
                  authenticated_message_id=None, original_decision_time=None, single_attempt_only=True,
                  existing_root=dict(path="docs/sdlc-records/governance/",work_id=WORK,
                     canonical_comment="https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                     author="ScalableParimal",author_id=226102895,association="OWNER",
                     created_updated_at="2026-10-30T12:31:51Z",
                     fresh_resolution="Current github issue_read get_comments result; original initial Audit scope not reused",
                     current_authority="Persistent root adoption plus Governance section 3 finding-led correction and current exact Human stage-start; no Master/product adoption")),
             predecessor=dict(result=refs[VER+"result.json"],report=refs[VER+"report.md"],
                  evidence=refs[VER+"verification-evidence.json"],execution_status=v["execution_status"],
                  outcome=v["outcome"],application_execution_status="COMPLETED (Application process-specific outcome field)",
                  application_outcome=app["outcome"],failed_prior_verifications="Preserved history; not current assurance or live writer"),
             output_scope=dict(root=OWN,exact_paths=sorted(EXCLUDE),no_source_or_history_writes=True),
             runtime=dict(role=ROLE,runtime_agent_id=ACTOR,
                  identity_basis="Current developer-assigned Independent Governance Review; only running registry agent matches current assignment, Lifecycle and Timing Review; current COPILOT_AGENT_SESSION_ID separately observed",
                  host_session="ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
                  copilot_agent_session_id=os.environ.get("COPILOT_AGENT_SESSION_ID"),
                  effective_principal="int-scl-010\\parimal",
                  preparer="4d0c3747-fde6-48c7-b125-5adb2af5b80c",applier="ec7a8339-a9b5-4710-bb5b-a8760309005d",
                  verifier="8e0bf478-bfeb-461b-90ed-64033f60f8d5",
                  excluded_coordinator="bbd899a3-3c5f-444e-9d88-5df37ef2d3d6",
                  separation="All distinct; not active Remediation or Orchestrator; title and shared OS principal are not role proof",
                  concurrency="Registry showed only this current reviewer running; idle historic actors are not inferred writers; no lock"),
             capabilities=dict(read="All exact predecessor bindings read and SHA-256 confirmed; hidden-inclusive filesystem manifest and Git observations",
                  checks="Python native JSON/metadata positive/negative tests and non-mutating reads, hashlib, subprocess Git",
                  publication="Own helper created via apply_patch in explicit authorized scope; inherited ACL Authenticated Users Modify; os.access observed. Validated .partial fsync -> Windows rename no overwrite -> readback, followed by separate fresh process readback",
                  acl="whoami int-scl-010\\parimal; attempts inherited ACL owner INT-SCL-010\\Parimal, Administrators/SYSTEM FullControl, Users ReadAndExecute, Authenticated Users Modify; no write probes or enforced sandbox claim",
                  source_permissions="Per-input access and readonly attributes in manifest; write-capable tools and writable ACLs are procedural conduct restrictions, not blockers",
                  helper=ref(OWN+"reviewer.py"),native_json_complete_object_selftests="PASS"),
             operations=dict(prequalification=[
                  "1207 current mandatory reviewer Skill read",
                  "1208 role read; absent optional .github/copilot-instructions.md and AGENTS.md observed, no write",
                  "1209 current Review Guideline/Prompt/Request read and directory discovery",
                  "1210 request, Master paths and attempt enumeration",
                  "current host metadata via get_current_session",
                  "1211 expected missing invocation.json; actual schema uses attempt.json; no publication occurred",
                  "1212 prerequisite schema discovery; output encoding error only, no input writes",
                  "1213 common metadata/30.1/33.1 and predecessor schema read",
                  "list_agents scope all: only running current reviewer; idle history not treated as concurrent writers",
                  "1214-1216 exact status, authority, effective principal, ACL, runtime env and repository reads",
                  "github issue_read get_comments: current root decision independently resolved",
                  "1217 attempt identity allocation, shape-only prerequisite reads, absent optional instructions",
                  "apply_patch creation of only own unpublished reviewer.py helper",
                  "1218 unpublished preflight stopped at schema assumption execution_status on Application; no attempt/partial was published",
                  "1219 fresh Application result schema read: process-specific outcome COMPLETED, not PASS; attempt and partial absent confirmed",
                  "1220 unpublished preflight rejected mistaken generic Application record_type; no publication reached",
                  "1221 exact Application record_type application_result, process Governance Amendment Application, outcome COMPLETED read",
                  "Own unpublished helper corrected to require exact Application-specific record_type/process/outcome; checks not weakened"
                  ],events=list(EVENTS),
                  limits="Tool-call observable sequence and helper operation events; no exhaustive OS trace or external authentication"),
             limitations=LIMITS)
    print(json.dumps(dict(preflight_native_validation="PASS",files=len(initial["files"]),outcome="QUALIFIED",
                          invocation=publish("attempt.json",a)),indent=2))

def readback():
    selftests()
    a = load(OWN+"attempt.json")
    validate(a)
    b = read(OWN+"attempt.json")
    assert json.loads(b) == a
    current = snapshot()
    stable = compare(a["input_manifest"],current)
    assert a["authorization"]["fresh_start_exact_ascii"] == START
    event("independent fresh process invocation readback and integrity/native/schema check", [OWN+"attempt.json"], outcome="PASS")
    m = common("input_manifest")
    m["snapshot"] = a["input_manifest"]
    mr = publish("input-manifest.json",m)
    c = common("checkpoint")
    c.update(sequence=1,last_confirmed_boundary="Invocation validated, flushed, atomically published without overwrite, then independently read back before substantive assessment",
             repository_effects="Only exact own helper and invocation/manifest/checkpoint records; no source or upstream writes",
             unfinished_work=["Substantive independent Review"],observed_evidence=dict(invocation=ref(OWN+"attempt.json"),
                  input_manifest=mr,comparison=stable,events=list(EVENTS)),blockers=[],
             pending_gates=["Separate complete Governance Audit after PASS Review and fresh Human start"],
             safe_continuation_prerequisites="Stable bounded inputs; remain read-only; single authorized attempt only")
    cr = publish("checkpoint-0001.json",c)
    print(json.dumps(dict(invocation=ref(OWN+"attempt.json"),checkpoint=cr,comparison=stable),indent=2))

def bound(r):
    assert type(r) is dict and type(r["bytes"]) is int and type(r["sha256"]) is str
    actual = ref(r["path"])
    assert actual["bytes"] == r["bytes"] and actual["sha256"] == r["sha256"], "stale binding: "+r["path"]
    return actual

def upstream_common(d, process, actor):
    native(d)
    for k in ["schema_version","record_type","record_id","feature","work_id","creator","created_at_utc",
              "clock_basis","process","attempt_id","gate_refs"]:
        assert k in d, "fresh Verification common metadata missing: "+k
    assert d["schema_version"] == "1.0" and d["work_id"] == WORK and d["process"] == process
    assert type(d["creator"]) is dict and d["creator"]["runtime_agent_id"] == actor
    assert type(d["gate_refs"]) is dict
    assert datetime.fromisoformat(d["created_at_utc"]).utcoffset().total_seconds() == 0
    assert json.loads(json.dumps(d,ensure_ascii=False,allow_nan=False)) == d

SOURCES = [
    ".github/agents/independent-governance-review.agent.md",
    ".github/skills/independent-governance-review/SKILL.md",
    "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md",
    "docs/ai/prompts/INDEPENDENT_GOVERNANCE_REVIEW_PROMPT.md",
    "docs/ai/request/INDEPENDENT_GOVERNANCE_REVIEW_REQUEST.md",
    "docs/ai/sdlc/SDLC_GOVERNANCE.md",
    "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
    "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md",
    "docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
    "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md",
    "docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md",
    "docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",
    ".github/skills/requirement-update/SKILL.md",
    "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md",
    "docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md",
    "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
    "docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md",
    "docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md",
    "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md",
    ".github/skills/independent-governance-verification/SKILL.md",
]

def assess():
    import difflib
    selftests()
    a = load(OWN+"attempt.json")
    validate(a)
    cp1 = load(OWN+"checkpoint-0001.json")
    assert cp1["last_confirmed_boundary"].startswith("Invocation validated")
    bound(cp1["observed_evidence"]["invocation"])
    pre = compare(a["input_manifest"],snapshot())
    refs,v,app = prerequisites()
    proposal = load(PREP+"attachments/exact-proposal.json")
    auth = load(APP+"evidence/human-authorization.json")
    ae = load(APP+"evidence/application-evidence.json")
    pf = load(APP+"evidence/preflight.json")
    appcp = load(APP+"checkpoint-0001.json")
    appterm = load(APP+"checkpoint-0002.json")
    vi = load(VER+"attempt.json")
    ve = load(VER+"verification-evidence.json")
    vm = load(VER+"input-manifest.json")
    for p in ["attempt.json","input-manifest.json","checkpoint-0001.json","checkpoint-0002.json",
              "checkpoint-0003.json","checkpoint-final.json","verification-evidence.json","result.json"]:
        upstream_common(load(VER+p),"Independent Governance Verification","8e0bf478-bfeb-461b-90ed-64033f60f8d5")
    assert vi["authorization"]["fresh_start_exact_ascii"] == VERSTART
    assert vi["authorization"]["single_attempt_only"] is True
    assert vi["retry"]["retroactive_authorization"] is False and vi["retry"]["prior_assurance_valid"] is False
    assert all(c["outcome"] == "PASS" for c in ve["criteria"]) and len(ve["criteria"]) == 13
    assert not ve["blockers"] and not v["blockers"] and ve["outcome"] == "PASS"
    assert ve["machine_checks"]["outcome"] == "PASS"
    assert ve["machine_checks"]["actual_application_outcome"] == "COMPLETED"
    for k in ["report","evidence","input_manifest","invocation","invocation_readback",
              "machine_checkpoint","source_inspection_checkpoint","final_checkpoint"]:
        bound(v[k])
    for c in ve["criteria"]:
        for r in c["refs"]:
            bound(r)
    assert auth["approval_exact_ascii"] == APPROVAL and auth["separate_stage_start_exact_ascii"] == APPSTART
    assert auth["target_bindings"] == proposal["targets"] and auth["actors"] == proposal["actors"]
    assert auth["approval_route"] == proposal["approval_route"] and auth["byte_contract"] == proposal["byte_contract"]
    for r in auth["package"]:
        bound(r)
    assert ae["outcome"] == "COMPLETED" and ae["error"] is None and ae["preservation_error"] is None
    assert pf["outcome"] == "PASS" and pf["all_five_before_any_write"] is True
    assert appcp["outcome"] == "PASS"
    for r in [pf["invocation"],pf["invocation_readback"],pf["human_authorization"],
              ae["invocation"],ae["preflight"],ae["helper"]]:
        bound(r)
    for k in ["report","evidence","invocation"]:
        bound(app[k])
    definitions = {}
    for actor in proposal["actors"]:
        definitions[actor["role"]] = bound(actor["definition"])
    assert len({r["path"] for r in definitions.values()}) == 4
    assert definitions["planned_reviewer"] == ref(".github/agents/independent-governance-review.agent.md")
    assert definitions["planned_verifier"] == ref(".github/agents/independent-governance-verification.agent.md")
    for actor in proposal["actors"][1:]:
        assert actor["actual_attempt"] is None and actor["current_runtime_identity"] is None
        assert actor["current_capability_evidence"] is None and actor["fresh_stage_start"] is None
    bound(proposal["actors"][0]["attempt"])
    targets = []
    diffs = []
    historical_bases = {}
    for t in proposal["targets"]:
        p = t["path"]
        after = read(p)
        assert len(after) == t["expected_after_bytes"] and sha(after) == t["expected_after_sha256"]
        base = after
        for r in reversed(t["replacements"]):
            old,new = r["before"].encode("utf-8"),r["after"].encode("utf-8")
            assert base.count(new) == 1
            base = base.replace(new,old,1)
        assert len(base) == t["base_bytes"] and sha(base) == t["base_sha256"]
        forward = base
        offsets = []
        for r in t["replacements"]:
            old,new = r["before"].encode("utf-8"),r["after"].encode("utf-8")
            assert r["expected_occurrences"] == 1 and forward.count(old) == 1
            offset = forward.index(old)
            assert offset == r["sequential_input_byte_offset"]
            offsets.append(offset)
            forward = forward.replace(old,new,1)
        assert forward == after
        after.decode("utf-8")
        assert not after.startswith(b"\xef\xbb\xbf") and b"\n" not in after.replace(b"\r\n",b"")
        assert after.endswith(b"\r\n") == t["expected_after_final_newline"]
        assert base.endswith(b"\r\n") == t["base_final_newline"]
        diffs.extend(difflib.unified_diff(base.decode("utf-8").splitlines(keepends=True),
                     after.decode("utf-8").splitlines(keepends=True),fromfile="a/"+p,tofile="b/"+p))
        historical_bases[p] = dict(path=p,bytes=len(base),sha256=sha(base))
        targets.append(dict(path=p,base=historical_bases[p],after=ref(p),sequential_offsets=offsets,
                            exact_forward_reverse_equal=True,utf8_no_bom_crlf=True,
                            final_newline=after.endswith(b"\r\n")))
    patch = "".join(diffs).encode("utf-8")
    assert patch == read(PREP+"attachments/minimal.patch")
    assert len(targets) == 5 and proposal["no_master_change"] and proposal["no_product_change"]
    approved_paths = {x["path"] for x in targets}
    original = load(APP+"evidence/input-manifest.json")["files"]
    changed = []
    for r in original:
        actual = ref(r["path"])
        if (actual["bytes"],actual["sha256"]) != (r["bytes"],r["sha256"]):
            changed.append(r["path"])
            assert r["path"] in approved_paths and r == historical_bases[r["path"]]
    assert len(original) == 474 and set(changed) == approved_paths
    assert len(original)-len(changed) == 469
    assert sorted(ae["actual_changed_paths"]) == sorted(approved_paths)
    for r in ae["final_inventory"]:
        bound(r)
    for r in vm["snapshot"]["files"]:
        bound(r)
    vm_paths = {r["path"] for r in vm["snapshot"]["files"]}
    initial_paths = {r["path"] for r in a["input_manifest"]["files"]}
    added_since_ver_snapshot = sorted(initial_paths-vm_paths)
    assert not vm_paths-initial_paths
    assert added_since_ver_snapshot and all(p.startswith(VER) for p in added_since_ver_snapshot)
    source_refs = [ref(p) for p in SOURCES]
    source_text = {p:read(p).decode("utf-8-sig") for p in SOURCES}
    masters = {
        "docs/ai/sdlc/SDLC_GOVERNANCE.md":"79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
        "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md":"6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
        "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md":"08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C"
    }
    for p,h in masters.items():
        assert ref(p)["sha256"] == h
    report_text = read(PREP+"report.md").decode("utf-8")
    assert "transient" in report_text.lower() and "same-principal" in report_text.lower()
    assert "not an extra Human Approval validity condition" in report_text
    audit = load(AUDIT+"result.json")
    assert audit["outcome"] == "INCONSISTENT"
    bound(audit["report"])
    invresult = load(INV+"result-revision-0002.json")
    bound(proposal["investigation_report"])
    bound(proposal["investigation_result"])
    for p in [APP+"attachments/application-tool.py",VER+"verifier.py"]:
        read(p)  # Inspection only. Neither upstream actor's executable is run.
    event("independent Review source reasoning and assurance adequacy completed",
          SOURCES+[PREP+"report.md",APP+"report.md",VER+"report.md"],
          outcome="PASS",basis="Direct affected-source/Master/coupled-control inspection and independently executed bound byte/state checks, not copying Verification conclusion")
    review_criteria = [
        ("R01","Current Review authorization and predecessor",
         "Exact fresh actual Human Review start follows separately authorized fresh Verification PASS. Correct Work ID/cycle/repository/five-file package. Failed prior verifier records remain unsuccessful history; no retroauthorization or competing-writer inference.",
         [OWN+"attempt.json",VER+"result.json",VER+"attempt.json"]),
        ("R02","Distinct actual reviewer and approved planned binding",
         "Reviewer 9b69bce7-c71e-487c-8893-23715797ad44 differs from preparer 4d0c3747-fde6-48c7-b125-5adb2af5b80c, applier ec7a8339-a9b5-4710-bb5b-a8760309005d, verifier 8e0bf478-bfeb-461b-90ed-64033f60f8d5 and excluded coordinating actor. Actual reviewer definition exactly matches approved planned binding; shared host/principal/title is not role proof.",
         [OWN+"attempt.json",PREP+"attachments/exact-proposal.json",".github/agents/independent-governance-review.agent.md"]),
        ("R03","Current qualification, native schema and record-first boundary",
         "Current reads/hash/Git/permission observations and native JSON required-field/positive-negative roundtrip tests establish capability. Complete actual invocation including 510-file hidden-inclusive input manifest validated while partial, flushed, atomically no-overwrite published in tool 1222 and independently fresh-process read back in 1223 before substantive Review. Common metadata and process-specific fields validated. Two unpublished helper schema assumptions corrected before any invocation publication; no replacement invocation.",
         [OWN+"attempt.json",OWN+"checkpoint-0001.json",OWN+"input-manifest.json"]),
        ("R04","Exact Human approval, one-time designation and Application authority",
         "Supplied actual exact approval/designation matches native Application authorization, complete package report/proposal/patch, all five replacements/fingerprints/byte contract/actors/route/exclusions. Separate Application start retained. Governance root freshly resolved; section 3 finding-led non-Master continuation, not reuse of initial bootstrap-stage authority. Approval/designation is not capability or stage-start; unavailable authenticated Human message IDs/times not invented.",
         [APP+"evidence/human-authorization.json",PREP+"report.md",APP+"attempt.json","docs/ai/sdlc/SDLC_GOVERNANCE.md"]),
        ("R05","Application completeness, scope and assurance ordering",
         "Application process-specific native outcome COMPLETED, not PASS; errors absent. Own qualification/readback and complete all-five preflight precede source writes in bound records and inspected helper control flow. Every after matches approved bytes; reverse/forward single-occurrence reconstruction and offsets reproduce all bases/afters and exact approved patch. No unapproved bytes or paths, rollback, product work or adoption.",
         [APP+"result.json",APP+"evidence/application-evidence.json",APP+"evidence/preflight.json",APP+"attachments/application-tool.py",PREP+"attachments/minimal.patch"]),
        ("R06","Fresh Verification evidence adequacy and currency",
         "Fresh verifier records contain common native metadata, distinct actual identity, approval bindings, qualified partial/publication/readback sequence, 13 supported PASS criteria, complete target/path/preservation checks and limits. Bound final report/result/evidence/checkpoints independently rehashed. All 500 verifier manifest inputs still match; additions are only its ten own outputs. Failed initial/replacement verifier attempts preserved, not current assurance. Review checks support adequacy without replacing designated Verification or rerunning its helper.",
         [VER+"attempt.json",VER+"checkpoint-0001.json",VER+"result.json",VER+"verification-evidence.json",VER+"verifier.py"]),
        ("R07","F003 coherent lifecycle-qualified initial clarification",
         "Update Guideline section 2 is normative and now admits identified immutable unapproved initial source only before first formal approval, with Analysis questions, explicit Human answers/decisions and explicit update request. Prompt inputs/paragraph, Request source/status/initial fields and Skill 3/4 consistently propagate it. Existing source-preservation/lineage under Artifact 8.4 and Update 7/14 remain. Result stays unapproved; Update 16, Skill 7/8 and Analysis 14/phases 5-10 still require subsequent Analysis, complete independent Verification, resolution and separate formal Human Requirement Approval. Already-approved changes retain approved-source route and section 8 non-finding controls. No fabricated Finding/approval or implementation authorization.",
         ["docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md","docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md","docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",".github/skills/requirement-update/SKILL.md","docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md","docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md"]),
        ("R08","F004 stage-specific actors without impossible future records",
         "Only enhancement Actor/Human Approval paragraph changes. Actual preparer has its own current attempt; intended applier needs fresh designation and qualifies in its own Application invocation before any source work. Future verifier/reviewer are planned definition/hash identities only until successful predecessor and fresh start, then actual matching definition and current qualification. Definition mismatch blocks for updated exact Human decision/approval. Four actor separation, applier coordinator exclusions and separate Audit start preserved. Matches unchanged Application Guideline/Prompt/Request and Master 3.5/33.1; does not make approval capability evidence. Enhancement-only form remains separate from this finding-led correction.",
         ["docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md","docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md","docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md","docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md","docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md"]),
        ("R09","Minimal approved policy, human authority and exclusions",
         "Selected directions were explicit separate Human decisions before proposal; exact approved amendment implements only those directions and existing controls. Four Update artifacts plus one Request paragraph are sufficient propagation; no Requirement Update Agent exists to change. No new stage, authority, artifact category, generic risk-acceptance gate, product Requirement/Plan or security boundary created. No fix, Audit, adoption, staging, commit, push or product execution.",
         [PREP+"report.md",PREP+"attachments/exact-proposal.json","docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md"]),
        ("R10","52-core and seven separately reported mechanism boundaries",
         "All three Masters remain byte-exact. No catalog membership, process/agent addition or separate mechanism is merged into the core count. 52 core and seven same-framework groups remain distinct: Governance Audit, Governance Remediation, Orchestration, Portability Assessment, Amendment Application, independent Verification, independent Review. This is scoped amendment Review, not seven-group/full-catalog Audit coverage.",
         ["docs/ai/sdlc/SDLC_GOVERNANCE.md","docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md","docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md"]),
        ("R11","Procedural non-mutation, full scope and publication contract",
         "All 474 pre-Application inputs checked: exactly five approved changed; other 469 unchanged. All 510 Review inputs including hidden .github and relied records unchanged through boundaries. Exact own file/partial exclusions only, no whole-root or other-actor exclusions. Git HEAD/branch/index/refs/staged/unstaged state preserved. Ordered actor-visible operations and errors retained. Writable tools/ACLs are disclosed, no write probes or source writes. Exact proposal discloses transient/same-principal residual risks and this Review retains them without adding an approval-validity gate.",
         [OWN+"attempt.json",OWN+"input-manifest.json",APP+"evidence/input-manifest.json",PREP+"report.md"]),
        ("R12","Effectiveness and next separate complete Audit gate",
         "Non-Master changes require approved exact Application, independent Verification and Review PASS plus complete Audit CONSISTENT with every required count zero and all seven groups without unresolved issue before effectiveness. Review cannot declare effectiveness or close findings. Latest complete Audit remains INCONSISTENT with two Medium findings, ambiguity 1 and unsupported control 1; other counts zero. Candidate Masters/product root remain unadopted. No prior resolved finding reopened. Only separate fresh Human-started complete Audit may follow; Master adoption, if later pursued, is a distinct Human decision.",
         ["docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md","docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md",AUDIT+"result.json"])
    ]
    criteria = [dict(id=i,criterion=t,outcome="PASS",reasoning=why,refs=[ref(p) for p in paths])
                for i,t,why,paths in review_criteria]
    post = compare(a["input_manifest"],snapshot())
    c = common("checkpoint")
    c.update(sequence=2,last_confirmed_boundary="Substantive independent five-file Review completed; current inputs rechecked",
             repository_effects="Own records/helper only; no evaluated source/upstream/history mutations",
             unfinished_work=["Final snapshot comparison and immutable evidence/report/result publication"],
             observed_evidence=dict(pre_comparison=pre,post_comparison=post,criteria=criteria,
                  targets=targets,patch=dict(bytes=len(patch),sha256=sha(patch),approved_patch_equal=True),
                  sources=source_refs,upstream_bindings=refs,
                  application_preservation=dict(original_count=474,unchanged_count=469,exact_changed_paths=sorted(changed)),
                  verification_currency=dict(original_count=len(vm_paths),all_unchanged=True,only_added_paths=added_since_ver_snapshot),
                  verification_criteria_count=len(ve["criteria"]),latest_audit=dict(result=ref(AUDIT+"result.json"),outcome=audit["outcome"],counts=audit["counts"]),
                  actual_roles=dict(reviewer=ACTOR,preparer=a["runtime"]["preparer"],applier=a["runtime"]["applier"],verifier=a["runtime"]["verifier"]),
                  helper=ref(OWN+"reviewer.py"),events=list(EVENTS),
                  direct_inspection="Current affected five sources, coupled Analysis/Application controls, applicable Masters, exact proposal/approval/Application and fresh Verification reports/records; upstream helpers inspected only, never executed",
                  source_tool_observations=[
                    "After 1223 fresh readback: parallel view calls read five affected sources, exact patch and report ranges; large reads continued by exact ranges",
                    "One invalid patch range 151..300 exceeded its 108 lines; corrected read 86..108; no write or missing evidence",
                    "Master Governance 3/24; Artifact 3.2-3.5/8.4/33.1; Traceability 8/30.1/42; Analysis 14 and phases 5-10 directly read",
                    "Application Guideline/Prompt/Request, Verification Guideline/Skill, Corrective Prompt and actual proposal/application/verification report criteria directly read",
                    "1224..1226 Python native read-only evidence-shape/authority/Audit-state inspection",
                    "rg and exact view ranges inspected Application helper readback/preflight/apply control flow and fresh Verifier validator/partial/publish/readback; no upstream code execution",
                    "Current helper invoked for independent Review checks and snapshot boundaries; full argument identity bound by helper fingerprint"
                  ]),
             blockers=[],pending_gates=["Separate fresh Human complete Governance Audit initiation"],
             safe_continuation_prerequisites="All evaluated inputs unchanged immediately before final publications; remain within exact own output scope")
    cr = publish("checkpoint-0002.json",c)
    print(json.dumps(dict(outcome="PASS",criteria=len(criteria),evaluated_inputs=len(a["input_manifest"]["files"]),
                          original_application_inputs=len(original),unchanged_non_targets=469,checkpoint=cr),indent=2))

def final():
    selftests()
    a = load(OWN+"attempt.json")
    validate(a)
    c = load(OWN+"checkpoint-0002.json")
    validate(c)
    assessment = c["observed_evidence"]
    assert all(x["outcome"] == "PASS" for x in assessment["criteria"]) and not c["blockers"]
    comparison = compare(a["input_manifest"],snapshot())
    cf = common("checkpoint")
    cf.update(sequence=3,last_confirmed_boundary="Final complete 510-input content/path-set/Git comparison immediately before success publication",
              repository_effects="Only exact own records/helper; no source/upstream/history effects",
              unfinished_work=["Own final evidence/report/result publication and fresh-process readback"],
              observed_evidence=dict(comparison=comparison,assessment=ref(OWN+"checkpoint-0002.json"),
                    invocation=ref(OWN+"attempt.json"),helper=ref(OWN+"reviewer.py"),events=list(EVENTS)),
              blockers=[],pending_gates=["Separate complete Governance Audit start"],
              safe_continuation_prerequisites="Final records immutable, own scope only; no downstream stage")
    cfr = publish("checkpoint-final.json",cf)
    e = common("review_evidence")
    e.update(outcome="PASS",criteria=assessment["criteria"],input_manifest=ref(OWN+"input-manifest.json"),
             checkpoints=[ref(OWN+"checkpoint-0001.json"),ref(OWN+"checkpoint-0002.json"),cfr],
             invocation=ref(OWN+"attempt.json"),exact_evaluated_state=dict(targets=assessment["targets"],
                    repository=a["repository"],input_count=len(a["input_manifest"]["files"])),
             assessment=assessment,authorization=a["authorization"],runtime=a["runtime"],capabilities=a["capabilities"],
             assurance_mode="procedural non-mutation",concurrency=a["runtime"]["concurrency"],
             operations=dict(prequalification=a["operations"],invocation_publication="1222 success and 1223 independent fresh-process readback before substantive work",
                    assessment_checkpoint=ref(OWN+"checkpoint-0002.json"),final_events=list(EVENTS),
                    publication_events="Own partial/fsync/native validation/atomic no-overwrite/fresh readback is observed in helper and tool sequence; final independent readback is separate tool output, not a fabricated earlier timestamp"),
             limitations=LIMITS,unresolved_review_findings=[],blockers=[],originating_findings="GOV-AUD-20261102-003 and GOV-AUD-20261102-004 accepted; not closed pending full Audit",
             next_permitted_process="Complete Governance Audit only after separate fresh Human initiation",
             source_writes=False,other_actor_record_writes=False,audit_run=False,effectiveness_claimed=False,
             master_adopted=False,product_root_adopted=False,staging_commit_push=False,downstream_started=False)
    compare(a["input_manifest"],snapshot())
    er = publish("review-evidence.json",e)
    lines = [
        "# Independent Governance Review Report", "",
        "**Outcome: PASS — procedural non-mutation assurance.**",
        "**Scope: approved five-file amendment GOV-AUD-20261102-003 and GOV-AUD-20261102-004 and its fresh passing independent Verification only.**", "",
        f"Canonical identity: `{ATTEMPT}:review_report`.",
        f"Work ID: `{WORK}`; Cycle `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1; attempt `{ATTEMPT}`.",
        f"Repository `ScalableParimal/SupportIQ`, `{ROOT}`; HEAD `{a['repository']['head']}`; branch `{a['repository']['branch']}`.",
        "Product Requirement / Implementation Plan: N/A. No product content or behavior assessed.",
        "This report is Independent Governance Review, not approval, Application, a substitute Verification, a complete Governance Audit, finding closure, effectiveness or baseline adoption.", "",
        "## 1. Actual authorization, independent identity and qualification", "",
        "Actual fresh Human Review stage-start (exact ASCII wording):", "'"+START+"'", "",
        "Actual exact Human approval/designation:", "'"+APPROVAL+"'", "",
        "Actual separate Application start:", "'"+APPSTART+"'", "",
        "Actual fresh valid Verification retry start:", "'"+VERSTART+"'", "",
        "Source is the actual current user-supplied parent-conversation decisions and stage start. Authenticated message/author IDs and original decision times are unavailable and not invented. Exact quotes preserve ASCII punctuation. No approval is inferred from hashes, starts or policy direction, and no additional residual-risk acknowledgement gate is imposed.",
        "Root adoption was freshly resolved through canonical OWNER comment https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236 (author ScalableParimal, user 226102895; created/updated 2026-10-30T12:31:51Z). Repository/HEAD/Work ID/root and all three Master fingerprints match. The initial bootstrap Audit stage is not reused; Governance section 3 finding-led non-Master continuation plus current Human starts and exact approval governs. Product root and candidate Master baseline remain unadopted.", "",
        f"Current reviewer harness identity `{ACTOR}`, Copilot invocation `{a['runtime']['copilot_agent_session_id']}`, effective principal `int-scl-010\\parimal`, host `{a['runtime']['host_session']}`.",
        "Current developer-assigned reviewer role plus registry attribution establishes this invocation's identity, not a shared session title or an external authenticity guarantee. Distinct from preparer `4d0c3747-fde6-48c7-b125-5adb2af5b80c`, applier `ec7a8339-a9b5-4710-bb5b-a8760309005d`, verifier `8e0bf478-bfeb-461b-90ed-64033f60f8d5`, and excluded coordinating actor `bbd899a3-3c5f-444e-9d88-5df37ef2d3d6`. This reviewer is not active Remediation or Orchestrator.",
        "Actual reviewer `.github/agents/independent-governance-review.agent.md` equals approved planned SHA-256 `1CD8CCC4A96EFA64D4AA3B64DDDB2874F2337A45301B6B953033FC9016A9812E`. Four approved definition paths and fingerprints remain distinct.", "",
        "Current runtime capability is evidenced by successful input reads, SHA-256 computations, non-mutating Git path/status/index/ref/HEAD/diff checks, per-input effective access/attributes, and native JSON complete-object positive/negative selftests. Current whoami/Get-Acl observed owner INT-SCL-010\\Parimal, Users ReadAndExecute, Authenticated Users inherited Modify, Administrators/SYSTEM FullControl. Write-capable tools and writable ACLs confer no source-write authority; no write probe was made.",
        "Own publication used strict native actual-object metadata/identity/reference/type checks, serialize/parse equality, validated UTF-8 .partial, flush/fsync, same-directory Windows atomic rename without overwrite, and fresh readback. The invocation including full hidden-inclusive manifest was published by tool 1222 and independently re-opened in fresh process 1223 before substantive assessment. Two Application-schema assumptions failed only in unpublished preflight; corrected to exact application_result / Governance Amendment Application / COMPLETED without weakening checks. No malformed final invocation or replacement invocation was published.",
        f"Invocation: `{OWN}attempt.json`, {ref(OWN+'attempt.json')['bytes']} bytes, SHA-256 `{ref(OWN+'attempt.json')['sha256']}`.",
        f"Independent record-first boundary: `{OWN}checkpoint-0001.json`, SHA-256 `{ref(OWN+'checkpoint-0001.json')['sha256']}`.", "",
        "## 2. Current predecessor, exact approved state and independent evidence", "",
        "The current governing predecessor is fresh Verification `20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216`: execution COMPLETED, outcome PASS. Initial incomplete invocation and unauthorized replacement `20261102T152557Z-efc37bf9-a1dd-4f02-b768-d797e0636818` remain preserved unsuccessful history, not valid assurance; no retroauthorization, reopening or live-writer inference. Canonical Investigation revision 0002 bindings are used, not older invalid bundles.",
        "Application's native process-specific result is COMPLETED, not a blanket PASS. Bound qualification/readback/all-five preflight, exact approval and target/actor/route bindings, per-target operations, preservation evidence and terminal records were inspected. Application and Verification helper control flows were inspected as source, never executed. Their procedural record ordering does not constitute a trusted exhaustive OS write trace.",
        "This Review independently inspected actual affected text and coupled controls and recalculated bound target/patch/current-state identities to assess governance coherence and assurance adequacy. It did not merely repeat the verifier conclusion or replace designated Verification.", "",
        "| Approved after target | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for t in assessment["targets"]:
        r=t["after"]
        lines.append(f"| `{t['path']}` | {r['bytes']} | `{r['sha256']}` |")
    lines += ["", "All five actual afters match the exact approved proposal. Reverse reconstruction recovers every approved base; forward single-occurrence byte replacements and sequential offsets recover complete afters. Native combined unified diff equals the approved patch. UTF-8 without BOM, CRLF and final-newline states preserved: first four no final newline, fifth yes. All other bytes preserved.", "",
              "### Canonical upstream bindings", "",
              "| Record | Bytes | SHA-256 |", "|---|---:|---|"]
    for p in [PREP+"report.md",PREP+"result.json",PREP+"attachments/exact-proposal.json",PREP+"attachments/minimal.patch",
              APP+"report.md",APP+"result.json",APP+"evidence/application-evidence.json",APP+"checkpoint-0002.json",
              VER+"report.md",VER+"result.json",VER+"verification-evidence.json",
              INV+"report-revision-0002.md",INV+"result-revision-0002.json"]:
        r=ref(p)
        lines.append(f"| `{p}` | {r['bytes']} | `{r['sha256']}` |")
    lines += ["", "## 3. Independent criterion-by-criterion Review", ""]
    for criterion in assessment["criteria"]:
        lines += ["### "+criterion["id"]+" — "+criterion["criterion"]+": PASS", "",
                  criterion["reasoning"], "",
                  "Evidence: "+"; ".join("`"+r["path"]+"` (SHA-256 `"+r["sha256"]+"`)" for r in criterion["refs"])+".", ""]
    lines += [
        "## 4. Evaluated-input scope, operation evidence and preservation", "",
        f"The input manifest binds **{len(a['input_manifest']['files'])}** filesystem inputs, hidden-inclusive including `.github`, all current relied sources, approval/proposal/Application/Verification/Investigation/Audit and pre-existing history. Exact presence/path sets, tracked/untracked state, byte counts/SHA-256 and per-file access/readonly attributes are recorded. Expected absences include AGENTS.md, .github/copilot-instructions.md and product records root. .git internals are not represented as a file inventory; index, refs, HEAD/branch/status and full staged/unstaged diff identities are separately bound.",
        "Only this actor's exact designated own output filenames and corresponding partials are excluded, never a whole records root or any other actor's attempt. Inventory/hash coverage is not a claim that every file received substantive governance assessment.",
        "All 474 pre-Application inputs were checked: only the five approved targets changed, other 469 unchanged, none removed. All 500 verifier-snapshot inputs still match; the only ten additions are its own completed outputs. All 510 Review inputs remain unchanged at fresh invocation readback, preassessment, post-assessment and final prepublication boundaries. No additions/removals/renames or unexplained index/worktree drift. Current pre-existing modifications and all historical records retained.",
        "Ordered actor-visible evidence records current identity/tools/arguments or integrity-bound safe representations, observable read paths, outcomes/errors, helper events and publication/readback boundaries. A corrected out-of-range view request and two unpublished preflight schema errors are disclosed, not hidden. Meaningful checkpoints bind the actual before/after input state and safe continuation; not every tool call is a separate checkpoint. UTC record creation is preparation time, not an exact publication timestamp.", "",
        "## 5. Material limitations and residual risks", "",
    ]
    lines += ["- "+x for x in LIMITS]
    lines += ["",
        "Exact approved proposal section 7/8 discloses these material residual risks and this report/evidence retains them. There is no exhaustive trusted OS event stream, enforced source-write exclusion, independent tamper monitor or guaranteed security. Only this reviewer was running in the observed registry; idle/stale prior metadata is not evidence of live writers. No exclusive no-edit interval is guaranteed and external writers cannot be excluded. Matching endpoints show the bytes observed, not a continuous write-free history.", "",
        "## 6. Completion, canonical outputs and safe stop", "",
        "**All 12 Review criteria PASS; no unresolved Review finding or required-evidence blocker remains for this scope.**",
        "GOV-AUD-20261102-003 and GOV-AUD-20261102-004 remain accepted/not closed pending the separate complete Audit. Prior resolved findings are not reopened. Latest complete Audit remains reported INCONSISTENT: Critical 0, High 0, Medium 2, Low 0, Ambiguities 1, Missing Governance Controls 0, Unsupported Governance Controls 1, Broken References 0. No new Audit was run or claimed.",
        "Non-Master amendment effectiveness still requires full Audit CONSISTENT, every required count zero, and all seven separate groups assessed without unresolved issue. Passing Review does not declare effectiveness or adopt Masters/product root. Any later Master-baseline adoption requires its separate explicit Human decision after applicable gates.",
        f"Canonical evidence: `{er['path']}`, {er['bytes']} bytes, SHA-256 `{er['sha256']}`.",
        f"Input manifest: `{OWN}input-manifest.json`, SHA-256 `{ref(OWN+'input-manifest.json')['sha256']}`.",
        f"Substantive boundary: `{OWN}checkpoint-0002.json`, SHA-256 `{ref(OWN+'checkpoint-0002.json')['sha256']}`.",
        f"Final boundary: `{cfr['path']}`, SHA-256 `{cfr['sha256']}`.",
        f"Terminal result: `{OWN}result.json`, published after this report/evidence and binding their actual bytes. This earlier report does not claim its own or its later result's future fingerprint.",
        "**Next permitted process: separately Human-initiated complete Governance Audit of the full current 52-core catalog, current applicable source set and all seven mechanism groups. This report does not start it.**",
        "No source/upstream/history correction, approval, Audit, adoption, staging, commit, push or product work. Only this reviewer-owned attempt's records/helper were created. **STOP.**", ""
    ]
    text = "\n".join(lines)
    compare(a["input_manifest"],snapshot())
    rr = publish("report.md",text)
    r = common("result")
    r.update(execution_status="COMPLETED",outcome="PASS",report=rr,evidence=er,
             invocation=ref(OWN+"attempt.json"),invocation_readback=ref(OWN+"checkpoint-0001.json"),
             input_manifest=ref(OWN+"input-manifest.json"),assessment_checkpoint=ref(OWN+"checkpoint-0002.json"),
             final_checkpoint=cfr,exact_evaluated_state=e["exact_evaluated_state"],
             criteria=assessment["criteria"],unresolved_items=[],blockers=[],
             originating_findings=dict(ids=["GOV-AUD-20261102-003","GOV-AUD-20261102-004"],
                                       disposition="Accepted; not closed pending full Audit"),
             latest_audit_reported_state=assessment["latest_audit"],assurance_mode="procedural non-mutation",
             limitations=LIMITS,next_permitted_process="Complete Governance Audit only after separate fresh Human stage-start",
             next_gate="Human reviews this handoff and separately initiates full Audit; not started",
             final_input_comparison=compare(a["input_manifest"],snapshot()),
             helper=ref(OWN+"reviewer.py"),operations_before_result=list(EVENTS),
             downstream_started=False,audit_run=False,effectiveness_claimed=False,findings_closed=False,
             master_adopted=False,product_root_adopted=False,source_writes=False,other_actor_record_writes=False,
             staging_commit_push=False,publication_time="Exact publication timestamp not captured; ordered events and fresh readback establish sequence, not exact instant")
    resultref = publish("result.json",r)
    print(json.dumps(dict(outcome="PASS",report=rr,result=resultref,evidence=er,next="Separate fresh-process final readback; then STOP, no Audit"),indent=2))

def final_readback():
    selftests()
    a = load(OWN+"attempt.json")
    validate(a)
    r = load(OWN+"result.json")
    validate(r)
    for k in ["report","evidence","invocation","invocation_readback","input_manifest","assessment_checkpoint","final_checkpoint"]:
        bound(r[k])
    evidence = load(r["evidence"]["path"])
    validate(evidence)
    assert r["criteria"] == evidence["criteria"] and r["outcome"] == evidence["outcome"] == "PASS"
    assert not r["downstream_started"] and not r["audit_run"] and not r["effectiveness_claimed"]
    comparison = compare(a["input_manifest"],snapshot())
    for n in OUTPUT_NAMES:
        assert not (ROOT/(OWN+n+".partial")).exists()
    print(json.dumps(dict(independent_fresh_process_final_readback="PASS",outcome=r["outcome"],
                          report=ref(r["report"]["path"]),result=ref(OWN+"result.json"),evidence=ref(r["evidence"]["path"]),
                          inputs_unchanged=comparison["file_count"],helper=ref(OWN+"reviewer.py"),
                          next_permitted_process=r["next_permitted_process"],downstream_started=False),indent=2))

if __name__ == "__main__":
    os.chdir(ROOT)
    sys.stdout.reconfigure(encoding="utf-8")
    {"prepare":prepare,"readback":readback,"assess":assess,"final":final,"final-readback":final_readback}[sys.argv[1]]()
