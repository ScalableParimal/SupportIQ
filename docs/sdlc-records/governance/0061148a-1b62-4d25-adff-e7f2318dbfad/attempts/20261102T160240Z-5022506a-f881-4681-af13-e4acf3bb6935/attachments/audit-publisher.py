"""Actor-owned Audit preparation/publication helper; never writes its inputs."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
AID = "20261102T160240Z-5022506a-f881-4681-af13-e4acf3bb6935"
ROLE = "SDLC Governance Audit"
ACTOR = "f39a6108-fbf1-47b2-b95a-8267a3f07530"
BASE = ROOT / "docs/sdlc-records/governance" / WORK / "attempts"
OWN = BASE / AID
START = "Yes, initiate the complete Governance Audit under the existing Work ID and Cycle 1 using the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 Application and fresh Verification PASS and Review PASS"
IDS = {
    "proposal": "20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d",
    "application": "20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494",
    "verification": "20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216",
    "review": "20261102T154422Z-cdfe6363-b6ac-42d2-8896-979df6f5d322",
}
EXPECTED = {
    "proposal/report.md": (39577, "A925ECCE1D7593DE1955EC0CA416A1BDFD1AA67A5B1800129BF8FA3C1B685677"),
    "proposal/result.json": (11450, "A4BEE48991E0CA74D414BDDA1957220F0703E1FEF7F62AE50536E9EDB6A725ED"),
    "proposal/attachments/exact-proposal.json": (21495, "086D48C77EC7D6C052615498DC82B380493B2C0610F9AAF070D1FFF08580D29C"),
    "proposal/attachments/minimal.patch": (13651, "DFE0F97EE5EC19D0194E6FFB9FC2C3CD5104F41B9B9DCA908837556E1E99F1DD"),
    "application/report.md": (9379, "6964F08042A633D53790E52FD6089AAA268C6D9DBC37E5DC88B999383160C6C6"),
    "application/result.json": (10315, "2B45D3CC36B665D0CCB561D0C0C32DADA35D9260319A62A1AC6B8B36B1B80CF7"),
    "application/evidence/application-evidence.json": (199421, "9C0C75BD3E2C96655F6F6BB09F73056A1C243B490DBAFB1A687EBB84EE168D4B"),
    "verification/report.md": (29429, "A6760AB96EBA87BBC92EE6E1BA50989594D55C313651934177457591A3B04B82"),
    "verification/result.json": (159760, "9DF69D773325B6271F05E7339743FD9ED2D8BF0B8374D6C384037EBABB7DE6EB"),
    "verification/verification-evidence.json": (1918232, "A62DD58BFB6197081C20BB3F945C4584A4F75ECC260DA5D427710E8F9E03DD09"),
    "review/report.md": (33155, "230DB33BA1A52DCFBD4AA598B9941F5D4E62DA16BE02FC3AE8992F1AAE9011ED"),
    "review/result.json": (211628, "32231D5616AD71F0AB22B277EE3C1F54F5CF7D48FE45334919010A09E8F96D16"),
    "review/review-evidence.json": (1311046, "B1127A42B57CFBA0BD78092D32E95C6ACA6F8D5B1FEF83C1F756A78725E82A75"),
}
MASTER_HASHES = {
    "SDLC_GOVERNANCE.md": "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
    "SDLC_ARTIFACT_GOVERNANCE.md": "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
    "SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C",
}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def rel(p):
    return Path(p).relative_to(ROOT).as_posix()


def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": rel(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest().upper()}


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, text=True).strip()


def pairs(values):
    result = {}
    for k, v in values:
        if k in result:
            raise ValueError("Duplicate JSON key: " + k)
        result[k] = v
    return result


def load(p):
    return json.loads(Path(p).read_text("utf-8-sig"), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def native(obj):
    if obj is None or type(obj) in (str, bool, int):
        return
    if type(obj) is list:
        for item in obj:
            native(item)
        return
    if type(obj) is dict:
        for k, v in obj.items():
            assert type(k) is str
            native(v)
        return
    raise TypeError("Non-native JSON value: " + repr(type(obj)))


def common(kind):
    return {
        "schema_version": "1.0", "record_type": kind, "record_id": AID + ":" + kind,
        "feature": "Governance framework only; no product feature",
        "work_id": WORK, "attempt_id": AID, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
        "cycle": 1, "process": ROLE,
        "creator": {"identity": ACTOR, "role": ROLE, "runtime_agent_id": ACTOR,
                    "copilot_agent_session_id": os.environ.get("COPILOT_AGENT_SESSION_ID"),
                    "session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
                    "identity_basis": "Current sole running same-task Audit in visible harness registry; not cryptographic external identity"},
        "created_at_utc": now(),
        "clock_basis": "Python timezone-aware system UTC at record preparation; not exact publication time",
        "gate": {"applicability": "No formal human gate created by Audit"},
        "related_records": [], "task_context": "No product task; existing governance cycle 1",
    }


def validate(obj, kind):
    native(obj)
    assert type(obj) is dict
    required = ["schema_version", "record_type", "record_id", "feature", "work_id",
                "attempt_id", "cycle_id", "cycle", "process", "creator", "created_at_utc",
                "clock_basis", "gate", "related_records", "task_context"]
    assert all(k in obj for k in required)
    assert obj["record_type"] == kind and obj["work_id"] == WORK and obj["attempt_id"] == AID
    assert obj["record_id"] == AID + ":" + kind
    assert obj["creator"]["identity"] == ACTOR and obj["creator"]["role"] == ROLE
    assert datetime.datetime.fromisoformat(obj["created_at_utc"]).utcoffset().total_seconds() == 0
    assert type(obj["related_records"]) is list and type(obj["gate"]) is dict
    if kind == "audit_invocation":
        for k in ["requested_scope", "input_manifest", "repository_context", "stage_start",
                  "persistence", "qualification", "predecessors", "outputs", "execution_status"]:
            assert k in obj
        assert obj["stage_start"]["actual_wording"] == START
        assert obj["execution_status"] == "INVOCATION PUBLISHED; substantive assessment not started"
        assert len(obj["persistence"]["masters"]) == 3
    encoded = json.dumps(obj, ensure_ascii=False, allow_nan=False, indent=2).encode("utf-8") + b"\n"
    decoded = json.loads(encoded, object_pairs_hook=pairs)
    assert decoded == obj
    assert json.dumps(decoded, sort_keys=True, ensure_ascii=False) == json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return encoded


def publish_json(path, obj):
    path = Path(path)
    assert path.is_relative_to(OWN)
    encoded = validate(obj, obj["record_type"])
    partial = path.with_name(path.name + ".partial")
    assert not path.exists() and not partial.exists(), "No overwrite"
    path.parent.mkdir(parents=True, exist_ok=True)
    with partial.open("xb") as f:
        f.write(encoded)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == encoded and load(partial) == obj
    validate(load(partial), obj["record_type"])
    assert not path.exists()
    os.rename(partial, path)  # Windows same-filesystem no-overwrite rename.
    assert path.read_bytes() == encoded and load(path) == obj
    return ref(path)


def sources():
    return sorted(p for base in [ROOT / ".github", ROOT / "docs/ai"]
                  for p in base.rglob("*") if p.is_file())


def inputs():
    # pathlib includes dot directories; never follow product artifact references.
    paths = set(sources())
    paths.update(p for p in (ROOT / "docs/sdlc-records/governance" / WORK).rglob("*")
                 if p.is_file() and not p.is_relative_to(OWN))
    for p in [ROOT / "AGENTS.md", ROOT / ".github/copilot-instructions.md"]:
        if p.is_file():
            paths.add(p)
    paths.add(Path(__file__).resolve())
    return [ref(p) for p in sorted(paths)]


def repo():
    return {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
            "head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
            "origin": git("remote", "get-url", "origin"), "status": git("status", "--porcelain=v1"),
            "index": ref(ROOT / ".git/index")}


def preflight():
    assert not (OWN / "attempt.json").exists(), "ONE ATTEMPT ONLY: already published"
    assert hashlib.sha256(b"abc").hexdigest() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    context = repo()
    assert context["head"] == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert context["origin"] == "https://github.com/ScalableParimal/SupportIQ.git"
    masters = [ref(ROOT / "docs/ai/sdlc" / n) for n in MASTER_HASHES]
    for m in masters:
        assert m["sha256"] == MASTER_HASHES[Path(m["path"]).name]
    preds = {}
    for key, (size, sha) in EXPECTED.items():
        role, rest = key.split("/", 1)
        p = BASE / IDS[role] / rest
        entry = ref(p)
        assert entry["bytes"] == size and entry["sha256"] == sha, key
        if p.suffix == ".json":
            native(load(p))
        preds[key] = entry
    for role, expected in [("application", "COMPLETED"), ("verification", "PASS"), ("review", "PASS")]:
        result = load(BASE / IDS[role] / "result.json")
        assert result["outcome"] == expected, role
        if role != "application":
            assert result["execution_status"] == "COMPLETED"
            assert all(c["outcome"] == "PASS" for c in result["criteria"])
        for field in ["report", "evidence"]:
            binding = result[field]
            assert type(binding) is dict
            actual = ref(ROOT / binding["path"])
            assert binding["sha256"] == actual["sha256"]
            if "bytes" in binding:
                assert binding["bytes"] == actual["bytes"]
    # Current non-mutating identity and ACL observation, not a source write probe.
    principal = subprocess.check_output(["whoami"], text=True).strip()
    acl = subprocess.check_output(["icacls", str(BASE)], text=True)
    assert principal and acl
    test = common("publisher_selftest")
    test.update({"unicode": "native \u2192 JSON", "nested": {"booleans": [True, False], "nothing": None},
                 "record_validation": "Actual complete object strict native JSON round-trip"})
    testref = publish_json(OWN / "evidence/publisher-selftest.json", test)
    try:
        publish_json(OWN / "evidence/publisher-selftest.json", test)
    except AssertionError:
        pass
    else:
        raise AssertionError("Collision guard did not reject existing final")
    assert ref(OWN / "evidence/publisher-selftest.json") == testref
    manifest = common("audit_input_manifest")
    manifest.update({"inventory_method": "Hidden-inclusive pathlib recursive file enumeration; all .github and docs/ai sources and all existing Work-ID governance records; own helper included; own outputs excluded to avoid circularity",
                     "files": inputs(), "governance_source_count": len(sources()),
                     "product_artifact_contents_inspected": False})
    manifest_ref = publish_json(OWN / "evidence/input-manifest.json", manifest)
    invocation = common("audit_invocation")
    invocation.update({
        "requested_scope": "Complete 52-core catalog, all seven separately reported mechanisms, and actual current governance-source inventory; no product-content inspection",
        "repository_context": context, "input_manifest": manifest_ref,
        "stage_start": {"actual_wording": START, "source": "Actual Human instruction supplied to this invocation",
                        "message_id": None, "authenticated_source_time": None,
                        "limitation": "Platform authenticated message identity/time not exposed; not invented",
                        "scope": "One fresh complete Audit only; no replacement invocation or other stage"},
        "predecessors": preds,
        "persistence": {
            "route": "Ordinary established governance-root route, not a second bootstrap",
            "root": "docs/sdlc-records/governance/", "authorized_output_scope": rel(OWN),
            "root_adoption_evidence": {
                "url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                "id": 6522916236, "author": "ScalableParimal", "author_id": 226102895,
                "author_association": "OWNER", "created_at": "2026-10-30T12:31:51Z",
                "updated_at": "2026-10-30T12:31:51Z",
                "validation": "Live authenticated GitHub issue_read get_comments during this invocation; unchanged owner-attributed decision",
                "use": "Established governance-root authority only; initial one-time stage authorization not reused"},
            "masters": masters,
            "master_baseline": "Candidate unadopted bootstrap comparison authority only",
            "product_root": "Not adopted; no adoption or product activation"},
        "qualification": {
            "effective_principal": principal, "attempts_acl_observation": acl,
            "role_specific_observed_capabilities": [
                "Non-mutating reads of Masters, current role, Skill and actual upstream records",
                "SHA-256 known-answer selftest and actual upstream byte/hash checks",
                "Hidden-inclusive complete input enumeration",
                "Strict JSON native-object validation, serialization/parse equality on actual complete records",
                "Flushed validated .partial then same-filesystem Windows atomic no-overwrite rename",
                "Own-record exact readback and collision rejection selftest"],
            "publisher_selftest": testref,
            "boundary": "Procedural nonmutation, not sandbox enforced; no source write permission or source write probe",
            "limitations": ["No exhaustive trusted event log", "No coordinated source lock",
                           "Endpoint hashes cannot exclude transient or same-principal tampering",
                           "No exact publication timestamp captured", "Harness identity is not external cryptographic identity"]},
        "recovery": {
            "current_actor": ACTOR,
            "visible_registry": "Only currently running same-task Audit is this actor; all other visible agents idle",
            "history": "Prior unsuccessful Verification invocation/replacement and older incomplete records preserved; neither live-writer proof nor current valid assurance",
            "current_assurance": "Explicitly separately started fresh Verification PASS and Review PASS named in predecessors",
            "cycle": "Continue established GOV-REMEDIATION-PROSPECTIVE-001 Cycle 1; no retroauthorization"},
        "outputs": {"report": rel(OWN / "report.md"), "result": rel(OWN / "result.json"),
                    "evidence": rel(OWN / "evidence/audit-evidence.json")},
        "execution_status": "INVOCATION PUBLISHED; substantive assessment not started",
        "related_records": list(preds.values()),
        "ordering": "Independent separate-process invocation validation/readback required before substantive assessment",
    })
    validate(invocation, "audit_invocation")
    assert repo() == context, "Repository changed before invocation publication"
    for entry in manifest["files"]:
        assert ref(ROOT / entry["path"]) == entry, entry["path"]
    assert not (OWN / "attempt.json").exists()
    out = publish_json(OWN / "attempt.json", invocation)
    print(json.dumps({"invocation": out, "manifest": manifest_ref,
                      "source_count": len(sources()), "inputs": len(manifest["files"]),
                      "next": "Independent fresh readback; no substantive assessment yet"}, indent=2))


def readback():
    invocation = load(OWN / "attempt.json")
    validate(invocation, "audit_invocation")
    assert invocation["creator"]["runtime_agent_id"] == ACTOR
    manifest = load(ROOT / invocation["input_manifest"]["path"])
    validate(manifest, "audit_input_manifest")
    assert ref(ROOT / invocation["input_manifest"]["path"]) == invocation["input_manifest"]
    for entry in manifest["files"]:
        assert ref(ROOT / entry["path"]) == entry, entry["path"]
    assert repo() == invocation["repository_context"]
    check = common("audit_invocation_readback")
    check.update({"invocation": ref(OWN / "attempt.json"),
                  "manifest": invocation["input_manifest"], "all_input_files_unchanged": len(manifest["files"]),
                  "outcome": "PASS", "validation": "Fresh separate Python process reopens stored invocation, strict-parses entire native objects, validates common and invocation schema and every input binding before substantive assessment",
                  "publication_sequence": "Publisher command returned final invocation hash; this subsequent command independently reread it",
                  "related_records": [ref(OWN / "attempt.json"), invocation["input_manifest"]]})
    print(json.dumps(publish_json(OWN / "evidence/invocation-readback.json", check), indent=2))


if __name__ == "__main__":
    {"preflight": preflight, "readback": readback}[sys.argv[1]]()
