Read and follow:
docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md
Subject Type [FINDING / HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING)]. For FINDING, complete the Finding Source and Finding Investigation fields below. For a governance enhancement, do not create or imply a finding; complete these separate Enhancement Request fields and identify the non-finding investigation result. RESERVED STABLE WORK ID (per SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 30.1). Enhancement Investigation: [FINDING INVESTIGATION REPORT PATH/RESULT; IDENTIFY AS NON-FINDING; EVIDENCE THAT REQUEST SOURCE, AUTHORIZATION, SCOPE, AFFECTED GOVERNANCE ARTIFACTS, AND CONSTRAINTS WERE ESTABLISHED]. Proposed Governance Amendment: [CANONICAL PROCESS-OWNED REPORT PATH/ID/SHA-256; EXACT PER-FILE CONTENT OR UNAMBIGUOUS DIFF; TARGET PATHS; BASE AND EXPECTED-AFTER SHA-256; SCOPE; EXCLUSIONS; NOT-APPLIED STATE].

Actor and Human Approval fields (enhancement only; stage-specific): record the proposal preparer, intended one-time initial applier [identity/environment/one-time scope], intended verifier, and intended reviewer by role/Agent definition repository-relative path and content SHA-256. At proposal preparation, bind only the actual preparer to its own current unique attempt and record its current runtime identity/environment and qualification evidence [record path/ID/SHA-256 and capability observations] separately. The intended applier requires fresh exact Human Approval and one-time designation; no separate pre-existing qualification attempt is required. After its separate fresh Application stage-start, the applier must publish and integrity-check its own current attempt, identity, permissions, and role-specific capability evidence before any source write; before Application source work, both preparer and applier must be bound to their own attempts. Record future verifier/reviewer bindings as planned identity-only paths and hashes, not attempts, current runtime identities, capabilities, or stage starts; do not require, create, or publish their attempts before predecessor gates. Only after complete successful Application and a fresh Verification stage-start may the actual verifier publish its own attempt and current qualification; only after passing independent Verification and a fresh Review stage-start may the actual reviewer do so. Each actual verifier/reviewer definition path and hash must match its approved planned binding; mismatch blocks that stage pending updated attributable Human decision and exact approval. Follow the Governance Amendment Application controls for these bindings and gates. Check all four actors' distinctness using actor-identity bindings, not display name alone; the applier must also differ from the SDLC Process Orchestrator and any Governance Remediation actor barred from self-edit in its active cycle. Different OS identities, hosts, or repositories are not required unless an applicable, explicitly approved security boundary requires them. Record the approval decision/source/time, approved report fingerprint, and exact targets without treating approval/designation as capability evidence. Each Application, Verification, Review, and Audit request must separately record its fresh attributable stage-start instruction and each actual actor must qualify in its own current invocation under SDLC_ARTIFACT_GOVERNANCE.md section 33.1; stage-start is not part of or a substitute for patch approval.


Finding Source:
[Requirement Analysis Verification / Implementation Plan Verification / Implementation Verification / Implementation Review / Other]

Affected Artifact:
[Requirement / Requirement Analysis / Implementation Plan / Implementation / Tests / Configuration / Documentation / Other]

Affected Components / Sections:
[List affected components, files, tasks, sections, or artifacts]

Current Approved Requirement (path, version/status, and approval evidence):
`[PATH / VERSION / STATUS / APPROVAL EVIDENCE]`

Current Approved Implementation Plan (path, version/status, and approval evidence, if applicable): [PATH / VERSION / STATUS / APPROVAL EVIDENCE]

Finding Investigation:
[Path or investigation result]

Relevant Architecture / Engineering Guidelines:
[List relevant guidelines]

Observed Evidence:
[Verification results, test results, repository findings, or other evidence]

Additional Context:
[Any additional information relevant to the decision]
The Finding fields above are not applicable to a non-finding enhancement. Never substitute enhancement provenance or proposal authorization for Human Approval of the exact change.
