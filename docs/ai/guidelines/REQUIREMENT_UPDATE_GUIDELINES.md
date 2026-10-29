# Requirement Update Guidelines

## 1. Purpose

Define how AI must safely update an existing requirement after the human has answered analysis questions and approved relevant recommendations or clarifications.

These guidelines govern **applying approved decisions to the requirement**. Requirement discovery and analysis are governed by:

`docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`

---

## 2. Required Inputs

Before updating, AI must have:

1. The current approved Requirement version and its version ID and SHA-256.
2. The relevant analysis findings/questions, where applicable.
3. The human's answers and explicit decisions.
4. Any recommendations explicitly approved by the human.
5. The subject type: Finding-led corrective update or human-requested, non-finding Requirement amendment. For a non-finding request, use the existing request record and establish its source, scope, decision authority, disposition, and rationale under SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8.
6. The affected Requirement IDs and the request details required by SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 8, where applicable.

If a material decision is still unresolved, do not silently decide it.

---

## 3. Decision Authority

Apply this priority:

```text
Explicit Human Decision
        ↓
Existing Valid Requirement
        ↓
Approved Clarification / Constraint
        ↓
AI Recommendation
```

AI recommendations, observations, and assumptions are **not requirements** unless explicitly approved.

If a human answer is itself ambiguous, ask for clarification instead of interpreting it.

---

## 4. Preserve Existing Requirements

The update is normally an **incremental change**, not a rewrite.

AI must:

- Preserve valid existing requirements.
- Preserve existing terminology and structure where practical.
- Change only what is necessary to incorporate approved decisions.
- Avoid rewriting unrelated sections.
- Avoid removing information that remains valid.

Use the **minimum necessary change** principle.

---

## 5. Apply Approved Decisions Completely

When a human decision changes a requirement:

1. Update the directly affected statement.
2. Check other sections affected by the same decision.
3. Update related business rules, validation, scope, acceptance criteria, or contracts where applicable.
4. Remove or revise statements that are now superseded.
5. Ensure the final document describes one consistent behavior.

Do not update only the sentence where the original question appeared if the decision has wider consequences.

---

## 6. Recommendations and Assumptions

### Approved Recommendation

Incorporate only the approved portion.

### Rejected Recommendation

Do not incorporate it.

### Unanswered Recommendation

Do not incorporate it.

### Existing Assumption

After human decisions:

- Replace it with an explicit requirement if the behavior was approved.
- Remove it if rejected.
- Keep it explicitly identified if it remains unresolved and material.

Never silently convert an assumption into an approved requirement.

---

## 7. Conflicts and Superseded Requirements

If an approved decision changes an existing Requirement:

- Never revise, overwrite, edit in place, or remove the source Requirement version.
- Create a new, separately identifiable immutable Requirement version under `docs/requirement/` and bind it to the source version using the metadata and verification required by SDLC_ARTIFACT_GOVERNANCE.md section 8.4.
- Check dependent statements in the new version, remove contradictions from that version, and preserve unrelated requirements.
- Record status changes in the existing governed process records; do not mutate the frozen Requirement bytes to change a status.

If it is unclear whether the human intended to change an existing Requirement, ask before creating a new version. Creating a version does not approve it. The resulting version remains subject to complete Requirement Analysis Verification and Human Requirement Approval. The final version must not contain two contradictory statements describing the same behavior.

---

## 8. Scope Control

Do not expand scope during the update.

Maintain:

- **In Scope** — explicitly approved functionality.
- **Out of Scope** — explicitly excluded functionality.
- **Deferred / Undecided** — not yet approved.

Do not add "helpful" features, technical enhancements, or speculative functionality.

---

## 9. Business Requirement vs Implementation

Keep the requirement focused on **what the system must do**.

Do not introduce implementation details such as:

- Specific classes or methods
- Repository names
- ORM APIs
- Framework-specific code
- Internal file structure
- Database implementation details

unless they are explicitly approved technical constraints that belong in the requirement.

For example:

> Customer email must be unique.

is a business/data requirement.

> Create a SQL Server unique index on Email.

is normally an implementation-plan decision.

---

## 10. Consistency Review

After applying all approved decisions, perform a second-pass review.

Verify:

- Requirements are internally consistent.
- Business rules remain consistent.
- Scope remains correct.
- Validation remains aligned.
- Data/contract expectations remain aligned where applicable.
- Acceptance criteria reflect the final behavior.
- Dependencies and constraints remain accurate.
- No unresolved material decision was silently resolved.
- No unapproved AI recommendation was introduced.
- No unrelated requirement was changed.

---

## 11. Requirement Quality

The updated requirement should be:

- Clear
- Unambiguous
- Testable
- Implementable
- Internally consistent
- Consistent in terminology
- Explicit about important scope boundaries

Do not invent numerical targets, business rules, fields, behaviors, or constraints that were not provided or approved.

---

## 12. Change Summary

After updating, provide a concise summary containing:

### Added
New approved requirements.

### Modified
Existing requirements changed by approved decisions.

### Removed / Superseded
Requirements replaced or made obsolete by approved decisions.

### Scope
Any approved scope changes.

### Remaining Open Questions
Material decisions still unresolved.

### Assumptions
Material assumptions that remain.

The summary must describe the actual changes; do not claim changes that were not made.

---

## 13. Approval Status

AI must distinguish:

- **Draft Updated Requirement** — changes have been applied but human approval is pending.
- **Ready for Human Review** — consistency validation is complete and the document is ready for review.
- **Approved Requirement** — only when the human has explicitly approved it.

AI must never label the requirement "Approved" on its own.

---

## 14. File Modification Rules

When explicitly asked to update a Requirement:

- Create only the new immutable Requirement version required for the approved update under `docs/requirement/`; do not modify, overwrite, or remove the source or any previously created version.
- Bind the new version and source version using the existing process records and metadata required by SDLC_ARTIFACT_GOVERNANCE.md section 8.4. Record status changes in those records, not in the frozen Requirement bytes.
- Modify no other Requirement artifact or product artifact without separate authorization. Own-output record publication is permitted only under section 33.1 of SDLC_ARTIFACT_GOVERNANCE.md and section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md; it does not authorize additional substantive artifact changes.
- Do not modify source code.
- Do not create an implementation plan unless explicitly requested.
- Do not create tests.
- Do not modify unrelated documentation.
- Do not modify the AI guidelines or prompts.

If the user requests only a proposed update/draft, do not create or modify any Requirement version.

---

## 15. Final Validation Checklist

Before presenting the updated requirement:

- [ ] Correct requirement document was updated.
- [ ] All relevant human decisions were incorporated.
- [ ] Only approved recommendations were incorporated.
- [ ] Valid existing requirements were preserved.
- [ ] Superseded statements were revised.
- [ ] No contradictions remain.
- [ ] Scope is correct.
- [ ] Business rules are consistent.
- [ ] Acceptance criteria are aligned, where applicable.
- [ ] No material assumption was silently converted into a requirement.
- [ ] No unrelated content was changed.
- [ ] No unnecessary implementation detail was introduced.
- [ ] Remaining open questions are identified.
- [ ] Approval status is clearly stated.

---

## 16. Standard Update Workflow

Requirement Update applies approved human decisions and prepares the updated Requirement. It does not replace Requirement Analysis or Requirement Analysis Verification, and it does not itself constitute Human Requirement Approval or mark the Requirement approved.

```text
Current Requirement
        ↓
Analysis Findings
        ↓
Human Decisions
        ↓
Apply Approved Decisions
        ↓
Update Affected Sections
        ↓
Consistency Review
        ↓
Final Validation
        ↓
Create new immutable Requirement version and verify source preservation/read-back
        ↓
Change Summary
        ↓
Requirement Analysis
        ↓
Complete Requirement Analysis Verification
        ↓
Resolve Findings / Decisions
        ↓
Human Requirement Approval
        ↓
Approved Requirement = Source of Truth
        ↓
Plan Impact Evaluation
        ↓
Implementation Planning / Plan Update as Required
        ↓
Implementation Plan Verification as Required
        ↓
Resolve Plan Verification Findings / Decisions as Required
        ↓
Human Review Approval as Required
        ↓
Human Plan Approval as Required
```

Requirement Analysis Verification is separate from Human Requirement Approval. The updated Requirement becomes the approved source of truth only after explicit Human Requirement Approval. After Requirement Approval, Plan Impact Evaluation is required. Follow the applicable Implementation Planning / Plan Update, Implementation Plan Verification, Human Review Approval, and Human Plan Approval processes as required. After required plan verification and resolution of findings and decisions, Human Review Approval is the required gate that precedes separate Human Plan Approval and authorizes only progression to it.

## Final Principle

> **AI may incorporate and clarify approved human decisions, but must not invent, silently decide, or broaden the requirement.**

The requirement becomes the new source of truth only after explicit human approval.