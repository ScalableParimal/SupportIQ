"""Own canonical Audit assessment, evidence and publication. Never writes inputs."""
import runpy
from pathlib import Path
import json
import re
import collections

H=Path(__file__).parent
Q=runpy.run_path(str(H/"audit-checks.py"),run_name="audit_checks_import")
ROOT,SCOPE,A,ATTEMPT=(Q[k] for k in ("ROOT","SCOPE","A","ATTEMPT"))
P=Q["P"]
ref,publish,record=(P[k] for k in ("ref","publish","record"))
load,compare=Q["load"],Q["compare"]
I=load(SCOPE/"evidence/integrity-checks.json")
INV=load(SCOPE/"attempt.json")
F3="GOV-AUD-20261102-003"
F4="GOV-AUD-20261102-004"
PREFIX=SCOPE.relative_to(ROOT).as_posix()
LIMITS=[
 "Read-only conduct is procedural, not an enforced sandbox; write-capable tools and ACLs exist.",
 "Endpoint path/content and index/HEAD/branch checks cannot exclude transient writes or same-principal tampering.",
 "No exhaustive trusted OS event log, continuous observation, enforced no-edit lock or exhaustive external-writer detection is available.",
 "Human decisions are attributed actual caller-conversation evidence; authenticated original message IDs/times are not exposed and are not invented.",
 "Runtime registry/task attribution is procedural, not authenticated external actor identity; a shared session title is not a process invocation.",
 "Host UTC values are preparation/observation samples, not exact filesystem publication timestamps.",
 "No product artifacts, runtime capability of uninvoked product roles, Master adoption or target portability conclusion is assessed."
]

def quote(path,start,end):
    ls=(ROOT/path).read_text(encoding="utf-8").splitlines()
    return {"source":ref(path),"lines":[start,end],"text":"\n".join(ls[start-1:end])}

FINDINGS=[
 {"id":F3,"severity":"Medium","category":"Lifecycle Inconsistency","secondary_categories":["Unsupported Governance"],
  "title":"Requirement Update's unconditional approved-source prerequisite excludes the initial clarification path",
  "source_document":"docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md",
  "source_section":"2 Required Inputs, item 1 (line 17)",
  "related_document":"docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",
  "related_section":"14 Requirement Update Rules (lines 294-318); 17 Suggested AI Execution Flow, Phases 5-10 (lines 416 onward)",
  "issue":"The Requirement Update bundle requires an already approved source Requirement in every invocation. Requirement Analysis explicitly routes initial, Human-decided clarifications through that separate process before complete Analysis Verification and Human Requirement Approval. There is no initial-unapproved-source branch in the Update inputs or execution procedure. Approval of clarification decisions is not approval of the source Requirement.",
  "evidence":[quote("docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md",15,23),
              quote("docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md",10,16),
              quote("docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",1,14),
              quote(".github/skills/requirement-update/SKILL.md",31,50),
              quote("docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",294,318),
              quote("docs/ai/guidelines/REQUIREMENT_ANALYSIS_GUIDELINES.md",416,432),
              quote("docs/ai/sdlc/SDLC_GOVERNANCE.md",145,157),
              quote("docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",359,365)],
  "impact":"A first Requirement that needs decisions incorporated cannot satisfy both detailed routes without an unavailable prior Requirement approval or an unauthorized interpretation of 'approved'. This can block correct lifecycle execution or encourage conflating approved decisions with formal Requirement Approval. No actual product execution or gate bypass is asserted.",
  "recommended_resolution":"Through Investigation and Corrective Change Decision, reconcile the source-status prerequisites across the Update Guideline, Prompt, Request and Skill with the initial analysis/update route. Preserve immutable version identity, explicitly approved decisions, reanalysis, complete Verification and separate Human Requirement Approval. Do not waive approval or grant analysis write authority.",
  "human_decision_required":"Yes",
  "human_decision_reason":"The auditor cannot choose or amend normative lifecycle wording. Any correction requires the governed decision, exact Human Approval and authorized application route."},
 {"id":F4,"severity":"Medium","category":"Ambiguity",
  "title":"Enhancement Corrective Request does not distinguish current actor attempts from planned future assurance identities",
  "source_document":"docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md",
  "source_section":"Actor and Human Approval fields (enhancement only), line 5",
  "related_document":"docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
  "related_section":"Preconditions, line 7; corresponding Application Prompt and Request stage-boundary controls",
  "issue":"The enhancement Request instructs that preparer, applier, verifier and reviewer role hashes are 'each bound to that actor's own unique attempt record' and asks for current runtime/qualification fields without a planned-future-stage qualifier. The Application Guideline expressly permits only planned verifier/reviewer path/hash bindings before Application and forbids requiring their attempts before predecessor gates. The Request does not say whether its all-four-attempt fields are later-stage placeholders or required proposal-stage inputs. This is an unresolved stage-timing ambiguity, not proof that any actor actually started early.",
  "evidence":[quote("docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md",1,5),
              quote("docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",5,9),
              quote("docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md",1171,1175)],
  "impact":"An enhancement requester/preparer can reasonably read the template as requiring premature future actor attempts or as an impossible prerequisite. Another reader may defer those fields, but that timing is not specified. This affects the enhancement-to-Application definition relationship, not the valid finding-led GOV-AUD-20261102-002 Application or its scoped PASS assurance.",
  "recommended_resolution":"Investigate and decide explicit stage-specific fields: bind actual current preparer/applier attempts where applicable, mark future verifier/reviewer definitions planned identity-only, and require each future actor's fresh attempt/current capability only after its predecessor and fresh Human start. Obtain exact Human Approval before any template correction.",
  "human_decision_required":"Yes",
  "human_decision_reason":"Stage-specific normative template correction and any exact amendment approval belong to the governed corrective route; the Audit may not silently supply the missing interpretation."}
]

def counts():
    c={k:0 for k in ["Critical","High","Medium","Low","Ambiguities","Broken References",
                     "Missing Governance Controls","Unsupported Governance Controls"]}
    categories={"Ambiguity":"Ambiguities","Broken Reference":"Broken References",
                "Missing Governance":"Missing Governance Controls","Unsupported Governance":"Unsupported Governance Controls"}
    for f in FINDINGS:
        c[f["severity"]]+=1
        for category in {f["category"],*f.get("secondary_categories",[])}:
            if category in categories:c[categories[category]]+=1
    return c

def supplement():
    resolution=[]
    for b in I["record_bindings"]:
        if b["outcome"]=="MISSING":
            # These references explicitly live in their record owner's attempt.
            raw=b["reference"]["path"]
            assert raw in ("attempt.json","attachments/pre-review-manifest.json")
            owner=(ROOT/b["record"]).parent
            actual=ref(owner/raw)
            assert actual["sha256"]==b["reference"]["sha256"] and actual["bytes"]==b["reference"]["bytes"]
            resolution.append({"original_scanner_record":b["record"],"location":b["location"],
               "raw_attempt_relative_path":raw,"canonical":actual,"outcome":"MATCH",
               "reason":"Attempt-relative reference resolved within explicitly identified owning attempt, not repository root"})
    assert len(resolution)==2
    path_context=[]
    for r in I["references"]:
        if r["treatment"]=="REVIEW":
            if r["target"]=="scripts/tests/runtime":
                reason="Prohibition shorthand ('scripts/tests/runtime'), not a required file or directory reference."
            elif r["target"]=="docs/sdlc-records/product/":
                reason="Prospectively adopted product-root contract; currently absent/unadopted and no product process invoked. Its present creation is not required."
            else:raise AssertionError(r)
            path_context.append(dict(r,final_treatment=reason,broken_reference=False))
    sources=I["source_inventory"];names=collections.defaultdict(list)
    for s in sources:names[Path(s["path"]).name].append(s["path"])
    bare=[]
    for s in sources:
        text=(ROOT/s["path"]).read_text(encoding="utf-8")
        for n,line in enumerate(text.splitlines(),1):
            for name in re.findall(r"(?<![A-Za-z0-9_/\\-])([A-Z][A-Z0-9_]+\.md)",line):
                if re.fullmatch(r"V\d+\.md",name):
                    bare.append({"source":s["path"],"line":n,"filename":name,
                                 "treatment":"PRODUCT VERSION EXAMPLE; no content inspected or existence required"})
                    continue
                matches=names.get(name,[])
                assert len(matches)==1,(s["path"],n,name,matches)
                bare.append({"source":s["path"],"line":n,"filename":name,"resolved":matches[0]})
    headers=[]
    for s in I["core"]:
        if s["path"].startswith(".github/"):
            t=(ROOT/s["path"]).read_text(encoding="utf-8");assert t.startswith("---\n")
            front=t.split("---",2)[1]
            assert re.search(r"(?m)^name:\s*\S",front) and re.search(r"(?m)^description:\s*\S",front)
            headers.append({"source":s,"frontmatter":"name and description present; identity/purpose manually assessed against designated process"})
    assert len(headers)==19
    histids=[
      "20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55",
      "20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694",
      "20261030T161112Z-9c79d789-1b9a-479c-a9e7-6e692747330f",
      "20261031T043137Z-7d2b35df-98a6-4d50-8761-48fe0f724e0f",
      "20261031T072633Z-4c6c7de5-037e-49d1-a594-97b7ef0c5319",
      "20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0",
      "20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37",
      "20261102T075750Z-1210d4b1-8300-4b17-8f6b-911a2f64958e",
      "20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd",
      "20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1",
      "20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb",
      "20261102T102710Z-08b5280b-b77a-4b15-80a5-5f62de0357ff",
      "20261102T112012Z-8c073220-022a-4a9f-84fd-20968bcaa186",
      "20261102T1130Z-81995642-42b8-42c4-94e3-4b6d994c10bc"]
    historical=[]
    for aid in histids:
        p=A/aid/"result.json";d=load(p)
        bindings=[]
        for loc,r in Q["nodes"](d):
            rp=r["path"].replace("\\","/")
            if rp.startswith("docs/sdlc-records/governance/") and re.fullmatch("[0-9a-fA-F]{64}",r["sha256"]):
                actual=ref(rp)
                assert actual["sha256"]==r["sha256"].upper()
                if "bytes" in r:assert actual["bytes"]==r["bytes"]
                bindings.append({"location":loc,"resolved":actual})
        # Preserve native status fields, never coerce heterogeneous historical schemas.
        historical.append({"attempt":aid,"report":ref(A/aid/"report.md"),"result":ref(p),
          "status_fields":{k:v for k,v in d.items() if k in
            ["outcome","execution_status","execution_termination","executionTermination","termination",
             "application_outcome","remediation_status","cycle_admitted","cycle_basis","cycle_subjects",
             "human_scope_decision_ref","findingOutcomes","planChangeRequired","finding_outcomes","finding_confirmed",
             "investigation_outcome","source_or_prior_record_modified"]},
          "immutable_record_bindings_verified":bindings})
    initialv=load(A/histids[2]/"result.json")
    ptargets=[]
    for target in initialv["P1_P5_targets"]:
        actual=ref(target["path"])
        assert actual["sha256"]==target["expected_after_sha256"] and actual["bytes"]==target["current_bytes"]
        ptargets.append(actual)
    v=load(A/Q["IDS"]["verification"]/"checkpoint-0004.json")
    rv=load(A/Q["IDS"]["review"]/"checkpoint-0004.json")
    assert v["outcome"]=="PASS" and rv["outcome"]=="PASS"
    # Validate canonical report table byte/hash triples, not only JSON references.
    tablechecks=[]
    for role,aid in Q["IDS"].items():
        path=A/aid/"report.md";text=path.read_text(encoding="utf-8")
        for line in text.splitlines():
            match=re.match(r"\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([A-Fa-f0-9]{64})`\s*\|",line)
            if match:
                rp,num,sha=match.groups()
                if not rp.startswith(("docs/",".github/")):continue
                actual=ref(rp)
                if actual["sha256"]!=sha.upper():
                    # Proposal/Application excluded active Remediation identity is the approved historical preimage.
                    assert rp==".github/agents/sdlc-governance-remediation.agent.md"
                    actual=ref(A/Q["IDS"]["application"]/"attachments/target-before.bin")
                assert actual["bytes"]==int(num) and actual["sha256"]==sha.upper()
                tablechecks.append({"report":path.relative_to(ROOT).as_posix(),"path":rp,"bytes":int(num),"sha256":sha.upper(),"outcome":"MATCH"})
    return {"attempt_relative_resolution":resolution,"literal_path_context":path_context,"bare_filename_references":bare,
       "core_skill_agent_frontmatter":headers,"historical_records":historical,"initial_five_after_states":ptargets,
       "verification_final_readback":ref(A/Q["IDS"]["verification"]/"checkpoint-0004.json"),
       "review_final_readback":ref(A/Q["IDS"]["review"]/"checkpoint-0004.json"),
       "report_table_bindings":tablechecks,"binding_failures_after_resolution":[],
       "notes":[
        "Raw scanner's two MISSING labels are root-only resolution limitations, resolved here under their explicit owning attempts; no evidence or schema default substituted.",
        "Proposal 'including final newline' narrative is imprecise; exact machine base/after/patch and final-newline-unchanged bindings independently resolve the actual approved absence.",
        "Review report prepends 'Yes, ' to the fresh start while attempt/result and actual supplied Human instruction preserve 'Initiate one fresh ...'. Narrative prefix is not used as authority. Exact decision evidence agrees in identity, scope, retry and exclusions; no conflicting decision or unauthorized stage is established. This nonmaterial transcription observation does not substitute for any gate.",
        "Historical failed Review and unpublished Audit preparation are not successful stages, source defects or evidence of live competing writers.",
        "Earlier GOV-001/GOV-002 and addressed GOV-AUD-20261102-001 are retained as previously disposed. No new current basis to reopen them."
       ]}

RATIONALES={
 "requirement-analysis":"Read-only initial analysis, explicit Human clarification decisions, separate Requirement Update, reanalysis and complete Analysis Verification before formal Requirement Approval; no planning/implementation. Its locally correct initial-update relationship exposes F003 in the Update bundle.",
 "requirement-analysis-verification":"Complete current analysis and resulting Requirement compared with authoritative source and approved decisions; verification read-only, findings resolved/reverified, Human Approval separate; no task-only scope.",
 "implementation-planning":"Current approved Requirement and repository/architecture evidence; creates candidate Plan, risk/verification/task traceability, no silent business change or implementation; Plan Verification and distinct review/plan Human gates follow.",
 "requirement-update":"Immutable new Requirement version from explicitly approved decisions, prior bytes preserved and separate downstream analysis/verification/approval; unconditional approved-source prerequisite conflicts with initial-update route (F003).",
 "implementation-plan-verification":"Complete candidate current Plan, not merely changed tasks, against current approved Requirement and actual evidence; read-only; findings route corrective controls, distinct Human Review Approval then Plan Approval.",
 "implementation":"Only approved Requirement/Plan authority; task IDs context, repository validation and complete self-check; no upstream edits or direct deviation-to-code; independent Verification/Review/Acceptance and separate Commit/Push gates.",
 "implementation-verification":"Complete current implementation against current approved Requirement/Plan; actual available test/build evidence, no invented execution, no direct fixes; PASS is not Human Acceptance or approval.",
 "implementation-review":"Independent read-only review of complete current implementation, Verification and evidence; risks/findings explicit, Human Acceptance separate, no source corrections or Commit/Push authority.",
 "finding-investigation":"Findings/provenance/evidence contextualized without correction, acceptance or implementation; governance enhancement remains non-finding, independent source observations, corrective handoff and product exclusion honored.",
 "corrective-change-decision":"Artifact-specific accept/reject/defer/no-plan-change decisions and recommendation/plan route, not execution; exact governance proposals and separate approval/application/assurance remain gated. Enhancement Request actor-timing field is ambiguous (F004)."
}

CHECK_LABELS={
 "guideline":["Master alignment","lifecycle","authority","read/write boundary","Human Approval","verification","change control","scope","status","outputs","downstream","terminology","paths","unsupported rules","material controls"],
 "prompt":["correct Guideline","Guideline exists","Guideline conformance","terminology","source truth","Human Approval","read-only boundary","modification authority","verification preserved","approval preserved","no direct correction","findings/deviations","report","unsupported rules","material controls"],
 "request":["correct Prompt","Prompt exists","required inputs","placeholders/terminology","artifact names","Requirement references","Plan references","task context","complete scope","evidence","Human decisions","paths","case/naming","obsolete references","Prompt consistency"],
 "skill":["exists","frontmatter identity/purpose","Guideline link","Master authority","procedure","no override","Prompt relationship","Request relationship","process boundary","write boundary","Human Approval","verification/review","corrective boundary","handoff","unsupported rules","material controls","terminology","paths"],
 "agent":["exists","frontmatter identity/purpose","correct Skill","Skill exists","process identity","no policy duplication","authority","write boundary","read-only boundary","Human Approval","Human Acceptance","verification","corrective boundary","no bypass","no unauthorized authority","no AI approval","upstream nonmutation","paths"]
}

def coverage():
    rows=[]
    for r in I["core"]:
        path=r["path"];slug=None;kind="master";affected=[]
        for stem,s in zip(Q["STEMS"],Q["SLUGS"]):
            if path==f"docs/ai/guidelines/{stem}_GUIDELINES.md":kind="guideline";slug=s
            if path==f"docs/ai/prompts/{stem}_PROMPT.md":kind="prompt";slug=s
            if path==f"docs/ai/request/{stem}_REQUEST.md":kind="request";slug=s
            if path==f".github/skills/{s}/SKILL.md":kind="skill";slug=s
            if path==f".github/agents/{s}.agent.md":kind="agent";slug=s
        if slug=="requirement-update":affected=[F3]
        if path=="docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md":affected=[F4]
        exceptionchecks=[]
        if affected==[F3]:
            exceptionchecks={"guideline":[1,2,11,14],"prompt":[14],"request":[],"skill":[15]}[kind]
        if affected==[F4]:exceptionchecks=[3,10,15]
        if kind=="master":
            rationale={
             "SDLC_GOVERNANCE.md":"Defines Human/AI authority, source Requirement to approval lifecycle, separate Plan gates, complete verification, corrective routing and adoption/effectiveness. No inter-Master contradiction found.",
             "SDLC_ARTIFACT_GOVERNANCE.md":"Defines 52-core catalog, ten Skills/nine Agents (Requirement Update Skill-only), artifact status/rights/immutability, distinct assurance actors and current-invocation publication. No new authority inferred from tool access.",
             "SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md":"Defines evidence links, artifact-specific changes, durable attempts/publication/recovery, governance-root bootstrap, prospective adoption and optional centralized framework consumption. Existing governance-root authority retained; candidate baseline/product root not adopted."
            }[Path(path).name]
            checks=[{"id":n,"check":label,"outcome":"PASS"} for n,label in enumerate(
              ["authority","lifecycle","artifact rights/status","Human gates","change propagation","traceability","persistence","Master-to-Master consistency"],1)]
        else:
            rationale=RATIONALES[slug]
            checks=[{"id":n,"check":label,"outcome":"FINDING" if n in exceptionchecks else "PASS"}
                    for n,label in enumerate(CHECK_LABELS[kind],1)]
            if affected==[F3] and kind=="request":
                checks.append({"id":"S01","check":"Cross-document initial lifecycle source-status compatibility",
                               "outcome":"FINDING"})
        rows.append({"source":r,"kind":kind,"process":slug,"assessed":True,"result":"FINDINGS" if affected else "PASS",
                     "finding_ids":affected,"rationale":rationale,"checks":checks})
    assert len(rows)==52
    return rows

def ck(id,outcome,basis):
    return {"id":id,"outcome":outcome,"basis":basis}

def mechanisms(evidenceref):
    ids=Q["IDS"]
    def stage(role):
        aid=ids[role]
        return [ref(A/aid/"attempt.json"),ref(A/aid/"report.md"),ref(A/aid/"result.json")]
    groups=[]
    def add(name,result,checks,records,applicability):
        src=I["mechanism_sources"][name]
        groups.append({"group":name,"expected":1,"present":1,"assessed":1,"source_expected":len(src),
          "source_present":len(src),"source_assessed":len(src),"result":result,
          "sources":src,"common_authority":[r for r in I["core"] if r["path"].startswith("docs/ai/sdlc/")],
          "evidence":records,"applicability":applicability,"checks":checks})
    add("Governance Audit","PASS",[
      ck("A01","PASS","52 expected/found/assessed; 76 actual source files classified, not a count proxy; all seven groups separately assessed."),
      ck("A02","PASS","Exact CONSISTENT/all-eight-zero/all-seven-resolved rule; this INCONSISTENT outcome does not qualify."),
      ck("A03","PASS","Current invocation/manifest first publication and separate readback before assessment; procedural nonmutation and endpoints disclosed."),
      ck("A04","PASS","Complete canonical report and evidence precede result; result binds actual hashes. Report/result paths and stable identities are forward-bound without circular self/future digest."),
      ck("A05","PASS","Audit owns output only, not remediation/adoption/approval or product execution. Subsequent Remediation terminal-anchor validation remains a later authorized actor responsibility.")
    ],[ref(SCOPE/"attempt.json"),ref(SCOPE/"evidence/input-manifest.json"),evidenceref],
       "Current Audit invoked; report/result identities resolved by terminal result publication. A04 is validated as a completion invariant before terminal result.")
    add("Governance Remediation","PASS",[
      ck("M01","PASS","Finding-led scope, separate stages/fresh Human starts and actual prospective cycle admission maintained; non-finding enhancement not invented as a finding."),
      ck("M02","PASS","Current coordinator binds prior complete Audit and Investigation; proposal/approval/Application/Verification/Review separately owned. Earlier no-plan-change historical dispositions retained."),
      ck("M03","PASS","Active Remediation self-edit barred; designated distinct one-time applier applied only approved bytes, independent verifier/reviewer followed."),
      ck("M04","PASS","Approved item-2 correction preserves original authorization immutable and uses new linked own-action evidence, exact commit/diff/list/conditions; no Push expansion or self-containing commit requirement."),
      ck("M05","PASS","No product scope, approval, adoption or automatic downstream authority. Pending future final Remediation report is not an Audit prerequisite; it must later independently hash Audit result/report.")
    ],stage("coordinator")+stage("proposal")+stage("application")+stage("verification")+stage("review"),
       "Existing finding-led prospective Cycle 1 invoked and paused between separately Human-started stages; current final handoff not yet authorized or published.")
    add("SDLC Process Orchestration","FAIL",[
      ck("O01","PASS","Artifact 4.4 and O6.1/O6.6/O9 require fresh attributable Human initiation at each start/retry/transition; initiation not formal approval."),
      ck("O02","PASS","Product-scoped coordinator, no governance amendment coordination, self-approval or direct finding-to-code; own durable state only, safe recovery and serialized shared-checkout writes."),
      ck("O03","FAIL","Initial clarification transition dispatches Requirement Update, whose approved-source-only inputs cannot implement the pre-first-approval route (F003). No unstated exception is supplied."),
      ck("O04","NOT APPLICABLE","No product Orchestrator actually invoked. Session title/role registry is not stage proof; no attempt/start records or runtime capabilities inferred.")
    ],[evidenceref],"Definition assessed; product runtime records/capability NOT APPLICABLE, not a runtime PASS.")
    add("SDLC Portability Assessment","PASS",[
      ck("P01","PASS","All five links resolve under same Masters; advisory-only target-specific recommendation, not adoption/readiness approval."),
      ck("P02","PASS","Entry before target execution and reassessment on relevant changes; source framework evidence separated from target observations."),
      ck("P03","PASS","Explicit blocker Human decisions; concerns routed by kind; governance-defect candidates routed to governed audit/investigation, not direct fixes."),
      ck("P04","PASS","Own persistence/context, no auto Agent invocation, target writes, source modification or product-repository content inspection during this Audit."),
      ck("P05","NOT APPLICABLE","No target-project Portability Assessment invoked; no target content inspected or runtime capability inferred.")
    ],[evidenceref],"All five definitions assessed; target assessment invocation/report/result and runtime capability NOT APPLICABLE.")
    add("Governance Amendment Application","FAIL",[
      ck("G01","PASS","Current finding-led Application execution_status COMPLETED and outcome EXACT APPROVED BYTES APPLIED; no invalid generic PASS assertion."),
      ck("G02","PASS","Exact actual Human approval/designation and separate start bind report/proposal/patch, target path/base/after/scope/roles/exclusions; fresh one-time authority only."),
      ck("G03","PASS","Four distinct actor definitions/attempts/runtime identities; applier separate from active Remediation and Orchestrator; current qualification and all-base prewrite checks precede source write."),
      ck("G04","PASS","Fresh exact replacement and inverse plus generated 4115-byte LF patch match; before 48379/current 49225, UTF8 no BOM/1363 CRLF/no EOF newline preserved, one approved source changed."),
      ck("G05","PASS","Application baseline/366 others and index/HEAD/branch preservation evidenced by independent Verification; current 413-file bounded baseline unchanged. Actor-owned immutable evidence and separate final readbacks resolve."),
      ck("G06","FAIL","Enhancement proposal Request's all-four-own-attempt wording is not stage-qualified against Application planned-only future assurance control (F004). Current finding-led applied bytes and assurance remain valid; definition relationship unresolved.")
    ],stage("proposal")+stage("application")+[ref(A/ids["application"]/"attachments/evidence.json"),
       ref(A/ids["application"]/"attachments/application.json"),ref(A/ids["application"]/"checkpoint-0002.json"),evidenceref],
       "Current applied finding correction stage-specific checks PASS. Group FAIL is a separate enhancement-definition timing ambiguity, not a reclassification of the completed Application.")
    add("Independent Governance Verification","PASS",[
      ck("V01","PASS","Fresh Verification start after successful Application; actual verifier identity differs from preparer/applier/reviewer and matches approved planned definition."),
      ck("V02","PASS","14 V01-V14 PASS criteria with independent reads/hashes/exact replacement/inverse/patch/encoding/change-set and cross-document evidence."),
      ck("V03","PASS","Current invocation/permissions/capability and own immutable outputs/read-only source conduct established; no role-name-only or historical-capability substitution."),
      ck("V04","PASS","Exact approved one-path change complete; record/report hashes resolve; checkpoint-0004 independent separate terminal readback PASS. No substitute full Audit, effectiveness or adoption.")
    ],stage("verification")+[ref(A/ids["verification"]/"attachments/evidence.json"),ref(A/ids["verification"]/"checkpoint-0004.json")],
       "Invoked scoped amendment Verification PASS; its 14 actual criteria retained in evidence, not re-performed as another process.")
    add("Independent Governance Review","PASS",[
      ck("R01","PASS","Fresh Review retry after Verification PASS; four distinct runtime actors and definition hashes match approved identities; failed predecessors remain unsuccessful historical attempts."),
      ck("R02","PASS","Eight R01-R08 criteria PASS for approved intent/exact scope, immutable authorization route, Human gates, authority, catalog/cross-document/effectiveness boundaries."),
      ck("R03","PASS","Hidden-inclusive manifest404/117/31.github, qualified invocation before assessment, own atomic partial publication and checkpoint-0004 separate final readback resolve."),
      ck("R04","PASS","Source read-only procedural assurance and endpoint limits disclosed. Exact machine/caller decision evidence resolves narrative imprecisions; no authority or approved-byte ambiguity established. No Audit, adoption or effectiveness substitute.")
    ],stage("review")+[ref(A/ids["review"]/"attachments/review-evidence.json"),ref(A/ids["review"]/"checkpoint-0004.json")],
       "Latest distinct scoped Review PASS assessed, not silently replacing failed Review attempts or claiming global framework consistency.")
    assert len(groups)==7
    return groups

def table(headers,rows):
    def cell(x):return str(x).replace("|","\\|").replace("\n"," ")
    return "\n".join(["| "+" | ".join(headers)+" |","| "+" | ".join("---" for _ in headers)+" |"]+
                     ["| "+" | ".join(cell(x) for x in row)+" |" for row in rows])+"\n"

def report(evidence,rows,groups,sup,comparison):
    out=["# SDLC Governance Consistency Audit\n"]
    def add(s):out.append(s+"\n")
    add("**Execution: COMPLETED. Overall result: INCONSISTENT.** This is an AI Governance Audit only, not Human Approval, Human Acceptance, effectiveness or adoption.")
    add(table(["Core expected","Core found","Core audited","Actual governance sources","Mechanism groups expected/present/assessed"],[[52,52,52,76,"7 / 7 / 7"]]))
    add(table(list(counts()),[list(counts().values())]))
    add("There are **two unique findings**, both Medium. The Ambiguities counter describes F004; Unsupported Governance Controls describes F003's unsupported universal approved-source prerequisite (a secondary category of its lifecycle inconsistency). Category counters overlap severity counters and do not create extra findings. No separate missing-control finding is asserted.")
    add("## Audit Scope")
    add(f"Work ID `0061148a-1b62-4d25-adff-e7f2318dbfad`; cycle `GOV-REMEDIATION-PROSPECTIVE-001`, Cycle 1. Attempt `{ATTEMPT}`. Canonical report identity `{ATTEMPT}:audit_report`; terminal result identity `{ATTEMPT}:audit_result`.")
    add(f"Canonical report `{PREFIX}/report.md`; terminal result `{PREFIX}/result.json`. These are stable identities/paths, not self/future digests. The result is published after this report/evidence and binds their actual final hashes; a new checkpoint records separate-process final readback.")
    add("Repository `ScalableParimal/SupportIQ`, root `C:\\PARIMAL_SHERE\\SCALABLE_SOLUTIONS\\SupportIQ`; HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`; branch `sdlc-framework-onboarding`; origin `https://github.com/ScalableParimal/SupportIQ.git`.")
    add("Fresh actual Human start, verbatim:\n\n> Yes, initiate a fresh complete Governance Audit retry with corrected process-specific preflight validation; no other stage")
    add("This is the authorized fresh retry, not a completion claim for preserved preparation `20261102T115616Z-ab050be4-c4db-46ae-a5eb-a9fcf9bb41cb`. That preparation failed an incorrect generic outcome assertion before invocation publication or substantive audit. Its helper/selftest remain unchanged. Current retry validates actual process-specific status schemas without fallback/coercion.")
    add("The adopted governance-root authorization was independently live-resolved from OWNER ScalableParimal's issue-3 comment `https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236`, created/updated 2026-10-30T12:31:51Z. Ordinary established-root continuation applies. It is not a new bootstrap, reuse of its old Audit start, prospective Master adoption or product-root adoption. Three Masters remain candidate/unadopted bootstrap comparison authority under Governance §3; product root remains unadopted.")
    add("Current qualification: actual read/hash/Git/native JSON/publication capability, Windows principal `int-scl-010\\parimal`, attempts-root ACL/access observations and exact permitted output scope are recorded in attempt.json. Current actor is a dedicated Audit invocation, not the product Orchestrator despite session-title metadata. Its own observed running Audit identity is not counted as a competing writer; old terminal/start metadata is not liveness evidence. No conflicting live writer observed in available registry/recovery evidence. Shared writable principal/tool access does not enlarge authority.")
    add("Persistence order: corrected native-object publisher selftest; hidden-inclusive manifest; validated/flushed .partial and Windows atomic no-overwrite invocation publication; **fresh separate-process invocation/manifest/predecessor/index readback before substantive assessment**, observed at 2026-11-02T12:00:03.614745+00:00 (not publication time). Masters then read in full, mechanism definitions inspected before detailed comparison, all Guidelines → Prompts → Requests → Skills → Agents read, paths/matrix and current/historical evidence assessed. Checkpoint-0001 follows full catalog/integrity work; checkpoint-0002 precedes canonical evidence/report. Final result cannot precede report/evidence.")
    add("Only this exact attempt's own output subtree is excluded from evaluated input comparisons. Hidden-inclusive os.walk enumerated **413 governance/source/record files, 120 directories and 31 .github files**, including all 76 sources, current roles and relied upstream/failed preparation records. No .git-content scan or product-content audit was performed; index is separately hashed. Product path/size exclusions are inventory metadata only.")
    add(table(["Own preassessment record","Bytes","SHA-256"],[[r["path"],r["bytes"],r["sha256"]] for r in
        [ref(SCOPE/"attempt.json"),ref(SCOPE/"evidence/input-manifest.json"),ref(SCOPE/"evidence/publisher-selftest.json"),ref(SCOPE/"checkpoint-0001.json")]]))
    add("### Complete expected core catalog and per-artifact disposition")
    add("The tables below list every expected artifact, not a count proxy. Class totals are 3 Masters + 10 Guidelines + 10 Prompts + 10 Requests + 10 Skills + 9 Agents = 52. All exist, were opened and assessed. The remaining 24 actual source files are the seven groups' separate definitions, listed below. No unresolved additional source or duplicate governance-content file was found. Evidence contains every per-artifact numbered criterion; local summaries do not waive those criteria.")
    add(table(["Masters (3)","Bytes","SHA-256","Assessment"],[[r["source"]["path"],r["source"]["bytes"],r["source"]["sha256"],r["rationale"]] for r in rows if r["kind"]=="master"]))
    add("Product Requirements, analyses, Plans, source, tests, configuration, migrations, product documentation and product Approval/Acceptance content are excluded permanently. No product finding, runtime execution, target-project assessment or target portability conclusion is inferred from paths. Governance record contents are inspected only as required mechanism evidence.")
    add("## Separately Reported Mechanism Alignment")
    add("Same framework and three common Masters; these seven groups are outside the 52-core denominator. Definition source totals exclude the three shared Masters: 2+1+1+5+5+5+5=24. Runtime NOT APPLICABLE does not mean capability established or a stage passed.")
    add(table(["Group","Groups expected/present/assessed","Sources expected/present/assessed","Result"],[
       [g["group"],"1 / 1 / 1",f'{g["source_expected"]} / {g["source_present"]} / {g["source_assessed"]}',g["result"]] for g in groups]))
    for g in groups:
        add("### "+g["group"]+" — "+g["result"])
        add(g["applicability"])
        add(table(["Source path","Bytes","SHA-256"],[[s["path"],s["bytes"],s["sha256"]] for s in g["sources"]]))
        add(table(["Check","Outcome","Evidence-based rationale"],[[c["id"],c["outcome"],c["basis"]] for c in g["checks"]]))
        if g["group"]=="Governance Audit":
            add(f"Own evidence `{evidence['path']}`, record identity `{ATTEMPT}:audit_evidence`, {evidence['bytes']} bytes, SHA-256 `{evidence['sha256']}`. Current report/result stable identities and subsequent result binding are described in Audit Scope; no circular self/future fingerprint.")
        add(table(["Required evidence path","Bytes","SHA-256"],[[e["path"],e["bytes"],e["sha256"]] for e in g["evidence"]]))
    add("### Current approved amendment and predecessor assessment")
    add("Application is COMPLETED / EXACT APPROVED BYTES APPLIED (not outcome PASS). Verification and Review are COMPLETED / PASS. Four distinct runtime attributions: preparer `0939dcbe-f104-454a-a8bd-62e36810ccd3`, applier `7282643f-d89b-4b2d-b082-475ffc440fce`, verifier `8e77a262-4464-46d1-9078-a3fefb37d387`, reviewer `65a71a53-2334-4a40-8a52-6378200d5f56`. Each uses its own attempt and current qualification; approved planned future identities were not claimed as then-current future capability. No externally authenticated principal claim is made.")
    add("Actual combined approval/designation supplied by the Human and recorded in Application, verbatim:\n\n> I approve the identified exact report/proposal/patch and section 8 route with all target, role, scope and assurance bindings above; freshly designate the proposed one-time applier; do not start Application")
    add("Separate Application start:\n\n> Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-002 under the approved exact package")
    add("Separate Verification start:\n\n> Yes, initiate Independent Governance Verification for the GOV-AUD-20261102-002 amendment Application only")
    add("Latest actual Review retry start, from caller and exact attempt/result binding (not the imprecise report prefix):\n\n> Initiate one fresh Independent Governance Review retry with the corrected manifest and atomic publication prerequisites; no other stage")
    add("Proposal section 8 and its machine package bind exact report/proposal/patch fingerprints, roles, one-time route, one target base/after, encoding/scope/exclusions and separate assurance. No residual-risk acknowledgement gate is added. Current source change to 49,225 bytes / `404AF9126BC310AEA79BA7616AB8E25C0AD5EE7F48B360F1AF515EA4DC9F942F` is authorized drift, not an unauthorized baseline mismatch. Audit independently reconstructs it from 48,379-byte `EBFE9E9A369F2FA367F7A4728893106338DBDB6245A2016E2A248E7228148153` preimage: one exact byte replacement, inverse and regenerated patch all match; 1,363 CRLF delimiters/no BOM/no final newline preserved. Application's independent Verification records one approved source change and 366 other baseline files unchanged; current manifest endpoints independently match all 413 current files.")
    add("Verification V01–V14 and Review R01–R08 actual criteria are all PASS and integrity-bound. Separate terminal checkpoints are rehashed. These are scoped assurance for the exact amendment; they never claimed complete-framework consistency and do not suppress new full-Audit findings.")
    add("Previously reported GOV-AUD-20261102-002 is **addressed on its actual current source basis**: authorization remains immutable, later own-action evidence links original path/ID/hash and exact authorized staged content, retains conditions and does not expand Push. No commit/push occurred. The new F003/F004 findings concern different current text, not reopening the old finding.")
    add("Prior GOV-AUD-20261102-001 is addressed by the approved 3,438-byte linked clarification (`8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA`) and its separate PASS Verification/Review. Historical GOV-001/GOV-002 remain admitted/disposed under the explicit prospective cycle and NO PLAN CHANGE REQUIRED decision. Initial five corrected sources match their recorded approved after hashes. Originals, failed Reviews and old incomplete attempts remain unchanged; no retroactive reclassification or new historical authentication is made.")
    add(table(["Historical/current record","Bytes","SHA-256"],[[x[k]["path"],x[k]["bytes"],x[k]["sha256"]] for x in sup["historical_records"] for k in ("report","result")]))
    add("## Repository Reference Findings")
    add("**None: Broken References = 0.** All exact core/mechanism paths and expected Skill→Guideline/Prompt/Request, Agent→Skill, Prompt→Guideline and Request→Prompt relationships resolve. 321 explicit path occurrences and all recognized bare governance filenames were checked; per-occurrence results are in evidence. Directory casing/names agree. No file was silently moved, renamed or corrected.")
    add("Absent ApprovalAlarm guide/script references are conditional integration with explicit skip behavior, not mandatory missing sources. 'scripts/tests/runtime' in Portability Prompt is a prohibition shorthand, not a required path. Unadopted `docs/sdlc-records/product/` is a prospective product-root contract, not an Audit creation prerequisite. Product example paths and placeholders were assessed only as definitions. Two attempt-relative Review checkpoint links initially labeled MISSING by a root-only scanner resolve exactly within their owning attempt; supplementary canonical resolutions preserve the raw scan and demonstrate matching bytes/hash. No fallback status or unresolved evidence failure remains.")
    add("## Governance Consistency Findings")
    for f in FINDINGS:
        add("### Finding ID — "+f["id"]+"\n\n**"+f["title"]+"**")
        for label,key in [("Severity","severity"),("Category","category"),("Source Document","source_document"),("Source Section","source_section"),("Related Document","related_document"),("Related Section","related_section"),("Issue","issue")]:
            add("**"+label+":** "+f[key])
        if f.get("secondary_categories"):add("**Secondary Category:** "+", ".join(f["secondary_categories"]))
        add("**Evidence:**")
        for e in f["evidence"]:
            add(f"- `{e['source']['path']}`, lines {e['lines'][0]}–{e['lines'][1]}, SHA-256 `{e['source']['sha256']}`:\n\n"+ "\n".join("> "+line for line in e["text"].splitlines()))
        for label,key in [("Impact","impact"),("Recommended Resolution","recommended_resolution"),("Human Decision Required","human_decision_required")]:
            add("**"+label+":** "+f[key])
        add(f["human_decision_reason"])
    for kind,title in [("guideline","Guideline Consistency Summary"),("prompt","Prompt Consistency Summary"),
       ("request","Request Template Consistency Summary"),("skill","SDLC Process Skill Consistency Summary"),
       ("agent","SDLC Process Agent Consistency Summary")]:
        add("## "+title)
        add(f"All {sum(r['kind']==kind for r in rows)} inspected; every applicable Skill §{ {'guideline':9,'prompt':10,'request':11,'skill':12,'agent':13}[kind]} criterion is separately indexed in audit-evidence.json. 'PASS except' is not a waived check: listed failed criteria remain findings.")
        add(table(["Exact expected artifact","Bytes","SHA-256","Result / rationale"],[
           [r["source"]["path"],r["source"]["bytes"],r["source"]["sha256"],
            r["result"]+(" ("+", ".join(r["finding_ids"])+")" if r["finding_ids"] else "")+" — "+r["rationale"]]
             for r in rows if r["kind"]==kind]))
    add("## Skill and Agent Traceability Summary")
    add(table(["Process","Guideline","Prompt","Request","Skill","Agent","Traceability"],[
        [t["process"],t["guideline"],t["prompt"],t["request"],t["skill"],t["agent"] or "NOT APPLICABLE — Master-designated Skill-only",
         t["link_resolution"]+("; semantic exception "+", ".join(t["semantic_exceptions"]) if t["semantic_exceptions"] else "")]
         for t in I["core_traceability"]]))
    add("All ten Skills have correct name/purpose frontmatter and governed bundle links; all nine Agents have name/purpose, designated Skill and bounded entry-point authority. No missing Requirement Update Agent finding: it is expressly Skill-only in Artifact §4. No Agent bypass, self-approval, direct corrective implementation or unauthorized upstream mutation authority found. F003 is faithfully repeated across the Update bundle, so matching links alone do not establish semantic consistency; F004 is a Request timing exception, not missing role definitions.")
    add("## Cross-Document Consistency Summary")
    themes=[
      ("Master consistency","PASS","No contradiction between the three comparison Masters found; target baseline is not adopted by this Audit."),
      ("Requirement lifecycle","FINDING "+F3,"Source→analysis→approved decisions→immutable updated Requirement→analysis refresh→complete Verification→resolve decisions→formal Human Approval. Update inputs prematurely demand approved source."),
      ("Planning lifecycle","PASS","Approved Requirement→candidate Plan→complete Plan Verification→resolve findings→Human Review Approval→separate Plan Approval; review approval only permits progression to plan approval."),
      ("Implementation lifecycle","PASS","Approved Requirement/Plan→implementation→self-check→independent complete Verification→Review→Human Acceptance→separate authorized Commit/Push."),
      ("Artifact identity/status/supersession","PASS","Immutable Requirement versions and records; current approved comparators distinct from candidates; Verified/Approved/Accepted not interchangeable; supersession recorded without destructive overwrite."),
      ("Findings and corrective change","PASS except "+F4,"Investigation→artifact-specific decision→required exact Human Approval→authorized apply→required Verification/Review. No direct finding-to-code. Accepted no-plan-change disposition preserved. Enhancement Request future-attempt timing ambiguous."),
      ("Human authority","PASS","Initiation, formal approval, acceptance, adoption and Commit/Push are separate; AI cannot confer them or infer missing/stale/NO as YES."),
      ("Complete scope and task IDs","PASS","Task IDs/context/change locations do not narrow complete Requirement Analysis Verification, Plan Verification, implementation Verification/Review where required."),
      ("Read/write boundaries","PASS","Read-only verification/review/investigation remain nonmutating; implementations/updates limited to approved artifact-specific scope; Audit owns output only."),
      ("Evidence classification/outputs","PASS except "+F4,"Executed vs unexecuted evidence distinguished, missing capability blocks applicable stages, native records/fingerprints and reports preserved. No future actor capability inferred; Request timing needs explicit qualifier."),
      ("Upstream material propagation","PASS","Requirement changes trigger reanalysis/Verification/Human Approval/Plan impact and downstream reapproval; Plan changes reverify/reapprove and invalidate stale implementation authority."),
      ("Terminology/path relationships","PASS","Requirement vs Approved Requirement, Plan vs Approved Plan, Human Review vs Plan Approval and Acceptance retained; F003 concerns premature approval state, not harmless capitalization."),
      ("Persistence/recovery/central consumption","PASS","Actor-owned attempts, approved roots, safe partial/no-overwrite publication, durable reports/results and fresh retries preserved; optional central consumption remains conditional, not activated.")
    ]
    add(table(["Theme","Assessment","Rationale"],themes))
    add("The two issues are current textual comparisons, not inferred from product state or an exhaustive historical re-audit. Severity Medium reflects meaningful execution ambiguity/blockage without a demonstrated bypass of a major Human/verification gate. F004 is expressly Ambiguity because the Request could be read as later population; the auditor does not silently choose that interpretation or assert actual premature invocation.")
    add("## Governance Gaps")
    add("Missing Governance Controls = 0. No distinct absent control finding. The initial-source lifecycle and future-attempt timing issues are captured once as F003/F004, not multiplied into new findings. Required evidence for all seven rows was available and assessed; uninvoked runtime evidence is explicitly NOT APPLICABLE, not missing or passed.")
    add("## Unsupported or Excessive Governance")
    add("Unsupported Governance Controls = 1: F003's universal approved-source prerequisite is unsupported on the initial pre-approval update path. It is the same Medium lifecycle finding, not an additional finding. F004 is counted as Ambiguity rather than confirmed unsupported control because later population is a possible reading. Neither problematic rule is silently enforced or waived. No new residual-risk acknowledgement, prior-same-actor-success, different-host/principal, future-coordinator-before-Audit or unapproved product activation prerequisite is imposed.")
    add("## Human Decisions Required")
    add("No normative wording, finding acceptance or correction is selected by this Audit. Human may separately authorize bounded Governance Remediation continuation to independently validate this new result/report and register/route F003/F004 in the existing Work ID/Cycle 1. That start is not finding acceptance, correction approval, Investigation start, adoption or product activation. Each subsequent Investigation/Corrective Decision/Application/Verification/Review/Audit requires its own applicable Human decision/start and exact approval gates.")
    add("Any decision to reconcile initial Requirement source statuses or enhancement actor-field timing belongs to the governed corrective path. No stage is automatically invoked. Adoption of the prospective Master baseline, a product root and target portability decisions remain separate unmet authorities outside this Audit.")
    add("## Recommended Corrective Actions")
    add("1. Preserve and hand off this complete canonical Audit/result/evidence; a separately authorized Remediation actor must independently recompute result SHA-256, confirm its final report/evidence bindings and record the result path/identity/verified digest/outcome in its canonical terminal handoff under the same Work ID/cycle.\n2. Separately Human-start Finding Investigation for F003/F004 if authorized; no root-cause investigation is performed here. Route confirmed dispositions through Corrective Change Decision and required exact Human Approval; use a distinct authorized applier where required.\n3. For F003, reconcile all four Update artifacts with the initial clarification route while retaining immutable versions, decision approval, full reanalysis/Verification and separate formal Requirement Approval.\n4. For F004, specify stage-specific current versus planned actor fields without precreating future attempts/capabilities or weakening distinct-actor/approval controls.\n5. After approved correction and required independent Verification/Review, separately initiate another **complete** 52-core plus seven-group Audit, not a finding-only recheck. No source edits, application or other stage has been performed by this Audit.")
    add("## Overall Audit Result")
    add("**INCONSISTENT.** Complete execution: 52/52/52 core; actual inventory 76, all sources assessed; seven groups assessed, five PASS and two FAIL (Orchestration/F003 and Application definition relationship/F004). Two unique Medium findings, including one Ambiguity and one Unsupported Governance Control; all other five counters zero. No CANNOT COMPLETE mechanism or unassessed artifact is represented as pass.")
    add("Only exact CONSISTENT with **all eight counts zero** and all seven groups resolved qualifies for governance-amendment effectiveness. This Audit does **not** establish effectiveness despite the scoped Application/Verification/Review successes and addressed old finding. It never approves/accepts the framework, adopts Masters/product root or activates product processes.")
    add("### Operational evidence and limitations")
    add(f"All {comparison['baseline_files']} initial governance/source/record paths and bytes/hash bindings remain endpoint-identical; directory set, Git HEAD/branch/status and `.git/index` (10,274 bytes, `51D40838E46A8C974CD8D5B034AF87A2F170EC592D0C5CC8C57890100A8748B6`) unchanged. Only own fresh output files added. Five preexisting approved source corrections and current approved Remediation change were retained; no source/upstream/history edits, stage dispatch, product activity, staging, commit, branch creation or push.")
    add("Available actor-visible operation evidence: read governing definitions/Masters; actual filesystem and hidden-inclusive inventory; nonmutating identity/ACL/Git checks; invocation-before-assessment publication/readback; full ordered source reads; read scoped upstream reports/results/evidence; native JSON/full-byte diff/hash/path checks; current checkpoint endpoint comparisons; own immutable evidence/report/result publication; fresh separate final readback. The UTF-8 stdout display error during a read was corrected with no file effects. Root-only reference scan limits were resolved in supplementary evidence without altering earlier scan records.")
    add("\n".join("- "+x for x in LIMITS))
    add("### Canonical own evidence bindings")
    own=[ref(SCOPE/"attempt.json"),ref(SCOPE/"evidence/input-manifest.json"),
         ref(SCOPE/"evidence/integrity-checks.json"),ref(SCOPE/"checkpoint-0001.json"),
         ref(SCOPE/"checkpoint-0002.json"),evidence]
    add(table(["Record path","Bytes","SHA-256"],[[x["path"],x["bytes"],x["sha256"]] for x in own]))
    add(f"Result `{PREFIX}/result.json`, identity `{ATTEMPT}:audit_result`, follows and binds this canonical report. A later fresh-process checkpoint-0003 binds its actual digest and readback; this report claims no digest for itself, its future result, or that future checkpoint. The future Remediation final report is a subsequent terminal anchor, never an Audit publication precondition. **STOP — no other stage authorized or started.**")
    return "\n".join(out).encode("utf-8")

def complete():
    sup=supplement()
    assert not I["bindings_requiring_classification"] and not sup["binding_failures_after_resolution"]
    rows=coverage();comparison=compare()
    assert not any(comparison[k] for k in ["changed","added","removed"]) and comparison["directory_set_unchanged"]
    assert comparison["repository"]==INV["repository_context"]
    publish("checkpoint-0002.json",record("audit_checkpoint",sequence=2,
       confirmed_boundary="Complete 52-core plus seven-mechanism comparison and upstream evidence checks; findings finalized; complete endpoint recheck before canonical evidence/report/result",
       input_comparison=comparison,finding_ids=[F3,F4],counts=counts(),blockers=[],
       unfinished_work="Publish validated canonical evidence/report, then terminal result, then separate fresh-process readback",
       no_other_stage_authorized=True))
    # Groups carry a path/identity forward reference to own evidence; avoid circular evidence hash.
    forward={"path":PREFIX+"/evidence/audit-evidence.json","record_id":ATTEMPT+":audit_evidence"}
    groups=mechanisms(forward)
    ev=record("audit_evidence",invocation=ref(SCOPE/"attempt.json"),
       input_manifest=ref(SCOPE/"evidence/input-manifest.json"),executed_checks=ref(SCOPE/"evidence/integrity-checks.json"),
       own_execution_helpers=[ref(SCOPE/"evidence"/name) for name in
          ["retry-publisher.py","audit-checks.py","complete-audit.py","publisher-selftest.json"]],
       checkpoint_0001=ref(SCOPE/"checkpoint-0001.json"),checkpoint_0002=ref(SCOPE/"checkpoint-0002.json"),
       scope={"expected":52,"found":52,"audited":52,"source_inventory_count":76,"mechanism_groups":7},
       inventory=I["source_inventory"],core_assessments=rows,traceability=I["core_traceability"],
       mechanism_alignment=groups,findings=FINDINGS,counts=counts(),supplementary_checks=sup,
       final_input_comparison=comparison,limitations=LIMITS,
       effectivity=False,master_adoption=False,product_root_adoption=False,
       source_writes=0,other_actor_record_writes=0,other_stage_started=False,
       execution_status="COMPLETED",outcome="INCONSISTENT")
    # Validate the ACTUAL complete objects, not a reduced sample.
    for obj in [ev,rows,groups,FINDINGS]:
        encoded=json.dumps(obj,ensure_ascii=False,allow_nan=False)
        assert json.loads(encoded)==obj
    evref=publish("evidence/audit-evidence.json",ev)
    finalgroups=mechanisms(dict(evref,record_id=ATTEMPT+":audit_evidence"))
    body=report(evref,rows,finalgroups,sup,comparison)
    required=["Audit Scope","Separately Reported Mechanism Alignment","Repository Reference Findings",
      "Governance Consistency Findings","Guideline Consistency Summary","Prompt Consistency Summary",
      "Request Template Consistency Summary","SDLC Process Skill Consistency Summary","SDLC Process Agent Consistency Summary",
      "Skill and Agent Traceability Summary","Cross-Document Consistency Summary","Governance Gaps",
      "Unsupported or Excessive Governance","Human Decisions Required","Recommended Corrective Actions","Overall Audit Result"]
    assert all(("## "+s).encode() in body for s in required)
    assert b"`n" not in body and b"$(" not in body and b"{{" not in body
    reportref=publish("report.md",body)
    after=compare()
    assert after==comparison
    result=record("audit_result",execution_status="COMPLETED",outcome="INCONSISTENT",
       report=dict(reportref,record_id=ATTEMPT+":audit_report"),
       evidence=[dict(evref,record_id=ATTEMPT+":audit_evidence"),ref(SCOPE/"evidence/integrity-checks.json"),
          ref(SCOPE/"evidence/input-manifest.json"),ref(SCOPE/"checkpoint-0001.json"),ref(SCOPE/"checkpoint-0002.json")],
       invocation=ref(SCOPE/"attempt.json"),scope={"expected":52,"found":52,"audited":52,"actual_source_inventory":76},
       counts=counts(),findings=FINDINGS,mechanisms=finalgroups,
       current_amendment_stage_status={"Application":{"execution_status":"COMPLETED","outcome":"EXACT APPROVED BYTES APPLIED"},
        "Verification":{"execution_status":"COMPLETED","outcome":"PASS","criteria_pass":14},
        "Review":{"execution_status":"COMPLETED","outcome":"PASS","criteria_pass":8}},
       final_input_comparison=after,limitations=LIMITS,
       effectiveness_qualifying=False,master_adoption=False,product_root_adoption=False,
       source_writes=0,other_actor_record_writes=0,other_stage_started=False,product_content_audited=False,
       next_gate="STOP. Separate fresh Human authorization required for bounded Governance Remediation continuation; that actor must independently validate this Audit result/report and route F003/F004. No Investigation/Decision/Application/adoption/product process started.",
       terminal_anchor_obligation="Subsequent authorized same-cycle Remediation canonical final report must bind independently verified Audit result hash, identity, report binding and outcome; its result then binds its final report. Not an Audit prerequisite.",
       final_readback="Separate fresh-process readback follows in new immutable checkpoint-0003.json; not yet claimed by this result at preparation.",
       publication="Full native JSON .partial exclusive creation, validate bytes/roundtrip, flush/fsync, same-volume Windows atomic no-overwrite rename and exact readback")
    assert json.loads(json.dumps(result,ensure_ascii=False,allow_nan=False))==result
    rr=publish("result.json",result)
    print(json.dumps({"report":reportref,"result":rr,"evidence":evref,"counts":counts(),
       "groups":[{"group":g["group"],"result":g["result"]} for g in finalgroups]},indent=2))

if __name__=="__main__":
    complete()
