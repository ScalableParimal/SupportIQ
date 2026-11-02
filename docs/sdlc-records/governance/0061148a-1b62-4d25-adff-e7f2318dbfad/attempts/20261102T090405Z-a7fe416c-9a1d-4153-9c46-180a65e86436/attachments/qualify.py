import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[7]
os.chdir(ROOT)
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T090405Z-a7fe416c-9a1d-4153-9c46-180a65e86436"
BASE = Path("docs/sdlc-records/governance") / WORK / "attempts" / ATTEMPT

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def ref(path):
    p = Path(path)
    b = p.read_bytes()
    return {"path": p.as_posix(), "sha256": sha(b), "bytes": len(b)}

def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args]).decode().strip()

def encode(d):
    b = (json.dumps(d, ensure_ascii=True, indent=2) + "\n").encode("utf-8")
    assert json.loads(b) == d
    return b

def publish(path, b):
    path = Path(path)
    assert path.is_relative_to(BASE)
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists()
    tmp = path.with_name(path.name + ".partial")
    with tmp.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == b
    os.rename(tmp, path)
    assert path.read_bytes() == b
    return ref(path)

if __name__ == "__main__":
    assert ROOT == Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
    assert os.name == "nt"
    assert git("rev-parse", "HEAD") == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert git("remote", "get-url", "origin") == "https://github.com/ScalableParimal/SupportIQ.git"
    assert not Path("docs/sdlc-records/product", WORK).exists()
    masters = {
        "docs/ai/sdlc/SDLC_GOVERNANCE.md": "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
        "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md": "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
        "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C",
    }
    for p, h in masters.items():
        assert ref(p)["sha256"] == h
    initial = Path("docs/sdlc-records/governance", WORK, "attempts/20261030T123604Z-15be0f40-a028-4166-bb27-fbf5fdefecc4/attempt.json")
    first = json.loads(initial.read_bytes())
    assert first["work_id"] == WORK
    assert first["authorization"]["comment_id"] == 6522916236
    governing = [
        ".github/agents/corrective-change-decision.agent.md",
        ".github/skills/corrective-change-decision/SKILL.md",
        "docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md",
        "docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md",
        "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md",
        *masters,
    ]
    # Byte fingerprints only; substantive input comparison has not begun.
    originals = [ref(p) for top in [Path(".github"), Path("docs"), Path("README.md")]
                 for p in ([top] if top.is_file() else sorted(top.rglob("*")))
                 if p.is_file() and not p.is_relative_to(BASE)]
    input_specs = [
        ("20261102T085032Z-8be0cc46-2de4-4ea4-a24e-3d341030d824/report.md", "3C6496F1EBC96BAA77573A77D928424914DA533B56081247273B6C3B4E5ABB40"),
        ("20261102T085032Z-8be0cc46-2de4-4ea4-a24e-3d341030d824/result.json", "6751C6325AA46E2A9F8818E0B7A783E1702DB39E75A1C52FAB7BCCF0766F082E"),
        ("20261102T085032Z-8be0cc46-2de4-4ea4-a24e-3d341030d824/evidence/investigation-evidence.json", "8FB5CF17464D416CFC0E7451C2967594E5B60E983F3473A9B258D02BE619FC98"),
        ("20261102T082552Z-6dfe39f3-18aa-40b8-88be-56850b13b291/report-revision-0001.md", "A1A19F188ADFEED3CA9D9602880FD71F599A1141F0BF6DBF2D538F93AA682EE8"),
        ("20261102T082552Z-6dfe39f3-18aa-40b8-88be-56850b13b291/result.json", "5D1F2BDC3E235CDD6C3A95F06838B7AFAC63A6C0FA9D7F96730FD2D6A81D8056"),
        ("20261102T084120Z-84eb5d6a-4ec3-4c1f-9122-17edda7c6d51/report.md", "84D6194D5FBCF02ED26DC81341F68843F37A7B04B9B0A1BE7416B3B4647B7F0C"),
        ("20261102T084120Z-84eb5d6a-4ec3-4c1f-9122-17edda7c6d51/result.json", "5A55C4D055607FD5898FF7D87E7B74A2BFACA52818F4FB24B9C637FAE8453EF1"),
        ("20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0/report.md", "CE975EE00E642B93AF50EF8FF0FF418101CE821F2E94121D43E0B260A012BF6B"),
        ("20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0/evidence/investigation-evidence.json", "8D008604EFEC599AC751EB1B457FD72750E3B4ECB7E0B5071087E64F1A67F977"),
        ("20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0/result.json", "080C02F1FD262C1690261A0E74505C7AEC6EA9ACBBDFFFDF58BAB91759826F54"),
    ]
    inputs = []
    for tail, expected in input_specs:
        rr = ref(BASE.parent / tail)
        assert rr["sha256"] == expected, tail
        inputs.append(rr)
    who = subprocess.check_output(["whoami"]).decode().strip()
    record = {
        "schema_version": "1.0", "record_type": "invocation", "record_id": ATTEMPT + ":invocation",
        "work_id": WORK, "attempt_id": ATTEMPT, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
        "cycle_number": 1, "creator": ATTEMPT, "role": "Corrective Change Decision",
        "process": "Corrective Change Decision & Plan Update", "subject_type": "FINDING",
        "finding_id": "GOV-AUD-20261102-001",
        "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "clock_basis": "Current host UTC record-preparation sample, not publication time",
        "actor_identity": {"invocation": ATTEMPT, "runtime": "Current direct Corrective Change Decision conversation; platform runtime agent ID not exposed", "definition": ref(governing[0])},
        "repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT), "head": git("rev-parse", "HEAD"),
                       "branch": git("branch", "--show-current"), "status_porcelain": git("status", "--short"), "source_manifest": originals},
        "output_scope": BASE.as_posix(), "status": "QUALIFIED; awaiting independent invocation readback before substantive comparison",
        "authorization": {
            "actual_human_start": "Yes, initiate Corrective Change Decision for GOV-AUD-20261102-001 only; prepare a proposal without applying changes",
            "source": "Actual user instruction in current conversation; authenticated platform message identity/time not exposed",
            "scope": "Only FINDING GOV-AUD-20261102-001 decision and own proposal/output records; no application, other-record correction, downstream stage, adoption, commit or push",
            "approval_granted": False,
            "root_adoption": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                              "author": "ScalableParimal", "author_id": 226102895, "association": "OWNER",
                              "created_at": "2026-10-30T12:31:51Z", "updated_at": "2026-10-30T12:31:51Z",
                              "decision_body_sha256": first["authorization"]["decision_body_sha256"],
                              "current_check": "GitHub issue_read get_comments during this qualification resolves unchanged OWNER root-adoption comment with matching HEAD and Master hashes; initial Audit-only stage is not reused"},
            "reservation": ref(initial),
            "pre_master_basis": "SDLC_GOVERNANCE section 3 normal corrective workflow after bootstrap; no candidate Master adoption or product baseline implied"
        },
        "qualification": {
            "effective_identity": who,
            "token_sid": "S-1-5-21-2809803128-1021655904-3966773769-1002",
            "current_nonmutating_checks": [
                "whoami /user and /groups succeeded in current invocation; Authenticated Users enabled",
                "Current parent ACL has Authenticated Users Allow Modify/Synchronize and no observed deny",
                "Current parent read/enumeration, source reads, SHA-256, Git state and os.access R/W/X succeeded",
                "Python 3.14.7 on Windows; JSON UTF-8 serialize/parse, exact-byte checks, fsync and same-filesystem os.rename no-overwrite route",
                "No source write probe; only own partial records may be published",
                "Existing Work ID reservation validated; no corresponding product Work ID directory",
                "Recent predecessor terminal metadata readable; historical in_progress records alone do not prove live writer",
                "Current runtime invocation is this actor, not a competing writer; no other actor dispatched or concurrent writer reported by current human start"
            ],
            "capability_limitations": "Procedure is write-capable; ACLs do not sandbox this actor. No exhaustive execution log or proof excluding transient same-principal tampering or external concurrent writers. Point-in-time hashes and no-overwrite own scope bound the claim.",
            "recovery_boundary": "Continue existing Work ID in new own attempt. Preserve all originals and pre-existing unrelated changes; stop on drift, collision, mismatch or uncertain capability."
        },
        "governing": [ref(p) for p in governing], "inputs": inputs,
        "ordered_ledger": [
            {"sequence": 1, "event": "Load current Skill, governing Guideline/Prompt/Request, actor and publication/qualification rules"},
            {"sequence": 2, "event": "Nonmutating root-adoption, identity, permissions, source-state, reservation, input hash and recovery qualification; no substantive affected report comparison"},
            {"sequence": 3, "event": "Serialize/parse-check, flush and atomically publish own invocation with no overwrite; independent readback is next"}
        ],
        "publisher_script": ref(Path(__file__).relative_to(ROOT))
    }
    for x in originals + inputs + record["governing"]:
        assert ref(x["path"]) == x
    b = encode(record)
    print(json.dumps(publish(BASE / "attempt.json", b)))
