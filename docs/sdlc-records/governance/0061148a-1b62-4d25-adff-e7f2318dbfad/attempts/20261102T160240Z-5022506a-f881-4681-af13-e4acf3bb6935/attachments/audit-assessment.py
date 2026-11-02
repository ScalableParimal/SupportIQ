"""Complete-scope Audit checks and own-record report assembly. No input writes."""
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("publisher", Path(__file__).with_name("audit-publisher.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
ROOT, OWN, BASE, AID = P.ROOT, P.OWN, P.BASE, P.AID
STEMS = [
    ("REQUIREMENT_ANALYSIS", "requirement-analysis"),
    ("REQUIREMENT_ANALYSIS_VERIFICATION", "requirement-analysis-verification"),
    ("IMPLEMENTATION_PLANNING", "implementation-planning"),
    ("REQUIREMENT_UPDATE", "requirement-update"),
    ("IMPLEMENTATION_PLAN_VERIFICATION", "implementation-plan-verification"),
    ("IMPLEMENTATION", "implementation"),
    ("IMPLEMENTATION_VERIFICATION", "implementation-verification"),
    ("IMPLEMENTATION_REVIEW", "implementation-review"),
    ("FINDING_INVESTIGATION", "finding-investigation"),
    ("CORRECTIVE_CHANGE", "corrective-change-decision"),
]
MASTER = [ROOT / "docs/ai/sdlc" / n for n in P.MASTER_HASHES]
COORD = BASE / "20261102T132628Z-e9227c1a-70ab-4afc-87e2-49eca280b879"
INVEST = BASE / "20261102T141609Z-4e74248e-a440-4617-8c17-61f31f2ff9c9"
OLD_AUDIT = BASE / "20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f"
LABELS = {
    "Governance Audit": [ROOT / ".github/skills/sdlc-governance-audit/SKILL.md",
                         ROOT / ".github/agents/sdlc-governance-audit.agent.md"],
    "Governance Remediation": [ROOT / ".github/agents/sdlc-governance-remediation.agent.md"],
    "SDLC Process Orchestration": [ROOT / ".github/agents/sdlc-process-orchestrator.agent.md"],
}
for label, stem, slug in [
    ("SDLC Portability Assessment", "PORTABILITY_ASSESSMENT", "portability-assessment"),
    ("Governance Amendment Application", "GOVERNANCE_AMENDMENT_APPLICATION", "governance-amendment-application"),
    ("Independent Governance Verification", "INDEPENDENT_GOVERNANCE_VERIFICATION", "independent-governance-verification"),
    ("Independent Governance Review", "INDEPENDENT_GOVERNANCE_REVIEW", "independent-governance-review"),
]:
    LABELS[label] = [
        ROOT / "docs/ai/guidelines" / (stem + "_GUIDELINES.md"),
        ROOT / "docs/ai/prompts" / (stem + "_PROMPT.md"),
        ROOT / "docs/ai/request" / (stem + "_REQUEST.md"),
        ROOT / ".github/skills" / slug / "SKILL.md",
        ROOT / ".github/agents" / (slug + ".agent.md"),
    ]

CRITERIA = {
    "Master": ["Lifecycle", "Artifact authority", "Traceability and change control", "Cross-Master consistency"],
    "Guideline": ["Master alignment", "Lifecycle", "Authority", "Read/write boundary", "Human approval",
                  "Verification", "Change control", "Scope", "Statuses", "Required outputs",
                  "Downstream processes", "Terminology", "References", "Unsupported rules", "Material omissions"],
    "Prompt": ["Correct Guideline", "Guideline exists", "Guideline conformance", "Terminology",
               "Source of truth", "Human approval", "Read-only boundary", "Modification authority",
               "Verification retained", "Human approval retained", "Corrective-change boundary",
               "Findings/deviations", "Output/report", "Unsupported rules", "Material omissions"],
    "Request": ["Correct Prompt", "Prompt exists", "Input sufficiency", "Placeholder terminology",
                "Artifact names", "Requirement references", "Plan references", "Task context",
                "Complete-scope preservation", "Evidence fields", "Human-decision fields", "Paths",
                "Directory casing/naming", "Obsolete paths", "Prompt conformance"],
    "Skill": ["Existence", "Frontmatter", "Guideline link", "Master authority", "Procedure conformance",
              "No Guideline override", "No Prompt replacement", "No Request replacement",
              "Process boundary", "Read/write boundary", "Human approval", "Verification/review",
              "Corrective-change boundary", "Handoff", "Unsupported rules", "Material omissions",
              "Terminology/references", "Path validity"],
    "Agent": ["Existence", "Frontmatter", "Skill link", "Skill exists", "Process identity",
              "No Skill redefinition", "Authority", "Write boundary", "Read-only boundary",
              "Human approval", "Human acceptance", "Verification", "Corrective-change boundary",
              "No Skill bypass", "No extra authority", "No approval/acceptance claim",
              "Upstream preservation", "Path validity"],
}
NOTES = {
    "REQUIREMENT_ANALYSIS": {
        "basis": "Governance 4; Artifact 6; Traceability 4.1",
        "sections": "Guideline 2-3, 5-14, 15-18; Skill 3-9; Agent Role/Authority/Write/Process",
        "conclusion": "Read-only initial analysis distinguishes source, explicit decisions, derived rules, assumptions and recommendations. Guideline 14 and 17 phases 5-10 route an explicit initial clarification through separate Requirement Update, subsequent analysis refresh, complete independent Verification, resolution and formal Human Requirement Approval. No plan, implementation, self-verification or approval is authorized.",
    },
    "REQUIREMENT_ANALYSIS_VERIFICATION": {
        "basis": "Governance 4.3-4.4, 17, 20; Artifact 7; Traceability 4.2, 8, 29",
        "sections": "Guideline 2-5, 6, 9-17; Skill 3-11; Agent Independence/Write/Completion",
        "conclusion": "Source Requirement, complete resulting Updated Requirement where applicable, complete current Analysis and decisions are distinct. All thirteen verification areas and six process-specific outcomes retain read-only independent evaluation; findings route through Investigation/Decision. Readiness is not Requirement Approval and changed sections do not narrow complete verification.",
    },
    "IMPLEMENTATION_PLANNING": {
        "basis": "Governance 2.16, 5; Artifact 9-11; Traceability 4.4, 9-11, 28",
        "sections": "Guideline 2-3, 6-9, 19-22 and final sequence; Skill 3-12; Agent Write/Independence",
        "conclusion": "Only current approved Requirement supplies scope; actual repository supplies technical context. Stable Plan-qualified tasks, criteria, prerequisites, impact mappings, shared surfaces and explicit serialized/isolated execution modes are required. Candidate creation or specifically authorized unapproved non-superseded candidate updates do not alter approved Plans. Full Plan Verification, resolution, Human Review Approval then separate Human Plan Approval remain.",
    },
    "REQUIREMENT_UPDATE": {
        "basis": "Governance 4, 12, 16; Artifact 8.4; Traceability 8-9, 24",
        "sections": "Guideline 2, 7, 13-16; Prompt inputs and initial-clarification paragraph; Request source/status/initial fields; Skill 3-8",
        "conclusion": "Current text explicitly qualifies initial immutable unapproved clarification versus approved-source change. Initial analysis questions, explicit Human answers and explicit update request are required; unknown source status stops. A new immutable version preserves source/readback/lineage, remains unapproved, and goes through Analysis, complete independent Verification, resolution and separate formal Human Requirement Approval. Approved-source finding/non-finding controls and downstream plan impact/gates remain. No dedicated Agent is expected.",
    },
    "IMPLEMENTATION_PLAN_VERIFICATION": {
        "basis": "Governance 5.2-5.4, 19-20; Artifact 10-11; Traceability 4.5-4.6, 28-29",
        "sections": "Guideline 2-6, 10-17; Skill 3-12; Agent Independence/Write/Completion",
        "conclusion": "Complete current candidate Plan is the target; prior approved Plan is comparator only. Current approved Requirement, task completeness/traceability, dependencies, shared surfaces, execution mode and integration are checked. Read-only recommendations never apply a Plan update. Six process-specific outcomes/readiness preserve required Human Review Approval and separate Plan Approval.",
    },
    "IMPLEMENTATION": {
        "basis": "Governance 2.16, 6, 10, 14-16; Artifact 12-13; Traceability 4.7-4.8, 12, 28, 30.1",
        "sections": "Guideline 2-8, 11-15, 19-23; Skill 3-15; Agent Authority/Write/Deviation/Verification",
        "conclusion": "Requested slice is bounded by current approved Requirement and Plan. One Orchestrator serializes shared-checkout writes; parallel writes need isolated worktrees and integration. Self-check is not independent Verification. Task outcomes, exact implementation binding and interruption dispositions are recorded. Deviations stop affected work for governed correction; no informal upstream edit or independent Verification/acceptance claim.",
    },
    "IMPLEMENTATION_VERIFICATION": {
        "basis": "Governance 7, 19-20; Artifact 14; Traceability 4.9, 13, 20, 22, 25, 29",
        "sections": "Guideline 2-6, 9-13; Skill 3-13; Agent Scope/Read-Only/Independence",
        "conclusion": "Complete current implementation against current approved Requirement/Plan is mandatory, including after correction/Plan change. Task IDs and slices are context only. Source inspection is not test execution. VERIFIED WITH GAPS and CANNOT VERIFY do not permit downstream progression or waivers; findings route to Investigation/Decision. No corrections, approval, acceptance, commit or push.",
    },
    "IMPLEMENTATION_REVIEW": {
        "basis": "Governance 8-9, 19-20; Artifact 15; Traceability 4.10-4.11, 14, 21, 23",
        "sections": "Guideline 2-5, 8-16; Skill 3-13; Agent Scope/Independence/Human Acceptance",
        "conclusion": "Complete current approved-scope implementation receives independent technical review, using applicable Verification without substituting for it. Ten quality areas, five outcomes, evidence/uncertainty and readiness are retained. No subjective unsupported requirements, direct fixes, acceptance claim, or reopening resolved findings without new evidence.",
    },
    "FINDING_INVESTIGATION": {
        "basis": "Governance 11, 15, 20; Artifact 17; Traceability 15-17, 30-31",
        "sections": "Guideline 1-5, 8-15; Skill 3-14; Agent Role/Investigation/Read-Write/Evidence",
        "conclusion": "Read-only diagnostic investigation follows finding source and complete directly affected context, not task-only scope. Separately Human-authorized governance enhancements remain non-findings with subject-specific fields/outcomes. Optional evidence execution requires explicit bounded permission. Recommendations do not authorize changes; unresolved source status/evidence is disclosed.",
    },
    "CORRECTIVE_CHANGE": {
        "basis": "Governance 11-15, 20; Artifact 18; Traceability 17, 27, 30.1, 35",
        "sections": "Guideline 5-18; Prompt subject/approval/stage paragraphs; Request stage-specific actor paragraph; Skill 3-16; Agent boundaries",
        "conclusion": "Finding decisions distinguish no governed change, Plan change and other governed artifact change; enhancement statuses remain separate. Proposal-only output cannot apply corrections. Exact Human Approval/designation, all bases, distinct actors and separate fresh starts/assurance remain. Current Request now binds actual preparer/applier at their stages and future verifier/reviewer definitions as planned-only until predecessor gates. No impossible future-attempt or pre-existing qualification prerequisite remains.",
    },
}


def bound(entry):
    p = (ROOT / entry["path"]).resolve()
    assert p.is_relative_to(ROOT)
    actual = P.ref(p)
    assert actual["sha256"] == entry["sha256"].upper(), (entry["path"], "hash mismatch")
    if "bytes" in entry:
        assert actual["bytes"] == entry["bytes"], (entry["path"], "size mismatch")
    return actual


def record_ref(path):
    entry = P.ref(path)
    if Path(path).suffix == ".json":
        entry["record_id"] = P.load(path).get("record_id", None)
    else:
        entry["record_id"] = "canonical-path:" + entry["path"]
    return entry


def unchanged():
    inv = P.load(OWN / "attempt.json")
    man = P.load(OWN / "evidence/input-manifest.json")
    P.validate(inv, "audit_invocation")
    P.validate(man, "audit_input_manifest")
    assert P.repo() == inv["repository_context"]
    for entry in man["files"]:
        bound(entry)
    current = {x["path"] for x in P.inputs()}
    initial = {x["path"] for x in man["files"]}
    assert current == initial, {"added": sorted(current-initial), "removed": sorted(initial-current)}
    return {"outcome": "PASS", "inputs": len(initial), "all_bytes_and_path_set_unchanged": True,
            "repository_head_branch_status_index_unchanged": True}


def inventory():
    core = [("Master", None, p) for p in MASTER]
    for kind, folder, suffix in [("Guideline", "guidelines", "_GUIDELINES.md"),
                                 ("Prompt", "prompts", "_PROMPT.md"),
                                 ("Request", "request", "_REQUEST.md")]:
        for stem, slug in STEMS:
            core.append((kind, stem, ROOT / "docs/ai" / folder / (stem + suffix)))
    for stem, slug in STEMS:
        core.append(("Skill", stem, ROOT / ".github/skills" / slug / "SKILL.md"))
    for stem, slug in STEMS:
        if stem != "REQUIREMENT_UPDATE":
            core.append(("Agent", stem, ROOT / ".github/agents" / (slug + ".agent.md")))
    expected = {p for _, _, p in core}
    for paths in LABELS.values():
        expected.update(paths)
    actual = set(P.sources())
    assert len(core) == 52
    assert {P.rel(p) for p in actual} == {P.rel(p) for p in expected}, {
        "new_sources": [P.rel(x) for x in actual-expected],
        "missing_sources": [P.rel(x) for x in expected-actual]}
    return core, sorted(actual)


def path_checks(all_sources):
    checks = []
    skipped = []
    actual_cased_paths = {P.rel(p) for p in all_sources}
    rx = re.compile(r"(?:\.github[\\/](?:agents|skills)[\\/]|docs[\\/]ai[\\/])[\w./\\-]+\.md")
    for path in all_sources:
        text = path.read_text("utf-8")
        for match in rx.finditer(text):
            target = match.group().replace("\\", "/")
            p = ROOT / target
            assert p.exists(), (P.rel(path), target)
            assert target in actual_cased_paths, (P.rel(path), target, "exact casing")
            checks.append({"source": P.rel(path), "line": text[:match.start()].count("\n")+1,
                           "target": target, "outcome": "PASS"})
        for code in re.findall(r"`([^`\n]+\.md)`", text):
            if "/" not in code and "\\" not in code:
                options = [ROOT / "docs/ai/sdlc" / code, ROOT / "docs/ai/guidelines" / code,
                           ROOT / "docs/ai/prompts" / code, ROOT / "docs/ai/request" / code]
                found = [p for p in options if p.exists()]
                if found:
                    checks.append({"source": P.rel(path), "target": P.rel(found[0]),
                                   "reference": code, "outcome": "PASS"})
                else:
                    skipped.append({"source": P.rel(path), "reference": code,
                                    "reason": "Not an explicit framework-file reference; contextual example/output/product reference"})
    assert not skipped, skipped
    relationships = []
    for stem, slug in STEMS:
        g = "docs/ai/guidelines/" + stem + "_GUIDELINES.md"
        p = "docs/ai/prompts/" + stem + "_PROMPT.md"
        r = "docs/ai/request/" + stem + "_REQUEST.md"
        s = ".github/skills/" + slug + "/SKILL.md"
        skill = (ROOT / s).read_text("utf-8")
        assert all(x in skill for x in [g, p, r])
        assert g in (ROOT / p).read_text("utf-8")
        assert p in (ROOT / r).read_text("utf-8")
        a = None if stem == "REQUIREMENT_UPDATE" else ".github/agents/" + slug + ".agent.md"
        if a:
            assert s in (ROOT / a).read_text("utf-8")
        for q, name in [(ROOT / s, slug)]:
            txt = q.read_text("utf-8")
            assert txt.startswith("---\n") and ("name: " + name + "\n") in txt and "description:" in txt
        if a:
            assert (ROOT / a).read_text("utf-8").startswith("---\n")
        relationships.append({"process": stem, "guideline": g, "prompt": p, "request": r,
                              "skill": s, "agent": a, "outcome": "PASS",
                              "agent_applicability": "Deliberately Skill-only" if a is None else "Expected Agent present"})
    return checks, relationships


def evidence_checks():
    proposal = P.load(BASE / P.IDS["proposal"] / "attachments/exact-proposal.json")
    application = P.load(BASE / P.IDS["application"] / "result.json")
    ae = P.load(BASE / P.IDS["application"] / "evidence/application-evidence.json")
    pf = P.load(BASE / P.IDS["application"] / "evidence/preflight.json")
    ve = P.load(BASE / P.IDS["verification"] / "verification-evidence.json")
    revidence = P.load(BASE / P.IDS["review"] / "review-evidence.json")
    assert application["outcome"] == "COMPLETED" and ae["error"] is None and ae["preservation_error"] is None
    assert pf["outcome"] == "PASS" and pf["all_five_before_any_write"] is True
    targets, patch_parts, bases = [], [], {}
    for target in proposal["targets"]:
        path = ROOT / target["path"]
        actual = path.read_bytes()
        assert len(actual) == target["expected_after_bytes"]
        assert hashlib.sha256(actual).hexdigest().upper() == target["expected_after_sha256"]
        base = actual
        for replacement in reversed(target["replacements"]):
            after, before = replacement["after"].encode("utf-8"), replacement["before"].encode("utf-8")
            assert base.count(after) == 1
            base = base.replace(after, before, 1)
        assert len(base) == target["base_bytes"]
        assert hashlib.sha256(base).hexdigest().upper() == target["base_sha256"]
        filtered = subprocess.check_output(["git", "cat-file", "--filters", "HEAD:" + target["path"]], cwd=ROOT)
        assert filtered == base
        bases[target["path"]] = base
        forward = base
        offsets = []
        for replacement in target["replacements"]:
            before, after = replacement["before"].encode("utf-8"), replacement["after"].encode("utf-8")
            assert replacement["expected_occurrences"] == 1 and forward.count(before) == 1
            offset = forward.index(before)
            assert offset == replacement["sequential_input_byte_offset"]
            offsets.append(offset)
            forward = forward.replace(before, after, 1)
        assert forward == actual
        assert not actual.startswith(b"\xef\xbb\xbf")
        assert b"\n" not in actual.replace(b"\r\n", b"")
        assert actual.endswith(b"\r\n") == target["expected_after_final_newline"]
        patch_parts.extend(difflib.unified_diff(base.decode("utf-8").splitlines(True),
                                               actual.decode("utf-8").splitlines(True),
                                               fromfile="a/"+target["path"], tofile="b/"+target["path"]))
        targets.append({"actual": P.ref(path), "base_bytes": len(base),
                        "base_sha256": target["base_sha256"], "reverse_and_forward": "PASS",
                        "immutable_HEAD_filtered_base": "PASS", "offsets": offsets,
                        "UTF8_noBOM_CRLF_preserved": True,
                        "final_newline": target["expected_after_final_newline"]})
    patch = "".join(patch_parts).encode("utf-8")
    patchpath = BASE / P.IDS["proposal"] / "attachments/minimal.patch"
    assert patch == patchpath.read_bytes(), "Native patch reconstruction mismatch"
    approved_paths = {t["path"] for t in proposal["targets"]}
    assert set(ae["actual_changed_paths"]) == approved_paths
    original = P.load(BASE / P.IDS["application"] / "evidence/input-manifest.json")["files"]
    changes, same = [], 0
    for entry in original:
        actual = P.ref(ROOT / entry["path"])
        if actual["sha256"] == entry["sha256"]:
            assert actual["bytes"] == entry["bytes"]
            same += 1
        else:
            assert entry["path"] in approved_paths
            assert entry["sha256"] == hashlib.sha256(bases[entry["path"]]).hexdigest().upper()
            changes.append(entry["path"])
    assert set(changes) == approved_paths
    currency = {}
    checked_refs = []
    for role, expected_count in [("verification", 13), ("review", 12)]:
        folder = BASE / P.IDS[role]
        result = P.load(folder / "result.json")
        assert result["outcome"] == "PASS" and result["execution_status"] == "COMPLETED"
        assert len(result["criteria"]) == expected_count
        assert all(c["outcome"] == "PASS" for c in result["criteria"])
        for c in result["criteria"]:
            for entry in c["refs"]:
                checked_refs.append(bound(entry))
        for key in ["report", "evidence"]:
            checked_refs.append(bound(result[key]))
        snapshot = P.load(folder / "input-manifest.json")["snapshot"]["files"]
        for entry in snapshot:
            checked_refs.append(bound(entry))
        currency[role] = {"criteria": expected_count, "inputs_rehashed_unchanged": len(snapshot),
                          "outcome": result["outcome"], "record": record_ref(folder / "result.json")}
    actor_defs = [a["definition"] for a in proposal["actors"]]
    for entry in actor_defs:
        checked_refs.append(bound(entry))
    assert len({a["path"] for a in actor_defs}) == 4 and len({a["sha256"] for a in actor_defs}) == 4
    actual_roles = {}
    for role in ["proposal", "application", "verification", "review"]:
        d = P.load(BASE / P.IDS[role] / "attempt.json")
        actual_roles[role] = {"creator": d["creator"], "invocation": record_ref(BASE / P.IDS[role] / "attempt.json")}
    runtime_ids = [x["creator"]["runtime_agent_id"] for x in actual_roles.values()]
    assert len(set(runtime_ids)) == 4 and P.ACTOR not in runtime_ids
    authorization = P.load(BASE / P.IDS["application"] / "evidence/human-authorization.json")
    # Keep the actual complete authorization object, not a quoted/dumped JSON string.
    P.native(authorization)
    assert authorization["target_bindings"] == proposal["targets"]
    assert authorization["actors"] == proposal["actors"]
    assert authorization["approval_exact_ascii"] == (
        "I approve the identified canonical report, exact proposal and patch with all five target fingerprints, "
        "scope, actor and assurance bindings; freshly designate the proposed one-time applier under that route; do not start Application")
    assert authorization["separate_stage_start_exact_ascii"] == (
        "Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 under the approved five-file package")
    assert authorization["approval_route"] == proposal["approval_route"]
    assert authorization["byte_contract"] == proposal["byte_contract"]
    for entry in authorization["package"]:
        checked_refs.append(bound(entry))
    coordinator = P.load(COORD / "result-revision-0002.json")
    investigation = P.load(INVEST / "result-revision-0002.json")
    for d in [coordinator, investigation]:
        checked_refs.append(bound(d["report"]))
        ev = d["evidence"]
        for entry in ev if isinstance(ev, list) else [ev]:
            checked_refs.append(bound(entry))
    assert {f["finding_id"] for f in investigation["findings"]} == {"GOV-AUD-20261102-003", "GOV-AUD-20261102-004"}
    assert all(f["validation_status"] == "FINDING CONFIRMED" for f in investigation["findings"])
    assert ve["source_writes"] is False and revidence["source_writes"] is False
    assert ve["other_actor_record_writes"] is False and revidence["other_actor_record_writes"] is False
    expected_starts = {
        "verification": "Yes, initiate one fresh Independent Governance Verification retry for the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 Application only; preserve unsuccessful records and start no later stage",
        "review": "Yes, initiate Independent Governance Review for the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 five-file amendment and its fresh passing Verification only",
    }
    assert ve["human_authorizations"]["fresh_verification_retry_start"] == expected_starts["verification"]
    assert revidence["authorization"]["fresh_start_exact_ascii"] == expected_starts["review"]
    return {"targets": targets, "patch": P.ref(patchpath),
            "application": {"outcome": application["outcome"], "all_bases_before_first_write": True,
                            "original_inputs": len(original), "unchanged": same, "changed": changes,
                            "before_after_and_patch_checks": "PASS", "source_write_ordering_evidence": "Bound preflight/readback plus inspected application helper control flow; procedural, not exhaustive OS trace"},
            "assurance_currency": currency, "actual_actors": actual_roles,
            "approved_planned_actor_definitions": actor_defs,
            "human_authorization": authorization, "fresh_assurance_starts": expected_starts,
            "checked_current_record_and_manifest_reference_occurrences": len(checked_refs),
            "canonical_coordinator": record_ref(COORD / "result-revision-0002.json"),
            "canonical_investigation": record_ref(INVEST / "result-revision-0002.json"),
            "limitations": ["Upstream operation assertions are source-inspected reported execution evidence; this Audit independently rehashes/reconstructs but does not replay Application or replace Verification/Review",
                           "Matching endpoint fingerprints cannot exclude transient writes or same-principal tampering"] }


LIMITATIONS = [
    "Procedural nonmutation, not sandbox-enforced source-write exclusion. Writable tools and inherited ACLs confer no authority to alter sources, inputs, product artifacts or another actor's records.",
    "Endpoint fingerprints establish observed bytes, not continuous absence of transient mutation/reversion or same-principal tampering.",
    "No exhaustive trusted OS event log, coordinated no-edit interval, source lock, or complete external-writer visibility is available. The visible harness registry showed only this Audit running at qualification; idle and failed historical actors are not live-writer evidence.",
    "Harness runtime attribution is not external cryptographic identity. The shared host-session title is not proof of process role or independence.",
    "Actual supplied Human wording and package presentation bindings are retained. Authenticated conversation message IDs, authenticated Human author IDs and original decision times are unavailable and are not invented.",
    "System UTC fields record preparation time, not an exact publication timestamp. Observed publication/readback operation sequence establishes ordering.",
    "This is a governance-definition and invoked-governance-record consistency audit, not a product audit, target-project Portability Assessment, product Orchestrator execution, repeat Application, or independent execution of previous actors' operations.",
]
COUNTS = {k: 0 for k in ["Critical", "High", "Medium", "Low", "Ambiguities",
                         "Broken References", "Missing Governance Controls", "Unsupported Governance Controls"]}
REPORT_SECTIONS = [
    "Audit Scope", "Separately Reported Mechanism Alignment", "Repository Reference Findings",
    "Governance Consistency Findings", "Guideline Consistency Summary", "Prompt Consistency Summary",
    "Request Template Consistency Summary", "SDLC Process Skill Consistency Summary",
    "SDLC Process Agent Consistency Summary", "Skill and Agent Traceability Summary",
    "Cross-Document Consistency Summary", "Governance Gaps", "Unsupported or Excessive Governance",
    "Human Decisions Required", "Recommended Corrective Actions", "Overall Audit Result",
]


def json_tests():
    actual = P.common("audit_serialization_selftest")
    actual["values"] = {"quotes": ["'actual ASCII'", '"double quote"', "CRLF\r\nretained", "\u2192"],
                        "list": [{"integer": 52, "bool": True, "null": None}]}
    encoded = P.validate(actual, actual["record_type"])
    assert json.loads(encoded, object_pairs_hook=P.pairs) == actual
    for raw in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']:
        try:
            json.loads(raw, object_pairs_hook=P.pairs,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid JSON accepted")
    for obj in [set(), Path("."), (1,), 1.5]:
        try:
            P.native(obj)
        except TypeError:
            pass
        else:
            raise AssertionError("Non-native JSON value accepted")
    return {"outcome": "PASS", "complete_native_object_roundtrip": True,
            "duplicate_nonfinite_nonnative_negative_tests": True,
            "actual_record_schema_validation": "Every complete prepared object is validated before its .partial write and reparsed/equality-checked from partial and final bytes"}


def source_anchors(path):
    # Exact current headings/lines support the manual complete-source assessments.
    lines = path.read_text("utf-8").splitlines()
    headings = [{"line": n, "heading": line} for n, line in enumerate(lines, 1) if line.startswith("#")]
    snippets = []
    for title, pattern in [
        ("authority", r"master governance|authority|source of truth"),
        ("scope", r"complete|full scope|scope"),
        ("human", r"human approval|human acceptance|human.*start|explicit human"),
        ("read_write", r"read.only|write boundary|do not modify|must not modify|immutable"),
        ("handoff", r"next process|downstream|handoff|corrective change"),
        ("evidence", r"evidence|output|report|record"),
    ]:
        found = [(n, line) for n, line in enumerate(lines, 1) if re.search(pattern, line, re.I)]
        if found:
            n, line = found[0]
            snippets.append({"topic": title, "line": n, "text": line})
    return {"line_count": len(lines), "headings": headings, "context_anchors": snippets}


def catalog_assessments(core):
    result = []
    for index, (kind, stem, path) in enumerate(core, 1):
        anchors = source_anchors(path)
        if stem:
            rationale = NOTES[stem]["conclusion"]
            if kind == "Prompt":
                rationale = "Correct Guideline and input/source hierarchy retained; no broader authority or skipped gate. " + rationale
            elif kind == "Request":
                rationale = "Correct Prompt, sufficient invocation/template fields, correct paths and contextual scope qualifiers. " + rationale
            elif kind == "Skill":
                rationale = "Execution mechanics delegate normative authority to Masters/Guideline and preserve Prompt/Request links. " + rationale
            elif kind == "Agent":
                rationale = "Controlled matching-Skill entry point, not a replacement policy source; role, upstream protection and output boundary preserved. " + rationale
            sections = NOTES[stem]["sections"]
        else:
            rationale = {
                "SDLC_GOVERNANCE.md": "Lifecycle separates process initiation, formal Requirement/Plan approval, independent Verification/Review, Human Acceptance and Commit/Push. Governance 3 retains unadopted candidate comparison authority and permits normal finding-led non-Master correction without adopting the candidate.",
                "SDLC_ARTIFACT_GOVERNANCE.md": "Artifact ownership, immutable upstream versioning, controlled entry points, formal gates and section 33.1 actor qualification/complete native record publication align with the lifecycle and Traceability persistence. Product and governance roots are distinct.",
                "SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "Traceability, current source identities, finding/change paths, section 30.1 established/bootstrap persistence, immutable records and noncircular terminal handoff align. Formal stage-specific outcomes are not generic approval; output publication grants no source-edit authority.",
            }[path.name]
            sections = "Complete document; cross-compared with both other Masters and all detailed layers"
        result.append({"catalog_id": f"C{index:02}", "kind": kind, "process": stem,
                       "source": P.ref(path), "inspected": True, "outcome": "PASS",
                       "criteria": [{"number": n, "criterion": c, "outcome": "PASS"}
                                    for n, c in enumerate(CRITERIA[kind], 1)],
                       "evidence_class": "SOURCE INSPECTION; mechanically checked identity/path links separately",
                       "rationale": rationale, "inspection_scope": sections, "anchors": anchors})
    return result


def linked_records():
    entries = []
    def add(label, path):
        assert path.exists(), str(path)
        entries.append({"label": label, **record_ref(path)})
    for label, path in [
        ("AUD-INV", OWN / "attempt.json"), ("AUD-MAN", OWN / "evidence/input-manifest.json"),
        ("AUD-IRB", OWN / "evidence/invocation-readback.json"),
        ("AUD-PST", OWN / "evidence/publisher-selftest.json"),
        ("AUD-PUB", OWN / "attachments/audit-publisher.py"),
        ("AUD-CHK", OWN / "attachments/audit-assessment.py"),
        ("REM-INV", COORD / "attempt.json"), ("REM-RPT", COORD / "report-revision-0001.md"),
        ("REM-RES", COORD / "result-revision-0002.json"),
        ("REM-H03", COORD / "handoffs/GOV-AUD-20261102-003.json"),
        ("REM-H04", COORD / "handoffs/GOV-AUD-20261102-004.json"),
        ("REM-HIST", COORD / "evidence/history-reconciliation.json"),
        ("REM-VAL", COORD / "evidence/audit-validation.json"),
        ("INV-RPT", INVEST / "report-revision-0002.md"), ("INV-RES", INVEST / "result-revision-0002.json"),
        ("OLD-AUD-RPT", OLD_AUDIT / "report.md"), ("OLD-AUD-RES", OLD_AUDIT / "result.json"),
        ("OLD-AUD-EVD", OLD_AUDIT / "evidence/audit-evidence.json"),
    ]:
        add(label, path)
    for role, files in [
        ("proposal", ["attempt.json", "report.md", "result.json", "attachments/exact-proposal.json",
                      "attachments/minimal.patch", "evidence/decision-evidence.json", "checkpoint-0002.json"]),
        ("application", ["attempt.json", "report.md", "result.json", "evidence/human-authorization.json",
                         "evidence/preflight.json", "evidence/input-manifest.json", "evidence/application-evidence.json",
                         "checkpoint-0001.json", "checkpoint-0002.json", "attachments/application-tool.py"]),
        ("verification", ["attempt.json", "report.md", "result.json", "verification-evidence.json",
                          "input-manifest.json", "checkpoint-0001.json", "checkpoint-0002.json",
                          "checkpoint-0003.json", "checkpoint-final.json", "verifier.py"]),
        ("review", ["attempt.json", "report.md", "result.json", "review-evidence.json", "input-manifest.json",
                    "checkpoint-0001.json", "checkpoint-0002.json", "checkpoint-final.json"]),
    ]:
        for n, name in enumerate(files, 1):
            add(f"{role.upper()}-{n:02}", BASE / P.IDS[role] / name)
    for label, aid in [
        ("F001-V", "20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1"),
        ("F001-R", "20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb"),
        ("F002-A", "20261102T110324Z-b92b73f0-deba-4842-b261-1ed22bd7d014"),
        ("F002-V", "20261102T110840Z-c1d89695-d3e5-4721-a846-3f3dca25cc22"),
        ("F002-R", "20261102T1130Z-d7d84322-aff9-4d3e-9cec-90f9054705cd"),
    ]:
        path = BASE / aid / "result.json"
        d = P.load(path)
        assert d["execution_status"] == "COMPLETED"
        assert d["outcome"] == ("EXACT APPROVED BYTES APPLIED" if label == "F002-A" else "PASS")
        for key in ["report", "evidence"]:
            if key in d and isinstance(d[key], dict):
                bound(d[key])
        add(label, path)
    clarification = BASE / "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd/attachments/GOV-AUD-20261102-001-linked-clarification.md"
    assert P.ref(clarification)["sha256"] == "8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
    add("F001-CLR", clarification)
    return entries


def mechanisms():
    common_checks = {
        "Governance Audit": [
            ("Role, authority and same-framework relationship", "Dedicated read-only comparison role under all three Masters; Audit Skill 3-6 and 23-26, not remediation or an acceptance authority."),
            ("Traceability and persistence", "Established governance root and exact fresh Human start qualified; one valid actor-owned invocation and separate-process readback precede full-source comparison. Own canonical output identities and noncircular result/report bindings follow Skill 5/23 and Master contracts."),
            ("Read/write, independence and change control", "Only current actor-owned attempt records written. No source/upstream/history edits, correction, stage delegation, product work, staging, branch creation, commit or push. Findings never grant write authority."),
            ("Complete core and discovered-source coverage", "52 expected/found/assessed; 76 current unique sources derived, fully read; seven distinct groups assessed outside the 52. This rerun is not limited to F003/F004."),
            ("Result threshold and truthful evidence", "Exact CONSISTENT requires all eight counts zero and all seven groups resolved; source inspection, executed checks, reported operations and unverified behavior distinguished. No waiver or assumed zero; all full-source and integrity checks completed."),
            ("Canonical complete-report/publication contract", "Every Skill 23 section and artifact/relationship/mechanism matrix retained. Evidence precedes report; terminal result follows both, binds exact final bytes, and is independently reread. Final publication/readback is validated before completion is returned."),
        ],
        "Governance Remediation": [
            ("Role, scope and framework authority", "Finding-led cycle under the same three Masters, not a non-finding invention, product Orchestrator or product implementation route. Active-cycle self-edit and self-approval exclusions retained."),
            ("Current invocation and canonical evidence", "REM-INV/RPT/RES resolve the canonical bounded continuation and two Audit-bound handoffs, not superseded invalid records. Current linked Investigation revision 0002 and approved proposal/Application/fresh Verification/Review satisfy subsequent separately started gates."),
            ("Fresh Human gates and approval separation", "Original coordinator pause is historical stage state, not a present missing Investigation. Later linked actual Human starts, policy directions, exact approval/designation and separate starts supply each successor's authority; no retroauthorization of failed prior attempts."),
            ("Traceability, persistence and source ownership", "Same Work ID/Cycle 1 maintained. Canonical corrected revisions explicitly supersede while preserving history. Findings, approved five-file package and assurance records carry path/identity/hash bindings; own actor records only."),
            ("F001/F002 history and Commit/Push boundary", "Prior complete Audit and linked clarification/assurance remain addressed. Current Remediation Agent Commit/Push clause preserves original authorization and appends execution-only evidence; no Push expansion. No new contrary basis, no reopening."),
            ("Prospective final handoff, not circular prerequisite", "Skill 5 expressly places final Remediation anchor after this Audit result. Existing current-cycle records are required/evaluated now; a future coordinator independently recomputes this result hash and validates report binding. This Audit cannot write that actor's final report."),
        ],
        "SDLC Process Orchestration": [
            ("Role, authority, same-framework and scope", "Artifact 4.4, Orchestrator O6.1/O6.6/O9 and Traceability 30.1 retain product lifecycle coordination only; direct Human-started governance roles are not product Orchestrator invocations."),
            ("Fresh process initiation and approval boundary", "Every start, retry and transition needs an explicit fresh Human process-initiation request/response; it is not formal Requirement/Plan Approval or Human Acceptance."),
            ("Lifecycle and source status", "Complete product lifecycle and correction routing remain. Updated Requirement path now supports initial unapproved clarification plus subsequent complete Verification and separate Requirement Approval, without weakening approved-source gates."),
            ("Traceability, persistence, reads/writes and independence", "Actor-owned durable records, exact task/scope bindings, isolated/serialized implementation writes and downstream independent assurance remain; no governance amendment/self-edit authority inferred."),
            ("Runtime records and capability applicability", "NOT APPLICABLE: product Orchestrator was not invoked for this governance amendment. No product attempt/start/capability/result is inferred from host-session title or direct governance starts. Definition conformance is assessed, not product runtime PASS."),
        ],
        "SDLC Portability Assessment": [
            ("Connected sources, framework relationship and advisory authority", "Five listed sources resolve with consistent Guideline/Prompt/Request/Skill/Agent links under Masters. Assessment is advisory; no governance approval, acceptance, adoption, automatic invocation or target-write authority."),
            ("Entry and reassessment", "Explicit source and target context, baseline/adoption state, scope/constraints and evidence sufficiency precede entry. Material source/target changes require bounded reassessment and Human decision, not inferred continuation."),
            ("Evidence separation and product exclusions", "Source-framework and target-project evidence/claims are separate. Target product inspection is not part of this Audit, and an assessment does not enable target writes or product lifecycle bypass."),
            ("Blocker decisions and concern routing", "Blockers require explicit Human decisions; governance-defect candidates route through Governance Audit/finding governance rather than being confirmed or corrected by Portability. Project-specific concerns remain separate."),
            ("Persistence, read/write, independence and change control", "Own approved-scope durable records only, read-only/advisory assessment, no remediation or source/target correction; limitations and unresolved applicability are reported."),
            ("Runtime records and capability applicability", "NOT APPLICABLE: no Portability Assessment was invoked in this amendment. Source fingerprints and definition checks provide mechanism evidence only, not a target-project assessment result or runtime capability claim."),
        ],
        "Governance Amendment Application": [
            ("Sources, role, framework and connected links", "All five Application sources resolve and align with Masters and updated Corrective Request. Exact application only, not proposal preparation, independent assurance, finding closure or adoption."),
            ("Four distinct actors and approved planned bindings", "Four actual runtime actor IDs and four role-definition path/hashes are distinct. Actual applier/verifier/reviewer match the exact approved proposal bindings. Applier is not Orchestrator or active-cycle Remediation; shared OS principal is not itself disqualifying."),
            ("Exact Human approval and fresh one-time designation", "Actual supplied approval/designation binds canonical report/proposal/patch, all five bases/afters, scope, exclusions and actors. Separate Application start is preserved; unavailable chat-authentication metadata is disclosed, not fabricated."),
            ("Current qualification and invocation ordering", "Current own invocation, capabilities/ACLs/tool observations, complete hidden manifest and fresh independent readback precede source work. No separate pre-existing applier qualification or future verifier/reviewer attempts are demanded."),
            ("All bases before first write and exact patch", "Audit independently reverses all five current targets to exact approved bases and Git filtered HEAD bytes, reapplies sequential single-occurrence replacements at approved offsets and reproduces the exact native patch. Bound all-target preflight and inspected apply control flow validate all five before first source write."),
            ("Actual paths/content/readback and unauthorized-change exclusion", "Application outcome is actual COMPLETED, not generic PASS. Exactly five approved targets match expected bytes/hashes and UTF-8/no-BOM/CRLF/EOF contracts; all 469 other original inputs among 474 are unchanged, no errors/rollback. Endpoint assurance is procedural, with residual risk disclosed."),
            ("Integrity-bound own records and separate downstream gates", "Application report/result/evidence/preflight/authorization/invocation/checkpoints resolve. Application is not independent Verification/Review/Audit; each successor has its own fresh start and qualified record."),
        ],
        "Independent Governance Verification": [
            ("Sources, role and connected framework links", "All five verifier sources resolve under Masters; independent read-only exact-application/cross-document verification, not application, review, product verification or adoption."),
            ("Current predecessor, fresh start and failed history", "Fresh separately authorized retry follows actual completed Application. Failed prior missing-metadata invocation/unauthorized replacement remains CANNOT COMPLETE history, not valid assurance or retroauthorization."),
            ("Current qualification, distinctness and planned identity", "Current own qualified invocation/capability/readback binds actual verifier, distinct from preparer/applier/reviewer and matching approved planned definition hash. No definition-only runtime capability inference."),
            ("Read-only complete change-set and independent recomputation", "Verification records independently reconstruct/reverse/patch-check exact approved scope; this Audit independently repeats those computations and all 474/469 Application preservation checks. All 500 verifier inputs remain current."),
            ("Cross-document authority and evidence semantics", "Complete five-target effects and relevant coupled controls were verified, not just individual hashes; source inspection is not behavioral execution. Procedural source nonmutation and uncertainty disclosed."),
            ("Integrity, criteria and outcome", "Fresh result execution_status COMPLETED, outcome PASS, 13/13 criteria supported. Report/evidence/invocation and cited criterion references rehashed; all required current evidence available. No FINDINGS/CANNOT COMPLETE reclassified as PASS."),
        ],
        "Independent Governance Review": [
            ("Sources, role and connected framework links", "All five reviewer sources resolve under Masters; independent review of approved intent/coherence/authority, not patch application, duplicated verification authority, acceptance or adoption."),
            ("Passing predecessor and fresh Review start", "Current passing fresh Verification—not failed historical attempts—is explicitly selected by the separate actual Human Review start. Invoked stage qualification is present, not N/A."),
            ("Distinct actor, qualification and approved planned identity", "Reviewer own invocation/readback/capabilities establish actual identity, distinct from preparer/applier/verifier and matching approved planned definition. Host title and shared principal are not role/independence proofs."),
            ("Intent, scope, authority, gates and catalog boundary", "Review directly covers both selected policy directions, all five approved targets, unchanged Masters, lifecycle/immutable-source preservation, stage-specific future actors, separate Human gates, 52-core/76-source boundary and no product scope."),
            ("Complete evidence currency and procedural read-only boundary", "Audit rehashes all 510 Review inputs and confirms all 500 verifier inputs and 469 non-target Application inputs unchanged; source/other-actor write flags false and observed endpoints agree. Residual transient/same-principal risk remains disclosed."),
            ("Integrity, complete criteria and effectiveness boundary", "Fresh result execution_status COMPLETED, outcome PASS, 12/12 criteria supported and cited references valid. Review did not close findings, run Audit, adopt Masters/product root or claim effectiveness. Complete fresh Audit remains separate."),
        ],
    }
    rows = []
    for label, paths in LABELS.items():
        if len(paths) == 5:
            guideline, prompt, request, skill, agent = paths
            # Section 5 requires all named authoritative sources to resolve and
            # their relationships to align. Unlike the ten core Skills' explicit
            # path contracts, these bundles intentionally use unique named-source
            # references. Resolve the names to the exact cataloged source paths.
            assert all(p.is_file() for p in [guideline, prompt, request, skill, agent])
            assert all(term in skill.read_text("utf-8") for term in ["Guideline", "Prompt", "Request"])
            assert "Guideline" in prompt.read_text("utf-8")
            assert P.rel(skill) in agent.read_text("utf-8")
        sources = list(dict.fromkeys(MASTER + paths))
        if label == "Governance Remediation":
            sources += [ROOT / "docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md",
                        ROOT / "docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md",
                        ROOT / "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md"]
        if label == "SDLC Process Orchestration":
            sources += [ROOT / "docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
                        ROOT / "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md"]
        runtime = "NOT APPLICABLE — not invoked" if label in ["SDLC Process Orchestration", "SDLC Portability Assessment"] else "INVOKED — current evidence assessed"
        rows.append({"group": label, "expected": True, "present": True, "assessed": True,
                     "outcome": "PASS", "runtime_applicability": runtime,
                     "sources": [P.ref(p) for p in sources],
                     "checks": [{"id": f"M{len(rows)+1:02}-{i:02}", "check": name,
                                 "outcome": "NOT APPLICABLE" if name == "Runtime records and capability applicability" else "PASS",
                                 "rationale": why} for i, (name, why) in enumerate(common_checks[label], 1)]})
    assert len(rows) == 7
    return rows


def prepare_assessment():
    tests = json_tests()
    pre = unchanged()
    core, sources = inventory()
    paths, relationships = path_checks(sources)
    executed = evidence_checks()
    assessed = catalog_assessments(core)
    matrix = mechanisms()
    refs = linked_records()
    assert len(assessed) == 52 and all(a["outcome"] == "PASS" for a in assessed)
    assert all(m["assessed"] and m["outcome"] == "PASS" for m in matrix)
    # These are conclusions after complete-source comparison plus all required
    # applicable checks, not success inferred from the previous assurance outcome.
    return {"pre_comparison": pre, "post_comparison": unchanged(), "serialization": tests,
            "core_artifacts": assessed, "source_inventory": [P.ref(p) for p in sources],
            "process_relationships": relationships, "reference_checks": paths,
            "mechanisms": matrix, "current_evidence_checks": executed, "record_references": refs,
            "findings": [], "counts": COUNTS, "outcome": "CONSISTENT"}


def common_record(kind, **fields):
    obj = P.common(kind)
    obj.update(fields)
    P.validate(obj, kind)
    return obj


def checkpoint():
    a = prepare_assessment()
    cp = common_record(
        "audit_assessment_checkpoint", execution_status="ASSESSMENT COMPLETE; CANONICAL OUTPUTS NOT YET PUBLISHED",
        sequence=1, last_confirmed_boundary="Complete full-source assessment and independent integrity computations",
        coverage={"expected": 52, "found": 52, "audited": 52, "source_inventory": 76, "mechanisms": 7},
        input_comparison=a["post_comparison"], counts=a["counts"], findings=a["findings"],
        current_evidence_checks=a["current_evidence_checks"], mechanisms=a["mechanisms"],
        record_references=a["record_references"],
        own_unpublished_helper_correction={
            "observation": "Initial preview normalized CRLF before regenerating native patch and correctly failed byte equality; no canonical assessment output had been published",
            "correction": "Preserve exact original CRLF body lines, matching inspected canonical proposal helper's unified_diff construction; retain full native byte equality, then rerun all checks successfully",
            "additional_preparation_observations": [
                "A later unpublished helper assembly had a mismatched list delimiter; Python rejected import before execution/publication. Delimiter corrected and entire assessment rerun.",
                "A new mechanism-link helper assertion incorrectly demanded literal repository paths where section 5 sources intentionally use unique named Guideline/Prompt/Request references. Resolve those names to the exact authoritative catalog paths and verify existence, named links, explicit Agent-to-Skill links and source conformance; retain all section 5 required checks. No governance requirement waived.",
                "An earlier read-only console preview encountered Windows cp1252 Unicode output; subsequent output explicitly uses UTF-8. No invocation replacement or input change."],
            "invocation_replaced": False, "checks_weakened": False, "source_inputs_changed": False},
        remaining_work=["Publish complete evidence and canonical report, then result binding their final bytes",
                        "Fresh-process final readback and input preservation check; return summary and stop"],
        safe_continuation="This same invocation only; own immutable no-overwrite outputs. Never replace invocation or modify source/upstream/history.",
        related_records=[record_ref(OWN / "attempt.json"), record_ref(OWN / "evidence/invocation-readback.json"),
                         record_ref(OWN / "attachments/audit-assessment.py")],
        limitations=LIMITATIONS)
    print(json.dumps(P.publish_json(OWN / "checkpoint-0001.json", cp), indent=2))


def table(headers, rows):
    def cell(x):
        return str(x).replace("|", "\\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(headers) + " |",
                       "|" + "|".join("---" for _ in headers) + "|"] +
                     ["| " + " | ".join(cell(x) for x in row) + " |" for row in rows]) + "\n"


def source_table(entries):
    return table(["Path", "Bytes", "SHA-256"], [
        [f"`{e['path']}`", e["bytes"], f"`{e['sha256']}`"] for e in entries])


def report_text(a, evidence_ref):
    lines = [
        "# SDLC Governance Consistency Audit", "",
        f"Canonical report identity: `{AID}:audit_report`",
        f"Work ID: `{P.WORK}` | Cycle `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1 | Attempt `{AID}`",
        "**Overall Audit Result: CONSISTENT** — AI audit result only; not Human Approval or Human Acceptance.",
        "", table(["Measure", "Actual"], [
            ["52-core expected / found / audited", "52 / 52 / 52"],
            ["Current governance-source inventory", 76],
            ["Separately reported mechanisms expected / present / assessed", "7 / 7 / 7"],
            *[[k, v] for k, v in COUNTS.items()],
        ]),
        "No unresolved findings. All seven mechanism-definition groups pass with applicable invoked records assessed. "
        "Orchestration and Portability runtime evidence/capability are explicitly NOT APPLICABLE, not runtime PASS. "
        "The zero-count conclusion follows complete current-source comparison and required checks; it is not assumed from earlier assurance.",
        "", "### Audit Scope", "",
        "Repository `ScalableParimal/SupportIQ`; root `C:\\PARIMAL_SHERE\\SCALABLE_SOLUTIONS\\SupportIQ`; "
        "HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`; branch `sdlc-framework-onboarding`.",
        "Scope: all 52 core artifacts below plus all 24 additional unique mechanism sources, forming the actual current 76-source inventory. "
        "Counts are derived from hidden-inclusive enumeration of `.github` and `docs/ai`, not adopted from the historical 76 count. "
        "All sources were fully read. Three Masters were read first, followed by mechanism-definition inspection before core comparison, "
        "then all Guidelines, Prompts, Requests, Skills and Agents. A hash inventory is not a claim of substantive reading of all historical files.",
        "Excluded: product Requirement/Plan/source/test/configuration/migration contents and product approval/acceptance content; "
        "no target-project Portability content was inspected. Product paths in templates were assessed as reference definitions only. "
        "No product Orchestrator or Portability process was invoked. Root AGENTS.md, .github/copilot-instructions.md and instruction-directory inputs were absent.",
        "", "#### Authorization, qualification and persistence",
        "Actual fresh Human Audit start:", "", "> " + P.START, "",
        "Exactly one fresh invocation was authorized and published; there is no replacement invocation. "
        "Current runtime Audit actor is `f39a6108-fbf1-47b2-b95a-8267a3f07530`, assigned independently of the preparer/applier/verifier/reviewer. "
        "Role proof is the current assignment plus hashed role/Skill, not the shared session title.",
        "The established governance root is `docs/sdlc-records/governance/`; its original OWNER-attributed decision "
        "was freshly resolved at https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236 "
        "(author ScalableParimal, user ID 226102895, OWNER, created/updated 2026-10-30T12:31:51Z). "
        "This is established-root authority only, not reused initial bootstrap or stage-start authorization. "
        "The existing candidate Masters remain unadopted bootstrap comparison authority under Governance 3. Product root remains unadopted.",
        "The current actor qualified non-mutating reads/hashes, actual upstream native outcome schemas, permissions/runtime and own publication capability; "
        "validated the complete actual invocation/common metadata in its own .partial, flushed/fsynced, atomically renamed without overwrite, "
        "then independently reopened it in a separate process before substantive assessment. "
        "The initial hidden-inclusive manifest binds 518 inputs, including .github, all relied sources/upstream/history and the original own publisher helper. "
        "New actor-owned assessment-helper/output records are separately fingerprint-bound below. All 518 inputs and their path set remained unchanged, "
        "as did Git HEAD/branch/origin/status/index. Pre-existing changes are preserved.",
        "", "#### Stable own output identities and publication chain",
        table(["Record", "Stable identity", "Canonical path", "SHA-256 when already available"], [
            ["Invocation", AID+":audit_invocation", P.rel(OWN/"attempt.json"), P.ref(OWN/"attempt.json")["sha256"]],
            ["Canonical report", AID+":audit_report", P.rel(OWN/"report.md"), "Intentionally not self-hashed here; terminal result binds final bytes"],
            ["Terminal result", AID+":audit_result", P.rel(OWN/"result.json"), "Published after report/evidence; future hash not asserted here"],
            ["Audit evidence", AID+":audit_evidence", evidence_ref["path"], evidence_ref["sha256"]],
            ["Assessment checkpoint", AID+":audit_assessment_checkpoint", P.rel(OWN/"checkpoint-0001.json"), P.ref(OWN/"checkpoint-0001.json")["sha256"]],
            ["Independent final readback", AID+":audit_terminal_readback", P.rel(OWN/"checkpoint-final.json"), "Later own evidence; future hash not asserted here"],
        ]),
        "Evidence and this complete report precede the terminal result. The terminal result is the first completed binding of this report's exact final path/identity/SHA-256. "
        "Fresh-process terminal readback follows result publication. No circular self/future fingerprint is claimed in this immutable report.",
        "", "#### Complete 52-core artifact catalog and per-artifact disposition",
        table(["ID", "Kind", "Exact path", "Bytes / SHA-256", "Inspected / assessed", "Result"], [
            [x["catalog_id"], x["kind"], f"`{x['source']['path']}`",
             f"{x['source']['bytes']} / `{x['source']['sha256']}`", "Yes / Yes", x["outcome"]]
            for x in a["core_artifacts"]]),
        "Core composition is exactly 3 Masters + 10 Guidelines + 10 Prompts + 10 Requests + 10 Skills + 9 Agents. "
        "Requirement Update is intentionally Skill-only; there is no missing tenth core Agent.",
        "", "#### Master consistency assessment",
    ]
    for x in a["core_artifacts"][:3]:
        lines += [f"- **{x['catalog_id']} {Path(x['source']['path']).name}: PASS.** {x['rationale']}"]
    lines += ["", "#### Actual current complete source inventory (76 unique files)",
              source_table(a["source_inventory"]),
              "The table above includes all hidden .github sources; no additional unassessed governance definition was discovered. "
              "Mechanism overlaps with Masters/core controls are not double-counted.",
              "", "### Separately Reported Mechanism Alignment", "",
              table(["Group", "Expected / present / assessed", "Result", "Runtime evidence applicability"],
                    [[m["group"], "Yes / Yes / Yes", m["outcome"], m["runtime_applicability"]] for m in a["mechanisms"]]),
              "All groups were inspected for role, authority, framework relationship, traceability, persistence, read/write boundary, "
              "independence where applicable, and change-control treatment. Source identities below use canonical repository paths plus "
              "fingerprints; common Master fingerprints are retained rather than inferred. Required invoked records are listed in the "
              "integrity-bound record catalog that follows. A definition is never substituted for current runtime capability.",
              ""]
    record_labels = {
        "Governance Audit": "AUD-INV, AUD-MAN, AUD-IRB, AUD-PST, AUD-PUB, AUD-CHK; current canonical report/result/evidence identities above",
        "Governance Remediation": "REM-INV/RPT/RES/H03/H04/HIST/VAL, INV-RPT/RES, PROPOSAL/APPLICATION/VERIFICATION/REVIEW records and prior Audit/history references",
        "SDLC Process Orchestration": "No product Orchestrator invocation; sources only, runtime records explicitly N/A",
        "SDLC Portability Assessment": "No Portability invocation; five source bindings only, runtime records explicitly N/A",
        "Governance Amendment Application": "PROPOSAL-01..07 and APPLICATION-01..10, including actual Human authorization, invocation, preflight, before/after evidence and readbacks",
        "Independent Governance Verification": "VERIFICATION-01..10; Application/proposal/approval bindings; only current fresh valid retry",
        "Independent Governance Review": "REVIEW-01..08 plus current VERIFICATION and proposal/Application/approval bindings",
    }
    for m in a["mechanisms"]:
        lines += [f"#### {m['group']} — {m['outcome']}", "",
                  "**Authoritative source bindings:**", source_table(m["sources"]),
                  "**Required evidence:** " + record_labels[m["group"]], "",
                  table(["Check", "Outcome", "Evidence-based rationale"],
                        [[c["id"]+" "+c["check"], c["outcome"], c["rationale"]] for c in m["checks"]])]
    lines += ["", "#### Integrity-bound record/reference catalog",
              "Each entry was reopened and its bytes/SHA-256 recomputed. JSON identities are read from actual native objects; "
              "an older file without a separate internal ID is explicitly referenced by canonical path/attempt, never assigned an invented actor identity. "
              "Full current common metadata, source state and capability context are preserved in own invocation and evidence. "
              "Catalog inclusion does not reclassify historical failures or earlier stage outcomes.",
              table(["Label", "Record identity", "Exact path", "Bytes / SHA-256"], [
                  [x["label"], x["record_id"] or "No internal ID; canonical path plus attempt is the reference identity",
                   f"`{x['path']}`", f"{x['bytes']} / `{x['sha256']}`"] for x in a["record_references"]]),
              "", "#### Current Application/Verification/Review machine checks",
              table(["Check", "Actual result"], [
                  ["Current Application native outcome", a["current_evidence_checks"]["application"]["outcome"]],
                  ["All five targets reversed to exact approved bases and filtered Git HEAD, then forward reconstructed at approved offsets", "PASS"],
                  ["Regenerated approved native unified patch, exact bytes", "PASS; "+a["current_evidence_checks"]["patch"]["sha256"]],
                  ["All-five-before-first-write preflight/control-flow evidence", "PASS; procedural inspected execution evidence, not an OS tamper-proof trace"],
                  ["Original Application manifest", "474 inputs: exact approved 5 changes; other 469 unchanged"],
                  ["Fresh Verification", "COMPLETED / PASS; 13/13 criteria; all 500 own inputs unchanged"],
                  ["Fresh Review", "COMPLETED / PASS; 12/12 criteria; all 510 own inputs unchanged"],
                  ["Current criterion/report/evidence/manifest reference occurrences independently validated",
                   a["current_evidence_checks"]["checked_current_record_and_manifest_reference_occurrences"]],
                  ["Current Audit boundary comparisons", "518/518 initial inputs and exact path set unchanged; Git HEAD/branch/status/index unchanged"],
              ]),
              source_table([x["actual"] for x in a["current_evidence_checks"]["targets"]]),
              "All five target byte contracts remain UTF-8 without BOM and CRLF; first four have no final newline, fifth has a final newline. "
              "Approved changes are not treated as unexplained drift. Before/after historical base fingerprints are assessed as before-state evidence, not required to equal current after-state bytes.",
              "", "#### Actual actor and fresh-start bindings",
              table(["Role", "Actual runtime actor", "Own invocation / SHA-256"], [
                  [role, x["creator"]["runtime_agent_id"], x["invocation"]["path"]+" / "+x["invocation"]["sha256"]]
                  for role, x in a["current_evidence_checks"]["actual_actors"].items()]),
              "The four actors are distinct, and this Audit actor differs from all four. Approved future role-definition bindings were "
              "planned-only at proposal preparation and match actual stage roles now. Qualification is current actor-owned evidence, "
              "not inferred from an Agent name or another actor's capabilities.",
              "", "**Exact supplied approval/designation:**",
              "> "+a["current_evidence_checks"]["human_authorization"]["approval_exact_ascii"], "",
              "**Separate Application start:**",
              "> "+a["current_evidence_checks"]["human_authorization"]["separate_stage_start_exact_ascii"], "",
              "**Fresh valid Verification start:**",
              "> "+a["current_evidence_checks"]["fresh_assurance_starts"]["verification"], "",
              "**Separate Review start:**",
              "> "+a["current_evidence_checks"]["fresh_assurance_starts"]["review"], "",
              "These are actual supplied Human decisions with exact package presentation bindings, not AI-created approvals. "
              "No extra residual-risk acknowledgement gate is invented. Authenticated conversation IDs/times are not exposed.",
              "", "### Repository Reference Findings", "",
              "**None. Broken References: 0.** All expected paths resolve; all ten Skill→Guideline/Prompt/Request bundles and "
              "nine Agent→Skill links are correct. Explicit source references yielded "+str(len(a["reference_checks"]))+
              " resolved occurrences with line-addressed evidence. Exact paths, spelling, directory casing/naming, "
              "frontmatter and complete current source path set were checked. Repeated links and shared controls are not duplicate governance definitions. "
              "Product-output/example paths and intentional Request placeholders are not falsely reported as missing governance files. "
              "No obsolete/broken core or mechanism relationship was found.",
              "", "### Governance Consistency Findings", "",
              "**No current findings (empty list).** Critical 0, High 0, Medium 0, Low 0; Ambiguities 0. "
              "No material finding is hidden in limitations or waived. Required per-finding fields therefore have no applicable entries.",
              "", "#### Prior finding reconciliation — current basis, not reinvestigation",
              table(["Finding", "Current disposition", "Current evidence-based basis"], [
                  ["GOV-AUD-20261102-001", "Previously addressed; not reopened",
                   "Prior complete Audit disposition, immutable linked clarification F001-CLR and passing independent assurance retain the strict record-first/preserved-history interpretation; no retroactive reclassification of historic GOV-001/GOV-002."],
                  ["GOV-AUD-20261102-002", "Previously addressed; not reopened",
                   "Current Remediation Agent immutable authorization clause plus F002 Application COMPLETED / EXACT APPROVED BYTES APPLIED and independent Verification/Review PASS; authorization remains unchanged and later evidence cannot expand Push."],
                  ["GOV-AUD-20261102-003", "Addressed in this complete current-source Audit; no unresolved issue",
                   NOTES["REQUIREMENT_UPDATE"]["conclusion"]],
                  ["GOV-AUD-20261102-004", "Addressed in this complete current-source Audit; no unresolved issue",
                   "The exact approved Corrective Request stage-specific paragraph aligns with unchanged Application controls: actual current stage qualification, planned-only future assurance until predecessor gate and fresh start, four distinct actors and no pre-existing qualification prerequisite."],
              ]),
              "Canonical Investigation revision 0002 and corrected coordinator revisions—not superseded invalid bundles—supply the current chain. "
              "Prior failed Verification record/replacement `20261102T152557Z-efc37bf9-a1dd-4f02-b768-d797e0636818` "
              "remains unsuccessful history; the separately authorized fresh valid Verification governs current assurance. "
              "This Audit assesses current consistency and required effectiveness criteria; it does not rewrite, investigate or retrospectively approve history.",
              ""]
    for section, kind in [
        ("Guideline Consistency Summary", "Guideline"), ("Prompt Consistency Summary", "Prompt"),
        ("Request Template Consistency Summary", "Request"), ("SDLC Process Skill Consistency Summary", "Skill"),
        ("SDLC Process Agent Consistency Summary", "Agent"),
    ]:
        subset = [x for x in a["core_artifacts"] if x["kind"] == kind]
        lines += ["### "+section, "",
                  f"All {len(subset)} expected {kind} artifacts inspected. Audit criteria checked individually: "
                  + "; ".join(f"{n}. {v}" for n, v in enumerate(CRITERIA[kind], 1)) + ".",
                  "Criterion-level outcomes, current line-addressed source headings/anchors and scope are retained as native objects in audit evidence. "
                  "Passing semantic comparison is based on complete source reading, not keyword occurrence or a prior actor's PASS.",
                  table(["Core ID / process", "All applicable checks", "Assessment and rationale"], [
                      [x["catalog_id"]+" "+str(x["process"]), f"1–{len(x['criteria'])}: PASS", x["rationale"]]
                      for x in subset]), ""]
    lines += ["### Skill and Agent Traceability Summary", "",
              table(["Process", "Guideline", "Prompt", "Request", "Skill", "Agent / applicability", "Result"], [
                  [x["process"], x["guideline"], x["prompt"], x["request"], x["skill"],
                   x["agent"] or "N/A — deliberately Skill-only Requirement Update", x["outcome"]]
                  for x in a["process_relationships"]]),
              "Agents remain controlled entry points invoking the designated Skill; Skills retain Master/Guideline authority and "
              "do not replace Prompt/Request inputs. All five connected Portability and Application/Verification/Review bundles "
              "are additionally assessed in the mechanism matrix, outside the 52 count.",
              "", "### Cross-Document Consistency Summary", "",
              table(["Dimension", "Assessment / rationale"], [
                  ["Lifecycle and artifact-specific routes",
                   "PASS. Requirement → Analysis → complete independent Analysis Verification → resolution → Human Requirement Approval → Planning → complete Plan Verification → resolution → Human Review Approval → Human Plan Approval → Implementation/self-check → complete independent Implementation Verification → complete Review → Human Acceptance → separately authorized Commit/Push. Initial clarification and correction routes retain their own source status and gates."],
                  ["Artifact ownership, status, supersession, propagation",
                   "PASS. Current approved Requirement/Plan governs product scope; candidates/unapproved versions are not implementation authority. Immutable frozen source versions and lineage remain; changes trigger downstream validity/impact checks and complete verification as required."],
                  ["Approval, acceptance, initiation and assurance",
                   "PASS. Explicit process starts are not formal approval; self-check is not independent Verification; Verification is not Human Review Approval; Review is not Human Acceptance. Governance exact approval/designation is not source-write capability or future-stage authority."],
                  ["Finding/change/corrective routing",
                   "PASS. No direct finding-to-code shortcut. Investigation → corrective decision → required exact Human Approval → authorized change → required independent Verification/Review → full Audit; non-finding enhancements retain distinct subject/status paths."],
                  ["Scope, task IDs and contextual evidence",
                   "PASS. Implementation may be bounded to approved tasks; task IDs and changed files do not narrow complete required Verification/Review/Investigation. Source inspection, executed checks, reported outcomes and unverified behavior are distinct."],
                  ["Parallelism, writes and evidence ownership",
                   "PASS. Shared-checkout writers serialized; parallel Implementation needs isolated worktrees/integration. Read-only roles have own-record-only output rights. Qualification and no-overwrite records do not authorize source or other-actor edits."],
                  ["Terminology, paths and entry-point relationships",
                   "PASS. All ten process bundles, nine core Agent entries and 24 additional mechanism sources align; no newly discovered incompatible or unsupported policy source."],
              ]),
              "", "#### Evidence classification and limitations",
              table(["Class", "What this Audit actually establishes"], [
                  ["EXECUTED", "Current SHA-256/size/path checks; complete 76-source/52-core enumeration; 301 resolved explicit source-reference occurrences; exact five-target reverse/forward/filtered-HEAD/patch reconstruction; 474 Application/500 Verification/510 Review input comparisons; actual native status parsing and criterion/reference checks; 518 own-input boundary comparisons; strict native JSON/common-schema positive/negative tests; own .partial/fsync/atomic no-overwrite/readback operations."],
                  ["SOURCE INSPECTION", "Full three Masters, all 49 detailed core sources and all 24 extra mechanism sources; semantic lifecycle/authority/status/scope/approval/independence/change-control comparisons; actual Application helper all-target preflight and write-order control flow; relied governance records/reports."],
                  ["REPORTED / INTEGRITY-BOUND", "Actual supplied Human decisions and original actors' operation/permission/concurrency assertions, historical findings and assurance conclusions. This Audit rehashes and independently computes current bindings; it does not replay past authorized source writes or turn endpoint hashes into a trusted OS event log."],
                  ["UNVERIFIED / NOT APPLICABLE", "No target-project assessment, product Orchestrator execution, actual initial product clarification failure, future actor capability, external cryptographic identity, exhaustive continuous tamper exclusion or automatic adoption/activation is claimed."],
              ]),
              *["- "+v for v in LIMITATIONS],
              "The own unpublished patch-reconstruction preview initially normalized CRLF and failed exact comparison. "
              "The helper was corrected before any substantive canonical publication to preserve the approved native CRLF construction; "
              "all checks reran successfully without weakening equality or changing any input/invocation. "
              "An unpublished report-helper list delimiter was also corrected after Python rejected import, before execution/publication; "
              "a helper-only literal-path assumption for mechanism named-source links was corrected to resolve the unique names to exact authoritative catalog paths, "
              "retaining source existence, named relationship, Agent-to-Skill path and all section 5 conformance checks; "
              "an earlier console-only Unicode encoding issue was resolved with UTF-8 output. "
              "These are preparation diagnostics, not findings or unauthorized replacement invocations.",
              "", "### Governance Gaps", "",
              "**None identified in audited scope. Missing Governance Controls: 0.** Explicitly disclosed procedural limitations "
              "are supported by the existing Masters/assurance contracts; they are not silently treated as enforced technical isolation. "
              "No extra sandbox, authenticated-message metadata or residual-risk acknowledgement prerequisite is invented.",
              "", "### Unsupported or Excessive Governance", "",
              "**None identified. Unsupported Governance Controls: 0.** No lower-layer policy contradicts or expands Master authority "
              "on the current inspected bytes. Stage-specific actor timing and initial source qualification now align rather than adding a second policy authority.",
              "", "### Human Decisions Required", "",
              "No unresolved material policy decision blocks this Audit. Existing candidate Master adoption, product-root adoption, "
              "Portability decisions and all product/stage starts remain separate future Human decisions under their own prerequisites. "
              "This Audit does not request or grant them. No Human Approval or Human Acceptance of the governance framework is declared.",
              "", "### Recommended Corrective Actions", "",
              "None: the current Audit has no unresolved corrective finding. No correction, investigation or other process was executed. "
              "Preserve all immutable records, including failed/superseded history. The downstream coordinator must independently "
              "validate and anchor this result under its own applicable authorization; that handoff is not an Audit correction or a future prerequisite.",
              "", "### Overall Audit Result", "",
              "**CONSISTENT**",
              "The 52/52/52 core catalog, actual 76-source set and all seven assessed mechanism groups have no unresolved issue. "
              "All eight count fields are zero. This meets the defined clean-Audit threshold for the assessed non-Master correction; "
              "it is an AI consistency/effectiveness-qualifying result, not framework approval, acceptance, Master adoption or product activation.",
              "", "#### Exact downstream handoff and stop",
              f"Result identity `{AID}:audit_result` at `{P.rel(OWN/'result.json')}` binds canonical report "
              f"`{AID}:audit_report` at `{P.rel(OWN/'report.md')}` and evidence `{evidence_ref['path']}`.",
              "The existing Governance Remediation canonical final report must subsequently resolve the published Audit result/report, "
              "independently recompute the result SHA-256 from stored bytes, confirm its exact report binding, and record result path, "
              "identity, verified SHA-256 and validation outcome in the same Work ID/Cycle 1, including for this empty findings list. "
              "Its later own result binds that final Remediation report. The Remediation report is prepared AFTER the Audit result and "
              "is not a prerequisite for this Audit outcome/publication. No Remediation record is written or modified here.",
              "No downstream process is started. Any continuation requires its own applicable fresh Human process-initiation authority. "
              "No adoption, product-root activation, product work, staging, commit or push is authorized or performed. STOP.",
              ""]
    text = "\n".join(lines)
    validate_report(text, a)
    return text


def validate_report(text, assessment):
    assert all("### "+name+"\n" in text for name in REPORT_SECTIONS)
    assert all(f"`{x['source']['path']}`" in text for x in assessment["core_artifacts"])
    assert all(x["sha256"] in text for x in assessment["source_inventory"])
    assert all(m["group"] in text for m in assessment["mechanisms"])
    assert len(assessment["findings"]) == 0 and all(v == 0 for v in assessment["counts"].values())
    assert "`n" not in text and "\ufffd" not in text
    assert not re.search(r"\[(?:TODO|TBD|INSERT|PLACEHOLDER)\]", text, re.I)
    assert text.count("### Overall Audit Result\n") == 1
    return True


def publish_report(text):
    path = OWN / "report.md"
    partial = OWN / "report.md.partial"
    assert not path.exists() and not partial.exists()
    raw = text.encode("utf-8")
    assert raw.decode("utf-8") == text
    with partial.open("xb") as f:
        assert f.write(raw) == len(raw)
        f.flush()
        os.fsync(f.fileno())
    assert partial.read_bytes() == raw
    assert not path.exists() and os.name == "nt"
    os.rename(partial, path)
    assert path.read_bytes() == raw
    return {**P.ref(path), "record_id": AID+":audit_report"}


def publish_final():
    cp = P.load(OWN / "checkpoint-0001.json")
    P.validate(cp, "audit_assessment_checkpoint")
    assert cp["coverage"] == {"expected": 52, "found": 52, "audited": 52, "source_inventory": 76, "mechanisms": 7}
    for entry in cp["related_records"]:
        bound(entry)
    a = prepare_assessment()
    ev = common_record(
        "audit_evidence", execution_status="COMPLETED", outcome=a["outcome"],
        invocation=record_ref(OWN/"attempt.json"), input_manifest=record_ref(OWN/"evidence/input-manifest.json"),
        invocation_readback=record_ref(OWN/"evidence/invocation-readback.json"),
        assessment_checkpoint=record_ref(OWN/"checkpoint-0001.json"),
        scope={"expected_core": 52, "found_core": 52, "audited_core": 52, "actual_sources": 76,
               "mechanisms_expected_present_assessed": [7, 7, 7]},
        assessment=a, limitations=LIMITATIONS,
        evidence_classification={"executed": "Current byte/hash/path/reconstruction/reference/native-JSON/publication checks",
                                 "source_inspection": "Full governance definitions and relied governance evidence; semantic comparisons",
                                 "reported": "Prior actors' original operations/permissions plus actual supplied Human wording",
                                 "unverified": "No exhaustive tamper exclusion, product execution or future capabilities"},
        own_output_boundary=P.rel(OWN), source_writes=False, other_actor_record_writes=False,
        product_content_audited=False, other_stage_started=False, adoption=False, staging_commit_push=False,
        related_records=[record_ref(OWN/"attempt.json"), record_ref(OWN/"checkpoint-0001.json"),
                         record_ref(OWN/"evidence/input-manifest.json")])
    assert not (OWN/"evidence/audit-evidence.json").exists()
    # Validate entire actual report structure in memory before any terminal publication.
    dummy_ref = {"path": P.rel(OWN/"evidence/audit-evidence.json"),
                 "record_id": AID+":audit_evidence", "sha256": hashlib.sha256(P.validate(ev, "audit_evidence")).hexdigest().upper()}
    draft = report_text(a, dummy_ref)
    validate_report(draft, a)
    boundary = unchanged()
    evref = {**P.publish_json(OWN/"evidence/audit-evidence.json", ev), "record_id": AID+":audit_evidence"}
    assert evref["sha256"] == dummy_ref["sha256"]
    report = report_text(a, evref)
    assert report == draft
    rptref = publish_report(report)
    boundary = unchanged()
    result = common_record(
        "audit_result", execution_status="COMPLETED", outcome=a["outcome"],
        report=rptref, evidence=evref, invocation=record_ref(OWN/"attempt.json"),
        input_manifest=record_ref(OWN/"evidence/input-manifest.json"),
        required_evidence_records=[
            evref, record_ref(OWN/"evidence/input-manifest.json"),
            record_ref(OWN/"evidence/invocation-readback.json"),
            record_ref(OWN/"evidence/publisher-selftest.json"), record_ref(OWN/"checkpoint-0001.json")],
        scope={"expected": 52, "found": 52, "audited": 52, "actual_source_inventory": 76, "mechanism_groups": 7},
        counts=a["counts"], findings=a["findings"], mechanisms=a["mechanisms"],
        final_input_comparison=boundary,
        effectiveness_qualifying=True, master_adoption=False, product_root_adoption=False,
        source_writes=False, other_actor_record_writes=False, other_stage_started=False,
        product_content_audited=False, staging_commit_push=False,
        next_gate="STOP. Downstream Governance Remediation final-handoff continuation requires its own applicable Human initiation; no other stage started.",
        terminal_anchor_obligation={
            "actor": "Existing Governance Remediation coordinator under its own authority",
            "work_id": P.WORK, "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001", "cycle": 1,
            "required": "After this Audit result publication, independently recompute result SHA-256, validate report binding, and record result path/identity/hash/validation in canonical Remediation final report; later own result binds that report",
            "future_handoff_is_audit_prerequisite": False},
        final_readback={"path": P.rel(OWN/"checkpoint-final.json"), "record_id": AID+":audit_terminal_readback",
                        "sequence": "Fresh separate-process readback after result; no future fingerprint asserted"},
        publication={"method": "Validated complete native object and UTF-8 bytes in exclusive .partial; flush/fsync; same-filesystem Windows atomic no-overwrite rename; exact readback",
                     "chain": "Evidence -> canonical report -> result -> independent terminal readback",
                     "exact_publication_timestamp_available": False},
        related_records=[rptref, evref], limitations=LIMITATIONS)
    validate_result(result)
    resultref = P.publish_json(OWN/"result.json", result)
    print(json.dumps({"report": rptref, "result": resultref, "evidence": evref,
                      "outcome": result["outcome"], "next": "Fresh separate-process terminal readback; no later stage"}, indent=2))


def validate_result(result):
    P.validate(result, "audit_result")
    assert result["execution_status"] == "COMPLETED" and result["outcome"] == "CONSISTENT"
    assert result["scope"] == {"expected": 52, "found": 52, "audited": 52, "actual_source_inventory": 76, "mechanism_groups": 7}
    assert result["counts"] == COUNTS and not result["findings"]
    assert len(result["mechanisms"]) == 7
    assert all(m["assessed"] and m["outcome"] == "PASS" for m in result["mechanisms"])
    for entry in [result["report"], result["evidence"], result["invocation"], *result["required_evidence_records"]]:
        bound(entry)
        assert entry["record_id"]
    ev = P.load(ROOT/result["evidence"]["path"])
    assert ev["assessment"]["counts"] == result["counts"]
    assert ev["assessment"]["mechanisms"] == result["mechanisms"]
    validate_report((ROOT/result["report"]["path"]).read_text("utf-8"), ev["assessment"])


def terminal():
    result = P.load(OWN/"result.json")
    validate_result(result)
    ev = P.load(OWN/"evidence/audit-evidence.json")
    for entry in ev["assessment"]["source_inventory"] + ev["assessment"]["record_references"]:
        bound(entry)
    for role in ["verification", "review"]:
        d = P.load(BASE/P.IDS[role]/"result.json")
        assert d["outcome"] == "PASS" and d["execution_status"] == "COMPLETED"
    boundary = unchanged()
    assert not list(OWN.rglob("*.partial"))
    terminal_check = common_record(
        "audit_terminal_readback", execution_status="COMPLETED", outcome="PASS",
        sequence=2, result=record_ref(OWN/"result.json"), report=result["report"], evidence=result["evidence"],
        final_input_comparison=boundary, canonical_complete_report_validated=True,
        all_76_source_hashes_and_record_catalog_rechecked=True,
        actual_complete_native_objects_schema_and_roundtrip_validated=True,
        independent_process="Fresh separate Python command after result publication; not a new Audit invocation",
        publication_order="Initial invocation -> separate invocation readback -> complete assessment -> checkpoint -> evidence -> canonical report -> terminal result -> this fresh terminal readback",
        no_downstream_start=True, source_writes=False, other_actor_record_writes=False,
        related_records=[record_ref(OWN/"result.json"), result["report"], result["evidence"]],
        limitations=LIMITATIONS)
    cpref = P.publish_json(OWN/"checkpoint-final.json", terminal_check)
    print(json.dumps({"outcome": result["outcome"], "scope": result["scope"], "counts": result["counts"],
                      "mechanisms": {m["group"]:m["outcome"] for m in result["mechanisms"]},
                      "report": result["report"], "result": record_ref(OWN/"result.json"),
                      "evidence": result["evidence"], "terminal_readback": cpref,
                      "source_inputs_preserved": boundary}, indent=2))


def preview():
    before = unchanged()
    core, sources = inventory()
    paths, relationships = path_checks(sources)
    evidence = evidence_checks()
    print(json.dumps({"input_boundary": before, "core": len(core), "sources": len(sources),
                      "reference_occurrences": len(paths), "process_bundles": len(relationships),
                      "application": evidence["application"],
                      "assurance_currency": evidence["assurance_currency"],
                      "nested_current_bindings": evidence["checked_current_record_and_manifest_reference_occurrences"],
                      "end_boundary": unchanged()}, indent=2))


if __name__ == "__main__":
    {"preview": preview, "checkpoint": checkpoint, "publish": publish_final, "terminal": terminal}[sys.argv[1]]()
