# Implementation Prompt

Read and follow:

`docs/ai/guidelines/IMPLEMENTATION_GUIDELINES.md`

Implement the implementation tasks specified by the user.

Use:

- the current approved Requirement as the business source of truth,
- the current approved Implementation Plan as the implementation source of truth,
- the actual repository as the technical context.

Implement only the requested implementation slice.

Task IDs and the requested implementation slice are execution context only and must not override the current approved Requirement or current approved Implementation Plan.

Before implementing, confirm that the required approved Requirement and approved Implementation Plan are available.

Before writing, follow the approved Plan's concurrency/execution mode and the Orchestrator's checkout coordination. Do not perform concurrent writes in a shared checkout; use isolated worktrees and the approved integration/reconciliation step for authorized parallel implementation. If coordination, dependency, or checkout state is unknown, stop and request the required governed assessment.

Do not change the Requirement or Implementation Plan during implementation.

If a Requirement, architecture, Plan, or repository conflict is discovered:

- stop at the affected point,
- explain the conflict and its impact,
- ask for the required human decision,
- do not silently modify the Requirement or Implementation Plan.

If a material deviation from the current approved Requirement or Implementation Plan is required, stop and route it through the governed Finding Investigation and Corrective Change Decision & Plan Update process.

After implementation, perform the implementation self-check defined by the Implementation Guidelines.

After implementation, report:

- tasks implemented,
- files/projects changed,
- tests added or updated,
- test/build results,
- requirement traceability,
- plan traceability,
- deviations,
- unresolved issues,
- implementation self-check status.

Clearly distinguish:

- implementation evidence,
- reported evidence,
- deviations,
- unresolved issues.

Do not mark the implementation as approved or accepted.

Implementation Verification, Implementation Review, and Human Acceptance are separate subsequent stages.