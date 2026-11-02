import os, sys, json, hashlib, pathlib, datetime, subprocess, re, math

ROOT = pathlib.Path(__file__).resolve().parents[7]
os.chdir(ROOT)
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T162238Z-28a7c86b-114f-4d7f-8520-f09000a0df40"
BASE = pathlib.Path("docs/sdlc-records/governance") / WORK / "attempts"
OWN = BASE / ATTEMPT
AUD = BASE / "20261102T160240Z-5022506a-f881-4681-af13-e4acf3bb6935"
ROLE = pathlib.Path(".github/agents/sdlc-governance-remediation.agent.md")
PROCESS = "SDLC Governance Remediation"
START = "Yes, initiate the bounded final Governance Remediation continuation to validate and anchor the CONSISTENT Audit and produce its final handoff only"
ACTOR = {
    "identity": "d783452a-fbb0-49e2-ab02-b16bd833f26f",
    "role": PROCESS,
    "runtime_agent_id": "d783452a-fbb0-49e2-ab02-b16bd833f26f",
    "copilot_agent_session_id": "a85e6602-5e2f-493a-a9d2-4423740416c3",
    "session": "ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
    "identity_basis": "Current sole running bounded Final Handoff actor in harness registry plus current environment COPILOT_AGENT_SESSION_ID; session title is not role proof; not cryptographic external identity."
}
LIMITS = [
    "Procedural read-only boundaries, not an enforced filesystem sandbox.",
    "No exhaustive trusted event log or coordinated source lock.",
    "Endpoint fingerprints cannot exclude transient or same-principal tampering.",
    "Authenticated platform Human message IDs/times not exposed; not invented.",
    "No exact filesystem publication timestamp claimed; ordered operation/readback evidence is used.",
    "This continuation validates existing Audit bindings and closure; it is not a new complete Audit or a runtime test of uninvoked mechanisms."
]
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):
    return hashlib.sha256(b).hexdigest().upper()
def ref(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    d = {"path": p.as_posix(), "bytes": len(b), "sha256": digest(b)}
    if p.suffix == ".json":
        try:
            j = load(p)
        except (ValueError, UnicodeError) as e:
            # Historical invalid records remain raw-byte inputs, never valid assurance.
            d["json_parse_status"] = "INVALID historical input: " + type(e).__name__
        else:
            if isinstance(j, dict) and "record_id" in j:
                d["record_id"] = j["record_id"]
    return d
def pairs(items):
    d = {}
    for k,v in items:
        if k in d:
            raise ValueError("Duplicate JSON key: " + k)
        d[k] = v
    return d
def decode(b):
    return json.loads(b.decode("utf-8-sig"), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def load(p):
    return decode(pathlib.Path(p).read_bytes())
def native(v):
    assert type(v) in (dict,list,str,int,float,bool,type(None)), type(v)
    if type(v) is float:
        assert math.isfinite(v)
    if type(v) is dict:
        for k,x in v.items():
            assert type(k) is str
            native(x)
    if type(v) is list:
        for x in v: native(x)
def common(kind):
    return {
        "schema_version": "1.0", "record_type": kind,
        "record_id": ATTEMPT + ":" + kind, "feature": "Governance framework only; no product feature",
        "work_id": WORK, "attempt_id": ATTEMPT,
        "cycle_id": "GOV-REMEDIATION-PROSPECTIVE-001", "cycle": 1,
        "process": PROCESS, "creator": ACTOR, "created_at_utc": now(),
        "clock_basis": "Timezone-aware system UTC at record preparation; not publication time",
        "gate": {"applicability": "No formal human gate created or satisfied by this bounded continuation"},
        "related_records": [], "task_context": "No product task; existing governance Cycle 1"
    }
def validate(d):
    native(d)
    required = ["schema_version","record_type","record_id","feature","work_id","attempt_id",
                "process","creator","created_at_utc","clock_basis","gate","related_records","task_context"]
    assert type(d) is dict and all(k in d for k in required)
    for k in ["schema_version","record_type","record_id","feature","work_id","attempt_id","process","created_at_utc","clock_basis","task_context"]:
        assert type(d[k]) is str and d[k].strip(), k
    assert d["schema_version"] == "1.0" and d["work_id"] == WORK and d["attempt_id"] == ATTEMPT
    assert d["creator"] == ACTOR and type(d["creator"]) is dict
    assert d["creator"]["role"] == PROCESS
    assert type(d["gate"]) is dict and type(d["related_records"]) is list
    assert datetime.datetime.fromisoformat(d["created_at_utc"]).utcoffset().total_seconds() == 0
    assert d["cycle_id"] == "GOV-REMEDIATION-PROSPECTIVE-001" and d["cycle"] == 1
    if d["record_type"] == "remediation_invocation":
        for k in ["requested_scope","input_manifest","repository_context","stage_start","predecessors","persistence","qualification","recovery","outputs"]:
            assert k in d, k
        assert type(d["input_manifest"]) is dict
        assert type(d["qualification"]) is dict
        assert type(d["repository_context"]) is dict
        assert type(d["stage_start"]) is dict and d["stage_start"]["actual_wording"] == START
        assert type(d["predecessors"]) is list
        assert d["persistence"]["authorized_output_scope"] == OWN.as_posix()
    if d["record_type"] == "remediation_result":
        for k in ["execution_status","outcome","report","evidence","evaluated_state","unresolved_items","next_permitted_process"]:
            assert k in d, k
    b = (json.dumps(d,ensure_ascii=False,allow_nan=False,indent=2)+"\n").encode("utf-8")
    assert decode(b) == d
    assert b"`n" not in b and b"`r" not in b
    return b
def publish(name, d):
    p = OWN / name
    p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(), "Final record collision"
    q = p.with_name(p.name + ".partial")
    b = validate(d) if isinstance(d,dict) else d.encode("utf-8")
    with q.open("xb") as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert q.read_bytes() == b
    if isinstance(d,dict):
        assert decode(q.read_bytes()) == d
        validate(decode(q.read_bytes()))
    assert os.name == "nt", "This publisher relies on Windows no-overwrite rename semantics"
    os.rename(q,p)
    assert p.read_bytes() == b
    return ref(p)
def git(*a):
    return subprocess.check_output(["git","--no-pager",*a],text=True).strip()
def context():
    return {"canonical":"ScalableParimal/SupportIQ","root":str(ROOT),
            "head":git("rev-parse","HEAD"),"branch":git("branch","--show-current"),
            "origin":git("remote","get-url","origin"),"status":git("status","--porcelain=v1"),
            "index":ref(".git/index")}
def inventory():
    paths = []
    for r in [pathlib.Path(".github"),pathlib.Path("docs/ai"),pathlib.Path("docs/sdlc-records/governance")]:
        for p in r.rglob("*"):
            if p.is_file() and not p.is_relative_to(OWN):
                assert not p.is_symlink(), "Unresolved symlink in input manifest"
                paths.append(p)
    return [ref(p) for p in sorted(set(paths),key=lambda p:p.as_posix())]
def verify_ref(r):
    a = ref(r["path"])
    assert a["sha256"] == r["sha256"].upper(), ("fingerprint mismatch",r["path"])
    if "bytes" in r: assert a["bytes"] == r["bytes"], r["path"]
    # Markdown/native evidence identities are assigned by the binding record;
    # only JSON carries an independently machine-readable record_id field.
    if "record_id" in r and pathlib.Path(r["path"]).suffix == ".json":
        assert a.get("record_id") == r["record_id"], r["path"]
    return a
def preflight():
    assert not (OWN/"attempt.json").exists(), "One attempt only; no replacement"
    assert ref(ROLE)["bytes"] == 49225
    assert ref(ROLE)["sha256"] == "404AF9126BC310AEA79BA7616AB8E25C0AD5EE7F48B360F1AF515EA4DC9F942F"
    assert os.environ.get("COPILOT_AGENT_SESSION_ID") == ACTOR["copilot_agent_session_id"]
    assert digest(b"abc") == "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD"
    for b in [b'{"x":1,"x":2}',b'{"x":NaN}']:
        try: decode(b)
        except ValueError: pass
        else: raise AssertionError("Invalid JSON accepted")
    for v in [set([1]),float("inf"),(1,2)]:
        try: native(v)
        except AssertionError: pass
        else: raise AssertionError("Nonnative JSON accepted")
    # Non-mutating capability checks: actual reads, effective principal and directory ACL.
    principal = subprocess.check_output(["whoami"],text=True).strip()
    acl = subprocess.check_output(["icacls",str(BASE.resolve())],text=True)
    c = context()
    assert c["head"] == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c"
    assert c["origin"] == "https://github.com/ScalableParimal/SupportIQ.git"
    inputs = inventory()
    m = common("remediation_input_manifest")
    m.update({"entries":inputs,"entry_count":len(inputs),"hidden_inclusive":True,
              "scope":[".github/**","docs/ai/**","docs/sdlc-records/governance/**"],
              "exclusions":"Own new output scope and .git internals except separately fingerprinted index; no product inputs relied on",
              "repository_context":c})
    mr = publish("evidence/input-manifest.json",m)
    s = common("publisher_selftest")
    s.update({"sha256_known_answer":"PASS","strict_json_negative_tests":"PASS",
              "actual_complete_object_schema_and_roundtrip":"PASS",
              "capability_basis":"Current non-mutating reads, principal, ACL and publisher implementation inspection; actual permitted output publication/readback follows",
              "effective_principal":principal,"attempts_acl":acl})
    sr = publish("evidence/publisher-selftest.json",s)
    try: os.rename(OWN/"evidence/input-manifest.json",OWN/"evidence/publisher-selftest.json")
    except FileExistsError: pass
    else: raise AssertionError("Atomic rename overwrote existing final")
    verify_ref(mr); verify_ref(sr)
    assert inventory() == inputs and context() == c, "Inputs changed before invocation"
    a = common("remediation_invocation")
    a.update({
        "requested_scope":"ONLY bounded final Governance Remediation continuation: validate stored clean Audit, current bindings and closure; publish own canonical final report/result/evidence/handoff. No new Audit, corrections, other stage, adoption, Portability, product activation, staging, commit or push.",
        "input_manifest":mr,"repository_context":c,
        "stage_start":{"actual_wording":START,"source":"Actual Human message supplied to current invocation","authenticated_message_id":None,"authenticated_source_time":None,"scope":"ONE attempt; invalid published invocation means STOP; no autonomous replacement"},
        "predecessors":[ref(AUD/n) for n in ["attempt.json","report.md","result.json","evidence/audit-evidence.json","checkpoint-final.json"]],
        "persistence":{"root":"docs/sdlc-records/governance/","route":"Existing established Work ID; not bootstrap",
                       "authorized_output_scope":OWN.as_posix(),
                       "root_adoption_evidence":{"url":"https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236","author":"ScalableParimal","author_id":226102895,"association":"OWNER","created_at":"2026-10-30T12:31:51Z","validation":"Live authenticated GitHub issue_read get_comments during current preflight; root adoption only; initial stage authorization not reused"}},
        "qualification":{"effective_principal":principal,"attempts_acl":acl,"role_definition":ref(ROLE),
                         "capabilities":["Current source/upstream read access","Hidden-inclusive recursive enumeration","SHA-256 actual-byte fingerprints","Native JSON strict serialization/parsing and common-metadata/schema validation","Validated/flushed .partial; same-filesystem Windows atomic no-overwrite rename; exact fresh readback"],
                         "publisher_selftest":sr,"source_mutation_permission":"NONE","limitations":LIMITS},
        "recovery":{"existing_work_id":WORK,"bounded_resume":"Existing Audit already exists before this invocation; historical records remain unchanged; no prior invocation is retried or replaced","competing_actor_observation":"Harness sole running bounded Final Handoff entry is this actor; idle actors are not treated as active writers","incomplete_attempts":"Historical unsuccessful attempts retained for closure reconciliation; not valid assurance"},
        "outputs":{"report":(OWN/"report.md").as_posix(),"result":(OWN/"result.json").as_posix(),"evidence":(OWN/"evidence/closure-evidence.json").as_posix(),"handoff":(OWN/"handoff.md").as_posix()},
        "ordering":"Publish and independently fresh-readback this invocation before substantive closure assessment",
        "execution_status":"STARTED"
    })
    ar = publish("attempt.json",a)
    print(json.dumps({"preflight":"PASS","attempt":ar,"manifest_entries":len(inputs),"next":"Independent fresh-process readback BEFORE substantive assessment"},indent=2))

def bound_references(v):
    found = {}
    def walk(x):
        if type(x) is dict:
            if type(x.get("path")) is str and type(x.get("sha256")) is str and re.fullmatch("[0-9a-fA-F]{64}",x["sha256"]):
                found[(x["path"],x["sha256"].upper())] = x
            for y in x.values(): walk(y)
        elif type(x) is list:
            for y in x: walk(y)
    walk(v)
    return list(found.values())

def assess():
    a = load(OWN/"attempt.json")
    validate(a)
    rb = load(OWN/"evidence/invocation-readback.json")
    assert rb["outcome"] == "PASS"
    verify_ref(rb["invocation"])
    m = load(a["input_manifest"]["path"])
    assert inventory() == m["entries"] and context() == a["repository_context"]
    expected = {
        "report.md":(122315,"C72AF2A1761610365C36A249E8892B08C7A23BA2D9A7C1F47749C3BFEC796256"),
        "result.json":(37941,"CF073B8E08EDF728B6AB1B1CC300C842D3FEF15F512A084C85B7A7E8EF199222"),
        "evidence/audit-evidence.json":(550499,"9F0519457976E8D57E5C9F5A7C9DFFD7D03E5492529032D836F2FEAD66F00DF1"),
        "checkpoint-final.json":(5726,"9B00FE4F5100B7ECDCFA6774B249CDD57CC106079E63A172A45E2C245B955F3A")
    }
    audit_refs = {}
    for name,(size,sha) in expected.items():
        audit_refs[name] = verify_ref({"path":(AUD/name).as_posix(),"bytes":size,"sha256":sha})
    r = load(AUD/"result.json")
    e = load(AUD/"evidence/audit-evidence.json")
    f = load(AUD/"checkpoint-final.json")
    for j in [r,e,f]:
        native(j)
        assert decode(json.dumps(j,allow_nan=False).encode()) == j
        assert j["work_id"] == WORK and j["cycle_id"] == a["cycle_id"] and j["cycle"] == 1
        assert j["attempt_id"] == AUD.name
    assert r["execution_status"] == "COMPLETED" and r["outcome"] == "CONSISTENT"
    assert r["findings"] == [] and e["assessment"]["findings"] == []
    assert len(r["counts"]) == 8 and all(type(v) is int and v == 0 for v in r["counts"].values())
    assert r["scope"] == {"expected":52,"found":52,"audited":52,"actual_source_inventory":76,"mechanism_groups":7}
    assert f["execution_status"] == "COMPLETED" and f["outcome"] == "PASS"
    assert f["result"]["sha256"] == audit_refs["result.json"]["sha256"]
    assert r["report"]["sha256"] == audit_refs["report.md"]["sha256"]
    assert f["report"] == r["report"] and f["evidence"] == r["evidence"]
    verify_ref(f["result"]); verify_ref(r["report"]); verify_ref(r["evidence"])
    assert len(r["required_evidence_records"]) == 5
    for x in r["required_evidence_records"]: verify_ref(x)
    assessment = e["assessment"]
    sources = assessment["source_inventory"]
    assert len(sources) == 76 and len(assessment["core_artifacts"]) == 52
    live = [x for x in inventory() if x["path"].startswith((".github/","docs/ai/"))]
    assert {(x["path"],x["bytes"],x["sha256"]) for x in sources} == {(x["path"],x["bytes"],x["sha256"]) for x in live}
    all_current_refs = bound_references([r,assessment["record_references"],sources,f])
    for x in all_current_refs: verify_ref(x)
    groups = r["mechanisms"]
    assert len(groups) == 7 and len({x["group"] for x in groups}) == 7
    for x in groups:
        assert x["expected"] is True and x["present"] is True and x["assessed"] is True
        assert x["outcome"] == "PASS"
        for c in x["checks"]:
            if c["id"] in ("M03-05","M04-06"):
                assert x["group"] in ("SDLC Process Orchestration","SDLC Portability Assessment")
                assert c["outcome"] == "NOT APPLICABLE" and c["rationale"].startswith("NOT APPLICABLE:")
                assert x["runtime_applicability"].startswith("NOT APPLICABLE")
            else:
                assert c["outcome"] == "PASS"
    # Validate latest exact approved target after-state, without reapplying anything.
    proposal_id = "20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d"
    application_id = "20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494"
    verification_id = "20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216"
    review_id = "20261102T154422Z-cdfe6363-b6ac-42d2-8896-979df6f5d322"
    proposal = load(BASE/proposal_id/"attachments/exact-proposal.json")
    targets = []
    for t in proposal["targets"]:
        actual = verify_ref({"path":t["path"],"bytes":t["expected_after_bytes"],"sha256":t["expected_after_sha256"]})
        targets.append({"actual":actual,"findings":t["finding_ids"],"operation":t["operation"],
                        "replacement_count":len(t["replacements"]),"outcome":"PASS"})
    assert len(targets) == 5
    latest = {k:load(BASE/v/"result.json") for k,v in [
        ("proposal",proposal_id),("application",application_id),("verification",verification_id),("review",review_id)]}
    assert latest["application"]["outcome"] == "COMPLETED"
    assert latest["application"]["errors"] == [None,None]
    assert latest["verification"]["execution_status"] == "COMPLETED" and latest["verification"]["outcome"] == "PASS"
    assert latest["review"]["execution_status"] == "COMPLETED" and latest["review"]["outcome"] == "PASS"
    actors = {k:v["creator"]["runtime_agent_id"] for k,v in latest.items()}
    assert len(set(actors.values())) == 4 and ACTOR["runtime_agent_id"] not in actors.values()
    for k in ["verification","review"]:
        assert all(x["outcome"] == "PASS" for x in latest[k]["criteria"])
    verification_ref = ref(BASE/verification_id/"result.json")
    application_ref = ref(BASE/application_id/"result.json")
    review_ref = ref(BASE/review_id/"result.json")
    for successor,predecessor in [(latest["verification"],application_ref),(latest["review"],verification_ref),([r,e],review_ref)]:
        assert any(x["path"] == predecessor["path"] and x["sha256"] == predecessor["sha256"] for x in bound_references(successor))
    for k in ["application","verification","review"]:
        for x in bound_references(latest[k]):
            if x["path"].startswith("docs/sdlc-records/"):
                verify_ref(x)
    human = load(BASE/application_id/"evidence/human-authorization.json")
    assert human["approval_exact_ascii"] == "I approve the identified canonical report, exact proposal and patch with all five target fingerprints, scope, actor and assurance bindings; freshly designate the proposed one-time applier under that route; do not start Application"
    assert human["separate_stage_start_exact_ascii"] == "Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 under the approved five-file package"
    # Current source changes must be exactly the attributable 5 + 1 + 5 files.
    first_id = "20261030T143302Z-51b92d83-6dec-49aa-8bb7-3849581e9d55"
    first = load(BASE/first_id/"result.json")
    assert first["execution_termination"] == "COMPLETED"
    assert first["application_outcome"] == "SUCCESSFULLY APPLIED EXACT APPROVED BYTES"
    first_targets = first["exact_evaluated_state"]["target_manifest"]
    for t in first_targets:
        verify_ref({"path":t["target_path"],"bytes":t["expected_after_bytes"],"sha256":t["expected_after_sha256"]})
    changed = set(git("diff","--name-only").splitlines())
    expected_changes = {t["target_path"] for t in first_targets} | {ROLE.as_posix()} | {t["path"] for t in proposal["targets"]}
    assert changed == expected_changes and len(changed) == 11
    assert git("diff","--cached","--name-only") == ""
    # Reconcile the canonical actor-owned historical report/result pairs; no new
    # schema is retroactively imposed on older process-specific records.
    history_specs = [
        ("original-application",first_id,"report.md","result.json"),
        ("append-only-transcription","20261030T152030Z-63870b37-91d1-4807-980e-565596f1c694","report.md","result.json"),
        ("original-verification","20261030T161112Z-9c79d789-1b9a-479c-a9e7-6e692747330f","report.md","result.json"),
        ("original-review","20261031T043137Z-7d2b35df-98a6-4d50-8761-48fe0f724e0f","report.md","result.json"),
        ("prospective-admission","20261031T072633Z-4c6c7de5-037e-49d1-a594-97b7ef0c5319","report.md","result.json"),
        ("strict-investigation","20261102T072445Z-1d19ba42-5fc4-428b-a395-0de523e319c0","report.md","result.json"),
        ("no-additional-change-decision","20261102T073730Z-5ab1b82b-73b5-4a2b-90ad-584a38f80d37","report.md","result.json"),
        ("first-coordinator","20261102T075750Z-1210d4b1-8300-4b17-8f6b-911a2f64958e","report-revision-0001.md","result.json"),
        ("F001-application","20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd","report.md","result.json"),
        ("F001-verification","20261102T093828Z-237e94b9-3902-49d3-ab46-5011a3c989e1","report.md","result.json"),
        ("F001-review","20261102T094612Z-977731b8-9c8a-4df4-944b-15102e7c22cb","report.md","result.json"),
        ("F002-application","20261102T110324Z-b92b73f0-deba-4842-b261-1ed22bd7d014","report.md","result.json"),
        ("F002-verification","20261102T110840Z-c1d89695-d3e5-4721-a846-3f3dca25cc22","report.md","result.json"),
        ("F002-review","20261102T1130Z-d7d84322-aff9-4d3e-9cec-90f9054705cd","report.md","result.json"),
        ("prior-INCONSISTENT-Audit","20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f","report.md","result.json"),
        ("canonical-coordinator","20261102T132628Z-e9227c1a-70ab-4afc-87e2-49eca280b879","report-revision-0001.md","result-revision-0002.json"),
        ("canonical-investigation","20261102T141609Z-4e74248e-a440-4617-8c17-61f31f2ff9c9","report-revision-0002.md","result-revision-0002.json"),
        ("F003-F004-proposal",proposal_id,"report.md","result.json"),
        ("F003-F004-application",application_id,"report.md","result.json"),
        ("F003-F004-verification",verification_id,"report.md","result.json"),
        ("F003-F004-review",review_id,"report.md","result.json")
    ]
    history = []
    for label,aid,rname,jname in history_specs:
        rp,jp = BASE/aid/rname,BASE/aid/jname
        j = load(jp)
        rr = ref(rp)
        # Inspect native JSON body and report; identities/locations are preserved.
        rp.read_text(encoding="utf-8-sig")
        for x in bound_references(j):
            if x["path"] == rp.as_posix(): verify_ref(x)
        history.append({"label":label,"attempt":ref(BASE/aid/"attempt.json"),
                        "report":rr,"result":ref(jp),
                        "native_execution_status":j.get("execution_status",j.get("execution_termination",j.get("executionTermination"))),
                        "native_outcome":j.get("outcome",j.get("application_outcome",j.get("investigation_outcome",j.get("remediation_status"))))})
    for label in ["original-verification","original-review","F001-verification","F001-review","F002-verification","F002-review"]:
        row = next(x for x in history if x["label"] == label)
        assert load(row["result"]["path"])["outcome"] == "PASS"
    clarification = ref(BASE/"20261102T092357Z-ef6258d2-8754-40d8-bf30-34f22c3ccfbd/attachments/GOV-AUD-20261102-001-linked-clarification.md")
    assert clarification["bytes"] == 3438 and clarification["sha256"] == "8887DC81719F3D3E044323A1D32C1CA93D9102F03FD6F28CB79DC5608D3C8FFA"
    # The report-before-result direction must remain non-circular.
    report_text = (AUD/"report.md").read_text(encoding="utf-8")
    assert r["record_id"] in report_text
    assert audit_refs["result.json"]["sha256"] not in report_text
    assert audit_refs["report.md"]["sha256"] not in report_text
    assert not pathlib.Path("docs/sdlc-records/product").exists()
    assert inventory() == m["entries"] and context() == a["repository_context"]
    out = common("remediation_closure_evidence")
    out.update({
        "execution_status":"COMPLETED","outcome":"PASS",
        "invocation":ref(OWN/"attempt.json"),"invocation_readback":ref(OWN/"evidence/invocation-readback.json"),
        "input_manifest":a["input_manifest"],"audit":audit_refs,
        "audit_report_identity":r["report"]["record_id"],"audit_result_identity":r["record_id"],
        "audit_binding_validation":"PASS: independently recomputed stored result SHA-256; exact report/evidence/checkpoint/result identities and bytes match; empty findings list explicitly validated",
        "current_binding_references_verified":len(all_current_refs),
        "required_Audit_evidence_records":[verify_ref(x) for x in r["required_evidence_records"]],
        "source_inventory":sources,"core_scope":r["scope"],"counts":r["counts"],"findings":[],
        "mechanisms":[{k:x[k] for k in ["group","expected","present","assessed","outcome","runtime_applicability"]} for x in groups],
        "latest_exact_target_checks":targets,"initial_exact_targets":[ref(t["target_path"]) for t in first_targets],
        "actual_source_change_set":sorted(changed),"actor_separation":actors,
        "latest_human_authorization":ref(BASE/application_id/"evidence/human-authorization.json"),
        "fresh_assurance_starts":assessment["current_evidence_checks"]["fresh_assurance_starts"],
        "history":history,"linked_clarification":clarification,
        "historical_unsuccessful_records":"Preserved; prior F003/F004 Verification 20261102T152557Z-efc37bf9-a1dd-4f02-b768-d797e0636818 and other unsuccessful/replaced records are not valid assurance. Fresh human-started PASS Verification is used; no retroauthorization.",
        "final_input_comparison":{"outcome":"PASS","inputs":len(m["entries"]),"all_bytes_and_path_set_unchanged":True,"repository_head_branch_status_origin_index_unchanged":True},
        "non_circular_order":"Existing final Audit report -> Audit result -> current Remediation closure evidence/report -> later Remediation result -> presentation handoff",
        "remediation_status":"COMPLETE","master_baseline_adopted":False,"product_root_adopted":False,
        "product_orchestrator_invoked":False,"portability_invoked":False,
        "human_acceptance_claimed":False,"framework_human_approval_claimed":False,
        "source_writes":False,"upstream_or_history_writes":False,"staging_commit_push":False,
        "limitations":LIMITS,
        "prepublication_helper_diagnostics":"Before invocation publication a raw historical malformed JSON input was initially parsed as if valid; corrected to retain its exact raw hash and explicit invalid status, without treating it as assurance. During unpublished assessment, logical IDs on Markdown/native evidence were initially compared to JSON-only embedded IDs; corrected to retain external identity and verify actual bytes/hash. No published record, input check or governance rule was weakened."
    })
    er = publish("evidence/closure-evidence.json",out)
    print(json.dumps({"assessment":"PASS","evidence":er,"current_bindings":len(all_current_refs),"sources":len(sources),"history_pairs":len(history),"remediation_status":"COMPLETE"},indent=2))

def report():
    e = load(OWN/"evidence/closure-evidence.json")
    validate(e)
    assert e["outcome"] == "PASS" and e["remediation_status"] == "COMPLETE"
    a = load(OWN/"attempt.json")
    assert inventory() == load(a["input_manifest"]["path"])["entries"] and context() == a["repository_context"]
    lines = [
        "# FINAL GOVERNANCE STATUS", "",
        "Canonical Governance Remediation final report; AI governance-consistency closure only.",
        "Canonical report identity: `" + ATTEMPT + ":remediation_report`.",
        "Work ID: `" + WORK + "`; actor runtime ID `" + ACTOR["runtime_agent_id"] + "`.",
        "Own attempt: `" + ATTEMPT + "`; process: SDLC Governance Remediation.", "",
        "| Status field | Validated value |", "|---|---|",
        "| Remediation Cycle ID | GOV-REMEDIATION-PROSPECTIVE-001 |",
        "| Final Audit Cycle | Cycle 1 |",
        "| Audit Scope | 52 SDLC Governance artifacts |",
        "| Artifacts Expected | 52 |", "| Artifacts Found | 52 |", "| Artifacts Audited | 52 |"
    ]
    lines.extend("| " + k + " | " + str(v) + " |" for k,v in e["counts"].items())
    lines += [
        "| Overall Result | **CONSISTENT** |",
        "| Governance Remediation Status | **COMPLETE** |",
        "| Unresolved findings / pending corrective decisions or approvals | None |",
        "| Actual current governance-source inventory | 76, derived and fingerprint-checked; not 76 core artifacts |",
        "| Source/history modifications by this continuation | None |", "",
        "The existing complete Audit, not this bounded continuation, assessed all 3 Masters, 10 Guidelines, 10 Prompts, 10 Requests, 10 SDLC Process Skills and 9 SDLC Process Agents. This continuation did not re-Audit the 52. It independently validated current input applicability, stored Audit bindings and governed closure conditions. No clean result is inferred from hashes alone.", "",
        "## 1. Authorization, qualification and record-first execution", "",
        "Fresh actual Human stage-start supplied to this invocation:", "",
        "> " + START, "",
        "Scope is one bounded final continuation under the existing Work ID/Cycle 1; own new attempt records only. No replacement invocation is authorized. This start is not patch approval, Human Acceptance, baseline adoption, product-root adoption or authorization to begin another process.",
        "The current on-disk role is 49,225 bytes / SHA-256 `404AF9126BC310AEA79BA7616AB8E25C0AD5EE7F48B360F1AF515EA4DC9F942F`. The actual role and three Masters govern this continuation. Audit Skill loading supplies the applicable Audit-to-Remediation binding rules; no new Audit role or stage was invoked.",
        "Governance-root adoption was freshly resolved through the authenticated GitHub issue-read interface: OWNER ScalableParimal, user ID 226102895, https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236, created/updated 2026-10-30T12:31:51Z. Only established-root authority is retained; the original one-time Audit initiation is not reused.",
        "Repository: ScalableParimal/SupportIQ; HEAD `57ed3afe8a14a41bdbe38d4df621a99c836a0f4c`; branch `sdlc-framework-onboarding`. Eleven pre-existing unstaged governance-source modifications and the untracked governance records are preserved; nothing is staged.",
        "Current OS principal/ACLs, current runtime invocation environment and registry attribution, non-mutating reads/hashes, native JSON negative selftests, and the own-record publication route were established. A role label, session title, previous success or another actor's capability was not used as current capability evidence.",
        "The initial hidden-inclusive manifest contains 529 inputs under `.github`, `docs/ai` and all existing governance records, including relied sources/upstream/history. Own new outputs are excluded from that initial input set and bound separately. This manifest is an integrity inventory, not a claim of substantive re-investigation of every historical input.",
        "The complete actual invocation/common metadata and all own structured objects were schema/type checked, strictly serialized, parsed for exact native-object equality, validated in their own .partial, flushed/fsynced, and atomically published using same-filesystem Windows no-overwrite rename. Invocation publication was followed by independent fresh-process exact readback BEFORE substantive assessment. No invalid published invocation or autonomous replacement exists.",
        "One unpublished preflight helper assumption about parsing historical invalid JSON was corrected before the invocation existed; raw historical invalid inputs remain fingerprinted and explicitly invalid, not assurance. Unpublished assessment assumptions about logical IDs on non-JSON evidence, the two uninvoked runtime N/A checks, native Application no-error/completion schemas, and evidence-mediated predecessor references were corrected to match actual records and governing rules. No input, published output or upstream record was changed; no check was bypassed.", "",
        "## 2. Final Audit integrity anchor — non-circular chain", "",
        "| Record | Stable identity | Exact path | Bytes | Independently verified SHA-256 |",
        "|---|---|---|---:|---|"
    ]
    for name in ["report.md","result.json","evidence/audit-evidence.json","checkpoint-final.json"]:
        rr = e["audit"][name]
        identity = rr.get("record_id",e["audit_report_identity"] if name=="report.md" else "Native evidence binding")
        lines.append("| " + name + " | `" + identity + "` | `" + rr["path"] + "` | " + str(rr["bytes"]) + " | `" + rr["sha256"] + "` |")
    lines += [
        "", "**Validation outcome: PASS.** The stored Audit result SHA-256 was independently recomputed from actual bytes, not copied from the supplied summary. The result is COMPLETED/CONSISTENT and binds the exact canonical report by path, identity and SHA-256 and all five required evidence records. The final Audit checkpoint binds that same result/report/evidence and reports PASS. All eight counts are zero, findings is an actual empty JSON list, 52/52/52 core coverage is explicit, and all seven groups are assessed without unresolved issues.",
        "139 distinct current Audit/checkpoint/source/record fingerprint bindings were independently verified. The actual current `.github`/`docs/ai` source path set and all 76 fingerprints equal the Audit's assessed inventory. The latest exact five-file after-state, original five-file after-state, current Remediation definition and F001 linked clarification match their approved recorded bytes. All 529 pre-existing input paths/bytes and Git HEAD/branch/origin/status/index remain endpoint-identical.",
        "The Audit report preceded its result and identifies the result path/identity without a future result hash; it claims no self-hash. That already-existing Audit result precedes this final Remediation report. The later own `result.json` will bind this report and closure evidence. Neither this final report nor its handoff was treated as a prerequisite for the Audit. No circular completion condition is created.", "",
        "## 3. Separately Reported Mechanism Alignment", "",
        "Expected/found/assessed below are mechanism-group presence/assessment counts, not additional core artifacts. Detailed source/evidence/check rationales remain in the integrity-bound canonical Audit; this report preserves their actual conclusions.", "",
        "| Mechanism group | Expected | Found | Assessed | Result | Runtime applicability |", "|---|---:|---:|---:|---|---|"
    ]
    for g in e["mechanisms"]:
        runtime = "NOT APPLICABLE — not invoked; definitions assessed, no runtime PASS" if g["group"] in ("SDLC Process Orchestration","SDLC Portability Assessment") else "Invoked governance process; current stored evidence validated"
        lines.append("| " + g["group"] + " | 1 | 1 | 1 | " + g["outcome"] + " | " + runtime + " |")
    lines += [
        "", "All seven are same-framework checks outside the 52-core count. Uninvoked Orchestration and Portability runtime criteria remain NOT APPLICABLE, not failed, waived or runtime-capability PASS. Their future starts and current-environment capabilities are not established by this report.", "",
        "## 4. Remediation history — one preserved prospective cycle", "",
        "Cycle identity remains GOV-REMEDIATION-PROSPECTIVE-001 / Cycle 1 throughout. Successive Audits and stage attempts did not silently allocate or relabel Cycle 2. Historical correction/assurance before admission remains historical evidence, not retroactively Remediation-coordinated execution.", "",
        "| Finding / boundary | Investigation / decision / disposition | Applied correction and assurance |",
        "|---|---|---|",
        "| Historical GOV-001 | Authorized historical Audit identified executable Work ID ambiguity. Human explicitly admitted it prospectively; fresh strict Investigation confirmed historical issue addressed in current bytes. Corrective decision accepted FINDING ACCEPTED — NO PLAN CHANGE REQUIRED under Corrective 7.2/17. | Original approved P1 applied; original independent Verification/Review PASS retained for historical scope. No reapplication or invented fresh correction. |",
        "| Historical GOV-002 | Extra residual-risk acknowledgement approval-validity condition was historically confirmed; current four source artifacts address it. Same prospective admission/Investigation; no further source change required. | Original approved P2–P5 applied; original independent Verification/Review PASS. Risk disclosure remains; no extra approval-validity acknowledgement gate is imposed. |",
        "| GOV-AUD-20261102-001 | Record-linked clarification resolves interpretation of the strict Investigation report while preserving the original report and previous limitation. | Exact approved 3,438-byte linked attachment published under fresh designation/start; independent Verification PASS followed by separate Review PASS. |",
        "| GOV-AUD-20261102-002 | Remediation optional Commit/Push text had conflicted with immutable final authorization records. | Separately approved one-item replacement in Remediation section 43; separate Application, Verification PASS, Review PASS. No Commit/Push performed. |",
        "| GOV-AUD-20261102-003 | Prior complete Audit INCONSISTENT; canonical Investigation revision 0002 confirmed. Human selected initial-unapproved clarification versus approved-source-update policy before exact proposal. | Four Requirement Update artifacts corrected under approved five-file package; fresh valid Verification PASS then separate Review PASS; final complete Audit assesses current bytes as addressed. |",
        "| GOV-AUD-20261102-004 | Same originating Audit/Investigation; Human selected stage-specific actual/planned actor identity policy before exact proposal. | Corrective Change Request corrected in same approved package; same distinct assurance chain then complete clean Audit. |",
        "| Prior unsuccessful assurance / superseded records | Preserved as unsuccessful history, not rewritten, retroauthorized or substituted for PASS. In particular 20261102T152557Z-efc37bf9-a1dd-4f02-b768-d797e0636818 is not valid Verification. | A separate fresh Human start preceded valid Verification 20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216. Other failed/invalid historical attempts confer no authority. |",
        "| Final complete Audit | 20261102T160240Z-5022506a-f881-4681-af13-e4acf3bb6935: COMPLETED / CONSISTENT, all eight counts zero, no unresolved findings, seven groups PASS. | Current exact source bindings and predecessor closure conditions independently validated here; no resolved finding reopened without current evidence. |", "",
        "The initial source finding Audit, historical CANNOT COMPLETE Audits, the prior INCONSISTENT Audit and earlier paused coordinators remain immutable; this clean current Audit does not rewrite their actual outcomes or erase ordering/reporting limitations.", "",
        "### Canonical history record index", "",
        "The following actor-owned report/result pairs were freshly resolved and fingerprinted. Exact hashes and identities are retained here and in closure evidence; their bodies are not duplicated.", "",
        "| Stage | Canonical report path / SHA-256 | Canonical result path / SHA-256 |", "|---|---|---|"
    ]
    for row in e["history"]:
        rr,jr = row["report"],row["result"]
        lines.append("| " + row["label"] + " | `" + rr["path"] + "` / `" + rr["sha256"] + "` | `" + jr["path"] + "` / `" + jr["sha256"] + "` |")
    lines += [
        "", "The canonical later coordinator uses actual filenames `report-revision-0001.md` / `result-revision-0002.json`; Investigation uses `report-revision-0002.md` / `result-revision-0002.json`. Hyphens and append-only revision lineage are preserved. Earlier canonical records are not overwritten or adopted as current merely by timestamp.", "",
        "## 5. Human decisions and Human approvals", "",
        "| Decision / approval | Actual received authority and scope | Provenance / boundary |", "|---|---|---|",
        "| Governance-root adoption | OWNER decision above adopts governance root only for the identified repository; current fresh starts separately authorize later stages. | Live external GitHub source; not product-root or Master adoption. |",
        "| Prospective cycle admission | Human explicitly admitted historical GOV-001/GOV-002 under this Work ID, prior records historical only, no assumed source changes or criterion waiver. | Actual conversational decision retained in prospective-admission report; no authenticated message ID/time invented. |",
        "| Original exact five-file correction | Exact proposal and one-time actor route approved, followed by separate Application start; original approval-context plus append-only transcription correction retained. | Historical Application records, not reapproval here or retrospective cycle execution. |",
        "| GOV-001/GOV-002 no-further-change decision | Findings accepted; no new correction/Plan change proposed; no new corrective approval was required. | Actual decision report distinguishes absence of a proposed change from approval of past changes. |",
        "| F001 linked clarification | Fresh exact recovery-package approval and one-time publisher redesignation; separate fresh Application retry start. | Exact 3,438-byte payload, new target and assurance route bound in Application records. |",
        "| F002 exact Remediation amendment | Exact report/proposal/patch and section 8 route approved; fresh one-time applier designation; separate Application start. | Application report preserves supplied actual ASCII wording and bindings; not future Commit/Push authorization. |",
        "| F003/F004 policy choice | Initial-unapproved clarification versus approved-update policy and stage-specific future planned-only identities selected BEFORE proposal preparation. | Canonical proposal/investigation and linked actual decision evidence; AI recommendation is not the decision. |",
        "| F003/F004 exact correction approval | Exact canonical report/proposal/patch, all five targets/base/after fingerprints, actor/scope/assurance bindings approved and one-time applier freshly designated. | Actual supplied approval in integrity-bound human-authorization.json; distinct Application start, fresh Verification retry start, Review start and Audit start. |",
        "| This bounded final continuation | Exact fresh Human wording in section 1; one own attempt only. | Not a correction, other-stage start, adoption, Human Acceptance, framework approval or Commit/Push authorization. |", "",
        "No authenticated platform Human IDs/times were exposed for conversational decisions; their actual supplied wording/provenance and scope are preserved by process-owned records. Transcription is not independent creation of approval. No user silence, AI result, prior continuation permission or risk acknowledgement substitutes for a required Human decision.", "",
        "## 6. Corrections applied — historical, not writes by this invocation", "",
        "| File / section | Finding | Exact approved correction |", "|---|---|---|",
        "| docs/ai/request/PORTABILITY_ASSESSMENT_REQUEST.md — Work ID input / executable boundary | GOV-001 | P1: stable reserved Work ID required; unassigned is draft-only and blocks invocation/publication. |",
        "| docs/ai/guidelines/INDEPENDENT_GOVERNANCE_VERIFICATION_GUIDELINES.md — approval-validity/risk boundary | GOV-002 | P2: retain risk disclosure and safeguards without adding Human acknowledgement as approval-validity condition. |",
        "| docs/ai/guidelines/INDEPENDENT_GOVERNANCE_REVIEW_GUIDELINES.md — corresponding boundary | GOV-002 | P3: matching approval/risk alignment. |",
        "| docs/ai/request/INDEPENDENT_GOVERNANCE_VERIFICATION_REQUEST.md — matching approval input | GOV-002 | P4: matching risk-disclosure/non-validity boundary. |",
        "| docs/ai/request/INDEPENDENT_GOVERNANCE_REVIEW_REQUEST.md — matching approval input | GOV-002 | P5: matching risk-disclosure/non-validity boundary. |",
        "| Application-owned attachments/GOV-AUD-20261102-001-linked-clarification.md — entire exact new attachment | GOV-AUD-20261102-001 | Record-only approved linked clarification; originals preserved. |",
        "| .github/agents/sdlc-governance-remediation.agent.md — section 43 Optional Post-Completion Commit item 2 | GOV-AUD-20261102-002 | Immutable original authorization plus new linked post-commit execution evidence; no requirement that a commit contain its own hash; Push remains separately scoped. |",
        "| docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md — approved sequential replacements | GOV-AUD-20261102-003 | Distinguish initial unapproved clarification from approved Requirement update; neither grants approval or premature planning. |",
        "| docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md — matching scope/procedure | GOV-AUD-20261102-003 | Align with the same selected policy. |",
        "| docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md — status/input/clarification context | GOV-AUD-20261102-003 | Same controlled initial-versus-approved input semantics. |",
        "| .github/skills/requirement-update/SKILL.md — matching controlled execution boundary | GOV-AUD-20261102-003 | Same policy; Guideline authority, fresh initiation and human gates retained. |",
        "| docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md — amendment actor/qualification fields | GOV-AUD-20261102-004 | Actual preparer/applier at applicable stages; future verifier/reviewer definitions are planned-only until their separate stage; no impossible pre-existing future attempt/capability prerequisite. |", "",
        "Exact replacement text, section-level byte offsets, before/after hashes, approvals and independent assurance remain in the indexed immutable proposal/Application records. Current-source endpoints match those approved after-states. This continuation applied no correction, no cleanup and no self-definition change.", "",
        "## 7. Independent Verification and separate Independent Governance Review", "",
        "| Correction | Verification | Separately initiated Review after Verification | Later Audit |", "|---|---|---|---|",
        "| Original P1–P5, historical | PASS, original-verification index | PASS, original-review index; historical scope only | Later full Audits retained actual outcomes; current final clean Audit closes current consistency. |",
        "| F001 exact linked clarification | PASS, F001-verification | PASS, F001-review | Complete subsequent Audit chain, including final clean Audit. |",
        "| F002 exact section-43 amendment | PASS, F002-verification | PASS, F002-review: exact d7d84322 attempt, not unsuccessful similarly timed attempt | Complete prior INCONSISTENT Audit retained, later clean Audit assesses current state. |",
        "| F003/F004 approved five-file amendment | Fresh valid PASS, 20261102T153331Z-26be53f2-0644-4e2c-bf65-03760c760216; 13 criteria PASS | Fresh separate PASS, 20261102T154422Z-cdfe6363-b6ac-42d2-8896-979df6f5d322; 12 criteria PASS | Final Audit already existed before this report; 52-core and seven groups clean. |",
        "| No-additional-change decision / this final coordination | No new correction to independently verify | Not applicable: neither stage applies a new correction; historical assurance is not relabelled | Existing final Audit bindings validated, not rerun. |", "",
        "Latest preparer/applier/verifier/reviewer runtime identities are four distinct observed actors: `" + "`, `".join(e["actor_separation"][k] for k in ["proposal","application","verification","review"]) + "`. Their fresh attempts, report/result/evidence and predecessor references remain separate. The Review binds the passing Verification, which binds Application; Audit evidence binds passing Review. Runtime identity attribution is procedural, not external cryptographic identity. Verification and Review have not been combined or replaced by this coordinator's report.", "",
        "## 8. Separate prospective onboarding gates — handoff only", "",
        "**No onboarding process is activated here.** Candidate Master baseline and product persistence root remain unadopted. This AI clean Audit and Remediation COMPLETE are not Human Acceptance, Human governance-framework approval, Master adoption, product readiness or runtime capability.", "",
        "The next prospective Human adoption gate, if the Human chooses to onboard, is TRACEABILITY section 42 **initial adoption of the unchanged inherited exact three-file Master set**, after reviewing this bound clean target-repository Audit. A separate explicit attributable decision must name ScalableParimal/SupportIQ and exact source state, a baseline identity, all three paths and SHA-256 fingerprints below, scope, effective boundary, predecessor status and resolvable Audit evidence. No-change initial adoption does not require inventing an application/amendment of unchanged Masters. Adoption is prospective only and cannot retroactively cure earlier limitations, blocked/inactive/no-further-process or separate referral/no-further-work decisions.", "",
        "| Candidate Master path | Bytes | SHA-256 |", "|---|---:|---|"
    ]
    for s in e["source_inventory"]:
        if s["path"].startswith("docs/ai/sdlc/"):
            lines.append("| `" + s["path"] + "` | " + str(s["bytes"]) + " | `" + s["sha256"] + "` |")
    lines += [
        "", "Independently, TRACEABILITY section 30.1 requires a separate explicit attributable Human decision adopting exact `docs/sdlc-records/product/` for the canonical target repository/state, purpose/scope and actor-owned record scope BEFORE any product-process publication or Portability Assessment. Governance-root adoption or prospective Master adoption does not adopt this root.",
        "Then a separately fresh-Human-started Portability Assessment must establish current source-framework and target-project baselines and its own current capability/record scope. The authorized project Human must explicitly decide each recommended possible blocker with rationale before the first/next affected product SDLC activity. This is not Human Requirement Approval or Human Acceptance.",
        "Any product Orchestrator start or other product process requires its own applicable fresh initiation, current qualification and stage prerequisites. Ordinary Requirement/analysis/verification/approval, Plan/review/approval, implementation/assurance/acceptance gates remain. No automatic Portability, Orchestrator, product start, source migration, alarm activation, staging, Commit or Push follows.",
        "Optional post-completion Commit/Push remains unperformed and would require separate exact Human Acceptance and immutable Commit/Push authorization records under the current section 43; neither is supplied or inferred here. Baseline adoption is not either of those gates.", "",
        "## 9. Evidence, limitations and stop", ""
    ]
    for title,p in [
        ("Own invocation",OWN/"attempt.json"),
        ("Complete hidden-inclusive input manifest",OWN/"evidence/input-manifest.json"),
        ("Independent invocation readback",OWN/"evidence/invocation-readback.json"),
        ("Closure evidence",OWN/"evidence/closure-evidence.json")
    ]:
        x = ref(p)
        lines.append("- " + title + ": `" + x["path"] + "`, SHA-256 `" + x["sha256"] + "`.")
    lines += ["", "Evidence classification: EXECUTED current-byte/hash/native-object/reference/input-pathset/Git comparisons; SOURCE INSPECTION of current governing closure contracts and relevant process-owned reports; REPORTED assurance conclusions retained as those actors' conclusions. This coordination is not independent re-performance of their tests or a complete re-Audit.", ""]
    lines.extend("- " + x for x in LIMITS)
    lines += [
        "", "No actual prerequisite gap remains for bounded Remediation closure. Separate prospective adoption/onboarding/acceptance decisions are not retroactively added as closure prerequisites. If any final publication/readback fails, durable completion must not be inferred; stop progression and surface the exact failure.",
        "Canonical own terminal result path: `" + (OWN/"result.json").as_posix() + "`, identity `" + ATTEMPT + ":remediation_result`; it is later than this immutable report, so no future fingerprint is claimed.",
        "Non-authoritative downstream presentation handoff: `" + (OWN/"handoff.md").as_posix() + "`; prepared only after the actual result exists, then bound by the final readback checkpoint.",
        "**Final Audit confirmation:** the complete 52-artifact scope (3 Masters, 10 Guidelines, 10 Prompts, 10 Requests, 10 Skills, 9 Agents) and all seven separate same-framework groups reached CONSISTENT with all eight counts zero and no unresolved findings. This report anchors that actual result. **Governance Remediation COMPLETE. STOP; no later stage is started.**", ""
    ]
    text = "\n".join(lines)
    assert text.startswith("# FINAL GOVERNANCE STATUS")
    for section in ["Human decisions","Corrections applied","Independent Verification","Separate prospective","Remediation history","Final Audit confirmation"]:
        assert section in text
    # Do not mistake Markdown code spans such as `result.json` for a literal
    # PowerShell newline escape. Reject actual unpaired backtick escape tokens.
    prose = re.sub(r"`[^`\n]+`", "", text)
    assert "`n" not in prose and "`r" not in prose
    rr = publish("report.md",text)
    print(json.dumps({"report":rr,"next":"Fresh-process report/evidence readback before result"},indent=2))

if __name__ == "__main__":
    if sys.argv[1] == "preflight":
        preflight()
    elif sys.argv[1] == "assess":
        assess()
    elif sys.argv[1] == "report":
        report()
