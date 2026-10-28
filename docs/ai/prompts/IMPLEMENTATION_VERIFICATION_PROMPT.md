# Implementation Verification Prompt

Read and follow:

`docs/ai/guidelines/IMPLEMENTATION_VERIFICATION_GUIDELINES.md`

Use the Verification Request above to determine the scope and context of the verification.

Verify the complete current implementation against:

- the complete current approved Requirement
- the complete current approved Implementation Plan
- the applicable architecture
- applicable engineering guidelines
- relevant repository constraints and conventions
- available technical evidence

Task IDs, recently changed files, reported findings, and corrective changes are verification context only and must not restrict the verification scope.

Inspect the approved source documents and the actual repository relevant to the implementation.

Do not rely solely on previous AI summaries.

Perform all verification activities defined by the guideline.

Produce the complete verification report required by the guideline.

Clearly distinguish:

- executed evidence
- source inspection evidence
- reported evidence
- unverified information

Do not:

- modify the implementation
- modify tests, configuration, migrations, requirements, or implementation plans
- apply corrective changes
- silently change scope or requirements
- claim Human Acceptance

If a material finding is identified, report the evidence, impact, severity, confidence, and recommended next process.

If the implementation cannot be fully verified, identify the missing evidence or verification gap.

If changes are required, route the finding through the governed Finding Investigation and Corrective Change Decision & Plan Update process rather than applying the correction during verification.

At the end, state:

1. Overall verification status
2. Scope verified
3. Requirement traceability status
4. Implementation plan traceability status
5. Material findings, if any
6. Remaining verification gaps
7. Recommended next process