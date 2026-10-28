# Implementation Planning Prompt

Read and follow:

`docs/ai/guidelines/IMPLEMENTATION_PLANNING_GUIDELINES.md`

Create an implementation plan for the approved requirement document specified by the user.

Use the actual repository as the implementation context.

The user will provide:
1. The approved requirement document.
2. Any additional approved technical decisions or constraints.

Do not implement anything.

After creating the candidate Implementation Plan, the governed next stages are:

Candidate Implementation Plan
→ Plan Validation
→ Independent Implementation Plan Verification
→ Resolve Verification Findings / Decisions
→ Human Review Package (current plan; prior decisions and approvals; completed changes with reasons; unresolved items)
→ Human Review Approval (required; authorizes only progression to Human Plan Approval)
→ Human Plan Approval
→ Approved Implementation Plan
→ Implementation

After complete verification of the current Implementation Plan and resolution of all required verification findings and decisions, the Human Review package must present the current plan; prior decisions and approvals; completed changes with their reasons; and any other unresolved items with their status. Human Review Approval is a required manual human gate. It authorizes only progression to separate Human Plan Approval. It does not approve the plan, authorize implementation, waive unresolved required findings, or replace any Human Approval required before applying a corrective change. Human Plan Approval remains separate and alone authorizes implementation against the current approved plan.

After creating the plan, report:
- requirement-to-task traceability,
- implementation phases and dependencies,
- concurrency assessment across relevant tasks/features, including dependencies, shared change surfaces, execution mode, and integration/reconciliation requirements; do not infer safety from missing dependency declarations,
- affected projects/layers,
- testing and verification strategy,
- risks/dependencies,
- open technical decisions,
- scope exclusions,
- plan validation result,
- approval status.

Do not mark the implementation plan as approved. Approval remains a human decision.
