"""Actor-owned reproducible record publication/validation helper; not governance authority."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[7]
os.chdir(ROOT)
OWN = Path(__file__).resolve().parents[1]
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = OWN.name
CYCLE = "GOV-REMEDIATION-PROSPECTIVE-001"
ROLE = "SDLC Governance Remediation"
ATTEMPTS = OWN.parent
AUDIT = ATTEMPTS / "20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f"
START = "Yes, initiate bounded Governance Remediation continuation for GOV-AUD-20261102-002 only under the existing Work ID and cycle"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def cmd(*args):
    return subprocess.check_output(args, text=True, encoding="utf-8").strip()

def ref(path):
    p = Path(path)
    b = p.read_bytes()
    return {"path": p.resolve().relative_to(ROOT).as_posix(), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest().upper()}

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8-sig"))

def serialize(obj):
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    assert json.loads(b) == obj
    return b

def publish(path, data):
    path = Path(path)
    assert path.resolve().is_relative_to(OWN)
    assert not path.exists(), "Final record collision"
    partial = path.with_name(path.name + ".partial")
    path.parent.mkdir(parents=True, exist_ok=True)
    with partial.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == data
    if path.suffix == ".json":
        json.loads(partial.read_bytes())
    # Windows os.rename is same-filesystem and refuses an existing destination.
    assert os.name == "nt"
    os.rename(partial, path)
    assert path.read_bytes() == data
    return ref(path)

def snapshot():
    source = []
    records = []
    for base in [Path(".github"), Path("docs/ai")]:
        for p in sorted(base.rglob("*")):
            if p.is_file():
                source.append(ref(p))
    for p in sorted(ATTEMPTS.parent.rglob("*")):
        if p.is_file() and not p.resolve().is_relative_to(OWN):
            records.append(ref(p))
    return {"source": source, "prior_records": records}

def meta(kind):
    return {"schema_version": "1.0", "record_type": kind, "record_id": ATTEMPT + ":" + kind,
            "work_id": WORK, "attempt_id": ATTEMPT, "cycle_id": CYCLE, "cycle": 1,
            "creator": {"role": ROLE, "actor_identity": "local-coordination-invocation:" + ATTEMPT},
            "created_at_utc": now(), "clock_basis": "Current host UTC record-preparation sample, not publication time",
            "process": "Bounded Governance Remediation continuation"}

if __name__ == "__main__" and sys.argv[1] == "start":
    sample = {"quotes": "\"'`", "newline": "actual\nnewline", "native": [None, True, 1, {"x": "→"}]}
    assert json.loads(serialize(sample)) == sample
    assert not (OWN / "attempt.json").exists()
    origin = cmd("git", "remote", "get-url", "origin")
    head = cmd("git", "rev-parse", "HEAD")
    assert origin == "https://github.com/ScalableParimal/SupportIQ.git"
    assert head == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    acl = cmd("powershell.exe", "-NoProfile", "-Command",
              "(Get-Acl 'docs/sdlc-records/governance/" + WORK + "/attempts').AccessToString")
    identity = cmd("whoami")
    assert os.access(ATTEMPTS, os.W_OK) and os.access(AUDIT / "result.json", os.R_OK)
    role_path = Path(".github/agents/sdlc-governance-remediation.agent.md")
    role_text = role_path.read_text(encoding="utf-8-sig")
    assert "The Remediation actor may publish only its own coordination records" in role_text
    masters = [ref(p) for p in Path("docs/ai/sdlc").glob("SDLC_*.md")]
    expected = {"SDLC_GOVERNANCE.md": "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
                "SDLC_ARTIFACT_GOVERNANCE.md": "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
                "SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C"}
    for m in masters:
        if Path(m["path"]).name in expected:
            assert m["sha256"] == expected[Path(m["path"]).name]
    d = meta("invocation")
    d.update({"repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
                              "origin": origin, "head": head, "branch": cmd("git", "branch", "--show-current"),
                              "git_status": cmd("git", "--no-pager", "status", "--short")},
              "qualification": {"effective_os_identity": identity, "acl": acl, "read_access_checked": True,
                                "own_record_parent_write_access_checked": True,
                                "serializer_native_object_selftest": "PASS",
                                "publication_route": "Exclusive .partial create, native UTF-8 JSON, parse, flush/fsync, same-filesystem Windows no-overwrite rename, exact readback",
                                "source_write_probe": False, "role_definition": ref(role_path),
                                "limitations": "Procedural nonmutation, not sandbox-enforced; no authenticated platform actor ID exposed; local actor ID identifies this invocation only. Shared principal and transient writes cannot be excluded."},
              "authorization": {"actual_human_start": START, "source": "Actual current parent conversation user message",
                                "authenticated_message_id": None, "authenticated_human_time": None,
                                "scope": "Validate latest Audit integrity, reconcile existing cycle, route only GOV-AUD-20261102-002 for separately Human-initiated Investigation; own new attempt records only",
                                "excluded": ["all other stage invocations", "source/upstream edits", "finding acceptance", "correction approval/application", "adoption", "commit/push", "product work"]},
              "persistence": {"root": "docs/sdlc-records/governance/", "existing_work_id": WORK,
                              "own_scope": OWN.relative_to(ROOT).as_posix(),
                              "root_decision": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                                                "author": "ScalableParimal", "author_association": "OWNER",
                                                "created_at": "2026-10-30T12:31:51Z",
                                                "live_resolved_current_invocation": True,
                                                "scope": "Governance-root adoption and initial Audit only; NOT current continuation authority"},
                              "masters": masters, "product_root_and_master_baseline": "Not adopted; Masters comparison authority only"},
              "recovery": {"prior_cycle_attempt": ref(ATTEMPTS / "20261031T072633Z-4c6c7de5-037e-49d1-a594-97b7ef0c5319" / "attempt.json"),
                           "stale_unterminated_attempts": ["20261031053750Z-5a67f304-e4e5-4045-8721-235a47779233", "20261031T045348Z-a8d815b9-c331-44ca-b9b1-cc5ea5bdbde6"],
                           "liveness": "Start records do not establish live writers. Current native process enumeration inspected; no conflicting coordination identified. Own runtime process is not a competing writer; no exhaustive event log or exclusive sandbox proof."},
              "inputs": [ref(AUDIT / "attempt.json")],
              "baseline": snapshot(),
              "helper": ref(__file__),
              "designated_outputs": ["attempt.json", "report.md", "result.json", "attachments/validation.json", "attachments/investigation-handoff.md"],
              "ordering": "Qualification and publication only in this operation; substantive latest-Audit analysis begins after separate tool-call invocation readback"})
    print(json.dumps({"published_invocation": publish(OWN / "attempt.json", serialize(d)),
                      "source_files": len(d["baseline"]["source"]), "prior_records": len(d["baseline"]["prior_records"])}))
