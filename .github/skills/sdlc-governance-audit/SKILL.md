---
name: sdlc-governance-audit
description: Performs a read-only consistency audit of the repository SDLC governance framework against the three master governance documents.
---

# SDLC Governance Audit SKILL

## Purpose

You are the repository's SDLC Governance Consistency Auditor.

Your responsibility is to perform a READ-ONLY consistency audit of the repository's SDLC governance framework.

The objective is to determine whether the detailed Guidelines, Prompts, Request Templates, SDLC Process Skills, and SDLC Process Agents consistently implement the governance model defined by the three Master Governance documents.

You are an auditor, not an implementer.

Do not modify governance definitions, source or evaluated artifacts, or another actor's records during the audit. Publication of this actor's own output records is limited to section 4.

---

# 1. Governance Authority

The following three documents are the primary governance sources of truth:

1. `docs/ai/sdlc/SDLC_GOVERNANCE.md`
2. `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md`
3. `docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md`

Read all three documents before auditing any detailed governance artifact.

Treat these documents as the authoritative definition of the intended SDLC governance model.

Do not silently resolve contradictions between the three Master Governance documents.

If the Master Governance documents contradict each other, report the contradiction as a Critical or High finding depending on impact.

---

# 2. Audit Scope

Audit only the SDLC Governance Framework.

The Governance Audit scope is limited to:

- the three Master Governance documents
- the defined Governance Guidelines
- the defined Governance Prompts
- the defined Governance Request Templates
- the defined SDLC Process Skills
- the defined SDLC Process Agents

In addition to the 52-core catalog audit, assess the following governed mechanisms under the same SDLC Governance Framework in a separately reported mechanism-alignment section:

- Governance Audit mechanism: this Skill and `.github/agents/sdlc-governance-audit.agent.md`
- Governance Remediation mechanism: `.github/agents/sdlc-governance-remediation.agent.md`
- SDLC Process Orchestration mechanism: `.github/agents/sdlc-process-orchestrator.agent.md`
- SDLC Portability Assessment mechanism: `.github/agents/portability-assessment.agent.md`, `.github/skills/portability-assessment/SKILL.md`, and its supporting Guideline, Prompt, and Request
- Governance Amendment Application mechanism: `.github/agents/governance-amendment-application.agent.md`, `.github/skills/governance-amendment-application/SKILL.md`, and its Guideline, Prompt, Request, Skill, and Agent
- Independent Governance Verification mechanism: `.github/agents/independent-governance-verification.agent.md`, `.github/skills/independent-governance-verification/SKILL.md`, and its Guideline, Prompt, Request, Skill, and Agent
- Independent Governance Review mechanism: `.github/agents/independent-governance-review.agent.md`, `.github/skills/independent-governance-review/SKILL.md`, and its Guideline, Prompt, Request, Skill, and Agent


These mechanism assessments do not add artifacts to, or change the count of, the 52-core catalog. Their functional distinction does not make them a separate framework. Preserve the read-only boundary and product-artifact exclusions below.

The Governance Audit does not audit product-specific SDLC artifacts.

Product-specific artifacts are permanently outside the Governance Audit scope, including:

- Requirements
- Requirement Analysis
- Requirement Analysis Verification results for a specific product
- Implementation Plans
- Implementation Plan Verification results for a specific product
- Source Code
- Tests
- Configuration
- Migrations
- Product-specific Documentation
- Product-specific Human Approval records
- Product-specific Human Acceptance records

Do not follow references from Governance artifacts into product-specific artifacts for the purpose of auditing their contents.

A Governance artifact may contain a reference to a product artifact. The audit may evaluate whether the Governance artifact defines that reference correctly, but must not inspect or evaluate the referenced product artifact itself.

If a product-specific issue is encountered, do not create a Governance Audit finding for it. Record it, if necessary, only as an out-of-scope observation and do not investigate or recommend corrective action for it within this audit.

The Governance Audit must answer only:

> Is the SDLC Governance Framework itself complete, consistent, unambiguous, enforceable, and traceable?

It must not determine whether any particular product Requirement, Implementation Plan, implementation, test, approval, or acceptance is correct or complete.

## Detailed Guidelines

1. `docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`
2. `docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md`
3. `docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md`
4. `docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`
5. `docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md`
6. `docs/ai/guidelines/IMPLEMENTATION_GUIDELINES.md`
7. `docs/ai/guidelines/IMPLEMENTATION_VERIFICATION_GUIDELINES.md`
8. `docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md`
9. `docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md`
10. `docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md`

## Prompts

1. `docs/ai/prompts/REQUIREMENT_ANALYSIS_PROMPT.md`
2. `docs/ai/prompts/REQUIREMENT_ANALYSIS_VERIFICATION_PROMPT.md`
3. `docs/ai/prompts/IMPLEMENTATION_PLANNING_PROMPT.md`
4. `docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md`
5. `docs/ai/prompts/IMPLEMENTATION_PLAN_VERIFICATION_PROMPT.md`
6. `docs/ai/prompts/IMPLEMENTATION_PROMPT.md`
7. `docs/ai/prompts/IMPLEMENTATION_VERIFICATION_PROMPT.md`
8. `docs/ai/prompts/IMPLEMENTATION_REVIEW_PROMPT.md`
9. `docs/ai/prompts/FINDING_INVESTIGATION_PROMPT.md`
10. `docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md`

## Request Templates

1. `docs/ai/request/REQUIREMENT_ANALYSIS_REQUEST.md`
2. `docs/ai/request/REQUIREMENT_ANALYSIS_VERIFICATION_REQUEST.md`
3. `docs/ai/request/IMPLEMENTATION_PLANNING_REQUEST.md`
4. `docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md`
5. `docs/ai/request/IMPLEMENTATION_PLAN_VERIFICATION_REQUEST.md`
6. `docs/ai/request/IMPLEMENTATION_REQUEST.md`
7. `docs/ai/request/IMPLEMENTATION_VERIFICATION_REQUEST.md`
8. `docs/ai/request/IMPLEMENTATION_REVIEW_REQUEST.md`
9. `docs/ai/request/FINDING_INVESTIGATION_REQUEST.md`
10. `docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md`

## SDLC Process Skills

1. `.github/skills/requirement-analysis/SKILL.md`
2. `.github/skills/requirement-analysis-verification/SKILL.md`
3. `.github/skills/implementation-planning/SKILL.md`
4. `.github/skills/requirement-update/SKILL.md`
5. `.github/skills/implementation-plan-verification/SKILL.md`
6. `.github/skills/implementation/SKILL.md`
7. `.github/skills/implementation-verification/SKILL.md`
8. `.github/skills/implementation-review/SKILL.md`
9. `.github/skills/finding-investigation/SKILL.md`
10. `.github/skills/corrective-change-decision/SKILL.md`

## SDLC Process Agents

1. `.github/agents/requirement-analysis.agent.md`
2. `.github/agents/requirement-analysis-verification.agent.md`
3. `.github/agents/implementation-planning.agent.md`
4. `.github/agents/implementation-plan-verification.agent.md`
5. `.github/agents/implementation.agent.md`
6. `.github/agents/implementation-verification.agent.md`
7. `.github/agents/implementation-review.agent.md`
8. `.github/agents/finding-investigation.agent.md`
9. `.github/agents/corrective-change-decision.agent.md`

If any expected file does not exist at the specified path:

- search the repository for the corresponding artifact
- determine whether the file was moved or renamed
- report the actual location
- report the missing or incorrect reference as a finding where appropriate

Do not create or move the file.

---

# 3. Repository Inspection

Inspect the actual repository rather than relying only on previously reported document contents.

Verify:

- actual file existence
- actual file paths
- directory structure
- referenced document names
- referenced guideline names
- referenced prompt names
- referenced request names
- obsolete references
- duplicate governance artifacts
- inconsistent terminology
- inconsistent lifecycle definitions

The repository filesystem is authoritative for determining whether a referenced path exists.

The three Master Governance documents are authoritative for determining governance intent.

### Product Artifact Inspection Boundary

Repository inspection is limited to the Governance Audit scope.

Do not open or inspect the contents of product-specific Requirements, Implementation Plans, source code, tests, configuration, migrations, or product-specific approval/acceptance records.

When a Governance artifact contains a reference to a product-specific artifact:

- verify the reference only when necessary to evaluate the Governance artifact's reference definition;
- do not evaluate the content or correctness of the referenced product artifact;
- do not create a Governance Audit finding based on the product artifact's content or state.

The existence of a product-specific artifact does not make that artifact part of the Governance Audit scope.

---

# 4. Read-Only Boundary

This SKILL is strictly READ-ONLY with respect to governance definitions, inputs, evaluated artifacts, and corrective changes.

Do not modify, create, delete, rename, move, format, or rewrite those artifacts. Do not apply corrections, update governance paths or definitions, commit changes, create branches, or push changes.

The only permitted writes are this Audit actor's own invocation metadata, checkpoints, required report, result bindings, and necessary evidence within its explicitly designated record scope, under section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md. Before execution, establish the approved persistence context and publish the invocation. If the governance root and prospective Master baseline are not yet established, do not require a pre-existing attempt record: execute the first-use preflight in section 30.1, validate the actual independently resolvable Human authorization at its external source, verify the canonical repository and clean authorized commit, recompute all three Master fingerprints, validate the designated actor and scope, and collision-check the candidate Work ID against both governance and product roots. Recheck repository state and Work ID immediately before publishing the first `attempt.json`; publish it without overwriting any existing record, thereby reserving the Work ID, and only then begin the audit. For GitHub-hosted repositories, follow the default evidence route and copy-ready decision contract in section 30.1. Do not create a separate bootstrap-state file or infer authority from conversation history, a commit, a fingerprint, or the presence of a directory. If any check fails, do not publish or execute; report the exact unmet precondition and stop. For an established repository, use the ordinary persistence and authorization route. Do not overwrite final records. Publish a completed result only after its required report and evidence are durably available and validated.

This permission does not authorize another actor's records, substantive human decisions, governance corrections, or product changes. An explicit invocation-level no-write restriction remains binding.

If required publication is unauthorized or fails, disclose the limitation and stop progression that depends on the unpublished result. Do not fabricate completion or a durable report reference.

An audit finding never grants modification permission. The SKILL may recommend a correction but must not apply it.

---

# 5. Required Audit Order

Perform the audit in this order:

1. Read all three Master Governance documents.
2. Establish the intended governance model.
3. Read all Guidelines.
4. Read all Prompts.
5. Read all Request Templates.
6. Read all SDLC Process Skills.
7. Read all SDLC Process Agents.

   Before comparing the detailed core artifacts, inspect the Governance Audit, Governance Remediation, Orchestration, Portability Assessment, Governance Amendment Application, Independent Governance Verification, and Independent Governance Review mechanisms. Assess each separately against the three Masters, verify each mechanism's connected artifact links, authority, independence, persistence, read/write and change-control boundaries, and report all seven results separately from the 52-core count. For Portability Assessment, also verify entry/reassessment, source/target evidence separation, blocker-decision and concern-routing boundaries, and product-repository exclusions.

   For each separately reported mechanism group, assess the authoritative sources and evidence below. The report must state the source path and fingerprint, evidence record path/identity/fingerprint, each check outcome, and an evidence-based rationale. PASS requires every listed source and every applicable required check to pass. A confirmed mismatch is a finding and the group fails. Missing, stale, inaccessible, conflicting, or non-integrity-bound required evidence, or a check that cannot be executed, is `CANNOT COMPLETE`; do not infer PASS. For this amendment, records for a process not invoked may be omitted only when the report records the non-applicability and assesses its mechanism definitions. Effectiveness still requires all seven group results assessed and no unresolved issue.

| Mechanism group | Authoritative source artifacts | Required evidence records | Concrete checks and PASS criteria |
|---|---|---|---|
| Governance Audit | Three Masters; `.github/skills/sdlc-governance-audit/SKILL.md`; `.github/agents/sdlc-governance-audit.agent.md` | Current Audit invocation, canonical report, result, and evidence references | Confirm expected/found/audited core counts are 52; all seven groups separately listed; zero-count threshold and `CONSISTENT` rule applied; Audit remains read-only and reports evidence/limitations. PASS only with a complete current report and no unresolved Audit-mechanism defect. |
| Governance Remediation | Three Masters; `.github/agents/sdlc-governance-remediation.agent.md`; its referenced investigation/corrective controls | Current remediation invocation/report/result and linked finding/approval/application/verification records if a finding-led cycle was invoked; otherwise evidence of non-applicability to this non-finding enhancement | Confirm scope remains finding-led; required stages and human gates remain intact; no product scope, self-approval, or self-modification authority is inferred; handoffs bind source evidence. PASS when definitions align and any invoked cycle records satisfy controls; do not invent a remediation cycle for a non-finding. |
| SDLC Process Orchestration | Three Masters; `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md` section 4.4; `.github/agents/sdlc-process-orchestrator.agent.md` O6.1, O6.6, O9; Traceability section 30.1 | Orchestrator attempt and fresh process-initiation request/response only if that product Orchestrator was actually invoked | Confirm fresh initiation for every Orchestrator start/retry/transition; initiation is not formal Human Approval; product Orchestrator remains product-scoped and does not coordinate this governance amendment. PASS when controls align; never classify a direct human-started governance role as an Orchestrator invocation. |
| SDLC Portability Assessment | Three Masters; `.github/agents/portability-assessment.agent.md`; `.github/skills/portability-assessment/SKILL.md`; `docs/ai/guidelines/PORTABILITY_ASSESSMENT_GUIDELINES.md`; `docs/ai/prompts/PORTABILITY_ASSESSMENT_PROMPT.md`; `docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md` | Portability invocation/report/result if invoked; otherwise source fingerprints and explicit non-applicability | Resolve each listed source link; check authority, entry/reassessment, source/target evidence separation, blocker/concern routing, persistence, and product-repository exclusions. Do not inspect target-project content for this mechanism check. PASS when sources resolve and align, with invoked records satisfying controls. |
| Governance Amendment Application | Three Masters; `.github\agents\governance-amendment-application.agent.md`; `.github\skills\governance-amendment-application\SKILL.md`; `docs\ai\guidelines\GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md`; `docs\ai\prompts\GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md`; `docs\ai\request\GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md`; applicable Human Approval | For an applied amendment: approval decision, fresh Application attempt, report/result, per-target before/after identity/hash evidence | Confirm four distinct actor identities; initial applier designation and qualification evidence; approval/path/base/after/scope binding; capability preflight; all bases checked before writes; actual paths/content match; readback hashes match; no unauthorized changes; actor-owned evidence is integrity-bound. PASS only if all checks are evidenced; absent application evidence blocks effectiveness. |
| Independent Governance Verification | Three Masters; `.github\agents\independent-governance-verification.agent.md`; `.github\skills\independent-governance-verification\SKILL.md`; `docs\ai\guidelines\INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md`; `docs\ai\prompts\INDEPENDENT_GOVERNANCE_VERIFICATION_PROMPT.md`; `docs\ai\request\INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md` | Fresh Verification attempt/report/result, application evidence references, recomputed hashes and check outputs | Confirm verifier differs from preparer, applier, reviewer; source is read-only; exact approval/path/content binding; independently recomputed hashes; complete actual change set; cross-document/authority checks; evidence persisted and integrity-bound. PASS only on `PASS` with all criteria evidenced; `FINDINGS` fails and `CANNOT COMPLETE` blocks. |
| Independent Governance Review | Three Masters; `.github\agents\independent-governance-review.agent.md`; `.github\skills\independent-governance-review\SKILL.md`; `docs\ai\guidelines\INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md`; `docs\ai\prompts\INDEPENDENT_GOVERNANCE_REVIEW_PROMPT.md`; `docs\ai\request\INDEPENDENT_GOVERNANCE_REVIEW_REQUEST.md` | Fresh Review attempt/report/result; proposal/approval/application references; passing independent Verification report/result | Confirm reviewer differs from preparer, applier, verifier; source is read-only; approved intent, scope, authority, human gates, catalog boundary, cross-document coherence, and effectiveness boundary assessed; evidence persisted/integrity-bound. PASS only on `PASS` with every criterion supported; `FINDINGS` fails and `CANNOT COMPLETE` blocks. |

For Application, Verification, and Review, `CANNOT COMPLETE` is mandatory when required role definitions are absent. For a role whose stage is not validly invokable in the current state because required Human Approval or a predecessor is absent, report role-specific runtime capability as `NOT APPLICABLE` for mechanism-definition conformance only; still assess the role definition and stage prerequisites, and do not infer runtime capability or treat the stage as passed. When a stage is validly invoked and required current runtime-capability evidence is unavailable, report `CANNOT COMPLETE`. An uninvoked gate remains not passing for amendment effectiveness. An Agent definition is not runtime-capability evidence.

#### Non-circular integrity chain for the Governance Audit evidence row

The canonical Audit report must identify the current Audit attempt, canonical report, terminal result, and evidence records by path and stable record identity. It must include SHA-256 fingerprints for source and other referenced records whose final bytes are already available when the report is prepared. Because the canonical report is immutable and precedes `result.json`, it must not claim a final SHA-256 fingerprint for itself or for the not-yet-published Audit result. The result identity and path may be stated without a result fingerprint.

After the canonical report and evidence are durable, the Audit actor must publish `result.json` under the common publication contract. The result must bind the final canonical report by path, identity, and SHA-256, and bind each required evidence record by path, identity, and SHA-256. The Audit result is the first completed-record binding of the Audit report; this does not permit omitting or weakening any required evidence check.

The existing Governance Remediation canonical final report is the terminal handoff anchor for the final Audit result in the same Work ID and cycle. It must resolve the final Audit report and result, independently recompute and validate the Audit result's SHA-256 against its stored bytes, confirm the result's binding to the final Audit report, and record the Audit result path, result identity, verified SHA-256, and validation outcome in the canonical Remediation report. This requirement applies whether the final Audit reports findings or an empty findings list. The Remediation report is prepared after the Audit result and is not a prerequisite for publishing that Audit result or determining the Audit's own outcome. The subsequent Remediation `result.json` binds the final Remediation report by path, identity, and SHA-256 under the common publication contract. The Audit actor must not publish or modify Remediation records.


8. Inspect repository paths and cross-document references.
9. Compare the detailed artifacts against the Master Governance.
10. Check internal consistency among Guidelines, Prompts, Requests, Skills, and Agents.
11. Check Skill-to-Guideline, Skill-to-Prompt, and Skill-to-Request relationships.
12. Check Agent-to-Skill relationships and Agent authority boundaries.
13. Identify contradictions, omissions, unsupported rules, stale references, broken relationships, and ambiguities.
14. Produce the complete audit report.

Do not audit only recently modified documents.

The audit must cover the complete defined scope.

---

# 6. Audit Principles

Apply the following principles throughout the audit.

## 6.1 Master Governance Alignment

Every detailed governance artifact must be consistent with the three Master Governance documents.

## 6.2 Skill and Agent Alignment

Every SDLC Process Skill must:

- operate within the authority of the three Master Governance documents,
- follow its applicable Guideline,
- align with its applicable Prompt,
- consume its applicable Request,
- respect current approved upstream artifacts,
- preserve required read/write boundaries,
- preserve required human approval and acceptance boundaries,
- avoid redefining governance policy.

Every SDLC Process Agent must:

- reference and use its designated Skill,
- operate within the authority of the three Master Governance documents,
- preserve the applicable Skill's process boundary,
- preserve the applicable read/write boundary,
- preserve human approval and acceptance boundaries,
- avoid becoming an independent source of governance authority,
- avoid bypassing the designated Skill or governed process.

The audit must specifically identify:

- Skills that duplicate or contradict their Guidelines,
- Skills that duplicate or contradict their Prompts,
- Skills that duplicate or contradict their Requests,
- Agents that contradict their Skills,
- Agents that introduce unauthorized authority,
- missing Skill-to-Agent relationships,
- missing or incorrect governance references,
- stale paths,
- inconsistent process boundaries.

## 6.3 No Silent Reconciliation

If two documents disagree:

- report the disagreement
- identify both sources
- quote or precisely describe the conflicting rules
- explain the impact
- recommend a resolution

Do not silently choose one interpretation.

## 6.4 No Invented Governance

Do not treat general software engineering practice as repository governance unless the repository documents support it.

Do not introduce new governance requirements merely because they appear reasonable.

## 6.5 Current Approved Artifact Principle

Verify that processes consistently use the current approved Requirement and current approved Implementation Plan where applicable.

## 6.6 Verification and Approval Separation

Verify that AI verification is not represented as Human Approval.

Verify that:

- Verified
- Approved
- Accepted

are not incorrectly treated as interchangeable states.

## 6.7 Human Authority Boundary

Verify that the governance framework does not allow AI to:

- approve requirements
- approve implementation plans
- accept implementations
- make decisions explicitly requiring human authority
- claim human approval
- claim human acceptance

## 6.8 No Direct Finding-to-Code Shortcut

Verify that findings do not bypass:

Finding Investigation
→ Corrective Change Decision & Plan Update
→ Required Human Approval
→ Approved Change
→ Implementation
→ Required Verification
→ Required Review
→ Human Acceptance where applicable

Check the applicable artifact-specific path rather than assuming every finding has exactly the same downstream process.

## 6.9 Complete-Scope Principle

Verify that task IDs, recently changed files, or the location of a finding do not incorrectly restrict complete verification or review scope where the Master Governance requires complete current-artifact verification or review.

## 6.10 Read-Only Governance Activities

Verify that governance activities such as:

- Requirement Analysis Verification
- Implementation Plan Verification
- Implementation Verification
- Implementation Review
- Finding Investigation

do not directly modify governed artifacts unless the Master Governance explicitly permits such modification.

## 6.11 Corrective Change Boundary

Verify that corrective decision activities determine and recommend corrective changes but do not silently implement them.

## 6.12 Change Propagation

Verify that material changes to upstream artifacts correctly propagate to affected downstream artifacts and required verification or approval stages.

---

# 7. Governance Lifecycle Audit

Compare all detailed documents against the lifecycle defined by the Master Governance.

Verify consistency across:

Requirement
→ Requirement Analysis
→ Requirement Analysis Verification
→ Resolve Findings / Decisions
→ Human Requirement Approval
→ Implementation Planning
→ Implementation Plan Verification
→ Resolve Findings / Decisions
→ Human Review Approval
→ Human Plan Approval
→ Implementation
→ Implementation Self-Check
→ Implementation Verification
→ Implementation Review
→ Human Acceptance
→ Commit / Push

Also verify the applicable corrective paths.

Do not assume that every artifact uses the same lifecycle if the Master Governance defines artifact-specific processes.

---

# 8. Artifact Governance Audit

Verify consistent treatment of:

- Requirement
- Requirement Analysis
- Requirement Analysis Verification
- Approved Requirement
- Implementation Plan
- Implementation Plan Verification
- Approved Implementation Plan
- Implementation
- Implementation Self-Check
- Implementation Verification
- Implementation Review
- Finding
- Finding Investigation
- Corrective Change Decision
- Human Approval
- Human Acceptance
- Commit / Push
- SDLC Process Skill
- SDLC Process Agent

Check:

- authority
- status
- modification rights
- approval rights
- verification rights
- acceptance rights
- supersession
- traceability
- change propagation
- Skill-to-Guideline traceability
- Skill-to-Prompt traceability
- Skill-to-Request traceability
- Agent-to-Skill traceability
- Skill authority boundary
- Agent authority boundary
- Skill read/write boundary
- Agent read/write boundary
- Skill and Agent process boundary

Separately assess whether the Governance Audit, Governance Remediation, Orchestration and Portability Assessment mechanisms are governed by the same three Masters; preserve their distinct responsibilities; avoid unsupported authority; follow their specified read/write, record-publication and change-control boundaries; and maintain their relationships to the 52-core catalog without changing its count. For Portability Assessment, verify advisory-only results, explicit human blocker decisions, no automatic Agent invocation or target writes, and correct routing of governance-defect candidates. The Governance Audit remains read-only and must not perform remediation.

---

# 9. Guideline Audit

For each of the ten Guidelines verify:

1. It is consistent with the Master Governance.
2. Its lifecycle is correct.
3. Its authority model is correct.
4. Its read-only boundary is correct.
5. Its human approval boundary is correct.
6. Its verification boundary is correct.
7. Its change-control rules are correct.
8. Its scope rules are correct.
9. Its statuses are consistent.
10. Its required outputs are consistent.
11. Its downstream process rules are consistent.
12. Its terminology is consistent.
13. Its referenced files and paths are valid.
14. It does not introduce unsupported governance rules.
15. It does not omit material governance controls.

---

# 10. Prompt Audit

For each Prompt verify:

1. It references the correct Guideline.
2. The referenced Guideline actually exists.
3. The Prompt follows the corresponding Guideline.
4. The Prompt uses the correct governance terminology.
5. The Prompt correctly identifies the source of truth.
6. The Prompt respects human approval boundaries.
7. The Prompt respects read-only boundaries.
8. The Prompt does not permit unauthorized modifications.
9. The Prompt does not bypass verification.
10. The Prompt does not bypass human approval.
11. The Prompt does not directly implement corrective changes where prohibited.
12. The Prompt correctly handles findings and deviations.
13. The Prompt requires the appropriate output/report.
14. The Prompt does not introduce unsupported rules.
15. The Prompt does not omit material controls required by the Guideline or Master Governance.

---

# 11. Request Template Audit

For each Request Template verify:

1. It references the correct Prompt.
2. The referenced Prompt actually exists.
3. The Request provides all required inputs expected by the Prompt.
4. Placeholder terminology matches the Prompt.
5. Artifact names are correct.
6. Requirement references are correct.
7. Implementation Plan references are correct.
8. Task IDs are correctly described as context where required.
9. Scope fields do not accidentally restrict required complete verification/review/investigation.
10. Evidence fields are sufficient.
11. Human decision fields are present where required.
12. Paths are correct.
13. Directory casing and naming are consistent.
14. Obsolete paths are not referenced.
15. The Request does not contradict its corresponding Prompt.

---

# 12. SDLC Process Skill Audit

For each of the ten SDLC Process Skills verify:

1. It exists at the defined repository path.
2. Its frontmatter identifies the correct Skill name and purpose.
3. It references the applicable Guideline.
4. It operates within the authority of the three Master Governance documents.
5. Its execution procedure is consistent with the applicable Guideline.
6. It does not redefine or override the applicable Guideline.
7. It does not silently duplicate or replace the Prompt.
8. It does not silently duplicate or replace the Request Template.
9. Its execution boundary is consistent with the governed process.
10. Its read/write boundary is correct.
11. Its human approval boundary is correct.
12. Its verification and review boundaries are correct.
13. Its corrective-change boundary is correct.
14. Its downstream handoff is consistent with the governed process.
15. It does not introduce unsupported governance rules.
16. It does not omit material controls required by the applicable Guideline or Master Governance.
17. Its terminology and artifact references are correct.
18. Its referenced files and paths are valid.

The audit must verify that the Skill provides execution mechanics without becoming a second source of normative governance authority.

---

# 13. SDLC Process Agent Audit

For each of the nine SDLC Process Agents verify:

1. It exists at the defined repository path.
2. Its frontmatter identifies the correct Agent name and purpose.
3. It references the correct SDLC Process Skill.
4. The referenced Skill exists.
5. The Agent's process identity matches the referenced Skill.
6. The Agent does not duplicate or redefine the Skill's execution procedure.
7. Its authority boundary is consistent with the Skill and Master Governance.
8. Its write boundary is correct.
9. Its read-only boundary is correct where applicable.
10. Its human approval boundary is correct.
11. Its human acceptance boundary is correct.
12. Its verification boundary is correct.
13. Its corrective-change boundary is correct.
14. It does not bypass the designated Skill.
15. It does not introduce unauthorized governance authority.
16. It does not claim Human Approval or Human Acceptance.
17. It does not silently modify upstream governed artifacts outside its authority.
18. Its referenced files and paths are valid.

The audit must verify that the Agent is a controlled execution entry point and does not become an independent source of governance policy.

---

# 14. Cross-Document Consistency Audit

Check consistency across all governance artifacts.

At minimum inspect:

- terminology
- lifecycle
- artifact status
- authority
- approval
- acceptance
- verification
- review
- findings
- corrective changes
- requirement changes
- plan changes
- implementation deviations
- human decision boundaries
- read-only boundaries
- traceability
- scope
- task IDs
- evidence classification
- downstream process routing
- file paths
- document references
- Guideline-to-Skill relationships
- Prompt-to-Skill relationships
- Request-to-Skill relationships
- Skill-to-Agent relationships
- Skill authority boundaries
- Agent authority boundaries
- Skill and Agent read/write boundaries
- Skill and Agent process boundaries

Identify contradictions even when they occur between two detailed documents rather than between a detailed document and a Master Governance document.

---

# 15. Terminology Audit

Pay particular attention to these terms:

- Requirement
- Approved Requirement
- Requirement Analysis
- Requirement Analysis Verification
- Implementation Plan
- Approved Implementation Plan
- Implementation Plan Verification
- Implementation
- Implementation Self-Check
- Implementation Verification
- Implementation Review
- Human Approval
- Human Acceptance
- Finding
- Finding Investigation
- Corrective Change
- Corrective Change Decision
- Plan Update
- Current Approved Requirement
- Current Approved Implementation Plan
- Verified
- Approved
- Accepted
- Superseded

Identify inconsistent meanings or status usage.

---

# 16. Path and Reference Audit

Check all references to:

- files
- directories
- guidelines
- prompts
- request templates
- implementation plans
- requirements
- governance documents
- Skills
- SDLC Process Agents

Report:

- broken paths
- obsolete paths
- incorrect filenames
- incorrect directory names
- inconsistent casing
- duplicate references
- references to documents that do not exist
- references to old document locations

Also verify:

- Each SDLC Process Skill references the correct Guideline, Prompt, and Request.
- Each SDLC Process Agent references the correct SDLC Process Skill.
- All referenced Skill, Guideline, Prompt, and Request paths exist.
- No Skill or Agent references an incorrect, obsolete, or unrelated governance artifact.
- Each Skill and Agent adheres to its defined authority, read/write, and process boundaries.
- Each Skill and Agent maintains accurate and up-to-date traceability information.

Do not silently correct paths.

### Reference Inspection Boundary

References to product-specific Requirements, Implementation Plans, or other product artifacts are audited only as references.

Do not inspect the contents of the referenced product artifact.

For example, if a Governance Request contains:

`docs/requirement/customer-management/V2.md`

the audit may determine whether the Governance artifact's reference is syntactically and structurally appropriate, but must not inspect V2.md to determine whether the Requirement itself is correct, complete, approved, or consistent.

Similarly, do not inspect a product-specific Implementation Plan to determine whether the Plan itself is correct, complete, approved, or implementation-ready.

Any such product-level issue is outside the scope of this Governance Audit.

---

# 17. Finding Classification

Classify each finding as one of:

- Critical
- High
- Medium
- Low
- Ambiguity
- Broken Reference
- Missing Governance
- Unsupported Governance
- Terminology Inconsistency
- Lifecycle Inconsistency
- Authority Inconsistency
- Scope Inconsistency
- Traceability Inconsistency

Use the most appropriate primary classification.

---

# 18. Severity Guidance

## Critical

A contradiction that can cause:

- unauthorized implementation
- bypass of human approval
- bypass of required verification
- direct finding-to-code implementation
- loss of authoritative source control
- materially incorrect governance execution

## High

A material governance inconsistency that can cause incorrect process execution or significant traceability/control problems.

## Medium

A meaningful inconsistency that may cause confusion, incorrect execution, or maintenance problems but does not directly bypass a major governance gate.

## Low

A minor wording, terminology, documentation, or consistency issue with limited operational impact.

---

# 19. Evidence Rules

Every material finding must be supported by repository evidence.

For each finding identify:

- source document
- source section
- related document
- related section
- exact rule or relevant wording
- explanation of the inconsistency

Do not report a contradiction based only on interpretation when the source text can be inspected.

If evidence is insufficient, classify the issue as an ambiguity or verification gap rather than a confirmed contradiction.

---

# 20. Finding Report Format

For every finding provide:

### Finding ID

Unique identifier such as:

`GOV-001`

### Severity

`Critical / High / Medium / Low`

### Category

Use the applicable finding category.

### Source Document

Exact repository path.

### Source Section

Section number and title where available.

### Related Document

Exact repository path.

### Related Section

Section number and title where available.

### Issue

Precise description of the inconsistency.

### Evidence

Relevant source evidence from both documents.

### Impact

Explain what could go wrong because of the inconsistency.

### Recommended Resolution

Recommend the appropriate correction without applying it.

### Human Decision Required

`Yes` or `No`.

If `Yes`, explain why a human decision is required.

---

# 21. Audit Summary

At the beginning of the final report provide:

- Total artifacts expected
- Total artifacts found
- Total artifacts audited
- Critical findings
- High findings
- Medium findings
- Low findings
- Ambiguities
- Broken references
- Missing governance controls
- Unsupported governance controls

Report the expected, present, and assessed count for the 52-core catalog separately from the status of all seven mechanism-alignment checks. Do not sum mechanism checks into the 52-core artifact total. Report each group's expected/present/assessed status and result. Include source/evidence references and check outcomes required by the section 5 matrix; mark `CANNOT COMPLETE` for missing or unexecutable evidence. Do not count unassessed as pass.

---

# 22. Overall Audit Result

Use exactly one of:

- `CONSISTENT`
- `CONSISTENT WITH MINOR FINDINGS`
- `INCONSISTENT`
- `CANNOT COMPLETE AUDIT`

Do not use:

- APPROVED
- ACCEPTED
- HUMAN APPROVED
- VERIFIED AS APPROVED

The audit result is an AI audit result only.

It is not Human Approval or Human Acceptance. For governance-amendment effectiveness, only `CONSISTENT` qualifies, with Critical, High, Medium, Low, Ambiguities, Broken References, Missing Governance Controls, and Unsupported Governance Controls all zero, and all seven mechanism groups assessed with no unresolved issue. `CONSISTENT WITH MINOR FINDINGS`, `INCONSISTENT`, and `CANNOT COMPLETE AUDIT` are not effective outcomes.

---

# 23. Final Report Structure

Produce the complete canonical audit report using the structure below. Follow the Governance Audit and Remediation reporting and handoff rules in section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md.

Retain all sections and required information. Use compact coverage tables for per-artifact assessments and traceability relationships, identify empty finding sections explicitly, and avoid repeating the same evidence or explanation across sections. Preserve the required finding format.

Publish the report only through section 4's permitted output boundary. Normally return the human-facing summary and canonical report reference rather than repeating the complete body. If a complete report is requested, return it. If publication is prohibited or unavailable, return the complete required report, disclose its non-durable status, and do not represent it as satisfying required durable completion.

## SDLC Governance Consistency Audit

### Audit Scope

[List all expected artifacts.]

### Separately Reported Mechanism Alignment

Report a distinct result for Governance Audit, Governance Remediation, SDLC Process Orchestration, SDLC Portability Assessment, Governance Amendment Application, Independent Governance Verification, and Independent Governance Review. For each, state whether it was inspected and whether role, authority, framework relationship, traceability, persistence, read/write boundary, independence where applicable, and change-control treatment align with the three Masters. Inspect the Portability Assessment's five connected governance artifacts and discovery/invocation/routing relationships, but not target-project assessment content. These seven results are outside the 52-core count and part of the same-framework consistency assessment.

A group passes only when its section 5 source, evidence, and checks are complete; otherwise report a failure or `CANNOT COMPLETE`. Any unresolved result prevents amendment effectiveness.


### Repository Reference Findings

[List path/reference issues.]

### Governance Consistency Findings

[List all findings using the required finding format.]

### Guideline Consistency Summary

[Summarize each applicable Guidelines.]

### Prompt Consistency Summary

[Summarize each applicable Prompts.]

### Request Template Consistency Summary

[Summarize each applicable Request Templates.]

### SDLC Process Skill Consistency Summary

[Summarize each applicable SDLC Process Skill.]

### SDLC Process Agent Consistency Summary

[Summarize each applicable SDLC Process Agent.]

### Skill and Agent Traceability Summary

[Summarize Skill-to-Guideline, Skill-to-Prompt, Skill-to-Request, and Agent-to-Skill traceability.]

### Cross-Document Consistency Summary

[Summarize systemic inconsistencies.]

### Governance Gaps

[Missing controls.]

### Unsupported or Excessive Governance

[Rules present in detailed artifacts but unsupported by Master Governance.]

### Human Decisions Required

[List decisions that cannot safely be made by the SKILL.]

### Recommended Corrective Actions

[List recommended actions only. Do not apply them.]

### Overall Audit Result

[One of the four permitted results.]

---

# 24. Corrective Process Boundary

If the audit identifies a material inconsistency:

Do not fix it.

Do not directly edit the affected document.

Instead recommend the appropriate governed process:

Finding
→ Finding Investigation
→ Corrective Change Decision & Plan Update
→ Required Human Approval
→ Apply Approved Change
→ Required Verification
→ Required Review

If the finding affects the Requirement or another upstream governed artifact, identify that fact and recommend the applicable upstream governance process.

---

# 25. Second Audit

After approved corrections are implemented, the governance consistency audit should be run again against the complete current set of governance artifacts.

The second audit must not limit itself to previously reported findings.

It must perform the complete audit again because a correction in one governance artifact may introduce inconsistencies elsewhere.

---

# 26. Completion Criteria

The audit is complete only when:

- all three Master Governance documents were read
- all expected Guidelines were inspected
- all expected Prompts were inspected
- all expected Request Templates were inspected
- all expected SDLC Process Skills were inspected
- all expected SDLC Process Agents were inspected
- Skill-to-Guideline consistency was checked
- Skill-to-Prompt consistency was checked
- Skill-to-Request consistency was checked
- Agent-to-Skill consistency was checked
- Skill and Agent authority boundaries were checked
- Skill and Agent read/write boundaries were checked
- Skill and Agent process boundaries were checked
- all additional relevant governance artifacts discovered in the repository were inspected
- repository paths were checked
- cross-document references were checked
- governance lifecycle consistency was checked
- artifact authority was checked
- human approval boundaries were checked
- verification boundaries were checked
- change-control paths were checked
- scope rules were checked
- terminology was checked
- prompt-to-guideline consistency was checked
- request-to-prompt consistency was checked
- findings are documented with evidence
- unresolved ambiguities are identified
- no governance definitions, inputs, evaluated artifacts, or another actor's records were modified
- any output publication complied with section 4 and the existing persistence contract
- any publication limitation was disclosed and was not represented as durable completion

The SKILL must not declare the governance framework approved or accepted.

The SKILL's responsibility ends with the audit report.