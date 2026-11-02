"""Bounded coordinator checks and its own immutable outputs only."""
import sys
sys.dont_write_bytecode = True
from coordination import *

EXPECTED_AUDIT = {
    "report.md": (55902, "4246B0BAA6A945678034706AE02E26162CD2DB940D8FAC3F2AB7749D76B477A2"),
    "result.json": (27489, "3C628AA7BC8ECDF2194EC5FBA13911BB183B45A0BBA4CD57E81CF4B4FBF23231"),
    "evidence/audit-evidence.json": (4819789, "888ABF5B0E14829F0EC2FF824510DB1E3B8DB3CC1636F29B3DD6E44DF5104AF2")}
PRIOR = [
    ("Cycle admission", "20261031T072633Z-4c6c7de5-037e-49d1-a594-97b7ef0c5319", None, None),
    ("Prior coordinator", "20261102T084120Z-84eb5d6a-4ec3-4c1f-9122-17edda7c6d51",
     "84D6194D5FBCF02ED26DC81341F68843F37A7B04B9B0A1BE7416B3B4647B7F0C", "5A55C4D055607FD5898FF7D87E7B74A2BFACA52818F4FB24B9C637FAE8453EF1"),
    ("Historical Investigation", "20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0", None, None),
    ("No-plan-change Decision", "20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37", None, None),
    ("Earlier coordinator", "20261102T075750Z-1210d4b1-8300-4b17-8f6b-911a2f64958e", None, None),
    ("Failed Application", "20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31", None, None),
    ("Recovery Decision", "20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed",
     "F96D1A37D0F9CE9C5D423C86B84531D80E7C27D945C52FE559586792491D196F", None),
    ("Completed Application", "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd",
     "26EEC34BAB50AD8A67FEBDAC262D9A723700807C5BA27FBD932668CE16AB2B88", "8F9AEF423A96167C8A6247266F26989A22AB331FB033D7280AB8C46127359CD9"),
    ("Independent Verification", "20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1",
     "A1388E49A5F107443FAF3E5E32D4FDFB5B9C8CBC5EA4D4EBD4B56967E695B7E0", "D3F3680DA22EA8538482D1E5F7B6FACFD0A41A7C2D89E2E0369981311B4DFB43"),
    ("Independent Review", "20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb",
     "27A8D83B6B9D05E847B89DC07773CD2EB4362A64DA122198C9205793B446BF44", "E404F5B77FF317D431DFB3E6B8BF05FF6151480AFFE0ECA083AAED1DB9C41D1D")]
NEXT = ("Yes, initiate Finding Investigation for GOV-AUD-20261102-002 only under Work ID "
        + WORK + ", GOV-REMEDIATION-PROSPECTIVE-001 Cycle 1, using the bound Investigation handoff at "
        + (OWN / "attachments/investigation-handoff.md").relative_to(ROOT).as_posix()
        + "; read-only investigation with own new actor-owned records only; no other stage or correction is authorized.")

def check_binding(r):
    p = Path(r["path"])
    if not p.is_absolute():
        p = ROOT / p
    actual = ref(p)
    assert actual["sha256"] == r["sha256"].upper(), (r["path"], "hash mismatch")
    if "bytes" in r:
        assert actual["bytes"] == r["bytes"], (r["path"], "size mismatch")
    return actual

def walk_bindings(obj):
    found = []
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            found.append(check_binding(obj))
        for value in obj.values():
            found.extend(walk_bindings(value))
    elif isinstance(obj, list):
        for value in obj:
            found.extend(walk_bindings(value))
    return found

def validate():
    inv = load(OWN / "attempt.json")
    assert ref(OWN / "attempt.json")["sha256"] == "1FA0BEEFCB82C6B374738E82308C04DB43925101746BA95E5512C3CDB6C6F90A"
    assert snapshot() == inv["baseline"], "Input content or pathset changed"
    assert cmd("git", "rev-parse", "HEAD") == inv["repository"]["head"]
    assert cmd("git", "branch", "--show-current") == inv["repository"]["branch"]
    assert cmd("git", "--no-pager", "status", "--short") == inv["repository"]["git_status"]
    audit_refs = {}
    for name, (size, sha) in EXPECTED_AUDIT.items():
        rr = ref(AUDIT / name)
        assert (rr["bytes"], rr["sha256"]) == (size, sha)
        audit_refs[name] = rr
    result = load(AUDIT / "result.json")
    ev = load(AUDIT / "evidence/audit-evidence.json")
    assert result["execution_status"] == result["execution_termination"] == "COMPLETED"
    assert result["outcome"] == "CONSISTENT WITH MINOR FINDINGS"
    assert result["core_counts"] == {"expected": 52, "found": 52, "audited": 52}
    assert result["counts"] == {"Critical": 0, "High": 0, "Medium": 0, "Low": 1, "Ambiguities": 1,
                                "Broken References": 0, "Missing Governance Controls": 0, "Unsupported Governance Controls": 0}
    assert result["work_id"] == WORK and result["cycle_id"] == CYCLE and result["cycle_number"] == 1
    assert result["report"]["path"] == audit_refs["report.md"]["path"]
    assert result["report"]["sha256"] == audit_refs["report.md"]["sha256"]
    assert result["report"]["identity"] == AUDIT.name + ":audit_report"
    assert result["record_id"] == AUDIT.name + ":audit_result"
    assert ev["canonical_report"]["identity"] == result["report"]["identity"]
    assert result["unresolved_findings"] == ev["findings"]
    assert [f["finding_id"] for f in ev["findings"]] == ["GOV-AUD-20261102-002"]
    assert len(result["source_manifest"]) == len(ev["source_manifest"]) == 76
    assert result["source_manifest"] == ev["source_manifest"]
    assert len(result["mechanisms"]) == 7
    assert [m["group"] for m in result["mechanisms"] if m["result"] != "PASS"] == ["Governance Remediation"]
    assert result["effectiveness_qualifying"] is False
    audit_checks = walk_bindings(result)
    history = []
    for label, aid, report_sha, result_sha in PRIOR:
        p = ATTEMPTS / aid
        rr, rs = ref(p / "report.md"), ref(p / "result.json")
        if report_sha:
            assert rr["sha256"] == report_sha
        if result_sha:
            assert rs["sha256"] == result_sha
        obj = load(p / "result.json")
        binding = obj.get("report", obj.get("reportBinding", obj.get("canonicalReport", {})))
        # Older schema variants are identified by their actual fields, not guessed.
        if isinstance(binding, dict) and "path" in binding and "sha256" in binding:
            check_binding(binding)
        history.append({"label": label, "attempt_id": aid, "report": rr, "result": rs,
                        "result_identity": obj.get("record_id", obj.get("recordIdentity", obj.get("recordType"))),
                        "outcome": obj.get("outcome", obj.get("decision_status", obj.get("findingOutcomes", obj.get("executionTermination"))))})
    for aid in [PRIOR[-1][1], PRIOR[-2][1], PRIOR[-3][1]]:
        obj = load(ATTEMPTS / aid / "result.json")
        assert obj["execution_status"] == "COMPLETED"
    assert load(ATTEMPTS / PRIOR[-1][1] / "result.json")["outcome"] == "PASS"
    assert load(ATTEMPTS / PRIOR[-2][1] / "result.json")["outcome"] == "PASS"
    assert load(ATTEMPTS / PRIOR[5][1] / "result.json")["execution_status"] == "FAILED"
    clarification = ref(ATTEMPTS / PRIOR[-3][1] / "attachments/GOV-AUD-20261102-001-linked-clarification.md")
    assert clarification["bytes"] == 3438 and clarification["sha256"] == "8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
    failed_payload = ATTEMPTS / PRIOR[5][1] / "attachments/GOV-AUD-20261102-001-linked-clarification.md"
    assert not failed_payload.exists()
    v = meta("coordination_validation")
    v.update({"outcome": "PASS", "invocation": ref(OWN / "attempt.json"),
              "invocation_separate_readback": "Separate PowerShell/Python operation before substantive analysis; 99153 bytes and exact SHA-256 verified",
              "audit": audit_refs, "audit_result_identity": result["record_id"],
              "audit_report_identity": result["report"]["identity"],
              "audit_chain_validation": "PASS: independently recomputed stored result SHA-256; native result binds canonical final report identity/path/size/SHA-256 and evidence",
              "audit_result_binding_occurrences_validated": len(audit_checks), "audit_result_bindings": audit_checks,
              "audit_counts": result["counts"], "core_counts": result["core_counts"], "mechanisms": result["mechanisms"],
              "current_finding": ev["findings"][0], "finding_citations": ev["finding_citations"],
              "history": history, "prior_clarification": clarification,
              "audit_preservation": ev["preservation"], "audit_operations": ev["operations"],
              "source_state": inv["baseline"]["source"],
              "current_endpoint_preservation": {"source_files": 76, "prior_record_files": 264,
                                                "content_and_pathset": "UNCHANGED", "HEAD_branch_status": "UNCHANGED",
                                                "baseline": ref(OWN / "attempt.json")},
              "handoff_authority_sources": [ref(p) for p in [
                  ".github/agents/finding-investigation.agent.md", ".github/skills/finding-investigation/SKILL.md",
                  "docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md",
                  "docs/ai/prompts/FINDING_INVESTIGATION_PROMPT.md", "docs/ai/request/FINDING_INVESTIGATION_REQUEST.md"]],
              "helpers": [ref(__file__), ref(OWN / "attachments/coordination.py")],
              "next_human_start": NEXT,
              "limitations": ["Procedural nonmutation, not sandbox-enforced", "Endpoint checks cannot exclude transient writes or same-principal tampering",
                             "No exhaustive event log or authenticated current Human message ID/time", "Historical process conclusions retained as reported; not re-performed by this coordinator",
                             "Audit 328-file preservation is its reported/hashed evidence, not this invocation's 340-file endpoint population",
                             "Record-preparation clock samples are not exact publication timestamps"]})
    return v, result

def fmt(r):
    return "`" + r["path"] + "` | " + str(r["bytes"]) + " | `" + r["sha256"] + "`"

if sys.argv[1] == "prepare":
    v, result = validate()
    evidence_ref = publish(OWN / "attachments/validation.json", serialize(v))
    prefix = OWN.relative_to(ROOT).as_posix()
    lines = [
        "# GOVERNANCE REMEDIATION PAUSED", "",
        "Canonical bounded coordination report; not a new Audit, Investigation, corrective decision, final Remediation completion, or adoption.", "",
        "## Identity, authority and invocation",
        f"- Work ID: `{WORK}`; Remediation Cycle ID: `{CYCLE}`; Current Cycle: 1 (existing, not newly allocated).",
        f"- Actor: `{ROLE}`; local invocation identity: `local-coordination-invocation:{ATTEMPT}`. No authenticated platform actor ID is exposed.",
        f"- Attempt: `{ATTEMPT}`; canonical report identity: `{ATTEMPT}:coordination_report`.",
        f"- Fresh actual Human start: “{START}”. Source: actual current parent conversation; no authenticated message ID or Human timestamp exposed or invented.",
        "- Root authority: live-resolved OWNER comment https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236, 2026-10-30T12:31:51Z. Its root adoption does not authorize this continuation; the separate current start does.",
        "- Current OS identity, ACL, read/write access eligibility, exact repository HEAD/branch/status, role/Master hashes, native JSON serializer test, and no-overwrite route are recorded in the invocation.",
        "- Invocation published first, then independently read back in a separate tool operation before substantive analysis. All 76 source and 264 prior-record initial bindings matched. Own newly allocated scope only; no conflicting writer identified from available recovery/process observations; stale starts are not treated as live or complete.",
        "- Repository: ScalableParimal/SupportIQ; HEAD 57ed3afe8a14a41bdbe38d4df621a99c836a0f4c; branch sdlc-framework-onboarding. Five preexisting tracked governance modifications retained; no staging.",
        "- Masters remain bootstrap comparison authority only. Neither target Master baseline nor product root is adopted. Governance section 3 permits governed correction before adoption; no circular future coordinator record is imposed on the earlier Audit.",
        "", "## Latest complete Audit: independently validated bindings",
        "| Record | Bytes | Recomputed SHA-256 |", "|---|---:|---|"]
    for r in v["audit"].values():
        lines.append("| " + fmt(r) + " |")
    lines += [
        f"- Stored result identity: `{v['audit_result_identity']}`. Canonical report identity: `{v['audit_report_identity']}`.",
        "- Validation: **PASS**. The stored result was independently hashed and its canonical report path, identity, byte count and SHA-256 binding matched final stored bytes. Evidence path/identity/hash also matched; report/evidence use forward result identity, not a fictional future digest.",
        f"- {v['audit_result_binding_occurrences_validated']} native path/SHA-256 binding occurrences in the Audit result were re-resolved and matched, including all 76 current governance sources. This is bounded input-integrity validation, not a repeat full Audit.",
        "- Execution: **COMPLETED**. Actual outcome: **CONSISTENT WITH MINOR FINDINGS**. Findings list is not empty: only **GOV-AUD-20261102-002**.",
        "- Core scope: 52 expected / 52 found / 52 audited (3 Masters, 10 Guidelines, 10 Prompts, 10 Requests, 10 Skills, 9 Process Agents). 76 total governance source files; mechanisms are separate, not added to core counts.",
        "| Critical | High | Medium | Low | Ambiguities | Missing controls | Unsupported controls | Broken references |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
        "| 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |",
        "Low and Ambiguities describe the same single finding, not two.",
        "", "## Separately reported mechanism alignment",
        "| Mechanism | Groups expected / found / assessed | Sources expected / found / assessed | Audit result |",
        "|---|---|---|---|"]
    for m in result["mechanisms"]:
        lines.append(f"| {m['group']} | {m['expected']} / {m['present']} / {m['assessed']} | {m['source_expected']} / {m['source_present']} / {m['source_assessed']} | {m['result']} |")
    lines += [
        "", "## Current finding and bounded disposition",
        "- **GOV-AUD-20261102-002 — Low / Ambiguity**, registered by reference to the canonical Audit, preserving its original ID.",
        "- Affected artifact: `.github/agents/sdlc-governance-remediation.agent.md`, section 43 / Optional Post-Completion Commit item 2, lines 1309 and 1312.",
        "- Related authority: `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md` section 33.1 line 1191 and Traceability section 30.1 publication contract.",
        "- Issue: authorization records must exist before Commit/Push, but item 2 says to append the resulting commit identity to the same authorization record. It does not explicitly identify immutable later linked-record handling; published final records must not be modified in place.",
        "- Impact is prospective optional-route ambiguity. **No actual final-record mutation or unauthorized Commit/Push is established.**",
        "- Investigation result: **NOT STARTED / confirmation undecided**. Root cause and corrective options are for the separate Investigation.",
        "- Corrective decision: **NOT STARTED / no acceptance or rejection inferred**. No exact correction is proposed or approved by this coordinator.",
        "- The Audit recommendation to clarify a linked immutable record route is advisory input only, not adopted wording, convention, or application authority.",
        "- Proposed correction: **none at this stage**. Do not edit the active role or another source. Any future self-definition change remains governed by section 3.1, exact approval, distinct application authority and independent assurance.",
        "", "## Cycle history reconciled, not rewritten",
        "| Record/stage | Attempt | Disposition |", "|---|---|---|",
        f"| Prospective cycle admission | {PRIOR[0][1]} | Actual conversational Human admission of historical GOV-001/GOV-002; no retroactive relabelling of direct stages |",
        f"| Record-first Investigation / Decision | {PRIOR[2][1]} / {PRIOR[3][1]} | GOV-001/GOV-002 accepted — NO PLAN CHANGE REQUIRED under Corrective 7.2/17; not reopened |",
        f"| Earlier coordination | {PRIOR[4][1]} | Preserved as historical coordination, not final consistency |",
        f"| Prior Audit-to-coordinator handoff | {PRIOR[1][1]} | Routed GOV-AUD-20261102-001; remains immutable |",
        f"| Failed Application | {PRIOR[5][1]} | Terminal FAILED / CANNOT COMPLETE; tuple/list JSON comparison stopped before payload publication; failed payload still absent |",
        f"| Recovery Decision | {PRIOR[6][1]} | New scope/redesignation and exact approval supplied separately; no transfer of old approval or start |",
        f"| Completed Application | {PRIOR[7][1]} | Exact new 3438-byte linked clarification only; no historical report rewrite |",
        f"| Independent Verification | {PRIOR[8][1]} | Reported PASS, separately initiated; native completed result and bound report revalidated |",
        f"| Independent Review | {PRIOR[9][1]} | Reported PASS after Verification, distinct invocation; native completed result and bound report revalidated |",
        f"| Latest complete Audit | {AUDIT.name} | Previous GOV-AUD-20261102-001 assessed addressed; new different GOV-AUD-20261102-002 only |",
        f"| Current continuation | {ATTEMPT} | Integrity PASS; history reconciled; only new finding routed; PAUSED at next Human start |",
        "- The prior Investigation's original presentation defect remains in its immutable report; exact approved append-only clarification resolves it. No original Human message is newly authenticated and no transport cause is inferred.",
        "- Prior GOV-001/GOV-002 and addressed GOV-AUD-20261102-001 are not reopened or suppressed. This new finding is not a repeated identical finding triggering blind correction.",
        "- Prior Application, Verification and Review belong to their exact separately Human-started scopes. This coordinator references their results; it neither publishes them nor independently re-performs or upgrades their substantive assurance.",
        "", "## Human decisions, approvals, corrections and assurance",
        "- Current Human decision received: bounded continuation start, quoted above. It is not finding acceptance, correction approval, Investigation initiation, Human Acceptance, Commit/Push authorization or adoption.",
        "- Prior admission and exact clarification approval/recovery are retained only within their historical bindings. No authority transfers to GOV-AUD-20261102-002.",
        "- Current correction approval: **none**. Corrections applied by this invocation: **none**. No Verification or Review is started or required for an unapplied new correction at this handoff.",
        "- Prior correction cycle: Verification PASS followed by separately initiated Review PASS before the latest Audit, as bound above. This does not resolve the new finding.",
        "", "## Operational evidence and material limitations",
        "- Latest Audit disclosed an fsync error on its own unpublished helper opened read-only. Its durable checkpoint/source notes and absent final report/evidence/result were reconciled; helper flush mode corrected before publication. No published final record was overwritten. This does not convert the valid completed Audit into incomplete execution.",
        "- Audit evidence reports 328 preexisting in-scope source/record files unchanged at endpoints. That population belongs to that Audit. Current invocation baseline is 76 source files plus 264 prior-record files (340); all contents/pathsets and HEAD/branch/status remain unchanged at this endpoint.",
        "- Nonmutation is procedural, **not an enforced sandbox**. Endpoint checks cannot exclude transient writes or same-principal tampering. No exhaustive event log, continuous observation or exclusive repository lock is available.",
        "- Human identity/time beyond actual conversational attribution is unavailable; no authenticated message ID/time is invented. Host clock samples describe preparation, not exact filesystem publication times.",
        "- No product content inspected; no product work/tests/runtime, source/upstream mutation, approval/adoption, stage invocation, correction, stage nesting, commit or push.",
        "", "## Canonical evidence and record bindings",
        "| Record | Bytes | SHA-256 |", "|---|---:|---|",
        "| " + fmt(ref(OWN / "attempt.json")) + " |",
        "| " + fmt(evidence_ref) + " |"]
    for h in v["history"]:
        lines += ["| " + fmt(h["report"]) + " |", "| " + fmt(h["result"]) + " |"]
    lines += ["| " + fmt(v["prior_clarification"]) + " |",
        "", "## Exact pending Human gate and next action",
        "- Exact Human decision required: initiate or decline a **separate Finding Investigation** for GOV-AUD-20261102-002 only under the existing Work ID and Cycle 1.",
        "- Exact Human approval required now: **process-start authorization only**; no correction approval is requested. Any eventual governance decision/exact correction approval must be requested after Investigation and Corrective Change Decision.",
        "- Recommendation (advisory): initiate the bounded read-only Investigation. Options: initiate it, decline it, or defer it; decline/defer leaves remediation paused.",
        "- Autonomous continuation is not permitted: the current Human start expressly excludes all other stages, and each next stage needs its own fresh Human start.",
        f"- Copy-ready fresh Human start: **{NEXT}**",
        f"- Handoff: `{prefix}/attachments/investigation-handoff.md` (published after this report, with this report's final hash).",
        f"- Terminal result: `{prefix}/result.json`, identity `{ATTEMPT}:coordination_result`; published only after independent report/evidence/handoff readback, binding their final hashes. This earlier report claims no own/future-result fingerprint.",
        "- Exact next action after an affirmative response: a separately initiated Finding Investigation actor must qualify itself, resolve and rehash these inputs, publish/read back its own fresh invocation, investigate only this finding and directly relevant governance context, and route its report to a separately Human-started Corrective Change Decision.",
        "- Governance Remediation Status: **PAUSED**, not COMPLETE. Audit outcome remains CONSISTENT WITH MINOR FINDINGS; not effectiveness-qualifying, not Master/product-root adoption.",
        "- Alarm integration absent: both guide and script checked absent; no Start invoked. This has no effect on the Human gate.", ""]
    report_bytes = "\n".join(lines).encode("utf-8")
    for marker in ["<Work-ID>", "<Attempt-ID>", "[Finding ID]", "`n"]:
        assert marker.encode() not in report_bytes
    report_ref = publish(OWN / "report.md", report_bytes)
    handoff = [
        "# Finding Investigation handoff — awaiting separate Human initiation", "",
        f"Work ID: `{WORK}`; Cycle: `{CYCLE}`, Cycle 1.",
        f"Originating process/actor: {ROLE}; local invocation `{ATTEMPT}`.",
        f"Canonical coordinator report identity: `{ATTEMPT}:coordination_report`.",
        "| Input | Bytes | SHA-256 |", "|---|---:|---|",
        "| " + fmt(report_ref) + " |", "| " + fmt(evidence_ref) + " |",
        "| " + fmt(v["audit"]["report.md"]) + " |",
        "| " + fmt(v["audit"]["result.json"]) + " |",
        "| " + fmt(v["audit"]["evidence/audit-evidence.json"]) + " |", "",
        f"Audit report identity `{v['audit_report_identity']}`; result identity `{v['audit_result_identity']}`.",
        "Audit chain integrity: PASS. Actual completed outcome CONSISTENT WITH MINOR FINDINGS; core52/52/52, 76 governance sources, seven mechanisms assessed; six PASS and Remediation FAIL. Critical/High/Medium0, Low1, Ambiguities1 (same finding), missing/unsupported/broken0.",
        "", "## Sole assigned finding",
        "**GOV-AUD-20261102-002 — Low / Ambiguity**; source Audit report Governance Consistency Findings subsection (lines302–326).",
        "Affected `.github/agents/sdlc-governance-remediation.agent.md` section43 Optional Post-Completion Commit item2: line1309 requires authorization records before Commit/Push; line1312 says append resulting commit identity to the same authorization record.",
        "Related `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md` section33.1 line1191 prohibits modifying published final records in place and requires linked new records; also Traceability30.1.",
        "No actual mutation or unauthorized Commit/Push established. Confirmation, cause, viable options, finding acceptance and corrective decision are not supplied by this handoff. Audit's linked-record clarification recommendation remains advisory, not approved.",
        "", "## Required receiving-actor process",
        "After a fresh explicit Human start only, establish current identity/capability/authority, exact repository/state, existing Work ID and own new attempt scope; check recovery/liveness and publish/read back a no-overwrite invocation BEFORE substantive analysis.",
        "Resolve/rehash the canonical coordinator report/result, validation evidence and Audit result/report/evidence. Inspect directly relevant governance definitions and required evidence, not merely this summary. Use targeted/programmatic reads of the 4,819,789-byte Audit evidence.",
        "Follow the Finding Investigation Agent, designated Skill, Guideline, Prompt and Request. Use finding subject type, not a non-finding enhancement. Examine the complete directly affected governance context without unrelated redesign or product work.",
        "Determine confirmation/nonconfirmation, actual affected artifacts, cause, impact, existing authority/record rules, viable corrective options, required Human decisions/approval and recommended next process; return every required Investigation report field.",
        "Publish only this new Investigation actor's own invocation/report/result/evidence; no source or upstream edits, acceptance/approval, correction/application, adoption, commit/push, product activity or other-stage invocation.",
        "If a governed decision is needed, route to Corrective Change Decision for a separate Human start; do not execute or authorize that stage. Any proposed active Remediation definition change must preserve section3.1 authority and separation.",
        "", "## Historical exclusions and applicability",
        "Existing GOV-001/GOV-002 accepted NO PLAN CHANGE REQUIRED and not reopened. Previous GOV-AUD-20261102-001 addressed by exact approved linked clarification, separately initiated completed Application and passing Verification then Review; historical reports remain immutable. Those approvals/starts do not cover the new finding.",
        "The failed earlier Application remains terminal FAILED with no payload; recovery required fresh redesignation/exact approval/start, not transferred authority. Audit flush diagnostic was reconciled on unpublished helper only; Audit completed validly.",
        "Masters remain bootstrap comparison authority; target baseline/product root not adopted. This is a finding-led prospective-cycle continuation, not a new historical relabelling or adoption route.",
        "", "## Pending gate and stop",
        f"Exact proposed Human response: **{NEXT}**",
        "Until supplied: Investigation NOT STARTED; no acceptance/correction approval. Initiation request only, not a substantive governance-decision request.",
        f"Coordinator terminal result path `{prefix}/result.json`, identity `{ATTEMPT}:coordination_result`; later immutable result binds the report and this handoff. Rehash that stored result when consuming the handoff; no circular future digest is asserted here.",
        "Limitations: procedural nonmutation, shared writable principal, no exhaustive event log; endpoints cannot exclude transient/same-principal changes; no authenticated Human message ID/time. Current endpoint preservation checks do not replace independent Investigation.",
        "", "## Applicable source bindings",
        "| Source | Bytes | SHA-256 |", "|---|---:|---|"]
    for rr in v["handoff_authority_sources"]:
        handoff.append("| " + fmt(rr) + " |")
    handoff.append("")
    handoff_ref = publish(OWN / "attachments/investigation-handoff.md", "\n".join(handoff).encode("utf-8"))
    print(json.dumps({"report": report_ref, "validation": evidence_ref, "handoff": handoff_ref,
                      "audit_result_bindings_validated": len(v["audit_result_bindings"]),
                      "outcome": "PREPARED; separate-process readback required before terminal result"}))

elif sys.argv[1] == "finalize":
    # Caller must independently reload and validate the prepared outputs first.
    receipt = load(OWN / "checkpoint-0001.json")
    assert receipt["outcome"] == "PASS"
    v, result = validate()
    for rr in receipt["validated_outputs"]:
        check_binding(rr)
    walk_bindings(load(OWN / "attachments/validation.json"))
    d = meta("coordination_result")
    d.update({"execution_status": "COMPLETED", "execution_termination": "COMPLETED",
              "outcome": "BOUNDED CONTINUATION COMPLETED; GOVERNANCE REMEDIATION PAUSED",
              "governance_remediation_status": "PAUSED", "audit_outcome": result["outcome"],
              "finding_id": "GOV-AUD-20261102-002", "finding_confirmation": "NOT INVESTIGATED",
              "corrective_decision": "NOT STARTED", "correction_approval": "NONE",
              "report": dict(ref(OWN / "report.md"), identity=ATTEMPT + ":coordination_report"),
              "evidence": ref(OWN / "attachments/validation.json"),
              "handoff": ref(OWN / "attachments/investigation-handoff.md"),
              "invocation": ref(OWN / "attempt.json"), "independent_readback": ref(OWN / "checkpoint-0001.json"),
              "audit_result": dict(ref(AUDIT / "result.json"), identity=result["record_id"]),
              "audit_report": result["report"], "audit_chain_validation": "PASS",
              "core_counts": result["core_counts"], "counts": result["counts"], "mechanisms": result["mechanisms"],
              "preservation": v["current_endpoint_preservation"],
              "next_permitted_process": "Finding Investigation for GOV-AUD-20261102-002 only after separate fresh Human initiation",
              "exact_next_human_start": NEXT,
              "all_other_stages_started": False, "source_or_upstream_edits": False,
              "effectiveness_qualifying": False, "adoption": False, "commit_push": False,
              "limitations": v["limitations"]})
    print(json.dumps({"terminal_result": publish(OWN / "result.json", serialize(d)),
                      "outcome": d["outcome"]}))
