import os, sys, json, pathlib, hashlib, subprocess, datetime, difflib
sys.dont_write_bytecode = True
OWN = pathlib.Path(__file__).resolve().parent
ROOT = OWN.parents[5]
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = OWN.name
ACTOR = "8e0bf478-bfeb-461b-90ed-64033f60f8d5"
BASE = "docs/sdlc-records/governance/"+WORK+"/attempts/"
PROPOSER = BASE+"20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d/"
APPLIER = BASE+"20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494/"
INVESTIGATION = BASE+"20261102T141609Z-4e74248e-a440-4617-8c17-61f31f2ff9c9/"
PRIOR = BASE+"20261102T152557Z-efc37bf9-a1dd-4f02-b768-d797e0636818/"
INITIAL = BASE+"20261102T152301Z-f1b897f3-8a3f-4bdb-9d9c-24de14ee0869/"
START = "Yes, initiate one fresh Independent Governance Verification retry for the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 Application only; preserve unsuccessful records and start no later stage"
APPROVAL = "I approve the identified canonical report, exact proposal and patch with all five target fingerprints, scope, actor and assurance bindings; freshly designate the proposed one-time applier under that route; do not start Application"
APPSTART = "Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 under the approved five-file package"
NAMES = ["verifier.py","input-manifest.json","attempt.json","checkpoint-0001.json",
         "checkpoint-0002.json","checkpoint-0003.json","checkpoint-final.json",
         "verification-evidence.json","report.md","result.json"]
EXCLUDE = {(OWN/n).relative_to(ROOT).as_posix() for n in NAMES}
EXCLUDE |= {p+".partial" for p in list(EXCLUDE)}
EVENTS = []
READS = {}
LIMITS = [
 "Procedural non-mutation, not an enforced read-only sandbox. Writable tools and ACLs grant no authority to alter sources, evaluated inputs or other actors' records.",
 "Matching endpoint content/path-set fingerprints cannot prove absence of transient writes or same-principal tampering.",
 "Actor-visible ordered tool and helper operation evidence only; no exhaustive trusted OS event stream, independent tamper monitor or external authenticated identity guarantee.",
 "Current assignment and supplied harness actor ID establish this invocation's role; shared session title is not proof. No exclusive filesystem lock/no coordinated no-edit guarantee; external writers cannot be excluded. Idle/stale metadata is not evidence of live writers.",
 "Actual Human words supplied in current/parent conversation; authenticated message/author IDs and original decision times unavailable and not invented. Root GitHub comment identity/time separately resolvable.",
 "UTC record creation times describe preparation; exact publication timestamps not captured. Operation observations and separate process readbacks establish ordering, not exact publication times.",
 "No product execution/behavior test, Review or Governance Audit. This Verification cannot claim effectiveness, finding closure, product-root adoption or Master-baseline adoption."
]
MASTER = {
 "docs/ai/sdlc/SDLC_GOVERNANCE.md":"79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
 "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md":"6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
 "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md":"08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C"}
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
 PRIOR+"report.md":(18471,"12C124A81D90C2FE103609634815D938C598471F271CF54E7975E4BFB315F92E"),
 PRIOR+"result.json":(32344,"4EF05323144433148511B30F68271784E465C126AB88B0DCF59C484D67F29606"),
 PRIOR+"verification-evidence.json":(1782728,"6A7E21CFB389D97F7285AC1385331327AF0D2EC233799426D52DA3288FADF89D")}

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def event(op, paths=(), outcome="OK", **extra):
    EVENTS.append(dict(sequence=len(EVENTS)+1,actor=ACTOR,attempt=ATTEMPT,observed_at_utc=now(),
                       operation=op,paths=list(paths),outcome=outcome,**extra))
def strict(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise ValueError("Duplicate key "+k)
            d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs,
        parse_constant=lambda v: (_ for _ in ()).throw(ValueError("Nonfinite "+v)))
def encode(d):
    b=(json.dumps(d,ensure_ascii=False,allow_nan=False,indent=2)+"\n").encode("utf-8")
    assert strict(b)==d
    return b
def path(p):
    q=ROOT/p
    assert q.resolve().is_relative_to(ROOT)
    return q
def fingerprint(p):
    q=path(p) if isinstance(p,str) else p
    b=q.read_bytes()
    return dict(path=q.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def read(p):
    b=path(p).read_bytes(); r=dict(path=p,bytes=len(b),sha256=sha(b)); READS[p]=r
    event("read/SHA256", [p],bytes=len(b),sha256=sha(b))
    return b
def load(p): return strict(read(p))
def git(*args):
    cmd=["git","--no-optional-locks","--no-pager",*args]
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,check=True)
    event("non-mutating subprocess",arguments=cmd,stdout_sha256=sha(r.stdout),returncode=r.returncode)
    return r.stdout
def ps(script):
    cmd=["powershell","-NoProfile","-NonInteractive","-Command",script]
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,check=True)
    event("non-mutating permission/principal query",arguments=cmd,stdout_sha256=sha(r.stdout),returncode=r.returncode)
    return strict(r.stdout.decode("utf-8-sig"))
def permissions():
    return ps("$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); "
       "$paths=@('.', '.github', 'docs/ai', 'docs/sdlc-records/governance/"+WORK+"/attempts'); "
       "$rows=@(foreach($p in $paths){ $a=Get-Acl -LiteralPath $p; "
       "[pscustomobject]@{path=$p;owner=$a.Owner;rules=@($a.Access | ForEach-Object {"
       "[pscustomobject]@{identity=$_.IdentityReference.Value;rights=$_.FileSystemRights.ToString();"
       "type=$_.AccessControlType.ToString();inherited=$_.IsInherited}})}}); "
       "[pscustomobject]@{principal=[Security.Principal.WindowsIdentity]::GetCurrent().Name;rows=$rows}|ConvertTo-Json -Depth 8 -Compress")
def snapshot():
    tracked=sorted(x for x in git("ls-files","-z").decode("utf-8").split("\0") if x)
    files=[]; directories=[]
    for base,ds,fs in os.walk(ROOT):
        if pathlib.Path(base)==ROOT: ds[:]=[d for d in ds if d!=".git"]
        directories += [(pathlib.Path(base)/d).relative_to(ROOT).as_posix() for d in ds]
        for n in fs:
            q=pathlib.Path(base)/n; rel=q.relative_to(ROOT).as_posix()
            if rel in EXCLUDE: continue
            row=fingerprint(q); row.update(tracked=rel in tracked,mode=oct(q.stat().st_mode),
                 effective_read_observed=True)
            files.append(row)
    files.sort(key=lambda x:x["path"]); directories.sort()
    status=git("status","--porcelain=v1","--untracked-files=all").decode("utf-8").splitlines()
    status=[x for x in status if x[3:].replace("\\","/") not in EXCLUDE]
    state=dict(canonical_repository="ScalableParimal/SupportIQ",root=str(ROOT),
        head=git("rev-parse","HEAD").decode().strip(),branch=git("branch","--show-current").decode().strip(),
        origin=git("remote","get-url","origin").decode().strip(),index=fingerprint(ROOT/".git/index"),
        tracked=tracked,status_excluding_exact_own_outputs=status,
        staged_diff_sha256=sha(git("diff","--cached","--binary","--no-ext-diff")),
        worktree_diff_sha256=sha(git("diff","--binary","--no-ext-diff")))
    expected=[dict(path=p,present=path(p).exists()) for p in
        ["AGENTS.md",".github/copilot-instructions.md",".github/instructions","docs/AGENTS.md","docs/ai/AGENTS.md"]]
    s=dict(files=files,directories=directories,expected_presence_absence=expected,
         repository=state,permissions=permissions(),exact_own_output_exclusions=sorted(EXCLUDE),
         git_internals_boundary="No .git content inventory; HEAD/branch/origin/index/tracked/status and complete staged/worktree diffs bound separately",
         file_path_set_sha256=sha(encode([x["path"] for x in files])))
    event("complete hidden-inclusive input/path-set snapshot",[str(ROOT)],file_count=len(files),
          file_path_set_sha256=s["file_path_set_sha256"])
    return s
def common(kind,**extra):
    return dict(schema_version="1.0",record_type=kind,record_id=ATTEMPT+":"+kind,
        feature="Governance-only F003/F004; product feature N/A",work_id=WORK,cycle_id="GOV-REMEDIATION-PROSPECTIVE-001",
        cycle=1,process="Independent Governance Verification",attempt_id=ATTEMPT,
        creator=dict(role="Independent Governance Verification",runtime_agent_id=ACTOR),
        created_at_utc=now(),clock_basis="UTC record preparation, not exact publication time",
        gate_refs=dict(current="Fresh Human Independent Governance Verification retry stage-start",
            predecessor="Completed five-file Governance Amendment Application",
            later="Review and Audit not started; require their own gates and starts"),
        **extra)
def validate(d,kind=None):
    assert type(d) is dict
    required={"schema_version":str,"record_type":str,"record_id":str,"feature":str,
        "work_id":str,"cycle_id":str,"cycle":int,"process":str,"attempt_id":str,
        "creator":dict,"created_at_utc":str,"clock_basis":str,"gate_refs":dict}
    for k,t in required.items(): assert type(d.get(k)) is t and (d[k] if t is not int else d[k]>0),k
    assert d["schema_version"]=="1.0" and d["work_id"]==WORK and d["attempt_id"]==ATTEMPT
    assert d["cycle_id"]=="GOV-REMEDIATION-PROSPECTIVE-001" and d["cycle"]==1
    assert d["process"]=="Independent Governance Verification"
    assert d["creator"]==dict(role="Independent Governance Verification",runtime_agent_id=ACTOR)
    assert d["record_id"]==ATTEMPT+":"+d["record_type"]
    assert datetime.datetime.fromisoformat(d["created_at_utc"]).utcoffset()==datetime.timedelta(0)
    if kind: assert d["record_type"]==kind
    assert strict(encode(d))==d
    if d["record_type"]=="invocation":
        for k in ["requested_scope","inputs","task_context","repository","authorization","retry",
                  "output_scope","capabilities","governing_inputs","actors","targets","input_manifest",
                  "related_records","limitations","operation_evidence"]:
            assert k in d,k
        assert d["authorization"]["fresh_start_exact_ascii"]==START
        assert d["authorization"]["single_attempt_only"] is True
        assert d["retry"]["retroactive_authorization"] is False
        assert d["retry"]["prior_assurance_valid"] is False
        assert d["repository"]["canonical_repository"]=="ScalableParimal/SupportIQ"
        assert d["repository"]["head"]=="57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
        assert d["repository"]["branch"]=="sdlc-framework-onboarding"
        assert d["output_scope"]["exact_names"]==NAMES
        assert d["output_scope"]["root"]==OWN.relative_to(ROOT).as_posix()
        assert len(d["targets"])==5 and len(d["actors"])==4
        assert len({x["definition"]["path"] for x in d["actors"]})==4
        for item in d["inputs"]+d["governing_inputs"]+d["related_records"]:
            assert type(item["bytes"]) is int and len(item["sha256"])==64
            assert fingerprint(item["path"])=={k:item[k] for k in ["path","bytes","sha256"]}
        assert d["authorization"]["approval_exact_ascii"]==APPROVAL
        assert d["authorization"]["separate_application_start_exact_ascii"]==APPSTART
    return True
def stage(name,d,text=False):
    assert name in NAMES and name!="verifier.py"
    q=OWN/(name+".partial")
    assert not (OWN/name).exists() and not q.exists()
    if not text: validate(d)
    b=d.encode("utf-8") if text else encode(d)
    with q.open("xb") as h:
        assert h.write(b)==len(b); h.flush(); os.fsync(h.fileno())
    rb=q.read_bytes(); assert rb==b
    if not text:
        parsed=strict(rb); assert parsed==d; validate(parsed)
    event("validated and flushed own unpublished partial",[q.relative_to(ROOT).as_posix()],bytes=len(b),sha256=sha(b))
    return dict(path=(OWN/name).relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def rename(name,text=False):
    q=OWN/(name+".partial"); p=OWN/name
    assert q.exists() and not p.exists() and os.name=="nt"
    b=q.read_bytes()
    if not text: validate(strict(b))
    os.rename(q,p)
    assert p.read_bytes()==b
    event("atomic same-directory no-overwrite rename and final read/hash",[p.relative_to(ROOT).as_posix()],
          bytes=len(b),sha256=sha(b))
    return fingerprint(p)
def publish(name,d,text=False): stage(name,d,text); return rename(name,text)
def binding(r):
    return fingerprint(r["path"])=={k:r[k] for k in ["path","bytes","sha256"]}
def selftest():
    x=dict(quoted="'ASCII' \"double\"",unicode="α",crlf="x\r\n",nullable=None,values=[True,False,17,{"z":0}])
    assert strict(encode(x))==x
    for b in [b'{"x":1,"x":2}',b'{"x":NaN}']:
        try: strict(b)
        except ValueError: pass
        else: raise AssertionError("Invalid JSON accepted")
    assert len({ACTOR,"4d0c3747-fde6-48c7-b125-5adb2af5b80c","ec7a8339-a9b5-4710-bb5b-a8760309005d"})==3
    event("native complete-object JSON positive/negative selftests",outcome="PASS")
def initial_snapshot():
    return strict((OWN/"input-manifest.json").read_bytes())["snapshot"]
def checkpoint(name,sequence,boundary,pending):
    s=snapshot(); assert s==initial_snapshot(),"Evaluated input/path/Git/permission drift"
    d=common("checkpoint_"+str(sequence),sequence=sequence,last_confirmed_boundary=boundary,
        partial_outputs="Only verifier-owned records; no source effects",unfinished_work=pending,
        blockers=[],pending_gates=["No later stage started"],safe_continuation_prerequisites="Input snapshot unchanged, same single fresh-authorized invocation",
        related_records=[fingerprint(OWN/"attempt.json"),fingerprint(OWN/"input-manifest.json")],
        snapshot_matches_initial=True,snapshot=s,events=EVENTS.copy())
    return publish(name,d)
def prepare():
    assert ROOT.name=="SupportIQ" and ATTEMPT=="20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216"
    selftest()
    # Handoff resolution and qualification only, no substantive target evaluation.
    proposal=load(PROPOSER+"attachments/exact-proposal.json")
    appresult=load(APPLIER+"result.json"); prior=load(PRIOR+"result.json")
    assert appresult["outcome"]=="COMPLETED" and prior["outcome"]=="CANNOT COMPLETE"
    assert appresult["work_id"]==WORK and prior["work_id"]==WORK
    for p,(size,h) in SUPPLIED.items():
        b=read(p); assert (len(b),sha(b))==(size,h),p
    for p,h in MASTER.items(): assert sha(read(p))==h,p
    for a in proposal["actors"]: assert binding(a["definition"])
    governing=[
      ".github/agents/independent-governance-verification.agent.md",
      ".github/skills/independent-governance-verification/SKILL.md",
      "docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md",
      "docs/ai/prompts/INDEPENDENT_GOVERNANCE_VERIFICATION_PROMPT.md",
      "docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md",*MASTER]
    for p in governing: read(p)
    s=snapshot()
    manifest=common("evaluated_input_manifest",snapshot=s,related_records=[fingerprint(OWN/"verifier.py")],
         scope="Every present repository file including hidden .github and all prior/upstream records; exact own output files only excluded",
         inventory_not_substantive_read=True,events=EVENTS.copy())
    mf=stage("input-manifest.json",manifest)
    actors=proposal["actors"]
    actors[2]=dict(role="actual_verifier",definition=actors[2]["definition"],binding_state="ACTUAL_CURRENT_INVOCATION",
        runtime_agent_id=ACTOR,own_attempt_path=(OWN/"attempt.json").relative_to(ROOT).as_posix())
    inv=common("invocation",
        requested_scope="ONLY Independent Governance Verification of completed five-file Application GOV-AUD-20261102-003/004",
        task_context="N/A: governance-only correction; no product Requirement or Implementation Plan",
        inputs=[fingerprint(path(p)) for p in SUPPLIED if not p.startswith(PRIOR)],
        repository=s["repository"],input_manifest=mf,governing_inputs=[fingerprint(p) for p in governing],
        related_records=[fingerprint(PRIOR+"report.md"),fingerprint(PRIOR+"result.json"),
            fingerprint(PRIOR+"verification-evidence.json"),fingerprint(INITIAL+"invocation.json")],
        authorization=dict(fresh_start_exact_ascii=START,single_attempt_only=True,
            actual_source="Actual Human request in current conversation explicitly authorizes one new attempt; original approval/designation and Application start explicitly retained",
            authenticated_message_id=None,authenticated_author_id=None,original_decision_time=None,
            approval_exact_ascii=APPROVAL,separate_application_start_exact_ascii=APPSTART,
            existing_root=dict(root="docs/sdlc-records/governance/",work_id=WORK,
                canonical_comment="https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
                author="ScalableParimal",author_id=226102895,association="OWNER",
                created_updated_at="2026-10-30T12:31:51Z",
                fresh_resolution="github issue_read get_comments during this retry qualification",
                boundary="Original first-use Audit stage not reused. Root adoption persists; Governance section 3 normal finding-led continuation plus current fresh Human start permits only current Verification. Product root and candidate Master baseline remain unadopted")),
        retry=dict(prior_result=fingerprint(PRIOR+"result.json"),prior_outcome="CANNOT COMPLETE",
            prior_assurance_valid=False,retroactive_authorization=False,
            reconciliation="Initial invocation incomplete metadata; replacement not separately Human-started; both unsuccessful, immutable and excluded as assurance. This one fresh Human-authorized retry requalifies and rechecks independently.",
            scope="ONE new attempt only; invalid published invocation requires STOP, no automatic replacement"),
        output_scope=dict(root=OWN.relative_to(ROOT).as_posix(),exact_names=NAMES,
            permitted="Only this verifier's own new records; all sources/evaluated/upstream/history readonly"),
        actors=actors,targets=proposal["targets"],
        current_runtime=dict(role="Independent Governance Verification",runtime_agent_id=ACTOR,
            attribution="Harness identity supplied and previously registry-attributed to this invocation; current assigned role; not external authentication guarantee",
            copilot_agent_session_id=os.environ.get("COPILOT_AGENT_SESSION_ID"),
            host_session="ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
            effective_principal=s["permissions"]["principal"],
            separation="Not preparer/applier/reviewer/active Remediation/Orchestrator; shared session title not role proof"),
        capabilities=dict(read="All stage handoff/governing inputs successfully read and manifest files hashed",
            sha256="hashlib SHA256 on actual bytes; supplied package fingerprints match",
            checks="Python native strict JSON and non-mutating Git status/path/index/diff queries executed",
            current_permissions=s["permissions"],source_write_exclusion=False,write_probe=False,
            own_publication="Current Human explicitly authorizes own new attempt; inherited Modify permits own .partial creation, flush, validation and Windows atomic no-overwrite rename; current staged own manifest is successful current publication-capability evidence",
            assurance_mode="procedural non-mutation; current effective read and own-output write permission observed"),
        operation_evidence=dict(prequalification_tools=[
            "1196: current Skill/role/Guideline/Prompt/Request and Master 33.1/30.1 reads",
            "1197: exact qualification/common metadata/retry/publication rules, current environment and Get-Acl",
            "1198: required verifier role/Guideline/Prompt reread",
            "github issue_read issue 3 comments: current exact root decision resolved"],
            helper_sha256=fingerprint(OWN/"verifier.py"),events=EVENTS.copy(),
            limits="No trusted exhaustive OS log or exact filesystem publication times; helper events plus conversation tools provide actor-visible ordering"),
        limitations=LIMITS)
    stage("attempt.json",inv)
    # Validate both complete native actual objects and cross-bindings before ANY final rename.
    mi=strict((OWN/"input-manifest.json.partial").read_bytes())
    ii=strict((OWN/"attempt.json.partial").read_bytes())
    validate(mi); validate(ii,"invocation")
    assert fingerprint(OWN/"input-manifest.json.partial")["sha256"]==ii["input_manifest"]["sha256"]
    assert mi["snapshot"]==snapshot()
    print(json.dumps(dict(prepared=True,final_records_published=False,
        required_fields_and_types="PASS",actual_bindings="PASS",complete_native_object_roundtrip="PASS",
        manifest=mf,attempt_partial_sha256=sha((OWN/"attempt.json.partial").read_bytes()),
        next="Fresh-process validate/publish, then separate fresh-process readback; no substantive checks yet"),indent=2))
def publish_invocation():
    mi=strict((OWN/"input-manifest.json.partial").read_bytes())
    ii=strict((OWN/"attempt.json.partial").read_bytes())
    validate(mi); validate(ii,"invocation")
    assert mi["snapshot"]==snapshot()
    assert sha((OWN/"input-manifest.json.partial").read_bytes())==ii["input_manifest"]["sha256"]
    # Refuse publication unless the entire pair already validates and no collision exists.
    assert not (OWN/"input-manifest.json").exists() and not (OWN/"attempt.json").exists()
    mf=rename("input-manifest.json"); assert mf==ii["input_manifest"]
    iv=rename("attempt.json")
    print(json.dumps(dict(invocation=iv,manifest=mf,substantive_checks_started=False),indent=2))
def readback():
    ii=strict((OWN/"attempt.json").read_bytes()); mi=strict((OWN/"input-manifest.json").read_bytes())
    validate(ii,"invocation"); validate(mi)
    assert binding(ii["input_manifest"]) and mi["snapshot"]==snapshot()
    cp=common("checkpoint_1",sequence=1,last_confirmed_boundary="Independent fresh-process readback of published complete invocation/manifest before any substantive verification",
        related_records=[fingerprint(OWN/"attempt.json"),fingerprint(OWN/"input-manifest.json")],
        invocation_validated=True,manifest_validated=True,snapshot_matches_initial=True,
        fresh_process_id=os.getpid(),partial_outputs="No source effects; own records only",
        unfinished_work="All substantive Verification checks",blockers=[],
        pending_gates=["No later stage"],safe_continuation_prerequisites="Same one authorized attempt; unchanged evaluated snapshot",
        events=EVENTS.copy())
    print(json.dumps(publish("checkpoint-0001.json",cp),indent=2))

def assess():
    selftest()
    inv=load((OWN/"attempt.json").relative_to(ROOT).as_posix()); validate(inv,"invocation")
    rb=load((OWN/"checkpoint-0001.json").relative_to(ROOT).as_posix())
    assert rb["invocation_validated"] and rb["snapshot_matches_initial"]
    assert initial_snapshot()==snapshot()
    event("pre-assessment input boundary independently recomputed; begin substantive checks",outcome="PASS")
    for p,(size,h) in SUPPLIED.items():
        b=read(p); assert (len(b),sha(b))==(size,h),p
    proposal=load(PROPOSER+"attachments/exact-proposal.json")
    pr=load(PROPOSER+"result.json")
    ar=load(APPLIER+"result.json")
    ae=load(APPLIER+"evidence/application-evidence.json")
    ai=load(APPLIER+"attempt.json")
    auth=load(APPLIER+"evidence/human-authorization.json")
    pf=load(APPLIER+"evidence/preflight.json")
    acp=load(APPLIER+"checkpoint-0001.json")
    am=load(APPLIER+"evidence/input-manifest.json")
    terminal=load(APPLIER+"checkpoint-0002.json")
    prior=load(PRIOR+"result.json")
    assert prior["outcome"]=="CANNOT COMPLETE" and not prior["review_authorized"]
    assert inv["retry"]["prior_assurance_valid"] is False
    assert ar["outcome"]=="COMPLETED" and ae["outcome"]=="COMPLETED"
    assert ae["error"] is None and ae["preservation_error"] is None
    assert not ar["downstream_started"] and not ar["effectiveness_claimed"] and not ar["adopted"]
    assert proposal["work_id"]==WORK and proposal["cycle"]==1
    assert proposal["no_master_change"] and proposal["no_product_change"]
    assert auth["approval_exact_ascii"]==APPROVAL and auth["separate_stage_start_exact_ascii"]==APPSTART
    assert auth["authenticated_message_id"] is None and auth["original_decision_time"] is None
    for ak,pk in [("target_bindings","targets"),("actors","actors"),("approval_route","approval_route"),("byte_contract","byte_contract")]:
        assert auth[ak]==proposal[pk],ak
    for r in auth["package"]: assert binding(r)
    definitions=[a["definition"] for a in proposal["actors"]]
    assert len({d["path"] for d in definitions})==4 and len({d["sha256"] for d in definitions})==4
    for d in definitions: assert binding(d); read(d["path"])
    assert definitions[2]["path"]==".github/agents/independent-governance-verification.agent.md"
    assert inv["actors"][2]["definition"]==definitions[2] and inv["actors"][2]["runtime_agent_id"]==ACTOR
    assert proposal["actors"][0]["runtime_identity"]["runtime_agent_id"]=="4d0c3747-fde6-48c7-b125-5adb2af5b80c"
    assert ai["runtime"]["runtime_agent_id"]=="ec7a8339-a9b5-4710-bb5b-a8760309005d"
    assert ai["preparer_attempt"]["path"]==PROPOSER+"attempt.json"
    for a in proposal["actors"][1:]:
        assert a.get("actual_attempt") is None and a.get("current_runtime_identity") is None
        assert a.get("current_capability_evidence") is None and a.get("fresh_stage_start") is None
    for p in [".github/agents/sdlc-process-orchestrator.agent.md",".github/agents/sdlc-governance-remediation.agent.md"]:
        r=fingerprint(p); assert r["path"]!=definitions[1]["path"] and r["sha256"]!=definitions[1]["sha256"]; read(p)
    assert ai["permissions"]["principal"]=="INT-SCL-010\\Parimal"
    assert ai["capabilities"] and ai["permissions"]["rows"]
    assert pf["outcome"]=="PASS" and pf["all_five_before_any_write"]
    assert acp["outcome"]=="PASS" and acp["checked_input_count"]==474
    assert pf["invocation"]==acp["invocation"]==fingerprint(APPLIER+"attempt.json")
    assert pf["invocation_readback"]==fingerprint(APPLIER+"checkpoint-0001.json")
    assert ai["created_at_utc"]<acp["created_at_utc"]<pf["created_at_utc"]<ae["created_at_utc"]
    apphelper=read(APPLIER+"attachments/application-tool.py").decode("utf-8")
    # Inspect actual program control flow, never execute the applier/helper.
    pfbody=apphelper[apphelper.index("def preflight():"):apphelper.index("def apply():")]
    abody=apphelper[apphelper.index("def apply():"):apphelper.index("def terminal():")]
    assert pfbody.index('cp["outcome"]')<pfbody.index('for t in p["targets"]')
    assert 'all_five_before_any_write=True' in pfbody
    assert abody.index('afters = [(t, b, reconstruct(b, t)[0])')<abody.index('with q.open("r+b")')
    assert abody.index('check(pf["outcome"] == "PASS"')<abody.index('with q.open("r+b")')
    tpaths=[t["path"] for t in proposal["targets"]]
    assert tpaths==[
        "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md",
        "docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md",
        "docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",
        ".github/skills/requirement-update/SKILL.md",
        "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md"]
    bases={}; rows=[]; diffs=[]
    for t in proposal["targets"]:
        p=t["path"]; actual=read(p); base=actual
        assert t["encoding"]=="UTF-8" and t["bom"] is False and t["newline"]=="CRLF"
        for r in reversed(t["replacements"]):
            before=r["before"].encode("utf-8"); after=r["after"].encode("utf-8")
            assert base.count(after)==1
            base=base.replace(after,before,1)
        assert (len(base),sha(base))==(t["base_bytes"],t["base_sha256"])
        # HEAD filtered through actual Git working-tree conversion, not raw LF blobs.
        head_worktree=git("cat-file","--filters","HEAD:"+p)
        assert head_worktree==base,p
        rebuilt=base; offsets=[]
        for r in t["replacements"]:
            before=r["before"].encode("utf-8"); after=r["after"].encode("utf-8")
            assert r["expected_occurrences"]==1 and rebuilt.count(before)==1
            offset=rebuilt.index(before); assert offset==r["sequential_input_byte_offset"]
            offsets.append(offset); rebuilt=rebuilt.replace(before,after,1)
        assert rebuilt==actual
        assert (len(actual),sha(actual))==(t["expected_after_bytes"],t["expected_after_sha256"])
        assert base.endswith(b"\r\n")==t["base_final_newline"]
        assert actual.endswith(b"\r\n")==t["expected_after_final_newline"]
        for b in [base,actual]:
            assert not b.startswith(b"\xef\xbb\xbf")
            assert b.decode("utf-8").encode("utf-8")==b
            rem=b.replace(b"\r\n",b""); assert b"\r" not in rem and b"\n" not in rem
        bases[p]=base
        diffs.extend(difflib.unified_diff(base.decode("utf-8").splitlines(True),
            actual.decode("utf-8").splitlines(True),fromfile="a/"+p,tofile="b/"+p))
        pfr=next(r for r in pf["targets"] if r["path"]==p)
        assert pfr["sequential_offsets"]==offsets and pfr["reverse_to_exact_base"]
        operation=next(r for r in ae["operations"] if r["path"]==p)
        assert operation["before"]==dict(bytes=len(base),sha256=sha(base))
        assert operation["after"]==fingerprint(p)
        rows.append(dict(path=p,finding_ids=t["finding_ids"],
            approved_base=dict(bytes=len(base),sha256=sha(base)),
            actual_after=fingerprint(p),approved_after=dict(bytes=t["expected_after_bytes"],sha256=t["expected_after_sha256"]),
            independently_reconstructed=True,immutable_HEAD_worktree_base_equal=True,
            exact_sequential_single_occurrence_offsets=offsets,utf8_no_bom_crlf=True,
            final_newline=actual.endswith(b"\r\n")))
    patch="".join(diffs).encode("utf-8")
    assert patch==read(PROPOSER+"attachments/minimal.patch")
    assert set(ae["actual_changed_paths"])==set(tpaths)
    old={x["path"]:x for x in am["files"]}; final={x["path"]:x for x in ae["final_inventory"]}
    assert len(old)==474 and set(old)==set(final)
    changed=[]; unchanged=[]
    for p,r in old.items():
        b=read(p); actual=dict(path=p,bytes=len(b),sha256=sha(b))
        assert actual==final[p]
        (unchanged if actual==r else changed).append(p)
        if p in bases: assert (r["bytes"],r["sha256"])==(len(bases[p]),sha(bases[p]))
    assert set(changed)==set(tpaths) and len(unchanged)==469
    s=snapshot(); current={r["path"] for r in s["files"]}
    additions=sorted(current-set(old)); removals=sorted(set(old)-current)
    assert not removals
    assert all(p.startswith((APPLIER,INITIAL,PRIOR)) for p in additions),additions
    for k in ["head","branch","origin"]: assert s["repository"][k]==ai["repository"][k]==ae["final_repository"][k]
    assert s["repository"]["index"]["sha256"]==ai["repository"]["index"]["sha256"]==ae["final_repository"]["index"]["sha256"]
    initial_status=ai["repository"]["status_excluding_own_attempt"]
    post_status=ae["final_repository"]["status_excluding_own_attempt"]
    before_tracked={r[3:]:r[:2] for r in initial_status if not r.startswith("??")}
    after_tracked={r[3:]:r[:2] for r in post_status if not r.startswith("??")}
    actual_tracked={r[3:]:r[:2] for r in s["repository"]["status_excluding_exact_own_outputs"] if not r.startswith("??")}
    assert actual_tracked==after_tracked
    assert {p:v for p,v in after_tracked.items() if p not in tpaths}==before_tracked
    bound_checks=[]
    def walk(v,source,loc="$"):
        if isinstance(v,dict):
            if isinstance(v.get("path"),str) and type(v.get("bytes")) is int and isinstance(v.get("sha256"),str):
                p=v["path"].replace("\\","/")
                if p.startswith(("docs/",".github/")):
                    b=read(p); mode="current exact bytes"
                    if (len(b),sha(b))!=(v["bytes"],v["sha256"]):
                        assert p in bases and (len(bases[p]),sha(bases[p]))==(v["bytes"],v["sha256"]),(source,loc,p)
                        mode="exact historical base independently recovered and matched immutable HEAD working-tree representation"
                    bound_checks.append(dict(source=source,location=loc,reference=v,mode=mode))
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
    canonical_investigation=load(INVESTIGATION+"result-revision-0002.json")
    assert canonical_investigation["work_id"]==WORK
    audit=load(BASE+"20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f/result.json")
    assert audit["outcome"]=="INCONSISTENT"
    related=[
      *MASTER,"docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
      "docs/ai/prompts/REQUIREMENT_ANALYSIS_PROMPT.md",
      "docs/ai/guidelines/CORRECTIVE_CHANGE_GUIDELINES.md","docs/ai/prompts/CORRECTIVE_CHANGE_PROMPT.md",
      "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
      "docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md",
      "docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md",
      ".github/skills/governance-amendment-application/SKILL.md"]
    for p in related: read(p)
    for p,h in MASTER.items(): assert sha(read(p))==h
    # Semantic assertions are corroboration of actual source inspection, not product tests.
    guideline=read(tpaths[0]).decode("utf-8")
    prompt=read(tpaths[1]).decode("utf-8")
    request=read(tpaths[2]).decode("utf-8")
    skill=read(tpaths[3]).decode("utf-8")
    corrective=read(tpaths[4]).decode("utf-8")
    analysis=read("docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md").decode("utf-8")
    for phrase in ["identified unapproved source","current approved Requirement","resulting version remains unapproved",
        "immutable source and version lineage","complete independent Requirement Analysis Verification",
        "separate formal Human Requirement Approval","stop and request clarification"]:
        assert phrase in guideline,phrase
    assert "Do not invent a Finding or formal Requirement Approval" in prompt
    assert "RESULT REMAINS UNAPPROVED" in request
    assert "Preserve the initial result as unapproved" in skill
    assert "Post-Requirement-Update Requirement Analysis" in analysis
    for phrase in ["planned identity-only paths and hashes","only the actual preparer",
         "both preparer and applier must be bound to their own attempts",
         "mismatch blocks that stage","each actual actor must qualify in its own current invocation"]:
        assert phrase in corrective,phrase
    for phrase in ["transient","same-principal","not an extra Human Approval validity"]:
        assert phrase.lower() in read(PROPOSER+"report.md").decode("utf-8").lower(),phrase
    final_snapshot=snapshot(); assert final_snapshot==initial_snapshot()
    d=common("checkpoint_2",sequence=2,last_confirmed_boundary="All independent machine byte/binding/preservation checks completed afresh after compliant invocation/readback",
        related_records=[fingerprint(OWN/"attempt.json"),fingerprint(OWN/"checkpoint-0001.json")],
        outcome="PASS",actual_application_outcome=ar["outcome"],
        targets=rows,patch=dict(bytes=len(patch),sha256=sha(patch),exact_native_diff_equal=True),
        authority=dict(approval_exact_ascii=APPROVAL,application_start_exact_ascii=APPSTART,
            verification_retry_start_exact_ascii=START,complete_approval_target_actor_route_byte_contract_equal=True,
            package=[fingerprint(p) for p in SUPPLIED if not p.startswith(PRIOR)]),
        actors=proposal["actors"],
        application_ordering=dict(invocation=fingerprint(APPLIER+"attempt.json"),
            readback=fingerprint(APPLIER+"checkpoint-0001.json"),preflight=fingerprint(APPLIER+"evidence/preflight.json"),
            helper=fingerprint(APPLIER+"attachments/application-tool.py"),
            inspected_helper_gates_all_bases_and_full_reconstructions_before_first_write=True,
            observation="Bound ordered readback/preflight records plus actual inspected helper control flow, not trusted exhaustive OS write trace"),
        preservation=dict(original_count=474,unchanged_count=469,exact_changed_paths=changed,
            additions_since_application=additions,removals=removals,
            all_current_tracked_status_matches_application_final=True,preexisting_tracked_modification_count=len(before_tracked),
            HEAD_branch_origin_index_unchanged=True),
        nested_binding_checks=bound_checks,read_inputs=sorted(READS.values(),key=lambda x:x["path"]),
        latest_audit_reported_state=audit,prior_unsuccessful_records=fingerprint(PRIOR+"result.json"),
        prior_assurance_reused=False,retroactive_authorization=False,
        snapshot_matches_initial=True,snapshot=final_snapshot,limitations=LIMITS,
        unfinished_work="Human-facing cross-document Verification criterion assessment and final publication",
        blockers=[],pending_gates=["Separate Review only after valid Verification PASS and separate fresh Human start"],
        safe_continuation_prerequisites="Same one qualified invocation, unchanged evaluated input snapshot",events=EVENTS.copy())
    print(json.dumps(publish("checkpoint-0002.json",d),indent=2))

def criteria(cp):
    return [
      dict(id="V01",criterion="Current Human stage-start, scope and predecessor",outcome="PASS",
        evidence="Exact new Human ASCII start authorizes ONE fresh Verification retry only, after complete Application. Current Work ID/cycle/repository/package resolved. Prior terminal CANNOT COMPLETE is preserved as unsuccessful, not assurance, and not retroactively authorized.",
        refs=[fingerprint(OWN/"attempt.json"),fingerprint(PRIOR+"result.json"),fingerprint(APPLIER+"result.json")]),
      dict(id="V02",criterion="Common metadata, qualification and record-first boundary",outcome="PASS",
        evidence="Current Artifact section 33.1 and Traceability section 30.1 read before publication. Both full native actual invocation and manifest objects validated for common fields/types, references, scope, actors, authorization and exact bytes while .partial; fsync and atomic no-overwrite rename followed. Separate fresh process reopened/validated both finals and entire input boundary before substantive checks. This attempt's invocation is valid; no replacement invocation was created.",
        refs=[fingerprint(OWN/"attempt.json"),fingerprint(OWN/"input-manifest.json"),fingerprint(OWN/"checkpoint-0001.json")]),
      dict(id="V03",criterion="Independent current verifier and approved actor bindings",outcome="PASS",
        evidence="Actual verifier harness ID 8e0bf478-bfeb-461b-90ed-64033f60f8d5 differs from actual preparer 4d0c3747-fde6-48c7-b125-5adb2af5b80c and applier ec7a8339-a9b5-4710-bb5b-a8760309005d. Four role definition paths/hashes are distinct. Actual verifier definition equals approved planned binding. Reviewer remains planned-only independent definition, with no future runtime/attempt invented. Applier is separately distinct from excluded Orchestrator/active-cycle Remediation definitions. Current assignment/harness attribution, not shared session title or an external identity guarantee, establishes current role.",
        refs=[fingerprint(".github/agents/independent-governance-verification.agent.md"),fingerprint(PROPOSER+"attempt.json"),fingerprint(APPLIER+"attempt.json")]),
      dict(id="V04",criterion="Current capabilities, permissions and own publication",outcome="PASS",
        evidence="Successful current reads, SHA256 computation, Git non-mutating path/status/index/diff queries, complete-object strict JSON positive/negative selftests and own partial/flush/atomic-no-overwrite publication/readback establish executable capability. Current ACL/principal evidence is captured in manifest and invocation. Write-capable tools and inherited Modify are disclosed; no source-write probe. Publication limited to exact own attempt paths.",
        refs=[fingerprint(OWN/"input-manifest.json"),fingerprint(OWN/"attempt.json")]),
      dict(id="V05",criterion="Exact approval/designation and separate Application start",outcome="PASS",
        evidence="Actual supplied ASCII approval/designation and separate start equal Application Human authorization. Approved full report/proposal/patch paths/sizes/hashes, all target replacement objects, actor definitions, route, byte contract and exclusions checked as native complete objects. Exact scoped one-time applier designation is fresh, not historical authority. No approval inferred from hash/start/direction; no extra residual-risk acknowledgement gate imposed. Authenticated chat IDs/time unavailable and not invented.",
        refs=[fingerprint(APPLIER+"evidence/human-authorization.json"),fingerprint(PROPOSER+"report.md"),fingerprint(PROPOSER+"attachments/exact-proposal.json"),fingerprint(PROPOSER+"attachments/minimal.patch")]),
      dict(id="V06",criterion="Actual Application qualification, ordering and complete result",outcome="PASS",
        evidence="Native Application result is COMPLETED, with no error/preservation error/downstream/adoption/effectiveness claim. Its own actual attempt/current permissions/capability evidence, independent readback and all-five preflight bind exact records. Recorded ordering plus inspected actual helper control flow requires independent readback, complete approval checks, all bases and full reconstruction before first write, then exact post-write readback. This is procedural evidence, not an exhaustive trusted OS write trace.",
        refs=[fingerprint(APPLIER+"attempt.json"),fingerprint(APPLIER+"checkpoint-0001.json"),
              fingerprint(APPLIER+"evidence/preflight.json"),fingerprint(APPLIER+"attachments/application-tool.py"),
              fingerprint(APPLIER+"evidence/application-evidence.json"),fingerprint(APPLIER+"result.json")]),
      dict(id="V07",criterion="Five approved base and after byte identities; exact patch",outcome="PASS",
        evidence="Every actual after target was independently reverse-reconstructed to the approved base; Git immutable HEAD's filtered working-tree representation equals each base. Every forward single occurrence/byte offset matches; complete after bytes equal approved hashes and the native combined unified diff equals approved patch. Raw Git LF blobs are not confused with approved CRLF worktree bytes. UTF8/noBOM/CRLF and first-four-no-final-newline/fifth-final-newline states preserved. All other bytes in every target preserved.",
        refs=[fingerprint(OWN/"checkpoint-0002.json"),fingerprint(PROPOSER+"attachments/exact-proposal.json"),fingerprint(PROPOSER+"attachments/minimal.patch")]),
      dict(id="V08",criterion="Complete scope, other-file preservation and nested bindings",outcome="PASS",
        evidence=f"All 474 pre-Application inputs rehashed afresh: five approved changed paths exactly, 469 unchanged, zero removal. Full Application final inventory matches actuals. Added paths reconcile only to Application outputs and preserved earlier unsuccessful verifier records. Six preexisting tracked modifications retained; current tracked statuses equal Application final; HEAD/branch/origin/index unchanged. All {len(cp['nested_binding_checks'])} nested reference occurrences checked, including historical bases; canonical Investigation revision 0002/terminal checkpoint used.",
        refs=[fingerprint(OWN/"checkpoint-0002.json"),fingerprint(APPLIER+"evidence/input-manifest.json"),fingerprint(INVESTIGATION+"result-revision-0002.json")]),
      dict(id="V09",criterion="F003 cross-document lifecycle and immutable source lineage",outcome="PASS",
        evidence="Guideline section 2, Prompt input 1/2/6 and initial paragraph, Request source-status/initial fields, and Skill sections 3/4 consistently admit only the identified immutable unapproved initial clarification source before first formal approval, with explicit Analysis questions, Human answers/decisions and update request. Result remains unapproved; source/result lineage/immutability preserved under Artifact section 8.4 and Update sections 7/14. Subsequent Analysis, complete independent Verification, resolution and separate formal Human Requirement Approval remain required (Update section 16/Skill 8/Analysis 14, phases 5-10). Approved-source changes retain current approved source. No implementation against unapproved Requirement or finding-control bypass introduced.",
        refs=[fingerprint(p) for p in [
          "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md","docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md",
          "docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",".github/skills/requirement-update/SKILL.md",
          "docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md","docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md"]]),
      dict(id="V10",criterion="F004 stage-specific actual versus planned actors",outcome="PASS",
        evidence="Only the enhancement actor-fields paragraph changed. Actual preparer bound at proposal stage; intended applier freshly designated and qualifies in its own separately started Application, with preparer/applier own attempts before source work. Future verifier/reviewer are planned definition path/hash only until successful predecessor gates and fresh starts. Each actual actor must publish/readback its own current qualification and match approved planned binding, otherwise stop for updated Human decision/exact approval. Four distinct actors, additional applier exclusions, separate Audit fresh-start and current-invocation requirements remain. Matches unchanged Application controls; no future capability asserted.",
        refs=[fingerprint("docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md"),
          fingerprint("docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md"),
          fingerprint("docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md"),
          fingerprint("docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md")]),
      dict(id="V11",criterion="52-core and seven-group boundary; no over-propagation",outcome="PASS",
        evidence="Only five identified non-Master existing artifacts changed. No artifact/category/group added or removed; Requirement Update has no Agent to align. Seven separately assessed mechanisms remain Governance Audit, Governance Remediation, SDLC Process Orchestration, SDLC Portability Assessment, Governance Amendment Application, Independent Governance Verification, Independent Governance Review, outside 52-core count. Three Masters and unchanged Analysis/Application coupled controls retain applicable relationships. Product Requirement/Plan are N/A; no broader product work or new workflow authority created.",
        refs=[fingerprint("docs/ai/sdlc/SDLC_GOVERNANCE.md"),fingerprint("docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md"),
              fingerprint("docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md"),fingerprint(OWN/"checkpoint-0002.json")]),
      dict(id="V12",criterion="Human gates, Master/non-Master effectiveness and prior status",outcome="PASS",
        evidence="Existing governance-root decision freshly resolved; normal finding-led non-Master continuation allowed under Governance section 3, not reused bootstrap stage authority. Product root and candidate Master baseline remain unadopted. This Verification alone does not close either finding or claim effectiveness. Separate Review then full qualifying Audit required; non-Master effectiveness does not require adopting candidate Masters, while Master change/adoption retains separate Human gate. Latest full Audit remains INCONSISTENT until new full Audit. Earlier resolved findings not reopened.",
        refs=[fingerprint("docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md"),fingerprint("docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md"),
              fingerprint(BASE+"20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f/result.json")]),
      dict(id="V13",criterion="Procedural nonmutation, full hidden input boundary and limitations",outcome="PASS",
        evidence="Manifest includes hidden .github, all relied governing/role/source and approval/proposal/Application/upstream/history/unsuccessful records, actual path sets, expected presence/absence, tracked/untracked states, bytes/SHA256, file modes, current ACLs and Git/index/worktree state. Only exact own output paths excluded. Fresh readback, preassessment, machine boundary, post-source-inspection and final prepublication comparisons all equal initial. Own helper evolved only in explicitly excluded own unpublished helper path; final helper identity bound. No source/upstream/other-actor write. Actor-visible ordered operations/errors and concurrency limits disclosed. Exact proposal discloses transient/same-principal residual risks; report/evidence retain them without extra approval gate.",
        refs=[fingerprint(OWN/"input-manifest.json"),fingerprint(OWN/"checkpoint-0001.json"),fingerprint(OWN/"checkpoint-0002.json")])
    ]

def finish():
    cp=load((OWN/"checkpoint-0002.json").relative_to(ROOT).as_posix())
    assert cp["outcome"]=="PASS" and cp["snapshot_matches_initial"]
    inv=load((OWN/"attempt.json").relative_to(ROOT).as_posix()); validate(inv,"invocation")
    assert inv["authorization"]["fresh_start_exact_ascii"]==START
    assert cp["prior_assurance_reused"] is False
    for p,(size,h) in SUPPLIED.items():
        b=read(p); assert (len(b),sha(b))==(size,h)
    for r in cp["targets"]: assert binding(r["actual_after"])
    cr=criteria(cp); assert len(cr)==13 and all(c["outcome"]=="PASS" for c in cr)
    semantic_sources=[
      PROPOSER+"report.md",PROPOSER+"attachments/exact-proposal.json",APPLIER+"report.md",
      "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md","docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md",
      "docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",".github/skills/requirement-update/SKILL.md",
      "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md","docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
      "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",*MASTER]
    for p in semantic_sources: read(p)
    boundary=checkpoint("checkpoint-0003.json",3,
        "Cross-document source inspection/criterion assessment complete; no discrepancies or unresolved required evidence in this five-file Verification scope",
        "Final input recheck and own report/evidence/result publication only")
    final=checkpoint("checkpoint-final.json",4,
        "Final prepublication complete input/path-set/Git/permission comparison equals initial; all thirteen criteria PASS",
        "Publish own final Verification evidence/report/result; stop without starting Review")
    ops=[
      dict(sequence=1,tool="functions.powershell",shells=["1196","1197","1198"],
           operation="Read exact current verifier Skill/role/Guideline/Prompt/Request, Artifact 33.1 and Traceability 30.1; environment/principal/ACL qualification"),
      dict(sequence=2,tool="functions.github-mcp-server-issue_read",
           arguments=dict(owner="ScalableParimal",repo="SupportIQ",issue_number=3,method="get_comments",perPage=100),
           operation="Fresh existing-root OWNER comment 6522916236 resolution; original bootstrap stage NOT current-stage authorization"),
      dict(sequence=3,tool="functions.apply_patch",
           operation="Created only new attempt's own explicitly excluded unpublished verifier.py helper"),
      dict(sequence=4,tool="functions.powershell",shells=["1199"],
           operation="Prepare complete native actual invocation/manifest .partial; required-field/type/identity/binding/roundtrip/flush checks before any final rename; no substantive assessment"),
      dict(sequence=5,tool="functions.powershell",shells=["1200"],
           operation="Fresh-process revalidate both complete partial objects and unchanged snapshot; atomic same-directory no-overwrite final publication/read/hash"),
      dict(sequence=6,tool="functions.powershell",shells=["1201"],
           operation="Independent fresh-process final invocation/manifest validation and complete input-boundary recheck; checkpoint before substantive checks"),
      dict(sequence=7,tool="functions.apply_patch / functions.powershell",shells=["1202"],
           operation="Independent assessment within same single qualified attempt; unpublished semantic disclosure assertion used lowercase same-principal against actual report's capitalized Same-principal; stopped before machine checkpoint publication, no source changes",
           outcome="Repairable unpublished helper assertion error; not missing input/base/authority"),
      dict(sequence=8,tool="functions.apply_patch / functions.powershell",shells=["1203"],
           operation="Corrected only case matching in own unpublished assertion, preserving required disclosure check. Recomputed full input boundary and all machine checks afresh in SAME attempt; no new invocation, no replacement/restart; all checks passed and machine checkpoint published"),
      dict(sequence=9,tool="functions.view / functions.rg",
           operation="Read actual target lifecycle/actor paragraphs, complete Prompt/Request and relevant Skill; Analysis 14/phases 5-10, Application controls, approved full route/exclusions/risks, Application report, Masters 3/4/42 and propagation boundaries. Optional guessed Audit guideline search path absent; no required input missing and no Audit executed."),
      dict(sequence=10,tool="functions.powershell",shells=["1204"],
           operation="Read exact Artifact 3.5 seven-group/non-Master effectiveness and 8.4 immutable Requirement rules"),
      dict(sequence=11,tool="functions.apply_patch / functions.powershell",
           operation="Only own final helper/criterion/report/evidence/result preparation; complete semantic-boundary and final input rechecks; validated/flushed partials, atomic no-overwrite publication and readback/hash")
    ]
    initial=initial_snapshot()
    ev=common("verification_evidence",execution_status="COMPLETED",outcome="PASS",
        subject="Completed approved five-file Application GOV-AUD-20261102-003 and GOV-AUD-20261102-004 only",
        related_records=[fingerprint(OWN/"attempt.json"),fingerprint(OWN/"checkpoint-0001.json"),
            fingerprint(OWN/"checkpoint-0002.json"),boundary,final],
        criteria=cr,unresolved_findings=[],blockers=[],limitations=LIMITS,
        assurance_mode="procedural non-mutation",
        input_manifest=fingerprint(OWN/"input-manifest.json"),
        exact_evaluated_state=dict(targets=cp["targets"],repository=initial["repository"]),
        machine_checks=cp,
        human_authorizations=dict(fresh_verification_retry_start=START,approval_designation=APPROVAL,
            separate_application_start=APPSTART,source="Actual Human wording explicitly supplied in current/parent request",
            authenticated_message_id=None,authenticated_author_id=None,original_decision_time=None),
        root_authority=inv["authorization"]["existing_root"],
        current_runtime=inv["current_runtime"],
        own_unpublished_helper_evolution=dict(initial_qualification_helper_reference=inv["operation_evidence"]["helper_sha256"],
            final_executed_helper=fingerprint(OWN/"verifier.py"),
            boundary="Only this exact own helper path is excluded. It was extended for checks/publication after qualification; no source or evaluated input changed. Prior helpers/invocations/records remain immutable manifest inputs."),
        prior_unsuccessful_records=dict(prior_result=fingerprint(PRIOR+"result.json"),
            prior_report=fingerprint(PRIOR+"report.md"),prior_evidence=fingerprint(PRIOR+"verification-evidence.json"),
            earlier_initial_invocation=fingerprint(INITIAL+"invocation.json"),
            status="Preserved unsuccessful, not valid assurance. No retroactive authorization or record repair. This one fresh start authorizes only this new attempt."),
        operation_observations=ops,source_inspection_refs=[fingerprint(p) for p in semantic_sources],
        final_comparison=dict(matches_initial=True,checkpoint=final,
            files=len(initial["files"]),hidden_inclusive=True,exact_own_exclusions=sorted(EXCLUDE)),
        next_permitted_process="Independent Governance Review only upon separate fresh Human stage-start and current reviewer qualification",
        downstream_started=False,review_performed=False,audit_run=False,
        effectiveness_claimed=False,findings_closed=False,master_adopted=False,product_root_adopted=False,
        source_writes=False,other_actor_record_writes=False,staging_commit_push=False,
        events=EVENTS.copy())
    # Validate complete evidence natively and recheck all actual inputs before publishing PASS evidence.
    validate(ev); assert initial==snapshot()
    ef=publish("verification-evidence.json",ev)
    lines=[
      "# Independent Governance Verification Report","",
      "**Outcome: PASS — procedural non-mutation assurance.**",
      "**Scope: completed approved five-file Application GOV-AUD-20261102-003 and GOV-AUD-20261102-004 only.**","",
      f"Work ID: `{WORK}`; Cycle `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1.",
      f"Attempt: `{ATTEMPT}`; record identity: `{ATTEMPT}:verification_report`.",
      "Repository: `ScalableParimal/SupportIQ`, `C:\\PARIMAL_SHERE\\SCALABLE_SOLUTIONS\\SupportIQ`.",
      f"HEAD `{initial['repository']['head']}`; branch `{initial['repository']['branch']}`.",
      "Product feature / Approved Requirement / Approved Implementation Plan: N/A; governance-only subject.",
      "This is Independent Governance Verification only. It is not Review, Governance Audit, approval, application, effectiveness, closure or baseline adoption.","",
      "## 1. Fresh authority, qualification and unsuccessful-record reconciliation","",
      "Actual fresh Human stage-start (exact ASCII quote):",
      "'"+START+"'","",
      "This authorizes ONE new qualified Verification attempt only. The initial incomplete invocation and unauthorized replacement/terminal records remain unchanged and unsuccessful, not valid assurance. The present Human start does not retroactively authorize that replacement. No prior byte-check conclusion was reused as proof; required checks were executed afresh after the current compliant invocation/readback boundary. No further replacement attempt was created.",
      "Actual original Human exact approval/designation (exact ASCII quote):",
      "'"+APPROVAL+"'","",
      "Actual separate Human Application stage-start (exact ASCII quote):",
      "'"+APPSTART+"'","",
      "These actual Human decisions were explicitly supplied in the current/parent request. Their authenticated platform message IDs/author IDs and original decision times are unavailable; none is invented. Approval is not inferred from fingerprints or stage-start. Exact approved report/proposal/patch, targets, base/after fingerprints, replacements, scope/exclusions, actors, byte contract and route match the actual authorization record. No additional residual-risk acknowledgement validity gate is imposed.",
      "Before own invocation publication, the exact current role/Skill/Guideline/Prompt/Request and Artifact Governance section 33.1/Traceability section 30.1 were read. Both complete native actual invocation and hidden-inclusive manifest objects were prepared under .partial; explicit required-field/type/binding validation and strict serialize/parse equality completed before any final rename. This validator implements current common metadata requirements; it does not claim a separately adopted external schema.",
      f"Invocation `{fingerprint(OWN/'attempt.json')['path']}`, {fingerprint(OWN/'attempt.json')['bytes']} bytes, SHA-256 `{fingerprint(OWN/'attempt.json')['sha256']}`.",
      f"Input manifest `{fingerprint(OWN/'input-manifest.json')['path']}`, {fingerprint(OWN/'input-manifest.json')['bytes']} bytes, SHA-256 `{fingerprint(OWN/'input-manifest.json')['sha256']}`.",
      "A fresh publishing process independently revalidated both partial objects and the full unchanged snapshot before validated/flushed atomic same-directory Windows no-overwrite renames. A separate fresh process independently reopened and integrity-checked both finals and the complete input boundary before substantive checks.",
      f"Independent boundary/readback `{fingerprint(OWN/'checkpoint-0001.json')['path']}`, SHA-256 `{fingerprint(OWN/'checkpoint-0001.json')['sha256']}`. Tool ordering: prepare 1199, publish 1200, separate readback 1201, subsequent machine assessment 1202/1203.",
      "The only internal assessment error was an unpublished case-sensitive residual-disclosure assertion: lowercase same-principal versus the actual report's capitalized Same-principal. The same attempt corrected that helper assertion without weakening disclosure checks, rechecked all input boundaries and reran all checks. No malformed or incomplete final record was published, no source repaired, and no new invocation/restart occurred.","",
      "## 2. Current independent identity, runtime capability and permission","",
      f"Verifier harness ID `{ACTOR}`; Copilot invocation `{inv['current_runtime']['copilot_agent_session_id']}`; principal `{inv['current_runtime']['effective_principal']}`; host session `ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60`.",
      "Attribution is the supplied/current harness identity plus current independent-verifier assignment and exact approved definition binding, not shared session title or an externally authenticated identity guarantee. This verifier is not preparer, applier, reviewer, active Remediation actor or Orchestrator.",
      "Actual preparer runtime `4d0c3747-fde6-48c7-b125-5adb2af5b80c`; actual applier runtime `ec7a8339-a9b5-4710-bb5b-a8760309005d`. Four approved definition paths and fingerprints are distinct. Actual verifier definition `.github/agents/independent-governance-verification.agent.md` equals approved planned SHA-256 `ECD11EFE7F0078FE0B258DE819C8E473A3CF3EC674C8999E49F04194D62B8958`.",
      "Reviewer remains planned-only `.github/agents/independent-governance-review.agent.md`, SHA-256 `1CD8CCC4A96EFA64D4AA3B64DDDB2874F2337A45301B6B953033FC9016A9812E`; no reviewer attempt/current runtime/capability/start is invented. At Review, its actual independent identity must match and qualify under its own fresh start.",
      "Observed current capability includes complete input reads/SHA256, non-mutating Git status/tracked/index/HEAD/branch/diff queries, native complete-object strict JSON roundtrip and duplicate/nonfinite negative selftests, and own authorized flushed partial/atomic-no-overwrite publication/readback. ACLs show Users ReadAndExecute and inherited Authenticated Users Modify; Administrators/SYSTEM FullControl. Writable ACLs/tools are not themselves a blocker under the procedural contract, and no source-write probe was performed.","",
      "## 3. Exact authority package and actual Application","",
      "Existing governance-root decision was freshly resolved through canonical OWNER comment https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236; author ScalableParimal, user 226102895, created/updated 2026-10-30T12:31:51Z. Its repository/HEAD/WorkID/root/three Master hashes match. This preserves existing root adoption; it does not reuse the original bootstrap Audit stage as Verification authority. Governance section 3 permits normal finding-led non-Master continuation under the present fresh start. Product root and candidate Master baseline remain unadopted.",
      "Canonical Investigation revision 0002 and terminal checkpoint bindings were resolved and recomputed; superseded bundles were not used as current conclusions. Both accepted findings remain separate and not closed.",
      "The native Application outcome is **COMPLETED**, not a blanket PASS. Its actual own attempt, current runtime/permission/capability evidence, separate invocation readback, full five-target preflight, actual report/result/evidence and terminal checkpoint match their exact bindings. Bound record ordering plus inspection of the actual non-executed Application helper control flow establishes the procedural all-five-before-first-write/readback ordering. It is not proof from an exhaustive trusted OS event stream.",
      "",
      "| Canonical package/Application input | Bytes | SHA-256 |",
      "|---|---:|---|"]
    for p in [PROPOSER+"report.md",PROPOSER+"result.json",PROPOSER+"attachments/exact-proposal.json",
          PROPOSER+"attachments/minimal.patch",PROPOSER+"evidence/decision-evidence.json",
          APPLIER+"report.md",APPLIER+"result.json",APPLIER+"evidence/application-evidence.json",APPLIER+"checkpoint-0002.json"]:
        r=fingerprint(p); lines.append(f"| `{p}` | {r['bytes']} | `{r['sha256']}` |")
    lines+=["","## 4. Independent byte-exact checks and preservation","",
      "Every actual target was independently reversed to its exact approved base, matched against immutable HEAD content in Git working-tree representation, and replayed through every approved sequential single-occurrence UTF8 replacement at the exact byte offset. Complete reconstructed after bytes equal actual bytes and approved after hashes. The native regenerated combined unified diff equals the approved minimal.patch bytes. Raw Git LF blobs are distinguished from CRLF worktree bytes; no normalization of evaluated files was performed.",
      "All five targets preserve UTF8 without BOM and CRLF. Targets 1-4 preserve no final newline; target 5 preserves a final CRLF. All nonreplacement bytes in each target are preserved.","",
      "| Target | Exact base bytes / SHA-256 | Actual after bytes / SHA-256 |",
      "|---|---|---|"]
    for r in cp["targets"]:
        b=r["approved_base"]; a=r["actual_after"]
        lines.append(f"| `{r['path']}` | {b['bytes']} / `{b['sha256']}` | {a['bytes']} / `{a['sha256']}` |")
    lines+=["",
      f"All 474 original Application input files were independently rehashed: exactly the five approved targets changed; other 469 unchanged; zero original input removed. Additional paths reconcile to Application-owned outputs and the two preserved unsuccessful verifier attempts only. Six preexisting tracked modifications remain, actual tracked statuses equal the Application final set, and HEAD/branch/origin/index remain unchanged.",
      f"All {len(cp['nested_binding_checks'])} nested bound path/byte/hash reference occurrences were recomputed, not merely one per path. Historical base references are distinguished from current after bytes and independently recovered. Machine assessment read {len(cp['read_inputs'])} distinct input paths. Inventory/hash reads do not mean every file received substantive governance assessment.",
      f"The current manifest covers {len(initial['files'])} repository inputs, including hidden .github, current governing sources/roles and every relied approval/proposal/Application/Investigation/Audit/upstream/history/unsuccessful record. It records exact paths/presence/expected absences/directories, tracked/untracked state, byte counts/SHA256, file modes, applicable current ACLs and Git/index/worktree state. Only the exact own output names and their partials are excluded, never a whole records root or prior attempt.",
      "Full comparisons equal the initial bounded snapshot at independent readback, preassessment, machine boundary, source-inspection boundary and final prepublication. Meaningful checkpoints retain that evidence. No additions/removals/renames or unexplained index/worktree drift occurred within the evaluated set.","",
      "## 5. Criterion-by-criterion Verification result",""]
    for c in cr:
        lines += [f"### {c['id']} — {c['criterion']}: PASS",c["evidence"],""]
    lines+=["## 6. Cross-document effects and downstream boundaries","",
      "F003: The four actual Update artifacts now admit initial immutable unapproved clarification only before first formal Human approval, bind initial Analysis questions/explicit Human answers and explicit update request, preserve immutable source/result lineage and keep the result unapproved. Existing Update sections 7/13/14/16 and Skill 5/7/8 preserve complete downstream Analysis, independent Verification, resolution and separate formal Human Requirement Approval. Approved-source changes retain the approved-source branch. This agrees with Analysis section 14/phases 5-10 and Master Artifact section 8.4; no product behavior was executed or implementation authorized.",
      "F004: Only the enhancement Actor/Human Approval paragraph changes. Current preparer/applier attempts and qualification are stage-specific; future verifier/reviewer bindings stay planned-only until successful predecessors and fresh stage-starts. Matching approved definition/current own qualification, four distinct roles, applier coordinator exclusions and separate Audit start remain. This aligns with unchanged Application Guideline/Prompt/Request; no premature future attempt or current capability is invented.",
      "No Master, Analysis, Application-control, product artifact, artifact count or mechanism-group amendment was needed or applied. The exact five-artifact propagation is minimal and consistent. Requirement Update has no Agent to align. The seven separately assessed mechanism groups remain outside the 52-core count: Governance Audit, Governance Remediation, SDLC Process Orchestration, SDLC Portability Assessment, Governance Amendment Application, Independent Governance Verification, Independent Governance Review.",
      "Artifact Governance section 3.5 requires authorized application, passing independent Verification and Review, then complete Audit CONSISTENT with every required count zero and all seven groups without unresolved issue before non-Master effectiveness. A Master change additionally needs separate prospective-baseline adoption. This PASS is only the Verification gate; it neither makes these changes effective nor adopts the existing candidate Masters or product root.",
      "Latest complete Audit `20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f` remains reported INCONSISTENT: Critical 0, High 0, Medium 2, Low 0, Ambiguities 1, Missing Governance Controls 0, Unsupported Governance Controls 1, Broken References 0. No new full Audit was run or claimed. Both findings remain accepted/not closed; prior resolved findings are not reopened.","",
      "## 7. Procedural assurance limitations and events",""]
    lines += ["- "+x for x in LIMITS]
    lines+=["",
      "The exact approved proposal discloses these material residual risks, and this report/evidence retains them. Residual-risk acknowledgement is disclosure, not another Human Approval validity gate.",
      "Operation evidence combines ordered actor-visible tool calls (arguments or integrity-bound safe representations, errors/outcomes and observable paths) with structured helper events. Events cover current qualification, partial validation, separate publication/readback, independent checks, repaired unpublished assertion, source inspection and final comparisons. No exhaustive trusted OS trace, enforced technical source-write exclusion or security guarantee is claimed.",
      "No coordinated exclusive filesystem interval is guaranteed. Current actor is not a competing writer; idle/stale prior metadata is not evidence of live concurrency. External writers and same-principal tampering cannot be excluded. Matching endpoints show the bytes observed, not a continuous write-free history.",
      "The exact own helper path was explicitly excluded from evaluated inputs and extended only as this verifier's unpublished implementation helper. Qualification-time and final helper fingerprints are retained in evidence; all earlier helpers/invocations/final records were evaluated as immutable inputs. Only the current actor's new records were published.","",
      "## 8. Canonical output bindings, completion and stop","",
      f"Evidence: `{ef['path']}`; {ef['bytes']} bytes; SHA-256 `{ef['sha256']}`.",
      f"Machine checkpoint: `{fingerprint(OWN/'checkpoint-0002.json')['path']}`; SHA-256 `{fingerprint(OWN/'checkpoint-0002.json')['sha256']}`.",
      f"Source-inspection boundary: `{boundary['path']}`; SHA-256 `{boundary['sha256']}`.",
      f"Final boundary: `{final['path']}`; SHA-256 `{final['sha256']}`.",
      "This report's result.json is published only after final report/evidence bytes are durably available; it binds their exact path/size/SHA256. Complete actual native objects are validated/strictly roundtripped before partial flush/atomic no-overwrite final publication, then independently read back. No existing final record was overwritten.",
      "**No unresolved Verification finding or required-evidence blocker remains for this five-file scope. PASS.**",
      "**Next permitted gate: separate fresh Human initiation of Independent Governance Review by the approved distinct reviewer, with its own current qualification, complete input manifest, publication/readback and matching planned identity. This report does not start Review.**",
      "Only after passing Review may a separately Human-started complete Governance Audit assess the full current 52-core/seven-group scope and effectiveness conditions. No Review, Audit, source fix, application, approval, adoption, staging, commit, push or product work occurred. **STOP.**",""]
    report="\n".join(lines)
    assert "`n" not in report and "[STABLE ID]" not in report
    rf=publish("report.md",report,text=True)
    assert initial==snapshot()
    result=common("verification_result",execution_status="COMPLETED",outcome="PASS",
        subject_type="GOVERNANCE_APPLICATION",finding_ids=["GOV-AUD-20261102-003","GOV-AUD-20261102-004"],
        related_records=[fingerprint(OWN/"attempt.json"),fingerprint(OWN/"checkpoint-0001.json"),
            fingerprint(APPLIER+"result.json"),fingerprint(PRIOR+"result.json")],
        report=rf,evidence=ef,input_manifest=fingerprint(OWN/"input-manifest.json"),
        invocation=fingerprint(OWN/"attempt.json"),invocation_readback=fingerprint(OWN/"checkpoint-0001.json"),
        machine_checkpoint=fingerprint(OWN/"checkpoint-0002.json"),
        source_inspection_checkpoint=boundary,final_checkpoint=final,
        exact_evaluated_state=dict(targets=cp["targets"],repository=initial["repository"],
            hidden_inclusive_manifest=fingerprint(OWN/"input-manifest.json")),
        criteria=cr,unresolved_findings=[],blockers=[],limitations=LIMITS,
        assurance_mode="procedural non-mutation",
        actual_application_status="COMPLETED",
        prior_attempt_disposition="Preserved unsuccessful, not valid assurance; no retroactive authorization",
        single_fresh_retry_start=START,additional_replacement_attempt_created=False,
        final_input_comparison=dict(matches_initial=True,observed_file_count=len(initial["files"]),
            exact_own_output_exclusions=sorted(EXCLUDE),checkpoint=final,
            observation="Fresh full snapshot equality immediately before terminal publication",
            final_helper=fingerprint(OWN/"verifier.py"),events=EVENTS.copy()),
        next_permitted_process="Independent Governance Review only after separate fresh Human Review stage-start",
        next_gate=dict(process="Independent Governance Review",stage_started=False,
            planned_definition=fingerprint(".github/agents/independent-governance-review.agent.md"),
            prerequisites=["Separate fresh explicit Human Review stage-start after this PASS",
              "Distinct actual reviewer matching approved planned definition binding",
              "Reviewer-owned current qualification/input manifest/invocation publication/independent readback before checks"]),
        review_performed=False,downstream_started=False,audit_run=False,effectiveness_claimed=False,
        findings_closed=False,master_adopted=False,product_root_adopted=False,
        source_writes=False,other_actor_record_writes=False,staging_commit_push=False)
    validate(result)
    for k in ["report","evidence","input_manifest","invocation","invocation_readback",
              "machine_checkpoint","source_inspection_checkpoint","final_checkpoint"]:
        assert binding(result[k]),k
    assert initial==snapshot()
    rr=publish("result.json",result)
    print(json.dumps(dict(outcome="PASS",report=rf,result=rr,evidence=ef,next_gate="Separate fresh Human Independent Governance Review start; no later stage started"),indent=2))

if __name__=="__main__":
    {"prepare":prepare,"publish-invocation":publish_invocation,"readback":readback,
     "assess":assess,"finish":finish}[sys.argv[1]]()
