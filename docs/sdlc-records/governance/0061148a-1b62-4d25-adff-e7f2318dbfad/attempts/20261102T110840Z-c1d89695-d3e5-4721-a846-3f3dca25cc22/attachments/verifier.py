import os, sys, json, hashlib, pathlib, subprocess, datetime

ROOT = pathlib.Path(__file__).resolve().parents[7]
os.chdir(ROOT)
ATTEMPT = "20261102T110840Z-c1d89695-d3e5-4721-a846-3f3dca25cc22"
BASE = "docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/"
OWN = BASE + ATTEMPT + "/"
OUTPUTS = ["attempt.json", "checkpoint-0001.json", "checkpoint-0002.json",
           "checkpoint-0003.json", "checkpoint-0004.json", "report.md", "result.json",
           "attachments/evidence.json", "attachments/verifier.py"]
EXCLUSIONS = {OWN + n + suffix for n in OUTPUTS for suffix in ["", ".partial"]}
ACTOR = "independent-governance-verification:" + ATTEMPT

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def fp(p):
    b = pathlib.Path(p).read_bytes()
    return {"path": str(p).replace("\\", "/"), "bytes": len(b), "sha256": sha(b)}

def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args]).decode("utf-8").strip()

def snapshot():
    tracked = set(git("ls-files", "-z").split("\0"))
    files = []
    for folder, dirs, names in os.walk("."):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for n in sorted(names):
            p = (pathlib.Path(folder) / n).as_posix()
            if p not in EXCLUSIONS:
                files.append(dict(fp(p), tracked=p in tracked))
    files.sort(key=lambda x: x["path"])
    return {
        "files": files, "file_count": len(files), "manifest_sha256": sha(encode(files)),
        "head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
        "index": fp(".git/index"), "tracked_paths": sorted(p for p in tracked if p),
        "status": git("status", "--porcelain=v1", "--untracked-files=all"),
        "product_root_present": pathlib.Path("docs/sdlc-records/product").exists(),
        "expected_absences": ["docs/sdlc-records/product"],
        "exclusions_exact": sorted(EXCLUSIONS),
    }

def encode(d):
    return (json.dumps(d, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")

def strict_load(b):
    def pairs(xs):
        d = {}
        for k, v in xs:
            if k in d:
                raise ValueError("duplicate key")
            d[k] = v
        return d
    return json.loads(b, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def publish(name, obj):
    p = pathlib.Path(OWN + name)
    p.parent.mkdir(parents=True, exist_ok=True)
    b = obj if isinstance(obj, bytes) else encode(obj)
    if not isinstance(obj, bytes):
        assert strict_load(b) == obj
        assert encode(strict_load(b)) == b
    partial = pathlib.Path(str(p) + ".partial")
    assert not p.exists() and not partial.exists(), "publication collision"
    with partial.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == b
    if not isinstance(obj, bytes):
        assert strict_load(partial.read_bytes()) == obj
    os.rename(partial, p)  # Windows rename fails if destination exists.
    assert p.read_bytes() == b
    return fp(p.as_posix())

def bootstrap():
    assert sha(b"abc") == "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD"
    native = {"quote": "'ASCII' \"double\"", "bool": True, "null": None,
              "unicode": "\u2014", "array": [1, {"nested": False}], "newline": "a\nb"}
    assert strict_load(encode(native)) == native
    for bad in [b'{"x":1,"x":2}', b'{"x":NaN}']:
        try:
            strict_load(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("strict JSON selftest")
    s = snapshot()
    d = {
        "schema_version": 1, "record_type": "verification_invocation", "record_id": ATTEMPT + ":invocation",
        "attempt_id": ATTEMPT, "work_id": "0061148a-1b62-4d25-adff-e7f2318dbfad",
        "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001", "cycle": 1, "finding_id": "GOV-AUD-20261102-002",
        "created_at_utc": now(), "clock_basis": "runtime UTC; not an authenticated Human decision timestamp",
        "actor": {"identity": ACTOR, "role": "Independent Governance Verification",
                  "runtime_agent_id_observed": "8e77a262-4464-46d1-9078-a3fefb37d387",
                  "identity_basis": "only running matching verifier in visible roster; association is procedural, not authenticated attestation",
                  "session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
                  "os_principal": "INT-SCL-010\\Parimal",
                  "role": fp(".github/agents/independent-governance-verification.agent.md")},
        "independence": {"preparer_runtime": "0939dcbe-f104-454a-a8bd-62e36810ccd3",
                         "applier_runtime": "7282643f-d89b-4b2d-b082-475ffc440fce",
                         "reviewer_role": ".github/agents/independent-governance-review.agent.md",
                         "reviewer_not_started": True, "excluded_active_remediation": "4dc4dd1b-4bd6-4b42-82d4-2b8b74920c36",
                         "distinct_role_and_invocation": True, "not_orchestrator": True},
        "stage_start": {"actual_quote": "Yes, initiate Independent Governance Verification for the GOV-AUD-20261102-002 amendment Application only",
                        "source": "actual Human instruction supplied in current invocation; no authenticated message ID or decision timestamp exposed",
                        "scope": "completed Application only; own fresh records under existing WorkID attempts",
                        "no_invented_message_metadata": True},
        "repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT)},
        "capability": {"current_read_and_hash": "Python binary read and hashlib SHA-256; known-vector PASS",
                       "checks": "git non-mutating reads, full non-.git byte/path snapshot, exact in-memory byte comparison, strict native JSON",
                       "permissions": "observed source and attempts ACL: current principal owner; Authenticated Users Modify; no write exclusion",
                       "publication": "Human scope plus Master Artifact 33.1/Traceability 30.1 and role/skill own-record boundary; atomic no-overwrite publication, flush, strict validation, separate readback",
                       "publication_scope": OWN, "exclusions_exact": sorted(EXCLUSIONS),
                       "source_writes_prohibited": True, "write_probes_performed": False,
                       "technical_source_write_prevention": False,
                       "strict_json_selftests": "native complete object roundtrip and canonical reserialization PASS; duplicate-key/nonfinite rejection PASS"},
        "assurance": {"mode": "procedural non-mutation",
                      "residual_risks": "Endpoint fingerprints cannot exclude transient writes or same-principal tampering. No exhaustive trusted OS event stream, sandbox write exclusion, or security guarantee.",
                      "concurrency": "Only matching verifier running in visible roster; preparer/applier/remediation idle. This actor is not a competing writer. No enforced no-edit lock or exhaustive external writer detection.",
                      "operation_evidence": "Actor-visible ordered tool transcript plus this own integrity-bound script and checkpoints; no exhaustive event log.",
                      "qualification_operations": [
                          "Read required skill, role, guideline, prompt, request using Get-Content",
                          "Located Masters and publication sections; read application result solely for identity/predecessor qualification",
                          "whoami, ACL, git status/HEAD/branch non-mutating observations",
                          "get_current_session and list_agents current identity/concurrency observations",
                          "Errors retained: absent optional .github/copilot-instructions.md; substring section lookup; cp1252 decode error; corrected UTF-8 reads; no repair/source write",
                          "apply_patch created only own designated attachments/verifier.py",
                          "Python bootstrap: known hash/JSON tests, full manifest, publication then separate command readback before substantive comparison"]},
        "input_snapshot": s,
        "predecessor_claims": {"application": BASE + "20261102T110324Z-b92b73f0-deba-4842-b261-1ed22bd7d014/result.json",
                               "proposal": BASE + "20261102T105400Z-5145fb48-c113-4ff7-a263-5ff861ca39c5/result.json"},
        "source_actions_authorized": False, "review_authorized": False, "audit_authorized": False,
        "effectiveness_claimed": False, "master_or_product_adoption": False,
    }
    print(json.dumps(publish("attempt.json", d)))

if __name__ == "__main__":
    if sys.argv[1] == "bootstrap":
        bootstrap()
    elif sys.argv[1] == "readback":
        p = OWN + "attempt.json"
        b = pathlib.Path(p).read_bytes()
        d = strict_load(b)
        assert encode(d) == b and d["actor"]["identity"] == ACTOR
        s = snapshot()
        old = d["input_snapshot"]
        assert s["manifest_sha256"] == old["manifest_sha256"]
        assert s["index"] == old["index"] and s["head"] == old["head"] and s["branch"] == old["branch"]
        print(json.dumps(publish("checkpoint-0001.json", {
            "record_id": ATTEMPT + ":record-first-readback", "actor": ACTOR,
            "time_utc": now(), "attempt": fp(p), "complete_native_object_equality": True,
            "canonical_serializer_equality": True, "input_snapshot_unchanged": True,
            "script": fp(OWN + "attachments/verifier.py"), "outcome": "PASS",
            "operation": "fresh separate Python process reads actual published invocation and recomputes all bounded inputs before substantive checks"})))
