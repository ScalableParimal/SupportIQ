"""Own read-only Audit integrity/path checks; no source writes."""
import runpy
from pathlib import Path
import json
import re
import difflib
import sys

HERE = Path(__file__).parent
P = runpy.run_path(str(HERE/"retry-publisher.py"), run_name="audit_publisher_import")
ROOT, SCOPE, ATTEMPT = P["ROOT"], P["SCOPE"], P["ATTEMPT"]
ref, publish, record, state = (P[k] for k in ("ref","publish","record","state"))
A = SCOPE.parent
STEMS = ["REQUIREMENT_ANALYSIS","REQUIREMENT_ANALYSIS_VERIFICATION","IMPLEMENTATION_PLANNING",
         "REQUIREMENT_UPDATE","IMPLEMENTATION_PLAN_VERIFICATION","IMPLEMENTATION","IMPLEMENTATION_VERIFICATION",
         "IMPLEMENTATION_REVIEW","FINDING_INVESTIGATION","CORRECTIVE_CHANGE"]
SLUGS = ["requirement-analysis","requirement-analysis-verification","implementation-planning","requirement-update",
         "implementation-plan-verification","implementation","implementation-verification","implementation-review",
         "finding-investigation","corrective-change-decision"]
IDS = {
 "proposal":"20261102T105400Z-5145fb48-c113-4ff7-a263-5ff861ca39c5",
 "application":"20261102T110324Z-b92b73f0-deba-4842-b261-1ed22bd7d014",
 "verification":"20261102T110840Z-c1d89695-d3e5-4721-a846-3f3dca25cc22",
 "review":"20261102T1130Z-d7d84322-aff9-4d3e-9cec-90f9054705cd",
 "coordinator":"20261102T101503Z-5b64dd0c-2466-47bc-ad65-ff4979343565"}

def load(p):
    return json.loads(Path(p).read_bytes())

def compare():
    initial=load(SCOPE/"evidence/input-manifest.json")
    current=P["inventory"]()
    before={r["path"]:(r["bytes"],r["sha256"]) for r in initial["files"]}
    after={r["path"]:(r["bytes"],r["sha256"]) for r in current["files"]}
    return {"baseline_files":len(before),"current_files":len(after),
            "changed":[p for p in before.keys() & after.keys() if before[p]!=after[p]],
            "added":sorted(after.keys()-before.keys()),"removed":sorted(before.keys()-after.keys()),
            "directory_set_unchanged":initial["directories"]==current["directories"],
            "repository":state()}

def nodes(obj, loc="$"):
    if isinstance(obj,dict):
        if isinstance(obj.get("path"),str) and isinstance(obj.get("sha256"),str):
            yield loc,obj
        for k,v in obj.items():yield from nodes(v,loc+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):yield from nodes(v,loc+f"[{i}]")

def inspect():
    manifest=load(SCOPE/"evidence/input-manifest.json")
    sr=manifest["source_inventory"]
    masters=[r["path"] for r in sr if r["path"].startswith("docs/ai/sdlc/")]
    core=masters[:]
    for folder,suffix in [("guidelines","GUIDELINES"),("prompts","PROMPT"),("request","REQUEST")]:
        core += [f"docs/ai/{folder}/{stem}_{suffix}.md" for stem in STEMS]
    core += [f".github/skills/{s}/SKILL.md" for s in SLUGS]
    core += [f".github/agents/{s}.agent.md" for s in SLUGS if s!="requirement-update"]
    assert len(set(core))==52
    assert all((ROOT/p).is_file() for p in core)
    mechanisms={
      "Governance Audit":[".github/skills/sdlc-governance-audit/SKILL.md",".github/agents/sdlc-governance-audit.agent.md"],
      "Governance Remediation":[".github/agents/sdlc-governance-remediation.agent.md"],
      "SDLC Process Orchestration":[".github/agents/sdlc-process-orchestrator.agent.md"]}
    for name,stem,slug in [
      ("SDLC Portability Assessment","PORTABILITY_ASSESSMENT","portability-assessment"),
      ("Governance Amendment Application","GOVERNANCE_AMENDMENT_APPLICATION","governance-amendment-application"),
      ("Independent Governance Verification","INDEPENDENT_GOVERNANCE_VERIFICATION","independent-governance-verification"),
      ("Independent Governance Review","INDEPENDENT_GOVERNANCE_REVIEW","independent-governance-review")]:
        mechanisms[name]=[f"docs/ai/guidelines/{stem}_GUIDELINES.md",f"docs/ai/prompts/{stem}_PROMPT.md",
                          f"docs/ai/request/{stem}_REQUEST.md",f".github/skills/{slug}/SKILL.md",f".github/agents/{slug}.agent.md"]
    expected=set(core)|{p for ps in mechanisms.values() for p in ps}
    actual={r["path"] for r in sr}
    assert expected==actual and len(expected)==76
    traces=[]
    for stem,slug in zip(STEMS,SLUGS):
        paths=[f"docs/ai/guidelines/{stem}_GUIDELINES.md",f"docs/ai/prompts/{stem}_PROMPT.md",
               f"docs/ai/request/{stem}_REQUEST.md",f".github/skills/{slug}/SKILL.md"]
        g,p,r,s=[(ROOT/x).read_text(encoding="utf-8") for x in paths]
        assert paths[0] in p and paths[1] in r and all(x in s for x in paths[:3])
        assert f"name: {slug}" in s
        ag=None if slug=="requirement-update" else f".github/agents/{slug}.agent.md"
        if ag: assert paths[3] in (ROOT/ag).read_text(encoding="utf-8")
        traces.append({"process":slug,"guideline":paths[0],"prompt":paths[1],"request":paths[2],"skill":paths[3],
                       "agent":ag,"link_resolution":"PASS","semantic_exceptions":
                       ["GOV-AUD-20261102-003"] if slug=="requirement-update" else
                       ["GOV-AUD-20261102-004"] if slug=="corrective-change-decision" else []})
    references=[]
    for rr in sr:
        path=rr["path"];text=(ROOT/path).read_text(encoding="utf-8")
        for lineno,line in enumerate(text.splitlines(),1):
            # Inspect literal explicit Markdown governance paths. Generalized placeholders are context, not missing artifacts.
            found=re.findall(r"(?:\.github[\\/][A-Za-z0-9_./\\-]+|docs[\\/][A-Za-z0-9_./\\-]+|scripts[\\/][A-Za-z0-9_./\\-]+)",line)
            for item in found:
                target=item.rstrip(".,;:").replace("\\","/")
                if "<" in line and not target.endswith(".md"):continue
                exists=(ROOT/target).exists()
                optional=target in ("docs/tools/ApprovalAlarm.md","scripts/ApprovalAlarm.ps1")
                product=target.startswith(("docs/requirement/","docs/implementation/"))
                references.append({"source":path,"line":lineno,"target":target,"exists":exists,
                  "treatment":"CONDITIONAL OPTIONAL alarm integration, explicitly skip if absent" if optional else
                  "PRODUCT REFERENCE ONLY; content excluded" if product else "RESOLVED" if exists else "REVIEW"})
    target=ROOT/".github/agents/sdlc-governance-remediation.agent.md"
    preimage=A/IDS["application"]/"attachments/target-before.bin"
    proposal=load(A/IDS["proposal"]/"attachments/proposal.json")
    old=proposal["replacement"]["before"].encode("utf-8");new=proposal["replacement"]["after"].encode("utf-8")
    before=preimage.read_bytes();after=target.read_bytes()
    assert before.count(old)==1 and after.count(new)==1
    assert before.replace(old,new,1)==after and after.replace(new,old,1)==before
    assert ref(preimage)["sha256"]==proposal["base"]["sha256"]
    assert ref(target)["sha256"]==proposal["expected_after"]["sha256"]
    patch="".join(difflib.unified_diff(before.decode("utf-8").splitlines(True),after.decode("utf-8").splitlines(True),
                fromfile="a/.github/agents/sdlc-governance-remediation.agent.md",
                tofile="b/.github/agents/sdlc-governance-remediation.agent.md"))
    patch_bytes=(A/IDS["proposal"]/"attachments/proposed.patch").read_bytes()
    patch_match=patch.replace("\r\n","\n").encode("utf-8")==patch_bytes
    # Fingerprint checks do not substitute for assessment of approval/authority.
    checks=[];seen=set();historical=[]
    for role,aid in IDS.items():
        files=[A/aid/"result.json", A/aid/"attempt.json"]
        for more in ["attachments/proposal.json","attachments/application.json","attachments/evidence.json",
                     "attachments/review-evidence.json","checkpoint-0001.json","checkpoint-0002.json",
                     "checkpoint-0003.json","checkpoint-0004.json"]:
            p=A/aid/more
            if p.exists():files.append(p)
        for p in files:
            doc=load(p)
            assert json.loads(json.dumps(doc,ensure_ascii=False))==doc
            for loc,rr in nodes(doc):
                rp=rr["path"].replace("\\","/");digest=rr["sha256"].upper()
                if len(digest)!=64 or not re.fullmatch("[0-9A-F]{64}",digest):continue
                key=(rp,digest,rr.get("bytes"))
                if key in seen:continue
                seen.add(key)
                path=Path(rp)
                if not path.is_absolute():path=ROOT/path
                if not path.is_file():
                    checks.append({"record":p.relative_to(ROOT).as_posix(),"location":loc,"reference":rr,"outcome":"MISSING"})
                    continue
                actualref=ref(path)
                ok=actualref["sha256"]==digest and ("bytes" not in rr or actualref["bytes"]==rr["bytes"])
                if ok:
                    checks.append({"record":p.relative_to(ROOT).as_posix(),"location":loc,"reference":rr,"outcome":"MATCH"})
                elif rp==".github/agents/sdlc-governance-remediation.agent.md" and digest==proposal["base"]["sha256"]:
                    checks.append({"record":p.relative_to(ROOT).as_posix(),"location":loc,"reference":rr,
                       "outcome":"HISTORICAL APPROVED BASE MATCHES PRESERVED PREIMAGE","preserved":ref(preimage)})
                else:
                    historical.append({"record":p.relative_to(ROOT).as_posix(),"location":loc,"reference":rr,
                                       "current":actualref,"outcome":"REQUIRES APPLICABILITY CLASSIFICATION"})
    records=[]
    for role,aid in IDS.items():
        d=load(A/aid/"result.json")
        if role=="application":
            assert d["execution_status"]=="COMPLETED" and d["outcome"]=="EXACT APPROVED BYTES APPLIED"
        if role in ("verification","review"):
            assert d["execution_status"]=="COMPLETED" and d["outcome"]=="PASS"
        for f in ["attempt.json","report.md","result.json"]:
            records.append(dict(ref(A/aid/f),stage=role,record_identity=d.get("record_id",aid+":"+f)))
    v=load(A/IDS["verification"]/"result.json")
    rv=load(A/IDS["review"]/"result.json")
    assert len(v["criteria"])==14 and all(c["outcome"]=="PASS" for c in v["criteria"])
    assert len(rv["review"]["criteria"])==8 and all(c["outcome"]=="PASS" for c in rv["review"]["criteria"])
    runtimeids=["0939dcbe-f104-454a-a8bd-62e36810ccd3","7282643f-d89b-4b2d-b082-475ffc440fce",
                "8e77a262-4464-46d1-9078-a3fefb37d387","65a71a53-2334-4a40-8a52-6378200d5f56"]
    assert len(set(runtimeids))==4
    for role in ["preparer","proposed_one_time_applier","planned_verifier_identity_only","planned_reviewer_identity_only"]:
        rr=proposal["roles"][role];assert ref(ROOT/rr["path"])==rr
    comp=compare()
    assert not comp["changed"] and not comp["added"] and not comp["removed"] and comp["directory_set_unchanged"]
    invocation=load(SCOPE/"attempt.json")
    assert comp["repository"]==invocation["repository_context"]
    data=record("executed_integrity_checks",core=[ref(p) for p in core],mechanism_sources={n:[ref(p) for p in ps] for n,ps in mechanisms.items()},
       source_inventory=sr,core_count=52,source_count=76,core_traceability=traces,references=references,
       source_duplicate_hashes=[h for h in {r["sha256"] for r in sr} if sum(r["sha256"]==h for r in sr)>1],
       input_comparison=comp,record_bindings=checks,bindings_requiring_classification=historical,
       predecessor_records=records,verification_criteria=v["criteria"],review_criteria=rv["review"]["criteria"],
       amendment={"before":ref(preimage),"after":ref(target),"replacement_exact":True,"inverse_exact":True,
          "generated_patch_exact":patch_match,"patch":ref(A/IDS["proposal"]/"attachments/proposed.patch"),
          "UTF8_no_BOM":not before.startswith(b"\xef\xbb\xbf") and not after.startswith(b"\xef\xbb\xbf"),
          "CRLF_before":before.count(b"\r\n"),"CRLF_after":after.count(b"\r\n"),
          "no_final_newline_preserved":not before.endswith(b"\n") and not after.endswith(b"\n"),
          "four_runtime_actors":runtimeids,"role_paths_hashes_match":True},
       limitations="Executed hashes/path/JSON/diff checks, not runtime product tests or a replacement for source-semantic assessment")
    print(json.dumps({"core":len(core),"sources":len(sr),"references":len(references),
      "unresolved_literal_paths":[r for r in references if r["treatment"]=="REVIEW"],
      "binding_matches":len(checks),"binding_failures":[r for r in checks if r["outcome"]=="MISSING"],
      "historical_references":historical,"patch_exact":patch_match,"comparison":comp},ensure_ascii=True,indent=2))
    print(json.dumps(publish("evidence/integrity-checks.json",data),indent=2))
    print(json.dumps(publish("checkpoint-0001.json",record("audit_checkpoint",sequence=1,
       confirmed_boundary="Invocation separately read back before substantive work; all sources read; complete catalog and first integrity/path comparison complete",
       source_scope=76,core_scope=52,input_comparison=comp,evidence=ref(SCOPE/"evidence/integrity-checks.json"),
       unfinished_work="Complete semantic finding/mechanism rationale and canonical report publication",
       blockers=[],pending_gate="No other stage authorized",source_writes=0)),indent=2))

if __name__=="__main__":
    inspect()
