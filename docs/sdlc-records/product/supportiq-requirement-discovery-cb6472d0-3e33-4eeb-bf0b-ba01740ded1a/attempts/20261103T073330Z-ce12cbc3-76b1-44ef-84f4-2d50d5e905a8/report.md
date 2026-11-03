# Q5 deletion and retention clarification recorded

Work `supportiq-requirement-discovery-cb6472d0-3e33-4eeb-bf0b-ba01740ded1a`; own attempt `20261103T073330Z-ce12cbc3-76b1-44ef-84f4-2d50d5e905a8`; actor
`orchestrator-coordination-b677bc83-551e-4ea7-b797-747b46c78aff`.
State **REQUIREMENT_DECISION_PENDING**. Q5 material confirmations and Q6-Q10 pending.

## Complete actual source

All six actual fields and full rationale/deferrals/tail are in `attachments/q5.json`.
Raw UTF-8 transport text, exact character/byte offsets, transport suffixes and reconstruction/
native JSON equality tests preserve the response. Source bytes 35888, SHA-256
`D60E09FD0D7FDDB4EECE32FFCB619C36953B6F0F65029AB12B616DC2E0693495`.
This report is not a replacement for actual words. Local integrity does not authenticate
Human byte-whitespace, native message ID or decision time; unavailable values remain null.

## Actual decisions recorded, not implemented

Distinct exact-version and complete logical-document/all-version deletion requests.
Appropriately authorized tenant users/owners request; independent Tenant Admin approves;
requesting Tenant Admin requires an eligible independent second Tenant Admin, otherwise pending.
Exact original-submitter restriction preserved without inventing an extra deletion-role rule.
Tenant background deletion service executes only approved scope; no Platform Admin content bypass.

Explicit independent approval immediately excludes retrieval/citation and starts the immutable
UTC 24-hour primary-purge clock, not submission. Includes originals/content-bearing metadata,
extracted text/chunks/embeddings/index/caches/temp and other active derived copies. Cancel/discard
in-flight retrieval and stop/regenerate affected generation before delivery; delayed processing
cannot recreate content. Preserve unrelated versions only if independently eligible.

Component deletion/verification needs content-free evidence; no overall success from one
component. Controlled idempotent transient retry; persistent failures escalate to Operations/
Security, notify Tenant Admin/requester accurately. Missed 24-hour deadline is Overdue,
exclusion persists, no false success. Retry/backoff/SLAs deferred, not deadline waiver.
Actual listed states: DeletionPending (approved awaiting execution), RetrievalExcluded,
Purging, PartiallyPurged, PurgeFailed, Overdue, Purged (all primary components independently
verified). Primary purge and backup expiry are distinct.

Encrypted backup max 30 days from each backup creation (UTC), not document deletion;
no immediate deletion of whole backup containing unrelated data. Restore deletion/suppression
and all lifecycle restrictions and verify before any user/AI access; no deadline reset or
deleted-content eligibility. Content-free audit retained 365 days from each record creation,
then authorized controlled removal; no original content/embeddings/secrets retained in audit.
Q5 does not waive 24h/30d/365d obligations. Its characterization of Q4 as lifecycle-specific
does not rewrite original Q4 audit/technical deferrals.

Non-current/failed/rejected/superseded/expired/overdue content remains ineligible; only explicitly
authorized tenant human inspection. Exact lifecycle retention periods deferred, not indefinite
authority or waiver of approved deletion. Mandatory 180-day independent review remains; old
version currentness cannot override validity. Potential broader validity-extension wording is
preserved and held for confirmation below.

Narrow mandatory legal/regulatory exception requires separately documented Legal Authority
approval, independent Security review, legal basis/exact tenant-data scope/duration/review/
release conditions/audit. No ordinary admin discretion, implied hold or content-access override.
Hold/deadline and broader legal-access wording require confirmation; no policy selected.

Full rationale prioritizes controlled tenant isolation, retrieval safety, verified deletion
and bounded backup/audit retention. Technical backup/audit storage/verification/retry/escalation/
restoration/scheduling details and exact lifecycle schedules remain explicitly deferred.

## Material confirmation package for parent

### Q5-C01 — Expired-content validity extension versus independent reapproval

Actual `lifecycle_retention`: Reapproval or an explicitly authorized validity extension must be completed before the document becomes AI eligible again.

Confirm a validity extension cannot substitute for required eligible tenant non-submitter Knowledge Reviewer approval/formal re-review, reset the 180-day clock by itself, or bypass any current eligibility restriction; if a new route is intended, explicitly define its authority and scope.

### Q5-C02 — Legal retention exception and approved-deletion retrieval exclusion

Actual `backup_audit`: Legally retained content must remain excluded from AI retrieval unless separately and legitimately authorized.

Confirm legal hold/retention authority cannot return deletion-approved content to AI retrieval/citation or reinstate it; define whether the quoted exception applies only to otherwise eligible content outside approved deletion, or explicitly identify any intended change.

### Q5-C03 — Legal hold release and 24-hour purge deadline

Actual `deletion_scope`: Applicable legal and regulatory retention requirements must take precedence over ordinary deletion schedules.

When an authorized legal hold blocks physical purge, how is the original deadline/hold status recorded, and what exact deadline and start event govern purge after hold release? Specify authority/evidence; do not infer pause, reset or extension.

### Q5-C04 — Deferred failed/rejected retention versus existing draft purge obligation

Actual `lifecycle_retention`: The exact automatic retention and deletion periods for failed, rejected, superseded, expired, and overdue content are explicitly deferred.

Confirm whether the Q5 failed/rejected retention deferral and non-automatic rejection deletion intentionally replace the draft failed/rejected 24-hour purge obligation, or whether that obligation remains. Exact lifecycle durations remain pending; no indefinite retention or silent waiver inferred.

These are unresolved applicability questions, not adopted policy. No permission
for validity-extension bypass, deletion-approved reinstatement, inferred hold clock or indefinite
failed/rejected retention is established. No original Q2-Q5 final is altered.

## Q6 topics for parent only

Actual Analysis section 9 Q6 / RA-A06 / RA-M06:
- Initial tenant category and priority values/defaults, including meanings.
- Mapping versioning and authority to request/approve/change mappings.
- Supported queue/escalation suggestion rules and human review; AI cannot autonomously escalate.
- Which human-approved override values and original AI suggestions must be retained, and for how long.
- Rationale and explicit unresolved taxonomy details.

These topics are returned, not asked; no taxonomy/queue/priority policy selected.

## Publication boundary

Current own invocation qualified/published/read back first, then full evidence/checkpoint/report,
result last. Current adoptions/owner/body hashes, 78 fingerprints, hidden-inclusive framework set,
Windows identity/ACL and predecessor records checked. Extended paths, exclusive validated partials,
flush/fsync, atomic same-directory Windows no-overwrite rename and fresh readbacks used.
Historical finals unchanged. No PRD/source edit, Requirement Approval, new process/nested agent,
runtime/deployment, staging, commit or push. Before any affected later transition assess changed
clarification scope/Portability applicability; no assessment or downstream process invoked here.
