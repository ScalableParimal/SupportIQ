import sys
sys.dont_write_bytecode = True
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[7]
os.chdir(ROOT)
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ID = "20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed"
PARENT = Path("docs/sdlc-records/governance") / WORK / "attempts"
BASE = PARENT / ID
FAILED = PARENT / "20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31"
PRIOR = PARENT / "20261102T091035Z-596baef3-924d-408f-9d4a-6cb55ef76e42"
PAYLOAD = PARENT / "20261102T090405Z-a7fe416c-9a1d-4153-9c46-180a65e86436/attachments/proposed-linked-clarification.md"
PAYLOAD_HASH = "8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
OLD_TARGET = FAILED / "attachments/GOV-AUD-20261102-001-linked-clarification.md"
START = "Initiate the bounded Corrective Change Decision continuation to prepare recovery for this failed Application only; no application"
STATUS = "FINDING ACCEPTED \u2014 OTHER GOVERNED ARTIFACT CHANGE REQUIRED"

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": sha(b)}

def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args]).decode().strip()

def common(kind):
    return {"schema_version": "1.0", "record_type": kind, "record_id": ID + ":" + kind,
            "work_id": WORK, "attempt_id": ID, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
            "cycle_number": 1, "creator": ID, "role": "Corrective Change Decision",
            "process": "Corrective Change Decision & Plan Update", "subject_type": "FINDING",
            "finding_id": "GOV-AUD-20261102-001",
            "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "clock_basis": "Host UTC preparation sample, not filesystem publication time"}

def encode(d):
    # All records must use JSON-native structures; do not normalize away mismatches.
    b = (json.dumps(d, ensure_ascii=True, indent=2) + "\n").encode()
    assert json.loads(b) == d
    return b

def publish(p, b):
    p = Path(p)
    assert p.is_relative_to(BASE)
    p.parent.mkdir(parents=True, exist_ok=True)
    assert not p.exists()
    tmp = p.with_name(p.name + ".partial")
    with tmp.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == b
    os.rename(tmp, p)
    assert p.read_bytes() == b
    return ref(p)

def manifest():
    return [ref(p) for top in [Path(".github"), Path("docs"), Path("README.md")]
            for p in ([top] if top.is_file() else sorted(top.rglob("*")))
            if p.is_file() and not p.is_relative_to(BASE)]

def checks(x, label, out):
    if isinstance(x, dict):
        if isinstance(x.get("path"), str) and isinstance(x.get("sha256"), str) and len(x["sha256"]) == 64:
            actual = ref(x["path"])
            assert actual["sha256"] == x["sha256"].upper(), (label, x)
            if "bytes" in x:
                assert actual["bytes"] == x["bytes"], (label, x)
            out.append({"origin": label, "actual_reference": actual, "outcome": "PASS"})
        for k, v in x.items():
            checks(v, label + "/" + k, out)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            checks(v, label + "/" + str(i), out)

def unchanged(inv):
    assert manifest() == inv["repository"]["manifest"]
    assert git("rev-parse", "HEAD") == inv["repository"]["head"]
    assert git("branch", "--show-current") == inv["repository"]["branch"]
    assert git("status", "--short") == inv["repository"]["status"]
    assert not os.path.lexists(OLD_TARGET)
    return {"files": len(inv["repository"]["manifest"]), "all_bytes_paths_head_branch_status_match": True,
            "old_payload_target_absent": True, "exclusion": BASE.as_posix(),
            "limitation": "Point-in-time only; transient same-principal tampering/unobserved concurrent writes cannot be excluded; no exhaustive execution log"}

def qualify():
    assert ROOT == Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ") and os.name == "nt"
    prior_inv = json.loads((PRIOR / "attempt.json").read_bytes())
    for rr in prior_inv["governing"]:
        assert ref(rr["path"]) == rr
    assert git("rev-parse", "HEAD") == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert git("remote", "get-url", "origin") == "https://github.com/ScalableParimal/SupportIQ.git"
    inputs = []
    for p, h in {
        FAILED / "report.md": "2FADAD89CB3A0434E9C11C09D2F8640AF6C1193EA8601EF4C099300D20977670",
        FAILED / "result.json": "B866C146CF2060E0CD12A0E085C9B252C14A8F131ADF820E6D154BA70D92D260",
        FAILED / "evidence/failure-evidence.json": "5212B6E494D4174162484EA68D78F4EE448F9D8F78245B07C4B3BFB8DCF40552",
        PRIOR / "report.md": "581358B61D54BE3A44C9636DDEFB8D5A53DA1411160FCB23E57C42D6FF671D38",
        PRIOR / "result.json": "9A7D6E611DCD5821F3FE83E2D2BCB5250D401F49FA475D160BFAC47DE64917A7",
        PAYLOAD: PAYLOAD_HASH,
    }.items():
        rr = ref(p)
        assert rr["sha256"] == h
        inputs.append(rr)
    assert ref(PAYLOAD)["bytes"] == 3438 and not os.path.lexists(OLD_TARGET)
    # Terminal identity/status metadata only, not failure analysis before invocation.
    failure_metadata = json.loads((FAILED / "result.json").read_bytes())
    terminal_status = {k: v for k, v in failure_metadata.items()
                       if k in ["execution_termination", "outcome", "application_outcome", "status"]}
    inv = common("invocation")
    inv.update({
        "status": "QUALIFIED; independent readback required before substantive recovery comparison",
        "repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
                       "head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
                       "status": git("status", "--short"), "manifest": manifest()},
        "actor_identity": {"definition": ref(".github/agents/corrective-change-decision.agent.md"),
                           "invocation": ID, "runtime": "Current direct recovery decision invocation; no separate harness ID exposed"},
        "output_scope": BASE.as_posix(), "governing": prior_inv["governing"], "inputs": inputs,
        "authorization": {
            "fresh_human_start": START, "source": "Actual current user message; authenticated platform message identity/time not exposed",
            "scope": "Recovery decision/proposal only for failed Application of GOV-AUD-20261102-001; preserve all final records; no application or downstream process",
            "reported_prior_exact_approval": "Human explicitly approved complete section 4 of report SHA256 581358B61D54BE3A44C9636DDEFB8D5A53DA1411160FCB23E57C42D6FF671D38 then separately started Application; current user reports this history; resolve actual Application evidence after readback",
            "recovery_change_approved": False, "retry_started": False,
            "root_adoption": {"url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                              "author": "ScalableParimal", "association": "OWNER", "author_id": 226102895,
                              "created_at": "2026-10-30T12:31:51Z", "updated_at": "2026-10-30T12:31:51Z",
                              "current_check": "GitHub issue_read during current qualification resolves unchanged OWNER root adoption, matching current HEAD and three Master fingerprints; initial Audit-only start not reused"},
            "reservation": prior_inv["authorization"]["reservation"],
        },
        "qualification": {
            "identity": subprocess.check_output(["whoami"]).decode().strip(),
            "token_sid": "S-1-5-21-2809803128-1021655904-3966773769-1002",
            "current_checks": [
                "Current whoami /user, attempts-parent ACL: Authenticated Users Allow Modify/Synchronize; no observed deny",
                "Current source/parent reads, enumeration, SHA-256, Git and JSON parse succeeded",
                "Python on Windows; JSON-native serialize/parse self-test, fsync, atomic same-filesystem no-overwrite rename and exact-byte readback route",
                "No source write-probe; only own .partial publication",
                "Existing Work ID reservation/root resolved; prior terminal failure is not live work; historical in_progress does not prove a live writer",
                "This runtime is this actor, not a competitor; no agent dispatched or concurrent writer reported by Human start",
            ],
            "limits": "Write-capable shared OS principal; no sandbox/no-edit window/repository lock/continuous monitoring/exhaustive log. Endpoint hashes cannot exclude transient same-principal tampering.",
        },
        "predecessor_terminal_metadata": terminal_status,
        "bootstrap_status": "Governance root adopted; Master baseline candidate/unadopted; normal non-Master corrective workflow permitted; no product baseline",
        "serializer_self_test": json.loads(encode({"differences": [[27, 63, 167], [42, 63, 167]], "check": True})),
        "publisher_script": ref(Path(__file__).relative_to(ROOT)),
        "ordering": ["Q1 current governance/qualification/root/state/hash checks only",
                     "Q2 validated own invocation publish; no substantive failure/source analysis yet",
                     "Q3 independent invocation readback required next; only then recovery comparison"],
    })
    checks(inv, "invocation_before_publication", [])
    assert manifest() == inv["repository"]["manifest"]
    print(json.dumps(publish(BASE / "attempt.json", encode(inv))))

if __name__ == "__main__":
    qualify()
