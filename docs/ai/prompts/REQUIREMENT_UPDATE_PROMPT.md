# Requirement Update Prompt

Read and follow:

`docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`

Using those guidelines, update the requirement document specified by the user.

The user will provide:

1. The requirement document to update `<REQUIREMENT_DOCUMENT_PATH>`.
2. The human decisions and approved clarifications to incorporate.
3. The relevant analysis findings/questions being addressed.
4. Any recommendations explicitly approved by the human.

Apply only the decisions explicitly provided by the user.

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