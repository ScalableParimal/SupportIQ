Read and follow:
docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md
Subject Type [FINDING / HUMAN-REQUESTED GOVERNANCE ENHANCEMENT (NON-FINDING)]. For FINDING, complete the Finding Source and Finding Investigation fields below. For a governance enhancement, do not create or imply a finding; complete these separate Enhancement Request fields and identify the non-finding investigation result. RESERVED STABLE WORK ID (per SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 30.1). Enhancement Investigation: [FINDING INVESTIGATION REPORT PATH/RESULT; IDENTIFY AS NON-FINDING; EVIDENCE THAT REQUEST SOURCE, AUTHORIZATION, SCOPE, AFFECTED GOVERNANCE ARTIFACTS, AND CONSTRAINTS WERE ESTABLISHED]. Proposed Governance Amendment: [CANONICAL PROCESS-OWNED REPORT PATH/ID/SHA-256; EXACT PER-FILE CONTENT OR UNAMBIGUOUS DIFF; TARGET PATHS; BASE AND EXPECTED-AFTER SHA-256; SCOPE; EXCLUSIONS; NOT-APPLIED STATE].

Actor and Human Approval fields (enhancement only): for proposal preparer, one-time initial applier [identity/environment/one-time scope], verifier, and reviewer, record the role/Agent definition repository-relative path and content SHA-256, each bound to that actor's own unique attempt record; record current runtime identity/environment separately. Check distinctness using the actor-identity bindings, not display name alone. Different OS identities, hosts, or repositories are not required unless an applicable, explicitly approved security boundary requires them. Qualification evidence [record path/ID/SHA-256 and capability observations]; approval decision/source/time; approved report fingerprint and exact targets. Each Application, Verification, Review, and Audit request must separately record its fresh attributable stage-start instruction; this is not part of or a substitute for patch approval.


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
