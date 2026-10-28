# Requirement Analysis Guidelines

## 1. Purpose

This document defines the standard process and rules for AI-assisted requirement analysis.

These guidelines are reusable across features and projects. They define **how AI must analyze requirements**, not the business requirements of any particular feature.

The goal is to produce a clear, complete, consistent, traceable, and human-approved requirement before implementation planning or coding begins.

---

## 2. Role of AI

AI acts as a requirement-analysis assistant.

AI must:

- Understand and structure the requirement.
- Identify missing information, ambiguity, conflicts, and assumptions.
- Extract explicit business rules and constraints.
- Identify scope and boundaries.
- Identify relevant technical and architectural impact without turning recommendations into requirements.
- Ask focused questions when a human decision is required.
- Maintain traceability from requirement to implementation and testing.
- Update the requirement only after the human has made the required decisions.

AI must not independently make unresolved business decisions.

---

## 3. Source-of-Truth Rules

Before analysis begins:

1. Identify the authoritative requirement document.
2. Treat the authoritative document as the primary source of truth.
3. Preserve the terminology used by the requirement unless clarification is necessary.
4. If multiple sources contain conflicting information:
   - identify the conflict,
   - identify the affected requirement,
   - do not silently choose one,
   - ask the human to resolve it.
5. Do not treat AI recommendations, implementation plans, code, or assumptions as approved requirements unless explicitly approved by the human.

---

## 4. Requirement Understanding

First understand what the requirement actually asks for.

Identify, where applicable:

- Business objective
- Actors/users
- Functional requirements
- Business rules
- Inputs
- Outputs
- Expected behavior
- Validation rules
- Error/exception scenarios
- Data requirements
- Integration requirements
- Non-functional requirements
- Constraints
- Dependencies
- Scope boundaries

Do not introduce functionality merely because it appears technically useful.

---

## 5. Completeness Analysis

Check whether the requirement contains enough information to be implemented without making significant business assumptions.

Look for missing information related to:

- Required fields
- Optional fields
- Validation
- Business rules
- Workflow/state transitions
- Error behavior
- Permissions/security
- Data ownership
- External integrations
- Performance expectations
- Pagination/filtering/sorting
- Concurrency
- Audit requirements
- Failure scenarios

Only raise gaps that are relevant to the requested feature.

Classify findings as:

- **Blocking** — implementation cannot safely proceed without a decision.
- **Important** — implementation can proceed only with a reasonable risk or requires clarification.
- **Minor** — useful clarification but unlikely to block implementation.

---

## 6. Ambiguity Detection

Identify statements that can reasonably have more than one interpretation.

For each ambiguity:

1. Quote or reference the relevant requirement.
2. Explain the possible interpretations.
3. Explain the implementation/business impact.
4. Ask a focused question.
5. Do not silently select an interpretation.

Example:

> "Search customers by name"

Possible ambiguity:

- Exact match
- Partial match
- Case-sensitive
- Case-insensitive

Ask for the intended behavior before finalizing the requirement.

---

## 7. Conflict Detection

Check for contradictions:

- Within the same requirement document.
- Between different sections of the requirement.
- Between requirement statements and stated constraints.
- Between the current requirement and explicitly approved decisions.

When a conflict is found:

- State both conflicting statements.
- Explain the conflict.
- Identify what is affected.
- Ask the human to resolve it.

Do not resolve business conflicts based on personal preference.

---

## 8. Business Rule Extraction

Explicitly identify business rules that must remain true.

Examples include:

- Uniqueness
- Allowed states/statuses
- Required fields
- Validation limits
- State transitions
- Relationships
- Business constraints
- Calculation rules

Distinguish:

- **Explicit rule** — directly stated in the requirement.
- **Derived rule** — logically required by an explicit requirement.
- **Recommendation** — a proposed approach that requires human approval.

Never present a recommendation as an approved business rule.

---

## 9. Scope and Boundaries

Clearly separate:

### In Scope

Functionality explicitly required or explicitly approved.

### Out of Scope

Functionality explicitly excluded.

### Deferred / Undecided

Functionality discussed but not yet approved.

Do not expand scope because AI believes the feature would be more complete with additional functionality.

Avoid speculative features and unnecessary architecture.

---

## 10. Assumption Handling

AI must not hide assumptions.

When an assumption is necessary:

- State it explicitly.
- Explain why it is needed.
- Identify its impact.
- Ask for confirmation if it materially affects behavior, architecture, data, security, or testing.

Use clear terminology such as:

> Assumption — requires confirmation

Do not convert an assumption into an approved requirement without human confirmation.

---

## 11. Technical and Architectural Impact

After understanding the business requirement, identify its technical impact.

Consider:

- API impact
- Application/service-layer impact
- Domain impact
- Infrastructure/data-access impact
- Database impact
- Frontend impact
- Integration impact
- Testing impact
- Security impact
- Performance/scalability impact

Keep this analysis separate from the business requirement.

A technical recommendation is not automatically a requirement.

Avoid over-engineering. Recommend the minimum architecture needed to satisfy the approved requirement and existing project architecture.

---

## 12. Traceability

Maintain a clear relationship:

```text
Requirement
    ↓
Business Rule
    ↓
Implementation Task
    ↓
Test
    ↓
Verification
```

Every implementation decision should be traceable to:

- an explicit requirement,
- an approved clarification,
- or an explicitly approved technical decision.

If something cannot be traced to one of these, identify it rather than silently introducing it.

---

## 13. AI Questions

Questions to the human must be:

- Specific
- Necessary
- Actionable
- Limited to decisions that materially affect the requirement

Avoid asking questions whose answers can be directly determined from the requirement.

Group related questions when possible.

For each question, explain why the decision matters when the impact is not obvious.

Do not overwhelm the human with speculative questions.

---

## 14. Requirement Update Rules

The initial analysis is **read-only**.

AI must not modify the authoritative requirement during the analysis phase.

The sequence is:

```text
Source Requirement
    ↓
Initial Requirement Analysis
    ↓
AI Questions
    ↓
Human Decisions
    ↓
Updated Requirement
    ↓
Post-Requirement-Update Requirement Analysis / Analysis Refresh
    ↓
Requirement Analysis Verification
    ↓
Resolve Verification Findings / Decisions
    ↓
Human Requirement Approval
```

Only after the human has resolved the identified questions should AI prepare an updated requirement. Following a Requirement Update, perform Requirement Analysis or refresh the analysis against the resulting updated Requirement before complete Requirement Analysis Verification.

The updated requirement must then be independently verified against the authoritative source requirement before it is presented for final human approval.

Requirement Analysis Verification is a separate verification activity. It does not constitute human approval of the requirement.

If the verification identifies findings, ambiguities, inconsistencies, or decisions that require resolution, those items must be resolved before the requirement is presented for final human approval.

When updating:
- Preserve existing valid requirements.
- Incorporate approved decisions.
- Remove or revise superseded statements only when appropriate.
- Do not add unapproved functionality.
- Keep terminology consistent.
- Keep scope explicit.
The updated requirement becomes the new source of truth only after human approval.
---

## 15. Human Approval Gates

Human approval is required at these points:

### Gate 1 — Requirement Approval

Human approves the updated/final requirement after Requirement Analysis Verification has been completed and all material verification findings, ambiguities, conflicts, and required decisions have been resolved.

Only after this approval does the finalized requirement become the approved source of truth for implementation planning.

### Gate 2 — Implementation Plan Approval

A separate implementation plan is created from the approved requirement.

The implementation plan must be independently verified before human approval.

After complete verification and resolution of required findings and decisions, Human Review Approval is required; it authorizes only progression to separate Human Plan Approval. Human approves the implementation plan through that separate Human Plan Approval before implementation begins.

### Gate 3 — Implementation Acceptance

Implementation proceeds only from the approved requirement and approved implementation plan.

After implementation verification and implementation review are completed, human acceptance is required before the implementation is considered accepted.

The AI must not treat analysis output, verification output, recommendations, or implementation review results as human approval.

---

## 16. Prohibited AI Behaviors

AI must not:

- Invent business requirements.
- Silently resolve ambiguity.
- Silently resolve conflicts.
- Convert recommendations into requirements.
- Expand feature scope without approval.
- Introduce speculative functionality.
- Modify the requirement during read-only analysis.
- Start implementation before the required approval gate.
- Assume a technical implementation is a business requirement.
- Duplicate requirements unnecessarily.
- Over-engineer the solution.
- Ignore existing project architecture or approved constraints.
- Treat generated code as proof that a requirement was correct.
- Treat Requirement Analysis Verification as human approval.
- Treat verification findings as resolved without the required resolution or human decision.

---

## 17. Standard Analysis Workflow

Use this workflow for every requirement-analysis exercise:

### Phase 1 — Identify Source

- Locate the authoritative requirement.
- Identify any supporting documents.
- Establish source priority.

### Phase 2 — Understand

- Summarize the objective.
- Identify actors, behavior, data, rules, constraints, and scope.

### Phase 3 — Analyze

Check:

- Completeness
- Ambiguity
- Conflicts
- Business rules
- Assumptions
- Scope
- Dependencies
- Technical impact

### Phase 4 — Questions

Produce only the questions that require human decisions.

### Phase 5 — Human Decisions

Wait for the human to resolve the questions.

### Phase 6 — Update Requirement

Prepare the revised requirement using the approved decisions.

This phase is performed through the separate Requirement Update process (see `REQUIREMENT_UPDATE_GUIDELINES.md`), only when the human has explicitly requested the update and supplied the approved decisions. It does not authorize modifying the authoritative requirement during the initial analysis, and it does not constitute Human Requirement Approval.

### Phase 7 — Post-Requirement-Update Requirement Analysis / Analysis Refresh

After the Requirement is updated, analyze or refresh the Requirement Analysis against the resulting updated Requirement and the approved decisions. This post-update analysis is required before complete Requirement Analysis Verification.

### Phase 8 — Requirement Analysis Verification

Independently verify the complete current requirement analysis and updated requirement against the authoritative source requirement.

Check whether:

- The requirement analysis correctly represents the source requirement.
- All approved human decisions have been incorporated.
- Identified ambiguities, conflicts, and gaps have been appropriately resolved.
- No unapproved requirements or functionality have been introduced.
- Scope and boundaries remain consistent.
- Business rules remain consistent.
- Assumptions are explicitly identified.
- The updated requirement remains implementation-neutral.
- The requirement is complete enough to proceed to implementation planning.

### Phase 9 — Resolve Verification Findings / Decisions

If Requirement Analysis Verification identifies findings, ambiguities, contradictions, missing information, or decisions requiring resolution:

- Identify the affected requirement or analysis item.
- Determine whether human input is required.
- Obtain the required human decision when applicable.
- For routine clarification or decision resolution, update the requirement or analysis only using the applicable approved human decision.
- For routine clarification or decision resolution, update the requirement or analysis only through its applicable authorized update process, using the applicable approved human decision.
- Re-run Requirement Analysis Verification when the change materially affects the verified content.

Do not proceed to human requirement approval while material verification findings remain unresolved.

Material findings affecting a governed artifact must not be corrected directly through Requirement Analysis or Requirement Analysis Verification. Route them through:

Finding
→ Finding Investigation
→ Corrective Change Decision & Plan Update
→ Required Human Approval
→ Apply Approved Change
→ Required Verification

Requirement Analysis Verification remains read-only and must not apply corrections.

### Phase 10 — Requirement Approval

Wait for explicit human approval of the finalized requirement.

The AI must not interpret verification status as human approval.

### Phase 11 — Handoff

Only after human approval, use the finalized requirement as the source for implementation planning.

---

## 18. Standard Analysis Output

Unless the human requests another format, structure the analysis as:

```text
# Requirement Analysis

## 1. Understanding
- Business objective
- Actors
- Main functionality

## 2. Explicit Requirements
- Functional requirements
- Business rules
- Constraints

## 3. Scope
### In Scope
### Out of Scope
### Deferred / Undecided

## 4. Ambiguities
| ID | Requirement | Ambiguity | Impact |
|----|-------------|-----------|--------|

## 5. Conflicts
| ID | Statements | Conflict | Impact |
|----|------------|----------|--------|

## 6. Missing / Incomplete Information
| ID | Missing Information | Importance | Impact |
|----|---------------------|------------|--------|

## 7. Assumptions
| ID | Assumption | Impact | Confirmation Required |
|----|------------|--------|------------------------|

## 8. Technical Impact
- API
- Application
- Domain
- Infrastructure
- Database
- Frontend
- Testing
- Security
- Performance

## 9. Questions Requiring Human Decision
1. ...
2. ...

## 10. Analysis Conclusion
- Ready for requirement finalization: Yes/No
- Blocking decisions: ...
- Next step: ...
```

---

## 19. Final Principle

The objective of requirement analysis is not to make the requirement look complete by filling gaps with AI assumptions.

The objective is to make the requirement **explicit, unambiguous, bounded, traceable, independently verified, and human-approved** before implementation planning begins.

The controlling sequence is:

```text
Understand
    ↓
Analyze
    ↓
Identify Gaps / Ambiguities / Conflicts
    ↓
Ask Human
    ↓
Human Decides
    ↓
Update Requirement
    ↓
Requirement Analysis Verification
    ↓
Resolve Verification Findings / Decisions
    ↓
Human Approves
    ↓
Create Implementation Plan
