import os, sys, json, hashlib, pathlib, subprocess, datetime

ROOT = pathlib.Path(__file__).resolve().parents[6]
OWN = pathlib.Path(__file__).resolve().parent
ATTEMPT = OWN.name
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ACTOR = "8e0bf478-bfeb-461b-90ed-64033f60f8d5"
NAMES = ["verifier.py", "manifest.json", "invocation.json", "invocation-readback.json",
         "checkpoint-0001.json", "checkpoint-0002.json", "checkpoint-final.json",
         "verification-evidence.json", "report.md", "result.json"]
EXCLUDE = {str((OWN/n).relative_to(ROOT)).replace("\\","/") for n in NAMES}
EXCLUDE |= {p+".partial" for p in list(EXCLUDE)}
EVENTS = []

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(b):
    return hashlib.sha256(b).hexdigest().upper()

def event(op, paths, outcome="OK", **extra):
    EVENTS.append(dict(sequence=len(EVENTS)+1, actor=ACTOR, attempt=ATTEMPT,
                       observed_at_utc=now(), operation=op, paths=paths, outcome=outcome, **extra))

def strict(b):
    def pairs(xs):
        d = {}
        for k,v in xs:
            if k in d: raise ValueError("Duplicate JSON key: "+k)
            d[k]=v
        return d
    return json.loads(b, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def encoded(obj):
    b = (json.dumps(obj, ensure_ascii=False, allow_nan=False, indent=2)+"\n").encode("utf-8")
    assert strict(b) == obj
    return b

def fp(p):
    b=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), bytes=len(b), sha256=digest(b))

def git(*args):
    c=["git","--no-optional-locks","--no-pager",*args]
    r=subprocess.run(c, cwd=ROOT, capture_output=True, check=True)
    event("non-mutating subprocess", [], arguments=c, stdout_sha256=digest(r.stdout), returncode=r.returncode)
    return r.stdout.decode("utf-8").rstrip("\r\n")

def snapshot():
    tracked=set(git("ls-files","-z").split("\0"))
    files=[]; dirs=[]
    for base,ds,fs in os.walk(ROOT):
        if pathlib.Path(base)==ROOT: ds[:]=[d for d in ds if d!=".git"]
        dirs.extend((pathlib.Path(base)/d).relative_to(ROOT).as_posix() for d in ds)
        for f in fs:
            p=pathlib.Path(base)/f; rel=p.relative_to(ROOT).as_posix()
            if rel in EXCLUDE: continue
            x=fp(p); x["tracked"]=rel in tracked
            x["mode"]=oct(p.stat().st_mode); files.append(x)
    files.sort(key=lambda x:x["path"]); dirs.sort()
    state=dict(head=git("rev-parse","HEAD"), branch=git("branch","--show-current"),
               index=fp(ROOT/".git/index"),
               tracked=sorted(x for x in tracked if x),
               status=git("status","--porcelain=v1","--untracked-files=all"),
               staged_diff_sha256=digest(git("diff","--cached","--binary","--no-ext-diff").encode()),
               worktree_diff_sha256=digest(git("diff","--binary","--no-ext-diff").encode()))
    # Own records are allowed additions only; no other untracked path is ignored.
    state["status_excluding_exact_own_outputs"]="\n".join(
        line for line in state.pop("status").splitlines()
        if line[3:].replace("\\","/") not in EXCLUDE)
    absences=[]
    for rel in ["AGENTS.md",".github/copilot-instructions.md",".github/instructions",
                "docs/AGENTS.md","docs/ai/AGENTS.md"]:
        absences.append(dict(path=rel,present=(ROOT/rel).exists()))
    s=dict(root=str(ROOT),files=files,directories=dirs,expected_presence_absence=absences,
           repository=state, exact_output_exclusions=sorted(EXCLUDE))
    event("hidden-inclusive bounded inventory, SHA256 and Git state", [str(ROOT)],
          files=len(files), path_set_sha256=digest(encoded([x["path"] for x in files])))
    return s

def publish(name,obj,text=False):
    assert name in NAMES and name!="verifier.py"
    p=OWN/name; partial=OWN/(name+".partial")
    assert not p.exists() and not partial.exists()
    b=obj.encode("utf-8") if text else encoded(obj)
    if not text: assert strict(b)==obj
    with partial.open("xb") as h:
        h.write(b); h.flush(); os.fsync(h.fileno())
    assert partial.read_bytes()==b
    if not text: assert strict(partial.read_bytes())==obj
    # Windows rename is atomic within this directory and fails if target exists.
    assert os.name=="nt"
    os.rename(partial,p)
    rb=p.read_bytes(); assert rb==b
    event("validated flushed partial -> atomic no-overwrite rename -> read/hash", [p.relative_to(ROOT).as_posix()], bytes=len(rb), sha256=digest(rb))
    return fp(p)

def compare(name):
    before=strict((OWN/"manifest.json").read_bytes())["snapshot"]
    after=snapshot()
    # All directories already existed at baseline. Exact output files alone are excluded.
    equal=before==after
    delta={}
    if not equal:
        b={x["path"]:x for x in before["files"]}; a={x["path"]:x for x in after["files"]}
        delta=dict(added=sorted(a.keys()-b.keys()),removed=sorted(b.keys()-a.keys()),
                   changed=[p for p in sorted(a.keys()&b.keys()) if a[p]!=b[p]],
                   repository_equal=before["repository"]==after["repository"],
                   directories_equal=before["directories"]==after["directories"])
    obj=dict(record_type="verification_input_checkpoint",actor=ACTOR,attempt=ATTEMPT,
             observed_at_utc=now(),matches_initial=equal,delta=delta,snapshot=after,events=EVENTS.copy())
    out=publish(name,obj)
    assert equal, json.dumps(delta)
    return out

def invocation():
    assert ROOT.name=="SupportIQ", str(ROOT)
    sample={"quote":"'ASCII' \"double\"", "nested":[None,True,False,{"x":"α\r\n"}], "number":17}
    assert strict(encoded(sample))==sample
    event("native JSON strict serialize/parse equality self-test",[],test_pass=True)
    manifest=publish("manifest.json",dict(record_type="verification_input_manifest",actor=ACTOR,
                     attempt=ATTEMPT,created_at_utc=now(),snapshot=snapshot()))
    obj=dict(record_type="independent_governance_verification_invocation",work_id=WORK,
       attempt_id=ATTEMPT,cycle_id="GOV-REMEDIATION-PROSPECTIVE-001",cycle=1,
       process="Independent Governance Verification",created_at_utc=now(),
       actor=dict(runtime_agent_id=ACTOR,role="Independent Governance Verification",
          runtime_agent_id_basis="list_agents(scope=all): sole running agent is Lifecycle and Timing Verification; current assigned role; not shared session title",
          copilot_agent_session_id=os.environ.get("COPILOT_AGENT_SESSION_ID"),
          host_session="ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
          effective_principal="INT-SCL-010\\Parimal",externally_authenticated_identity_claimed=False),
       fresh_human_start="Yes, initiate Independent Governance Verification for the GOV-AUD-20261102-003 and GOV-AUD-20261102-004 five-file Application only",
       human_attribution="Actual current human request supplied to this invocation; no authenticated message ID or decision timestamp exposed or invented",
       stage_scope="Completed five-file Application only; no Review, Audit, adoption, fixes, product work, staging, commit or push",
       separation=dict(preparer="4d0c3747-fde6-48c7-b125-5adb2af5b80c",applier="ec7a8339-a9b5-4710-bb5b-a8760309005d",
          verifier=ACTOR,reviewer="planned independent-governance-review definition only, no current runtime asserted",
          not_active_remediation_or_orchestrator=True),
       capabilities=dict(read="Get-Content/Path.read_bytes successfully used for required role/guideline/prompt/request and stage handoff resolution",
          sha256="Get-FileHash and hashlib available; skill fingerprint independently computed",
          checks="Python 3, Git read-only queries with --no-optional-locks, full hidden-inclusive inventory available",
          source_write_exclusion=False,own_publication="Current Human explicitly authorizes only new verifier-owned attempt records; inherited Authenticated Users Modify; actual publication of manifest demonstrates capability",
          permissions="INT-SCL-010\\Parimal; attempt root inherited Users ReadAndExecute; Authenticated Users Modify; Administrators/SYSTEM FullControl; no write probe",
          events="Actor-visible ordered tool calls in conversation; helper structured ordered read/hash/check/publication events",
          unavailable="No exhaustive trusted OS event stream, external authentication, source-write sandbox or same-principal tamper exclusion"),
       assurance_mode="procedural non-mutation",
       residual_risks=["Matching endpoint fingerprints cannot prove absence of transient writes or same-principal tampering",
          "Shared principal/tools can write, but have no authority to alter sources or upstream records",
          "No coordinated exclusive filesystem lock; registry shows only this running invocation, idle metadata is not evidence of live writers; external concurrency cannot be excluded"],
       publication_scope=str(OWN.relative_to(ROOT)).replace("\\","/"),
       exact_owned_output_names=NAMES,manifest=manifest,
       preliminary_operations=[
          "Read mandatory skill through Get-Content",
          "get_current_session: shared host metadata, not role proof",
          "Environment identity + Get-FileHash + Get-Acl permissions probe",
          "Read required role, guideline, prompt and request; directory/instruction discovery",
          "Read Git status/HEAD/branch without optional locks; locate masters",
          "Read proposal/application result actor and authority metadata only for qualification",
          "list_agents all scope: one running verifier; idle entries not live writers"],
       events=EVENTS.copy())
    print(json.dumps(publish("invocation.json",obj)))

def readback():
    inv=strict((OWN/"invocation.json").read_bytes())
    man=strict((OWN/"manifest.json").read_bytes())
    assert inv["actor"]["runtime_agent_id"]==ACTOR
    assert inv["manifest"]==fp(OWN/"manifest.json")
    assert man["snapshot"]==snapshot()
    obj=dict(record_type="independent_fresh_process_invocation_readback",
         process_id=os.getpid(),actor=ACTOR,attempt=ATTEMPT,observed_at_utc=now(),
         invocation=fp(OWN/"invocation.json"),manifest=fp(OWN/"manifest.json"),
         invocation_strict_parse=True,manifest_strict_parse=True,input_snapshot_matches=True,
         events=EVENTS.copy())
    print(json.dumps(publish("invocation-readback.json",obj)))

if __name__=="__main__":
    if sys.argv[1]=="invocation": invocation()
    elif sys.argv[1]=="readback": readback()
    elif sys.argv[1]=="checkpoint": print(json.dumps(compare(sys.argv[2])))
