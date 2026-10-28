# Requirement Analysis Verification Prompt
Read and follow:

`docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md`

Independently verify the complete current Requirement Analysis and, when a Requirement Update has occurred, the complete resulting Updated Requirement against:

- the complete current Source Requirement
- the complete resulting Updated Requirement, where applicable
- applicable approved constraints
- explicit approved decisions
- available supporting evidence

Treat the Source Requirement, resulting Updated Requirement, complete current Requirement Analysis, and applicable human decisions as distinct verification inputs/targets where applicable. Do not treat the Updated Requirement as implicit in the Requirement Analysis.

Verify:

1. Requirement coverage
2. Interpretation accuracy
3. Scope alignment
4. Functional requirement completeness
5. Business rule completeness
6. Non-functional requirements where applicable
7. Acceptance criteria
8. Ambiguities
9. Contradictions and consistency
10. Assumptions
11. Dependencies
12. Decisions required
13. Implementation-neutrality

Identify:

- missing requirements
- incorrect interpretations
- scope gaps
- scope creep
- unsupported assumptions
- ambiguities
- contradictions
- missing decisions
- acceptance-criteria gaps
- dependency gaps
- non-functional gaps
- premature implementation decisions

For every material finding, provide:

- classification
- severity
- evidence
- impact
- confidence
- recommended action

If a human/business decision is required, identify the decision explicitly and explain why it cannot safely be assumed.

Do not:

- modify the source requirement
- modify the requirement analysis
- create an implementation plan
- implement code
- make unapproved business decisions
- silently change scope
- claim Human Requirement Approval

If corrections are required, provide precise recommended changes but do not apply them.

Route material findings affecting governed artifacts through Finding Investigation and Corrective Change Decision & Plan Update, followed by required Human Approval before applying an approved change and the required verification. Do not apply corrections during verification.

Verify the complete current analysis, not only recently changed sections.

If the requirement analysis has previously been modified, verify the complete updated analysis again.

Clearly distinguish:

- executed evidence
- source inspection evidence
- reported evidence
- unverified information

Return the complete verification report defined by:

`docs/ai/guidelines/REQUIREMENT_ANALYSIS_VERIFICATION_GUIDELINES.md`