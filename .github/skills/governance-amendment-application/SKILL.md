# Governance Amendment Application Skill

Use the current Application Guideline, Prompt, Request, exact proposal report, and Human Approval record. This Skill permits only controlled application after all approval and actor-authority preconditions are established.

Before writing: establish the work ID and authorized record scope; validate approval identity, scope, exclusions, exact content, paths, fingerprints, and named actor; confirm the applier differs from the preparer, verifier, and reviewer, and also differs from the SDLC Process Orchestrator and any Governance Remediation actor barred from self-edit during its active cycle (these additional exclusions apply only to the applier); inspect repository state; hash all targets; compare all bases before the first write.

If any precondition is missing, ambiguous, stale, or mismatched, do not write. Otherwise apply exactly the approved content to the approved paths and no others. Capture actual before/after hashes, bytes, path list, tool results, and any failure. If interrupted or partially applied, stop and report actual state; never claim success or silently roll back.

Publish only this Skill actor's invocation, report, result, and necessary evidence within its designated scope. Do not approve, independently verify, review, audit, adopt a baseline, commit, or push. Successful application hands off to independent Verification.

Before any source write, confirm actual runtime identity and capability evidence for read, SHA-256, path/check execution, exact approved-target write, readback, and publication to this actor's own record scope. Confirm capability without changing a source file. Require a fresh human stage-start instruction distinct from patch approval. Missing capability or scope evidence means `CANNOT COMPLETE` before writes. After application, verify target file identities and expected-after hashes and bind all evidence to this attempt. The Agent definition alone does not establish capability.
