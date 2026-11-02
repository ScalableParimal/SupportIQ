import os, sys, json, pathlib, hashlib, subprocess, datetime, ctypes
ROOT = pathlib.Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
os.chdir(ROOT)
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
AID = "20261102T095721Z-41a83464-3195-451d-b548-d1b60f72c62f"
BASE = pathlib.Path("docs/sdlc-records/governance") / WORK / "attempts"
OWN = BASE / AID
ROLE = "SDLC Governance Audit"
ACTOR = "d3ddb004-dc45-4b54-a491-1541f446762b"
REVIEW = "20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb"
VERIFY = "20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1"
APPLICATION = "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd"
START = "Yes, initiate the complete Governance Audit under the existing Work ID and prospective Remediation cycle using the completed clarification, Verification PASS and Review PASS"
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):
    return hashlib.sha256(b).hexdigest().upper()
def ref(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(b),"sha256":digest(b)}
def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8-sig"))
def cmd(*args):
    return subprocess.check_output(args, text=True, encoding="utf-8", errors="strict").strip()
def metadata(kind):
    return {"schema_version":"1.0","record_type":kind,"record_id":AID+":"+kind,
            "work_id":WORK,"attempt_id":AID,"creator":ACTOR,"role":ROLE,"process":ROLE,
            "cycle_id":"GOV-REMEDIATION-PROSPECTIVE-001","cycle_number":1,
            "created_at_utc":now(),"clock_basis":"Python current UTC preparation sample, not publication time"}
def encode(o):
    b=(json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8")
    assert json.loads(b)==o
    assert b"\xef\xbb\xbf" != b[:3] and not b.endswith(b"\n\n")
    assert b"\\`n" not in b
    return b
def publish(p,o):
    p=pathlib.Path(p)
    assert p.is_relative_to(OWN),p
    assert not p.exists(),p
    b=encode(o) if not isinstance(o,bytes) else o
    partial=p.with_name(p.name+".partial")
    p.parent.mkdir(parents=True,exist_ok=True)
    with partial.open("xb") as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert partial.read_bytes()==b
    os.rename(partial,p) # Windows same-filesystem MoveFile, no replacement.
    assert p.read_bytes()==b
    return ref(p)
def source_paths():
    return sorted([p for base in ["docs/ai",".github/agents",".github/skills"]
                   for p in pathlib.Path(base).rglob("*.md")])
def snapshot():
    # Governance inputs/records only. Product artifacts are not opened.
    paths=source_paths()+[p for p in pathlib.Path("docs/sdlc-records/governance").rglob("*")
                         if p.is_file() and not p.is_relative_to(OWN)]
    return [ref(p) for p in sorted(set(paths))]
def checkref(r):
    actual=ref(r["path"])
    assert actual["sha256"]==r["sha256"].upper(),(r,actual)
    if "bytes" in r and r["bytes"] is not None: assert actual["bytes"]==r["bytes"],(r,actual)
    return actual
def selftests():
    native={"scope":{"before":{"exists":False,"bytes":None,"sha256":None},"roles":["a","b","c","d"]},
            "approval":"Yes; § and ? remain distinct","complete":True}
    assert json.loads(encode(native))==native
    assert isinstance(json.loads(encode(native))["scope"]["roles"],list)
    assert digest("§".encode())!=digest("?".encode())
    return {"native_complete_object_roundtrip":True,"list_not_tuple":True,
            "null_and_boolean_preserved":True,"unicode_distinct":True,
            "strict_utf8_no_BOM_one_final_LF":True}
def preflight():
    assert cmd("git","rev-parse","--show-toplevel").lower().replace("\\","/")==ROOT.as_posix().lower()
    assert cmd("git","rev-parse","HEAD")=="57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    masters={"SDLC_GOVERNANCE.md":"79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
             "SDLC_ARTIFACT_GOVERNANCE.md":"6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
             "SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md":"08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C"}
    for name,h in masters.items(): assert ref(pathlib.Path("docs/ai/sdlc")/name)["sha256"]==h
    rr=load(BASE/REVIEW/"result.json");vr=load(BASE/VERIFY/"result.json")
    for o,n in [(rr,12),(vr,13)]:
        assert o["outcome"]=="PASS" and o["execution_status"]=="COMPLETED"
        assert len(o["criteria"])==n and all(c["outcome"]=="PASS" for c in o["criteria"])
        checkref(o["report"]);checkref(o["evidence"])
    assert not rr["unresolved_Review_findings"] and not vr["unresolved_verification_findings"]
    expected={REVIEW:("27A8D83B6B9D05E847B89DC07773CD2EB4362A64DA122198C9205793B446BF44","E404F5B77FF317D431DFB3E6B8BF05FF6151480AFFE0ECA083AAED1DB9C41D1D"),
              VERIFY:("A1388E49A5F107443FAF3E5E32D4FDFB5B9C8CBC5EA4D4EBD4B56967E695B7E0","D3F3680DA22EA8538482D1E5F7B6FACFD0A41A7C2D89E2E0369981311B4DFB43")}
    for aid,hs in expected.items():
        for name,h in zip(["report.md","result.json"],hs):assert ref(BASE/aid/name)["sha256"]==h
    assert not (pathlib.Path("docs/sdlc-records/product")/WORK).exists()
    q=metadata("current_invocation_qualification")
    q.update(repository={"canonical":"ScalableParimal/SupportIQ","root":str(ROOT),
        "HEAD":cmd("git","rev-parse","HEAD"),"branch":cmd("git","branch","--show-current"),
        "origin":cmd("git","remote","get-url","origin"),"status":cmd("git","status","--porcelain=v1"),
        "index_fingerprint":ref(".git/index") if pathlib.Path(".git/index").is_file() else None},
        identity={"agent_id":ACTOR,"role_definition":ref(".github/agents/sdlc-governance-audit.agent.md"),
          "effective_OS_identity":cmd("whoami","/user"),"process_id":os.getpid(),
          "separation":"Current Audit invocation distinct from preparer/application/verifier/reviewer/coordinator; shared writable OS principal, not isolation",
          "registry_observation":"Only running Post Clarification Full Audit d3ddb004-dc45-4b54-a491-1541f446762b is this invocation. 27 prior actors idle; no competing writer observed."},
        capabilities={"python":sys.version,"nonmutating_read":True,"SHA256":True,"strict_native_JSON":selftests(),
          "publication_route":"Windows same-filesystem os.rename(partial,final), fails if final exists; xb partial, fsync, validate and readback",
          "scope_acl":cmd("powershell","-NoProfile","-Command","(Get-Acl '"+str(BASE)+"').AccessToString"),
          "access_check":os.access(BASE,os.R_OK|os.W_OK|os.X_OK),
          "not_sandboxed":True},
        authorization={"actual_wording":START,"source":"Actual fresh Human stage-start supplied in current user request","platform_message_id":None,
          "authenticated_time":None,"not_substantive_approval":True},
        root_decision={"url":"https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
          "id":6522916236,"author":"ScalableParimal","author_association":"OWNER","created_at":"2026-10-30T12:31:51Z",
          "updated_at":"2026-10-30T12:31:51Z","current_resolution":"github issue_read get_comments during this invocation; body unchanged, exact HEAD and three Master fingerprints match",
          "use":"Established governance-root adoption only; initial one-time stage-start not reused"},
        source_manifest=[ref(p) for p in source_paths()],preservation_manifest=snapshot(),
        predecessors=[ref(BASE/a/n) for a in [REVIEW,VERIFY,APPLICATION] for n in ["attempt.json","report.md","result.json"]],
        recovery={"existing_work_id":True,"no_first_use_rebootstrap":True,
          "historical_nonterminal_attempts":["20261031053750Z-5a67f304-e4e5-4045-8721-235a47779233","20261031T045348Z-a8d815b9-c331-44ca-b9b1-cc5ea5bdbde6"],
          "disposition":"Retained historical incomplete/malformed records, not inferred completed or live. Prospective cycle admission and later strict record-first investigation/decision reconcile current continuation; read and assess actual cycle evidence after record-first.",
          "failed_Application":"20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31 terminal failure preserved; exact retry predecessor completed and assured"},
        limitations=["Procedural nonmutation, not enforced sandbox","No exhaustive event log or coordinated no-edit window",
          "Endpoint manifests cannot exclude transient writes or same-principal tampering","Governance content only; product artifacts not inspected",
          "No exact filesystem publication timestamps captured; clocks describe preparation"])
    assert q["capabilities"]["access_check"]
    qr=publish(OWN/"evidence/qualification.json",q)
    a=metadata("audit_invocation")
    a.update(actor_identity=q["identity"],scope={"stage":"complete Governance Audit","core_expected":52,"mechanisms_expected":7,
       "source_inventory_observed":len(q["source_manifest"]),"output_scope":OWN.as_posix(),
       "excluded":["corrections","nested stages","product artifacts","commit","push","baseline/product-root adoption"]},
       repository_context=q["repository"],authorization=q["authorization"],root_decision=q["root_decision"],
       qualification=qr,predecessors=q["predecessors"],task_context="Governance only; no product task",
       execution_status="STARTED",outputs={"canonical_report":(OWN/"report.md").as_posix(),"result":(OWN/"result.json").as_posix()})
    assert snapshot()==q["preservation_manifest"]
    ar=publish(OWN/"attempt.json",a)
    print(json.dumps({"qualification":qr,"invocation":ar,"next":"Separate process readback BEFORE substantive assessment"}))
FAMILIES = [
 ("REQUIREMENT_ANALYSIS","requirement-analysis","Analysis only; unresolved business decisions remain Human; verification then Requirement Approval."),
 ("REQUIREMENT_ANALYSIS_VERIFICATION","requirement-analysis-verification","Independent complete current analysis/resulting Requirement verification; no update or approval."),
 ("IMPLEMENTATION_PLANNING","implementation-planning","Current approved Requirement; plan only; concurrency/dependency/checkout assessment; separate review/plan gates."),
 ("REQUIREMENT_UPDATE","requirement-update","Explicit Human decisions; immutable new Requirement version, status in records; downstream analysis/verification/approval; Skill-only."),
 ("IMPLEMENTATION_PLAN_VERIFICATION","implementation-plan-verification","Independent complete plan check including concurrency; task IDs contextual; no plan edit or approval."),
 ("IMPLEMENTATION","implementation","Approved Requirement and Plan, approved mode/coordination; bounded implementation and self-check; no upstream edits or acceptance."),
 ("IMPLEMENTATION_VERIFICATION","implementation-verification","Complete current implementation independently verified; evidence classes and gaps; no correction or acceptance."),
 ("IMPLEMENTATION_REVIEW","implementation-review","Complete engineering review distinct from Verification and Human Acceptance; read-only; route concerns."),
 ("FINDING_INVESTIGATION","finding-investigation","Diagnostic/read-only; artifact-specific relevant context; findings and non-finding enhancements separated."),
 ("CORRECTIVE_CHANGE","corrective-change-decision","Disposition/proposal only; exact approvals and distinct actors; no direct corrective application; defined no-change status.")
]
def core_inventory():
    rows=[dict(ref(p),layer="Master",family=p.stem,conclusion="PASS",
               rationale="Lifecycle, authority, publication and traceability comparison authority; candidate, not adopted.")
          for p in sorted(pathlib.Path("docs/ai/sdlc").glob("*.md"))]
    for stem,slug,reason in FAMILIES:
        for layer,p in [("Guideline",pathlib.Path("docs/ai/guidelines")/(stem+"_GUIDELINES.md")),
                        ("Prompt",pathlib.Path("docs/ai/prompts")/(stem+"_PROMPT.md")),
                        ("Request",pathlib.Path("docs/ai/request")/(stem+"_REQUEST.md")),
                        ("Skill",pathlib.Path(".github/skills")/slug/"SKILL.md")]+(
                       [] if stem=="REQUIREMENT_UPDATE" else [("Agent",pathlib.Path(".github/agents")/(slug+".agent.md"))]):
            rows.append(dict(ref(p),layer=layer,family=stem,conclusion="PASS",rationale=reason))
    assert len(rows)==52 and len({r["path"] for r in rows})==52
    return rows
def governance_links():
    import re
    results=[]
    for p in source_paths():
        t=p.read_text(encoding="utf-8-sig").replace("\\","/")
        for target in sorted(set(re.findall(r"(?:docs/ai/|\.github/)[A-Za-z0-9_./-]+(?:\.md|/)",t))):
            # Regex may consume a trailing punctuation period, never product contents.
            target=target.rstrip(".")
            exists=pathlib.Path(target).exists()
            results.append({"source":p.as_posix(),"target":target,"exists":exists,"outcome":"PASS" if exists else "UNRESOLVED"})
    return results
def nested_bindings(o,source):
    results=[]
    def walk(x,loc="$"):
        if isinstance(x,dict):
            p=x.get("path");h=x.get("sha256")
            if isinstance(p,str) and isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdefABCDEF" for c in h):
                r={"source":source,"object_location":loc,"expected":x}
                try:
                    effective=dict(x)
                    if not pathlib.Path(p).exists() and len(pathlib.Path(p).parts)==1:
                        effective["path"]=(pathlib.Path(source).parent/p).as_posix()
                        r["resolution"]="Actor-record-relative basename, resolved under originating result directory"
                    r.update(actual=checkref(effective),outcome="PASS")
                except Exception as e:r.update(outcome="MISMATCH",error=str(e))
                results.append(r)
            for k,v in x.items():walk(v,loc+"."+k)
        elif isinstance(x,list):
            for n,v in enumerate(x):walk(v,loc+"["+str(n)+"]")
    walk(o)
    return results
def inspect_bindings():
    pairs=[(REVIEW,"result.json"),(REVIEW,"evidence/review-evidence.json"),
           (VERIFY,"result.json"),(VERIFY,"evidence/verification-evidence.json"),
           (APPLICATION,"result.json"),(APPLICATION,"evidence/application-evidence.json"),
           ("20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed","attachments/exact-recovery-approval-request.json"),
           ("20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed","result.json"),
           ("20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0","result.json"),
           ("20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37","result.json"),
           ("20261102T075750Z-1210d4b1-8300-4b17-8f6b-911a2f64958e","result.json"),
           ("20261102T084120Z-84eb5d6a-4ec3-4c1f-9122-17edda7c6d51","result.json"),
           ("20261031T072633Z-4c6c7de5-037e-49d1-a594-97b7ef0c5319","result.json"),
           ("20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55","result.json"),
           ("20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694","result.json"),
           ("20261030T161112Z-9c79d789-1b9a-479c-a9e7-6e692747330f","result.json"),
           ("20261031T043137Z-7d2b35df-98a6-4d50-8761-48fe0f724e0f","result.json"),
           ("20261102T082552Z-6dfe39f3-18aa-40b8-88be-56850b13b291","result.json")]
    results=[]
    for aid,name in pairs:
        p=BASE/aid/name
        results+=nested_bindings(load(p),p.as_posix())
    return results
def semantic_checks():
    app=load(BASE/APPLICATION/"result.json")
    request=load(BASE/"20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed"/"attachments/exact-recovery-approval-request.json")
    v=load(BASE/VERIFY/"evidence/verification-evidence.json")
    r=load(BASE/REVIEW/"evidence/review-evidence.json")
    assert app["approved_scope_complete"]==request["scope"]==r["approved_scope_complete"]
    assert app["before"]["presence"]=="ABSENT" and app["before"]["sha256"] is None and app["before"]["bytes"] is None
    target=pathlib.Path(app["after"]["path"]);payload=pathlib.Path(request["scope"]["payload_source"]["path"])
    b=target.read_bytes()
    assert b==payload.read_bytes() and len(b)==3438
    assert digest(b)=="8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
    assert b.isascii() and b"\r" not in b and b.endswith(b"\n") and not b.endswith(b"\n\n")
    assert app["actual_substantive_path_list"]==app["approved_substantive_path_list"]==[target.as_posix()]
    roles=request["scope"]["roles"]
    assert len(roles)==4
    # Native role objects retained, not reduced to names.
    original=BASE/"20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0"
    assert ref(original/"report.md")["sha256"]=="CE975EE00E642B93AF50EF8FF0FF418101CE821F2E94121D43E0B260A012BF6B"
    assert ref(original/"evidence/investigation-evidence.json")=={
      "path":(original/"evidence/investigation-evidence.json").as_posix(),"bytes":22254,
      "sha256":"8D008604EFEC599AC751EB1B457FD72750E3B4ECB7E0B5071087E64F1A67F977"}
    failed=BASE/"20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31"
    assert not (failed/"attachments/GOV-AUD-20261102-001-linked-clarification.md").exists()
    expected={
      "docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md":"A0D0C5E8826305937A3E82DD2B39A805D329740D95C3068E913BB986F3697208",
      "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md":"D82D8CD812DF36A9F1D049485107986C5BEA8685F87595A84BD7A9239D3B25F8",
      "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md":"257E8F8FBCEFD31A8211CC2C24930D2E83783C1D358659A4BC2F26ADF547D902",
      "docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md":"9F2C3B2379DD5E9371DC5A2BE1028CB7BD918EDF6FA81557BC266EE63AA49B97",
      "docs/ai/request/INDEPENDENT_GOVERNANCE_REVIEW_REQUEST.md":"0809F2006DF7485033DC340571BD390AFF04E0A31C2B545DA98A96F132CC77BA"}
    assert set(cmd("git","diff","--name-only").splitlines())==set(expected)
    assert not cmd("git","diff","--cached","--name-only")
    for p,h in expected.items():assert ref(p)["sha256"]==h
    # Independently reconstruct the five historical exact changes from frozen before bytes.
    import re
    oldapp=BASE/"20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55"
    olde=load(oldapp/"evidence/application-evidence.json")
    proposal=(BASE/"20261030T142338Z-2a4c9f75-42df-4f80-a5c7-0d5b845b890a"/"report.md").read_text(encoding="utf-8-sig")
    approved=json.loads(re.search(r"```json\s*(.*?)```",proposal,re.S).group(1))
    reconstruction=[]
    for op,recorded in zip(approved,olde["target_manifest"]):
        for key in ["operation","target_path","base_sha256","expected_after_sha256","old_utf8","new_utf8"]:
            assert op[key]==recorded[key]
        before=pathlib.Path(recorded["before_evidence"]["path"]).read_bytes()
        after=pathlib.Path(recorded["after_evidence"]["path"]).read_bytes()
        old=op["old_utf8"].replace("\r\n","\n").replace("\n","\r\n").encode("utf-8")
        new=op["new_utf8"].replace("\r\n","\n").replace("\n","\r\n").encode("utf-8")
        assert before.count(old)==1
        assert before.replace(old,new,1)==after==pathlib.Path(op["target_path"]).read_bytes()
        assert digest(before)==op["base_sha256"] and digest(after)==op["expected_after_sha256"]
        reconstruction.append({"operation":op["operation"],"target":ref(op["target_path"]),
          "before":ref(recorded["before_evidence"]["path"]),"after":ref(recorded["after_evidence"]["path"]),
          "single_exact_approved_replacement":"PASS"})
    context=load(oldapp/"evidence/approval-context.json")
    original_response=context["exact_approval_verbatim"]
    linked=BASE/"20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694"/"attachments/IGV-FIND-001-approval-transcription-correction.md"
    attributed=next(l[2:] for l in linked.read_text(encoding="utf-8").splitlines() if l.startswith("> I approve the exact report"))
    diffs=[{"offset":i,"original_codepoint":ord(a),"attributed_codepoint":ord(b)}
           for i,(a,b) in enumerate(zip(original_response,attributed)) if a!=b]
    assert diffs==[{"offset":27,"original_codepoint":63,"attributed_codepoint":167},
                   {"offset":42,"original_codepoint":63,"attributed_codepoint":167}]
    assert len(original_response)==len(attributed)==133
    assert digest(original_response.encode())=="B56EFD8E79335C945F829E267E977398B0E685347B86019A18ABE3A48573DE19"
    assert digest(attributed.encode())=="F64D83824A1A31FA470FAC6FC36631F5687B468F6EC9DA777C2EFD0253ECF085"
    return {"scope_complete_native_equality":True,"approved_scope":request["scope"],
      "actual_approval_and_start":app["actual_approval_and_separate_stage_start"],
      "before":app["before"],"after":app["after"],"payload_exact_binary_equality":True,
      "four_actor_native_bindings":roles,"original_preserved":ref(original/"report.md"),
      "line15_resolved":ref(original/"evidence/investigation-evidence.json"),
      "old_failed_attachment_absent":True,"P1_P5_exact_current_state":[ref(p) for p in expected],
      "original_five_change_reconstruction":reconstruction,"response_codepoint_differences":diffs,
      "Verification_criteria":[{"criterion":c["criterion"],"outcome":c["outcome"],"title":c["title"]} for c in v["criteria"]],
      "Review_criteria":[{"criterion":c["criterion"],"outcome":c["outcome"],"title":c["title"],"reasoning":c["reasoning"]} for c in r["criteria"]],
      "current_inputs_unchanged":snapshot()==load(OWN/"evidence/qualification.json")["preservation_manifest"]}
FINDING = {
 "finding_id":"GOV-AUD-20261102-002","severity":"Low","category":"Ambiguity",
 "source_document":".github/agents/sdlc-governance-remediation.agent.md",
 "source_section":"43 Completion Report / Optional Post-Completion Commit, item 2",
 "related_document":"docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
 "related_section":"33.1 Publication of Existing Governed Process Records; also Traceability 30.1 Publication and incomplete writes",
 "issue":"The optional post-completion route requires authorization records to exist before Commit/Push, then directs appending the resulting commit identity to the same authorization record without specifying an immutable linked-record route.",
 "evidence":[
   "Before any Commit or Push under this section, both of the following separate, attributable human-gate records must exist under the Work ID",
   "After creating an authorized commit, append the full resulting commit identity to this same authorization record.",
   "Published final records must not be modified in place. Draft preparation is limited to the actor's own designated unpublished output. Subsequent corrections or supersession must use linked new records under the applicable governed process."],
 "impact":"Limited prospective record-handling ambiguity in an optional, uninvoked post-completion route. A literal in-place append would violate final-record immutability; a compliant linked successor may be intended but is not stated. No actual authorization mutation, unauthorized commit or push is established.",
 "recommended_resolution":"Through Finding Investigation and Corrective Change Decision, clarify how a later commit identity is added by an authorized linked new immutable record while retaining the original authorization and exact staged-diff binding. Obtain required Human decision/exact approval before any change.",
 "human_decision_required":True,
 "human_decision_reason":"The audit cannot select or implement an unstated record-update convention or grant publication/commit authority. The responsible Human must decide any clarification through governed change control.",
 "not_a_reopening":"New source-text ambiguity; not historical GOV-001/GOV-002 or clarified GOV-AUD-20261102-001."
}
COUNTS={"Critical":0,"High":0,"Medium":0,"Low":1,"Ambiguities":1,
        "Broken References":0,"Missing Governance Controls":0,"Unsupported Governance Controls":0}
OUTCOME="CONSISTENT WITH MINOR FINDINGS"
def checkrow(cid,title,rationale,outcome="PASS"):
    return {"check_id":cid,"title":title,"outcome":outcome,"rationale":rationale}
def mechanism_matrix():
    masters=[ref(p) for p in sorted(pathlib.Path("docs/ai/sdlc").glob("*.md"))]
    def bundle(stem,slug):
        return [ref("docs/ai/guidelines/"+stem+"_GUIDELINES.md"),
          ref("docs/ai/prompts/"+stem+"_PROMPT.md"),ref("docs/ai/request/"+stem+"_REQUEST.md"),
          ref(".github/skills/"+slug+"/SKILL.md"),ref(".github/agents/"+slug+".agent.md")]
    def row(name,sources,checks,records,na=None):
        return {"group":name,"expected":1,"present":1,"assessed":1,
          "source_expected":len(sources)-3,"source_present":len(sources)-3,"source_assessed":len(sources)-3,
          "sources":sources,"checks":checks,"evidence_records":records,"runtime_non_applicability":na,
          "result":"FAIL" if any(c["outcome"]=="FAIL" for c in checks) else "PASS"}
    def records(aids):
        out=[]
        for aid in aids:
            for name in ["attempt.json","report.md","result.json"]:
                p=BASE/aid/name
                if p.exists():out.append(ref(p))
        return out
    ownrefs=[ref(OWN/"attempt.json"),ref(OWN/"evidence/qualification.json"),ref(OWN/"checkpoint-0001.json")]
    auditchecks=[
      checkrow("AUD01","Complete catalog","Actual unique inventory 52 core and 24 additional mechanism sources; all 52 assessed, no count inflation."),
      checkrow("AUD02","All seven groups and exact threshold","Seven separately assessed groups, eight counts; Low1 and Ambiguities1 exclude CONSISTENT/effectiveness."),
      checkrow("AUD03","Read-only and identity","Fresh qualified independent Audit, own scope only; source readers were bounded read-only evidence collection, not governed process stages."),
      checkrow("AUD04","Current canonical chain","Invocation/qualification separate-process readback precedes substantive work. Evidence then canonical report then result. Result binds final report/evidence; no self/future digest in report."),
      checkrow("AUD05","Limitations and subsequent handoff","Procedural conduct, no sandbox/exhaustive event log/no-edit window; final Remediation anchor is later, not an Audit prerequisite.")]
    remchecks=[
      checkrow("REM01","Scope/framework/catalog","Sections2/3/33 preserve same-framework 52+7, governance-only finding-led boundary and independence."),
      checkrow("REM02","Prospective cycle admission","20261031T072633Z Human admission identifies historical actual GOV001/GOV002 as new prospective subjects; not retroactive coordination."),
      checkrow("REM03","Actual cycle records","Strict record-first Investigation, no-additional-change Decision, coordination, prior full Audit, Low-finding routing, recovery and clarification assurance resolve actual predecessor chain."),
      checkrow("REM04","Human gates and application authority","Sections6-8/19/23/25/40 preserve exact approval, distinct actors and separately started stages; no product/self-approval/self-modification authority inferred."),
      checkrow("REM05","Handoff applicability","Actual source/report/result bindings recomputed; historical malformed/incomplete attempts not treated as live/successful; future final coordinator is not demanded now."),
      checkrow("REM06","Immutable optional authorization records","Section43 optional Commit/Push item2 says append commit identity to same existing authorization record; linked immutable publication route unspecified. GOV-AUD-20261102-002 remains unresolved.","FAIL")]
    orchchecks=[
      checkrow("ORC01","Fresh initiation","O6.1/O6.6/O9 require fresh response per start/retry/transition; no inferred/reused response."),
      checkrow("ORC02","Human authority","Artifact4.4 and O9 distinguish invocation interlock from formal Approval/Acceptance; no gate bypass."),
      checkrow("ORC03","Product-only/own records/concurrency","Orchestrator does not coordinate this amendment; product persistence and own interlock metadata, links rather than another actor publication, serialization/integration controls align.")]
    portchecks=[
      checkrow("PORT01","Five connected links/authority","Agent follows Skill; Skill uses Guideline/Prompt/Request under three Masters; five references resolve."),
      checkrow("PORT02","Entry and reassessment","Guideline3 preserves separate product-root/Master adoption, pre-first-SDLC entry and material-change reassessment; no automatic repeated invocation."),
      checkrow("PORT03","Evidence separation","Separate immutable source-framework/target-project identities, allowed paths/fingerprints and evidence classes; neither repository changed."),
      checkrow("PORT04","Blocker and concern routing","Human decides applicability of possible blockers; six concern classes, governance defect candidates do not self-create Audit findings; no target adaptation treated as framework finding."),
      checkrow("PORT05","Persistence/read-only/exclusions","Work ID reserved for executable requests; unassigned draft-only. No target contents inspected; outputs only authorized scope, no automatic Agent/product work.")]
    appchecks=[
      checkrow("APP01","All five definitions/current capability","All five present and aligned. Actual Application own qualification/readback and runtime evidence present, not inferred from definition."),
      checkrow("APP02","Four distinct identities/exclusions","Preparer/applier actual own attempts, verifier/reviewer planned definition-only until proper gates; actual later definitions match. Applier not Orchestrator/active barred Remediation."),
      checkrow("APP03","Exact approval and fresh start","Native complete scope equals exact recovery approval request; actual combined designation/approval and separate retry start retained, no platform identity/time invented."),
      checkrow("APP04","Bases before writes and exact path/bytes","Historical all-five frozen before/after images reconstruct from approved single replacements; current P1-P5 exactly match. Clarification base ABSENT with null hash/bytes, one exact new destination, approved 3438-byte payload."),
      checkrow("APP05","Readback/preservation/failed retry","Application record-first checkpoints, atomic no-overwrite results and per-target evidence bind exact output. Failed attempt preserved terminal; old attachment absent; no authority transferred or unauthorized target change observed."),
      checkrow("APP06","Bounded outcome","Application success not independent assurance, effectivity or adoption. Shared-principal/event limitations retained; no corrective work by this Audit.")]
    vchecks=[
      checkrow("VER01","Five definitions and independent identity","All five resolve; actual verifier differs from preparer/applier/reviewer and matches planned hash; own current qualification and first-publication records."),
      checkrow("VER02","Fresh initiation and predecessor","Separate Human start after complete Application; exact approval/proposal/application references and full native scope retained."),
      checkrow("VER03","Independent hashes/full actual changes","V01-V13 all supported PASS; actual evidence/result refs rehashed; target equality and complete five-path tracked change set independently reconfirmed by this Audit."),
      checkrow("VER04","Read-only/change/cross-document controls","Bounded full-input manifests, operation/checkpoint/final comparisons and authority/lifecycle/catalog/effectiveness assessments evidenced. No new risk-ack approval gate."),
      checkrow("VER05","Durable integrity and limitations","Own report/result/evidence bindings pass. Procedural nonmutation explicitly not technical write exclusion; cannot exclude transient/same-principal tampering.")]
    rchecks=[
      checkrow("REV01","Five definitions and independent identity","All five resolve; distinct reviewer matches approved planned binding, own qualified invocation after PASS Verification."),
      checkrow("REV02","Exact intent/scope/authority/gates","R01-R12 supported PASS; exact approval/application/proposal retained, no broader source change, self-approval or automatic stage invocation."),
      checkrow("REV03","Catalog/cross-document/effectiveness","Review checks 52+7 and same Masters, substantive clarification scope, non-Master amendment vs separate Master adoption; not replacement Verification."),
      checkrow("REV04","Durable integrity/read-only","Current native result/evidence references rehashed, procedural manifest/operation/final comparisons retained; no unresolved Review findings; limitations not security guarantees.")]
    return [
      row("Governance Audit",masters+[ref(".github/skills/sdlc-governance-audit/SKILL.md"),ref(".github/agents/sdlc-governance-audit.agent.md")],auditchecks,ownrefs),
      row("Governance Remediation",masters+[ref(".github/agents/sdlc-governance-remediation.agent.md")],remchecks,
        records(["20261031T072633Z-4c6c7de5-037e-49d1-a594-97b7ef0c5319","20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0",
          "20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37","20261102T075750Z-1210d4b1-8300-4b17-8f6b-911a2f64958e","20261102T084120Z-84eb5d6a-4ec3-4c1f-9122-17edda7c6d51"])),
      row("SDLC Process Orchestration",masters+[ref(".github/agents/sdlc-process-orchestrator.agent.md")],orchchecks,[],
        "Product Orchestrator not invoked. Direct Human-started governance roles and read-only Audit source collection are not Orchestrator starts. No product records inspected."),
      row("SDLC Portability Assessment",masters+bundle("PORTABILITY_ASSESSMENT","portability-assessment"),portchecks,[],
        "Not invoked; product root and target Master baseline unadopted. Definition conformance only; no runtime PASS or target-project content assessment inferred."),
      row("Governance Amendment Application",masters+bundle("GOVERNANCE_AMENDMENT_APPLICATION","governance-amendment-application"),appchecks,records([APPLICATION,"20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55","20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694"])),
      row("Independent Governance Verification",masters+bundle("INDEPENDENT_GOVERNANCE_VERIFICATION","independent-governance-verification"),vchecks,records([VERIFY,"20261030T161112Z-9c79d789-1b9a-479c-a9e7-6e692747330f"])),
      row("Independent Governance Review",masters+bundle("INDEPENDENT_GOVERNANCE_REVIEW","independent-governance-review"),rchecks,records([REVIEW,"20261031T043137Z-7d2b35df-98a6-4d50-8761-48fe0f724e0f"]))]
def recordrefs():
    names={
      "20261102T082552Z-6dfe39f3-18aa-40b8-88be-56850b13b291":["report-revision-0001.md","result.json","evidence/audit-evidence-revision-0001.json"],
      "20261102T092301Z-f9d89334-bb88-4964-9ddc-113629d7dfed":["report.md","result.json","attachments/exact-recovery-approval-request.json"],
      "20261102T090912Z-6020e838-a5e7-4bf0-9f6e-f24fcd1d1e31":["report.md","result.json","evidence/failure-evidence.json"],
      "20261102T085032Z-8be0cc46-2de4-4ea4-a24e-3d341030d824":["report.md","result.json"],
      "20261102T090405Z-a7fe416c-9a1d-4153-9c46-180a65e86436":["report.md","result.json"],
      APPLICATION:["report.md","result.json","evidence/application-evidence.json","attachments/GOV-AUD-20261102-001-linked-clarification.md"],
      VERIFY:["report.md","result.json","evidence/verification-evidence.json"],
      REVIEW:["report.md","result.json","evidence/review-evidence.json"]}
    out=[]
    for aid,ns in names.items():
        for n in ns:out.append(ref(BASE/aid/n))
    for g in mechanism_matrix():
        out+=g["evidence_records"]
    # Include retained role qualification, preflight, checkpoints, approval and target evidence,
    # bound natively by the upstream terminal results/evidence, not duplicate their report bodies.
    seen=set();unique=[]
    for r in out:
        if r["path"] not in seen:
            seen.add(r["path"]);p=pathlib.Path(r["path"])
            identity=None
            if p.suffix==".json":
                o=load(p);identity=o.get("record_id",o.get("record_identity"))
            r=dict(r,identity=identity or (p.parent.name+":"+p.name))
            unique.append(r)
    return unique
def parent_finding_evidence():
    p=pathlib.Path(FINDING["source_document"])
    lines=p.read_text(encoding="utf-8-sig").splitlines()
    related=pathlib.Path(FINDING["related_document"])
    sources=[(p,lines),(related,related.read_text(encoding="utf-8-sig").splitlines())]
    citations=[]
    for text in FINDING["evidence"]:
        matches=[{"path":path.as_posix(),"line":n,"quote":line}
                 for path,ls in sources for n,line in enumerate(ls,1) if text in line]
        assert len(matches)==1,(text,matches)
        citations+=matches
    return citations
def build_report(e,evidence_ref):
    q=load(OWN/"evidence/qualification.json")
    core=e["core_inventory"]
    text=[
      "# SDLC Governance Consistency Audit\n",
      "## Audit Summary\n",
      f"**Overall result: {OUTCOME}.** Completed full-scope Audit; not a scoped spot-check. This is an AI audit result, not Human Approval or Human Acceptance.\n",
      "| Required measure | Actual |\n|---|---:|",
      "| Total core artifacts expected | 52 |\n| Total core artifacts found | 52 |\n| Total core artifacts audited | 52 |"]
    text += [f"| {k} | {v} |" for k,v in COUNTS.items()]
    text += [
      "\nOne finding, GOV-AUD-20261102-002 (Low, Ambiguity). Low and Ambiguities count the same finding on severity and category axes, not two findings. Seven mechanisms assessed: six PASS, Governance Remediation FAIL. No unresolved evidence gap or unassessed source. This result is **not effectiveness-qualifying**.\n",
      "## Audit Scope\n",
      f"Repository: `ScalableParimal/SupportIQ`, `{ROOT}`; HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`, branch `sdlc-framework-onboarding`. Work ID `{WORK}`; prospective cycle `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1. Audit attempt `{AID}`; actor `{ACTOR}`.\n",
      f"Current invocation: `{OWN.as_posix()}/attempt.json`, SHA-256 `{ref(OWN/'attempt.json')['sha256']}`. Current qualification: `{OWN.as_posix()}/evidence/qualification.json`, SHA-256 `{ref(OWN/'evidence/qualification.json')['sha256']}`. Separate-process pre-assessment readback: `checkpoint-0001.json`, SHA-256 `{ref(OWN/'checkpoint-0001.json')['sha256']}` under this same attempt.\n",
      f"Fresh actual Human start: “{START}”. Source: actual current user-supplied instruction. Authenticated platform message ID and decision-event time unavailable; not invented. It is stage initiation only, not change approval/adoption.\n",
      "The OWNER decision at https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236 was freshly resolved through GitHub issue_read: author ScalableParimal, association OWNER, ID6522916236, created/updated2026-10-30T12:31:51Z. Its repository, HEAD, root, Work ID and all three Master fingerprints match. The governance root is established; its original one-time Audit start is not reused. The five known authorized tracked governance changes and existing records are retained; a fresh-bootstrap clean-tree requirement is not incorrectly imposed on this established continuation. No product-root or Master-baseline adoption is established.\n",
      "All three Masters were read as candidate/unadopted comparison authority under Governance3. The actual source inventory comprises 45 docs/ai Markdown files, 16 Agent files and 15 Skill files =76 unique source identities, 758068 bytes. The fixed core is 3 Masters+10 Guidelines+10 Prompts+10 Requests+10 Skills+9 Agents=52. The remaining24 distinct files implement seven separate mechanism groups and do not inflate the core total. No additional in-scope Markdown definition was discovered in those governed directories.\n",
      "Publication/assessment order: current-role/Master authority and nonmutating qualification/predecessor checks; qualified own no-overwrite invocation publication; separate-process readback/checkpoint; substantive Master/mechanism/core comparison; path/binding/native scope checks; meaningful-boundary comparison; evidence/report; separate-process final readback/input comparison; result last. Exact publication instants were not captured; creation clocks are not publication timestamps.\n",
      "Bounded read-only evidence readers inspected two independent core partitions and the Orchestrator/Portability definitions under the Masters. They did not invoke governed process Skills/stages, publish records or perform corrections. Their notes are bound in this actor's evidence. Parent adjudication: unpopulated Request-template fields, concurrency preconditions and fresh-start requirements are not source defects merely because no product invocation is supplied. Parent findings/results remain this Audit actor's responsibility.\n",
      "### Complete source catalog and fingerprints\n",
      "Every expected core artifact is individually listed below with its current fingerprint and assessment. Additional source rows are separately labeled; their group results are below. SHA-256 values refer to actual stored bytes, not assumed contents. Per-layer checks cover Audit Skill9-13; shared consistency/reference checks cover6-8/14-16/26.\n",
      "| Scope/layer | Exact source path | Bytes | SHA-256 | Source assessment |\n|---|---|---:|---|---|"]
    bypath={r["path"]:r for r in core}
    for p in source_paths():
        r=ref(p);c=bypath.get(r["path"])
        scope="Core/"+c["layer"] if c else "Mechanism"
        verdict="PASS" if c or p.as_posix()!=FINDING["source_document"] else "Low ambiguity GOV-AUD-20261102-002"
        text.append(f"| {scope} | `{r['path']}` | {r['bytes']} | `{r['sha256']}` | {verdict} |")
    text += [
      "\n## Separately Reported Mechanism Alignment\n",
      "Each group is expected/present/assessed **1/1/1**, separately from52. Source counts below exclude the three shared Masters. The source table supplies exact source fingerprints; the evidence record supplies each group's complete native source/evidence references and check outcomes. Referenced Investigation/Corrective controls are the FINDING_INVESTIGATION and CORRECTIVE_CHANGE families in the core table. PASS is mechanism conformance with applicable evidence, not product runtime capability, Human Approval or global effectiveness.\n",
      "| Mechanism | Definition sources expected/present/assessed | Result |\n|---|---|---|"]
    for g in e["mechanisms"]:
        n=g["source_expected"]
        text.append(f"| {g['group']} | {n}/{n}/{n} | **{g['result']}** |")
    for g in e["mechanisms"]:
        text.append("\n### "+g["group"]+"\n")
        if g["runtime_non_applicability"]:text.append("Runtime evidence: NOT APPLICABLE — "+g["runtime_non_applicability"]+"\n")
        text.append("| Check | Outcome | Evidence-based rationale |\n|---|---|---|")
        for c in g["checks"]:
            text.append(f"| {c['check_id']} {c['title']} | {c['outcome']} | {c['rationale']} |")
        if g["evidence_records"]:
            ids=sorted({pathlib.Path(r["path"]).parent.name for r in g["evidence_records"] if pathlib.Path(r["path"]).name in ["report.md","result.json","attempt.json"]})
            text.append("\nEvidence attempts (exact report/result paths, identities and hashes in the record-reference table/evidence): "+", ".join("`"+x+"`" for x in ids)+".")
    text += [
      "\n### Current Audit directed integrity chain\n",
      f"Canonical report identity `{AID}:audit_report`, path `{OWN.as_posix()}/report.md`. Terminal result identity `{AID}:audit_result`, path `{OWN.as_posix()}/result.json`. Canonical evidence identity `{e['record_id']}`, path `{evidence_ref['path']}`, SHA-256 `{evidence_ref['sha256']}`. This immutable report does not claim its own or its future result's final SHA-256. The result is published only after report/evidence durable validation and binds their final bytes. A later Remediation coordinator must independently hash this Audit result and validate its report binding in its own canonical report/result, even with findings. That later handoff is not an input/precondition to this Audit, and this Audit publishes no Remediation record.\n",
      "### Required execution evidence and historical applicability\n",
      f"All record paths below are relative to `{BASE.as_posix()}/`. For Markdown, the stable identity is the originating attempt plus canonical filename; JSON native record identities are retained in the evidence. Each row is an actual recomputed file binding. Upstream evidence is not duplicated as this actor's report.\n",
      "| Record path relative to attempts root | Bytes | SHA-256 |\n|---|---:|---|"]
    for r in e["record_references"]:
        text.append(f"| `{pathlib.Path(r['path']).relative_to(BASE).as_posix()}` | {r['bytes']} | `{r['sha256']}` |")
    text += [
      "\n5518 structured path/SHA-256 occurrences were independently recomputed across current assurance/approval/results and required historical records, with zero mismatches. Five historical Review checkpoint basenames resolve relative to their owning result directory; an initial root-only diagnostic failed those five lookups, then exact actor-relative resolution matched every recorded digest. This was an auditor lookup error, not altered evidence. The latest Review evidence contributes529 path/hash occurrences and latest Verification evidence4612; these traversal counts differ from their reported413/4210 earlier check counts because the actual traversed object sets differ. No count is substituted as proof.\n",
      "Current approval scope objects compare natively equal across the exact recovery request, Application result and Review evidence. Approved and actual substantive paths are the same single new attachment. Its ABSENT base retains null bytes/hash; the payload equals approved source exactly:3438 ASCII UTF-8 bytes, noBOM, LF-only, one finalLF, SHA-2568887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA. Old failed-attempt attachment remains absent. All five P1-P5 changes independently reconstruct as single exact approved replacements from retained before-images and equal retained after-images/current files; the tracked change set is exactly those five files, with no staged change.\n",
      "Cycle history: initial P1-P5 Application and append-only IGV-FIND-001 transcription qualification retain their original Human attribution limits and separate Verification/Review PASS for that historical scope. Prospective Human admission at20261031T072633Z is an actual finding-led admission, not relabelled historical coordination. Strict record-first Investigation20261102T072445Z and Decision20261102T073730Z support GOV001/GOV002 accepted/no-plan-change-required dispositions without fabricating a new application. Later coordination remains paused, not final. Previous full Audit20261102T082552Z completed CONSISTENT WITH MINOR FINDINGS (oneLow GOV-AUD-20261102-001; RemediationFAIL/other6PASS), not incomplete execution or qualifying consistency.\n",
      "GOV-AUD-20261102-001 now has an exact approved append-only linked clarification, separately initiated Application, Verification13/13PASS and Review12/12PASS. The immutable original report still contains its three line15 markers and line27 presentation defect; the linked record resolves metadata to actual22254-byte evidence and explicitly distinguishes U+003F/U+00A7 at codepoint offsets27/42. Both responses are133 codepoints,133/135 UTF-8 bytes, and exact response digests match. No original Human message is newly authenticated, transport cause inferred or historical report replaced. All14 required Investigation fields remain identifiable; wholesale invalidity is unsupported. That prior Low is addressed by linked evidence, not suppressed or rewritten. New GOV-AUD-20261102-002 concerns different current source wording.\n",
      "Failed Application20261102T090912Z remains terminal FAILED/CANNOT COMPLETE, with no payload publication. Recovery20261102T092301Z separately proposed a new one-time scope and received actual redesignation/exact approval; separate fresh retry start is retained. Old approval/start were not transferred. Earlier invalid/incomplete attempts remain historical and are not inferred complete/live; current registry showed only this Audit running, prior roles idle. Historical reported execution is distinguished from independently rerun hash/byte/scope checks.\n",
      "## Repository Reference Findings\n",
      "None. All76 expected actual source paths exist.264 explicit repository governance-path relationships resolved with zero broken paths; associated basename/family links and Agent/Skill identities were checked in source inspection. Product examples/placeholders are reference definitions only, not missing actual products. No product content was opened. No moved/renamed/duplicate in-scope source was found. Stable record-relative historical checkpoint references resolve at their actual owning attempt.\n",
      "## Governance Consistency Findings\n",
      "### GOV-AUD-20261102-002\n",
      "**Severity:** Low. **Category:** Ambiguity.\n",
      f"**Source Document:** `{FINDING['source_document']}`. **Source Section:** {FINDING['source_section']}.\n",
      f"**Related Document:** `{FINDING['related_document']}`. **Related Section:** {FINDING['related_section']}.\n",
      "**Issue:** "+FINDING["issue"]+"\n",
      "**Evidence:**"]
    for c in e["finding_citations"]:
        text.append(f"- `{c['path']}`, line{c['line']}: “{c['quote']}”")
    text += [
      "\n**Impact:** "+FINDING["impact"]+"\n",
      "**Recommended Resolution:** "+FINDING["recommended_resolution"]+"\n",
      "**Human Decision Required:** Yes. "+FINDING["human_decision_reason"]+"\n",
      "This is an ambiguity, not a confirmed historical mutation or an unsupported extra approval gate. Higher-severity bypass is not established. The Audit does not select a silent interpretation or apply a fix. No Critical/High/Medium findings; no other current findings.\n",
      "## Guideline Consistency Summary\n",
      "All10 core Guidelines: PASS against Master lifecycle, authority, read-only/write boundaries, human and verification gates, change control, complete scope, statuses, outputs, downstream routing, terminology, references, unsupported-rule and omitted-control tests (Skill9). Shared family assessments below identify all10 families and every corresponding layer; no product invocation outcome is inferred.\n",
      "| Core family | Guideline | Prompt | Request | Skill | Agent | Substantive assessment |\n|---|---|---|---|---|---|---|"]
    for stem,slug,why in FAMILIES:
        text.append(f"| {stem} | PASS | PASS | PASS | PASS | {'N/A Skill-only' if stem=='REQUIREMENT_UPDATE' else 'PASS'} | {why} |")
    text += [
      "\n## Prompt Consistency Summary\n",
      "All10 Prompt entries in the family table: PASS. Correct existing Guideline and source-of-truth references; corresponding process identity and terminology; Human/read-only/change boundaries; no verification/approval/corrective shortcut; appropriate findings/evidence/output requirements. Skill10's15 checks assessed for each Prompt. They are controlled execution inputs, not replacement normative authorities.\n",
      "## Request Template Consistency Summary\n",
      "All10 Request entries: PASS. Corresponding Prompt resolves, required inputs/evidence/decision fields and artifact names match, taskIDs remain context where complete scope is mandatory, paths/casing and scope fields align (Skill11's15 checks). Template placeholders are intentionally unpopulated schemas, not failed actual invocations. There is no dedicated Requirement Update Agent to demand.\n",
      "## SDLC Process Skill Consistency Summary\n",
      "All10 Skill entries: PASS. Frontmatter identity/purpose, designated Guideline/Prompt/Request, Master subordination, mechanics not policy duplication, current upstream sources, read/write/approval/verification/review/corrective boundaries, terminology and downstream handoff assessed (Skill12's18 checks). Source-only conformance is not product execution capability. Requirement Update preserves new immutable versions/status-in-records; Planning/PlanVerification/Implementation preserve dependency/concurrency controls.\n",
      "## SDLC Process Agent Consistency Summary\n",
      "All9 expected Agent entries: PASS. Correct frontmatter, designated existing Skill and process identity; no bypass/redefinition or unauthorized upstream edit; authority/read/write/Human Approval/Acceptance/verification/corrective boundaries and references assessed (Skill13's18 checks). Requirement Update remains intentionally Skill-only. Governance control, advisory and assurance Agents are assessed separately, not silently counted as core.\n",
      "## Skill and Agent Traceability Summary\n",
      "For every family stem F and slug S in the family table, Guideline=`docs/ai/guidelines/F_GUIDELINES.md`, Prompt=`docs/ai/prompts/F_PROMPT.md`, Request=`docs/ai/request/F_REQUEST.md`, Skill=`.github/skills/S/SKILL.md`, and expected Agent=`.github/agents/S.agent.md`; exact expanded paths/fingerprints are individually listed in the catalog. Slugs in table order: requirement-analysis; requirement-analysis-verification; implementation-planning; requirement-update; implementation-plan-verification; implementation; implementation-verification; implementation-review; finding-investigation; corrective-change-decision.30 Skill-to-Guideline/Prompt/Request relationships and9 Agent-to-Skill relationships resolve and align; Prompt-to-Guideline and Request-to-Prompt checked for all10. Each layer retains the Masters as authority. Referenced complete core set is52, not53.\n",
      "## Cross-Document Consistency Summary\n",
      "The three Masters agree on ordinary and artifact-specific corrective lifecycles, current approved upstream use, explicit Human gates, AI verification versus Approval/Acceptance, immutable records/Requirement versions, downstream propagation, complete scope, and governance/product boundaries. No Master-to-Master contradiction found. Lifecycle includes analysis verification/resolution before Requirement Approval, complete plan verification/resolution before separate Human Review Approval then Plan Approval, implementation self-check before independent Verification/Review and Human Acceptance before Commit/Push. Finding paths remain artifact-specific; no direct finding-to-code shortcut. Changed artifact/Plan tasks do not carry stale verification automatically. Skill/Agent authority remains execution mechanics/entry boundary, not policy.\n",
      "Concurrency definitions require assessed dependencies/shared surfaces/checkout context; unknown safety sequences/serializes, shared-checkout writes use one coordinator, isolated worktrees require integration/reconciliation. No product concurrency execution was audited. Orchestrator fresh initiation is not formal approval or governance coordination. Portability is advisory, source/target-separated and Human-blocker-decided. Seven same-framework mechanisms remain outside core counting. One cross-document optional authorization-update ambiguity is explicitly reported above, not silently reconciled.\n",
      "## Governance Gaps\n",
      "Missing Governance Controls=0. No missing/unassessed required source, unavailable runtime evidence for a validly invoked assurance stage, or unresolved binding gap identified. Not-invoked Orchestrator/Portability runtime evidence is explicitly N/A; no runtime PASS inferred. Lack of product-root/Master adoption is a preserved future boundary, not a candidate-Audit defect.\n",
      "## Unsupported or Excessive Governance\n",
      "Unsupported Governance Controls=0. No extra residual-risk acknowledgement approval-validity gate is imposed. No fabricated blanket approval, new registry/state artifact, retrospective adoption, future-coordinator prerequisite, source correction, or product process authority is introduced.\n",
      "## Human Decisions Required\n",
      "GOV-AUD-20261102-002 requires governed clarification of the optional commit-identity record route; exact correction/approval is not supplied or inferred. Separate Human process initiation is required before any downstream Remediation/Investigation/Decision. Existing clarification approval and stage starts remain limited to their bound subjects. Target Master baseline and product root remain unadopted; any later adoption must follow its own gates and this nonqualifying Audit does not permit it. No Acceptance/Commit/Push decision requested or performed.\n",
      "## Recommended Corrective Actions\n",
      "1. Hand this completed Audit/report/result to a separately Human-started bounded Remediation continuation for Cycle1; preserve original IDs and distinguish addressed001 from new002.\n",
      "2. Route002 through Finding Investigation and Corrective Change Decision; obtain required Human decision/exact approval before a narrowly scoped clarification. Do not edit the Agent or historical authorization records from this Audit.\n",
      "3. If an approved correction is applied, require separately initiated independent Verification, Review and another complete52-core/seven-mechanism Audit. Do not reduce the next Audit to changed files.\n",
      "4. The coordinator must bind this result's actual SHA-256 and validate its canonical-report binding in its own later report, regardless of nonempty findings. It cannot mark remediation complete on this outcome.\n",
      "## Overall Audit Result\n",
      f"**{OUTCOME}** — all52 core artifacts and all7 mechanism groups assessed; oneLow ambiguity in Governance Remediation. Critical0, High0, Medium0, Low1, Ambiguities1, BrokenReferences0, MissingGovernanceControls0, UnsupportedGovernanceControls0. Mechanisms6PASS/1FAIL; no unresolved evidence gaps. Only exactCONSISTENT with all eight counts0 and all seven groups resolved qualifies for effectiveness. This Audit does not qualify, adopt, approve or accept the framework/product.\n",
      "### Limitations and non-actions\n",
      f"All {len(q['preservation_manifest'])} preexisting in-scope governance source/record files and their path set match qualification at meaningful endpoints; only this actor's exact attempt scope is excluded. HEAD/branch/index and external status checks remain bound. This is procedural nonmutation on a shared writable OS principal, not a sandbox or guaranteed prevention. No exhaustive trusted event log, coordinated no-edit window, repository lock or continuous observation is available; endpoints cannot exclude transient writes or same-principal tampering. Source reader notes and upstream reports are classified as reported/source-inspection evidence; actual hashes/bytes/scope comparisons are executed evidence. Product-specific content, tests/build/runtime, alarm integration, corrections, other stages, Git commit/branch/push and Human decisions were not performed. Exact publication time and original parent-message authentication are unavailable, not fabricated. Output-preparation diagnostic: Windows fsync rejected a read-only handle on the still-unpublished own helper. Checkpoint0002 and three source-note files had published successfully; canonical evidence/report/result were absent. Progression stopped, exact effects were read back, only the unpublished helper was corrected to flush through its own read/write handle, and existing final records were revalidated/reused without overwrite. No source action, terminal success or downstream stage occurred at that failure. The Audit actor's responsibility ends with this report and its bound result."
    ]
    return ("\n".join(text)+"\n").encode("utf-8")
def preservation_check():
    q=load(OWN/"evidence/qualification.json")
    current=snapshot()
    assert current==q["preservation_manifest"],"Governance input content/path set drift"
    repo=q["repository"]
    assert cmd("git","rev-parse","HEAD")==repo["HEAD"]
    assert cmd("git","branch","--show-current")==repo["branch"]
    assert cmd("git","status","--porcelain=v1")==repo["status"]
    assert ref(".git/index")==repo["index_fingerprint"]
    return {"outcome":"PASS","source_and_preexisting_record_files":len(current),
      "source_files":len(source_paths()),"excluded_scope":OWN.as_posix(),
      "HEAD_branch_index_status_unchanged":True,"content_and_pathset_unchanged":True,
      "proof_limit":"Endpoint observation, no exclusion of transient writes or same-principal tampering"}
def prepare():
    assert not (OWN/"report.md").exists() and not (OWN/"result.json").exists()
    links=governance_links();bindings=inspect_bindings();semantic=semantic_checks()
    assert all(r["outcome"]=="PASS" for r in links)
    assert all(r["outcome"]=="PASS" for r in bindings)
    assert semantic["current_inputs_unchanged"]
    assert len(source_paths())==76 and sum(p.stat().st_size for p in source_paths())==758068
    c=metadata("checkpoint_0002")
    c.update(sequence=2,boundary="Complete substantive scope, native approval/payload/P1-P5 reconstruction and all bindings assessed",
      preservation=preservation_check(),bindings_checked=len(bindings),binding_failures=0,
      core_expected=52,core_present=52,core_assessed=52,mechanisms_assessed=7,
      finding_ids=[FINDING["finding_id"]],outcome=OUTCOME,unfinished="Prepare/publish evidence/report; fresh separate-process readback and result last")
    if (OWN/"checkpoint-0002.json").exists():
        cr=ref(OWN/"checkpoint-0002.json")
        assert cr["sha256"]=="F03C3123F6C897907173ADCCE02B11EB5AB719C877E875AAD7B0D52D6C447130"
        prior=load(cr["path"])
        assert prior["boundary"]==c["boundary"] and prior["preservation"]==c["preservation"]
    else:
        cr=publish(OWN/"checkpoint-0002.json",c)
    notes=[]
    tempnames=[
      ("core-upstream-source-notes.md",r"C:\Users\Parimal\AppData\Local\Temp\1793613610389-copilot-tool-output-bd3685f5a0b2429b960fd0944181709d.txt"),
      ("core-downstream-source-notes.md",r"C:\Users\Parimal\AppData\Local\Temp\1793613676586-copilot-tool-output-f0ac881a015c47b99adbeec9c13a238c.txt"),
      ("advisory-mechanism-source-notes.md",r"C:\Users\Parimal\AppData\Local\Temp\1793613773650-copilot-tool-output-22649d78055c4a64b8f244e76c67eb8e.txt")]
    import re
    actual_hashes={ref(p)["sha256"] for p in source_paths()}
    for name,p in tempnames:
        b=pathlib.Path(p).read_bytes()
        for h in re.findall(r"\b[0-9A-Fa-f]{64}\b",b.decode("utf-8-sig")):
            assert h.upper() in actual_hashes,("Source note hash differs from actual catalog",h)
        target=OWN/"evidence"/name
        if target.exists():
            assert target.read_bytes()==b
            notes.append(ref(target))
        else:
            notes.append(publish(target,b))
    # Freeze this own evidence helper only after compilation and native self-tests.
    code=pathlib.Path(__file__).read_bytes()
    compile(code,str(OWN/"evidence/audit-controller.py"),"exec")
    scriptpath=OWN/"evidence/audit-controller.py"
    assert not scriptpath.exists()
    with pathlib.Path(__file__).open("r+b") as f:
        f.flush();os.fsync(f.fileno())
    os.rename(__file__,scriptpath)
    scriptref=ref(scriptpath)
    e=metadata("audit_evidence")
    e.update(core_inventory=core_inventory(),source_manifest=[ref(p) for p in source_paths()],
      core_counts={"expected":52,"present":52,"assessed":52},
      mechanisms=mechanism_matrix(),counts=COUNTS,outcome=OUTCOME,findings=[FINDING],
      finding_citations=parent_finding_evidence(),record_references=recordrefs(),
      binding_checks=bindings,binding_summary={"checked":len(bindings),"passed":len(bindings),"failed":0},
      governance_path_checks=links,governance_path_summary={"checked":len(links),"broken":0},
      native_semantic_checks=semantic,qualification=ref(OWN/"evidence/qualification.json"),
      invocation=ref(OWN/"attempt.json"),record_first_checkpoint=ref(OWN/"checkpoint-0001.json"),
      meaningful_boundary=cr,source_reader_notes=notes,controller=scriptref,
      source_reader_adjudication="Template placeholders and non-invoked product preconditions are not source defects; evidence readers are not separate governed process invocations or audit decision authorities.",
      operations=[
        {"order":1,"kind":"read-only qualification","operations":"Skill/role/Master publication authority, Git root/HEAD/status, whoami/token/ACL, external root decision, predecessor JSON/hash/criteria, recovery/liveness metadata; no substantive source comparison"},
        {"order":2,"kind":"own publication","operations":"Python preflight: native qualification then invocation, fsync/atomic no-overwrite rename/readback; successful tool output recorded hashes"},
        {"order":3,"kind":"separate-process readback","operations":"Fresh PowerShell/Python reload/hash/strict-value/preservation check; checkpoint0001 before substantive comparisons"},
        {"order":4,"kind":"source inspection","operations":"Full Master reads; Audit/Remediation/Application/Verification/Review mechanisms; three bounded read-only source evidence collection tasks for two core partitions and advisory mechanisms; no process Skills/stages or writes by readers"},
        {"order":5,"kind":"actual evidence comparison","operations":"View actual cycle, Investigation/Decision, Application/recovery/approval/Verification/Review reports and native evidence; inspect historical immutable qualification and failed terminal records"},
        {"order":6,"kind":"executed checks","operations":"source catalog hashes and264 explicit links,5518 structured bindings, native scope equality, payload exact bytes/encoding, P1-P5 before/after reconstruction, response codepoints/hash and current path set"},
        {"order":7,"kind":"diagnostics","operations":"Initial preflight enumeration encountered known historical malformed JSON; safely enumerated as historical, no edits. Large tool outputs read by targeted ranges. Five initial root-relative checkpoint lookups resolved against owning result directory; zero final mismatches. Unicode stdout rendering not trusted; native ord/hash checks used. Windows fsync on own unpublished helper opened rb failed Bad file descriptor before rename. Checkpoint0002 and three source notes already durably present, canonical evidence/report/result absent, exact file effects independently read back. Only unpublished helper changed to r+b flush/fsync; same actor output preparation continued after unchanged-input and no-overwrite existing-record validation. No source work or premature terminal success at failure."},
        {"order":8,"kind":"report preparation","operations":"checkpoint0002 and unchanged-input comparison; source notes copied as own evidence, final controller frozen, complete actual JSON native object self-test; evidence then report publication"},
        {"order":9,"kind":"required subsequent gate","operations":"Separate fresh-process report/evidence readback, final manifest/index/status comparison, checkpoint0003 then result; completed record only after this succeeds"}],
      event_coverage="Actor-visible ordered tool/operation groups and returned operation results; no invented within-parallel ordering or precise publication timestamps; no exhaustive trusted OS event stream.",
      self_tests=selftests(),preservation=preservation_check(),
      canonical_report={"path":(OWN/"report.md").as_posix(),"identity":AID+":audit_report"},
      terminal_result={"path":(OWN/"result.json").as_posix(),"identity":AID+":audit_result"},
      unresolved_evidence_gaps=[],effectiveness_qualifying=False,Master_adopted=False,product_root_adopted=False,
      limitations=load(OWN/"evidence/qualification.json")["limitations"])
    # The complete native evidence object is tested, not a surrogate sample.
    assert json.loads(encode(e))==e
    er=publish(OWN/"evidence/audit-evidence.json",e)
    report=build_report(e,er)
    required=["Audit Scope","Separately Reported Mechanism Alignment","Repository Reference Findings",
      "Governance Consistency Findings","Guideline Consistency Summary","Prompt Consistency Summary",
      "Request Template Consistency Summary","SDLC Process Skill Consistency Summary",
      "SDLC Process Agent Consistency Summary","Skill and Agent Traceability Summary",
      "Cross-Document Consistency Summary","Governance Gaps","Unsupported or Excessive Governance",
      "Human Decisions Required","Recommended Corrective Actions","Overall Audit Result"]
    decoded=report.decode("utf-8")
    assert all("## "+s in decoded for s in required)
    assert len(e["core_inventory"])==52 and len(e["mechanisms"])==7 and len(e["findings"])==1
    assert "{evrel}" not in decoded and "{ev['" not in decoded and "`n" not in decoded
    assert not report.startswith(b"\xef\xbb\xbf") and b"\r" not in report and report.endswith(b"\n")
    preservation_check()
    rr=publish(OWN/"report.md",report)
    print(json.dumps({"evidence":er,"report":rr,"script":scriptref,"outcome":OUTCOME,"counts":COUNTS,
      "next":"Separate-process finalize with expected report and evidence SHA256 from this output"}))
def finalize(expected_report,expected_evidence):
    assert not (OWN/"result.json").exists()
    rr=ref(OWN/"report.md");er=ref(OWN/"evidence/audit-evidence.json")
    assert rr["sha256"]==expected_report and er["sha256"]==expected_evidence
    e=load(er["path"]);assert e["record_id"]==AID+":audit_evidence"
    assert e["counts"]==COUNTS and e["outcome"]==OUTCOME
    assert len(e["core_inventory"])==52 and len(e["mechanisms"])==7
    assert e["findings"]==[FINDING]
    for r in [e["qualification"],e["invocation"],e["record_first_checkpoint"],e["meaningful_boundary"],e["controller"]]+e["source_reader_notes"]+e["record_references"]+e["source_manifest"]:
        checkref(r)
    assert all(x["outcome"]=="PASS" for x in inspect_bindings())
    assert semantic_checks()["current_inputs_unchanged"]
    final=preservation_check()
    c=metadata("checkpoint_0003")
    c.update(sequence=3,boundary="Separate fresh-process complete report/evidence readback and all final inputs validated before result",
      report=dict(rr,identity=AID+":audit_report"),evidence=dict(er,identity=e["record_id"]),
      preservation=final,outcome="PASS",unfinished="Terminal result publication only; no downstream stage")
    cr=publish(OWN/"checkpoint-0003.json",c)
    r=metadata("audit_result")
    r.update(execution_status="COMPLETED",execution_termination="COMPLETED",outcome=OUTCOME,
      core_counts={"expected":52,"found":52,"audited":52},counts=COUNTS,
      mechanisms=[{k:g[k] for k in ["group","expected","present","assessed","source_expected","source_present","source_assessed","result"]} for g in e["mechanisms"]],
      report=dict(rr,identity=AID+":audit_report"),evidence=dict(er,identity=e["record_id"]),
      invocation=ref(OWN/"attempt.json"),qualification=e["qualification"],
      record_first_checkpoint=e["record_first_checkpoint"],meaningful_boundary=e["meaningful_boundary"],
      independent_final_readback=cr,source_reader_notes=e["source_reader_notes"],controller=e["controller"],
      source_manifest=e["source_manifest"],repository_context=load(OWN/"attempt.json")["repository_context"],
      actor_identity=load(OWN/"attempt.json")["actor_identity"],human_stage_start=START,
      unresolved_findings=[FINDING],unresolved_evidence_gaps=[],
      addressed_prior_finding="GOV-AUD-20261102-001: linked correction and bounded assurance assessed; historical originals retained",
      historical_dispositions="GOV-001/GOV-002: confirmed historically/current text addressed, no-additional-change Decision retained; no retrospective approval or coordination",
      final_input_comparison=final,binding_summary=e["binding_summary"],path_summary=e["governance_path_summary"],
      effectiveness_qualifying=False,Master_baseline_adopted=False,product_root_adopted=False,
      human_approval_or_acceptance_claimed=False,serializer_self_tests=selftests(),
      downstream_handoff={"originating_actor":ACTOR,"originating_process":ROLE,
        "cycle":"GOV-REMEDIATION-PROSPECTIVE-001","cycle_number":1,
        "next_permitted_process":"Separately Human-started bounded Governance Remediation continuation to route new Low ambiguity; no stage started",
        "finding_ids":["GOV-AUD-20261102-002"],"severity":"Low","pending_Human_decision":"Governed clarification of optional authorization commit-identity update route",
        "integrity_requirement":"Receiving coordinator must independently recompute this stored result SHA256 and validate its exact canonical-report binding in its own later canonical report/result; do not overwrite or append to Audit records",
        "completion_blocker":"Not CONSISTENT; Low1,Ambiguities1,RemediationFAIL. No effectiveness/adoption/Remediation COMPLETE."},
      limitations=e["limitations"],non_actions=["No source or another actor record mutation","No correction/investigation/decision/application/verification/review/remediation stage","No product inspection or work","No commit/branch/push"])
    assert json.loads(encode(r))==r
    # Revalidate final inputs immediately before the completed result publication.
    preservation_check()
    resultref=publish(OWN/"result.json",r)
    print(json.dumps({"result":resultref,"report":rr,"evidence":er,"readback_checkpoint":cr,
      "outcome":OUTCOME,"counts":COUNTS,"mechanisms":r["mechanisms"]}))
if __name__=="__main__":
    if sys.argv[1]=="preflight":preflight()
    elif sys.argv[1]=="prepare":prepare()
    elif sys.argv[1]=="finalize":finalize(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=="diagnose":
        links=governance_links();bindings=inspect_bindings()
        print(json.dumps({"core":len(core_inventory()),"sources":len(source_paths()),
          "links":len(links),"broken_links":[r for r in links if r["outcome"]!="PASS"],
          "bindings":len(bindings),"binding_errors":[r for r in bindings if r["outcome"]!="PASS"],
          "semantic":semantic_checks()},ensure_ascii=False)[:7000])
