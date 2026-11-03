# Q4 authority clarification recorded

Work `supportiq-requirement-discovery-cb6472d0-3e33-4eeb-bf0b-ba01740ded1a`; own attempt `20261103T070934Z-f7d837c5-680b-4a05-a5c8-54c8d3602915`; actor
`orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff`.
State **REQUIREMENT_DECISION_PENDING**; Q5-Q10 pending.

## Source and actual outcome

All three complete actual fields (`tenant_admin_authority`, `bootstrap_recovery_authority`,
`rationale_deferrals`), including the full tail, are retained in `attachments/q4-auth.json`.
Raw UTF-8 text, character/byte offsets, transport suffixes and full reconstruction/native
JSON equality tests are preserved. Local retained-text integrity is not authenticated Human
byte-whitespace/message-ID/native-time proof. Unknown authenticated values remain null.
This report is a presentation, not replacement for the actual fields.

The supplied answers resolve Q4-C01 and Q4-C02 from the linked prior report through new
clarification evidence. Original Q4 words, questions and pending-history records remain unchanged.

## Administrative authority recorded; not executed

Only an authorized Platform Admin approves subsequent Tenant Admin assignments/removals/
privileged restoration. Existing Tenant Admin may nominate/request but not independently
approve or execute. After explicit authorization, an authorized Platform Admin or controlled
provisioning process executes with target identity/tenant/account-status/eligibility checks;
approver and executing actor/process are recorded separately. Requestor cannot approve their
own request. Last Tenant Admin removal is blocked unless authorized replacement has been
successfully assigned or a separately authorized recovery path is available. Reactivation
never automatically restores privilege; fresh Platform Admin authorization is required.

Organization Owner or formally designated Security Authority independently authorizes initial
Platform Admin bootstrap. Designated Security/Identity Administrator verifies identity/
eligibility; authorized DevOps/Deployment Operator executes the one-time process and invalidates
temporary credentials/privileges. No circular dependency on an existing administrator.

Last Platform Admin recovery uses Owner/Security Authority authorization, separate authorized
Security/Identity Administrator legitimacy/identity verification and authorized technical
operator execution for an explicitly nominated replacement. No self-registration, ordinary
password-recovery escalation or reliance on unavailable administrator accounts.

Last Tenant Admin recovery is approved by an authorized Platform Admin and executed by an
independent authorized technical operator or controlled provisioning process, limited to the
affected tenant's administrative control and preserving identity/status/membership checks.

Authorization, identity verification and execution are separated responsibilities; no person
may request, approve and execute their own privileged bootstrap/recovery. Three distinct
individuals are preferred where staffing permits. The actual minimum is independent Human
authorization and execution, separate identity-verification evidence and comprehensive audit.
No additional staffing policy is selected here.

Trusted organizational/out-of-band identity checks, business justification, nominated identity,
MFA before normal administrative access, temporary-credential invalidation, explicit privilege
assignment (no inheritance), affected compromised/replaced-account session/refresh-token
revocation and tamper-resistant audit are recorded requirements. Audit preserves request/
approval/verifier/executor/outcome/timestamps/revocation evidence without secrets.

Q2/Q3 eligible non-submitter Knowledge Reviewer permission remains separately authorized.
Tenant isolation and first-release prohibition on exceptional Platform Admin tenant-content
access remain unchanged. Account administration/recovery grants no content override.

## Rationale, deferrals and remaining state

Full actual rationale explains accountability, prevention of self-escalation, elimination of
unavailable-administrator dependencies, recoverability and safety over convenience.
Organizational designation/delegation procedures, deployment tools, recovery runbooks,
identity-verification technologies/evidence formats, SLAs/escalation/notification timings
and future automated emergency recovery are explicitly deferred, not implied authority.
No further material authority ambiguity identified in these supplied answers; no new
clarification loop is requested. Concrete operational designations still must be established
before any affected operation; this record authorizes none.

Q5-Q10 remain pending. Q4's audit-retention deferral versus the stated draft 365-day
content-free metadata obligation stays with Q5; it is not a waiver. The previously supplied
bounded Q5 form is unchanged and was not asked or rediscovered here.

## Publication and boundaries

Current adoption comments/owner/body fingerprints, 78-input fingerprints, hidden-inclusive
framework set, current Windows identity/ACL and predecessor bindings were qualified.
Own invocation first/readback, immutable own utility reuse for current validated publication,
then full evidence/checkpoint/report and result last. Extended absolute Windows paths,
exclusive validated partials, flush/fsync, atomic same-directory no-overwrite rename and
fresh byte/hash/native-object readbacks used. Historical finals and source files unchanged.
No PRD change, Requirement Approval, process initiation, nested agent, runtime/deployment,
staging, commit or push. Execution completed means only this bounded transcription completed.
