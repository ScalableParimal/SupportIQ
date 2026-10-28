# Implementation Review Prompt
Read and follow:

`docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md`

Review the complete current implementation against the current approved Requirement and current approved Implementation Plan.

Perform a technical review covering the applicable areas defined in the guideline, including:

- architecture
- design quality
- code quality
- error handling
- validation and data integrity
- security
- performance
- testing
- configuration and operational concerns
- repository consistency

Do not limit the review to recently changed files or corrective changes.

Do not implement corrections.

Do not modify source code, tests, configuration, migrations, requirements, or implementation plans.

Do not introduce new requirements that are not supported by the approved Requirement, Plan, or applicable engineering guidelines.

Clearly distinguish:

- facts
- source inspection evidence
- executed evidence
- reported evidence
- assumptions
- recommendations

If a material issue is identified, provide evidence, impact, severity, and confidence.

If a potentially material issue cannot be reliably determined, recommend Finding Investigation instead of treating it as a confirmed defect.

Do not claim Human Acceptance.

Return the complete review report defined by:

`docs/ai/guidelines/IMPLEMENTATION_REVIEW_GUIDELINES.md`