"""Audit-owned native serializer, manifest and exclusive publication helper."""
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T115616Z-ab050be4-c4db-46ae-a5eb-a9fcf9bb41cb"
SCOPE = ROOT / "docs/sdlc-records/governance" / WORK / "attempts" / ATTEMPT
ACTOR = {"identity": ATTEMPT + ":audit-actor", "role": "SDLC Governance Audit",
         "runtime_agent_id": "1831d5ce-ee60-497b-ba25-8217357c77cd",
         "identity_basis": "Only currently running same-task Audit entry in visible harness registry; local invocation identity is definitive; no external authentication claim",
         "session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60"}

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def ref(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    b = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b)}

def publish(relative, value):
    p = SCOPE / relative
    assert p.resolve().is_relative_to(SCOPE.resolve())
    p.parent.mkdir(parents=True, exist_ok=True)
    assert not p.exists(), "final collision"
    b = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8") if not isinstance(value, bytes) else value
    partial = p.with_name(p.name + ".partial")
    with partial.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    actual = partial.read_bytes()
    assert actual == b
    if p.suffix == ".json":
        assert json.loads(actual) == value
        assert isinstance(value, (dict, list))
    elif p.suffix == ".py":
        ast.parse(actual.decode("utf-8"))
    elif p.suffix == ".md":
        assert b and b.decode("utf-8")
        assert b"`n" not in b
    # On Windows os.rename is same-filesystem, atomic and refuses an existing destination.
    assert os.name == "nt"
    os.rename(partial, p)
    assert p.read_bytes() == b
    return ref(p)

def record(kind, **fields):
    return dict(schema_version="1.0", record_type=kind, record_id=ATTEMPT+":"+kind,
                work_id=WORK, attempt_id=ATTEMPT, cycle_id="GOV-REMEDIATION-PROSPECTIVE-001",
                cycle=1, creator=ACTOR, created_at_utc=now(),
                clock_basis="Python timezone-aware UTC preparation clock, not exact publication time", **fields)

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def state():
    return {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
            "head": git("rev-parse","HEAD"), "branch": git("branch","--show-current"),
            "origin":git("remote","get-url","origin"), "status":git("status","--short"),
            "index":ref(".git/index")}

def inventory():
    files, dirs, excluded = [], [], []
    for base, dnames, fnames in os.walk(ROOT):
        dnames[:] = sorted(d for d in dnames if d != ".git")
        rel = Path(base).relative_to(ROOT)
        if (ROOT / rel).resolve().is_relative_to(SCOPE.resolve()):
            dnames[:] = []
            continue
        dirs.append(rel.as_posix())
        for f in sorted(fnames):
            p = Path(base)/f
            rp = p.relative_to(ROOT).as_posix()
            if rp.startswith((".github/", "docs/ai/", "docs/sdlc-records/governance/")):
                files.append(ref(p))
            else:
                excluded.append({"path":rp, "bytes":p.stat().st_size, "reason":"Non-governance/product content not opened or evaluated"})
    return record("evaluated_input_manifest", traversal="os.walk explicitly includes hidden dot directories/files; only .git and this actor output scope pruned; no PowerShell non-Force enumeration",
                  files=files, directories=dirs, excluded_content=excluded,
                  source_inventory=[f for f in files if f["path"].startswith((".github/","docs/ai/"))],
                  file_count=len(files), directory_count=len(dirs),
                  github_file_count=sum(f["path"].startswith(".github/") for f in files))

if __name__ == "__main__":
    if sys.argv[1] == "init":
        assert hashlib.sha256(b"abc").hexdigest().upper() == "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD"
        test = record("publisher_selftest", native={"list":[True,False,None,1,{"quoted":"a\"b\nc"}]})
        testref = publish("evidence/publisher-selftest.json",test)
        try:
            publish("evidence/publisher-selftest.json",test)
            raise RuntimeError("collision unexpectedly accepted")
        except AssertionError:
            assert json.loads((SCOPE/"evidence/publisher-selftest.json").read_bytes()) == test
        inputs=inventory()
        sources=inputs["source_inventory"]
        assert len(sources) == 76
        master_expected={
          "docs/ai/sdlc/SDLC_GOVERNANCE.md":"79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
          "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md":"6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
          "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md":"08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C"}
        for p,h in master_expected.items(): assert ref(p)["sha256"] == h
        pre={
          "review/report.md":("20261102T1130Z-d7d84322-aff9-4d3e-9cec-90f9054705cd","report.md","E8BBBCEC0AE7E865773096E420EFEB3F1350F54B4225198BDEE9436138998D79"),
          "review/result.json":("20261102T1130Z-d7d84322-aff9-4d3e-9cec-90f9054705cd","result.json","852E0E357A5D24B802DEF018E6FCEB7BD4BF27BA728DB322685AB738EC8A1DE7"),
          "review/evidence":("20261102T1130Z-d7d84322-aff9-4d3e-9cec-90f9054705cd","attachments/review-evidence.json","D86AE46C91DCB2085ED8D15DF1ABC7F67A9F9F71E3B6A333BC737EC26D4A71BD"),
          "verification/report.md":("20261102T110840Z-c1d89695-d3e5-4721-a846-3f3dca25cc22","report.md","02E8B7CD6AD7F599E9F9C4A411DC1A7C5DA535C366A218CD7BB3D633CF173825"),
          "verification/result.json":("20261102T110840Z-c1d89695-d3e5-4721-a846-3f3dca25cc22","result.json","B3FE365B38492FF67E017CA1048F2BFBEB9442795AF1939FA209D1A06EA75C40"),
          "application/report.md":("20261102T110324Z-b92b73f0-deba-4842-b261-1ed22bd7d014","report.md","FE784908BD9A7F5B193D830538F7DA7AE1EAB949987A63F3FC6E53A95F4AF627"),
          "application/result.json":("20261102T110324Z-b92b73f0-deba-4842-b261-1ed22bd7d014","result.json","C18F9CE97C385DBD3FDBC506AB63395A963809C4BAF77287D7392FC2F85072AF")}
        preds={}
        for label,(aid,f,h) in pre.items():
            path=SCOPE.parent/aid/f
            rr=ref(path); assert rr["sha256"]==h
            if f=="result.json":
                obj=json.loads(path.read_bytes())
                assert obj["outcome"] in ("PASS","COMPLETED")
            preds[label]=rr
        assert ref(".github/agents/sdlc-governance-remediation.agent.md")["sha256"]=="404AF9126BC310AEA79BA7616AB8E25C0AD5EE7F48B360F1AF515EA4DC9F942F"
        current=state()
        assert current["head"]=="57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
        assert current["origin"]=="https://github.com/ScalableParimal/SupportIQ.git"
        manifest=publish("evidence/input-manifest.json",inputs)
        attempt=record("audit_invocation",
            process="SDLC Governance Audit", requested_scope="Complete 52-core catalog and all seven mechanism groups; current 76-source inventory; governance only",
            repository_context=current, input_manifest=manifest, predecessors=preds,
            task_context="No product task; existing prospective governance cycle 1",
            stage_start={"actual_wording":"Yes, initiate the complete Governance Audit under the existing Work ID and Cycle 1 using the GOV-AUD-20261102-002 Application, Verification PASS and Review PASS",
                         "source":"Actual Human instruction supplied in this invocation; source platform ID/authenticated time not exposed","not_approval_or_adoption":True},
            persistence={"root":"docs/sdlc-records/governance/","authorized_output_scope":SCOPE.relative_to(ROOT).as_posix(),
                "root_evidence":{"url":"https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236","id":6522916236,
                 "author":"ScalableParimal","author_association":"OWNER","created_at":"2026-10-30T12:31:51Z",
                 "live_resolution":"github issue_read get_comments during this invocation; canonical repository owner attribution and exact HEAD/Masters revalidated",
                 "use":"Established root adoption only; one-time initial stage authorization is not reused"},
                "master_baseline":"Candidate, unadopted; three Masters are bootstrap comparison authority only","product_root":"Not adopted; no product records authorized"},
            qualification={"effective_windows_principal":subprocess.check_output(["whoami"],text=True).strip(),
                "declared_tools":"PowerShell/Python reads, SHA256, JSON, AST checks; own record publisher; no source write permission under this invocation",
                "observed":"Current file reads and predecessor hashes, git HEAD/branch/status/index checks and abc SHA256 passed; complete hidden-inclusive manifest; attempts ACL Authenticated Users Modify; own publisher flushed validated partial, Windows no-overwrite rename, exact native JSON readback and collision selftest passed",
                "publisher_selftest":testref,"permission_boundary":"Procedural nonmutation, not sandbox-enforced; no source write probe",
                "limitations":["No exhaustive trusted event log","Endpoint hashes cannot exclude transient/same-principal tampering","No coordinated source lock","Record-preparation clock is not exact publication time"]},
            recovery={"incomplete_historical":["20261031053750Z-5a67f304-e4e5-4045-8721-235a47779233","20261031T045348Z-a8d815b9-c331-44ca-b9b1-cc5ea5bdbde6"],
                "basis":"Existing prospective cycle and successive terminal reports preserve historical attempts; old start metadata alone is not evidence of liveness; visible registry has one same-task running Audit, this actor, all other visible agents idle",
                "failed_reviews":"Two CANNOT COMPLETE attempts retained; current explicit fresh retry is PASS and integrity checked; not source findings"},
            execution_status="INVOCATION PUBLISHED; substantive assessment not started",
            outputs={"report":"report.md","result":"result.json","evidence":"evidence/audit-evidence.json"},
            ordering="Manifest and invocation published before substantive assessment; independent separate-process attempt readback is mandatory next")
        ar=publish("attempt.json",attempt)
        print(json.dumps({"attempt":ar,"manifest":manifest,"files":inputs["file_count"],"dirs":inputs["directory_count"],"sources":len(sources),"github":inputs["github_file_count"]},indent=2))
    elif sys.argv[1]=="readback":
        p=SCOPE/"attempt.json"; obj=json.loads(p.read_bytes())
        assert obj["attempt_id"]==ATTEMPT and obj["work_id"]==WORK
        assert ref(ROOT/obj["input_manifest"]["path"])==obj["input_manifest"]
        assert ref(".git/index")==obj["repository_context"]["index"]
        for rr in obj["predecessors"].values(): assert ref(ROOT/rr["path"])==rr
        print(json.dumps({"independent_readback":"PASS","invocation":ref(p),"manifest":obj["input_manifest"],"observed_utc":now(),"substantive_work_permitted_next":True},indent=2))
