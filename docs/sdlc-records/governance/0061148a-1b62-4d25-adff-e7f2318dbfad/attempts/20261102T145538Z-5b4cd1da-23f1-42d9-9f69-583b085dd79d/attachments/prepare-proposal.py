import sys, json, difflib
from pathlib import Path
from preflight import ROOT, WORK, ATTEMPT, OWN, INV, COORD, AUDIT, ref, sha, now, serialize, publish, command

STATUS = "FINDING ACCEPTED — OTHER GOVERNED ARTIFACT CHANGE REQUIRED"
F003 = "GOV-AUD-20261102-003"
F004 = "GOV-AUD-20261102-004"
REPORT = OWN / "report.md"
RESULT = OWN / "result.json"
PROPOSAL = OWN / "attachments/exact-proposal.json"
PATCH = OWN / "attachments/minimal.patch"
EVIDENCE = OWN / "evidence/decision-evidence.json"
GUIDE = "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md"
PROMPT = "docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md"
REQUEST = "docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md"
SKILL = ".github/skills/requirement-update/SKILL.md"
CCA = "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md"
CHANGES = {}

def change(path, before, after):
    CHANGES.setdefault(path, []).append((before, after))

change(GUIDE,
       "1. The current approved Requirement version and its version ID and SHA-256.",
       "1. The source Requirement path, immutable version ID, and SHA-256, with its lifecycle status and applicable approval evidence: either the identified unapproved source for initial analysis clarification before first Human Requirement Approval, or the current approved Requirement for an approved-source change.")
change(GUIDE,
       "5. The subject type: Finding-led corrective update or human-requested, non-finding Requirement amendment. For a non-finding request, use the existing request record and establish its source, scope, decision authority, disposition, and rationale under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.",
       "5. The update context: Initial Analysis Clarification (pre-approval), Finding-led corrective update, or human-requested, non-finding Requirement amendment. For an approved-source non-finding amendment, use the existing request record and establish its source, scope, decision authority, disposition, and rationale under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.")
change(GUIDE,
       "If a material decision is still unresolved, do not silently decide it.",
       "For Initial Analysis Clarification, bind the initial Requirement Analysis questions and explicit human answers/decisions, and require an explicit request to perform Requirement Update. Preserve the immutable source and version lineage under SDLC_ARTIFACT_GOVERNANCE.md section 8.4. The resulting version remains unapproved; approval of clarification decisions is not Human Requirement Approval. Follow section 16: subsequent Requirement Analysis, complete independent Requirement Analysis Verification, resolution of findings/decisions, then separate formal Human Requirement Approval before planning as approved. This branch neither permits implementation against an unapproved Requirement nor bypasses applicable finding-led corrective controls; a change to an already-approved Requirement must use the approved-source path. If source lifecycle status or applicable approval evidence cannot be established, stop and request clarification.\n\nIf a material decision is still unresolved, do not silently decide it.")
change(PROMPT,
       "1. The subject type: Finding-led corrective update or human-requested, non-finding Requirement amendment.\n2. The current approved Requirement version path, immutable version ID, and SHA-256.",
       "1. The update context: Initial Analysis Clarification (pre-approval), Finding-led corrective update, or human-requested, non-finding Requirement amendment.\n2. The source Requirement path, immutable version ID, SHA-256, lifecycle status, and applicable approval evidence, qualified by the initial-clarification or approved-source path in Guideline section 2.")
change(PROMPT,
       "6. For a human-requested non-finding amendment, the existing request details and responsible human decision, including scope, disposition, and rationale, as specified by SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.",
       "6. For an approved-source human-requested non-finding amendment, the existing request details and responsible human decision, including scope, disposition, and rationale, as specified by SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.\n\nFor Initial Analysis Clarification, provide the initial analysis questions, explicit human answers/decisions, and explicit update request under Guideline section 2. Do not invent a Finding or formal Requirement Approval. The resulting immutable version remains unapproved and follows the separate downstream stages below; a change to an already-approved Requirement must retain the approved-source path.")
change(REQUEST,
       "Subject Type:\n[FINDING-LED CORRECTIVE UPDATE / HUMAN-REQUESTED REQUIREMENT AMENDMENT (NON-FINDING)]\n\nCurrent approved Requirement version:\n[PATH / IMMUTABLE VERSION ID / SHA-256]",
       "Update context:\n[INITIAL ANALYSIS CLARIFICATION (PRE-APPROVAL) / FINDING-LED CORRECTIVE UPDATE / HUMAN-REQUESTED REQUIREMENT AMENDMENT (NON-FINDING)]\n\nSource Requirement version:\n[PATH / IMMUTABLE VERSION ID / SHA-256 / LIFECYCLE STATUS]\n\nSource path and approval evidence:\n[INITIAL CLARIFICATION: IDENTIFIED IMMUTABLE UNAPPROVED SOURCE BEFORE FIRST FORMAL HUMAN REQUIREMENT APPROVAL; OR APPROVED-SOURCE CHANGE: CURRENT APPROVED REQUIREMENT AND ITS APPROVAL EVIDENCE. FOLLOW GUIDELINE SECTION 2; UNESTABLISHED STATUS BLOCKS UPDATE.]\n\nFor initial analysis clarification:\n[INITIAL ANALYSIS/QUESTION REFERENCES / EXPLICIT HUMAN ANSWERS AND DECISIONS / EXPLICIT REQUEST TO PERFORM UPDATE. CLARIFICATION DECISIONS ARE NOT FORMAL REQUIREMENT APPROVAL; RESULT REMAINS UNAPPROVED PENDING SUBSEQUENT ANALYSIS, COMPLETE INDEPENDENT VERIFICATION, RESOLUTION, AND SEPARATE HUMAN REQUIREMENT APPROVAL.]")
change(REQUEST,
       "For a human-requested non-finding amendment, complete the existing request details:",
       "For an approved-source human-requested non-finding amendment, complete the existing request details:")
change(SKILL,
       "2. Establish the subject type and resolve the current approved Requirement version, immutable version ID, and SHA-256.\n3. For a human-requested non-finding amendment, resolve the existing request details, scope, responsible human decision, disposition, and rationale under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8; do not invent a Finding.",
       "2. Establish the update context and source lifecycle path under Guideline section 2; resolve the source Requirement path, immutable version ID, SHA-256, lifecycle status, and applicable approval evidence. Use the identified unapproved source only for initial analysis clarification before first formal approval; retain the current approved source for an approved-source change.\n3. For Initial Analysis Clarification, resolve the initial analysis questions, explicit human answers/decisions, and explicit update request; do not invent a Finding or formal Requirement Approval. For an approved-source human-requested non-finding amendment, resolve the existing request details, scope, responsible human decision, disposition, and rationale under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.")
change(SKILL,
       "1. Establish the current approved Requirement version as the immutable source and record its ID and SHA-256.\n2. Establish whether the update is Finding-led or a human-requested non-finding amendment.",
       "1. Establish the lifecycle-qualified immutable source under Guideline section 2 and record its path, version ID, SHA-256, status, and applicable approval evidence; stop if that source status cannot be established.\n2. Establish whether the update is Initial Analysis Clarification (pre-approval), Finding-led, or an approved-source human-requested non-finding amendment. Preserve the initial result as unapproved through the downstream gates in section 8; approved clarification decisions do not constitute Human Requirement Approval.")
change(CCA,
       "Actor and Human Approval fields (enhancement only): for proposal preparer, one-time initial applier [identity/environment/one-time scope], verifier, and reviewer, record the role/Agent definition repository-relative path and content SHA-256, each bound to that actor's own unique attempt record; record current runtime identity/environment separately. Check distinctness using the actor-identity bindings, not display name alone. Different OS identities, hosts, or repositories are not required unless an applicable, explicitly approved security boundary requires them. Qualification evidence [record path/ID/SHA-256 and capability observations]; approval decision/source/time; approved report fingerprint and exact targets. Each Application, Verification, Review, and Audit request must separately record its fresh attributable stage-start instruction; this is not part of or a substitute for patch approval.",
       "Actor and Human Approval fields (enhancement only; stage-specific): record the proposal preparer, intended one-time initial applier [identity/environment/one-time scope], intended verifier, and intended reviewer by role/Agent definition repository-relative path and content SHA-256. At proposal preparation, bind only the actual preparer to its own current unique attempt and record its current runtime identity/environment and qualification evidence [record path/ID/SHA-256 and capability observations] separately. The intended applier requires fresh exact Human Approval and one-time designation; no separate pre-existing qualification attempt is required. After its separate fresh Application stage-start, the applier must publish and integrity-check its own current attempt, identity, permissions, and role-specific capability evidence before any source write; before Application source work, both preparer and applier must be bound to their own attempts. Record future verifier/reviewer bindings as planned identity-only paths and hashes, not attempts, current runtime identities, capabilities, or stage starts; do not require, create, or publish their attempts before predecessor gates. Only after complete successful Application and a fresh Verification stage-start may the actual verifier publish its own attempt and current qualification; only after passing independent Verification and a fresh Review stage-start may the actual reviewer do so. Each actual verifier/reviewer definition path and hash must match its approved planned binding; mismatch blocks that stage pending updated attributable Human decision and exact approval. Follow the Governance Amendment Application controls for these bindings and gates. Check all four actors' distinctness using actor-identity bindings, not display name alone; the applier must also differ from the SDLC Process Orchestrator and any Governance Remediation actor barred from self-edit in its active cycle. Different OS identities, hosts, or repositories are not required unless an applicable, explicitly approved security boundary requires them. Record the approval decision/source/time, approved report fingerprint, and exact targets without treating approval/designation as capability evidence. Each Application, Verification, Review, and Audit request must separately record its fresh attributable stage-start instruction and each actual actor must qualify in its own current invocation under SDLC_ARTIFACT_GOVERNANCE.md section 33.1; stage-start is not part of or a substitute for patch approval.")

def metadata(kind):
    return {"schema_version": "1.0", "record_type": kind, "record_id": ATTEMPT + ":" + kind,
            "work_id": WORK, "attempt_id": ATTEMPT, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001",
            "cycle": 1, "process": "Corrective Change Decision & Plan Update",
            "creator": {"role": "Corrective Change Decision Agent", "runtime_agent_id": "4d0c3747-fde6-48c7-b125-5adb2af5b80c",
                        "copilot_agent_session_id": "1684b491-8eea-41fb-864d-541e7920e172"},
            "created_at_utc": now(), "clock_basis": "Current UTC at record preparation; no exact publication timestamp claimed"}

def check_inputs():
    a = json.loads((ROOT / OWN / "attempt.json").read_bytes())
    assert ref(OWN / "attempt.json")["sha256"] == "B5244B2C7C6A5F439E9C3694EC298F160FC15D023B02CBBD7660F30B2E5BEB85"
    assert ref(OWN / "evidence/input-manifest.json") == a["input_manifest"]
    m = json.loads((ROOT / a["input_manifest"]["path"]).read_bytes())
    for r in m["files"]:
        assert ref(r["path"]) == r, r["path"]
    existing = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                if p.is_file() and ".git" not in p.relative_to(ROOT).parts and not p.is_relative_to(ROOT / OWN)}
    assert existing == {r["path"] for r in m["files"]}, "Pre-existing inventory changed"
    assert command("git", "rev-parse", "HEAD") == a["repository_context"]["head"]
    assert command("git", "branch", "--show-current") == a["repository_context"]["branch"]
    assert command("git", "--no-pager", "status", "--short") == a["repository_context"]["working_tree_status"]
    assert sha((ROOT / ".git/index").read_bytes()) == "51D40838E46A8C974CD8D5B034AF87A2F170EC592D0C5CC8C57890100A8748B6"
    return a, m

def validate_references():
    checked = []
    def walk(x):
        if isinstance(x, dict):
            if isinstance(x.get("path"), str) and isinstance(x.get("sha256"), str) and len(x["sha256"]) == 64:
                p = (ROOT / x["path"]).resolve()
                assert p.is_relative_to(ROOT), p
                assert p.is_file(), p
                r = ref(p.relative_to(ROOT))
                assert r["sha256"] == x["sha256"].upper(), r
                assert "bytes" not in x or r["bytes"] == x["bytes"], r
                checked.append(r)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for path in [INV / "result-revision-0002.json", INV / "checkpoint-0003.json",
                 INV / "evidence/evidence-rev-1.json", COORD / "result-revision-0002.json"]:
        walk(json.loads((ROOT / path).read_bytes()))
    ir = json.loads((ROOT / INV / "result-revision-0002.json").read_bytes())
    assert ir["report"]["path"].endswith("report-revision-0002.md")
    assert ir["supersedes"]["path"].endswith("result-revision-0001.json")
    assert "supersedes report-revision-0001.md" in (ROOT / INV / "report-revision-0002.md").read_text("utf-8")
    assert {f["finding_id"] for f in ir["findings"]} == {F003, F004}
    cr = json.loads((ROOT / COORD / "result-revision-0002.json").read_bytes())
    assert "supersed" in json.dumps(cr).lower()
    return checked

def build():
    targets, diffs, afters = [], [], {}
    for path, replacements in CHANGES.items():
        base = (ROOT / path).read_bytes()
        assert not base.startswith(b"\xef\xbb\xbf")
        base.decode("utf-8", errors="strict")
        assert base.count(b"\r\n") == base.count(b"\n"), path
        after = base
        ops = []
        for before, replacement in replacements:
            old = before.replace("\n", "\r\n").encode("utf-8")
            new = replacement.replace("\n", "\r\n").encode("utf-8")
            assert after.count(old) == 1, (path, before)
            offset = after.index(old)
            after = after.replace(old, new, 1)
            ops.append({"before": old.decode("utf-8"), "after": new.decode("utf-8"),
                        "expected_occurrences": 1, "sequential_input_byte_offset": offset})
        assert after != base
        assert after.count(b"\r\n") == after.count(b"\n")
        assert after.endswith(b"\r\n") == base.endswith(b"\r\n")
        assert b"`n" not in after
        # Reconstruction from the actual native JSON object must be byte-exact.
        check = base
        for op in json.loads(serialize(ops)):
            before, new = op["before"].encode("utf-8"), op["after"].encode("utf-8")
            assert check.count(before) == 1
            assert check.index(before) == op["sequential_input_byte_offset"]
            check = check.replace(before, new, 1)
        assert check == after
        reverse = after
        for op in reversed(ops):
            new, old = op["after"].encode("utf-8"), op["before"].encode("utf-8")
            assert reverse.count(new) == 1
            reverse = reverse.replace(new, old, 1)
        assert reverse == base
        d = "".join(difflib.unified_diff(base.decode("utf-8").splitlines(keepends=True),
                                       after.decode("utf-8").splitlines(keepends=True),
                                       fromfile="a/" + path, tofile="b/" + path, n=3))
        diffs.append(d)
        afters[path] = after.decode("utf-8")
        targets.append({"path": path, "finding_ids": [F004 if path == CCA else F003],
                        "encoding": "UTF-8", "bom": False, "newline": "CRLF",
                        "base_final_newline": base.endswith(b"\r\n"),
                        "expected_after_final_newline": after.endswith(b"\r\n"),
                        "base_bytes": len(base), "base_sha256": sha(base),
                        "expected_after_bytes": len(after), "expected_after_sha256": sha(after),
                        "operation": "Apply sequential exact single-occurrence UTF-8 byte replacements; preserve all other bytes",
                        "replacements": ops})
    assert len(targets) == 5
    assert list(CHANGES) == [GUIDE, PROMPT, REQUEST, SKILL, CCA]
    assert "already-approved Requirement must use the approved-source path" in afters[GUIDE]
    assert "complete independent Requirement Analysis Verification" in afters[GUIDE]
    assert "before first formal approval" in afters[SKILL]
    assert "do not require, create, or publish their attempts before predecessor gates" in afters[CCA]
    assert "no separate pre-existing qualification attempt is required" in afters[CCA]
    patch = "".join(diffs).encode("utf-8")
    return targets, patch

def main():
    a, manifest = check_inputs()
    checked = validate_references()
    targets, patch = build()
    if "--preview" in sys.argv:
        print(patch.decode("utf-8"))
        print(json.dumps([{k:v for k,v in t.items() if k != "replacements"} for t in targets], indent=2))
        print("PREVIEW ONLY: no proposal/report/result publication; integrity checks PASS.")
        return
    assert "--publish" in sys.argv
    assert not (ROOT / REPORT).exists() and not (ROOT / RESULT).exists()
    cp = metadata("checkpoint")
    cp.update(sequence=1, phase="ASSESSMENT_AND_PROPOSAL_PREPARATION_COMPLETE",
              last_confirmed_boundary="Invocation separately fresh-read and validated before substantive assessment; now separate decisions and in-memory exact proposal reviewed",
              invocation=ref(OWN / "attempt.json"), input_manifest=a["input_manifest"],
              observed_evidence={"pre_existing_inputs": len(manifest["files"]), "nested_bindings_validated": len(checked),
                                 "proposal_target_count": len(targets), "exact_reconstruction_and_reverse_selftests": "PASS"},
              partial_effects="Own invocation/manifest/helpers only; no source or upstream writes",
              unfinished_work=["Publish exact proposal, evidence, canonical report and terminal result", "Fresh terminal readback"],
              pending_gate="Exact Human Approval and fresh one-time applier designation; no later stage authorized",
              safe_continuation="This actor may finish only its own decision records")
    cpr = publish(OWN / "checkpoint-0001.json", serialize(cp))
    roles = []
    for role, p, state in [
        ("proposal_preparer", ".github/agents/corrective-change-decision.agent.md", "ACTUAL_CURRENT_ATTEMPT"),
        ("intended_one_time_applier", ".github/agents/governance-amendment-application.agent.md", "PROPOSED_IDENTITY_ONLY_PENDING_FRESH_HUMAN_DESIGNATION"),
        ("planned_verifier", ".github/agents/independent-governance-verification.agent.md", "PLANNED_IDENTITY_ONLY"),
        ("planned_reviewer", ".github/agents/independent-governance-review.agent.md", "PLANNED_IDENTITY_ONLY")]:
        r = {"role": role, "definition": ref(p), "binding_state": state}
        if role == "proposal_preparer":
            r.update(attempt=ref(OWN / "attempt.json"), runtime_identity=a["creator"])
        else:
            r.update(actual_attempt=None, current_runtime_identity=None, current_capability_evidence=None,
                     fresh_stage_start=None, note="No future attempt or current qualification is asserted or created")
        roles.append(r)
    assert len({r["definition"]["path"] for r in roles}) == 4
    assert len({r["definition"]["sha256"] for r in roles}) == 4
    p = metadata("exact_governance_proposal")
    p.update(subject_type="FINDING", finding_ids=[F003,F004], state="PROPOSED_NOT_APPROVED_NOT_APPLIED",
             canonical_report={"path": REPORT.as_posix(), "record_id": ATTEMPT + ":corrective_decision_report"},
             investigation_report=ref(INV / "report-revision-0002.md"), investigation_result=ref(INV / "result-revision-0002.json"),
             scope="Five non-Master governance artifacts; F003 four-artifact Requirement Update bundle; F004 one enhancement actor-fields paragraph",
             exclusions=a["authorized_scope"]["exclusions"], targets=targets, actors=roles,
             patch_publication_path=PATCH.as_posix(),
             approval_route="Fresh exact Human Approval and fresh explicit one-time applier designation may be combined in one attributable decision. Neither is supplied. Every later process needs its own fresh start; no pre-existing applier qualification record or future assurance attempt is required.",
             byte_contract="Exact sequential replacements and byte/hash fields are binding; unified diff is the corresponding minimal presentation patch. All target UTF-8/CRLF/BOM/final-newline properties preserved.",
             no_master_change=True, no_product_change=True)
    pr = publish(PROPOSAL, serialize(p))
    patchref = publish(PATCH, patch)
    relied = [GUIDE,PROMPT,REQUEST,SKILL,CCA,
              "docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
              "docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md",
              "docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md",
              ".github/skills/corrective-change-decision/SKILL.md",
              ".github/agents/corrective-change-decision.agent.md",
              "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
              "docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md",
              "docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md",
              "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md",
              "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md",
              ".github/agents/governance-amendment-application.agent.md",
              ".github/agents/independent-governance-verification.agent.md",
              ".github/agents/independent-governance-review.agent.md",
              ".github/agents/sdlc-governance-remediation.agent.md",
              "docs/ai/sdlc/SDLC_GOVERNANCE.md","docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
              "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md"]
    e = metadata("decision_evidence")
    e.update(input_manifest=a["input_manifest"], invocation=ref(OWN / "attempt.json"),
             checkpoint=cpr, proposal=pr, patch=patchref, all_preexisting_input_count=463,
             source_inspection=[ref(x) for x in relied],
             upstream=[ref(INV / n) for n in ["report-revision-0002.md","result-revision-0002.json","checkpoint-0003.json","evidence/evidence-rev-1.json"]],
             coordinator=[ref(COORD/n) for n in ["report-revision-0001.md","result-revision-0002.json","handoffs/GOV-AUD-20261102-003.json","handoffs/GOV-AUD-20261102-004.json"]],
             audit=[ref(AUDIT/n) for n in ["report.md","result.json","evidence/audit-evidence.json"]],
             executed_checks={"nested_bindings": checked, "source_inventory_and_git_state": "PASS",
                              "strict_native_json_roundtrip": "PASS", "exact_reconstruction_and_reverse": "PASS",
                              "single_occurrence_replacements": "PASS", "encoding_newline_final_newline_preservation": "PASS",
                              "target_scope_exactly_five_non_Master_paths": "PASS"},
             preparation_corrections=[{"phase":"Unpublished proposal helper preview",
                                      "observed":"First strict nested-reference check encountered an existing path containing .. which Windows did not resolve as a readable long path",
                                      "correction":"Normalize the existing path with Path.resolve, require it to remain within the repository, then require existence, exact size and hash. No check removed or weakened; rerun passed before proposal/report/result publication",
                                      "authority_or_input_missing":False}],
             helpers=[ref(OWN/"attachments/preflight.py"),ref(OWN/"attachments/prepare-proposal.py")],
             classifications={"executed":"Current integrity, native JSON, in-memory proposal reconstruction, publication and readback checks only; not independent governance Verification or Review",
                              "source_inspection":"Current source bytes and applicable process/approval controls",
                              "reported":"Human start and selections as supplied; upstream investigation and audit conclusions remain process-owned",
                              "unverified":"Actual product lifecycle execution, premature assurance invocation, future actor capabilities or approvals; none asserted"},
             limitations=["Read-only boundary procedural, not sandbox-enforced; ACL permits Modify",
                          "No exhaustive trusted event log; same-principal tampering or transient mutation/reversion not excluded",
                          "Endpoint hashes establish observed bytes, not a continuous mutation-free history",
                          "Human chat decision source has no exposed authenticated message ID or original timestamp",
                          "Future actors' runtime identity/capability/attempt/start not yet available and not required before their stage"])
    er = publish(EVIDENCE, serialize(e))
    table = "\n".join("| `"+t["path"]+"` | "+str(t["base_bytes"])+" / `"+t["base_sha256"]+"` | "+str(t["expected_after_bytes"])+" / `"+t["expected_after_sha256"]+"` | "+str(t["base_final_newline"])+" |" for t in targets)
    roletext = "\n".join("- **"+r["role"]+"**: `"+r["definition"]["path"]+"`, "+str(r["definition"]["bytes"])+" bytes, SHA-256 `"+r["definition"]["sha256"]+"`; "+r["binding_state"]+"." for r in roles)
    report = f"""# Corrective Change Decision & Plan Update Report

Canonical record: `{ATTEMPT}:corrective_decision_report`  
Work ID: `{WORK}`  
Cycle: `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1  
Attempt: `{ATTEMPT}`  
Subject: FINDING — {F003} and {F004}, separately decided  
State: **PROPOSAL ONLY — NOT APPROVED — NOT APPLIED**

## 1. Execution context, authorization and source authority

Repository: ScalableParimal/SupportIQ, `C:\\PARIMAL_SHERE\\SCALABLE_SOLUTIONS\\SupportIQ`; HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`, branch `sdlc-framework-onboarding`. The exact uncommitted source state, hidden `.github`, and all pre-existing upstream/history records are bound by the 463-file input manifest `{a["input_manifest"]["path"]}`, SHA-256 `{a["input_manifest"]["sha256"]}`. `.git` internals and this own attempt are excluded from that inventory; Git HEAD/branch/status and index were checked separately. Inventory does not mean every file was substantively read.

The current role, Skill, Guideline, Prompt, Request, relevant Master sections, and coupled controls were loaded. No AGENTS.md, copilot-instructions.md or *.instructions.md was found. The fresh invocation `attempt.json` was validated, flushed, atomically published without overwrite, and independently read back in a separate tool call before substantive assessment. Invocation SHA-256: `B5244B2C7C6A5F439E9C3694EC298F160FC15D023B02CBBD7660F30B2E5BEB85`. The separate readback rehashed all 463 inputs successfully. `checkpoint-0001.json` records the subsequent completed assessment/proposal-preparation boundary, not a fabricated earlier timestamp.

Actual supplied Human start: “Yes, initiate Corrective Change Decision & Plan Update for these two findings only; prepare proposals without applying changes or starting later stages”. Presentation binds both finding IDs, this Work ID/cycle, and Investigation revision 0002. Source: actual Human response supplied in the current request from the parent conversation; no authenticated message/author ID or original decision time is exposed. None is invented.

Human's separately selected proposal directions:
- F003: “Use the lifecycle-qualified initial-clarification and approved-source paths described above”.
- F004: “Use stage-specific current attempts and planned-only future assurance identities as described above”.

These are policy-direction/proposal and process-start authorizations only, **not exact Human Approval, application designation, capability evidence, or a later-stage start**.

The existing governance root decision was freshly resolved through GitHub issue_read: https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236; author ScalableParimal, user ID 226102895, OWNER association; created/updated 2026-10-30T12:31:51Z. Its repository, HEAD, root, Work ID and all three Master fingerprints match. The initial bootstrap stage is not reused as authority for this process. Current start plus normal findings lifecycle provides bounded continuation. SDLC_GOVERNANCE §3 permits normal finding-led non-Master correction before baseline adoption. **The prospective Master baseline and product root remain unadopted**; current Master bytes are comparison authority, not a claimed adopted product baseline.

Pre-existing six tracked modifications and historical records remain unchanged. The running-agent registry identified this assigned actor as `4d0c3747-fde6-48c7-b125-5adb2af5b80c`, distinct from the host session and `COPILOT_AGENT_SESSION_ID` `1684b491-8eea-41fb-864d-541e7920e172`; role proof is the current assignment plus hashed role definition, not the session title. Only this invocation was running in the observed registry; idle prior agents were not treated as competing writers. This is not exhaustive OS-wide liveness proof.

## 2. Canonical predecessor reconciliation and prior art

Investigation report: `{(INV/"report-revision-0002.md").as_posix()}`, SHA-256 `{ref(INV/"report-revision-0002.md")["sha256"]}`. Investigation result: `{(INV/"result-revision-0002.json").as_posix()}`, SHA-256 `{ref(INV/"result-revision-0002.json")["sha256"]}`. Revision 0002 is canonical by explicit report/result supersession and terminal checkpoint-0003 bindings, not filename ordering. All original revisions are preserved. Nested path/byte/hash bindings, including superseded references, were recomputed ({len(checked)} checked references). The result identifies both separate confirmed findings and binds the report and evidence; the checkpoint binds the exact revision-0002 report/result and revision-1 evidence.

Coordinator `{COORD.name}` report-revision-0001/result-revision-0002 and both handoffs were resolved and fingerprinted in evidence. The latest complete Audit `{AUDIT.name}` is retained as **reported INCONSISTENT**: 52 core artifacts, 76 source files, seven mechanism groups assessed; Critical/High 0, Medium 2, Low 0, Ambiguities 1, Unsupported Governance Controls 1, other counts 0; five groups PASS, Orchestration FAIL (F003), Amendment Application definition FAIL (F004). The overlapping ambiguity/unsupported counts are not additional findings. This process did not rerun or replace that Audit.

Prior-art keyword searches included current `.github`, `docs/ai`, and existing governance records. Existing Requirement Analysis §14 and phases 5–10 already state the initial update → analysis → complete Verification → formal approval sequence. Existing Requirement Update §§7, 13–16 and Master Artifact §8.4 already protect immutable versions and approval separation. Existing Application Guideline/Prompt/Request already distinguish current preparer/applier attempts from planned verifier/reviewer identities. Those controls are reused, not duplicated into a new process. No Requirement Update Agent exists to align. No change to Requirement Analysis, the Application bundle, Corrective Change Guideline/Prompt/Skill/Agent, or Masters is necessary. Earlier GOV-AUD-20261102-001/002 and historical GOV-001/002 are not reopened; the actual prior finding-led Application COMPLETED and independent Verification/Review PASS are not invalidated or reinterpreted.

## 3. F003 — separate ten-field decision

### 1. Decision Status
**{STATUS}**

### 2. Finding Summary
The Requirement Update Guideline, Prompt, Request and Skill universally demand an already-approved source, blocking the initial clarification branch expressly routed through Requirement Update before complete Verification and first formal Human Requirement Approval. Audit-reported Medium / Lifecycle Inconsistency, secondary overlapping Unsupported Governance; not a product requirement defect.

### 3. Investigation Result
Canonical revision 0002 separately confirms the inconsistency. Cause: missing lifecycle-qualified source-status branch across the four Update artifacts. Explicit Human clarification decisions do not equal formal Requirement Approval. No actual bypass or failed initial clarification execution is established.

### 4. Corrective Decision
Accept the finding. Propose only the four Update artifacts: distinguish an identified immutable unapproved initial source before first formal approval from the current approved source for approved-source changes; bind source ID/hash/status and applicable approval evidence. Initial clarification requires identified analysis questions, explicit Human answers/decisions and explicit update request. It creates a new immutable version with lineage under existing §8.4, remains unapproved, and requires subsequent Analysis, complete independent Requirement Analysis Verification, resolution, and separate formal Human Requirement Approval. Preserve existing approved-source finding/non-finding amendment controls, downstream plan evaluation and all plan gates. No initial-clarification fallback for an already-approved Requirement; no finding-led gate bypass; no permission to implement an unapproved Requirement.

Exact proposal: targets 1–4 in section 6 and the canonical diff below. Existing Analysis text needs no amendment. This reconciles the selected initial path with Master lifecycle/immutability rules without a Master change or unresolved material policy choice. Human selection is not approval of these exact bytes.

### 5. Plan Change Required
**N/A** — governance-only subject; no applicable product Approved Requirement or Implementation Plan established or needed. No product Plan change is proposed.

### 6. Plan Impact
Plan validity, tasks, dependencies, acceptance criteria, architecture, product scope, testing, prior implementation retention/rework and product verification applicability: **N/A**. There is no product implementation, plan amendment or product artifact change in this proposal. Governance impact is confined to source-state admission and truthful handoff; complete independent governance assurance and full re-Audit remain required.

### 7. Proposed Plan Amendment
**N/A**. The four exact governance-artifact amendments below are not an Implementation Plan and cannot authorize implementation.

### 8. Human Approval Required
**YES**, before application of this material normative governance correction. Exact paths, before/after hashes/bytes, proposal/report fingerprints, scope/exclusions and application route must be approved; a fresh scoped one-time applier must be explicitly designated.

### 9. Implementation Readiness
**WAITING FOR GOVERNANCE CHANGE APPROVAL**; additionally fresh one-time application authority designation remains outstanding. Not READY FOR IMPLEMENTATION.

### 10. Next Process
Human decision on the exact proposal and fresh one-time applier designation, then only a separately Human-started Application after its preconditions. No later process is started by this report.

## 4. F004 — separate ten-field decision

### 1. Decision Status
**{STATUS}**

### 2. Finding Summary
The enhancement-only Actor and Human Approval paragraph in Corrective Change Request asks for all four actors' own attempts/current runtime fields without stage timing, while Application controls require planned-only future verifier/reviewer identities. Audit-reported Medium / Ambiguity.

### 3. Investigation Result
Canonical revision 0002 separately confirms a Request timing ambiguity caused by conflating actual current attempts with planned future identity bindings. No premature verifier/reviewer invocation, false capability claim or assurance failure is established.

### 4. Corrective Decision
Accept only the documented ambiguity. Replace one paragraph in `CORRECTIVE_CHANGE_REQUEST.md`, aligning it with existing Application controls: proposal preparer actual current attempt; intended applier awaits fresh exact designation and may first qualify in its own Application attempt; before source work, actual preparer/applier own-attempt bindings; future verifier/reviewer definition paths/hashes planned-only until predecessor gate plus fresh stage-start. At each actual stage, own current attempt/readback/identity/permissions/capability; planned-binding mismatch stops for updated Human decision/exact approval. Preserve four distinct actors, additional applier exclusions, all exact approval/qualification/assurance gates and Audit fresh-start requirement. No impossible pre-existing applier qualification or future-attempt requirement is introduced.

Only target 5 changes. Existing Corrective Change Prompt/Guideline and Application bundle already state applicable approval and ordering controls and require no modification. This is a finding-led correction to an enhancement request template, **not a new non-finding enhancement** and not permission to use proposed text as current policy.

### 5. Plan Change Required
**N/A** — no applicable product Requirement/Implementation Plan; no Plan change proposed.

### 6. Plan Impact
All product tasks, acceptance criteria, architecture, scope, dependencies, testing, implementation dispositions and product verification: **N/A**. Governance impact is accurate stage-specific metadata; independent assurance and full re-Audit still required. Historical Application/Verification/Review results are not adversely affected by this ambiguity decision.

### 7. Proposed Plan Amendment
**N/A**; only the one exact governance Request paragraph is proposed.

### 8. Human Approval Required
**YES**, exact material governance correction plus fresh one-time applier designation as section 7. Direction selection/start is not approval.

### 9. Implementation Readiness
**WAITING FOR GOVERNANCE CHANGE APPROVAL**, with fresh application-authority designation also pending.

### 10. Next Process
Exact Human Approval/designation gate, then separately started authorized Application; stop here.

## 5. Options, minimal coordination and policy boundary

The Human selected the Investigation's lifecycle-qualified initial/approved-source direction for F003 and stage-specific current/planned-only direction for F004 before this start. This is not an AI ranking or invented policy decision. Rejected broader alternatives for this proposal scope are redesigning Analysis's pre-approval path or splitting multiple stage request templates; neither is needed for the selected directions.

Benefits: removes the initial-source contradiction and future-attempt timing ambiguity while retaining existing authority and assurance. Risks: confusing clarification with formal approval or planned identities with current capability; the proposed text expressly prevents both. Product runtime, operations, API/schema, integration, deployment and compatibility impact: none authorized. Governance compatibility: existing approved-source path, immutable history, actor separation and all gates retained. Validation impact: independent cross-document governance Verification and Review, then complete Audit; in-memory proposal selftests below are not substitutes.

The findings remain separately decided and mapped to disjoint targets. A single five-file exact approval/application package is proposed for coordination only; all five bases must validate before the first write. Partial approval is not authority for this combined package: any reduced/changed package requires an exact revised governed proposal and approval. No unrelated tightening/loosening, Master change, product-root adoption, historical correction, alarm integration or product work is proposed. If later inspection reveals a Master change or unresolved material policy decision, stop at that exact Human gate; do not expand this package.

## 6. Exact proposal and byte contract

Canonical proposal attachment: `{PROPOSAL.as_posix()}`, SHA-256 `{pr["sha256"]}` ({pr["bytes"]} bytes). This is machine-readable proposal detail, not another report or approval. It records exact single-occurrence before/after strings with CRLF, sequential byte offsets, expected sizes/hashes and lossless UTF-8 reconstruction. Canonical minimal patch: `{PATCH.as_posix()}`, SHA-256 `{patchref["sha256"]}` ({patchref["bytes"]} bytes). No replacement has been applied.

All targets retain UTF-8 without BOM and CRLF. Final-newline states below are preserved. The diff in this report is a human-readable LF rendering of that byte-preserving patch; exact replacements plus hashes govern application, not implicit editor/EOL normalization.

Bracketed form fields inside the proposed Request text are intentional invocation-template content, not unresolved values in this decision report. This report and its JSON records use actual identities/bindings or explicit not-applicable/not-yet-available states.

| Exact target | Base bytes / SHA-256 | Expected-after bytes / SHA-256 | Final CRLF |
|---|---|---|---|
{table}

### Exact minimal proposed diff

```diff
{patch.decode("utf-8").replace(chr(13)+chr(10), chr(10)).rstrip()}
```

## 7. Proposed actors, exact approval and one-time application route

{roletext}

Preparer actual own invocation: `{(OWN/"attempt.json").as_posix()}`, fingerprint above. Intended applier/verifier/reviewer have **no actual attempt, current runtime/capability evidence or start asserted here**. These are four distinct path/hash role bindings; actual invocation identity/independence still must be checked at each stage. Shared OS principal/host/repository is not itself disqualifying, and no new OS/security boundary is imposed.

Request a **fresh attributable Human decision** that may combine (a) exact approval of this canonical report/proposal/patch, all five target paths and each exact base/expected-after fingerprint, scope and exclusions, and (b) explicit one-time designation of the intended Governance Amendment Application actor bound to its definition path/hash, this Work ID/cycle, this exact package and one-time scope. Historical designations are not reusable. This actor must be distinct from preparer/verifier/reviewer, the SDLC Process Orchestrator and any active-cycle Governance Remediation actor barred from self-edit. No such decision has been received. The actual decision must be preserved through the existing Human-gate record contract; this report is the request, not an AI-created Human decision.

Approval/designation is not a process start or capability proof. Do not demand a separate pre-existing qualification record. Only after a **separate fresh Human Application stage-start**, the designated actor must qualify through non-mutating current runtime/permission/read/hash/path/exact-target-write-capability/readback/own-publication checks, atomically publish and independently read back its own current attempt, validate the entire exact approval and all five bases before source writes, then apply only approved bytes. Missing capability/authority or base mismatch means CANNOT COMPLETE without source writes; partial failure means stop, preserve exact partial state and report, no unapproved rollback. Definition hashes or this preparer's evidence are not another actor's capability proof.

Successful Application alone is not assurance/effectiveness. Only then may a distinct independent read-only Verifier receive a fresh Human Verification start, validate approval/applied bytes/cross-document effects and its approved planned identity, and publish its own qualified current invocation and report/result. Only after PASS may the distinct Reviewer do likewise with its fresh Human Review start and matching approved planned identity. Binding mismatch blocks that stage for an updated attributable Human decision and exact approval; do not silently substitute roles. Only after passing Review may a separately Human-started complete Governance Audit assess all 52 core artifacts, current applicable source set and all seven mechanism groups with the defined evidence matrix. No future attempt IDs are invented.

The current Independent Governance Verification/Review Guidelines' procedural non-mutation controls remain applicable when technical source-write exclusion is unavailable: bounded complete input manifests, actor-visible operation evidence and concurrency limits, boundary/final rechecks, and own-record-only publication. Residual-risk disclosure is retained below and must remain in their reports/evidence; it is not an extra Human Approval validity condition or a new risk-acceptance stage.

Effectiveness requires CONSISTENT, zero Critical/High/Medium/Low/Ambiguities/Missing Governance Controls/Unsupported Governance Controls/Broken References and all seven groups assessed without unresolved issues. This proposal does not assert that a future Audit will pass. These non-Master corrections do not require prospective-baseline adoption for their effectiveness after the gates; they also do not adopt the existing candidate Master set. Any Master adoption remains a separate later Human decision under its own prerequisites.

## 8. Evidence, selfchecks and limitations

Evidence: `{EVIDENCE.as_posix()}`, SHA-256 `{er["sha256"]}`. It binds the invocation, input manifest, checkpoint, all exact proposals, relied sources, canonical Investigation/coordinator/Audit records and helper source.

- **Executed:** current exact byte/hash checks, nested predecessor bindings, independent invocation readback, native complete-object strict JSON serialize/parse equality, sequential single-occurrence replacement reconstruction and reverse-to-base checks, encoding/EOL/final-newline checks, exact five-path non-Master scope, complete 463-input inventory/Git index/HEAD/branch/status recheck, and own-record validated `.partial` → flushed same-filesystem atomic no-overwrite publication/readback. These are process-record/proposal integrity selftests, not product tests or independent governance Verification/Review.
- **Source inspection:** current Update/Analysis, Corrective Change and Application controls, role definitions and applicable Master sections. Source reading is not executed behavioral evidence.
- **Reported:** actual supplied Human start and policy-direction selections; actor-owned Investigation/Audit conclusions and historical assurance statuses. Hash validation does not make this a repeat Audit or re-investigation.
- **Unverified/not yet applicable:** any actual initial product clarification failure, premature future-stage invocation, future actor capability, exact patch approval, designation or stage start. No claim is made.

Read-only was procedural, not sandbox-enforced. Current observed ACL permits Modify; no unapproved source-write probe was performed. Same-principal or transient mutation/reversion cannot be excluded. There is no exhaustive trusted event log or independent OS tamper monitor. Endpoint hashes establish the bytes observed, not a continuous event-free history. Human chat authenticated IDs/time are unavailable; no invented attribution/time was used. Exact publication time was not captured; UTC preparation times are not represented as publication times.

## 9. Completion and safe stop

Corrective decision/proposal preparation is completed for these two findings only. Both are accepted with other governed artifact changes required, **not corrected or closed**. No source/upstream/history bytes, product artifact, Requirement, Plan, test, configuration or migration was modified; no application, independent Verification/Review, Audit, adoption, staging, Commit or Push was performed. Only this attempt's own records were published.

Terminal result location: `{RESULT.as_posix()}`; it is published after this report/evidence and binds their final bytes. This earlier report intentionally does not claim its own or its later result's future fingerprint. The terminal checkpoint records subsequent fresh readback. **STOP: exact Human Approval plus fresh scoped one-time applier designation are the next necessary gate; no later process is initiated.**
"""
    check_inputs()
    rr = publish(REPORT, report.encode("utf-8"))
    result = metadata("corrective_decision_result")
    result.update(execution_status="COMPLETED", outcome="PROPOSALS_PREPARED_PENDING_EXACT_HUMAN_APPROVAL",
                  subject_type="FINDING", report=rr, proposal=pr, patch=patchref, evidence=er,
                  input_manifest=a["input_manifest"], invocation=ref(OWN/"attempt.json"), checkpoint=cpr,
                  findings=[{"finding_id":f,"decision_status":STATUS,"plan_change_required":"NOT_APPLICABLE",
                             "human_approval_required":True,"implementation_readiness":"WAITING FOR GOVERNANCE CHANGE APPROVAL",
                             "target_paths":[t["path"] for t in targets if f in t["finding_ids"]]} for f in [F003,F004]],
                  affected_targets=[{k:v for k,v in t.items() if k != "replacements"} for t in targets],
                  approved_requirement="NOT_APPLICABLE", approved_plan="NOT_APPLICABLE",
                  actors=roles, pending_gates=["Exact Human Approval of canonical report/proposal/patch, five paths and base/expected-after fingerprints",
                                             "Fresh explicit one-time applier designation; may be combined with exact approval",
                                             "Separate fresh Application stage-start and actual actor-owned current qualification before source writes"],
                  next_process="Human exact approval and fresh one-time application authority designation; no subsequent process started",
                  scope={"sources_changed":False,"upstream_changed":False,"applied":False,"approved":False,
                         "future_assurance_attempts_created":False,"later_stage_started":False,
                         "product_work":False,"masters_changed_or_adopted":False,"staging_commit_push":False})
    resultref = publish(RESULT, serialize(result))
    print(json.dumps({"report":rr,"result":resultref,"proposal":pr,"patch":patchref,"evidence":er,
                      "state":"Published; independent terminal readback still required"},indent=2))

if __name__ == "__main__":
    main()
