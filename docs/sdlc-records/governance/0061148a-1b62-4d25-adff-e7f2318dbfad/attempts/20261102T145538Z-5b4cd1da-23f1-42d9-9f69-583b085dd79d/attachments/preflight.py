import os, json, hashlib, subprocess, datetime
from pathlib import Path

ROOT = Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d"
BASE = Path("docs/sdlc-records/governance") / WORK / "attempts"
OWN = BASE / ATTEMPT
INV = BASE / "20261102T141609Z-4e74248e-a440-4617-8c17-61f31f2ff9c9"
COORD = BASE / "20261102T132628Z-e9227c1a-70ab-4afc-87e2-49eca280b879"
AUDIT = BASE / "20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def ref(path):
    p = Path(path)
    b = (ROOT / p).read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": sha(b)}

def serialize(obj):
    b = (json.dumps(obj, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")
    assert json.loads(b) == obj
    return b

def publish(path, data):
    p = ROOT / path
    assert p.is_relative_to(ROOT / OWN), p
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    partial = p.with_name(p.name + ".partial")
    with partial.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == data
    if p.suffix == ".json":
        assert serialize(json.loads(partial.read_bytes())) == data
    assert not p.exists()
    os.rename(partial, p)  # Windows same-volume atomic rename fails if destination exists.
    assert p.read_bytes() == data
    return ref(path)

def command(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()

def main():
    os.chdir(ROOT)
    assert os.name == "nt"
    assert os.environ["COPILOT_AGENT_SESSION_ID"] == "1684b491-8eea-41fb-864d-541e7920e172"
    assert command("git", "rev-parse", "--show-toplevel").lower() == str(ROOT).replace("\\", "/").lower()
    assert command("git", "remote", "get-url", "origin") == "https://github.com/ScalableParimal/SupportIQ.git"
    assert command("git", "rev-parse", "HEAD") == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert not (ROOT / "docs/sdlc-records/product" / WORK).exists()
    expected = [
        (INV / "report-revision-0002.md", 21951, "1B298794D8AA503E4C18AA3730754FA170D6196B7745160390BB9C68246D1365"),
        (INV / "result-revision-0002.json", 4974, "41F442FA05C1472939889612DF43307E39E91883F75404C90D6AA1965A5248EB"),
        (INV / "evidence/evidence-rev-1.json", 12658, "72B356B60629910EFC499D7E4693A32A764217C9C5642DBBE8D18E5B54A6BA05"),
        (INV / "checkpoint-0003.json", 4779, "910BBE2C56BF871DD8AD4BDF1EB9007D0BC3E369461B36C45FA429CF15D98277"),
        (INV / "evidence/input-manifest.json", 165221, "0E18596FBB7E41B56CD960234A3C39434ED7AD602AFF7DCAF925283B37419400"),
        (COORD / "report-revision-0001.md", None, "5FE8350E49986DA8E910D591181243C4184D8EB303259ACEBA848D2E4E544C0C"),
        (COORD / "result-revision-0002.json", None, "7A569DFDAE43885614BA9653AEBBB0FD6373297723037E8044CC417E2AD62D94"),
        (COORD / "handoffs/GOV-AUD-20261102-003.json", None, "2FFA0524A31614B95E65279630FBA63AE06E6025380D1F58C757B4EC22CBC153"),
        (COORD / "handoffs/GOV-AUD-20261102-004.json", None, "61FED7ADE5C3099CCF8EF8FA03D45372B1FD88BAD68539FB317482F2F6F78894"),
        (AUDIT / "report.md", 95024, "088A36B865B3B8D7773A3A6D1D5B41C14CBF2FA25E4A4FCAB2B49B2163495576"),
        (AUDIT / "result.json", 61780, "9C4F37321EB63C67D45DD2F698F50B75FC1CBC95BEFA5EA7DFB30663E5A71B70"),
        (AUDIT / "evidence/audit-evidence.json", 393511, "83F42FB9CCF86558B8EAB5068FD30FC344291A064B3C4BAAA143EDC54FD75F88"),
        (Path(".github/agents/sdlc-governance-remediation.agent.md"), 49225, "404AF9126BC310AEA79BA7616AB8E25C0AD5EE7F48B360F1AF515EA4DC9F942F"),
    ]
    validated = []
    for path, size, digest in expected:
        r = ref(path)
        assert len(digest) == 64
        assert r["sha256"] == digest, r
        assert size is None or r["bytes"] == size, r
        validated.append(r)
    manifest = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or ".git" in p.relative_to(ROOT).parts or p.is_relative_to(ROOT / OWN):
            continue
        manifest.append(ref(p.relative_to(ROOT)))
    assert any(r["path"] == ".github/skills/corrective-change-decision/SKILL.md" for r in manifest)
    assert any(r["path"] == ".github/agents/corrective-change-decision.agent.md" for r in manifest)
    # Validate that all pre-existing inputs stayed stable over manifest construction.
    assert all(ref(r["path"]) == r for r in manifest)
    m = {"schema_version": "1.0", "record_type": "input_manifest", "record_id": ATTEMPT + ":input-manifest",
         "work_id": WORK, "attempt_id": ATTEMPT, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001", "cycle": 1,
         "creator": "Corrective Change Decision Agent", "created_at_utc": now(),
         "scope": "All pre-existing repository files including hidden .github and all upstream/history records; .git internals and this own attempt excluded. Inventory is not a claim of substantive reliance or full-file reading.",
         "files": manifest}
    mr = publish(OWN / "evidence/input-manifest.json", serialize(m))
    actor = {"role": "Corrective Change Decision Agent",
             "runtime_agent_id": "4d0c3747-fde6-48c7-b125-5adb2af5b80c",
             "runtime_agent_id_basis": "Only running agent in list_agents all-scope registry matches this assigned invocation; registry identity distinguished from current host session and OS principal. Role authority comes from current developer assignment and hashed definition, not display title.",
             "copilot_agent_session_id": os.environ["COPILOT_AGENT_SESSION_ID"],
             "host_session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
             "effective_windows_principal": command("whoami"),
             "agent_definition": ref(".github/agents/corrective-change-decision.agent.md"),
             "skill": ref(".github/skills/corrective-change-decision/SKILL.md")}
    a = {"schema_version": "1.0", "record_type": "corrective_change_decision_invocation",
         "record_id": ATTEMPT + ":invocation", "work_id": WORK, "attempt_id": ATTEMPT,
         "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001", "cycle": 1,
         "process": "Corrective Change Decision & Plan Update", "subject_type": "FINDING",
         "finding_ids": ["GOV-AUD-20261102-003", "GOV-AUD-20261102-004"],
         "creator": actor, "created_at_utc": now(), "clock_basis": "Python datetime.now UTC at record preparation; not publication time",
         "repository_context": {"canonical": "ScalableParimal/SupportIQ", "root": str(ROOT),
             "head": command("git", "rev-parse", "HEAD"), "branch": command("git", "branch", "--show-current"),
             "working_tree_status": command("git", "--no-pager", "status", "--short"),
             "exact_source_manifest": mr},
         "persistence": {"root": "docs/sdlc-records/governance/", "actor_owned_scope": OWN.as_posix() + "/**",
             "existing_work_id": True, "product_collision": False,
             "root_adoption": {"source": "https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                 "validation": "Fresh GitHub issue_read get_comments returned author_association OWNER, user ScalableParimal id 226102895, comment id 6522916236; created/updated 2026-10-30T12:31:51Z. Exact repository/head/root/work and three Master bindings validated.",
                 "initial_audit_only": True, "continuation_authority": "Current fresh Human start and existing Work ID, not reuse of initial bootstrap start",
                 "master_comparison_authority": "SDLC_GOVERNANCE section 3 normal findings lifecycle before prospective Master baseline adoption; no Master or product-root adoption claimed"}},
         "human_stage_start": {"actual_wording": "Yes, initiate Corrective Change Decision & Plan Update for these two findings only; prepare proposals without applying changes or starting later stages",
             "source": "Actual Human response supplied in current user request, attributed to parent conversation; no authenticated message ID or original decision time exposed",
             "decision_time": None, "authenticated_author_id": None,
             "presentation_binding": {"work_id": WORK, "cycle": 1, "finding_ids": ["GOV-AUD-20261102-003", "GOV-AUD-20261102-004"],
                  "investigation_report": validated[0], "investigation_result": validated[1]},
             "scope": "Separate assessment of both findings; coordinated minimal proposal if lawful; no application or later stages",
             "not_patch_approval": True},
         "human_selected_proposal_directions": [
             {"finding_id": "GOV-AUD-20261102-003", "exact_selection": "Use the lifecycle-qualified initial-clarification and approved-source paths described above",
              "binding": "Initial immutable but unapproved Requirement clarification remains unapproved, preserves lineage; subsequent Analysis, complete Verification and separate formal Human Requirement Approval; preserve approved-source update path"},
             {"finding_id": "GOV-AUD-20261102-004", "exact_selection": "Use stage-specific current attempts and planned-only future assurance identities as described above",
              "binding": "Future verifier/reviewer planned identity-only; actual attempts/current capabilities/fresh starts at respective stages; preserve independence and assurance gates"}],
         "required_inputs_validated": validated, "input_manifest": mr,
         "qualification": {"capabilities": {
             "read": "All manifest inputs opened as bytes; hashes computed twice without source mutation",
             "hash_check": "hashlib SHA-256 with exact size/digest checks against canonical handoff; canonical JSON native object strict serialization/parse equality",
             "publication_route": "Current NTFS ACL on existing attempts parent: effective principal int-scl-010\\parimal; owner INT-SCL-010\\Parimal, Authenticated Users Modify; own-record publication only is permitted. Evidence manifest successfully flushed/validated and same-filesystem renamed without overwrite/read back.",
             "runtime": "Python execution and read-only git identity/state commands succeeded in current environment",
             "nonmutation": "Procedural, not sandbox-enforced; same-principal tampering/transient changes not excluded; no exhaustive event log"},
             "independence": "Proposal preparer only; no application, independent verification/review or audit performed. Future actors must be distinct.",
             "competing_attempts": "all-scope agent registry shows this as sole running actor; 44 idle historical agents do not establish active conflicting writes. Existing records inventoried; registry not exhaustive system-wide proof."},
         "authorized_scope": {"write": [OWN.as_posix() + "/**"], "all_other_paths": "read-only",
             "exclusions": ["source amendments", "application", "later stages", "product work", "Master adoption", "reopening GOV-AUD-20261102-001/002 or historical GOV001/002", "staging", "commit", "push"]},
         "pre_assessment_state": "Qualification only; substantive finding assessment not started; must independently read back invocation before assessment"}
    # Verify the original bootstrap Master bindings without adopting them.
    for p,h in [
        ("SDLC_GOVERNANCE.md","79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B"),
        ("SDLC_ARTIFACT_GOVERNANCE.md","6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860"),
        ("SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md","08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C")]:
        assert ref(Path("docs/ai/sdlc") / p)["sha256"] == h
    print(json.dumps({"manifest": mr, "invocation": publish(OWN / "attempt.json", serialize(a)), "inputs": len(manifest), "state": "PUBLISHED; separate fresh readback required"}, indent=2))

if __name__ == "__main__":
    main()
