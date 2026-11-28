# Optional UI Prototyping Prompt

Read and follow `docs/ai/guidelines/UI_PROTOTYPING_GUIDELINES.md` and the supplied `docs/ai/request/UI_PROTOTYPING_REQUEST.md`.

Execute only the explicitly assigned role: Creator or independent Verifier. Preserve the subject as optional UI prototyping, not a Finding unless a governed Finding is independently established. Use the exact current approved Requirement, explicit repository and per-Requirement applicability decisions, approved frontend baseline, human-supplied template URL/full commit/subpath, and adopted product record root. If any required source is missing, the safe result is no prototype and continuation without one; never infer opt-in or approval.

The Creator prepares one immutable mock-only candidate and its own records, without changing production files, dependencies, tests, configuration, migrations, or the template repository. The Verifier must be actor-distinct, read-only, and independently inspect the exact candidate and pinned template; publish its own report. Neither actor approves the candidate, initiates another stage, creates/modifies GitHub issues, commits, or pushes.

Human Prototype Approval is a separate, attributable GitHub issue-comment decision binding the exact Requirement, prototype, template, and passing Verifier evidence. If attribution or integrity cannot be established, do not treat it as approved. Only an approved Plan may authorize prototype reuse; Implementation Verification must check its Plan-bound conformance. Route Findings, Requirement defects, and human-suggested non-finding revisions as defined by the Guideline. Return only the role-specific result and identify evidence classifications and limitations.
