import sys, pathlib, types, json, os
sys.dont_write_bytecode = True
OLD = pathlib.Path(__file__).resolve().parent.parent/"20261102T152301Z-f1b897f3-8a3f-4bdb-9d9c-24de14ee0869/verifier.py"
m = types.ModuleType("preserved_readonly_verifier_primitives")
m.__file__ = str(OLD)
exec(compile(OLD.read_bytes(),str(OLD),"exec"),m.__dict__)
m.OWN = pathlib.Path(__file__).resolve().parent
m.ATTEMPT = m.OWN.name
m.EXCLUDE = {(m.OWN/n).relative_to(m.ROOT).as_posix() for n in m.NAMES}
m.EXCLUDE |= {p+".partial" for p in list(m.EXCLUDE)}
original_publish = m.publish

def publish(name,obj,text=False):
    if not text:
        obj = dict(obj)
        obj.update(schema_version="1.0",record_id=m.ATTEMPT+":"+name,
            work_id=m.WORK,feature="Governance-only F003/F004; product feature N/A",
            attempt_id=m.ATTEMPT,cycle_id="GOV-REMEDIATION-PROSPECTIVE-001",cycle=1,
            process="Independent Governance Verification",
            creator=dict(role="Independent Governance Verification",runtime_agent_id=m.ACTOR),
            created_at_utc=m.now(),clock_basis="UTC record preparation, not exact publication time")
        if name=="invocation.json":
            proposal=m.ROOT/"docs/sdlc-records/governance"/m.WORK/"attempts/20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d"
            application=m.ROOT/"docs/sdlc-records/governance"/m.WORK/"attempts/20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494"
            obj.update(repository_context=dict(canonical_repository="ScalableParimal/SupportIQ",
                 root=str(m.ROOT),head=m.git("rev-parse","HEAD"),branch=m.git("branch","--show-current")),
                 inputs=[m.fp(proposal/"report.md"),m.fp(proposal/"attachments/exact-proposal.json"),
                         m.fp(proposal/"attachments/minimal.patch"),m.fp(application/"result.json"),
                         m.fp(application/"evidence/human-authorization.json")],
                 applicable_task_context="N/A: governance-only subject; no product Requirement or Plan",
                 predecessor=m.fp(application/"result.json"),
                 retry=dict(previous_attempt=m.OLD if hasattr(m,"OLD") else OLD.parent.name,
                     reason="Preserve initial preparatory invocation unchanged; common structured metadata incomplete. No terminal conclusion or handoff. Repeat all substantive checks only after this qualified invocation publication/readback."),
                 governing_definitions=[m.fp(m.ROOT/p) for p in [
                     ".github/agents/independent-governance-verification.agent.md",
                     ".github/skills/independent-governance-verification/SKILL.md",
                     "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md",
                     "docs/ai/prompts/INDEPENDENT_GOVERNANCE_VERIFICATION_PROMPT.md",
                     "docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md"]],
                 existing_governance_root=dict(root="docs/sdlc-records/governance/",
                     source="https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                     fresh_resolution="github issue_read get_comments during qualification; OWNER ScalableParimal id 226102895; comment 6522916236 created/updated 2026-10-30T12:31:51Z; exact root/repository/WorkID/HEAD/Master hashes match",
                     authority_boundary="Original bootstrap stage not reused. Current Human fresh Verification start and normal finding-led continuation under Governance section 3; no product-root or Master adoption"),
                 preliminary_operation_evidence="Current conversation's ordered tool calls including root-authority resolution, Master governing-rule reads and discovery before corrected invocation. No retained substantive verdict; all checks repeated after readback.")
    return original_publish(name,obj,text)

m.publish=publish

BASE = "docs/sdlc-records/governance/"+m.WORK+"/attempts/"
PROPOSER = BASE+"20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d/"
APPLIER = BASE+"20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494/"
INVESTIGATION = BASE+"20261102T141609Z-4e74248e-a440-4617-8c17-61f31f2ff9c9/"
APPROVAL = "I approve the identified canonical report, exact proposal and patch with all five target fingerprints, scope, actor and assurance bindings; freshly designate the proposed one-time applier under that route; do not start Application"
APPSTART = "Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 under the approved five-file package"
SUPPLIED = {
 PROPOSER+"report.md":(39577,"A925ECCE1D7593DE1955EC0CA416A1BDFD1AA67A5B1800129BF8FA3C1B685677"),
 PROPOSER+"result.json":(11450,"A4BEE48991E0CA74D414BDDA1957220F0703E1FEF7F62AE50536E9EDB6A725ED"),
 PROPOSER+"attachments/exact-proposal.json":(21495,"086D48C77EC7D6C052615498DC82B380493B2C0610F9AAF070D1FFF08580D29C"),
 PROPOSER+"attachments/minimal.patch":(13651,"DFE0F97EE5EC19D0194E6FFB9FC2C3CD5104F41B9B9DCA908837556E1E99F1DD"),
 PROPOSER+"evidence/decision-evidence.json":(26178,"CD52373E75FF07654FCB496645F83F38ED96B612C5C3652882C329430B5B0A46"),
 APPLIER+"report.md":(9379,"6964F08042A633D53790E52FD6089AAA268C6D9DBC37E5DC88B999383160C6C6"),
 APPLIER+"result.json":(10315,"2B45D3CC36B665D0CCB561D0C0C32DADA35D9260319A62A1AC6B8B36B1B80CF7"),
 APPLIER+"evidence/application-evidence.json":(199421,"9C0C75BD3E2C96655F6F6BB09F73056A1C243B490DBAFB1A687EBB84EE168D4B"),
 APPLIER+"checkpoint-0002.json":(70499,"350100E17EF345D7116C7AE5FD8C1CC52CC367496A970534567014B0DD488F51"),
 INVESTIGATION+"report-revision-0002.md":(21951,"1B298794D8AA503E4C18AA3730754FA170D6196B7745160390BB9C68246D1365"),
 INVESTIGATION+"result-revision-0002.json":(4974,"41F442FA05C1472939889612DF43307E39E91883F75404C90D6AA1965A5248EB")}

READS = {}
def read(p):
    q=m.ROOT/p; b=q.read_bytes()
    READS[p]=m.fp(q)
    m.event("read exact input bytes and SHA256",[p],bytes=len(b),sha256=m.digest(b))
    return b

def load(p):
    d=m.strict(read(p))
    assert m.strict(m.encoded(d))==d
    return d

def assessment():
    import difflib, subprocess
    if not (m.OWN/"checkpoint-0001.json").exists():
        m.compare("checkpoint-0001.json")
    else:
        assert m.strict((m.OWN/"checkpoint-0001.json").read_bytes())["matches_initial"]
        assert m.strict((m.OWN/"manifest.json").read_bytes())["snapshot"]==m.snapshot()
        m.event("resume unpublished machine assessment after helper EOL representation correction",[],
            earlier_error="Raw HEAD blob is LF, approved worktree base is CRLF; core.autocrlf=true. No source/base fingerprint failure. Prior published checkpoint preserved; fresh complete input recheck passes.")
    for bad in [b'{"x":1,"x":2}',b'{"x":NaN}']:
        try: m.strict(bad)
        except ValueError: pass
        else: raise AssertionError("Strict JSON negative self-test failed")
    for p,(size,sha) in SUPPLIED.items():
        b=read(p); assert (len(b),m.digest(b))==(size,sha),p
    proposal=load(PROPOSER+"attachments/exact-proposal.json")
    propresult=load(PROPOSER+"result.json")
    appresult=load(APPLIER+"result.json")
    app=load(APPLIER+"evidence/application-evidence.json")
    auth=load(APPLIER+"evidence/human-authorization.json")
    ai=load(APPLIER+"attempt.json")
    pf=load(APPLIER+"evidence/preflight.json")
    cp=load(APPLIER+"checkpoint-0001.json")
    terminal=load(APPLIER+"checkpoint-0002.json")
    manifest=load(APPLIER+"evidence/input-manifest.json")
    assert appresult["outcome"]=="COMPLETED" and app["outcome"]=="COMPLETED"
    assert app["error"] is None and app["preservation_error"] is None
    assert proposal["work_id"]==m.WORK and proposal["cycle"]==1
    assert proposal["no_master_change"] and proposal["no_product_change"]
    assert auth["approval_exact_ascii"]==APPROVAL and auth["separate_stage_start_exact_ascii"]==APPSTART
    for a,b in [("target_bindings","targets"),("actors","actors"),("approval_route","approval_route"),("byte_contract","byte_contract")]:
        assert auth[a]==proposal[b],a
    assert ai["runtime"]["runtime_agent_id"]=="ec7a8339-a9b5-4710-bb5b-a8760309005d"
    assert proposal["actors"][0]["runtime_identity"]["runtime_agent_id"]=="4d0c3747-fde6-48c7-b125-5adb2af5b80c"
    definitions=[x["definition"] for x in proposal["actors"]]
    assert len({x["path"] for x in definitions})==4
    assert len({x["sha256"] for x in definitions})==4
    assert definitions[2]["path"]==".github/agents/independent-governance-verification.agent.md"
    for d in definitions: assert m.fp(m.ROOT/d["path"])==d
    for actor in proposal["actors"][1:]:
        assert actor.get("actual_attempt") is None
        assert actor.get("current_runtime_identity") is None
        assert actor.get("current_capability_evidence") is None
        assert actor.get("fresh_stage_start") is None
    assert pf["all_five_before_any_write"] and pf["outcome"]=="PASS" and cp["outcome"]=="PASS"
    assert pf["invocation"]==cp["invocation"]==m.fp(m.ROOT/(APPLIER+"attempt.json"))
    assert pf["invocation_readback"]==m.fp(m.ROOT/(APPLIER+"checkpoint-0001.json"))
    assert ai["created_at_utc"]<cp["created_at_utc"]<pf["created_at_utc"]<app["created_at_utc"]
    assert appresult["downstream_started"] is False
    assert appresult["effectiveness_claimed"] is False and appresult["adopted"] is False
    targets={t["path"]:t for t in proposal["targets"]}
    assert len(targets)==5
    bases={}; rows=[]; diffs=[]
    for path,t in targets.items():
        actual=read(path); base=actual
        for r in reversed(t["replacements"]):
            old=r["before"].encode("utf-8"); new=r["after"].encode("utf-8")
            assert base.count(new)==1,(path,"reverse occurrence")
            base=base.replace(new,old,1)
        assert (len(base),m.digest(base))==(t["base_bytes"],t["base_sha256"])
        # Obtain independent immutable repository base, not an applier-reported reconstruction.
        cmd=["git","--no-optional-locks","--no-pager","cat-file","--filters","HEAD:"+path]
        gh=subprocess.run(cmd,cwd=m.ROOT,capture_output=True,check=True)
        m.event("non-mutating subprocess exact repository blob",[path],arguments=cmd,stdout_sha256=m.digest(gh.stdout),returncode=gh.returncode)
        assert gh.stdout==base,(path,"HEAD working-tree representation base differs")
        rebuilt=base; offsets=[]
        for r in t["replacements"]:
            old=r["before"].encode("utf-8"); new=r["after"].encode("utf-8")
            assert r["expected_occurrences"]==1 and rebuilt.count(old)==1
            offset=rebuilt.index(old); assert offset==r["sequential_input_byte_offset"]
            offsets.append(offset); rebuilt=rebuilt.replace(old,new,1)
        assert rebuilt==actual
        assert (len(actual),m.digest(actual))==(t["expected_after_bytes"],t["expected_after_sha256"])
        for content in [base,actual]:
            assert content.decode("utf-8").encode("utf-8")==content
            assert not content.startswith(b"\xef\xbb\xbf")
            assert b"\n" not in content.replace(b"\r\n",b"") and b"\r" not in content.replace(b"\r\n",b"")
        assert base.endswith(b"\r\n")==t["base_final_newline"]
        assert actual.endswith(b"\r\n")==t["expected_after_final_newline"]
        bases[path]=base
        diffs.extend(difflib.unified_diff(base.decode("utf-8").splitlines(True),actual.decode("utf-8").splitlines(True),fromfile="a/"+path,tofile="b/"+path))
        pfr=next(x for x in pf["targets"] if x["path"]==path)
        assert pfr["sequential_offsets"]==offsets
        rows.append(dict(path=path,base=dict(bytes=len(base),sha256=m.digest(base)),
            actual_after=m.fp(m.ROOT/path),single_occurrence_offsets=offsets,
            independent_HEAD_worktree_representation_base_equal=True,complete_reconstruction_equal=True,
            utf8_no_bom_crlf=True,final_newline=actual.endswith(b"\r\n")))
    patch="".join(diffs).encode("utf-8")
    assert patch==read(PROPOSER+"attachments/minimal.patch")
    assert set(app["actual_changed_paths"])==set(targets)
    # Compare every original Application input, including hidden files and history.
    changed=[]; unchanged=[]; final={x["path"]:x for x in app["final_inventory"]}
    for x in manifest["files"]:
        q=m.fp(m.ROOT/x["path"]); read(x["path"])
        if q!=x: changed.append(x["path"])
        else: unchanged.append(x["path"])
        assert final[x["path"]]==q
        if x["path"] in targets:
            assert (x["bytes"],x["sha256"])==(len(bases[x["path"]]),m.digest(bases[x["path"]]))
    assert set(changed)==set(targets)
    nowstate=m.snapshot()
    original_paths={x["path"] for x in manifest["files"]}
    actual_paths={x["path"] for x in nowstate["files"]}
    additions=sorted(actual_paths-original_paths)
    prior=BASE+"20261102T152301Z-f1b897f3-8a3f-4bdb-9d9c-24de14ee0869/"
    assert all(p.startswith(APPLIER) or p.startswith(prior) for p in additions),additions
    assert not original_paths-actual_paths
    assert nowstate["repository"]["head"]==ai["repository"]["head"]==app["final_repository"]["head"]
    assert nowstate["repository"]["branch"]==ai["repository"]["branch"]==app["final_repository"]["branch"]
    assert nowstate["repository"]["index"]["sha256"]==ai["repository"]["index"]["sha256"]==app["final_repository"]["index"]["sha256"]
    # Check every bound path/bytes/hash occurrence, not merely the first occurrence per path.
    bound_checks=[]; visited=set()
    def walk(v,source,loc="$"):
        if isinstance(v,dict):
            if isinstance(v.get("path"),str) and isinstance(v.get("bytes"),int) and isinstance(v.get("sha256"),str):
                p=v["path"].replace("\\","/")
                if p.startswith(("docs/",".github/")):
                    b=read(p); historical=False
                    if (len(b),m.digest(b))!=(v["bytes"],v["sha256"]):
                        assert p in bases and (len(bases[p]),m.digest(bases[p]))==(v["bytes"],v["sha256"]),(source,loc,p,"bound mismatch")
                        historical=True
                    bound_checks.append(dict(source=source,location=loc,reference=v,mode="verified immutable HEAD/reconstructed historical base" if historical else "current bytes exact"))
            for k,x in v.items(): walk(x,source,loc+"."+k)
        elif isinstance(v,list):
            for i,x in enumerate(v): walk(x,source,loc+"["+str(i)+"]")
    for p in [PROPOSER+"attachments/exact-proposal.json",PROPOSER+"result.json",
              PROPOSER+"evidence/decision-evidence.json",PROPOSER+"checkpoint-0002.json",
              APPLIER+"result.json",APPLIER+"attempt.json",APPLIER+"evidence/preflight.json",
              APPLIER+"checkpoint-0001.json",APPLIER+"checkpoint-0002.json",
              APPLIER+"evidence/application-evidence.json",APPLIER+"evidence/human-authorization.json",
              INVESTIGATION+"result-revision-0002.json",INVESTIGATION+"checkpoint-0003.json"]:
        walk(load(p),p)
    audit=load(BASE+"20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f/result.json")
    # Read applicable sources as actual evidence, never execute upstream helpers or invoke processes.
    related=[
       "docs/ai/sdlc/SDLC_GOVERNANCE.md","docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",
       "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md",
       "docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
       "docs/ai/prompts/REQUIREMENT_ANALYSIS_PROMPT.md",
       "docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md",
       "docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md",
       "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
       "docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md",
       "docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md",
       ".github/skills/governance-amendment-application/SKILL.md",
       APPLIER+"attachments/application-tool.py"]
    for p in related: read(p)
    out=dict(record_type="independent_verification_machine_checks",outcome="PASS",
        targets=rows,patch=dict(bytes=len(patch),sha256=m.digest(patch),exact_native_diff_equal=True),
        supplied_input_fingerprints_checked=[READS[p] for p in SUPPLIED],
        approval=auth,proposal_scope=dict(scope=proposal["scope"],exclusions=proposal["exclusions"],
            actors=proposal["actors"],approval_route=proposal["approval_route"],byte_contract=proposal["byte_contract"]),
        application_schema_outcome=appresult["outcome"],application_ordering=dict(
            invocation=ai["created_at_utc"],readback=cp["created_at_utc"],preflight=pf["created_at_utc"],application_evidence=app["created_at_utc"],
            basis="Preparation metadata plus bound readback/preflight and inspected helper control flow; no exhaustive OS trace or exact publication timestamps"),
        application_preservation=dict(input_count=len(manifest["files"]),unchanged_count=len(unchanged),
            independently_changed_paths=changed,additions_since_application_manifest=additions,removals=[],
            current_HEAD_branch_index_equal=True),
        nested_binding_checks=bound_checks,read_inputs=sorted(READS.values(),key=lambda x:x["path"]),
        latest_audit_reported_state=audit,events=m.EVENTS.copy())
    return out

def machine():
    result=assessment()
    original=m.strict((m.OWN/"manifest.json").read_bytes())["snapshot"]
    assert original==m.snapshot()
    result["boundary_snapshot_matches_initial"]=True
    result["snapshot"]=original
    result["events"]=m.EVENTS.copy()
    print(json.dumps(publish("checkpoint-0002.json",result)))

def blocked():
    # No further substantive assessment. Preserve the observed results without converting
    # them into a valid process PASS; only final source-preservation checks and own records.
    cp=m.strict((m.OWN/"checkpoint-0002.json").read_bytes())
    inv=m.strict((m.OWN/"invocation.json").read_bytes())
    initial=m.strict((m.OWN/"manifest.json").read_bytes())["snapshot"]
    final=m.compare("checkpoint-final.json")
    assert initial==m.snapshot()
    blocker=dict(id="VERIFIER-INVOCATION-001",kind="missing fresh retry authorization",
        outcome="CANNOT COMPLETE",affected_scope="This verifier's replacement attempt, not an established defect in the five-file Application",
        evidence=[
           m.fp(m.ROOT/(BASE+"20261102T152301Z-f1b897f3-8a3f-4bdb-9d9c-24de14ee0869/invocation.json")),
           m.fp(m.OWN/"invocation.json"),m.fp(m.OWN/"invocation-readback.json")],
        observation="Initial verifier invocation omitted required common structured metadata. It was preserved without overwrite. Verifier then created a new replacement attempt explicitly labeled a retry, reused the sole supplied Human Verification stage-start, and repeated assessment. No separate fresh Human start for that retry is available.",
        rule="SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md section 30.1, Governance amendment stage invocation and handoff: retries and restarts require a fresh stage-start instruction; no response is inferred, reused, or automatically propagated.",
        disposition="STOP. Do not repair published records or infer retry authorization. Fresh explicit Human start is required for a new independent Verification invocation; requalify and independently check the bounded current inputs then.")
    criteria=[
      dict(id="authority",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="Actual supplied exact ASCII approval/designation and separate Application start match authorization record. Package fingerprints, route, target objects, actors and byte contract compared as complete native objects. Existing governance root freshly resolved through canonical OWNER comment. Bootstrap Audit start not reused as current-stage authority."),
      dict(id="own-stage-authorization",status="CANNOT COMPLETE",
           evidence="Only the original Human Verification stage-start is supplied. Replacement attempt's retry field explicitly requires a fresh start under section 30.1, which was not obtained."),
      dict(id="identity-and-independence",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="Harness registry sole running assigned verifier 8e0bf478-bfeb-461b-90ed-64033f60f8d5; separate Copilot invocation edd4a15d-4bb2-4605-a897-0e019144523c. Definition matches approved planned verifier binding ECD11EFE7F0078FE0B258DE819C8E473A3CF3EC674C8999E49F04194D62B8958. Preparer/applier runtime IDs differ. Reviewer planned definition differs; no current reviewer runtime claimed. Shared host title is not role proof."),
      dict(id="own-record-first",status="CANNOT COMPLETE",
           evidence="Initial invocation/readback published before checks but common record metadata incomplete. Replacement invocation/readback contain complete metadata and precede repeated machine checks; missing fresh retry start prevents valid replacement qualification. Both attempts retained unchanged."),
      dict(id="capabilities-permissions",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="Successful hidden-inclusive reads, hashlib SHA256, non-mutating Git checks, strict native full-object JSON tests, own validated/flushed partial -> Windows atomic no-overwrite rename and independent fresh-process readback. Writable inherited ACL and tools disclosed, no source-write probe."),
      dict(id="complete-input-boundary",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="Replacement manifest covers all repository files including hidden .github, upstream/history and earlier verifier preparatory records, path presence/absence, tracked/untracked state, directories, bytes, SHA256, file modes, HEAD/branch/index/status/diffs. Only exact replacement-owned output paths excluded. No entire record-root exclusion."),
      dict(id="application-ordering-and-status",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="Actual Application outcome COMPLETED, not generic PASS. Invocation, independent readback, preflight and terminal evidence match all hashes and ordered preparation records. Inspected helper requires readback/approval/full-set preflight and reconstruction before opening first source for write. Runtime qualification and permission evidence are current to applier's recorded invocation. This supports procedural ordering, not a trusted exhaustive write trace."),
      dict(id="all-five-exact-bytes",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="Independent reverse replacements recover every exact approved base. Git cat-file --filters HEAD:path independently matches CRLF worktree base; raw Git blobs use LF with core.autocrlf=true. Every forward single occurrence/offset matches, full after bytes equal approved hashes, unified diff equals exact approved patch. UTF8 no BOM/CRLF and first-four absent/fifth present final newline preserved."),
      dict(id="scope-and-preservation",status="OBSERVED CHECK PASSED; NOT A PROCESS PASS",
           evidence="All 474 pre-Application input identities recomputed: exactly five approved targets changed; other 469 equal, no removal. Additions reconciled to Application-owned outputs and earlier verifier preparatory records only; HEAD/branch/index and six preexisting tracked modifications preserved. Every bound reference occurrence checked, distinguishing exact historical base values from current-after bytes."),
      dict(id="F003-cross-document-effects",status="SOURCE INSPECTION COMPLETED; NO VALID VERIFICATION VERDICT",
           evidence="Actual four-artifact Update branch admits identified immutable unapproved initial clarification source only before first formal approval, with explicit Analysis questions/Human answers/update request. Result remains unapproved; lineage/immutable source preserved under Artifact section 8.4. Subsequent Analysis, complete independent Verification, findings resolution and separate formal Human Requirement Approval remain. Approved-source changes retain approved source. Matches existing Analysis section 14/phases 5-10 and Governance sections 3-4; no product execution performed."),
      dict(id="F004-cross-document-effects",status="SOURCE INSPECTION COMPLETED; NO VALID VERIFICATION VERDICT",
           evidence="Only enhancement actor-fields paragraph changed. Actual preparer/applier own attempts and qualification are stage-specific. Future verifier/reviewer planned definition path/hash only until predecessor gates and fresh starts. Actual matching binding/current qualification required at each stage. Four distinct roles, applier coordinator exclusions and separate starts retained. Aligns with unchanged Application Guideline/Prompt/Request."),
      dict(id="52-core-seven-groups-effectiveness",status="SCOPE INSPECTION COMPLETED; NO AUDIT OR EFFECTIVENESS CLAIM",
           evidence="No core/group addition/removal; five bounded text changes only. Masters unchanged at approved comparison hashes. Seven named mechanism groups remain separate from 52-core count. Non-Master correction follows ordinary finding lifecycle before Master adoption; it does not adopt product root or candidate Masters. Full independent Review and complete fresh Audit remain outstanding; latest actual Audit INCONSISTENT retained."),
      dict(id="nonmutation-and-final-boundary",status="OBSERVED CHECK PASSED; PROCEDURAL ONLY",
           evidence="Full replacement evaluated-input snapshot equals initial at fresh readback, machine boundaries and terminal boundary. Earlier preparatory records treated as immutable inputs. Only verifier-owned helpers/records created. No sources/upstream/history edited, no staging/commit/push. Endpoint hashes cannot prove absence of transient writes or same-principal tampering.")
    ]
    operations=[
      dict(order=1,tool="functions.powershell",shell="1171",action="Read mandatory verifier Skill"),
      dict(order=2,tool="functions.get_current_session",action="Shared host metadata, not current role proof"),
      dict(order=3,tool="functions.powershell",shells=["1172","1173","1174","1175","1176","1177"],
           action="Identity/environment/permissions/read/hash probes; required role/guideline/prompt/request and governing paths; stage handoff resolution; Git state non-mutating"),
      dict(order=4,tool="functions.list_agents",arguments=dict(scope="all",include_completed=False),
           action="One running assigned verifier, idle historical metadata not competing writer proof"),
      dict(order=5,tool="functions.apply_patch",action="Created only first verifier-owned helper"),
      dict(order=6,tool="functions.powershell",shells=["1178","1179"],
           action="First invocation/manifest publication and fresh-process readback"),
      dict(order=7,tool="functions.view / functions.rg / functions.powershell",
           shells=["1180","1181","1182"],action="Preliminary source/record/control-flow inspection; no retained process conclusion; detected own invocation metadata omission"),
      dict(order=8,tool="functions.github-mcp-server-issue_read",
           arguments=dict(owner="ScalableParimal",repo="SupportIQ",issue_number=3,method="get_comments",perPage=100),
           action="Fresh canonical root comment resolution; OWNER ScalableParimal user 226102895; comment 6522916236 exact root/HEAD/Master bindings; normal continuation not original stage authority"),
      dict(order=9,tool="functions.apply_patch / functions.powershell",shells=["1183","1184","1185"],
           action="New retry attempt helper, complete invocation/manifest publication and independent readback; missing fresh retry start now identified as blocker"),
      dict(order=10,tool="functions.view / functions.powershell",shells=["1186","1187"],
           action="Resolve actual route and inspect Application helper without executing it"),
      dict(order=11,tool="functions.apply_patch / functions.powershell",shell="1188",
           action="Machine assessment stopped on helper assertion comparing raw LF Git blob with approved CRLF worktree base; no source write and no machine conclusion publication"),
      dict(order=12,tool="functions.powershell / functions.apply_patch",shells=["1189","1190"],
           action="Confirmed core.autocrlf=true and exact filtered Git base; corrected only unpublished helper; repeated complete checks after unchanged-input recheck; published machine checkpoint"),
      dict(order=13,tool="functions.view / functions.powershell",shells=["1191","1192","1193"],
           action="Actual target/source semantic inspection. Read-only console command 1191 failed cp1252 arrow encoding; 1192 repeated with UTF8, no files written; 1193 summarized observed machine evidence"),
      dict(order=14,tool="functions.apply_patch / functions.powershell",
           action="Only own blocker/evidence/report/result preparation and final nonmutation checks; no further substantive checks or success handoff")
    ]
    limits=[
      "Procedural read-only conduct only, not an enforced source-write sandbox. Principal/tools can write, but source/upstream/other-actor writes are unauthorized.",
      "Matching endpoint content/path-set fingerprints cannot prove absence of a transient write or same-principal tampering.",
      "Actor-visible ordered tools and helper read/hash/check/publication events only; no exhaustive trusted OS event stream or independent tamper monitor.",
      "Only one running actor observed in registry; no coordinated exclusive filesystem lock or proof against external writers. Idle/stale metadata is not evidence of live concurrency.",
      "Actual Human words supplied from parent conversation; no authenticated message/author ID or original decision time exposed. None invented. Root GitHub comment identity/time is separately resolvable.",
      "Exact publication timestamps not captured; record UTC times identify preparation or observations, not exact filesystem publication times.",
      "Machine byte/integrity results and source inspection cannot cure this verifier's missing fresh retry authorization. No valid Verification PASS, Review, Audit, effectiveness, closure or adoption is established."
    ]
    evidence=dict(record_type="independent_governance_verification_evidence",
        execution_status="STOPPED",outcome="CANNOT COMPLETE",blocker=blocker,criteria=criteria,
        invocation=m.fp(m.OWN/"invocation.json"),invocation_readback=m.fp(m.OWN/"invocation-readback.json"),
        input_manifest=m.fp(m.OWN/"manifest.json"),machine_checkpoint=m.fp(m.OWN/"checkpoint-0002.json"),
        final_checkpoint=final,final_snapshot_matches_initial=True,
        machine_facts=cp,tool_operation_observations=operations,
        bounded_source_reads="Every relied canonical source/record is in the manifest; inventory/hash reads are not a claim that every repository file was semantically audited.",
        own_helpers=[m.fp(m.OWN/"verifier.py"),m.fp(OLD)],limitations=limits,
        last_confirmed_boundary="All evaluated input files/path sets and Git identity/index unchanged; stop for missing fresh retry start",
        pending_gates=["Fresh Human Verification start for a new qualified invocation","Only after valid independent Verification PASS: fresh Human Review start","Only after Review PASS: fresh Human complete Audit start"],
        events=m.EVENTS.copy())
    ev=publish("verification-evidence.json",evidence)
    lines=[
      "# Independent Governance Verification Report","",
      "**Outcome: CANNOT COMPLETE — no success handoff.**",
      "**Reason: this verifier's replacement attempt lacks the separately fresh Human retry stage-start required by current governance.**","",
      f"Work ID: `{m.WORK}`; Cycle `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1.",
      f"Canonical stopped attempt: `{m.ATTEMPT}`.",
      "Subject: completed five-file Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 only.",
      "Repository: ScalableParimal/SupportIQ; `C:\\PARIMAL_SHERE\\SCALABLE_SOLUTIONS\\SupportIQ`.",
      "HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`; branch `sdlc-framework-onboarding`.",
      "This is only Independent Governance Verification. No Review, Governance Audit, fix, approval, adoption or product work was performed.","",
      "## 1. Actual authority and independent identity","",
      "Actual supplied fresh Human start (ASCII quote preserved):",
      "'"+inv["fresh_human_start"]+"'","",
      "Actual supplied exact Human approval/designation:",
      "'"+APPROVAL+"'","",
      "Actual separate Human Application start:",
      "'"+APPSTART+"'","",
      "The supplied presentation binds the canonical report/proposal/patch, all five target/base/after fingerprints, byte properties, actors, assurance route and exclusions. Actual authorization JSON matches the complete approved proposal objects. No authenticated Human message ID/time was exposed or invented; original words were explicitly supplied for this invocation. Residual-risk disclosure is not an extra approval-validity gate.",
      "Existing governance root was freshly resolved through canonical OWNER comment https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236 (ScalableParimal, user 226102895, created/updated 2026-10-30T12:31:51Z). Repository/HEAD/WorkID/root/three Master hashes match. This does not reuse the initial bootstrap Audit start as current authority; normal non-Master finding-led continuation is allowed under Governance section 3. Product root and candidate Master baseline remain unadopted.",
      f"Current verifier harness runtime ID `{m.ACTOR}`; Copilot invocation `edd4a15d-4bb2-4605-a897-0e019144523c`; principal `INT-SCL-010\\Parimal`. Registry showed this sole running assigned verifier. Shared session title is not role proof and this is not an external authenticated identity claim.",
      "Preparer `4d0c3747-fde6-48c7-b125-5adb2af5b80c`; applier `ec7a8339-a9b5-4710-bb5b-a8760309005d`; current verifier differs. Approved reviewer remains planned definition-only. All four definition path/hash bindings are distinct; current verifier definition exactly matches approved planned hash. No current reviewer identity or future capability is invented. This actor is not the active Remediation actor or product Orchestrator.","",
      "## 2. Invocation failure and mandatory stop","",
      blocker["observation"],"",
      blocker["rule"],"",
      "The original fresh start authorized the initial invocation, not an automatically propagated retry. Creating a replacement attempt was not a license to reuse that response. The replacement invocation/readback and observed machine checks cannot cure this missing authority. The defect is in this verifier's execution, not a confirmed discrepancy in the five-file Application.",
      "Initial preparatory attempt `20261102T152301Z-f1b897f3-8a3f-4bdb-9d9c-24de14ee0869` remains unchanged with no terminal result and no handoff. The replacement explicitly links it and preserves it as evaluated historical input. This stopped result must not be used as a passing Verification.",
      blocker["disposition"],"",
      "## 3. Observed machine facts — not a valid assurance PASS","",
      f"All {cp['application_preservation']['input_count']} original Application inputs were independently rehashed. Exactly the approved five targets differ; the other {cp['application_preservation']['unchanged_count']} inputs match. No original input was removed. Additional paths reconcile to Application-owned outputs and the preserved initial verifier preparatory attempt only. The replacement manifest has {len(initial['files'])} repository inputs, including hidden .github and all upstream/history records; only exact own replacement output names are excluded.",
      f"All {len(cp['nested_binding_checks'])} nested path/byte/hash reference occurrences were checked, including historical base references, and {len(cp['read_inputs'])} distinct input paths were read by machine checks. Canonical Investigation revision 0002 and terminal checkpoint bindings were used, not superseded conclusions.",
      "Application's native outcome is COMPLETED, not a blanket PASS. Its invocation, readback, preflight, report/result/evidence and terminal bindings match. Helper source was inspected, never executed; it gates all five bases and complete reconstructions before first write. This is procedural ordering evidence, not proof from an exhaustive trusted write log.",
      "Each actual target independently reverses to the approved base and replays all sequential single-occurrence replacements at approved offsets. Git's immutable HEAD content in worktree representation also equals each base. Raw Git blobs are LF, while approved/current worktree bytes are CRLF with core.autocrlf=true; that representation distinction caused a stopped unpublished helper assertion and was corrected without weakening byte checks. Exact regenerated native unified diff equals the approved patch.",
      "All targets are UTF-8/no BOM/CRLF. First four have no final newline; fifth retains one. Complete after bytes match exactly; no normalization or source repair occurred.","",
      "| Target | Exact observed after bytes | SHA-256 |",
      "|---|---:|---|"]
    for row in cp["targets"]:
        a=row["actual_after"]
        lines.append(f"| `{row['path']}` | {a['bytes']} | `{a['sha256']}` |")
    lines+=["","## 4. Criterion-by-criterion disposition",""]
    for c in criteria:
        lines += [f"### {c['id']} — {c['status']}",c["evidence"],""]
    lines+=["## 5. Scope, evidence and residual limits","",
      "F003's four actual Update artifacts now distinguish initial immutable unapproved clarification from approved-source amendment, preserving lineage, unapproved status and later Analysis/complete independent Verification/separate Human Requirement Approval. F004's one actual Request paragraph distinguishes current attempts/qualification from future planned-only actors. These source-inspection observations are not product behavioral tests or a valid process PASS.",
      "The 52-core boundary and seven separately assessed mechanism groups are unchanged: Governance Audit, Governance Remediation, SDLC Process Orchestration, SDLC Portability Assessment, Governance Amendment Application, Independent Governance Verification, Independent Governance Review. No new group is counted among the 52. This stage did not run the full Audit.",
      "Three Master comparison fingerprints remain: Governance `79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B`; Artifact `6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860`; Traceability `08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C`.",
      "Both findings remain accepted, not closed. Latest complete Audit `20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f` remains reported INCONSISTENT (Critical 0, High 0, Medium 2, Low 0, Ambiguities 1, Missing 0, Unsupported 1, Broken References 0). Prior resolved findings are not reopened. Product Requirement/Plan are N/A.",
      "Non-Master effectiveness still requires valid independent Verification, separate Review and a complete qualifying Audit; it does not adopt the candidate Masters. Master adoption is a separate later Human decision under its own gates.",""]
    lines += ["- "+x for x in limits]
    lines+=["","## 6. Canonical records and final preservation","",
      f"Evidence: `{ev['path']}`; {ev['bytes']} bytes; SHA-256 `{ev['sha256']}`.",
      f"Invocation: `{m.fp(m.OWN/'invocation.json')['path']}`; SHA-256 `{m.fp(m.OWN/'invocation.json')['sha256']}`.",
      f"Fresh readback: `{m.fp(m.OWN/'invocation-readback.json')['path']}`; SHA-256 `{m.fp(m.OWN/'invocation-readback.json')['sha256']}`.",
      f"Input manifest: `{m.fp(m.OWN/'manifest.json')['path']}`; SHA-256 `{m.fp(m.OWN/'manifest.json')['sha256']}`.",
      f"Final boundary: `{final['path']}`; SHA-256 `{final['sha256']}`.",
      "Own records use native full-object strict JSON equality, validated/flushed .partial bytes, atomic same-directory Windows no-overwrite publication, independent fresh invocation readback and subsequent record readback/hash. No existing final record was overwritten. Final evaluated input content/path sets, index, HEAD, branch and pre-existing modifications match the replacement initial snapshot.",
      "No source/upstream/history change, fix, Review, Audit, approval, adoption, staging, commit, push or product work. Only own records were published. The terminal result is published after this report/evidence and binds their exact final bytes.","",
      "## 7. Next permitted gate and stop","",
      "**No Review handoff is authorized by this result.** Obtain a fresh explicit Human Independent Governance Verification stage-start for a new qualified invocation, preserving these records and independently rechecking current inputs. Only after a valid Verification PASS may a distinct reviewer be separately Human-started; only after passing Review may a separately started full Audit proceed. Do not treat observed byte checks as substitute assurance. **STOP.**",""]
    report=publish("report.md","\n".join(lines),text=True)
    assert initial==m.snapshot()
    result=dict(record_type="independent_governance_verification_result",
        execution_status="STOPPED",outcome="CANNOT COMPLETE",subject_type="GOVERNANCE_APPLICATION",
        finding_ids=["GOV-AUD-20261102-003","GOV-AUD-20261102-004"],
        report=report,evidence=ev,invocation=m.fp(m.OWN/"invocation.json"),
        invocation_readback=m.fp(m.OWN/"invocation-readback.json"),
        input_manifest=m.fp(m.OWN/"manifest.json"),final_checkpoint=final,
        exact_evaluated_state=dict(targets=cp["targets"],manifest=m.fp(m.OWN/"manifest.json"),
            HEAD=initial["repository"]["head"],branch=initial["repository"]["branch"],index=initial["repository"]["index"]),
        blockers=[blocker],criteria=criteria,limitations=limits,
        final_input_comparison=dict(matches_initial=True,scope="All manifest inputs/path sets and Git/index state; only exact own output exclusions",
            observation_basis="Fresh snapshot immediately before terminal publication",events=m.EVENTS.copy()),
        partial_outputs="Observed machine checks PASS and source inspections retained only as facts; not a valid Independent Verification conclusion",
        next_permitted_process="Await fresh Human Verification retry start; not Review",
        next_separate_review_gate="Only after valid independent Verification PASS and separate fresh Human Review start",
        review_authorized=False,downstream_started=False,audit_run=False,
        effectiveness_claimed=False,findings_closed=False,master_adopted=False,product_root_adopted=False,
        source_writes=False,other_actor_record_writes=False,staging_commit_push=False)
    rr=publish("result.json",result)
    print(json.dumps(dict(outcome="CANNOT COMPLETE",report=report,result=rr,evidence=ev),indent=2))

if __name__=="__main__":
    if sys.argv[1]=="invocation": m.invocation()
    elif sys.argv[1]=="readback": m.readback()
    elif sys.argv[1]=="checkpoint": print(json.dumps(m.compare(sys.argv[2])))
    elif sys.argv[1]=="machine": machine()
    elif sys.argv[1]=="blocked": blocked()
