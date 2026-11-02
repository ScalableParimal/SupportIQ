"""Proposal preparation only. Never writes the evaluated target."""
import difflib
import hashlib
import json
from pathlib import Path
import runpy

H = runpy.run_path(str(Path(__file__).with_name("publication-tools.py")))
ROOT, BASE, WORK, ATTEMPT = [H[k] for k in ("ROOT", "BASE", "WORK", "ATTEMPT")]
ref, publish, common, cmd = [H[k] for k in ("ref", "publish", "common", "cmd")]
inv = json.loads((BASE / "attempt.json").read_bytes())

def unchanged():
    for r in inv["baseline"]:
        assert ref(r["path"]) == r, r["path"]
    actual = {p.relative_to(ROOT).as_posix()
              for top in [ROOT / "docs", ROOT / ".github", ROOT / "README.md"]
              for p in ([top] if top.is_file() else top.rglob("*"))
              if p.is_file() and not p.is_relative_to(BASE)}
    assert actual == {r["path"] for r in inv["baseline"]}, "external path-set drift"
    assert cmd("git", "rev-parse", "HEAD") == inv["repository"]["head"]
    assert cmd("git", "branch", "--show-current") == inv["repository"]["branch"]
    assert cmd("git", "status", "--short") == inv["repository"]["status"]
    return {"baseline_records": len(inv["baseline"]), "content_and_path_sets": "UNCHANGED",
            "head_branch_status": "UNCHANGED", "exclusion": BASE.relative_to(ROOT).as_posix(),
            "limits": "Endpoint comparison, not proof against transient writes or same-principal tampering"}

bindings = []
def validate_tree(obj, loc="$"):
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            r = ref(obj["path"])
            assert r["sha256"] == obj["sha256"].upper(), (loc, obj["path"])
            if "bytes" in obj:
                assert r["bytes"] == obj["bytes"], (loc, obj["path"])
            bindings.append({"location": loc, "binding": r})
        for k, v in obj.items():
            validate_tree(v, loc + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            validate_tree(v, loc + "[" + str(i) + "]")

unchanged()
for r in inv["inputs"]:
    if r["path"].endswith("result.json"):
        validate_tree(json.loads((ROOT / r["path"]).read_bytes()), r["path"])
investigation = json.loads((BASE.parent / "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/result.json").read_bytes())
assert investigation["execution_status"] == "COMPLETED"
assert investigation["outcome"] == "CORRECTIVE DIRECTION IDENTIFIED"
assert investigation["finding_confirmed"] is True
prior_names = ["20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd",
               "20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1",
               "20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb"]
prior_art = []
for name in prior_names:
    p = BASE.parent / name / "result.json"
    o = json.loads(p.read_bytes())
    # Historical result inputs are not re-performed or promoted to current authority.
    for key in ["report", "evidence"]:
        if key in o:
            validate_tree(o[key], name + "." + key)
    prior_art.append({"result": ref(p), "reported_outcome": o.get("outcome"),
                      "classification": "Reported historical conclusion; current stored output bindings checked, stage not re-executed"})
payload = BASE.parent / prior_names[0] / "attachments/GOV-AUD-20261102-001-linked-clarification.md"
assert ref(payload)["bytes"] == 3438
prior_art.append({"payload": ref(payload), "purpose": "Existing linked immutable clarification precedent, no transferred approval"})

target = ".github/agents/sdlc-governance-remediation.agent.md"
before_bytes = (ROOT / target).read_bytes()
assert ref(target)["sha256"] == "EBFE9E9A369F2FA367F7A4728893106338DBDB6245A2016E2A248E7228148153"
text = before_bytes.decode("utf-8")
before = next(line for line in text.splitlines() if line.startswith("2. **Commit/Push Authorization (YES/NO):**"))
prefix = before.split(" After creating an authorized commit,")[0]
after = prefix + (
    " Preserve the published authorization record unchanged. After creating an authorized commit, "
    "the actor performing that authorized action must publish new immutable evidence within its own "
    "authorized attempt under the same Work ID, following section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md "
    "and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. Link the original authorization "
    "by canonical path, record ID, and SHA-256; record the full resulting commit identity and evidence "
    "that it matches the exact authorized staged diff and file list. Retain the original Work ID, "
    "scope, conditions, and permitted-action bindings. This later evidence records execution only; "
    "it does not alter or supersede the Human decision, authorize a different diff or commit, or "
    "grant or expand Push authorization. A Push is permitted only if the unchanged original "
    "authorization expressly authorizes Push, the linked evidence binds the resulting commit to "
    "that authorization and exact staged content, and the commit being pushed matches that identity. "
    "Publish this evidence after the commit; that commit need not contain its own identity or the "
    "later evidence.")
assert before_bytes.count(before.encode("utf-8")) == 1
expected = before_bytes.replace(before.encode("utf-8"), after.encode("utf-8"), 1)
assert before_bytes.count(b"\r\n") == expected.count(b"\r\n")
assert expected.replace(after.encode("utf-8"), before.encode("utf-8"), 1) == before_bytes
assert b"append the full resulting commit identity to this same authorization record" not in expected
assert prefix == after[:len(prefix)]
diff = "\n".join(difflib.unified_diff(text.splitlines(), expected.decode("utf-8").splitlines(),
                   fromfile="a/" + target, tofile="b/" + target, lineterm="")) + "\n"
role_paths = {
    "preparer": ".github/agents/corrective-change-decision.agent.md",
    "proposed_one_time_applier": ".github/agents/governance-amendment-application.agent.md",
    "planned_verifier_identity_only": ".github/agents/independent-governance-verification.agent.md",
    "planned_reviewer_identity_only": ".github/agents/independent-governance-review.agent.md",
    "excluded_orchestrator": ".github/agents/sdlc-process-orchestrator.agent.md",
    "excluded_active_remediation": target}
roles = {k: ref(v) for k, v in role_paths.items()}
assert len({r["path"] for r in roles.values()}) == len(roles)
assert len({r["sha256"] for r in roles.values()}) == len(roles)

cp = common("checkpoint")
cp.update({"sequence": 1, "invocation": ref(BASE / "attempt.json"),
    "first_readback_observation": "Separate PowerShell/Python operation after invocation publication and BEFORE substantive comparison validated 102241 bytes / SHA-256 4599570487520A7741F0528CD9A3779548269DB61867930F87243F41955BFDBF, 9 inputs and 357 baseline files. Tool operation completed successfully.",
    "last_confirmed_boundary": "Scoped source comparison and exact single-line proposal preparation completed in memory; target not written",
    "preservation": unchanged(), "unfinished_work": ["Publish exact proposal, complete report and result; independently read back"],
    "pending_gates": ["Exact Human Approval", "Fresh one-time applier designation", "Separate future stage starts"]})
cp_ref = publish("checkpoint-0001.json", cp)
patch_ref = publish("attachments/proposed.patch", diff.encode("utf-8"), raw=True)
proposal = common("governance_patch_proposal")
proposal.update({
    "status": "UNAPPROVED; NOT APPLIED",
    "target_paths": [target],
    "base": ref(target),
    "expected_after": {"path": target, "bytes": len(expected), "sha256": hashlib.sha256(expected).hexdigest().upper()},
    "encoding": "UTF-8 without BOM", "target_newline": "CRLF, preserved exactly; final newline unchanged",
    "replacement": {"occurrences_required": 1, "before": before, "after": after,
        "method": "Exact UTF-8 byte-string replacement once; no newline normalization"},
    "patch": patch_ref,
    "scope": "Section 43 Optional Post-Completion Commit item 2 only; all other target bytes unchanged",
    "exclusions": ["All other source paths", "Masters", "Historical records", "Product work", "Staging", "Commit", "Push", "Adoption"],
    "roles": roles,
    "preparer_attempt": ref(BASE / "attempt.json"),
    "application_route": "Proposed qualified one-time initial applier, subject to exact Human Approval/designation and separately fresh Application start. No standing authority inferred; old one-time designations not reusable.",
    "planned_role_limit": "Applier/verifier/reviewer bindings are proposals/identity-only, not current runtime capabilities or started attempts; future actors publish their own attempts only after predecessor gates and fresh starts.",
    "required_assurance": ["Authorized exact application", "Independent Verification PASS", "Independent Review PASS", "Complete Governance Audit CONSISTENT with all issue counts zero and all seven mechanisms assessed"],
    "master_adoption": "Not required for this non-Master amendment; target Master baseline and product root remain unadopted",
    "residual_risks": ["Procedural nonmutation, not sandbox enforced", "Endpoint hashes cannot exclude transient writes or same-principal tampering", "No exhaustive trusted event log"],
    "canonical_report": {"path": (BASE / "report.md").relative_to(ROOT).as_posix(), "identity": ATTEMPT + ":decision_report"}
})
proposal_ref = publish("attachments/proposal.json", proposal)

citations = []
for path, nums in [(target, [159, 161, 169, 1309, 1311, 1312, 1314]),
                   ("docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md", [1191])]:
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    for n in nums:
        citations.append({"artifact": ref(path), "line": n, "text": lines[n-1]})
evidence = common("decision_evidence")
evidence.update({"invocation": ref(BASE / "attempt.json"), "checkpoint": cp_ref,
    "inputs": inv["inputs"], "upstream_structured_binding_checks": bindings,
    "source_citations": citations, "prior_art": prior_art,
    "proposal": proposal_ref, "patch": patch_ref, "role_bindings": roles,
    "proposal_checks": {"single_exact_replacement": True, "unchanged_prefix": True, "all_other_bytes_retained": True,
        "encoding_crlf_retained": True, "no_target_write": True, "json_actual_object_roundtrip": True,
        "checks_scope": "Proposal preparation/integrity checks only, NOT Independent Governance Verification/Review"},
    "ordered_operations": [
        "Read current role/Skill/Guideline/Prompt/Request and applicable Master clauses",
        "Non-mutating current whoami/ACL/git/runtime checks and live GitHub adoption resolution",
        "Allocated own attempt; prepared own helper; hash-checked input set and source/record baseline",
        "Atomic no-overwrite attempt publication returned bytes/hash",
        "Separate Python process read back and checked invocation, 9 input and 357 baseline bindings BEFORE comparison",
        "Inspected Investigation, Audit finding, actual optional route, role boundaries and relevant linked precedent",
        "Prepared exact replacement in memory; checked unaffected bytes, encoding/newlines and identity distinctness",
        "Published checkpoint, exact patch and proposal under own attempt; then evidence before report/result"],
    "classification": {"executed": ["Current environment/identity checks", "Live root-decision resolution", "Hash/byte/JSON/reference validation", "Own publication/readback", "In-memory proposal integrity checks"],
        "source_inspection": ["Textual ambiguity and affected exact source", "Applicable current authority and role boundaries", "Prior immutable linked clarification text"],
        "reported": ["Audit 52-core/76-source/seven-mechanism coverage and outcome", "Investigation conclusion", "Historical Application and Verification/Review outcomes, not re-executed"],
        "unverified": ["Actual historical authorization mutation or unauthorized Commit/Push", "Authenticated Human conversation message ID/time", "Exhaustive event history", "Future actor capabilities/approval"]},
    "preservation": unchanged(), "limitations": proposal["residual_risks"],
    "human_start": inv["authorization"],
    "canonical_report": proposal["canonical_report"]})
evidence_ref = publish("attachments/evidence.json", evidence)

def table(rows):
    return "| Path | Bytes | SHA-256 |\n|---|---:|---|\n" + "\n".join(
        "| `" + r["path"] + "` | " + str(r["bytes"]) + " | `" + r["sha256"] + "` |" for r in rows) + "\n"

gate = (
    "Human decision required: approve or reject the exact proposal in this canonical report and "
    "attachments/proposal.json, binding this final report's result-bound SHA-256, proposal/patch "
    "fingerprints, the single target's base and expected-after fingerprints, scope/exclusions, "
    "and the one-time application route. If approving, explicitly designate the proposed "
    "Governance Amendment Application actor at its exact role path/SHA-256 as the one-time "
    "initial applier for this correction only, and bind the planned verifier/reviewer role "
    "paths/SHA-256 below. Approval/designation is not stage initiation. No historical designation "
    "is reused. No Application, Verification, Review or Audit starts until its separate fresh "
    "explicit Human instruction after its predecessor gates.")
report = f"""# Corrective Change Decision & Plan Update — GOV-AUD-20261102-002

Work ID: {WORK}
Cycle: GOV-REMEDIATION-PROSPECTIVE-001; Cycle 1.
Attempt: {ATTEMPT}
Canonical report identity: {ATTEMPT}:decision_report
Subject type: FINDING. Proposal only. No correction applied.

## 1. Decision Status

**FINDING ACCEPTED — OTHER GOVERNED ARTIFACT CHANGE REQUIRED.**
Acceptance here is an AI finding disposition, not Human Acceptance, patch
approval, authority to apply, or closure of the Audit finding.

## 2. Finding Summary

The current Remediation Agent section 43 Optional Post-Completion Commit
requires Human authorization before Commit/Push (line 1309), then item 2
(line 1312) says to append the resulting commit identity to that same record.
It does not distinguish an immutable published Human decision from linked
later execution evidence. A literal in-place append conflicts with Artifact
Governance section 33.1 line 1191. A logical gate-aggregate reading could be
compliant but is unspecified. This is a bounded **Low / Ambiguity**, not
proof of actual mutation, unauthorized Commit/Push, or a required extra
Push-approval gate. Optional Commit/Push are not authorized now.

Finding source: completed Governance Audit attempt
20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f, report lines 302–323.
Actual outcome: **CONSISTENT WITH MINOR FINDINGS**, not incomplete and not
qualifying for effectiveness. Core 52/52, 76 source files, seven mechanisms;
six PASS, Remediation FAIL. Critical/High/Medium 0; Low 1 and Ambiguities 1
count the same finding; other issue counts 0. No new Audit was executed here.

## 3. Investigation Result

Canonical Investigation attempt
20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff completed with
**CORRECTIVE DIRECTION IDENTIFIED**, finding confirmed. Source inspection
here confirms its bounded cause and current applicability; upstream report,
result and evidence hashes match the supplied bindings. The coordinator's
completed scoped handoff remains linked, not rewritten.

Current product Requirement, approved Implementation Plan, product
architecture/task IDs and approval evidence are **NOT APPLICABLE** to this
governance-only bootstrap correction, not missing product authorizations to
be invented. No product content was opened. Current Masters match the
live-resolved root decision but remain candidate/bootstrap comparison
sources, not an adopted target Master baseline. Product root remains
unadopted. Governance section 3 expressly permits ordinary finding
correction before Master adoption; no adoption prerequisite is invented.

## 4. Corrective Decision

Prepare the minimum local clarification of item 2 and its dependent Push
condition: preserve original authorization bytes, publish later commit
identity in new linked immutable evidence in the authorized action actor's
own attempt under the same Work ID, and make Push resolve that evidence
chain without expanding the original decision. Keep exact staged diff,
file list, Work ID, conditions and permitted actions bound. Later evidence
is execution evidence only, never a new Human YES or Push authorization.
It is published after the commit, so no commit must contain its own SHA.

Only `{target}` changes, section 43
Optional Post-Completion Commit item 2. No coupled Master, other role, or
historical-record amendment is indicated by the actual evidence.

Option A (linked later evidence) is selected as the proposed corrective
direction against the user's minimum-change/preserve-existing-rules
criteria and existing Artifact Governance 33.1 / Traceability 30.1 rules.
Option B (always require a later separate Push decision) is not selected:
it would change policy rather than clarify existing authorized-action
evidence. Deferral avoids exercising the optional route but leaves the
ambiguity unresolved. This selection is advisory until exact Human Approval.

Existing prior art: the 3438-byte GOV-AUD-20261102-001 linked clarification
preserved original report/result bytes and used later linked metadata.
Its historical Application and independent Verification/Review PASS are
attributed reported outcomes, not re-performed or transferred approval.
Historical GOV-001/GOV-002 dispositions and the addressed GOV-AUD-20261102-001
are not reopened. Earlier failed Application remains failed.

### Exact bounded amendment — UNAPPROVED / NOT APPLIED

Target encoding: UTF-8 without BOM; CRLF preserved, including final newline.
Exactly one occurrence of the following UTF-8 byte string is replaced;
all other target bytes must remain identical. No target write occurred.

**BEFORE** (one entire line, without its CRLF delimiter):

```text
{before}
```

**AFTER** (one entire line, without its CRLF delimiter):

```text
{after}
```

{table([proposal["base"], proposal["expected_after"]])}
The first row is the current BASE; the second is the proposed EXPECTED AFTER,
not an applied artifact. The machine-readable replacement and generated
unified diff are integrity-bound below; the report is the canonical decision
body and incorporates that exact proposal without a competing report.

Unchanged conditions: separate Human Acceptance only after correction,
Verification, Review and Audit; explicit exact-subject YES decisions before
actions; missing/NO/ambiguous/stale/mismatched gates block; only approved
governance paths; inspect branch/index/worktree/untracked state before
staging; never broad git add; stop for inseparable unrelated changes; exact
staged diff/list review and diff-check plus user confirmation do not replace
either gate; only expressly authorized actions; new commit, no amend.
Line 1309, item 1 and the full staging paragraph remain byte-identical.

## 5. Plan Change Required

**NOT APPLICABLE** — no applicable product approved Implementation Plan.
No plan update or plan approval is requested; this is the other-governed-
artifact status, not a fictional NO-PLAN-change corrective implementation.

## 6. Plan Impact

| Controlled dimension | Disposition |
|---|---|
| Current Plan validity | N/A; no product Plan is evaluated or overridden |
| Tasks, completed/partial/pending work and dependencies | N/A |
| Acceptance criteria | Product N/A; existing governance action gates preserved |
| Architecture, APIs, schema, persistence, security model | Product N/A; no change |
| Scope and constraints | Single governance item only; no scope expansion |
| Testing | Product tests/builds/runtime N/A; not executed |
| Verification/review | Future independent governance Verification then Review required |
| Deployment, infrastructure, integrations | N/A; no product change |

No retained product implementation is declared verified. Existing Audit
remains its original nonqualifying result; a new complete Audit is required
after approved application and independent assurance.

## 7. Proposed Plan Amendment

**NOT APPLICABLE.** The exact other-artifact proposal is in section 4 and
the bound proposal attachments. No approved Requirement or Plan is altered.

## 8. Human Approval Required

**YES.** A controlled active governance Agent definition changes.
{gate}

### Exact role bindings and application route

{table(list(roles.values()))}
Table order: actual preparer; proposed one-time applier; planned verifier
(identity-only); planned reviewer (identity-only); excluded SDLC Process
Orchestrator; excluded active Remediation actor. All role paths and hashes
are distinct. Actual preparer identity is `{H["ACTOR"]}`, bound to
this own invocation and observed runtime agent ID
0939dcbe-f104-454a-a8bd-62e36810ccd3. Runtime identity is separate from the
definition identity and is not an authenticated platform principal.

No existing effective standing application authority is established.
Historical one-time designations are not reusable. Propose a fresh scoped
one-time initial designation under Artifact Governance 3.5 and the current
Application Guideline. The candidate Application definition is an identity
binding, NOT proof of effective authority or executable capability. The
applier must differ from preparer, verifier, reviewer, Orchestrator and
active Remediation actor; no self-edit or future-definition authority is
inferred. Application authority is limited to this exact approved replacement.

Do not create future actor attempts now or claim their qualification.
After separate Application initiation the designated applier must publish
and independently read back its own current identity/permissions/capability
evidence before any target write, preflight every base and approval, apply
only approved bytes, read back exact after state, and stop on mismatch or
partial failure without unapproved rollback. No separate pre-existing
qualification attempt is demanded. Verification starts only after successful
Application and its own fresh Human start; Review starts only after PASS
Verification and its own fresh start. Each actual role path/hash must match
its approved planned binding or stop for an updated Human decision/approval.
Shared host/OS/repository alone does not defeat actor separation.

## 9. Implementation Readiness

**WAITING FOR GOVERNANCE CHANGE APPROVAL**, concurrently
**WAITING FOR APPLICATION AUTHORITY DESIGNATION**.
No application is ready or authorized. No Human approval is claimed.
The exact next Human gate is the combined decision/designation in section 8.
If approved/designated, the next safe boundary is to await a separate fresh
Application stage-start, not to apply automatically. If rejected, stop and
retain this immutable proposal; no silent amendment or substitution.

## 10. Next Process

Required Human exact correction approval and one-time actor designation
first; no other process runs in this invocation. Future sequence:
separately Human-started exact Application → separately Human-started
independent Verification → separately Human-started independent Review →
separately Human-started complete Governance Audit (52-core and all seven
mechanisms). Effectiveness requires CONSISTENT, zero issue counts and no
unresolved mechanism issue. Non-Master amendment does not require separate
Master adoption; the still-unadopted target Masters/product root are not
adopted by these stages. Human Acceptance/optional Commit/Push remain
separate later gates, never part of this proposal or automatic progression.

## Execution context, evidence, and limitations

Actual fresh Human start supplied in current parent conversation:

> {H["START"]}

This authorizes only this proposal process and own new records. No authenticated
original message ID or Human time is exposed; neither is invented.
Repository `{inv["repository"]["canonical"]}`, HEAD
`{inv["repository"]["head"]}`, branch `{inv["repository"]["branch"]}`.
Five preexisting tracked governance modifications and the untracked records
tree remain unchanged. Current source fingerprints, not HEAD alone, bind
the evaluated state.

Root adoption was live-resolved from OWNER ScalableParimal's decision at
https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236
(created/updated 2026-10-30T12:31:51Z). Its one-time initial Audit start was
not reused. Same-work reservation retained; no matching product-root Work ID.
Own current qualification, ACL/runtime/publication capability, authorization
and output scope were established before no-overwrite invocation publication.
A separate process read back the final invocation and validated all 9 inputs
and 357 baseline files before substantive comparison. Checkpoint 0001 records
that observed sequence and the later proposal-preparation boundary.

Executed evidence: current identity/ACL/git/runtime checks, live root decision
resolution, computed hashes/bytes, native complete-object JSON roundtrips,
no-overwrite publication/readback and in-memory exact replacement checks.
Source inspection: actual local wording and governing rules, role boundaries,
prior linked clarification. Reported: upstream Audit/Investigation and
historical assurance outcomes (stored bindings checked, not re-executed).
Unverified: historical actual mutation/unauthorized Commit/Push, authenticated
conversation identity/time, future actor capabilities and decisions.

Current roster showed only this matching runtime decision actor running,
others idle; it is not a competitor. Historical in-progress metadata alone
is not evidence of live writers or success. No conflicting live writer
observed; no continuous exclusion or exhaustive event log claimed.
Read-only is procedural, not sandbox-enforced; writable ACL/tool access
grants no source-write authority. Matching endpoint fingerprints cannot
exclude transient writes or same-principal tampering. Future Verification
and Review must disclose those limitations under their current Guidelines.
Residual-risk disclosure is not a new approval-validity gate. Clock samples
are preparation metadata, not exact filesystem publication times.

Only own new process records were written. No source, upstream/historical
record, Requirement, Plan, test, configuration or migration edit; no staging,
Commit, Push, adoption, product work, investigation restart, Application,
independent Verification/Review or Audit was executed. Proposal integrity
checks do not masquerade as those stages. Required exact text uses native
UTF-8, strict decode/roundtrip checks, no unexpanded template substitutions
or literal backtick-n pseudo-newlines.

## Machine-derived reference index

{table(inv["inputs"] + [ref(BASE / "attempt.json"), cp_ref, proposal_ref, patch_ref, evidence_ref])}
Role/source fingerprints and exact expected-after state are above and in the
proposal/evidence. The terminal result is published after this report and
binds its final bytes; neither this report nor earlier evidence claims a
future/self fingerprint. A subsequent own checkpoint records independent
final readback without editing this report/result in place.

## Completion

Scoped decision activities and required report are complete. Disposition:
accepted, exact other-governed-artifact proposal prepared, NOT applied.
The finding remains unresolved pending required Human and assurance gates.
STOP. No next stage is initiated.
"""
assert "`n" not in report
assert "\ufffd" not in report and "\ufffd" not in diff
unchanged()
report_ref = publish("report.md", report.encode("utf-8"), raw=True)
report_ref["identity"] = ATTEMPT + ":decision_report"
result = common("decision_result")
result.update({
    "execution_status": "COMPLETED",
    "execution_termination": "Scoped decision, exact proposal preparation and required reporting completed; no application or other stage",
    "outcome": "FINDING ACCEPTED \u2014 OTHER GOVERNED ARTIFACT CHANGE REQUIRED",
    "finding_disposition": "ACCEPTED",
    "report": report_ref, "evidence": evidence_ref, "proposal": proposal_ref, "patch": patch_ref,
    "invocation": ref(BASE / "attempt.json"), "checkpoint": cp_ref,
    "evaluated_base": proposal["base"], "proposed_after": proposal["expected_after"],
    "role_bindings": roles, "plan_change_required": "NOT APPLICABLE",
    "plan_impact": "NOT APPLICABLE; governance-only bootstrap correction",
    "proposed_plan_amendment": None, "human_approval_required": True,
    "human_approval_granted": False, "application_authority_designation_required": True,
    "implementation_readiness": "WAITING FOR GOVERNANCE CHANGE APPROVAL",
    "concurrent_gate": "WAITING FOR APPLICATION AUTHORITY DESIGNATION",
    "exact_next_human_gate": gate, "next_permitted_process": "Exact Human approval and fresh one-time designation; then await separate fresh Application start",
    "applied": False, "other_stage_started": False, "effectiveness_established": False,
    "master_baseline_adopted": False, "product_root_adopted": False,
    "commit": False, "push": False, "source_or_upstream_edits": False,
    "unresolved_items": ["Exact proposal approval", "Fresh scoped one-time applier designation",
        "Future Application, Verification, Review, complete Audit and each fresh stage-start"],
    "preservation": unchanged(), "serialization": "Native actual complete object dict/list/scalars roundtrip before every structured publication",
    "independent_final_readback": "Required next separate operation and new checkpoint; not claimed already executed",
    "limitations": evidence["limitations"]
})
result_ref = publish("result.json", result)
print(json.dumps({"report": report_ref, "result": result_ref, "proposal": proposal_ref,
                  "patch": patch_ref, "base": proposal["base"], "expected_after": proposal["expected_after"],
                  "upstream_binding_occurrences_checked": len(bindings), "roles": roles}, indent=2))
