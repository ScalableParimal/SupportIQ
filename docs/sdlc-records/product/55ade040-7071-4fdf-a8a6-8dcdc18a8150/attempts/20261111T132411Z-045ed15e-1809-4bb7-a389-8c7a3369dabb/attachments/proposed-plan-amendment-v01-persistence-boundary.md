# Proposed Plan Amendment - V-01 Persistence Responsibility

## Decision and boundary

This is a proposal only. It preserves approved Requirement v1.11 Section 7: the .NET 8 Web API owns persistence responsibility, while storage-specific persistence implementation is placed behind the distinct persistence boundary. It does not choose a concrete project layout or repository pattern. It does not modify Candidate v0.2. V-02 remains unresolved and is not remediated by this amendment.

## Bound base

- Candidate: `supportiq-product-implementation-plan` v0.2
- Path: `docs/sdlc-records/product/55ade040-7071-4fdf-a8a6-8dcdc18a8150/attempts/20261111T080022Z-6bcfff1e-cee4-4d86-ac38-a9cec718008c/attachments/implementation-plan-supportiq-v1.11-v0.2.md`
- Bytes: 52650
- SHA-256: `77E762C718ABABE40848F2E3C9C78C580DA4C60BF12A464BD0B6D7EECE033BA7`
- Source Requirement: v1.11, SHA-256 `56C9DC9CE23E73C7D23FB1EF52046C3DB007801F3589E7D7029C294D5F79ABBE`

## Exact content replacements

Apply each replacement once to the bound v0.2 content. Text shown in each new block is exact. No other plan content is authorized for change by this proposal.

### 1. Section 2, architecture boundary: Web API responsibility

**Replace:**

```text
- The browser is presentation-only and receives no provider keys or unrestricted service credentials. The API owns validation, authentication/authorization, tenant/team/resource scope, orchestration, contracts, job submission and persistence.
```

**With:**

```text
- The browser is presentation-only and receives no provider keys or unrestricted service credentials. The .NET 8 Web API owns the persistence responsibility specified by Requirement §7, in addition to validation, authentication/authorization, tenant/team/resource scope, orchestration, contracts and job submission. It uses the distinct storage-specific persistence boundary described in §6; this allocation does not prescribe a project layout.
```

### 2. Section 2, architecture boundary: storage-specific implementation

**Replace:**

```text
- Domain/application rules remain independent from infrastructure-specific types. API/presentation must not own persistence, worker, Azure, provider, or secret-management concerns. Keep Azure/provider adapters behind the minimum interfaces required by the approved boundaries; do not add generic repositories, CQRS/MediatR, extra layers, caches, packages, or services without demonstrated need.
```

**With:**

```text
- Domain/application rules remain independent from infrastructure-specific types. API/presentation owns the persistence responsibility specified by Requirement §7, but does not directly implement storage-specific persistence concerns; those are implemented behind the distinct persistence boundary described in §6. The API does not directly implement worker, Azure, provider, or secret-management concerns. Keep Azure/provider adapters behind the minimum interfaces required by the approved boundaries; do not add generic repositories, CQRS/MediatR, extra layers, caches, packages, or services without demonstrated need.
```

### 3. IP-01, completion evidence

**Replace:**

```text
Select no unnecessary packages/layers; record actual project layout and commands as implementation evidence.
```

**With:**

```text
Select no unnecessary packages/layers; record actual project layout, commands, and the Web API-to-persistence-boundary allocation as implementation evidence.
```

### 4. IP-02, target

**Replace:**

```text
**Target:** .NET domain/application contracts and persistence boundary; Azure SQL schema and migrations.
```

**With:**

```text
**Target:** .NET domain/application contracts; the storage-specific persistence boundary used by the .NET 8 Web API/application; Azure SQL schema and migrations.
```

### 5. IP-02, completion criterion

**Replace:**

```text
indexes are justified by specified lookups; no speculative fields or schema changes are added.
```

**With:**

```text
indexes are justified by specified lookups; the storage-specific persistence boundary implements the persistence operations the Web API/application uses to fulfill Requirement §7, and domain/application contracts do not expose storage-specific types; no speculative fields or schema changes are added.
```

### 6. Section 6, Web API/application layer

**Replace:**

```text
2. **.NET 8 ASP.NET Core Web API/application:** Identity, API contracts, validation, authorization, orchestration, read-only tools, configuration and job submission.
```

**With:**

```text
2. **.NET 8 ASP.NET Core Web API/application:** Identity, API contracts, validation, authorization, orchestration, read-only tools, configuration and job submission; owns the persistence responsibility specified by Requirement §7 and uses the distinct storage-specific persistence boundary in item 3.
```

### 7. Section 6, persistence boundary

**Replace:**

```text
3. **Domain/application and persistence boundary:** tenant-aware rules, SQL entities/migrations, activity/requests, permissions, jobs, evaluation metadata.
```

**With:**

```text
3. **Domain/application and persistence boundary:** tenant-aware rules and application contracts remain independent from storage-specific types. A distinct persistence component within this planned boundary implements the Azure SQL-specific persistence operations used by the Web API/application, including SQL entities/migrations, activity/requests, permissions, jobs and evaluation metadata. No concrete project layout or repository pattern is selected.
```

### 8. Section 8, architecture verification evidence

**Replace:**

```text
architecture boundary checks; no invented route/entity treated as required
```

**With:**

```text
architecture boundary checks including review of Web API persistence responsibility versus storage-specific implementation; no invented route/entity treated as required
```

## Exact candidate metadata replacements for a future Planning attempt

Apply each of these exact replacements only in the separately authorized Planning attempt after exact Human Approval. Replace `NEW_AUTHORIZED_PLANNING_ATTEMPT_ID` with the actual new invocation ID; the placeholder must never be published literally.

### Plan identity/version

**Replace:**

```text
- **Plan identity/version:** `supportiq-product-implementation-plan` / `0.2` (candidate; plan-local task IDs are stable within this identity/version).
```

**With:**

```text
- **Plan identity/version:** `supportiq-product-implementation-plan` / `0.3` (candidate; plan-local task IDs are stable within this identity/version).
```

### Candidate status

**Replace:**

```text
- **Status:** **Draft Candidate — self-validation complete; independent Implementation Plan Verification not performed.** Not Ready for Human Review Approval, not Human Plan Approved, and not authorized for implementation.
```

**With:**

```text
- **Status:** **Draft Candidate — self-validation is not a pass because V-02 remains unresolved; independent verification of predecessor v0.2 concluded CHANGES REQUIRED (V-01 High and V-02 Medium). This amendment addresses V-01 only.** Not Ready for Human Review Approval, not Human Plan Approved, and not authorized for implementation.
```

### Planning attempt identifier

**Replace:**

```text
- **Planning attempt:** `20261111T080022Z-6bcfff1e-cee4-4d86-ac38-a9cec718008c`.
```

**With:**

```text
- **Planning attempt:** `NEW_AUTHORIZED_PLANNING_ATTEMPT_ID`.
```

### Amendment basis

**Replace:**

```text
- **Amendment basis:** IPV-01 (Plan Verification attempt `20261107T133205Z-58d4f444-0acf-4ebf-b31b-d66dedca6e75`), Finding Investigation `20261111T052943Z-22085ae6-3b40-4731-b8c3-a4c14bdebc78`, Corrective Change Decision `20261111T072125Z-4ca95993-a4f2-4313-8c2c-06572696b017`, and Human Approval [issue comment 6790246131](https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6790246131) of the exact Option A amendment (SHA-256 `8FCC73D5DA66661180ECEDCAF7596687D584D80EC28C73E81A44A8A5C668E2C6`).
```

**With:**

```text
- **Amendment basis:** IPV-01 Option A, as approved by Human Approval [issue comment 6790246131](https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6790246131) of the exact amendment (SHA-256 `8FCC73D5DA66661180ECEDCAF7596687D584D80EC28C73E81A44A8A5C668E2C6`) and preserved in predecessor v0.2; V-01 Implementation Plan Verification `20261111T085840Z-3b354dae-b851-452c-898e-d067f2b9ee84`, Finding Investigation `20261111T092500Z-1e1dfb89-85d5-4db4-bf98-3cbe1b1f73cf`, and Corrective Change Decisions `20261111T121348Z-1ab2111e-d30f-4a20-adfe-e0661d43d9aa` and `20261111T132411Z-045ed15e-1809-4bb7-a389-8c7a3369dabb`; human-selected clarification preserves approved Requirement §7; exact amendment approval is recorded in the associated Implementation Planning attempt evidence.
```

### Self-validation result

**Replace:**

```text
**Result:** Self-validation **PASS WITH EXPLICIT DECISION GATES AND REPOSITORY LIMITATIONS**. This is the planning actor's validation only; it is not independent Implementation Plan Verification. The four approved-Requirement §17 decisions remain open and block only their dependent implementation tasks. Concurrency safety is not established, so implementation is serialized. Because independent verification and all later human gates have not occurred, status remains **Draft Candidate**.
```

**With:**

```text
**Result:** Self-validation **NOT A PASS** because V-02's repository-state discrepancy remains unresolved and outside this V-01 amendment. The V-01 clarification is applied only under the human-approved Planning revision and still requires independent verification. This is the planning actor's validation only; it is not independent Implementation Plan Verification. The four approved-Requirement §17 decisions remain open and block only their dependent implementation tasks. Concurrency safety is not established, so implementation is serialized. Candidate status remains **Draft Candidate**; it is not ready for Human Review Approval.
```

### Approval status and handoff

**Replace:**

```text
## 12. Approval Status and Handoff

- **Candidate plan status:** Draft Candidate v0.2; candidate v0.1 remains preserved as a superseded draft.
- **Independent Implementation Plan Verification:** Complete verification of candidate v0.2 has not been performed; required next process.
- **Human Review Approval:** Not requested or obtained.
- **Human Plan Approval:** Not requested or obtained.
- **Implementation authorization:** None. No implementation may begin from this candidate.
- **Governed next sequence:** Complete independent Implementation Plan Verification of candidate v0.2 → resolve verification findings and required decisions → complete current-plan Human Review package → Human Review Approval (progression only) → separate Human Plan Approval → Implementation using only the current approved Plan, under required Orchestrator coordination.
```

**With:**

```text
## 12. Approval Status and Handoff

- **Candidate plan status:** Draft Candidate v0.3; candidate v0.1 remains preserved as a superseded draft, and candidate v0.2 remains preserved as the superseded predecessor draft.
- **Independent Implementation Plan Verification:** Verification of v0.2 concluded CHANGES REQUIRED (V-01 High and V-02 Medium); v0.3 has not yet been verified. This V-01 amendment does not resolve V-02.
- **Human Review Approval:** Not requested or obtained.
- **Human Plan Approval:** Not requested or obtained.
- **Implementation authorization:** None. No implementation may begin from this candidate.
- **Governed next sequence:** Separately investigate and decide V-02, applying any approved correction through a fresh governed Planning attempt; complete full independent Implementation Plan Verification of the resulting candidate; resolve all findings and required decisions; complete the current-plan Human Review package → Human Review Approval (progression only) → separate Human Plan Approval → Implementation using only the current approved Plan, under required Orchestrator coordination.
```

These administrative changes do not correct V-02: the inaccurate observed-repository-state statement in Section 2 remains unchanged and is explicitly unresolved.

## Change impact and application route

- Plan sections: Section 1 identity/status/amendment basis; Section 2 architecture boundary; IP-01/IP-02; Section 6 layers; Section 8 verification evidence; Section 11 self-validation status; Section 12 status/handoff.
- Tasks: no task added or removed; IP-01 completion evidence and IP-02 target/completion criterion clarified. Existing task IDs and prerequisites remain unchanged.
- Requirements, approved architecture, scope, exclusions, provider choices, project layout, and repository-pattern decisions: unchanged.
- This proposal is not approval or authority to apply. After separate exact Human Approval, start a fresh Implementation Planning process with explicit scope to create v0.3 from v0.2 and apply only the approved replacements/metadata. Then independently verify the complete resulting candidate.

## Deterministic check

All 14 exact-text replacements (eight architecture/task/traceability changes and six metadata replacements) were confirmed to match once against the bound source. Applying them in memory, including the non-publishable placeholder for the future Planning attempt ID, produces 54436 UTF-8 bytes with SHA-256 `BB2D81C251F356D7E56AC4737EC71CA35BB6CF41587CAAF623E7DFCE67C20564`. This is a simulation fingerprint only, not the fingerprint of final v0.3. Candidate v0.2 was not written or modified.
