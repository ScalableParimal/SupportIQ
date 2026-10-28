# Implementation Planning Guidelines

## 1. Purpose

Define how AI must create an implementation plan from an approved requirement while using the actual repository as implementation context.

These guidelines govern **planning**, not requirement discovery and not implementation.

Requirement analysis is governed by:

`docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md`

Requirement updates are governed by:

`docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md`

---

## 2. Preconditions

Before creating the plan:

1. Identify the approved requirement document.
2. Confirm whether the requirement is explicitly approved.
3. Inspect the repository structure and relevant existing code.
4. Identify existing architecture, project references, conventions, dependencies, and test setup.
5. Identify any additional approved technical decisions or constraints.

Do not create an implementation plan from an unapproved or materially unresolved requirement.

If a material requirement or technical decision is unresolved, surface it rather than silently deciding it.

---

## 3. Sources of Authority

Use the following priority:

```text
Approved Requirement
        ↓
Approved Technical Decisions / Constraints
        ↓
Existing Repository Architecture and Conventions
        ↓
AI Technical Recommendations
```

AI recommendations must remain identifiable as recommendations unless explicitly approved.

Do not allow repository conventions to silently override an explicit approved requirement.

If the requirement conflicts with the existing architecture or repository conventions, identify the conflict and propose the minimum necessary resolution for human review.

---

## 4. Repository Analysis

Before planning implementation, inspect the relevant repository.

Where applicable, examine:

- Solution/project structure
- Project references
- Layer boundaries
- Existing source files
- Existing API conventions
- Application/service patterns
- Domain patterns
- Infrastructure/data-access patterns
- Database configuration
- Frontend structure
- HTTP client/service patterns
- Package/dependency versions
- Configuration conventions
- Existing test projects
- Test frameworks and conventions
- Build/run conventions
- Existing documentation relevant to the feature

Do not assume that a pattern exists simply because it is common in the technology stack.

Use the actual repository as evidence.

---

## 5. Architecture Fit

The plan must fit the existing approved architecture.

For each affected layer, identify the work required and respect its responsibility.

Do not:

- Introduce unnecessary layers.
- Introduce unnecessary packages.
- Move responsibilities between layers without justification.
- Create circular dependencies.
- Make a layer depend on a layer it should remain independent from.
- Expose infrastructure implementation details through higher layers unnecessarily.

If a change to architecture is genuinely required, identify it explicitly as an architectural decision and explain why.

---

## 6. Requirement-to-Plan Traceability

Every meaningful approved requirement must be traceable to implementation work and verification.

Use:

```text
Requirement
    ↓
Business Rule / Contract
    ↓
Implementation Task
    ↓
Test / Verification Evidence
```

Assign unique, stable Plan-local task identifiers to work that will be executed and tracked. Qualify task references by Plan identity and version, following section 28 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md.

Traceability identifiers must not be presented as new business requirements.

A requirement that has no implementation or verification coverage must be identified.

A planned task that cannot be traced to an approved requirement, approved technical constraint, repository need, or necessary verification should be identified as a possible scope concern.

## 6.1 Execution Record Traceability

The Implementation Plan defines approved implementation work. Ordinary execution progress must be recorded in existing governed process records according to section 30.1 of SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md, without informally changing approved task definitions.

Planning output must identify the Plan and source Requirement versions, task identifiers, completion criteria, and prerequisite references. When revising a Plan, provide the task-impact mapping required by the master change-control rules. A retained-work disposition does not establish current verification.

---

## 7. Planning Scope

Plan only the approved feature.

Clearly distinguish:

### In Scope

Work required to implement the approved requirement.

### Out of Scope

Functionality explicitly excluded by the requirement or approved decisions.

### Deferred / Undecided

Work that has been discussed but is not approved.

Do not add "nice-to-have" functionality.

Do not expand the requirement because a broader implementation would appear more complete.

---

## 8. Task Design

Implementation tasks should be:

- Specific
- Actionable
- Traceable
- Ordered by dependency
- Assigned to the appropriate project/layer
- Small enough to implement and verify
- Clear about expected behavior

Avoid vague tasks such as:

> Implement customer management.

Prefer tasks that identify the concrete implementation responsibility.

Each task should answer, where applicable:

- What must be changed?
- Where should it be changed?
- Why is the change required?
- What requirement does it satisfy?
- What dependency must exist first?
- How will it be verified?

---

## 9. Task Ordering and Dependencies

Organize tasks in a logical dependency order.

Typical ordering may be:

```text
Repository / Convention Verification
        ↓
Domain
        ↓
Application
        ↓
Infrastructure / Database
        ↓
API
        ↓
Frontend
        ↓
Integration / End-to-End Verification
```

This is only a planning pattern, not a mandatory sequence.

Adapt the order to the actual repository and feature.

Identify tasks that can safely be performed independently or in parallel when useful, but do not create artificial parallelism.

For tasks or features that may overlap, assess logical task and feature prerequisites and relevant shared change surfaces in the repository/checkout context, including files/components, APIs/contracts, schemas/migrations, configuration, and integration dependencies. Identify known related active or planned work and its checkout/worktree context.

Absence of a declared dependency is not evidence that work is independent or safe to run concurrently. If relevant dependencies or change surfaces are unknown or unassessed, concurrency safety is not established; sequence or serialize the affected work until it is assessed.

Record an explicit execution mode: read-only analysis/planning may overlap only where existing process boundaries and distinct output scopes permit; implementation writes in one shared checkout must be serialized by one Orchestrator; concurrent implementation writes require isolated worktrees and an explicit integration/reconciliation step before the work is combined and verified.

---

## 10. Data and Contract Planning

Where the requirement involves data or interfaces, plan the affected contracts explicitly.

Consider, where applicable:

- Request models
- Response models
- Domain entities
- Persistence models
- Validation
- Database schema
- Constraints
- Relationships
- API endpoints
- HTTP status behavior
- Search/filter behavior
- Pagination
- Error contracts
- Frontend types
- Client/service methods

Do not invent fields, endpoints, statuses, validation rules, or contracts that are not supported by the approved requirement or explicitly approved technical decisions.

If a contract detail is necessary for implementation but not defined, flag it as an open decision rather than silently inventing it.

---

## 11. Database Planning

When database changes are required, identify:

- Schema changes
- Entity mapping
- Constraints
- Indexes where justified
- Migrations
- Data migration needs
- Persistence behavior
- Integration-test requirements

Do not add indexes, tables, constraints, or migrations without a requirement, repository need, or technical justification.

Avoid optimizing based only on speculation.

---

## 12. Testing and Verification Strategy

The plan must include verification appropriate to the affected layers.

Consider:

```text
Domain
  → Unit tests

Application
  → Unit tests

Infrastructure / Database
  → Integration tests

API
  → API/integration tests

Frontend
  → Appropriate component/workflow tests

End-to-End
  → Final user-visible behavior verification
```

Use the repository's existing testing conventions where available.

Do not automatically introduce a new test framework or testing library if an existing project convention can be used.

Tests should verify behavior required by the approved requirement, not merely implementation details.

---

## 13. Non-Functional and Cross-Cutting Concerns

Consider only concerns relevant to the approved feature, such as:

- Security
- Authorization/authentication
- Performance
- Scalability
- Reliability
- Concurrency
- Data integrity
- Logging
- Error handling
- Observability
- Configuration
- Deployment
- Compatibility

Do not invent non-functional targets.

If a material non-functional requirement is missing, identify it as a requirement decision rather than silently creating a target.

---

## 14. Technical Decisions

For technical choices, distinguish:

### Existing Convention

Already established by the repository.

### Approved Technical Decision

Explicitly approved by the human.

### Required Technical Consequence

A technical consequence necessary to satisfy an approved requirement.

### AI Recommendation

A proposed approach that still requires human approval when it materially affects architecture, behavior, cost, security, or scope.

Do not disguise recommendations as mandatory implementation tasks.

---

## 15. Dependencies, Risks, and Open Decisions

Identify relevant:

- Internal dependencies
- External dependencies
- Environment requirements
- Database dependencies
- Configuration requirements
- Technical risks
- Open technical decisions

Do not turn speculative risks into blockers.

Classify meaningful unresolved items as:

- Blocking
- Important
- Minor

A blocking decision must be resolved before implementation can safely begin.

---

## 16. Avoid Over-Engineering

The plan should use the simplest architecture and implementation that satisfies the approved requirement and repository conventions.

Avoid introducing:

- Unnecessary abstractions
- Generic frameworks
- Additional layers
- Additional packages
- CQRS/MediatR-style patterns without need
- Generic repositories without need
- Premature caching
- Premature optimization
- Unrequested infrastructure
- Unrequested integrations

Technical sophistication is not a requirement by itself.

---

## 17. Implementation Boundaries

The plan must preserve established architectural boundaries.

For each task, identify the appropriate project/layer.

Do not plan implementation that causes:

- Domain → Infrastructure dependency
- Domain → API dependency
- Application → Infrastructure dependency when the architecture requires independence
- Application → API dependency
- Infrastructure-specific types leaking into business contracts
- Presentation components directly owning infrastructure concerns

Use the repository's actual architecture as the authority.

---

## 18. Configuration and Secrets

When configuration is required:

- Identify the configuration requirement.
- Follow existing repository configuration conventions.
- Keep secrets out of source code.
- Identify environment-specific configuration where applicable.
- Include setup/verification tasks when necessary.

Do not create or expose real credentials in the plan.

---

## 19. Plan Validation

Before presenting the plan, perform a final review:

- [ ] Approved requirement is the source of functional scope.
- [ ] Repository structure and conventions were inspected.
- [ ] Architecture boundaries are preserved.
- [ ] Every meaningful requirement has implementation coverage.
- [ ] Every important behavior has verification coverage.
- [ ] No unapproved functionality was added.
- [ ] No AI recommendation was silently treated as an approved decision.
- [ ] Tasks are actionable and appropriately scoped.
- [ ] Dependencies and ordering are logical.
- [ ] Data/API/database changes are consistent.
- [ ] Testing strategy is adequate.
- [ ] Relevant risks/open decisions are identified.
- [ ] Out-of-scope functionality is protected.
- [ ] No unnecessary packages/layers/architecture were introduced.
- [ ] Plan does not contain implementation code.
- [ ] Plan is implementable without unresolved material decisions.
- [ ] Plan and source Requirement references identify their exact versions.
- [ ] Executed task identifiers are unique and stable.
- [ ] Task completion criteria and prerequisite references are explicit.
- [ ] A revised Plan includes the required task-impact dispositions.

---

## 20. Standard Implementation Plan Structure

Unless the project has an established plan format, use:

```text
# Implementation Plan

## 1. Status and Scope
- Plan identity and version
- Source requirement identity, version, and approval evidence reference
- Approval status
- Feature scope
- Out of scope

## 2. Repository / Architecture Context
- Existing architecture
- Relevant conventions
- Affected projects/layers

## 3. Technical / Contract Decisions
- Approved decisions
- Required technical consequences
- Open decisions

## 4. Implementation Phases and Tasks
### Phase 1
### Phase 2
### ...

Each task should have:
- Task ID
- Description
- Target project/layer
- Requirement reference
- Prerequisite task IDs and external prerequisites where relevant
- Observable completion criteria

## 5. Concurrency and Integration
- Relevant related tasks/features and repository/checkout/worktree context
- Assessed logical prerequisites and shared change surfaces
- Approved execution mode and its scope
- Required integration/reconciliation activities and post-integration verification

## 6. Testing and Verification
- Unit tests
- Integration tests
- API/frontend verification
- End-to-end verification

## 7. Requirement Traceability
| Requirement | Implementation Tasks | Verification |
|-------------|----------------------|--------------|

## 8. Risks / Dependencies / Open Decisions
...

## 9. Explicitly Out of Scope
...

## 10. Plan Validation
...

## 11. Approval Status
Draft / Ready for Human Review Approval / Approved
```

---

## 21. Approval Status

The AI must distinguish:

- **Draft Implementation Plan** — planning work is still being refined.
- **Ready for Human Review Approval** — plan validation and complete Implementation Plan Verification are complete, and all required verification findings and decisions are resolved. This status is not Human Plan Approval.
- **Approved Implementation Plan** — only after required Human Review Approval and separate explicit Human Plan Approval.

AI must never mark the plan as approved by itself.

Implementation must not begin from an unapproved or superseded plan. Implementation must use the current approved Implementation Plan.

---

## 22. Planning vs Implementation

Creating the plan is a read/analyze/design activity.

During planning:

- Do not modify application source code.
- Do not implement tasks.
- Do not create migrations.
- Do not change database schema.
- Do not modify frontend/backend behavior.
- Do not create implementation files unless explicitly requested as part of planning artifacts.

The output is the implementation plan.

---

## Final Principle

> **The implementation plan translates an approved requirement into traceable, repository-aligned implementation work. It must not redefine the requirement or silently introduce architecture, scope, or technical decisions that have not been approved.**

The controlling sequence is:

```text
Approved Requirement
        +
Actual Repository
        ↓
Repository / Architecture Analysis
        ↓
Implementation Design
        ↓
Tasks + Dependencies
        ↓
Testing + Verification
        ↓
Traceability
        ↓
Candidate Implementation Plan
        ↓
Plan Validation
        ↓
Independent Implementation Plan Verification
        ↓
Resolve Verification Findings / Decisions
        ↓
Human Review Package (current plan; prior decisions and approvals; completed changes with reasons; unresolved items)
        ↓
Human Review Approval (required; authorizes only progression to Human Plan Approval)
        ↓
Human Plan Approval
        ↓
Approved Implementation Plan
        ↓
Implementation
```

After complete verification of the current Implementation Plan and resolution of all required verification findings and decisions, the Human Review package must present the current plan; prior decisions and approvals; completed changes with their reasons; and any other unresolved items with their status. Human Review Approval is a required manual human gate. It authorizes only progression to separate Human Plan Approval. It does not approve the plan, authorize implementation, waive unresolved required findings, or replace any Human Approval required before applying a corrective change. Human Plan Approval remains separate and alone authorizes implementation against the current approved plan.
