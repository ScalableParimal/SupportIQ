# SDLC Portability Assessment Guidelines

## 1. Purpose and outcome

Assess whether the existing SDLC Process Automation framework can be applied to an explicitly identified target project, what adaptations or gaps exist, what evidence is missing, and what governed next action is appropriate. This is a cross-project assessment mechanism within the existing framework, not a parallel SDLC, product implementation process, Governance Audit, or approval authority.

## 2. Authority and subject boundary

Operate under the three Master Governance documents and this Guideline. The Prompt controls invocation; the Request supplies a particular target and scope; the Skill defines reusable execution mechanics; the Agent is the controlled entry point. An assessment is advisory. It cannot approve requirements/plans, make an assessment recommendation binding, authorize writes, or silently classify an observation as a formal Governance Audit finding.

Keep evidence for the source framework and target project separate. Identify repository/workspace roots and immutable revisions/fingerprints where available. Inspect only authorized in-scope paths. The assessment actor is read-only in both repositories. It must not execute project scripts, tests, workflows, or runtime operations unless the invocation expressly authorizes that bounded execution and access. Static inspection is not proof of runtime behavior, safe cross-repository execution, or successful integration.

## 3. Entry, reuse and reassessment

For a new target project, before invoking this assessment establish (1) the target's separately and explicitly adopted product persistence root and (2) the target's adopted exact three-file Master baseline, after target-repository Audit and required assurance, under `SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` §§30.1 and 42. The governance-root bootstrap/Audit may precede these prerequisites but does not adopt the product root or Master baseline. This assessment is not an implicit root or baseline adopter; it must not be invoked or publish product-process records before both prerequisites are established. The assessment must then complete before the target's first SDLC activity. An explicit human may request reassessment at any time. Reassess after a material change that may affect applicability, including a relevant change to source-framework Masters or assessment/governance mechanisms; project requirements/scope, architecture, stack, repository/workspace boundaries or instructions; integrations, security/access controls, CI/testing, deployment or operations; or another declared input on which the prior result depended.

At invocation, state whether this is an initial, explicit reassessment, or material-change reassessment and identify the trigger. Reuse prior evidence only when source and target identities, fingerprints, scope, and applicability match and no material trigger invalidates that dimension. Otherwise reassess affected dimensions; use a complete reassessment when changed assumptions or scope affect the whole conclusion. Do not impose automatic time-based repetition or automatic invocation.

## 4. Assessment dimensions

Evaluate applicability from evidence, state why each dimension applies or does not apply, and cover at least:

1. Repository/workspace configuration, roots, ownership, checkout/worktree, and cross-repository boundaries.
2. Product requirements, architecture, technology stack, constraints, and project-specific instructions.
3. Compatibility and authorized use of Agents, Skills, Prompts, Requests, scripts, and workflows.
4. Governance lifecycle, human decisions/approvals, traceability, record ownership, and persistence authorization.
5. Security, privacy, access controls, and project-specific risk controls.
6. Testing/quality, CI/CD, deployment, and operational requirements.
7. AI-specific controls, evaluation, retrieval, and tool execution, where applicable.
8. Runtime/integration behavior that static evidence cannot establish.

Do not infer universal support from one project or technology. Identify assumptions, exclusions, confidence limits, and evidence needed to resolve uncertainty.

## 5. Assessment determinations and possible blockers

For each applicable dimension and overall, use only:

- `VERIFIED COMPATIBILITY` — evidence supports applicability within the stated scope and revision.
- `COMPATIBILITY WITH IDENTIFIED ADAPTATION` — use appears feasible subject to listed, unimplemented adaptations and decisions.
- `INCOMPATIBILITY / POSSIBLE BLOCKING CONDITION` — evidence supports a material incompatibility or risk that may warrant blocking project progression.
- `UNVERIFIED / INSUFFICIENT EVIDENCE` — evidence cannot establish the conclusion.
- `NOT APPLICABLE` — explain why.

The report recommends whether a possible blocking condition appears to apply. A human authorized for the target project explicitly decides whether it applies to that project. The AI must not make or record that human decision on the human's behalf. Record the actual attributable decision and scope with assessment evidence; do not label it Human Requirement Approval, Human Plan Approval, Human Acceptance, or Corrective Change Approval. Until a recommended possible blocker has an explicit human disposition, the safe recommendation is to hold the first SDLC activity or next affected activity; this is not an automatic AI block decision.

## 6. Concern classification and routing

Classify each material concern as one of:

- `FRAMEWORK GOVERNANCE DEFECT CANDIDATE`: preserve evidence and refer to Governance Audit evaluation. Only a finding established by an authorized finding source enters Finding Investigation and Governance Remediation. An assessment report alone does not create an Audit finding.
- `FRAMEWORK CAPABILITY ENHANCEMENT`: preserve as a non-finding and route to the separately authorized human-requested enhancement path, including Corrective Change Decision when applicable.
- `TARGET-PROJECT ADAPTATION`: document the target-specific decision/adaptation; refer to its authorized owner/process. Do not modify the target.
- `TARGET REQUIREMENT / ARCHITECTURE GAP`: refer to applicable Requirement Analysis/Update and human decision/approval. Do not decide product behavior.
- `INTEGRATION / RUNTIME UNCERTAINTY`: identify bounded evidence or authorized tests required; do not claim success from static inspection.
- `INSUFFICIENT EVIDENCE / UNRESOLVED HUMAN DECISION`: identify the precise gap and stop dependent conclusions.

For every concern record evidence, impact, verification status, affected source/target scope, recommendation, owner/next process, and required approvals. A target-project gap is not automatically a framework defect.

## 7. Evidence and report

Separate source-inspection, executed, reported, and unverified evidence. Identify request/trigger; source-framework and target identity/revision/scope; separate source/target evidence inventories; dimension applicability/determinations; classified concerns; adaptations/possible blockers; uncertainty/limitations; human blocker decision (pending if absent); traceable next process/approvals; and reassessment conditions. Bind report/result to stable work/attempt identities and source/target fingerprints where feasible under the existing persistence contract. Do not copy sensitive target data unnecessarily.

## 8. Read/write and invocation boundaries

Do not automatically invoke another Agent, activate the SDLC Process Orchestrator, initiate product work, change either repository, create product artifacts, or claim approval. Execution beyond read-only inspection requires separate explicit bounded authorization and its applicable process. Persistence permission covers only this actor's records in an explicitly authorized scope; it does not authorize target writes. Preserve user changes. No commit or push.

## 9. Completion

Complete only when each in-scope dimension has a determination or evidence blocker, source and target context are separate, material concerns have a classification and next process, and recommended blockers are presented for explicit human disposition. Publish only authorized process-owned records. Stop before another governed process or implementation. A human decision to proceed is not product Requirement/Plan approval or acceptance.
