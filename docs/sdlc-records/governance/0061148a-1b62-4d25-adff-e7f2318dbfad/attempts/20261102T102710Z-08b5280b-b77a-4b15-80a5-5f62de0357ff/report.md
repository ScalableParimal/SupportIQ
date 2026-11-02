# Finding Investigation - GOV-AUD-20261102-002

Work ID: 0061148a-1b62-4d25-adff-e7f2318dbfad.
Cycle: GOV-REMEDIATION-PROSPECTIVE-001; Cycle 1.
Attempt: 20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff.
Canonical report identity: 20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff:investigation_report.

## 1. Finding summary

**Confirmed: a bounded Low / Ambiguity in governance instructions.**
The Governance Remediation Agent's section 43 optional post-completion route
requires attributable authorization records before Commit/Push, then instructs
the actor to append a newly created commit identity to the same authorization
record. It does not distinguish an immutable individual decision record from a
logical gate's collection of linked records or explain a compliant later-record
route. The Master explicitly forbids in-place modification of published final
records.

The finding concerns this missing reconciliation, not a proven mutation,
unauthorized Commit/Push, mandatory Commit/Push requirement, or missing extra
approval gate. Commit/Push remain optional and are not currently authorized.
Investigation only: no acceptance/rejection decision, correction, exact patch,
application approval, or other process is performed here.

## 2. Finding source

Subject type: FINDING, not a human-requested non-finding enhancement.
The canonical completed Governance Audit at attempt
20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f identifies
GOV-AUD-20261102-002 at report lines 302-323, severity Low, category Ambiguity.
Its actual outcome is CONSISTENT WITH MINOR FINDINGS: core 52/52, 76 source
files, seven mechanisms assessed, six PASS and Governance Remediation FAIL;
Critical/High/Medium 0, Low 1 and Ambiguities 1 describing the same finding,
other counts 0. This is not a qualifying clean Audit or adoption evidence.

The validated coordinator is attempt
20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565, with its actual
attachments/investigation-handoff.md and result-bound report. Its report,
result, handoff, validation evidence, and the Audit report/result/evidence were
resolved and hashed, not replaced by a summary.

Actual fresh Human start, supplied in the current parent conversation:

> Yes, initiate Finding Investigation for GOV-AUD-20261102-002 only under the existing Work ID and Cycle 1 using the validated handoff from attempt 20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565; no correction or other stage

No authenticated Human message ID or original Human decision time is exposed;
neither is invented. This is stage initiation, not substantive corrective approval.

## 3. Finding validation

**Guideline classification: Requirement Ambiguity**, applied to the
governance-instruction requirement for post-commit record handling, not to an
approved product Requirement. The Audit category remains Low / Ambiguity;
no unsupported new finding classification is created. This classification
does not imply that the candidate Master baseline is adopted.

Source inspection independently confirms the cited current wording:

- Remediation Agent line 1309: authorization records must exist before
  Commit/Push; missing or ambiguous decisions block the action.
- Line 1312: after creating an authorized commit, append its full identity to
  the same authorization record; Push additionally depends on that binding.
- Artifact Governance line 1191: published final records must not be modified
  in place; subsequent correction/supersession uses linked new records.

The pre-commit authorization cannot already contain the resulting commit's
identity as an observed fact. Literal later editing of the published individual
authorization would conflict with immutability. A reading of "record" as a
logical gate aggregate could support a linked later record, but this is not
specified. This alternative limits the finding to ambiguity; it does not
disprove it or grant permission to mutate a final decision.

The immutability rule itself is clear. Investigation need not invent an
exception to it, nor determine actual historical misconduct, to identify a
bounded clarification direction. No test, environment, production-code or
verification defect is established.

## 4. Evidence

### Executed evidence

- Current non-mutating identity, ACL/access, repository HEAD/branch/remote/status,
  serializer and publication-capability checks. OS principal:
  int-scl-010\parimal. Current parent permits own-record publication; this is
  procedural authority, not a source-write sandbox.
- Live GitHub issue-comment resolution established author ScalableParimal,
  OWNER association, original/updated time 2026-10-30T12:31:51Z, and actual
  governance-root adoption decision at issue 3 comment 6522916236. Its initial
  Audit authorization was not reused as the current stage start.
- Machine-derived SHA-256 and byte checks against the supplied six canonical
  input fingerprints, all structured bindings in the coordinator/Audit results,
  and the coordinator's historical baseline. Fresh baseline: 76 source files
  and 272 preexisting record files. These are endpoint integrity checks, not a
  new 52-core/seven-mechanism Audit.
- Own no-overwrite invocation publication using exclusive .partial preparation,
  native JSON complete-object parse/equality, flush/fsync and same-filesystem
  Windows MoveFileExW without replacement. A separate tool operation read it
  back and revalidated input/path sets before substantive affected-source
  comparison. Checkpoint 0001 binds that boundary.
- Targeted parsing of the large Audit evidence, actual citation/line checks,
  relevant prior-art binding checks, and final own-record serialization,
  cross-binding and source/prior-record endpoint checks.

These are evidence-gathering/record-integrity activities expressly permitted by
the scoped request. No product tests/builds/runtime, staging, Commit or Push
were executed.

### Source inspection evidence

Current required Skill, Agent, Guideline, Prompt, Request, relevant Master
authority/publication/recovery clauses, full directly affected optional-route
context, section 3.1 active-definition boundary, Audit finding/citations, and
the relevant linked clarification and historical dispositions were read.
The textual ambiguity, root cause and impact below are source-inspection
conclusions, not executed behavioral evidence.

### Reported evidence, integrity-checked but not re-performed

The upstream full Audit coverage/conclusions, historical Application outcome,
independent Verification PASS and Review PASS remain their originating actors'
conclusions. This actor validated relevant stored bindings and inspected the
needed source/evidence; it did not re-execute those processes. The coordinator's
explanation that its unpublished-helper flush diagnostic did not make the
completed Audit incomplete remains attributed historical evidence.

### Unverified

No actual authorization-record mutation, unauthorized Commit/Push, historical
runtime exercise of this optional path, authenticated original conversation
message ID/time, author intent, or exhaustive mutation/event history is
established. No such event is inferred from this wording.

### Current source status, qualification and recovery

Repository: ScalableParimal/SupportIQ, canonical local root
C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ; HEAD
57ed3afe8a14a41bdbe38d4df621a99c836a0f4c; branch
sdlc-framework-onboarding. Five preexisting tracked governance modifications and
the untracked records tree were retained; nothing was staged.
Current source fingerprints, not HEAD alone, bind the evaluated state.

Governance-root adoption was live-resolved at
https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236.
Existing same-work reservation and coordinator continuation were retained.
Masters match the root decision's three fingerprints and are bootstrap
comparison authority, not an adopted target Master baseline. Product root and
Master baseline remain unadopted. Governance section 3 explicitly permits
ordinary governed finding correction before adoption.

The actor is local-finding-investigation:
20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff.
The visible runtime label/ID for this task is Commit Record Ambiguity
Investigation / b7ff5557-b3f4-44b4-87e4-7c6f5cdfc705; this matching current
actor was not treated as a competing writer. The roster is not independent
authentication. Historical stale starts are not proof of liveness or completion.
The coordinator's two stale historical attempts remain preserved; its validated
terminal continuation establishes the current handoff. No conflicting live
write was identified in available observations; no lock or exclusive technical
control is claimed.

The repository Request is a reusable unfilled template, not an invented
approval. The actual scoped Human request and bound handoff supply the finding
inputs. Current approved product Requirement/Implementation Plan, product
architecture, task IDs and product approvals are NOT APPLICABLE to this
governance-only bootstrap investigation. No product artifact was inspected.
No new approval/adoption is inferred from hashes, a directory or a PASS.

## 5. Expected behavior

Artifact Governance section 33.1 permits only own authorized records and
prohibits modifying published final records in place. Traceability section
30.1 requires final no-overwrite publication, durable references, original
human decision preservation, linked later records, and exact state/subject
binding. Metadata never creates substantive authority.

Within those rules, an optional later commit-identity observation must be
recorded without rewriting the earlier Human authorization. The earlier exact
staged diff/list, Work ID, actions and YES decision must remain resolvable.
Any Push must still be expressly authorized and match the actual bound commit.
Human Acceptance and Commit/Push Authorization remain distinct; neither is
inferred from completion, Verification, Review or staged-diff confirmation.
A missing, ambiguous, stale or mismatched gate blocks action.

## 6. Actual behavior

Actual observed artifact behavior is textual, not an executed Commit/Push.
Section 43 line 1312 uses "append ... to this same authorization record" and
then "bound in the record" without a linked immutable-record explanation.
Line 1309 already requires that authorization record to exist before the
commit. Adjacent line 1314 preserves strict staging, reviewed-diff, explicit
path and action-authorization safeguards. Nothing in that context explicitly
resolves the later immutable-record handling.

The difference is the missing mapping between a preexisting published decision
and a later commit-identity observation, not absence of immutability at Master
level. The Agent's wording cannot override the Master or authorize an in-place
append. The optional route has not become required work.

## 7. Root cause

**Bounded cause established by source inspection:** section 43 item 2 uses
"same authorization record" across two distinct lifecycle moments without
distinguishing immutable authorization bytes from a logical gate and its linked
post-commit evidence. Its Push condition repeats the unresolved single-record
reference. This is a local cross-document instruction-integration omission in
the governance mechanism, not a product implementation, schema, environment,
test or Master-authority defect.

Symptom: plausible in-place-append reading conflicts with final-record
immutability. Cause: missing explicit immutable linkage/lifecycle semantics.
Who introduced the text, original intent, and any actual harmful execution
cannot be determined from available evidence and are not needed to validate
this limited ambiguity.

Relevant prior art does not transfer authority: the 3438-byte linked
GOV-AUD-20261102-001 clarification preserved the original report/result and
recorded new metadata separately. Its completed Application and separately
initiated Verification/Review PASS demonstrate an existing record-preserving
pattern, not approval of a commit-authorization mechanism. Historical GOV-001
and GOV-002 remain accepted NO PLAN CHANGE REQUIRED; neither is reopened.
The failed earlier Application remains failed with no published payload; it is
not retroactively converted to success or reused as authorization.

## 8. Impact assessment

- **Affected correction surface:** Remediation Agent section 43, optional
  post-completion item 2 and its dependent Push-binding wording, in full
  context of item 1, line 1309 and line 1314. No Master edit is indicated.
- **Risk:** a future literal implementation could mutate a Human decision
  record, weaken immutable evidence, or block an otherwise authorized optional
  Push because the record-handling route is unclear. These are prospective
  risks, not observed incidents; Low / Ambiguity remains proportionate.
- **Production/API/schema/migration/infrastructure/security architecture:**
  no product change indicated. No technical access-control change or new
  persistence category/root is required. Human authorization/evidence
  integrity is the relevant governance boundary.
- **Requirement/Plan:** product Requirement and Implementation Plan are N/A.
  Corrective Decision must formally determine the governance artifact change
  and applicable plan disposition; this investigation does not issue it.
- **Tests/assurance:** no product tests are needed for textual confirmation.
  Any approved future correction needs scoped semantic checks of immutable
  original decision preservation, linked commit identity, exact subject/state
  and permitted actions, blocked missing/stale/mismatched authorization, and
  unchanged optionality/Acceptance separation; then the required independent
  Verification, independent Review and complete Governance Audit.
- **Operation/compatibility:** do not migrate or rewrite historical records.
  Preserve original authorization and exact staged-diff binding. New metadata
  must not imply authorization of a later different diff, commit or action.
- **Authority:** section 3.1 applies to any active Remediation definition
  change; inclusion in mechanism scope is not application authority.
- **Current cycle:** unresolved finding means no clean final Audit,
  Remediation completion, effectiveness or baseline/product adoption claim.

## 9. Corrective options

These are advisory directions, not selected/approved policy or an exact patch.

### Option A - clarify a linked immutable post-commit evidence route

Clarify the local Agent wording so an authorized actor records the resulting
full commit identity in a new linked immutable record within the already
permitted attempt/gate convention, referencing the unchanged original
authorization by path, identity and fingerprint and retaining its exact
staged-diff/list, Work ID and action bindings. Clarify the dependent Push
condition to resolve that chain rather than require editing original bytes.
Do not treat later evidence as a new YES or as expanded authorization.

Affected component: section 43 local wording only; no Master or historical
record edit indicated. Production, product tests, product architecture,
Requirement/Plan and migration/schema impacts are N/A; assurance is governance
semantic and required independent gates. Operational impact is an explicit
later linkage; low complexity. Risk is weak or circular linkage, authority
inflation, or accidental weakening of Push checks. Limitation: the exact
publisher/record placement and final wording must be settled by governed
decision and exact Human Approval, not this report. Use existing record types
and roots; do not create a mutable registry or new authority.

### Option B - explicitly separate commit authorization and later Push decision

Retain an immutable pre-commit authorization; where Push is wanted, obtain and
publish a separate linked Human decision for the actual resulting commit
before Push, through the existing gate convention. Preserve the staged-diff
binding and original decision; do not silently supersede it. This is a feasible
but larger workflow policy change rather than merely explaining how an
already-authorized action receives its later evidence.

Affected component: section 43 item 2/action-gate semantics and related
instructions only if the later decision identifies a necessary dependency.
No product production/API/schema/architecture, Requirement/Plan, migration or
runtime-test change is indicated. Governance assurance must additionally
exercise the two-decision sequence and no implicit transfer of Commit to Push
authority. Operational impact: more Human interaction and possible optional
Push delay; moderate complexity relative to A. Risks: unnecessary extra gate,
stale decision mismatch, or treating the later response as blanket authority.
Limitation: it changes current optional-route policy and therefore needs
explicit Human choice; investigation cannot impose it.

Leaving the text unchanged is not a corrective solution to the confirmed
ambiguity. Delaying or never invoking optional Commit/Push avoids exercising
the route but does not clarify the governance artifact.

## 10. Recommended option

**Recommend Option A**, advisory only. It reconciles the local wording with
already-existing immutability and traceability rules with the least policy
change, keeps Commit/Push optional, and preserves distinct Acceptance,
authorization, exact staged content and permitted-action checks.

Expected impact: a clear prospective immutable evidence chain, no source-wide
redesign and no historical rewriting. Risks and assurance needs are those
listed under A. Product Requirement/Plan and product architecture impact:
N/A. Exact text, publisher designation, permitted record location, approval
scope and implementation authorization are deliberately not supplied here.
Human decision/exact approval is required before any governance change.

## 11. Human decision requirement

**Required.** Route FINDING GOV-AUD-20261102-002 to the existing Corrective
Change Decision & Plan Update process for its acceptance/rejection,
governance-artifact disposition, bounded corrective direction and approval
requirements. This report's confirmation/recommendation is not that decision.

Any future amendment of the active Remediation Agent definition remains
subject to section 3.1: exact attributable Human Approval binding target/base/
expected-after fingerprints, scope/exclusions and application route/actor.
No self-authorization, future-definition authority or approval transfer is
permitted. Required distinct application/independent assurance and complete
Audit gates remain. No current Commit/Push, source edit, adoption, product work,
or next-stage initiation is authorized.

## 12. Remaining uncertainties and limitations

- Actual historical mutation, unauthorized Commit/Push, author intent and
  runtime behavior cannot be determined from available evidence. No defect
  beyond the bounded textual ambiguity is asserted. Actual incident attribution
  would require a separately authorized event/decision/repository history
  investigation, not expansion of this task.
- Final linked-record publisher/placement, exact wording and whether Human
  selects A or B remain for Corrective Decision and approval.
- Human start is attributable only to the actual supplied parent-conversation
  instruction; no authenticated message ID/time is exposed.
- Nonmutation is procedural, not sandbox-enforced. Endpoint hashes cannot
  exclude transient writes or same-principal tampering. No exhaustive trusted
  event log or continuous exclusive-writer observation is available.
- Host clock samples describe preparation, not exact filesystem publication.
- Historical conclusions are retained as reported, not re-performed or
  retrospectively repaired. Legacy historical metadata/encoding limitations
  are not new findings here. Preparatory read/output-format failures had no
  source or final-record effects and did not waive publication ordering.
- No lossless original approval authentication, framework-wide clean result,
  adoption, current product readiness or measured performance saving is claimed.

## 13. Investigation outcome

**CORRECTIVE DIRECTION IDENTIFIED.**
Finding confirmed; bounded source-level cause sufficiently understood.
Affected artifact: .github/agents/sdlc-governance-remediation.agent.md,
section 43 Optional Post-Completion Commit item 2 and its dependent Push
reference. Related authority: Artifact Governance 33.1 and Traceability 30.1.
Recommendation: immutable linked later evidence, not editing the original
authorization. Human decision/exact approval required.

Investigation execution completed after the scoped comparison and report
requirements. This outcome is neither corrective approval nor Remediation/
Audit completion. Only own investigation records were published; no correction
or other stage was executed.

## 14. Recommended next process

Corrective Change Decision & Plan Update, subject type FINDING, for this finding
only, under the same Work ID and Cycle 1, **after a separate fresh explicit
Human stage-start** using this canonical report and its bound result.

Exact next Human start gate:

> Yes, initiate Corrective Change Decision & Plan Update for FINDING GOV-AUD-20261102-002 only under Work ID 0061148a-1b62-4d25-adff-e7f2318dbfad, GOV-REMEDIATION-PROSPECTIVE-001 Cycle 1, using Finding Investigation attempt 20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff and its canonical report.md/result.json; prepare the bounded governance clarification decision only. No correction, application, other stage, adoption, Commit or Push is authorized.

This is an initiation request only, not a substantive decision/approval request.
STOP. No next process is initiated by this investigation.

## Machine-derived reference bindings

Every byte count and SHA-256 below was computed from the actual named file.
The table is a reference index, not another canonical report.

| Actual repository-relative path | Bytes | SHA-256 |
|---|---:|---|
| `.github/agents/finding-investigation.agent.md` | 4011 | `BECE1D3F5C20DD10B975E1536BB816232A47C2B43FDAAD76B13C4328DA84B218` |
| `.github/skills/finding-investigation/SKILL.md` | 10312 | `800D316A3AA97BFB3B2A3581FE16F8474C6DA2A199E3EB9CF397D3B7B2081448` |
| `docs/ai/guidelines/FINDING_INVESTIGATION_GUIDELINES.md` | 14928 | `14844FB1FA9865AB870CA1E3E8A50CD319756B2C8EA45231199B09368CC31BD2` |
| `docs/ai/prompts/FINDING_INVESTIGATION_PROMPT.md` | 3596 | `7550968BAAD60A9214C1E1C7E5476D6270EF99FE3D17E4F85E5D20CAD26D8175` |
| `docs/ai/request/FINDING_INVESTIGATION_REQUEST.md` | 1854 | `836F79EE60357C502A2181E8CB4B04D500C351219358E484C0639A9FD275C120` |
| `.github/agents/sdlc-governance-remediation.agent.md` | 48379 | `EBFE9E9A369F2FA367F7A4728893106338DBDB6245A2016E2A248E7228148153` |
| `docs/ai/sdlc/SDLC_GOVERNANCE.md` | 30926 | `79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B` |
| `docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md` | 54243 | `6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860` |
| `docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md` | 89025 | `08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/report.md` | 19130 | `0E819BDD31747BA24037C89130D1A25A8E642A7EB0BBF9DF267C34DBD815C768` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/result.json` | 7103 | `F65D96FC76105E4546CC5318BF7D3E4A8E41784486449BE3CE55726840CE2AD2` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/attachments/investigation-handoff.md` | 7361 | `59436AEE6D74EC483B89B62F190D6330B85241CB3359D126EFED31EEC43627B3` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565/attachments/validation.json` | 55730 | `0F7EEC40394147298283F62EDBF75E5F386AA3CA4AD55880D97FC695A3468B3F` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f/report.md` | 55902 | `4246B0BAA6A945678034706AE02E26162CD2DB940D8FAC3F2AB7749D76B477A2` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f/result.json` | 27489 | `3C628AA7BC8ECDF2194EC5FBA13911BB183B45A0BBA4CD57E81CF4B4FBF23231` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f/evidence/audit-evidence.json` | 4819789 | `888ABF5B0E14829F0EC2FF824510DB1E3B8DB3CC1636F29B3DD6E44DF5104AF2` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/attempt.json` | 103790 | `7BC95DB647253D1C99699E3B4905A43E6BC4F4D1C80E2BCF247C36DFB1018710` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/checkpoint-0001.json` | 1750 | `8A5522237BCC76F74D2BD7F5CEBFFCA0737D8ACC679DBC0874DFD9A772E3FA90` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0/report.md` | 12795 | `CE975EE00E642B93AF50EF8FF0FF418101CE821F2E94121D43E0B260A012BF6B` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0/result.json` | 3945 | `080C02F1FD262C1690261A0E74505C7AEC6EA9ACBBDFFFDF58BAB91759826F54` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37/report.md` | 10314 | `797566DC7A0C7A39186095A226986D59E4F46A75123E9C0133F388E042663E94` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37/result.json` | 3111 | `D7EF1315E9631CBBAA7448B80541A89FC64029B89ED246B77E979F745B2783AD` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd/report.md` | 6380 | `26EEC34BAB50AD8A67FEBDAC262D9A723700807C5BA27FBD932668CE16AB2B88` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd/result.json` | 33474 | `8F9AEF423A96167C8A6247266F26989A22AB331FB033D7280AB8C46127359CD9` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1/report.md` | 15150 | `A1388E49A5F107443FAF3E5E32D4FDFB5B9C8CBC5EA4D4EBD4B56967E695B7E0` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1/result.json` | 19616 | `D3F3680DA22EA8538482D1E5F7B6FACFD0A41A7C2D89E2E0369981311B4DFB43` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb/report.md` | 17061 | `27A8D83B6B9D05E847B89DC07773CD2EB4362A64DA122198C9205793B446BF44` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb/result.json` | 68261 | `E404F5B77FF317D431DFB3E6B8BF05FF6151480AFFE0ECA083AAED1DB9C41D1D` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd/attachments/GOV-AUD-20261102-001-linked-clarification.md` | 3438 | `8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA` |
| `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/attachments/evidence.json` | 52180 | `9D84E95108116DEBDAA4677BA1FF43D5878E9A2CD8D09CF64EFB19DDB95E2A74` |

Canonical result path: `docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts/20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff/result.json`; identity `20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff:investigation_result`. It is published after this report and binds its final bytes. This report does not assert its own or its later result's future digest.
