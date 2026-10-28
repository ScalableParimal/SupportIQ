# SDLC Governance Consistency Audit

## Record identity and context

- Record type: `SDLC Governance Audit Report`
- Report identity: `audit-report-gov-bootstrap-002-20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3`
- Work ID: `gov-bootstrap-002`
- Attempt ID: `20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3`
- Report created (UTC): 
2026-10-28T15:43:29Z
- Canonical repository: `ScalableParimal/SupportIQ`
- Authorized source state: branch `sdlc-framework-onboarding`, commit `1e5c0bfca119f41974ce9d666f200fb663b142a1` (pushed and clean at preflight)
- Report path: `
docs/sdlc-records/governance/gov-bootstrap-002/attempts/20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3/report.md
`
- Terminal result identity/path: `audit-result-gov-bootstrap-002-20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3` / `
docs/sdlc-records/governance/gov-bootstrap-002/attempts/20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3
/result.json` (result will bind this report SHA-256 after durable publication; report does not self-assert its final hash)
- First-use Human authorization: GitHub issue comment `6473000256`, author `ScalableParimal` (`OWNER`), [canonical permalink](https://github.com/ScalableParimal/SupportIQ/issues/1#issuecomment-6473000256); API evidence body SHA-256 `6947D5707742990D54B8BFC4FF003CBB3BABB3BA8B67DB03208B48ADE252C1B6`.
- Published attempt evidence: `
docs/sdlc-records/governance/gov-bootstrap-002/attempts/20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3
/attempt.json`, identity `20261028T152652Z-f8162b96-ff36-435c-a958-8d1ea72b36a3`, SHA-256 `22E18EEEE2AB02E97F29D418211C439D9B60BE066E4897A3F03010B3B8B19EE1`.
- Three Master fingerprints matched the authorized values: `SDLC_GOVERNANCE.md` `A89A0E74B9201496F03749AA7A1764380D7E483A0A158956B29CE8B746C1E014`; `SDLC_ARTIFACT_GOVERNANCE.md` `86EC0B35B723E6EAD868707945D9B425B781863A9520BB916792477D76703B13`; `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` `D7879C0552EAA9449017B132469FC2B74237E859DA6AA43A09F64A896D9F415C`.
- Prior-attempt history: the external authorization explicitly abandons `gov-bootstrap-001`, attempt `20261028T150357Z-e5aa3039-1e13-4e61-bf25-91c077dd98ea`, whose record disappeared. Its contents are unavailable and are not assumed or reconstructed.
- Scope boundary: initial complete Governance Audit only. No baseline adoption, product-root adoption, portability assessment, finding investigation, corrective change, other process invocation, commit, or push was performed or authorized by this Work ID.

## Audit Summary

| Measure | Result |
|---|---:|
| 52-core catalog expected / found / assessed | 52 / 52 / 52 |
| Separately reported mechanism groups expected / present / assessed | 7 / 7 / 7 |
| Critical findings | 0 |
| High findings | 0 |
| Medium findings | 1 |
| Low findings | 1 |
| Ambiguities | 1 |
| Broken references | 1 |
| Missing governance controls | 0 identified |
| Unsupported or excessive governance controls | 0 identified |

**Overall Audit Result: INCONSISTENT.** The catalog and all seven mechanism definitions were assessed. Two unresolved findings prevent a `CONSISTENT` result and block baseline adoption. This is an AI audit result only; it is not approval, acceptance, or baseline adoption.

## Audit Scope

The audited 52-core catalog was the three Masters; ten core Guidelines; ten core Prompts; ten core Request Templates; ten core SDLC Process Skills; and nine core SDLC Process Agents. All expected paths were present and assessed. The nine-agent catalog intentionally has no separate Requirement Update Agent; the Requirement Update Skill and its governing artifacts are present. Four separately reported process bundles (Portability Assessment, Governance Amendment Application, Independent Governance Verification, Independent Governance Review) and the dedicated Audit, Remediation, and Orchestrator definitions were also inspected. The fingerprint appendix lists all 76 inspected governance artifacts (52 core plus 24 supplemental).

| Core category | Expected / found / assessed | Expected artifacts |
|---|---:|---|
| Master Governance documents | 3 / 3 / 3 | `docs/ai/sdlc/SDLC_GOVERNANCE.md`; `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md`; `docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` |
| Guidelines | 10 / 10 / 10 | Requirement Analysis, Requirement Analysis Verification, Implementation Planning, Requirement Update, Implementation Plan Verification, Implementation, Implementation Verification, Implementation Review, Finding Investigation, Corrective Change |
| Prompts | 10 / 10 / 10 | The corresponding ten core process Prompts listed above |
| Request Templates | 10 / 10 / 10 | The corresponding ten core process Request Templates listed above |
| Skills | 10 / 10 / 10 | The corresponding ten core process Skills listed above |
| Agents | 9 / 9 / 9 | Requirement Analysis, Requirement Analysis Verification, Implementation Planning, Implementation Plan Verification, Implementation, Implementation Verification, Implementation Review, Finding Investigation, Corrective Change Decision |

Exact core paths are enumerated in the source fingerprint appendix. The following separately reported bundles are outside the 52-core count: `PORTABILITY_ASSESSMENT`, `GOVERNANCE_AMENDMENT_APPLICATION`, `INDEPENDENT_GOVERNANCE_VERIFICATION`, and `INDEPENDENT_GOVERNANCE_REVIEW`, each with its Guideline, Prompt, Request, Skill, and Agent; plus the Governance Audit Skill/Agent, Governance Remediation Agent, and Process Orchestrator Agent.

## Separately Reported Mechanism Alignment

Source identity and SHA-256 for each inspected definition are in Appendix A. The only invocation evidence created for this audit is its own attempt, report, and result. For mechanisms not invoked, no actor-owned runtime records are claimed; runtime capability/effectiveness is `NOT APPLICABLE` because prerequisites or authorization were absent. This is not a pass of an unexecuted stage.

| Mechanism | Expected / present / assessed definition sources | Runtime evidence and applicable check outcomes | Result |
|---|---:|---|---|
| Governance Audit | 2 / 2 / 2 (Audit Skill, Audit Agent) | Current attempt is bound to the external first-use authorization, exact commit and Master hashes; report/result use the authorized actor-owned scope. Read-only boundary, source scope, reporting and no-adoption boundaries conform. | PASS for Audit mechanism conformance; this Audit outcome is INCONSISTENT |
| Governance Remediation | 1 / 1 / 1 (Remediation Agent) | No remediation invocation or cycle was authorized or started. Role separation, finding-led stages, no-self-approval/application boundary, traceability and handoffs were assessed. Conditional ApprovalAlarm references do not resolve in this repository; see GOV-002. | FINDINGS |
| SDLC Process Orchestration | 1 / 1 / 1 (Orchestrator Agent) | No product Orchestrator invocation or Process Initiation response was made; this direct Audit start is not an Orchestrator run. Scope, authority, interlock/formal-gate separation, persistence, and handoffs were assessed. O3 wording and conditional ApprovalAlarm references are unresolved; see GOV-001 and GOV-002. | FINDINGS |
| SDLC Portability Assessment | 5 / 5 / 5 (Guideline, Prompt, Request, Skill, Agent) | Definitions and discovery/invocation/routing relationships were assessed. No target-project assessment or product-root adoption was performed; runtime assessment is NOT APPLICABLE under the authorized scope. | PASS for definition-level conformance only |
| Governance Amendment Application | 5 / 5 / 5 (Guideline, Prompt, Request, Skill, Agent) | No approved amendment or Application authorization exists in this Work ID; no application was performed. Exact-approval, scope, preflight, bounded write, read-back and handoff definitions were assessed. | PASS for definition-level conformance only |
| Independent Governance Verification | 5 / 5 / 5 (Guideline, Prompt, Request, Skill, Agent) | No applied amendment or separately approved Verification invocation exists; no Verification was performed. Independence, read-only, scope, evidence and reporting definitions were assessed. | PASS for definition-level conformance only |
| Independent Governance Review | 5 / 5 / 5 (Guideline, Prompt, Request, Skill, Agent) | No passing Verification result or separately approved Review invocation exists; no Review was performed. Independence, read-only, scope, evidence and reporting definitions were assessed. | PASS for definition-level conformance only |

## Repository Reference Findings

| Reference | Observed state | Assessment |
|---|---|---|
| `docs/tools/ApprovalAlarm.md` | Missing | Conditional reference in Orchestrator O5.0 and Remediation §18 cannot resolve. Per the supplied onboarding context, the helper was intentionally not copied because the target stack is TBD. Captured as GOV-002; no attempt to run the integration was made. |
| `scripts/ApprovalAlarm.ps1` | Missing | Conditional command target in the same agent sections cannot resolve. The target omission is deliberate per the supplied context; captured with GOV-002. |
| `docs/requirement/customer-management/V2.md` | Example-only reference in the Audit Skill | Not treated as an actual missing governance input or inspected as a product artifact. Product artifacts remain outside scope. |

No expected core governance artifact was missing. The product root was not adopted or created, and no product-specific contents were inspected.

## Governance Consistency Findings

### GOV-001

- **Severity:** Medium
- **Category:** Ambiguity
- **Source Document:** `.github/agents/sdlc-process-orchestrator.agent.md`
- **Source Section:** O3 process transition flow, around line 368; see also O2.7 and O6.2
- **Related Document:** `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md`
- **Related Section:** §4.4, Orchestrator authority and Process Initiation interlock; corroborated by `docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §31.4
- **Issue:** The O3 transition diagram labels the fresh interlock response `Explicit Human Approval`. The Master states that Process Initiation is an execution interlock only, authorizes only initiation, and is not formal Human Approval or a Human Gate. The Agent elsewhere correctly distinguishes the response as a Process Initiation response and O6.2 titles it as an Orchestrator-specific interlock. The diagram therefore conflicts with its own rule and the Master terminology.
- **Evidence:** Agent O3 flow: `PROCESS_INITIATION_APPROVAL_PENDING → Explicit Human Approval → Invoke Process` (around lines 365–370). Master §4.4: Process Initiation response is not formal Human Approval and does not satisfy a formal Human Gate. Agent O6.2 explicitly names the interlock as “not a formal Human Approval gate.”
- **Impact:** A human or downstream actor could read the O3 flow label as converting the initiation response into formal Human Approval, or mistake it for a formal gate, despite the clarifying text elsewhere.
- **Recommended Resolution:** Through the governed finding/corrective process, replace the O3 label with wording such as `Fresh Process Initiation response` and retain an explicit separation from any subsequent formal Human Gate. No change was applied.
- **Human Decision Required:** Yes. A change to a controlled Orchestrator governance definition requires the applicable human decision and exact approval.

### GOV-002

- **Severity:** Low
- **Category:** Broken Reference
- **Source Document:** `.github/agents/sdlc-process-orchestrator.agent.md` and `.github/agents/sdlc-governance-remediation.agent.md`
- **Source Section:** Orchestrator O5.0, especially lines 1042–1046; Remediation §18, line 576, and notification-only exception around line 1095
- **Related Document:** `docs/tools/ApprovalAlarm.md` and `scripts/ApprovalAlarm.ps1` (both absent from SupportIQ)
- **Related Section:** Not applicable; referenced target files are absent
- **Issue:** The Orchestrator and Remediation definitions conditionally direct the actor to consult `docs/tools/ApprovalAlarm.md` and invoke `scripts/ApprovalAlarm.ps1`. Neither target exists in this repository. The Human-provided onboarding context confirms these files were deliberately not copied because the target stack is TBD. The condition makes the integration inactive unless it is effective, so this audit did not treat the absence as a skipped formal gate; the references nevertheless remain unresolved in the framework.
- **Evidence:** Orchestrator O5.0 lines 1042–1046 states “After the integration is effective under” the absent guide, gives the absent script command, and points to the guide for details. Remediation §18 line 576 uses the same conditional guide and command. Repository path checks show both referenced paths absent.
- **Impact:** The optional alarm behavior cannot be validated or enabled in this target repository; the agent definitions retain references to unsupported files. Formal Human Gates remain required and are not replaced by this optional notification integration.
- **Recommended Resolution:** Before any baseline adoption or enabling this optional integration, make a human-approved target-specific choice: provide and govern the required guide/script for the target stack, or update the conditional references through the applicable Governance change process. No files were copied or changed.
- **Human Decision Required:** Yes. Selecting or changing target-specific notification integration and altering controlled Agent definitions require human direction and applicable approval.

## Guideline Consistency Summary

All ten core Guidelines and the four separately reported mechanism Guidelines were present and assessed against the Masters, Prompts, Requests, Skills, and applicable Agents. Their role, approval, scope, evidence, traceability, process-boundary, and output requirements were generally aligned. No standalone Guideline finding was identified. The repeated Requirement Analysis routine-clarification sentence is redundant but consistent: both statements require the applicable approved Human decision and authorized update process.

## Prompt Consistency Summary

All ten core Prompts and four supplemental mechanism Prompts were present and assessed. Their invocation inputs and process boundaries align with their Guidelines and the Master authority model. No standalone Prompt finding was identified.

## Request Template Consistency Summary

All ten core Request Templates and four supplemental mechanism Requests were present and assessed for required source identities, scope, authorization, predecessor evidence, and output locations. No standalone Request finding was identified.

## SDLC Process Skill Consistency Summary

All ten core Skills and four supplemental mechanism Skills were present and assessed. Core Skills consistently require their corresponding Guideline, Prompt, and Request; preserve own-process boundaries; separate human authority; and restrict writes to applicable outputs. The Governance Audit Skill correctly prescribes first-use persistence preflight, read-only evaluation and report-only responsibility. No standalone Skill finding was identified.

## SDLC Process Agent Consistency Summary

All nine core Agents and the seven separately reported mechanism Agents were present and assessed. Core Agent-to-Skill links were present for each expected core Agent. Governance Amendment Application, Independent Governance Verification, Independent Governance Review, and Portability Assessment Agents align with their separately reported bundles. Governance Audit, Remediation, and Orchestrator definitions were evaluated independently as mechanism groups. GOV-001 and GOV-002 are the only findings; both are in the Orchestrator/Remediation control layer.

## Skill and Agent Traceability Summary

| Process | Guideline | Prompt | Request | Skill | Agent |
|---|---|---|---|---|---|
| Requirement Analysis | `REQUIREMENT_ANALYSIS_GUIDELINES.md` | `REQUIREMENT_ANALYSIS_PROMPT.md` | `REQUIREMENT_ANALYSIS_REQUEST.md` | `requirement-analysis/SKILL.md` | `requirement-analysis.agent.md` |
| Requirement Analysis Verification | `REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md` | `REQUIREMENT_ANALYSIS_VERIFICATION_PROMPT.md` | `REQUIREMENT_ANALYSIS_VERIFICATION_REQUEST.md` | `requirement-analysis-verification/SKILL.md` | `requirement-analysis-verification.agent.md` |
| Implementation Planning | `IMPLEMENTATION_PLANNING_GUIDELINES.md` | `IMPLEMENTATION_PLANNING_PROMPT.md` | `IMPLEMENTATION_PLANNING_REQUEST.md` | `implementation-planning/SKILL.md` | `implementation-planning.agent.md` |
| Requirement Update | `REQUIREMENT_UPDATE_GUIDELINES.md` | `REQUIREMENT_UPDATE_PROMPT.md` | `REQUIREMENT_UPDATE_REQUEST.md` | `requirement-update/SKILL.md` | Not in expected core Agent catalog |
| Implementation Plan Verification | `IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md` | `IMPLEMENTATION_PLAN_VERIFICATION_PROMPT.md` | `IMPLEMENTATION_PLAN_VERIFICATION_REQUEST.md` | `implementation-plan-verification/SKILL.md` | `implementation-plan-verification.agent.md` |
| Implementation | `IMPLEMENTATION_GUIDELINES.md` | `IMPLEMENTATION_PROMPT.md` | `IMPLEMENTATION_REQUEST.md` | `implementation/SKILL.md` | `implementation.agent.md` |
| Implementation Verification | `IMPLEMENTATION_VERIFICATION_GUIDELINES.md` | `IMPLEMENTATION_VERIFICATION_PROMPT.md` | `IMPLEMENTATION_VERIFICATION_REQUEST.md` | `implementation-verification/SKILL.md` | `implementation-verification.agent.md` |
| Implementation Review | `IMPLEMENTATION_REVIEW_GUIDELINES.md` | `IMPLEMENTATION_REVIEW_PROMPT.md` | `IMPLEMENTATION_REVIEW_REQUEST.md` | `implementation-review/SKILL.md` | `implementation-review.agent.md` |
| Finding Investigation | `FINDING_INVESTIGATION_GUIDELINES.md` | `FINDING_INVESTIGATION_PROMPT.md` | `FINDING_INVESTIGATION_REQUEST.md` | `finding-investigation/SKILL.md` | `finding-investigation.agent.md` |
| Corrective Change Decision & Plan Update | `CORRECTIVE_CHANGE_GUIDELINES.md` | `CORRECTIVE_CHANGE_PROMPT.md` | `CORRECTIVE_CHANGE_REQUEST.md` | `corrective-change-decision/SKILL.md` | `corrective-change-decision.agent.md` |

Paths in the table are relative to their canonical category directories (`docs/ai/guidelines/`, `docs/ai/prompts/`, `docs/ai/request/`, `.github/skills/`, `.github/agents/`). All listed Skill-to-Guideline, Skill-to-Prompt, Skill-to-Request, and Agent-to-Skill links were checked. Requirement Update is an expected Skill process without a separate core Agent in the 52-core catalog, not a missing artifact.

## Cross-Document Consistency Summary

The three Masters consistently separate process invocation interlocks from formal Human Approval and retain approval, verification, review, and acceptance boundaries. Lifecycle, persistence, evidence binding, actor separation, scope, and change-control relationships were aligned across the audited artifacts except for the Orchestrator O3 label (GOV-001). The optional ApprovalAlarm path is conditionally fail-closed but unresolved in this target repository (GOV-002). No other systemic conflict was identified.

## Governance Gaps

None identified in the assessed governance controls. All expected source artifacts were present. GOV-002 is an unresolved optional integration reference, not a missing mandatory Human Gate or core governance control.

## Unsupported or Excessive Governance

None identified. The audit did not infer authority from the absent optional alarm integration or treat it as a new Human Gate.

## Human Decisions Required

1. Human decision and exact approval are required before changing the Orchestrator terminology in GOV-001.
2. Human direction is required to decide whether the target adopts or removes the optional ApprovalAlarm integration references in GOV-002; any controlled-definition changes require the applicable approval.
3. Any later baseline adoption is a separate prospective Human decision and was expressly outside this Work ID. This Audit makes no adoption decision.

## Recommended Corrective Actions

No corrective action was performed. If separately authorized, route findings through Finding Investigation → Corrective Change Decision & Plan Update → required Human Approval → Governance Amendment Application → independent Governance Verification → independent Governance Review → a complete second Governance Audit. Each process stage requires its own applicable authorization and fresh stage-start; this report does not start any downstream process. Do not consider baseline adoption unless a complete later Audit is `CONSISTENT` and all seven mechanism groups have no unresolved issue.

## Overall Audit Result

**INCONSISTENT.** Two unresolved findings remain: one Medium Ambiguity and one Low Broken Reference. These findings block baseline adoption. No Human Approval, Human Acceptance, framework approval, or prospective baseline adoption is declared or implied.

## Appendix A — Audited source fingerprints

The following SHA-256 values bind the inspected repository governance sources as observed for this Audit. This manifest contains the 52-core catalog and 24 supplemental mechanism/control artifacts. It does not include the two absent optional ApprovalAlarm targets.

| Repository-relative source path | SHA-256 |
|---|---|
| `.github/agents/corrective-change-decision.agent.md` | `9CCC6DD6758F22B558116B1E4B32AC404BCF4164574EF9D591FD02AB6E3C6B7D` |
| `.github/agents/finding-investigation.agent.md` | `BECE1D3F5C20DD10B975E1536BB816232A47C2B43FDAAD76B13C4328DA84B218` |
| `.github/agents/governance-amendment-application.agent.md` | `F9E76A0061A85D3DDCF7BA3AD0BAF62A67D6C05B7F1E4DB0EFDF4E4BD55BB06D` |
| `.github/agents/implementation.agent.md` | `0DB61A40276EC947CAC483DA68006805CC482179CB7E2009DF237E267640E7EC` |
| `.github/agents/implementation-planning.agent.md` | `FF95320D9EAA4C6B3813804680A19545E6A5226E1B0961F63531A63337DBBFD2` |
| `.github/agents/implementation-plan-verification.agent.md` | `9F3960FA0E7E159DA0823E4CD03067CF6CC64C2E7FEFBCAD08D697663FFCF844` |
| `.github/agents/implementation-review.agent.md` | `36E3E29521B0605BDBB76BC1FA90D053E596DFBD27CF76085E0CBDBB0C162297` |
| `.github/agents/implementation-verification.agent.md` | `52BF4AB894920110DD5219D9233EF91F8ED384DEB833559C96EF064B8BE65994` |
| `.github/agents/independent-governance-review.agent.md` | `1CD8CCC4A96EFA64D4AA3B64DDDB2874F2337A45301B6B953033FC9016A9812E` |
| `.github/agents/independent-governance-verification.agent.md` | `ECD11EFE7F0078FE0B258DE819C8E473A3CF3EC674C8999E49F04194D62B8958` |
| `.github/agents/portability-assessment.agent.md` | `5FB6F0F8C8331CA88A925A2192EB8D07319E62D83BF84926BA232D67483FBD26` |
| `.github/agents/requirement-analysis.agent.md` | `EF3D141E77A44FD963A586194657EDD08BF7CD32F3018148C3A44C33065B89DF` |
| `.github/agents/requirement-analysis-verification.agent.md` | `F108557731314BF0211FFE149BABBB89322DB5F832C19B3CDC37989327702E38` |
| `.github/agents/sdlc-governance-audit.agent.md` | `66E669A820290D99C398E932F3DFA8848740C26B6ABFD07E2294B36116197488` |
| `.github/agents/sdlc-governance-remediation.agent.md` | `738D3AF3715A7B563207ACD91D9E95E82C477D45AB142707029726557CE99CD4` |
| `.github/agents/sdlc-process-orchestrator.agent.md` | `6D87F26DC08C354393C72C135734A065B01B668557F0020B3E15436FB35C6AF4` |
| `.github/skills/corrective-change-decision/SKILL.md` | `795164E58AF028F97ECBA133BC6845B1D9D76699A27239BD663BDD681A89B7C3` |
| `.github/skills/finding-investigation/SKILL.md` | `800D316A3AA97BFB3B2A3581FE16F8474C6DA2A199E3EB9CF397D3B7B2081448` |
| `.github/skills/governance-amendment-application/SKILL.md` | `D471B3A59A9581D5DB108B837E7CB9571540DA029139385EF3D2C9055EB4D2C1` |
| `.github/skills/implementation/SKILL.md` | `849F840F616335255534ACFD8B4D4554BCCE183776D55D7EEF92ED2A11129FC2` |
| `.github/skills/implementation-planning/SKILL.md` | `3FE1A74939355CE3E4A1282B753F6F1646CCC72ED1D97A3D5C7D9BED6A70F416` |
| `.github/skills/implementation-plan-verification/SKILL.md` | `0C28F8DBDCF6E8C1166E7BF56987F96507F1954450536C1C79CAA58DA05B04BB` |
| `.github/skills/implementation-review/SKILL.md` | `98E8F4B9BA60986B366BF67C6739D35F2F795126B18BCA8146B10E864A8E2C29` |
| `.github/skills/implementation-verification/SKILL.md` | `F0161829F3EA90E91CBFB733824FEE6F4250029A871A79E5B3515694DF34E5FC` |
| `.github/skills/independent-governance-review/SKILL.md` | `1E5DDB5BC37E7F8531635D6C28B052B6BFE2645B7C42FB79BCA9A2E4E7329A76` |
| `.github/skills/independent-governance-verification/SKILL.md` | `26FBFC8E4495F33C4E92F843CFFFBC476ABD42D931D201EA9E75EC986E62E270` |
| `.github/skills/portability-assessment/SKILL.md` | `4098E4C679985E3713E9E2E8F01A7B2A664590D341D2F211F360BCDB5FF7038A` |
| `.github/skills/requirement-analysis/SKILL.md` | `F5A40ED08CD7DFB52B906FE4A046B721BB6A84B5B2D28037BB780C48BDE143B7` |
| `.github/skills/requirement-analysis-verification/SKILL.md` | `5FD4B6F9A795DE3A2DDD256444BA340B54CBA486CD0AF10A598F9E76BEF7BC3D` |
| `.github/skills/requirement-update/SKILL.md` | `EA24E0F8DD833597396B08A53BFA7E845740E8BCF9565D04F0844817FCE880FD` |
| `.github/skills/sdlc-governance-audit/SKILL.md` | `50FBD8B326E6AAE8E50F9437E56C58E6ADEA01C73982516CA8CC0D1826E084D2` |
| `docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md` | `F27DD117E77C08E8477A097A402034725C61DB0B1997B6A47F491A28F7548203` |
| `docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md` | `14844FB1FA9865AB870CA1E3E8A50CD319756B2C8EA45231199B09368CC31BD2` |
| `docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md` | `D7C97C0C58EE8EEF35B953CCF1067943779017558B2C958726279C3382C4F790` |
| `docs/ai/guidelines/IMPLEMENTATION_GUIDELINES.md` | `E1CB6A40293A40844395593F47FD59F3EBA4CAD5557A0914D88609011BE96ACE` |
| `docs/ai/guidelines/IMPLEMENTATION_PLAN_VERIFICATION_GUIDELINES.md` | `E177732877B5B720978EC5C4312B3035CA6C3E9B4F0A19ECFF0EFAADA88F4BF8` |
| `docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md` | `34D70CBF5CC9969BDC07859AC0916DBB7BB741C07A322464DE12F244FB3F926F` |
| `docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md` | `AE87137C108670A032387EE52D202440416AF800B10951C3934DACD1D2645F03` |
| `docs/ai/guidelines/IMPLEMENTATION_VERIFICATION_GUIDELINES.md` | `53334F00DD2D10AD1E4A13E0DBBCAA54C48846948CEF6C4219D9DB398636D9A7` |
| `docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md` | `982AA75859BD3650B950918EC9C468BA93CCEB9562205B53BF50AC7D930C2E2B` |
| `docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md` | `0495F43A8AFC8ECBBB7BA59FB0FEBCAF0A3276EB95EF16AE3B907636690645A7` |
| `docs/ai/guidelines/PORTABILITY_ASSESSMENT_GUIDELINES.md` | `6BC8096DAF7F03BB328CBD543CDB7D541EF29B9B97426CCD4AD0E1EAAF813D88` |
| `docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md` | `82FCD3A6B25A2CB6BDB81D9425773AEFCDD9AEB7D088061C0679415B54479D0F` |
| `docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md` | `469EDCBAEC0816DF59048F06E50A52E0989BD4313B2470C7B3B7E1C958122C3E` |
| `docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md` | `926AA6CC5C7B2DDC3E32105A1E353B402C60641F6AC0AF0D213BD68D2090CCE2` |
| `docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md` | `88A6829A67692AF4E8D62C7D6F4104FE4911BB056734CEE47D5AC2A47BF285E7` |
| `docs/ai/prompts/FINDING_INVESTIGATION_PROMPT.md` | `7550968BAAD60A9214C1E1C7E5476D6270EF99FE3D17E4F85E5D20CAD26D8175` |
| `docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md` | `A79DC98DF3842E42A11E02F4D9FABFEC0D2C6EC5A160AECA171EE78C7542A80D` |
| `docs/ai/prompts/IMPLEMENTATION_PLAN_VERIFICATION_PROMPT.md` | `0E6CDDF8264AB82B3592F417A8F27D193D43B01F80116F3AA6806750CB06FAD7` |
| `docs/ai/prompts/IMPLEMENTATION_PLANNING_PROMPT.md` | `0B59816CE459EFE1A2BDDC7E22E43264F1DA19DA991F2750ADC3E8020359BAF7` |
| `docs/ai/prompts/IMPLEMENTATION_PROMPT.md` | `22C1E53BA93361D3CFB5815C8074AC69E670D4379CD4EF2615CFABFD0577DA57` |
| `docs/ai/prompts/IMPLEMENTATION_REVIEW_PROMPT.md` | `541E921C13A113E60E626458E2D8365846E03BF89CA5920F609531FB453A6B68` |
| `docs/ai/prompts/IMPLEMENTATION_VERIFICATION_PROMPT.md` | `37D85F8A95A78C603C5B43853706725BF17E419946C160A3A84D914BE591CA05` |
| `docs/ai/prompts/INDEPENDENT_GOVERNANCE_REVIEW_PROMPT.md` | `9D01635FABC7AAB12A2C16F7C7C17E8B185E4CA4E87193E5E38808231CF5CC08` |
| `docs/ai/prompts/INDEPENDENT_GOVERNANCE_VERIFICATION_PROMPT.md` | `BA7592B3AEB09C579EB166EA528E5450A18E6838FC31C2C8BC216877D529254B` |
| `docs/ai/prompts/PORTABILITY_ASSESSMENT_PROMPT.md` | `1E4BDE2D46758989CB26B943258F0F86C138B7A4BE5E7CEE162F201C85D45C09` |
| `docs/ai/prompts/REQUIREMENT_ANALYSIS_PROMPT.md` | `C67D4E55893F1F6BF869C229BB39DA1172565CEDA8675EE9AAA6545C91010588` |
| `docs/ai/prompts/REQUIREMENT_ANALYSIS_VERIFICATION_PROMPT.md` | `696A1F949FFDDE6883E0FB563C6BD74F52AD217A5839591063229A54A84582D8` |
| `docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md` | `928F40F1C6F6C7240B67F5088EE4BAEE237C5EC415DB0F49B59167275C623717` |
| `docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md` | `4CC1BCD1FE2408FC52AEDA0D24826CDEDE36AD30115DCB6C982DFD6A876DE038` |
| `docs/ai/request/FINDING_INVESTIGATION_REQUEST.md` | `836F79EE60357C502A2181E8CB4B04D500C351219358E484C0639A9FD275C120` |
| `docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md` | `2E0C1E05659093C2E6FE61D1EB88DB4588074E8B1A71453522D2965F964203A5` |
| `docs/ai/request/IMPLEMENTATION_PLAN_VERIFICATION_REQUEST.md` | `07C21B7221D9F997AA0EE26277D4B02BDEBAB7E6CEC745BA2A5DE9DA7B8FDDF8` |
| `docs/ai/request/IMPLEMENTATION_PLANNING_REQUEST.md` | `1144F2D29334F8ED659B1BDA5420E3E60C99E7E52735449F8B5651E146C278EE` |
| `docs/ai/request/IMPLEMENTATION_REQUEST.md` | `094535F4D3441DBF828CAB02B5076EFFBF846D81875E9300B26E9D72822EE9BA` |
| `docs/ai/request/IMPLEMENTATION_REVIEW_REQUEST.md` | `0259E007FB826FBD4A4089FD680DFB089803587519C7AE8DA56BE19AD8D9AFD5` |
| `docs/ai/request/IMPLEMENTATION_VERIFICATION_REQUEST.md` | `2F5FB17EF01B9FA523FB42E0EDC492694CF8F09C70E9D47177990337B206F4DD` |
| `docs/ai/request/INDEPENDENT_GOVERNANCE_REVIEW_REQUEST.md` | `2E27B04BBB2AA2F50B6A73F23DC91E653A75223B6CCF3FEA3D6DF377A34F1B79` |
| `docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md` | `19950013220CB93E88FFBA0606763E8FA93A8A60950E57360C50F9ACFCC9132A` |
| `docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md` | `3D828F54C3540244F29321A73D86BD1BAB5A983B91626A747BAEE88AA32D407E` |
| `docs/ai/request/REQUIREMENT_ANALYSIS_REQUEST.md` | `77B5CE9804C04C02EB5759D5246C102F71540CC38F2B887D321E9AAD625CD275` |
| `docs/ai/request/REQUIREMENT_ANALYSIS_VERIFICATION_REQUEST.md` | `1E5700BCD74531672C34592B29B74AC2BAF946B9B6F44E65A52A4DF2B8179C4B` |
| `docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md` | `BF14D96CEABA89EA598B03CB6ACACE82CFE10BE8CCBC9430BC12A8130D937F00` |
| `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md` | `86EC0B35B723E6EAD868707945D9B425B781863A9520BB916792477D76703B13` |
| `docs/ai/sdlc/SDLC_GOVERNANCE.md` | `A89A0E74B9201496F03749AA7A1764380D7E483A0A158956B29CE8B746C1E014` |
| `docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` | `D7879C0552EAA9449017B132469FC2B74237E859DA6AA43A09F64A896D9F415C` |
