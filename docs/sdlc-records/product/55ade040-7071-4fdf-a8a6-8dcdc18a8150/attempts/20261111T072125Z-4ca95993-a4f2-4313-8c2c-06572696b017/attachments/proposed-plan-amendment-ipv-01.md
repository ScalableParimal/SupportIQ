# Proposed Plan Amendment — IPV-01 (PROPOSAL ONLY, NOT APPROVED, NOT APPLIED)

- **Work ID:** `55ade040-7071-4fdf-a8a6-8dcdc18a8150`
- **Corrective Change attempt:** `20261111T072125Z-4ca95993-a4f2-4313-8c2c-06572696b017`
- **Affected artifact:** candidate Implementation Plan `supportiq-product-implementation-plan` / `0.1` (draft candidate; not Human Plan Approved), [implementation-plan-supportiq-v1.11-v0.1.md](../../20261106T133655Z-aad237e2-4bec-4bc3-87c0-1d939b08a85d/attachments/implementation-plan-supportiq-v1.11-v0.1.md), 49,325 bytes, SHA-256 `66AB32440BC49F9FFFD4038310B790E37E56F5AFA8A2DA4D54F5DA4155F8C71D`.
- **Proposed target:** candidate `0.2`, produced by the governed application route that the human designates. The v0.1 file must not be edited in place.
- **Status of this text:** proposal for Human Approval. It does not change the Plan, does not select an option on the human's behalf, and does not authorize implementation.

Line numbers refer to v0.1. Existing task IDs are not renumbered. In the replacement text, wording that is new or changed is shown in **bold**.

---

## Part 1 — Option A (advisory recommendation of the Finding Investigation)

Option A adds one owned contract-readiness task, divided into per-slice milestones. This avoids a single system-wide API freeze.

### A1. New task — insert immediately after the `### Phase 4 — User-facing workflows` heading (line 123) and before IP-20

> **IP-19A — Establish per-slice API contract baselines and consumer readiness**
> **Target:** API presentation layer OpenAPI/contract artifacts and API contract test project(s). **Requirements:** §9 and its final-contract rule (schemas, validation, status codes, error responses, idempotency where needed, OpenAPI documentation); FR families of each slice below; §§13–14. **Prerequisites (per slice; each slice may become ready independently):** S1 identity, tenant, user, team, permission, settings/retention, tenant lifecycle and notification contracts — IP-05, IP-06, IP-08, IP-09; S2 ticket lifecycle, requests, assignment and urgency review — IP-10, IP-11, IP-13; S3 knowledge, indexing status, chat/citations and Copilot — IP-14, IP-15, IP-17, IP-18; S4 Customer Search/Read/unmask and Feedback Read — IP-12; S5 analytics — IP-19. Where a slice exposes asynchronous work, IP-07 is also a prerequisite for that slice. **Completion (per slice):** a versioned, reproducible OpenAPI description of exactly the operations consumed by the slice's UI task, generated from or checked against the producing API; it covers request/response schemas, validation rules, authorization/role scope, status codes and error responses, pagination/filter/sort where applicable, and 202/Job ID/status/result/cancellation and idempotency where required. API contract tests for those operations pass against the producer implementation. A slice readiness record names the slice, its contract version, its producer tasks and its consumer task. No route, field or value is added beyond the approved Requirement, and illustrative names are carried forward only where the design confirms them. D-01 through D-04 are not resolved by this task. **Task completion:** all slices S1–S5 are ready. **Change rule:** any change to a slice contract after readiness re-runs that slice's contract tests and reconciles the affected consumer task before that consumer proceeds.

### A2. Replacement prerequisites for the UI tasks

Only the **Prerequisites** clauses change; Target, Requirements and Completion stay as they are.

| Task (line) | v0.1 text | Proposed text |
| --- | --- | --- |
| IP-20 (126) | `IP-05, IP-06, IP-08, IP-09 and finalized API contracts.` | `IP-05, IP-06, IP-08, IP-09 and **IP-19A slice S1 ready**.` |
| IP-21 (129) | `IP-10, IP-11, IP-13, IP-20.` | `IP-10, IP-11, IP-13, IP-20, **IP-19A slice S2 ready**.` |
| IP-22 (132) | `IP-14, IP-15, IP-17, IP-18, IP-20.` | `IP-14, IP-15, IP-17, IP-18, IP-20, **IP-19A slice S3 ready**.` |
| IP-23 (135) | `IP-12, IP-20.` | `IP-12, IP-20, **IP-19A slice S4 ready**.` |
| IP-24 (138) | `IP-19, IP-20.` | `IP-19, IP-20, **IP-19A slice S5 ready**.` |

### A3. Consequential edits

| Location (v0.1 line) | v0.1 text | Proposed text |
| --- | --- | --- |
| §2 constraint (32) | `… and be reconciled before consumers are built.` | `… and be reconciled before consumers are built**; ownership, deliverables and readiness checks for this reconciliation are assigned to IP-19A**.` |
| IP-26 prerequisites (146) | `completion of every task IP-01 through IP-25.` | `completion of every task IP-01 through IP-25**, including IP-19A**.` |
| §5 dependency chain (155) | `… → IP-17/IP-18/IP-19 → IP-20–IP-24 → IP-25 …` | `… → IP-17/IP-18/IP-19 → **IP-19A (per slice)** → IP-20–IP-24 → IP-25 …` with the added sentence: **`Each IP-19A slice depends only on its own producer tasks, so a UI task may start as soon as its own slice is ready and its other prerequisites are complete.`** |
| §5 integration (162) | `… re-run impacted contract, authorization and migration tests; …` | `… re-run impacted contract, authorization and migration tests**; a contract change after an IP-19A slice is ready follows the IP-19A change rule**; …` |
| Traceability §4.1/§16 row (194) | `IP-01–IP-27, by module descriptions above` | `IP-01–IP-27 **(including IP-19A)**, by module descriptions above` |
| Traceability §§7–9 row (211) | `IP-01–IP-24; IP-26` / `Project/API/schema design review, contract tests, …` | `IP-01–IP-24 **(including IP-19A)**; IP-26` / `Project/API/schema design review, contract tests, **IP-19A per-slice OpenAPI contract and readiness evidence**, …` |

### A4. Version, status and disposition edits (for v0.2)

- §1 identity: `0.1` → `0.2` (candidate). Add the line **Amendment basis:** IPV-01 (Plan Verification attempt `20261107T133205Z-58d4f444-0acf-4ebf-b31b-d66dedca6e75`), Finding Investigation `20261111T052943Z-22085ae6-3b40-4731-b8c3-a4c14bdebc78`, Corrective Change Decision `20261111T072125Z-4ca95993-a4f2-4313-8c2c-06572696b017`, plus the Human Approval reference once it exists.
- §1 status, §12 handoff and §11 self-validation: set them to reflect v0.2 as a draft candidate that needs a complete new Implementation Plan Verification.
- §11 line 258: replace `no prior Plan disposition applies` with **`v0.1 disposition recorded: superseded draft candidate; tasks IP-01–IP-27 carried forward unchanged except the IP-20–IP-24 prerequisites and the IP-26 prerequisite clause; IP-19A added`**.
- **Task disposition:** IP-01–IP-19, IP-25 and IP-27 are carried forward unchanged. IP-20–IP-24 are carried forward with changed prerequisites. IP-26 is carried forward with a clarified prerequisite. IP-19A is new.

### A5. Explicitly unchanged

Architecture, scope, requirement families, exclusions, D-01–D-04, the serialized execution mode, the testing strategy (except the added contract-readiness evidence), the data/schema/migration approach, and the operational/configuration approach.

---

## Part 2 — Option B variant (acceptable alternative)

Option B adds no new task. Instead, each producer task gets a contract deliverable, and each UI task references its producers' contract completion.

- To the **Completion** of each of IP-05, IP-06, IP-07, IP-08, IP-09, IP-10, IP-11, IP-12, IP-13, IP-14, IP-15, IP-17, IP-18, IP-19, append: **`versioned, reproducible OpenAPI description of this task's consumer-facing operations (schemas, validation, scope, status/errors, pagination and async/idempotency where applicable) with passing API contract tests; no route/field beyond the approved Requirement.`**
- IP-20 prerequisites: `IP-05, IP-06, IP-08, IP-09 and finalized API contracts.` → `IP-05, IP-06, IP-08, IP-09 **(including their contract deliverables)**.` Similarly qualify the producer prerequisites in IP-21–IP-24.
- Line 162 integration: add **`before each UI task starts, confirm that the contract deliverables of all its producer tasks are present and mutually consistent for shared types (errors, pagination, job status).`**
- Make the same §2 line 32, line 211, version, status and disposition edits as in A3/A4, replacing the IP-19A references with "producer-task contract deliverables".
- **Known residual risk:** shared cross-cutting contracts (error envelope, pagination, job status) have no single owner. The added line-162 check is the only control.

---

## Part 3 — Not proposed

Option C, which relies only on the existing phase reconciliation or IP-26, is not proposed. IP-26 runs after the UI work and so does not close the pre-consumer gap. The Finding Investigation did not recommend it.
