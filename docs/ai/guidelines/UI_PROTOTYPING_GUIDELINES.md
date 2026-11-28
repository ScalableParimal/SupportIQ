# Optional UI Prototyping Guidelines

## 1. Purpose and authority

This guideline governs one optional UI-prototyping mechanism group with two separately defined actors: a Creator and an independent Verifier. The group is outside the 52-core catalog and adds no Requirement, Plan, implementation, review, or acceptance authority. The three Masters remain authoritative.

The prototype is a mock-data-only design reference, not production code. Existing Requirement, Plan, implementation, security, Verification, Review, Human Acceptance, and commit gates remain in force.

## 2. Applicability and entry

The optional branch follows Human Requirement Approval for the exact current Requirement version and precedes Implementation Planning. A repository-level human applicability setting may enable or disable the option. If it is absent or disabled, record `NOT OPTED IN` and continue; absence never implies consent or blocks the lifecycle. When enabled, obtain an explicit human `PROTOTYPE` or `SKIP` choice for each approved Requirement version. Silence means `SKIP`, recorded without blocking.

For an Orchestrator-invoked Creator or Verifier, require fresh Process Initiation Approval for that exact invocation. A directly invoked Creator or Verifier instead requires an explicit human request for that exact invocation; the Orchestrator-specific interlock does not apply to direct entry. The Creator and Verifier are separate processes; the Orchestrator must not invoke either automatically. If the adopted product persistence root, an approved Requirement, an approved frontend technology baseline, or an applicable template is unavailable, do not create or use a prototype. Record the reason when the authorized product record route exists and continue the product lifecycle without a prototype, unless an independent governance gate blocks it.

## 3. Template source and compatibility

Use only a human-supplied template repository URL, full immutable commit SHA, and optional repository subpath. Resolve and record the pinned commit, selected-file manifest fingerprint, license/provenance evidence, and approved frontend baseline used for compatibility. Validate that the selected template matches that approved baseline; do not infer technology from an unapproved draft or from the template itself.

Treat the template as untrusted, read-only input. Do not write to its repository, execute its scripts, install its dependencies, follow unapproved remote assets, use credentials, or place customer data/secrets in the prototype. If the pin, license, compatibility, or safety cannot be established, produce no prototype and continue without one. A scan is evidence, not proof of safety.

## 4. Creation and independent verification

The Creator may produce an immutable candidate only under its own attempt in the adopted product persistence root. The candidate must use synthetic/mock data and identify its Requirement version, repository applicability decision, template URL/commit/subpath/manifest fingerprint, technology baseline, and candidate SHA-256. It must not modify application source, tests, configuration, package manifests/lockfiles, migrations, or the template repository. New dependencies require separate confirmation under the applicable team rules; they are not added by this mechanism.

The Verifier must be a distinct actor from the Creator and must independently inspect the exact candidate and pinned source. It records a separate read-only report and checks Requirement traceability, template pin/provenance/compatibility, mock-only content, isolation from production paths/dependencies, artifact integrity, and absence of unauthorized changes. It may report `PASS`, `FINDINGS`, or `CANNOT COMPLETE`; a non-pass means the candidate cannot be approved or reused. The product lifecycle may continue without a prototype.

## 5. Human Prototype Approval and planning handoff

After a passing independent Verification, the authorized human may approve one exact candidate by an explicit GitHub issue comment on a human-selected issue. The comment evidence must be attributable and bind the Requirement version and SHA-256, candidate identity and SHA-256, template URL/full commit/subpath and manifest fingerprint, Verifier report identity/fingerprint, and approval scope. The process records the permalink, comment identity, author attribution, timestamp, exact body, and body fingerprint. The mechanism does not create, edit, or poll issues. If the comment or attribution cannot be verified from authorized evidence, no approval is inferred; proceed without a prototype.

Human Prototype Approval permits only the identified prototype to be considered by Planning. It is distinct from Human Requirement Approval, Human Review Approval, Human Plan Approval, Human Acceptance, and Process Initiation Approval. It does not approve a Plan or authorize implementation. A Plan that uses the prototype must reference its exact approved identity/fingerprint and include applicable acceptance criteria; Implementation Verification checks conformance to the approved Plan and prototype reference. If no approved prototype exists or the Plan elects not to use it, the Plan records that no prototype is used.

## 6. Findings, suggestions, and revisions

A verifier-reported Finding follows the existing Finding Investigation and Corrective Change Decision route. A Requirement defect follows Requirement Update and its required downstream analysis, Verification, approval, and plan-impact controls. Neither route is replaced by prototype approval.

A human-suggested prototype correction is a non-finding revision input unless it independently establishes a Finding. The Creator may prepare a new immutable candidate only after a fresh Creator stage-start. Never edit an approved candidate in place. Each revision receives a new identity and SHA-256, a fresh independent Verification, and a new Human Prototype Approval before Planning or Implementation may use it. A suggestion or issue URL is not approval.

## 7. Records and terminal outcomes

Creator artifacts and records remain only in the adopted product repository under the Creator's own authorized attempt; Verifier evidence remains in the Verifier's own attempt. Reuse existing Work ID and publication controls. Do not create a new persistence root. No actor commits, pushes, or modifies a remote repository. Record `NOT OPTED IN`, `SKIPPED`, `VERIFIED - PENDING HUMAN APPROVAL`, `APPROVED FOR PLAN REFERENCE`, `FINDINGS`, or `CANNOT COMPLETE` accurately. Any outcome without an approved candidate permits continuation without a prototype and does not imply failure of the product Requirement.
