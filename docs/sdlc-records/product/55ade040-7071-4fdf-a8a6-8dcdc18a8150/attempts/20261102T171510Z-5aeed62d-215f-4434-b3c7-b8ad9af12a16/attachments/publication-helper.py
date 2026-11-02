"""Administrative record publication only; never imports or executes project code."""
import datetime, hashlib, json, os, pathlib, re, subprocess, sys, uuid

ROOT = pathlib.Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
WORK = "55ade040-7071-4fdf-a8a6-8dcdc18a8150"
# Allocation timestamp is contextual, not a publication timestamp.
ATTEMPT = "20261102T171510Z-5aeed62d-215f-4434-b3c7-b8ad9af12a16"
BASE = ROOT / "docs/sdlc-records/product" / WORK / "attempts" / ATTEMPT
HEAD = "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
BRANCH = "sdlc-framework-onboarding"
AUDIT = ROOT / "docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T160240Z-5022506a-f881-4681-af13-e4acf3bb6935"
CLOSURE = AUDIT.parent / "20261102T162238Z-28a7c86b-114f-4d7f-8520-f09000a0df40"
MASTER_HASHES = {
    "SDLC_GOVERNANCE.md": "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
    "SDLC_ARTIFACT_GOVERNANCE.md": "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
    "SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C",
}
START = "Yes, initiate only the initial SupportIQ SDLC Portability Assessment under the exact read/publication scope and Work ID above"
EXCLUSIONS = [
    "Credentials, private keys, live secret-bearing .env files, user/customer datasets",
    "Unrelated repositories, dependency/build caches; no project scripts, builds, tests, workflows, runtime",
    ".git object/index contents not dumped; only bounded nonmutating Git metadata checks",
    "Historical governance records except explicitly referenced adoption/Audit/closure applicability metadata",
]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, text=True).strip()

def ref(p, record_id=None):
    p = pathlib.Path(p)
    if not p.is_absolute():
        p = ROOT / p
    data = p.read_bytes()
    r = {"path": p.relative_to(ROOT).as_posix(), "bytes": len(data),
         "sha256": hashlib.sha256(data).hexdigest().upper()}
    if record_id:
        r["record_id"] = record_id
    return r

def reject_duplicates(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("Duplicate JSON key: " + k)
        out[k] = v
    return out

def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8-sig"),
                      object_pairs_hook=reject_duplicates,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def validate(obj):
    assert type(obj) is dict
    required = ["schema_version", "record_type", "record_id", "feature", "work_id",
                "attempt_id", "process", "creator", "created_at_utc", "clock_basis",
                "gate", "related_records", "task_context"]
    assert all(k in obj for k in required)
    assert obj["schema_version"] == "1.0"
    assert obj["work_id"] == WORK and obj["attempt_id"] == ATTEMPT
    assert obj["process"] == "SDLC Portability Assessment"
    assert obj["creator"]["role"] == "SDLC Portability Assessment"
    assert obj["record_id"].startswith(ATTEMPT + ":")
    assert obj["creator"]["identity"] and obj["created_at_utc"].endswith("+00:00")
    assert type(obj["related_records"]) is list and type(obj["gate"]) is dict
    if obj["record_type"] == "invocation":
        for key in ["requested_scope", "input_references", "repository_context",
                    "authorization", "predecessor", "output_location", "qualification",
                    "source_inventory", "target_inventory", "publication"]:
            assert key in obj
        assert obj["authorization"]["fresh_start"]["wording"] == START
        assert obj["output_location"] == BASE.relative_to(ROOT).as_posix()
        assert len(obj["source_inventory"]) == 76
        assert obj["qualification"]["prior_governance_applicability"]["source_comparison"] == "PASS"
    if obj["record_type"] == "result":
        for key in ["execution_status", "outcome", "report", "evidence", "invocation",
                    "evaluated_state", "unresolved_items", "next_permitted_process"]:
            assert key in obj
        for key in ["report", "evidence", "invocation"]:
            check_ref(obj[key])

def check_ref(r):
    a = ref(r["path"])
    assert a["sha256"] == r["sha256"] and a["bytes"] == r["bytes"], r["path"]

def publish(name, obj):
    """Windows same-filesystem rename refuses replacement; no os.replace."""
    dst = BASE / name
    assert dst.resolve().is_relative_to(BASE.resolve())
    assert not dst.exists(), str(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    partial = pathlib.Path(str(dst) + ".partial")
    assert not partial.exists(), str(partial)
    if isinstance(obj, dict):
        validate(obj)
        data = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
        roundtrip = json.loads(data, object_pairs_hook=reject_duplicates)
        assert roundtrip == obj
    else:
        assert isinstance(obj, str)
        data = obj.encode("utf-8")
    with partial.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == data
    if isinstance(obj, dict):
        validate(load(partial))
        assert load(partial) == obj
    os.rename(partial, dst)
    assert dst.read_bytes() == data
    if isinstance(obj, dict):
        validate(load(dst))
    return ref(dst, obj["record_id"] if isinstance(obj, dict) else ATTEMPT + ":report")

def common(kind, creator):
    return dict(schema_version="1.0", record_type=kind, record_id=ATTEMPT + ":" + kind,
                feature="Initial SupportIQ SDLC portability assessment", work_id=WORK,
                attempt_id=ATTEMPT, process="SDLC Portability Assessment", creator=creator,
                created_at_utc=now(),
                clock_basis="Python timezone-aware local system UTC sampled at record preparation; not exact publication time",
                gate={"applicability": "No formal product approval or acceptance gate is created or satisfied"},
                related_records=[], task_context="Initial assessment; no approved Requirement, Plan, or Plan-local task")

def source_paths():
    return sorted([p for folder in [ROOT/".github", ROOT/"docs/ai"]
                   for p in folder.rglob("*") if p.is_file()],
                  key=lambda p: p.relative_to(ROOT).as_posix())

def qualify():
    assert os.name == "nt", "No-overwrite rename semantics qualified for this Windows invocation only"
    assert git("rev-parse", "HEAD") == HEAD and git("branch", "--show-current") == BRANCH
    assert git("remote", "get-url", "origin") == "https://github.com/ScalableParimal/SupportIQ.git"
    # Own unpublished preparation directory does not constitute a reservation.
    own_work = BASE.parents[1]
    assert own_work.name == WORK
    assert not (ROOT/"docs/sdlc-records/governance"/WORK).exists()
    existing = [p for p in own_work.rglob("*") if p.is_file()]
    assert existing == [BASE/"attachments/publication-helper.py.partial"], existing
    collisions = []
    for root in [ROOT/"docs/sdlc-records/governance", ROOT/"docs/sdlc-records/product"]:
        if not root.exists():
            continue
        for p in root.rglob("*.json"):
            if p.is_relative_to(own_work):
                continue
            # Collision discovery is a bounded identity-field search, not validation
            # or reuse of unrelated historical records (some are malformed).
            text = p.read_text(encoding="utf-8-sig")
            identities = re.findall(r'"(?:work_id|feature|feature_id)"\s*:\s*"([^"]*)"', text)
            if WORK in identities:
                collisions.append(p.relative_to(ROOT).as_posix())
        for p in root.rglob(WORK):
            if p != own_work:
                collisions.append(p.relative_to(ROOT).as_posix())
    assert not collisions, collisions
    for name, sha in MASTER_HASHES.items():
        assert ref(ROOT/"docs/ai/sdlc"/name)["sha256"] == sha
    expected = [
        (AUDIT/"report.md", 122315, "C72AF2A1761610365C36A249E8892B08C7A23BA2D9A7C1F47749C3BFEC796256"),
        (AUDIT/"result.json", 37941, "CF073B8E08EDF728B6AB1B1CC300C842D3FEF15F512A084C85B7A7E8EF199222"),
        (AUDIT/"evidence/audit-evidence.json", 550499, "9F0519457976E8D57E5C9F5A7C9DFFD7D03E5492529032D836F2FEAD66F00DF1"),
        (CLOSURE/"report.md", None, "B2C36B498F36A25A216498F072C401B90252E2030C58A0D3B69D4D76F959E68B"),
        (CLOSURE/"result.json", None, "8B0F4D67996B33CAAF35F43D3A86948C165A695C3D94A99213D99479489CD5A1"),
        (CLOSURE/"evidence/closure-evidence.json", None, "1A17EBF714DAFECF40CF5DAAB1D0758DD51DB208262A436B6C8E8CB4F71BAA46"),
    ]
    historical = []
    for p, size, sha in expected:
        r = ref(p)
        assert r["sha256"] == sha and (size is None or r["bytes"] == size), r
        historical.append(r)
    audit = load(AUDIT/"result.json")
    closure = load(CLOSURE/"result.json")
    assert audit["outcome"] == "CONSISTENT" and all(v == 0 for v in audit["counts"].values())
    assert len(audit["mechanisms"]) == 7 and not audit["findings"]
    assert closure["outcome"] == "COMPLETE" and not closure["findings"]
    for j in [audit, closure]:
        for k in ["report", "evidence", "input_manifest"]:
            check_ref(j[k])
    manifest = load(ROOT/audit["input_manifest"]["path"])
    sources = [ref(p) for p in source_paths()]
    old_sources = [r for r in manifest["files"]
                   if r["path"].startswith((".github/", "docs/ai/"))]
    assert len(sources) == 76 and {r["path"]: r for r in sources} == {r["path"]: r for r in old_sources}, "Current governance sources differ from adopted Audit state"
    targets = [ref(ROOT/"README.md"), ref(ROOT/"docs/requirement/SupportIQ_Product_Requirements_Document.docx")]
    creator = {
        "identity": "portability-invocation-" + str(uuid.uuid4()),
        "role": "SDLC Portability Assessment",
        "identity_basis": "Current explicit developer role, user-scoped invocation, exact on-disk Agent/Skill/Guideline/Prompt/Request loaded; invocation UUID is local attribution, not an external platform identity",
        "harness_session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
        "harness_evidence": "get_current_session returned this session and canonical SupportIQ working directory; its title is not role proof",
        "effective_os_identity": subprocess.check_output(["whoami"], text=True).strip(),
        "external_cryptographic_actor_identity": "Not available; not claimed",
    }
    inv = common("invocation", creator)
    inv.update(
        execution_status="invocation_prepared",
        trigger={"type": "initial", "reason": "Before first product SDLC activity; governance bootstrap/evaluations were not completed portability assessments", "prior_completed_assessment_reuse": "None"},
        requested_scope={
            "read": "Static governance/customizations and relevant target source, architecture/requirements docs, dependency manifests, configuration TEMPLATES, test/CI/deployment DEFINITIONS and Git metadata in this exact repository; includes hidden .github",
            "exclusions": EXCLUSIONS, "execution": "No project/runtime activity; nonmutating administrative filesystem/hash/Git checks and own-record publication only",
            "write": BASE.relative_to(ROOT).as_posix(), "dimensions": list(range(1,9)),
            "other_agents_or_stages": "Not authorized"},
        repository_context={
            "source": {"repository": "ScalableParimal/SupportIQ", "root": str(ROOT), "head": HEAD, "branch": BRANCH, "state": "HEAD plus source_inventory working-tree bytes"},
            "target": {"repository": "ScalableParimal/SupportIQ", "root": str(ROOT), "head": HEAD, "branch": BRANCH, "state": "HEAD plus target_inventory and applicable governance source_inventory"},
            "git_status": git("status", "--short", "--untracked-files=normal"),
            "worktrees": git("worktree", "list", "--porcelain"),
            "centralized_multi_root_route": "NOT APPLICABLE; repository-local consumption"},
        input_references={"source_manifest_location": "Embedded source_inventory", "target_manifest_location": "Embedded target_inventory", "request_template": ref(ROOT/"docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md"), "execution_request": "Current user message supplies filled executable request without modifying draft template"},
        source_inventory=sources, target_inventory=targets,
        authorization={
            "fresh_start": {"wording": START, "source": "Current caller/user conversation message", "attribution": "User-supplied fresh Human start; no independently fetched platform author ID or native timestamp for this conversational start", "scope": "Only initial assessment, exact read/publication scope and Work ID in this invocation", "native_platform_time": "Unavailable; user message displays 2026-11-02T22:40:01.302+05:30 as contextual current_datetime, not claimed as native start event time"},
            "master_adoption": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6583261503", "comment_id": 6583261503, "author": "ScalableParimal", "user_id": 226102895, "association": "OWNER", "created_at": "2026-11-02T17:06:37Z", "updated_at": "2026-11-02T17:06:37Z", "resolution": "Independently fetched in current invocation using GitHub MCP issue_read get_comments; exact body retained in subsequent own evidence", "baseline": "SupportIQ-Master-Baseline-001", "masters": MASTER_HASHES},
            "product_root_adoption": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6583299245", "comment_id": 6583299245, "author": "ScalableParimal", "user_id": 226102895, "association": "OWNER", "created_at": "2026-11-02T17:08:13Z", "updated_at": "2026-11-02T17:08:13Z", "root": "docs/sdlc-records/product/", "resolution": "Independently fetched in current invocation using GitHub MCP issue_read get_comments; exact body retained in subsequent own evidence"},
            "blocker_decision_authority": "Parimal Shere / ScalableParimal, repository OWNER",
            "blocker_dispositions": "None supplied; pending future Human decisions"},
        predecessor={"product_process": "NOT APPLICABLE; initial assessment", "governance_prerequisites": historical},
        output_location=BASE.relative_to(ROOT).as_posix(),
        qualification={
            "source_selection": "Exact repository-local five assessment artifacts plus three Masters read; loaded portability-assessment Skill; these active instructions govern the current invocation",
            "current_capabilities": {"read": "Successful actual Agent/Skill/Guideline/Prompt/Request/Master and Git metadata reads", "hash_json": "Successful SHA-256 and strict native JSON metadata decoding with Python", "external_decisions": "GitHub MCP issue_read resolved both new decisions with matching native metadata", "publication_route": "Windows filesystem, existing root ACL observed: Authenticated Users Modify; current OS identity observed; own .partial helper preparation succeeded. Final record route tested by this validated no-overwrite publication and independent fresh readback before assessment", "boundaries": "Procedural scope checks and exact output path assertions; NOT enforced sandbox or proof against same-principal tampering"},
            "prior_governance_applicability": {"source_comparison": "PASS", "sources": len(sources), "audit_manifest": ref(ROOT/audit["input_manifest"]["path"]), "audit_outcome": audit["outcome"], "counts": audit["counts"], "mechanism_count": len(audit["mechanisms"]), "closure_outcome": closure["outcome"], "validated_references": historical, "limits": "Reused only governance prerequisite applicability, not portability or runtime capability. Not a new Governance Audit. Earlier runtime N/A is not current capability proof"},
            "work_id_collision_check": {"matching_other_records": collisions, "both_roots_checked": True, "own_partial_helper": "Unpublished preparation only, no earlier reservation", "reservation": "This first no-overwrite attempt.json reserves Work ID"},
            "concurrency": "No existing product Work ID path before own preparation; no conflicting same-work invocation record found across both roots. Historical in_progress is not liveness; current harness session identity not a competitor. Read-only target assessment and unique output scope; no global writer exclusion or exhaustive OS event log claimed",
            "role_independence": "No independent verification/review role or prior-actor identity claimed; current role limited to initial advisory assessment",
        },
        publication={"contract": "UTF-8 strict complete JSON; full-object roundtrip/schema/field/binding validation in .partial; flush/fsync; same-filesystem Windows atomic rename with no replacement; fresh readback in a later tool call required before substantive assessment", "publication_time": "Exact filesystem publication timestamp not captured or inferred", "ordering": "Qualification only before this invocation; substantive assessment follows successful independent fresh readback"},
        limitations=["Nonmutation is procedural, not an enforced sandbox", "Endpoint hashes cannot exclude transient or same-principal tampering", "No exhaustive OS event log or cryptographic external actor proof", "Local uncommitted records are not remote backup; no commit/push authorized"],
    )
    result = publish("attempt.json", inv)
    print(json.dumps({"invocation": result, "source_count": len(sources), "target_count": len(targets), "qualification": "PASS; fresh independent readback still required"}, indent=2))

if __name__ == "__main__":
    assert sys.argv[1:] == ["qualify"]
    qualify()
