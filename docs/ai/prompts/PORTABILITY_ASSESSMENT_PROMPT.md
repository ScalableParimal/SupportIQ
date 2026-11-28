# SDLC Portability Assessment Prompt

Read and follow `docs/ai/guidelines/PORTABILITY_ASSESSMENT_GUIDELINES.md` and the invocation's `docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md`.

Assess only the identified target project and authorized paths. Bind source-framework evidence separately from target-project evidence. Record repository/workspace identity, revision/fingerprints, scope, trigger, human decisions supplied, and permissions. If target, scope, or permission is missing, stop and request it.

Apply each applicable dimension and the five determination states from the Guideline. Classify concerns using its six routing categories. Distinguish source-inspection, executed, reported, and unverified evidence. Do not equate a target gap with a framework defect, a recommendation with a human decision, or static inspection with runtime verification.

For the repository-baseline dimension, identify applicable files/checks,
existing rules, gaps, risks and missing evidence. Do not claim unchecked remote
security controls are enabled or expose secret values. Recommendations are
advisory; do not invoke Baseline Setup or decide its human gates.

For each possible blocker, recommend whether it appears applicable and state evidence, impact, and scope. A human authorized for the target project must explicitly decide whether it applies. Do not decide for the human or represent the recommendation as binding. If the decision is absent, report it pending and recommend holding the first/next affected SDLC activity.

Do not automatically invoke Agents; activate Orchestrator; modify either repository; execute scripts/tests/runtime behavior without express bounded authorization; approve requirements/plans; implement; commit; or push. Use the report structure and completion rules in the Guideline and Skill. Stop at this assessment's handoff.
