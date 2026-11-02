"""Own-record assembly/validation. Static administrative checks only."""
import datetime, hashlib, json, os, pathlib, runpy, sys

BASE = pathlib.Path(__file__).resolve().parents[1]
H = runpy.run_path(str(BASE/"attachments/publication-helper.py"))
ROOT, WORK, ATTEMPT = H["ROOT"], H["WORK"], H["ATTEMPT"]
load, ref, check_ref, publish, common = (H[k] for k in ["load", "ref", "check_ref", "publish", "common"])
INV = load(BASE/"attempt.json")
CREATOR = INV["creator"]
OVERALL = "COMPATIBILITY WITH IDENTIFIED ADAPTATION"
STATES = [
    "VERIFIED COMPATIBILITY", "COMPATIBILITY WITH IDENTIFIED ADAPTATION",
    "INCOMPATIBILITY / POSSIBLE BLOCKING CONDITION",
    "UNVERIFIED / INSUFFICIENT EVIDENCE", "NOT APPLICABLE",
]
CATEGORIES = [
    "FRAMEWORK GOVERNANCE DEFECT CANDIDATE", "FRAMEWORK CAPABILITY ENHANCEMENT",
    "TARGET-PROJECT ADAPTATION", "TARGET REQUIREMENT / ARCHITECTURE GAP",
    "INTEGRATION / RUNTIME UNCERTAINTY", "INSUFFICIENT EVIDENCE / UNRESOLVED HUMAN DECISION",
]

# Verbatim bodies returned by current GitHub MCP issue_read/get_comments.
MASTER_BODY = r"""I, Parimal Shere (ScalableParimal), explicitly adopt SupportIQ-Master-Baseline-001 as the prospective three-Master governance baseline for ScalableParimal/SupportIQ at C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 42. The target/source state is branch sdlc-framework-onboarding, HEAD 57ed3afe8a14a41bdbe38d4df621a99c836a0f4c, together with the assessed working-tree governance source state bound by the clean Audit below; HEAD alone is not that assessed state.

Exact adopted repository-relative paths and SHA-256:

docs/ai/sdlc/SDLC_GOVERNANCE.md: 79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B
docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md: 6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860
docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md: 08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C
Qualifying evidence under docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/:

20261102T160240Z-5022506a-f881-4681-af13-e4acf3bb6935/result.json, SHA-256 CF073B8E08EDF728B6AB1B1CC300C842D3FEF15F512A084C85B7A7E8EF199222: complete Audit CONSISTENT, 52/52 core artifacts, all eight counts zero, all seven mechanisms PASS; its bound canonical report and source manifest identify the assessed state.
20261102T162238Z-28a7c86b-114f-4d7f-8520-f09000a0df40/result.json, SHA-256 8B0F4D67996B33CAAF35F43D3A86948C165A695C3D94A99213D99479489CD5A1: Remediation COMPLETE with independently validated final Audit binding.
This is initial no-change adoption, not a Master amendment or application. No prior adopted SupportIQ baseline is established; historical approval/effectivity remains unknown where evidence is absent. The effective boundary is publication of this explicit Human decision for these exact bytes and assessed source state, prospectively only; subsequent processes must independently resolve it and recheck applicability. It does not retroactively cure or reclassify failed attempts or historical decisions. It does not adopt the product persistence root, start Portability Assessment or any product process, authorize alarm integration, grant Human Acceptance, or authorize source changes, staging, Commit or Push."""

PRODUCT_BODY = r"""I, Parimal Shere (ScalableParimal), separately and explicitly adopt the exact repository-relative product persistence root docs/sdlc-records/product/ for ScalableParimal/SupportIQ at C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ. Target state: branch sdlc-framework-onboarding, HEAD 57ed3afe8a14a41bdbe38d4df621a99c836a0f4c plus the assessed working-tree governance source state bound by the CONSISTENT Audit in governance Work ID 0061148a-1b62-4d25-adff-e7f2318dbfad, attempt 20261102T160240Z-5022506a-f881-4681-af13-e4acf3bb6935 (result SHA-256 CF073B8E08EDF728B6AB1B1CC300C842D3FEF15F512A084C85B7A7E8EF199222). The applicable prospective Master baseline is SupportIQ-Master-Baseline-001 adopted at https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6583261503.

Purpose and scope: durable product-subject SDLC execution records, including a separately initiated SupportIQ Portability Assessment. Applicable actor-owned publication scope is docs/sdlc-records/product/<Work-ID>/attempts/<Attempt-ID>/, with each stable Work ID reserved under the governing convention and each qualified process actor publishing only its own authorized invocation, checkpoints, report, result and permitted evidence or gate records after a fresh explicit Human stage-start. No shared or other actor's final records may be overwritten. This adoption is effective prospectively from publication of this Human decision; future actors must independently resolve it and recheck current applicability.

This decision adopts the root only. It does not start Portability Assessment, the SDLC Orchestrator or any product lifecycle stage; does not approve any Requirement, Plan, implementation or Human Acceptance; and does not authorize product/source changes, alarm integration, staging, Commit or Push. Those require their separate applicable authorizations. It does not retroactively cure earlier blocked or failed invocations."""

def current_input_comparison():
    current_source = [ref(p) for p in H["source_paths"]()]
    assert current_source == INV["source_inventory"]
    for r in INV["target_inventory"]:
        check_ref(r)
    assert H["git"]("rev-parse", "HEAD") == H["HEAD"]
    assert H["git"]("branch", "--show-current") == H["BRANCH"]
    assert H["git"]("status", "--short", "--untracked-files=normal") == INV["repository_context"]["git_status"]
    assert H["git"]("worktree", "list", "--porcelain") == INV["repository_context"]["worktrees"]
    assert H["git"]("diff", "--cached", "--name-status") == ""
    # Safe complete non-record, non-.git path set: no blind body reads.
    actual_paths = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                          if p.is_file() and ".git" not in p.relative_to(ROOT).parts
                          and not p.relative_to(ROOT).as_posix().startswith("docs/sdlc-records/"))
    expected_paths = sorted(r["path"] for r in INV["source_inventory"] + INV["target_inventory"])
    assert actual_paths == expected_paths
    for r in INV["predecessor"]["governance_prerequisites"]:
        check_ref(r)
    return {"outcome": "PASS", "source_files": 76, "target_files": 2,
            "source_target_bytes_and_path_sets_unchanged": True,
            "git_head_branch_status_worktrees_unchanged": True,
            "staged_diff": "Empty", "governance_prerequisite_bindings_unchanged": True,
            "observed_at_utc": H["now"](),
            "limits": "Endpoint comparison, not continuous monitoring; procedural nonmutation, no enforced sandbox"}

def dimension(i, title, state, evidence, concerns):
    return {"dimension": i, "title": title, "applicability": "Applicable",
            "determination": state, "evidence": evidence, "concerns": concerns}

DIMENSIONS = [
    dimension(1, "Repository/workspace configuration, ownership and boundaries", STATES[0],
              "Canonical Git metadata, one worktree, independently resolved OWNER declarations; exact same-checkout source and target inventories. Cross-repository route not applicable.", []),
    dimension(2, "Requirements, architecture, stack and project instructions", STATES[1],
              "PRD paragraphs 17-20, 245-267, 292, 328, 472-483: draft requirement, high-level architecture, illustrative contracts, provider choices deferred.", ["C-02", "C-05"]),
    dimension(3, "Compatibility and authorized use of execution mechanisms", STATES[0],
              "Exact current assessment chain loaded/fingerprinted and actual administrative read/hash/strict-JSON/publication/readback succeeded. Applies to this invocation only, not future actor/runtime discovery.", ["C-04", "C-07"]),
    dimension(4, "Lifecycle, human gates, traceability, ownership and persistence", STATES[1],
              "Both new adoptions independently resolved and current applicability verified; invocation-first publication passed. PRD 417-425 is abridged delivery guidance requiring mapping to controlling Masters.", ["C-01", "C-08"]),
    dimension(5, "Security, privacy, access and project risks", STATES[3],
              "PRD 65, 106-120, 204-222, 332-359, 389 specify controls; no enforcement or executed negative-test evidence.", ["C-03"]),
    dimension(6, "Testing/quality, CI/CD, deployment and operations", STATES[1],
              "PRD 188-202, 390-425, 485-505 specifies future deliverables; definitions/assets absent; numeric release thresholds explicitly require future Human approval.", ["C-04", "C-06"]),
    dimension(7, "AI controls, evaluation, retrieval and tools", STATES[1],
              "PRD FR-CA/KB/WF/EV and section 11 specify grounding, approved/current knowledge, abstention, tenant isolation, read-only allowlisted tools and versioned evaluation; implementation/evaluation evidence absent.", ["C-03", "C-05", "C-06"]),
    dimension(8, "Runtime/integration behavior beyond static evidence", STATES[3],
              "No project/runtime activity authorized or executed. No actual app, service state or integration results available.", ["C-07"]),
]

def concern(cid, category, priority, evidence, impact, scope, recommendation, owner, approvals, pb=None):
    return dict(concern_id=cid, classification=category, priority=priority,
                evidence=evidence, verification_status="SOURCE-INSPECTION; runtime enforcement unverified where applicable",
                impact=impact, affected_scope=scope, recommendation=recommendation,
                owner_next_process=owner, required_approvals=approvals, possible_blocker=pb)

CONCERNS = [
    concern("C-01", CATEGORIES[2], 1, "PRD 417-425 plus draft status at 18; source Master lifecycle",
            "Abridged workflow might be mistaken for authority to skip named verification/approval gates; no intentional bypass established",
            "Target delivery guidance and first governed product handoff",
            "Human disposition; explicitly subordinate PRD section 15 to adopted Masters; later authorized target mapping/update only",
            "Parimal Shere; separately initiated Requirement Analysis/Update if requested",
            "Attributable assessment disposition; actual decisions/update authorization and later Requirement Approval remain separate", "PB-01"),
    concern("C-02", CATEGORIES[3], 2, "PRD 18, 245-267, 292, 328; no approved Requirement/Plan evidence",
            "Illustrative design could be mistaken for finalized approved implementation authority",
            "Target PRD and future implementation planning",
            "Analyze exact candidate PRD completely and resolve contracts/architecture decisions; no preapproved Requirement needed to start analysis",
            "Target owner; Requirement Analysis, independent Verification, resolution/update as applicable",
            "Fresh stage starts and eventual explicit Human Requirement Approval; no additional initial blocker"),
    concern("C-03", CATEGORIES[4], 2, "PRD 65, 106-120, 207-218, 267, 332-359, 389-397; no implementation/test results",
            "Future tenant/content leakage, unsafe tools, missing purge/retention or secret enforcement cannot be excluded",
            "Target future authentication, retrieval/caches, data lifecycle, logs, service identities and read-only integrations",
            "Keep synthetic-only first release and prohibited business writes/message sends; plan and later execute negative isolation/security/retention tests with bounded authorization",
            "Target owner/security/design owner; governed analysis/planning then implementation/independent verification",
            "Applicable Requirement/Plan approvals, bounded execution authorization and distinct scope approval before broader/live integration", "PB-02"),
    concern("C-04", CATEGORIES[2], 3, "78-path non-record inventory: 76 source files, README and PRD only; PRD 390-425, 485-505",
            "No actual reproducible commands, test/CI/deployment assets or product-specific instructions for later actors",
            "Target future development, CI quality gates and deployment/operations",
            "Create project conventions/definitions only through approved later planning/implementation; pin dependencies; serialize shared-checkout writes or approve isolated-worktree integration",
            "Target technical owner; planning and independently verified approved Plan before implementation",
            "Fresh stage starts, Human Review Approval and Plan Approval; separate test/deploy execution scope; not initial-analysis blocker"),
    concern("C-05", CATEGORIES[3], 3, "PRD 252-265, 472-474 explicitly defers exact model/deployment/region",
            "Quota/availability/cost and embedding/index compatibility unknown; implementation must not silently choose",
            "Target provider, model/search adapters, index schema, worker and service/network design",
            "Retain Azure baseline; obtain later bounded validation scope and owner design choices before relying on them",
            "Target architecture owner/Parimal Shere; Requirement Analysis and applicable architecture/Plan process",
            "Actual scoped decisions and relevant Requirement/Plan approvals; no Azure activity now"),
    concern("C-06", CATEGORIES[5], 2, "PRD 188-202, 363-400, 481-483; no evaluation assets/results",
            "Cannot establish quality pass/fail or release suitability; sample counts are not numeric quality thresholds",
            "Target AI evaluation and release acceptance",
            "Propose exact metrics/thresholds, obtain explicit Human approval before release, version datasets/prompts/models and retain regression evidence",
            "Parimal Shere/product-quality owner; governed analysis/update and later authorized tests",
            "Actual Human numeric release-threshold approval, relevant Requirement/Plan gates, verification/review/acceptance", "PB-02"),
    concern("C-07", CATEGORIES[4], 2, "No project/runtime authorization, assets or executed integration evidence; only current administrative capability proven",
            "Future actor permissions and safe app/cloud/integration behavior not established",
            "Target future runtime/live integration/release and each later invocation",
            "Human disposition of stage-scoped possible condition; independently qualify each actor and separately authorize exact environment/data/commands",
            "Parimal Shere and future technical/quality owners; authorized later verification and affected runtime/release gates",
            "Actual scoped assessment disposition; applicable source/Plan approvals and bounded execution authorization", "PB-02"),
    concern("C-08", CATEGORIES[5], 1, "No PB-01/PB-02 disposition in start/adoptions; adoptions disclaim product starts/approvals",
            "First-process handoff cannot infer Human applicability decisions",
            "Target assessment handoff",
            "Request both explicit Human dispositions and rationale; recommend holding first activity pending them; no AI disposition or enforcement",
            "Parimal Shere/ScalableParimal OWNER; attributable assessment Human decision",
            "Actual assessment dispositions, distinct from subsequent fresh stage-start and product approvals"),
]

BLOCKERS = [
    {"recommendation_id": "PB-01", "concerns": ["C-01", "C-08"], "priority": 1,
     "appears_applicable_recommendation": "Yes, as a possible first-product-process handoff ambiguity; not proof of intended bypass",
     "recommended_affected_boundary": "Before first product SDLC activity; explicitly confirm controlling Master lifecycle and subordinate PRD section 15",
     "human_authority": "Parimal Shere / ScalableParimal OWNER", "human_decision": None,
     "human_decision_status": "PENDING", "binding_ai_decision": False},
    {"recommendation_id": "PB-02", "concerns": ["C-03", "C-06", "C-07", "C-08"], "priority": 2,
     "appears_applicable_recommendation": "Yes before future runtime/live integration/release, not a demand for built/tested application before Requirement Analysis",
     "recommended_affected_boundary": "Future affected runtime/live integration/release; Human explicitly dispositions applicability to first analytical activity and later activities",
     "human_authority": "Parimal Shere / ScalableParimal OWNER", "human_decision": None,
     "human_decision_status": "PENDING", "binding_ai_decision": False},
]

def declaration(key, body):
    j = dict(INV["authorization"][key])
    j.update(body=body, body_utf8_bytes=len(body.encode("utf-8")),
             body_utf8_sha256=hashlib.sha256(body.encode("utf-8")).hexdigest().upper(),
             evidence_basis="Actual current GitHub MCP issue_read get_comments response, transcribed exact body and returned native attribution/times",
             integrity_limit="Body snapshot hash identifies retained text; not raw HTTP bytes, remote signature or proof against later remote edits")
    return j

def finalize():
    assert not (BASE/"result.json").exists()
    check_ref({"path": (BASE/"attempt.json").relative_to(ROOT).as_posix(), "bytes": 29212,
               "sha256": "38C7335439CF1F7ED7989A9FFD5E28135928D73D6AE57D8D8547587398C10BC5"})
    assert {d["dimension"] for d in DIMENSIONS} == set(range(1,9))
    assert all(d["determination"] in STATES for d in DIMENSIONS)
    assert all(c["classification"] in CATEGORIES for c in CONCERNS)
    assert all(set(["evidence", "impact", "verification_status", "affected_scope", "recommendation", "owner_next_process", "required_approvals"]) <= set(c) for c in CONCERNS)
    audit = load(H["AUDIT"]/"result.json")
    audit_evidence = load(H["AUDIT"]/"evidence/audit-evidence.json")
    assert len(audit_evidence["assessment"]["core_artifacts"]) == 52
    assert len(audit_evidence["assessment"]["source_inventory"]) == 76
    assert all(x["outcome"] == "PASS" and x["assessed"] for x in audit["mechanisms"])
    assert len(audit["counts"]) == 8 and all(v == 0 for v in audit["counts"].values())
    assert load(H["CLOSURE"]/"result.json")["unresolved_items"] == []
    comparison = current_input_comparison()
    inv_ref = ref(BASE/"attempt.json", INV["record_id"])
    helper_refs = [ref(BASE/"attachments/publication-helper.py"), ref(pathlib.Path(__file__))]
    e = common("assessment_evidence", CREATOR)
    e.update(
        invocation=inv_ref, checkpoint=ref(BASE/"checkpoint-0001.json", ATTEMPT+":checkpoint"),
        requested_scope=INV["requested_scope"], trigger=INV["trigger"],
        source_framework={"identity": INV["repository_context"]["source"], "inventory": INV["source_inventory"],
                          "semantically_inspected": [
                              ".github/agents/portability-assessment.agent.md",
                              ".github/skills/portability-assessment/SKILL.md",
                              "docs/ai/guidelines/PORTABILITY_ASSESSMENT_GUIDELINES.md",
                              "docs/ai/prompts/PORTABILITY_ASSESSMENT_PROMPT.md",
                              "docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md",
                              "docs/ai/sdlc/SDLC_GOVERNANCE.md",
                              "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
                              "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md",
                              "docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
                              ".github/agents/requirement-analysis.agent.md",
                              "docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md"],
                          "inspection_limit": "Semantically inspected governing/entry and relevant source-of-truth/approval/publication sections, not a new whole-framework Audit; full 76-source fingerprint comparison is separate"},
        target_project={"identity": INV["repository_context"]["target"], "inventory": INV["target_inventory"],
                        "inspection": "README complete; DOCX package-name inventory and all 524 word/document.xml paragraphs parsed statically; no Office execution",
                        "locator": "One-based word/document.xml paragraph positions including table cells; report section 6 supplies precise ranges",
                        "absent_definitions": ["Application source", "Dependency/project/package manifests", "Configuration templates", "Product-specific instructions", "Standalone approved architecture", "Test definitions/fixtures", ".github/workflows", "Deployment/IaC", "Evaluation assets/results"]},
        authorization={"fresh_start": INV["authorization"]["fresh_start"],
                       "master_adoption": declaration("master_adoption", MASTER_BODY),
                       "product_root_adoption": declaration("product_root_adoption", PRODUCT_BODY),
                       "adoptions_start_product_process": False,
                       "human_blocker_dispositions_supplied": False},
        governance_prerequisite_applicability={
            "references": INV["predecessor"]["governance_prerequisites"],
            "audit_manifest": INV["qualification"]["prior_governance_applicability"]["audit_manifest"],
            "current_76_source_comparison": "PASS",
            "core_artifacts": 52, "source_files": 76,
            "audit_outcome": "CONSISTENT", "counts": audit["counts"],
            "mechanisms": [{"group": x["group"], "outcome": x["outcome"], "assessed": x["assessed"]} for x in audit["mechanisms"]],
            "remediation_outcome": "COMPLETE", "unresolved_items": [],
            "reused_for": "Master/product-root adoption prerequisites only, not completed portability assessment or runtime capability",
            "earlier_runtime_not_applicable": "Not current capability proof"},
        overall_determination=OVERALL, allowed_determinations=STATES, dimension_outcomes=DIMENSIONS,
        routing_categories=CATEGORIES, concerns=CONCERNS, recommended_possible_blockers=BLOCKERS,
        routing_category_coverage={
            CATEGORIES[0]: "None established; any future candidate goes to separately authorized Governance Audit evaluation, not automatic finding",
            CATEGORIES[1]: "No specific framework enhancement required/requested; later human-requested optional enhancement remains non-finding",
            CATEGORIES[2]: ["C-01", "C-04"], CATEGORIES[3]: ["C-02", "C-05"],
            CATEGORIES[4]: ["C-03", "C-07"], CATEGORIES[5]: ["C-06", "C-08"]},
        evidence_classes={
            "source_inspection": "File and XML inspection, bounded hidden-inclusive path inventories and source authority sections",
            "executed": "Nonmutating administrative filesystem/hash/Git/JSON checks, ZIP/XML parsing and own-record publication/readback only; NO project execution",
            "reported": "Strictly bound clean Audit/closure conclusions and product PRD decision rows; PRD rows are not formal approval evidence",
            "external_decisions": "Independently fetched actual GitHub comments; current conversational start only as supplied",
            "unverified": "App/cloud/runtime controls, provider availability, testing/evaluation quality and numeric release thresholds, later actor capabilities"},
        invocation_ordering={
            "invocation_published_first": True,
            "independent_readback_observed_at_utc": "2026-11-02T17:16:12.211164+00:00",
            "observation_basis": "Actual separate readback command stdout, before first substantive README/PRD read",
            "checkpoint": ref(BASE/"checkpoint-0001.json"),
            "exact_filesystem_publication_timestamp": "Not captured or inferred"},
        administrative_preparation_limits={
            "unpublished_fixes": ["Corrected preparation path to actual UTC-plus-UUID allocation before first publication",
                                 "Historical malformed JSON was not reused; collision discovery uses bounded identity-field search",
                                 "Compared complete source maps by path/content rather than manifest list ordering"],
            "published_invalid_invocations": 0, "replacement_attempts": 0,
            "static_read_stdout_encoding": "A PRD output attempt met console encoding error; corrected UTF-8 output and completed static read; no target effects"},
        final_input_comparison=comparison,
        administrative_helper_references=helper_refs,
        exclusions=INV["requested_scope"]["exclusions"],
        limitations=INV["limitations"] + [
            "No project/runtime/test execution, no actual product readiness assurance",
            "No exact conversational platform author ID/native start timestamp; none invented",
            "No exact filesystem publication timestamps; UTC preparation and readback observations distinguished",
            "No whole-framework re-Audit or global exclusive-writer claim",
            "Local records not remote backup"],
        next_permitted_process={"current": "Human assessment dispositions only; stop at handoff",
                                "candidate_after_dispositions": "Requirement Analysis, separately explicitly started and qualified",
                                "no_automatic_invocation": True},
        source_writes=False, product_artifact_writes=False, other_actor_record_writes=False,
        other_stage_started=False, nested_agents=False, orchestrator_activated=False,
        formal_requirement_or_plan_approval_claimed=False, human_acceptance_claimed=False,
        project_execution=False, staging_commit_push=False,
    )
    evidence_ref = publish("evidence/assessment-evidence.json", e)
    report_partial = BASE/"report.md.partial"
    text = report_partial.read_text(encoding="utf-8")
    assert text.startswith("# Initial SupportIQ SDLC Portability Assessment\n")
    assert WORK in text and ATTEMPT in text and OVERALL in text
    assert all("### C-" + f"{i:02}" in text for i in range(1,9))
    assert text.count("| **VERIFIED COMPATIBILITY** |") == 2
    assert text.count("| **COMPATIBILITY WITH IDENTIFIED ADAPTATION** |") == 4
    assert text.count("| **UNVERIFIED / INSUFFICIENT EVIDENCE** |") == 2
    for bad in ["[stable repository", "[exact scope", "[state]", "not assigned", "`n", "\\n"]:
        assert bad not in text, bad
    assert text.endswith("\n") and len(text) > 20000
    assert not (BASE/"report.md").exists()
    with report_partial.open("rb+") as f:
        f.flush()
        os.fsync(f.fileno())
    before = report_partial.read_bytes()
    os.rename(report_partial, BASE/"report.md")
    assert (BASE/"report.md").read_bytes() == before
    report_ref = ref(BASE/"report.md", ATTEMPT+":report")
    check_ref(evidence_ref)
    terminal_comparison = current_input_comparison()
    result = common("result", CREATOR)
    result.update(
        execution_status="COMPLETED", outcome=OVERALL,
        report=report_ref, evidence=evidence_ref, invocation=inv_ref,
        related_records=[ref(BASE/"checkpoint-0001.json", ATTEMPT+":checkpoint")],
        evaluated_state={
            "source": INV["repository_context"]["source"], "target": INV["repository_context"]["target"],
            "source_inventory": {"record": inv_ref, "json_member": "source_inventory", "files": 76},
            "target_inventory": {"record": evidence_ref, "json_member": "target_project.inventory", "files": 2},
            "head_alone_sufficient": False, "final_comparison": terminal_comparison},
        dimension_outcomes=DIMENSIONS,
        recommended_possible_blockers=BLOCKERS,
        human_disposition_status="PENDING for PB-01 and PB-02; no AI applicability decision",
        unresolved_items=["PB-01 Human applicability/rationale and target workflow mapping",
                          "PB-02 Human stage-scoped applicability/rationale",
                          "Target design, security, evaluation/threshold, CI/deployment and runtime evidence per report; not all prerequisites to initial analysis"],
        next_permitted_process={"now": "Human review and actual scoped possible-blocker dispositions; stop",
                                "candidate_only_after_resolution": "Separately started Requirement Analysis against exact draft PRD and this handoff",
                                "fresh_human_stage_start_required": True, "agent_invocation_authorized_by_this_result": False},
        publication={
            "required_report_evidence_available_before_result": True,
            "validation": "Common schema/required fields, complete native JSON object roundtrip, .partial readback, all bound references, flush/fsync, same-filesystem Windows atomic no-overwrite rename",
            "exact_publication_timestamp": "Not captured or inferred",
            "fresh_terminal_readback": "Required subsequent independent command; not preclaimed in this immutable result"},
        limitations=e["limitations"],
        source_writes=False, product_artifact_writes=False, other_actor_record_writes=False,
        nested_agents=False, later_process_started=False, orchestrator_activated=False,
        formal_approvals_claimed=False, human_acceptance_claimed=False,
        project_execution=False, staging_commit_push=False,
    )
    result_ref = publish("result.json", result)
    print(json.dumps({"report":report_ref, "evidence":evidence_ref, "result":result_ref,
                      "overall":OVERALL, "terminal_readback":"Still required in separate command"},indent=2))

if __name__ == "__main__":
    assert sys.argv[1:] == ["finalize"]
    finalize()
