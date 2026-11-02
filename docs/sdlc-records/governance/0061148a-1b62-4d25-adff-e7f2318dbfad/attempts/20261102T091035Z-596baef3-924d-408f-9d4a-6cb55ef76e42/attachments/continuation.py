import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[7]
os.chdir(ROOT)
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T091035Z-596baef3-924d-408f-9d4a-6cb55ef76e42"
CYCLE = "GOV-REMEDIATION-PROSPECTIVE-001"
PARENT = Path("docs/sdlc-records/governance") / WORK / "attempts"
BASE = PARENT / ATTEMPT
PRIOR = PARENT / "20261102T090405Z-a7fe416c-9a1d-4153-9c46-180a65e86436"
APPLICATION_ID = "20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31"
APPLICATION = PARENT / APPLICATION_ID
TARGET = APPLICATION / "attachments/GOV-AUD-20261102-001-linked-clarification.md"
PAYLOAD = PRIOR / "attachments/proposed-linked-clarification.md"
PAYLOAD_SHA = "8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
PUBLISHER = ".github/agents/governance-amendment-application.agent.md"
PUBLISHER_SHA = "F9E76A0061A85D3DDCF7BA3AD0BAF62A67D6C05B7F1E4DB0EFDF4E4BD55BB06D"
START = "Yes, initiate the bounded Corrective Change Decision continuation for GOV-AUD-20261102-001 only"
DESIGNATION = "Designate the recommended publisher and bounded scope above; do not approve or start Application"
STATUS = "FINDING ACCEPTED \u2014 OTHER GOVERNED ARTIFACT CHANGE REQUIRED"

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": p.as_posix(), "sha256": sha(b), "bytes": len(b)}

def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args]).decode().strip()

def encode(d):
    b = (json.dumps(d, ensure_ascii=True, indent=2) + "\n").encode()
    assert json.loads(b) == d
    return b

def common(kind):
    return {
        "schema_version": "1.0", "record_type": kind, "record_id": ATTEMPT + ":" + kind,
        "work_id": WORK, "attempt_id": ATTEMPT, "cycle_id": CYCLE, "cycle_number": 1,
        "creator": ATTEMPT, "role": "Corrective Change Decision",
        "process": "Corrective Change Decision & Plan Update",
        "subject_type": "FINDING", "finding_id": "GOV-AUD-20261102-001",
        "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "clock_basis": "Current host UTC record-preparation sample, not exact publication time",
    }

def publish(p, b):
    p = Path(p)
    assert p.is_relative_to(BASE) and not p.is_relative_to(APPLICATION)
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

def source_manifest():
    return [ref(p) for top in [Path(".github"), Path("docs"), Path("README.md")]
            for p in ([top] if top.is_file() else sorted(top.rglob("*")))
            if p.is_file() and not p.is_relative_to(BASE)]

def absent():
    # lexists also rejects a dangling link; this is a point-in-time base observation.
    assert not os.path.lexists(APPLICATION), APPLICATION
    assert not os.path.lexists(TARGET), TARGET
    return {
        "path": TARGET.as_posix(), "presence": "ABSENT", "base_sha256": None, "base_bytes": None,
        "base_semantics": "No existing bytes; not an empty-file fingerprint",
        "application_attempt_path": APPLICATION.as_posix(), "application_attempt_presence": "ABSENT",
        "observation_method": "Current non-mutating os.path.lexists on exact target and designated Application attempt; both false",
        "condition": "Recheck the entire target set immediately before any approved Application write; same-filesystem no-overwrite publication; any collision/drift requires stop, not alternate target",
        "not_a_reservation": True,
    }

def actual_checks(obj, origin, checks):
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str) and len(obj["sha256"]) == 64:
            rr = ref(obj["path"])
            assert rr["sha256"] == obj["sha256"].upper(), (origin, obj)
            if "bytes" in obj:
                assert rr["bytes"] == obj["bytes"], (origin, obj)
            checks.append({"origin": origin, "reference": rr, "outcome": "PASS"})
        for k, v in obj.items():
            actual_checks(v, origin + "/" + k, checks)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            actual_checks(v, origin + "/" + str(i), checks)

def unchanged(inv):
    before = inv["repository"]["source_manifest"]
    assert source_manifest() == before, "Pre-existing content/path-set drift"
    assert git("rev-parse", "HEAD") == inv["repository"]["head"]
    assert git("branch", "--show-current") == inv["repository"]["branch"]
    assert git("status", "--short") == inv["repository"]["status_porcelain"]
    absent()
    return {"files_compared": len(before), "all_bytes_paths_head_branch_status_match": True,
            "only_excluded_scope": BASE.as_posix(), "future_application_still_absent": True,
            "limitations": "Endpoint observations only; cannot exclude transient same-principal tampering, unobserved external writers or prove exhaustive execution history"}

def qualify():
    assert ROOT == Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ") and os.name == "nt"
    previous_inv = json.loads((PRIOR / "attempt.json").read_bytes())
    governing = previous_inv["governing"]
    for rr in governing:
        assert ref(rr["path"]) == rr
    assert git("rev-parse", "HEAD") == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert git("remote", "get-url", "origin") == "https://github.com/ScalableParimal/SupportIQ.git"
    assert not Path("docs/sdlc-records/product", WORK).exists()
    assert ref(PUBLISHER) == {"path": PUBLISHER, "sha256": PUBLISHER_SHA, "bytes": 1636}
    predecessor = []
    for p, h in {
        "report.md": "15FB06BDE62969F3C67CFE1F069E7BD26E0F5C7739CE246567AF3EC815DFA5CE",
        "result.json": "674DCAB5C85817EF07952F00ECB2DCA829649BAFDC82C50D40D98AF6C101EEDE",
        "attachments/proposed-linked-clarification.md": PAYLOAD_SHA,
    }.items():
        rr = ref(PRIOR / p)
        assert rr["sha256"] == h
        predecessor.append(rr)
    assert ref(PAYLOAD)["bytes"] == 3438
    # Invocation qualification only: prior terminal metadata, not report substance.
    previous_result = json.loads((PRIOR / "result.json").read_bytes())
    assert previous_result["execution_termination"] == "COMPLETED"
    assert previous_result["decision_status"] == STATUS and not previous_result["correction_applied"]
    authorization = {
        "fresh_human_continuation_start": START,
        "fresh_human_publisher_designation_verbatim": DESIGNATION,
        "source": "Actual current user message supplies/relays the two distinct fresh Human statements and the exact presented designation scope; no authenticated platform message identity or event time exposed",
        "attribution": "Human decisions received through current user instruction; not invented by this actor",
        "designated_publisher": {"role": "Governance Amendment Application", "definition": ref(PUBLISHER),
                                "future_attempt_identity": APPLICATION_ID, "future_actor_owned_scope": APPLICATION.as_posix(),
                                "exact_substantive_target": TARGET.as_posix(),
                                "permitted_other_outputs": "Publisher's own required invocation/checkpoint/report/result/evidence records only",
                                "one_time_subject": "GOV-AUD-20261102-001 only; same Work ID/cycle/Cycle 1",
                                "distinctness_conditions": "Distinct from preparer/verifier/reviewer/Orchestrator/active barred Remediation actor",
                                "designation_only": True, "capability_claim": False, "application_started": False},
        "approval_granted": False, "application_start_granted": False,
        "scope": "Only bounded continuation to fix exact destination/ABSENT base and finalize unchanged-payload approval package in this NEW decision attempt; no Application directory or publication",
        "root_adoption": {
            "url": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
            "author": "ScalableParimal", "author_id": 226102895, "association": "OWNER",
            "created_at": "2026-10-30T12:31:51Z", "updated_at": "2026-10-30T12:31:51Z",
            "decision_body_sha256": previous_inv["authorization"]["root_adoption"]["decision_body_sha256"],
            "current_check": "GitHub issue_read get_comments during this continuation qualification resolves unchanged OWNER root adoption with matching HEAD/Master fingerprints; initial Audit-only start not reused",
        },
        "reservation": previous_inv["authorization"]["reservation"],
    }
    inv = common("invocation")
    inv.update({
        "status": "QUALIFIED; independent readback required before substantive comparison",
        "actor_identity": {"invocation": ATTEMPT, "definition": ref(".github/agents/corrective-change-decision.agent.md"),
                           "runtime": "Current direct continuation invocation; no separate harness runtime ID exposed; this actor is not a competing writer"},
        "repository": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT), "head": git("rev-parse", "HEAD"),
                       "branch": git("branch", "--show-current"), "status_porcelain": git("status", "--short"), "source_manifest": source_manifest()},
        "output_scope": BASE.as_posix(), "predecessor": predecessor,
        "authorization": authorization, "governing": governing,
        "qualification": {
            "effective_identity": subprocess.check_output(["whoami"]).decode().strip(),
            "token_sid": "S-1-5-21-2809803128-1021655904-3966773769-1002",
            "current_checks": [
                "Current whoami /user and parent ACL inspection; Authenticated Users Allow Modify/Synchronize; no observed deny",
                "Current source reads, JSON parser, SHA-256, Git state and parent enumeration succeeded",
                "Current Python 3.14.7 Windows; UTF-8 serializer/parse, exact byte checks, fsync and same-filesystem os.rename refusing existing destination",
                "Only own partial records may be written; no source write probe",
                "Existing Work ID/root evidence and prior terminal metadata validated; future designated Application directory absent",
                "No other actor dispatched or concurrent writer reported by fresh Human start; historical in_progress records alone do not prove live writer",
            ],
            "permitted_publication_route": "Own .partial file validate/flush/fsync then same-filesystem Windows no-overwrite os.rename, independent subsequent readback",
            "limitations": "Write-capable shared OS principal, no enforced sandbox, exhaustive execution log, coordinated no-edit window, repository lock or continuous writer observation. Endpoint hashes cannot exclude transient same-principal tampering.",
        },
        "qualification_base_absence": absent(),
        "bootstrap_status": "Existing adopted governance root; Master texts candidate/unadopted; normal non-Master corrective workflow permitted before baseline adoption; no product baseline",
        "publisher_script": ref(Path(__file__).relative_to(ROOT)),
        "ordered_ledger": [
            "Q1: refresh unchanged governing instructions; current identity/ACL/Git, root adoption and source state",
            "Q2: machine-hash predecessor identities and payload; inspect terminal recovery metadata and designation binding; no substantive report comparison",
            "Q3: serialize/parse-check own invocation; validate all bindings, flush and no-overwrite publish; independent readback must precede substantive work",
        ],
    })
    actual_checks(inv, "invocation_prepublication", [])
    assert source_manifest() == inv["repository"]["source_manifest"]
    print(json.dumps(publish(BASE / "attempt.json", encode(inv))))

if __name__ == "__main__":
    assert sys.argv[1:] == ["qualify"]
    qualify()
