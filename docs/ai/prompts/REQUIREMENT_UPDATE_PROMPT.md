# Requirement Update Prompt

Read and follow:

`docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`

Using those guidelines, update the requirement document specified by the user.

The user will provide:

1. The subject type: Finding-led corrective update or human-requested, non-finding Requirement amendment.
2. The current approved Requirement version path, immutable version ID, and SHA-256.
3. The human decisions and approved clarifications to incorporate.
4. The relevant analysis findings/questions being addressed, where applicable.
5. Any recommendations explicitly approved by the human.
6. For a human-requested non-finding amendment, the existing request details and responsible human decision, including scope, disposition, and rationale, as specified by SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.

Apply only explicit human decisions. Do not invent a Finding for a non-finding request or decide business scope on behalf of the responsible human. Create a new immutable Requirement version under `docs/requirement/`; never overwrite, edit in place, or remove an existing version. Record status changes in the existing process records, not by changing the frozen Requirement bytes. Creating a version does not constitute Human Requirement Approval.

After updating:

- Perform the consistency and validation checks defined in `docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`.
- Provide a concise change summary.
- Identify remaining open questions and assumptions.
- Clearly state the approval status.

After Requirement Update, follow the separate governed stages:

Requirement Update
→ Requirement Analysis
→ Complete Requirement Analysis Verification
→ Resolve Findings / Decisions
→ Human Requirement Approval
→ Approved Requirement = Source of Truth
→ Plan Impact Evaluation
→ Implementation Planning / Plan Update as Required
→ Implementation Plan Verification as Required
→ Resolve Plan Verification Findings / Decisions as Required
→ Human Review Approval as Required
→ Human Plan Approval as Required

Do not treat Requirement Update checks or AI verification as Human Approval.
Do not mark the Requirement as approved. Approval remains a human decision.