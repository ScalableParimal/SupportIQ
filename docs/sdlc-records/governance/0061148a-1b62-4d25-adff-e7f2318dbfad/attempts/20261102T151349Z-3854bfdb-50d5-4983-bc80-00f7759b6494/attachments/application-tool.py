"""Actor-owned byte-aware approved application tool. No source writes in qualify/readback/preflight."""
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ")
WORK = "0061148a-1b62-4d25-adff-e7f2318dbfad"
ATTEMPT = "20261102T151349Z-3854bfdb-50d5-4983-bc80-00f7759b6494"
PREFIX = f"docs/sdlc-records/governance/{WORK}/attempts/"
OWN = PREFIX + ATTEMPT
PROPOSER = PREFIX + "20261102T145538Z-5b4cd1da-23f1-42d9-9f69-583b085dd79d"
AGENT = "ec7a8339-a9b5-4710-bb5b-a8760309005d"
ROLE = ".github/agents/governance-amendment-application.agent.md"
APPROVAL = "I approve the identified canonical report, exact proposal and patch with all five target fingerprints, scope, actor and assurance bindings; freshly designate the proposed one-time applier under that route; do not start Application"
START = "Yes, initiate only the scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004 under the approved five-file package"
PACKAGE = {
    "report.md": (39577, "A925ECCE1D7593DE1955EC0CA416A1BDFD1AA67A5B1800129BF8FA3C1B685677"),
    "result.json": (11450, "A4BEE48991E0CA74D414BDDA1957220F0703E1FEF7F62AE50536E9EDB6A725ED"),
    "attachments/exact-proposal.json": (21495, "086D48C77EC7D6C052615498DC82B380493B2C0610F9AAF070D1FFF08580D29C"),
    "attachments/minimal.patch": (13651, "DFE0F97EE5EC19D0194E6FFB9FC2C3CD5104F41B9B9DCA908837556E1E99F1DD"),
    "evidence/decision-evidence.json": (26178, "CD52373E75FF07654FCB496645F83F38ED96B612C5C3652882C329430B5B0A46"),
    "checkpoint-0002.json": (5065, "55ECCAAEB08772A4DBEA215EA59485F3EF9B552FE811A08E96D81A8034B2AB50"),
}
TARGETS = [
    "docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md",
    "docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md",
    "docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md",
    ".github/skills/requirement-update/SKILL.md",
    "docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md",
]
MASTER = {
    "docs/ai/sdlc/SDLC_GOVERNANCE.md": "79A3F15E5032AC1AB018B74DCEE772801E6F0AA883CA67BD51D64EF5ECA25A8B",
    "docs/ai/sdlc/SDLC_ARTIFACT_GOVERNANCE.md": "6CD023559372065329EFCAE6481345663887B9EC01F7A5E884962A1D74DCD860",
    "docs/ai/sdlc/SDLC_TRACEABILITY_AND_CHANGE_CONTROL.md": "08F33FFDB36D875AC05CD15362CDCCC119CFD63FB40D44D21E761C364A23AC7C",
}

def check(ok, text):
    if not ok:
        raise RuntimeError(text)

def sha(b):
    return hashlib.sha256(b).hexdigest().upper()

def path(p):
    q = ROOT / p
    check(q.resolve().is_relative_to(ROOT.resolve()), "Outside repository: " + p)
    for x in [q] + list(q.parents):
        if x == ROOT.parent:
            break
        check(not x.is_symlink() and not x.is_junction(), "Link/reparse path: " + str(x))
    return q

def ref(p):
    b = path(p).read_bytes()
    return {"path": p, "bytes": len(b), "sha256": sha(b)}

def bound(r):
    a = ref(r["path"])
    check(all(a[k] == r[k] for k in ("bytes", "sha256")), "Binding mismatch: " + r["path"])
    return a

def nodup(pairs):
    d = {}
    for k, v in pairs:
        check(k not in d, "Duplicate JSON key")
        d[k] = v
    return d

def parse(b):
    return json.loads(b.decode("utf-8"), object_pairs_hook=nodup,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def serial(obj):
    b = (json.dumps(obj, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")
    check(parse(b) == obj, "Strict JSON roundtrip failed")
    check(b"`n" not in b, "Literal backtick-n artifact")
    return b

def load(p):
    return parse(path(p).read_bytes())

def meta(kind, **kwargs):
    return dict(schema_version="1.0", record_type=kind, record_id=ATTEMPT + ":" + kind,
                work_id=WORK, attempt_id=ATTEMPT, cycle_id="GOV-REMEDIATION-PROSPECTIVE-001",
                cycle=1, process="Governance Amendment Application",
                creator={"role": "Governance Amendment Application", "runtime_agent_id": AGENT},
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                clock_basis="UTC record preparation, not exact publication time", **kwargs)

def publish_bytes(p, b, obj=None):
    check(p.startswith(OWN + "/"), "Publication outside own attempt")
    q = path(p)
    tmp = path(p + ".partial")
    check(not q.exists() and not tmp.exists(), "No-overwrite collision: " + p)
    if obj is not None:
        check(parse(b) == obj, "Publication object incomplete")
    q.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("xb") as f:
        check(f.write(b) == len(b), "Partial record write")
        f.flush()
        os.fsync(f.fileno())
    check(tmp.read_bytes() == b, "Partial readback mismatch")
    check(os.name == "nt", "Atomic no-overwrite rename relies on Windows semantics")
    os.rename(tmp, q)
    check(q.read_bytes() == b, "Published readback mismatch")
    return ref(p)

def publish(name, obj):
    return publish_bytes(OWN + "/" + name, serial(obj), obj)

def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT)

def gitstate():
    raw = git("status", "--porcelain=v1", "--untracked-files=all", "-z")
    # There are no renames in this source state. Preserve full status except this own scope.
    entries = [s for s in raw.decode("utf-8").split("\0") if s]
    check(not any(s[:2].strip() in ("R", "C") for s in entries), "Rename/copy needs explicit parser")
    return {"head": git("rev-parse", "HEAD").decode().strip(),
            "branch": git("branch", "--show-current").decode().strip(),
            "origin": git("remote", "get-url", "origin").decode().strip(),
            "status_excluding_own_attempt": [s for s in entries if not s[3:].startswith(OWN + "/")],
            "index": {"bytes": len((ROOT / ".git/index").read_bytes()),
                      "sha256": sha((ROOT / ".git/index").read_bytes())}}

def inventory():
    rows = []
    for base, dirs, files in os.walk(ROOT):
        rel = Path(base).relative_to(ROOT).as_posix()
        dirs[:] = sorted(d for d in dirs if not (rel == "." and d == ".git")
                         and (Path(base) / d).relative_to(ROOT).as_posix() != OWN)
        for d in dirs:
            path((Path(base) / d).relative_to(ROOT).as_posix())
        for f in sorted(files):
            p = (Path(base) / f).relative_to(ROOT).as_posix()
            rows.append(ref(p))
    return sorted(rows, key=lambda x: x["path"])

def compare_manifest(before, allowed=()):
    actual = inventory()
    old = {r["path"]: r for r in before}
    new = {r["path"]: r for r in actual}
    changed = sorted(k for k in old.keys() | new.keys() if old.get(k) != new.get(k))
    check(not set(changed) - set(allowed), "Unexpected repository changes: " + repr(changed))
    return actual, changed

def reconstruct(b, t):
    check(len(b) == t["base_bytes"] and sha(b) == t["base_sha256"], "Base mismatch " + t["path"])
    check(b.decode("utf-8").encode("utf-8") == b and not b.startswith(b"\xef\xbb\xbf"), "Encoding")
    check(b.replace(b"\r\n", b"").find(b"\n") < 0 and b.replace(b"\r\n", b"").find(b"\r") < 0, "EOL")
    check(b.endswith(b"\r\n") == t["base_final_newline"], "Base EOF")
    original = b
    offsets = []
    for r in t["replacements"]:
        a, c = r["before"].encode("utf-8"), r["after"].encode("utf-8")
        check(r["expected_occurrences"] == 1 and b.count(a) == 1, "Replacement cardinality")
        check(b.index(a) == r["sequential_input_byte_offset"], "Replacement offset")
        offsets.append(b.index(a))
        b = b.replace(a, c, 1)
    check(len(b) == t["expected_after_bytes"] and sha(b) == t["expected_after_sha256"], "After mismatch")
    check(not b.startswith(b"\xef\xbb\xbf") and b.decode("utf-8").encode("utf-8") == b, "After encoding")
    check(b.replace(b"\r\n", b"").find(b"\n") < 0 and b.replace(b"\r\n", b"").find(b"\r") < 0, "After EOL")
    check(b.endswith(b"\r\n") == t["expected_after_final_newline"], "After EOF")
    reverse = b
    for r in reversed(t["replacements"]):
        a, c = r["before"].encode("utf-8"), r["after"].encode("utf-8")
        check(reverse.count(c) == 1, "Reverse cardinality")
        reverse = reverse.replace(c, a, 1)
    check(reverse == original, "Other-byte preservation")
    return b, offsets

def selftest():
    o = {"quotes": [APPROVAL, START, "'ASCII'", "\r\n", "\u2014"], "null": None,
         "bool": True, "integer": 7, "list": [{"nested": "complete"}]}
    check(parse(serial(o)) == o, "Native object selftest")
    for invalid in [b'{"x":1,"x":2}', b'{"x":NaN}']:
        try:
            parse(invalid)
        except (RuntimeError, ValueError):
            pass
        else:
            raise RuntimeError("Strict JSON negative selftest")
    b, a = b"old\r\n", b"new\r\n"
    t = dict(path="synthetic", base_bytes=len(b), base_sha256=sha(b),
             expected_after_bytes=len(a), expected_after_sha256=sha(a),
             base_final_newline=True, expected_after_final_newline=True,
             replacements=[dict(before="old", after="new", expected_occurrences=1, sequential_input_byte_offset=0)])
    check(reconstruct(b, t)[0] == a, "Byte helper positive selftest")
    try:
        reconstruct(b"bad\r\n", t)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("Byte helper negative selftest")
    return "PASS: native JSON full-object equality, duplicate/nonfinite rejection, lossless quotes/CRLF, byte reconstruction/reversal and wrong-base rejection"

def package():
    rows = []
    for name, (size, digest) in PACKAGE.items():
        rows.append(bound({"path": PROPOSER + "/" + name, "bytes": size, "sha256": digest}))
    return rows

def actors(proposal):
    rows = []
    for a in proposal["actors"]:
        rows.append({"role": a["role"], "definition": bound(a["definition"]),
                     "binding_state": a["binding_state"]})
        if a["role"] == "proposal_preparer":
            bound(a["attempt"])
    check(len({x["definition"]["path"] for x in rows}) == 4, "Actor path separation")
    check(len({x["definition"]["sha256"] for x in rows}) == 4, "Actor hash separation")
    applier = next(x for x in rows if x["role"] == "intended_one_time_applier")
    check(applier["definition"]["path"] == ROLE, "Wrong applier role")
    exclusions = [ref(".github/agents/" + n + ".agent.md")
                  for n in ("sdlc-process-orchestrator", "sdlc-governance-remediation")]
    check(all(x["path"] != ROLE and x["sha256"] != applier["definition"]["sha256"] for x in exclusions),
          "Excluded actor reused")
    return rows, exclusions

def permissions():
    ps = r"""
$ErrorActionPreference='Stop'
$paths=@('.') + @('docs/ai/guidelines/REQUIREMENT_UPDATE_GUIDELINES.md','docs/ai/prompts/REQUIREMENT_UPDATE_PROMPT.md','docs/ai/request/REQUIREMENT_UPDATE_REQUEST.md','.github/skills/requirement-update/SKILL.md','docs/ai/request/CORRECTIVE_CHANGE_REQUEST.md','docs/sdlc-records/governance/0061148a-1b62-4d25-adff-e7f2318dbfad/attempts')
$rows=@(foreach($p in $paths) { $a=Get-Acl -LiteralPath $p; [pscustomobject]@{path=$p;owner=$a.Owner;access=$a.AccessToString;rules=@($a.Access | ForEach-Object { [pscustomobject]@{identity=$_.IdentityReference.Value;rights=$_.FileSystemRights.ToString();type=$_.AccessControlType.ToString();inherited=$_.IsInherited} })} })
[pscustomobject]@{principal=[System.Security.Principal.WindowsIdentity]::GetCurrent().Name;rows=$rows} | ConvertTo-Json -Depth 8 -Compress
"""
    out = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps], cwd=ROOT)
    obj = parse(out.decode("utf-8-sig").encode("utf-8"))
    for r in obj["rows"]:
        check(not any(x["type"] == "Deny" for x in r["rules"]), "Deny ACL requires further effective-access qualification")
        check(any(x["identity"] == "NT AUTHORITY\\Authenticated Users" and "Modify" in x["rights"]
                  and x["type"] == "Allow" for x in r["rules"]), "Modify permission not evidenced")
    for p in TARGETS:
        q = path(p)
        check(os.access(q, os.R_OK | os.W_OK) and not (q.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY),
              "Nonmutating access/readonly check failed: " + p)
    return obj

def qualify():
    tests = selftest()
    check(os.environ.get("COPILOT_AGENT_SESSION_ID") == "be2dfb00-d72f-4390-97fb-535d6712c314", "Invocation changed")
    pk = package()
    pr = load(PROPOSER + "/attachments/exact-proposal.json")
    ar, ex = actors(pr)
    for p, h in MASTER.items():
        check(ref(p)["sha256"] == h, "Governance-root Master binding changed")
    g = gitstate()
    check(g["head"] == "57ed3afe8a14a41bdbe38d4df621a99c836a0f4c", "Unexpected HEAD")
    check("ScalableParimal/SupportIQ" in g["origin"], "Wrong origin")
    perm = permissions()
    manifest = publish("evidence/input-manifest.json", meta("input_manifest", files=inventory(),
        exclusions=[".git internals (HEAD/index/status separately bound)", OWN],
        includes_hidden=True, inventory_not_substantive_read=True))
    human = publish("evidence/human-authorization.json", meta("supplied_human_authorization",
        source="Actual Human decisions in parent conversation explicitly supplied in current user request for transcription",
        authenticated_message_id=None, authenticated_author_id=None, original_decision_time=None,
        approval_exact_ascii=APPROVAL, separate_stage_start_exact_ascii=START,
        current_request="Execute ONLY approved scoped Governance Amendment Application for GOV-AUD-20261102-003 and GOV-AUD-20261102-004",
        package=pk, target_bindings=pr["targets"], actors=pr["actors"],
        approval_route=pr["approval_route"], byte_contract=pr["byte_contract"],
        approval_effect="Fresh exact approval and one-time scoped designation; separate fresh start; not historical authority",
        exclusions=["Masters", "product work", "historical edits", "other actors' records", "staging", "commit", "push",
                    "adoption", "Verification", "Review", "Audit"],
        unavailable_attribution="No authenticated Human message ID/time exposed; none invented",
        scope="Five-file combined exact package; all bases required before first source write"))
    root = dict(url="https://github.com/ScalableParimal/SupportIQ/issues/3#issuecomment-6522916236",
        author="ScalableParimal", author_id=226102895, association="OWNER",
        created_at="2026-10-30T12:31:51Z", updated_at="2026-10-30T12:31:51Z",
        observed_source="Fresh github-mcp-server-issue_read get_comments during current invocation",
        repository="ScalableParimal/SupportIQ", head=g["head"], work_id=WORK,
        adopted_root="docs/sdlc-records/governance/", master_fingerprints=MASTER,
        authority_limit="Root adoption retained; initial bootstrap Audit start NOT reused. Current normal finding-led non-Master continuation under SDLC_GOVERNANCE section 3 and fresh supplied decisions.",
        product_root="UNADOPTED", master_baseline="UNADOPTED_CANDIDATE")
    inv = meta("invocation", state="QUALIFIED_PENDING_INDEPENDENT_READBACK_BEFORE_SUBSTANTIVE_COMPARISON",
        repository=g, input_manifest=manifest, human_authorization=human, package=pk,
        actor_definitions=ar, excluded_applier_definitions=ex,
        preparer_attempt=pr["actors"][0]["attempt"],
        own_actor_attempt=OWN + "/attempt.json",
        runtime=dict(runtime_agent_id=AGENT,
            runtime_agent_id_basis="Current all-scope registry: sole running assigned Governance Amendment Application actor; not a competing writer. Current role assignment plus definition hash establishes role, not display title.",
            host_session="ahp-session:/3b5a7ec7-0668-474f-be38-020f06af1c60",
            copilot_agent_session_id=os.environ["COPILOT_AGENT_SESSION_ID"],
            python=sys.version, python_executable=sys.executable, principal=perm["principal"]),
        permissions=perm, capabilities=dict(
            read_hash_checks="Observed package/actor/Master reads and SHA-256; complete hidden-inclusive manifest; Git status/index/HEAD; lossless byte helper selftests",
            exact_target_write="Current powershell Python byte I/O available; target and inherited ACL Authenticated Users Modify with no Deny; os.access R_OK/W_OK and no readonly attribute on every exact approved target. No source write probe.",
            readback="Observed independent filesystem reads/hashes; separate fresh invocation readback next",
            own_publication="Validated native object -> UTF-8 .partial xb -> flush fsync -> readback -> Windows atomic rename no overwrite -> readback; own manifest and supplied authorization already published",
            permission_boundary="Procedural exact allowlist, not sandbox-enforced; never probe unapproved paths"),
        selftests=tests, root_authority=root, output_scope=OWN,
        source_write_allowlist=TARGETS,
        governing_inputs=[ref(p) for p in [
            ROLE, ".github/skills/governance-amendment-application/SKILL.md",
            "docs/ai/guidelines/GOVERNANCE_AMENDMENT_APPLICATION_GUIDELINES.md",
            "docs/ai/prompts/GOVERNANCE_AMENDMENT_APPLICATION_PROMPT.md",
            "docs/ai/request/GOVERNANCE_AMENDMENT_APPLICATION_REQUEST.md", *MASTER]],
        assurance_bindings="Verifier/reviewer planned identity-only; no attempts, runtime qualification or stage starts created",
        concurrency="Only current assigned actor running in observed registry; idle historical actors not treated as competing writers; no exhaustive OS-wide liveness proof",
        limitations=["Procedural source-write restriction, not technical isolation", "Endpoint hashes cannot exclude transient mutation/reversion or same-principal tampering",
                    "No exhaustive trusted event log", "UTC preparation times are not exact publication timestamps",
                    "Human authentication metadata/time unavailable; supplied wording preserved"])
    r = publish("attempt.json", inv)
    print(json.dumps({"invocation": r, "manifest": manifest, "authorization": human, "selftests": tests}))

def readback():
    # Fresh process/call, independently re-open every integrity-bound input and published record.
    i = load(OWN + "/attempt.json")
    bound(i["input_manifest"])
    bound(i["human_authorization"])
    for r in i["package"] + i["governing_inputs"]:
        bound(r)
    ar, ex = actors(load(PROPOSER + "/attachments/exact-proposal.json"))
    check(ar == i["actor_definitions"] and ex == i["excluded_applier_definitions"], "Actor changed")
    compare_manifest(load(i["input_manifest"]["path"])["files"])
    check(gitstate() == i["repository"], "Git changed during invocation qualification")
    r = publish("checkpoint-0001.json", meta("invocation_independent_readback",
        outcome="PASS", invocation=ref(OWN + "/attempt.json"), manifest=i["input_manifest"],
        checked_input_count=len(load(i["input_manifest"]["path"])["files"]),
        ordering="Fresh separate tool call/process after attempt publication; before substantive comparison/application"))
    print(json.dumps(r))

def preflight():
    i = load(OWN + "/attempt.json")
    cp = load(OWN + "/checkpoint-0001.json")
    check(cp["outcome"] == "PASS", "Invocation not read back")
    bound(cp["invocation"])
    package()
    p = load(PROPOSER + "/attachments/exact-proposal.json")
    actors(p)
    check([t["path"] for t in p["targets"]] == TARGETS, "Exact five targets differ")
    check(p["work_id"] == WORK and p["cycle"] == 1 and p["no_master_change"] and p["no_product_change"], "Scope")
    h = load(i["human_authorization"]["path"])
    check(h["approval_exact_ascii"] == APPROVAL and h["separate_stage_start_exact_ascii"] == START, "Human bindings")
    check(h["target_bindings"] == p["targets"] and h["actors"] == p["actors"], "Approval target/actor binding")
    check(h["approval_route"] == p["approval_route"] and h["byte_contract"] == p["byte_contract"], "Approval route/byte contract")
    permissions()
    compare_manifest(load(i["input_manifest"]["path"])["files"])
    check(gitstate() == i["repository"], "Git mismatch")
    rows, diffs = [], []
    for t in p["targets"]:
        check(t["encoding"] == "UTF-8" and not t["bom"] and t["newline"] == "CRLF", "Contract")
        b = path(t["path"]).read_bytes()
        a, offsets = reconstruct(b, t)
        diffs.extend(difflib.unified_diff(b.decode("utf-8").splitlines(keepends=True),
            a.decode("utf-8").splitlines(keepends=True), fromfile="a/" + t["path"], tofile="b/" + t["path"]))
        rows.append({"path": t["path"], "before": ref(t["path"]),
            "reconstructed_after": {"bytes": len(a), "sha256": sha(a)},
            "sequential_offsets": offsets, "encoding": "UTF-8", "bom": False, "newline": "CRLF",
            "final_newline": a.endswith(b"\r\n"), "reverse_to_exact_base": True})
    patch = "".join(diffs).encode("utf-8")
    check(patch == path(PROPOSER + "/attachments/minimal.patch").read_bytes(), "Native patch not exact reconstructed minimal diff")
    # Bind every repository-relative bytes/hash object in canonical proposal/report result/evidence/checkpoint.
    checked, seen = [], set()
    def walk(v):
        if isinstance(v, dict):
            if isinstance(v.get("path"), str) and "bytes" in v and "sha256" in v:
                rp = v["path"]
                if rp.startswith(("docs/", ".github/")) and rp not in seen:
                    check(isinstance(v["bytes"], int), "Nonnumeric bound size")
                    checked.append(bound(v)); seen.add(rp)
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    for n in ("attachments/exact-proposal.json", "result.json", "evidence/decision-evidence.json", "checkpoint-0002.json"):
        walk(load(PROPOSER + "/" + n))
    r = publish("evidence/preflight.json", meta("all_target_preflight", outcome="PASS",
        invocation=ref(OWN + "/attempt.json"), invocation_readback=ref(OWN + "/checkpoint-0001.json"),
        human_authorization=ref(i["human_authorization"]["path"]), package=package(),
        all_five_before_any_write=True, targets=rows, patch_bytes=len(patch), patch_sha256=sha(patch),
        nested_bound_inputs_checked=checked, selftests=selftest(), all_other_inputs_unchanged=True,
        scope_exclusions_validated=True, actor_separation_validated=True,
        interpretation="Exact approved bytes only; proposal preparation exclusions do not forbid this separately approved Application. No downstream stage."))
    print(json.dumps(r))

def apply():
    i = load(OWN + "/attempt.json")
    pf = load(OWN + "/evidence/preflight.json")
    check(pf["outcome"] == "PASS" and pf["all_five_before_any_write"], "Preflight missing")
    package()
    p = load(PROPOSER + "/attachments/exact-proposal.json")
    actors(p)
    bound(pf["invocation"]); bound(pf["invocation_readback"]); bound(pf["human_authorization"])
    permissions()
    compare_manifest(load(i["input_manifest"]["path"])["files"])
    check(gitstate() == i["repository"], "Pre-write Git mismatch")
    prepared = [(t, path(t["path"]).read_bytes()) for t in p["targets"]]
    afters = [(t, b, reconstruct(b, t)[0]) for t, b in prepared]
    check([t["path"] for t, b, a in afters] == TARGETS, "Write allowlist")
    results, error = [], None
    try:
        for t, before, after in afters:
            q = path(t["path"])
            check(q.read_bytes() == before, "Immediate target base changed: " + t["path"])
            # Approved byte-aware application, not text/editor normalization.
            with q.open("r+b") as f:
                check(f.read() == before, "Open-handle base mismatch")
                f.seek(0)
                check(f.write(after) == len(after), "Short approved byte write")
                f.truncate(len(after))
                f.flush()
                os.fsync(f.fileno())
            actual = ref(t["path"])
            check(actual["bytes"] == len(after) and actual["sha256"] == sha(after), "Target readback mismatch")
            check(q.read_bytes() == after, "Complete target byte readback")
            results.append({"path": t["path"], "before": {"bytes": len(before), "sha256": sha(before)},
                            "after": actual, "exact_reconstruction_readback": True,
                            "encoding": "UTF-8", "bom": False, "newline": "CRLF",
                            "final_newline": after.endswith(b"\r\n")})
    except Exception as e:
        error = type(e).__name__ + ": " + str(e)
    # If any runtime failure, preserve actual partial state; never rollback or continue writes.
    actuals = [ref(t) for t in TARGETS]
    preservation_error = None
    try:
        final_inventory, changed = compare_manifest(load(i["input_manifest"]["path"])["files"], TARGETS)
        final_git = gitstate()
        check(all(final_git[k] == i["repository"][k] for k in ("head", "branch", "origin", "index")), "Git identity/index changed")
        check(set(changed) == set(x["path"] for x in results) if error else set(changed) == set(TARGETS), "Unexpected changed targets")
    except Exception as e:
        preservation_error = str(e)
        final_inventory, changed, final_git = inventory(), None, gitstate()
    outcome = "COMPLETED" if error is None and preservation_error is None and len(results) == 5 else "CANNOT COMPLETE"
    evidence = publish("evidence/application-evidence.json", meta("application_evidence", outcome=outcome,
        invocation=ref(OWN + "/attempt.json"), preflight=ref(OWN + "/evidence/preflight.json"),
        operations=results, actual_targets=actuals, error=error, preservation_error=preservation_error,
        actual_changed_paths=changed, final_repository=final_git, non_target_endpoint_preservation=preservation_error is None,
        final_inventory=final_inventory, rollback_performed=False,
        helper=ref(OWN + "/attachments/application-tool.py"),
        semantics="Applier post-write identity/hash/readback only; not independent Verification/Review/Audit",
        limitations=i["limitations"]))
    lines = ["# Governance Amendment Application Report", "",
        f"Work ID: `{WORK}`; Cycle GOV-REMEDIATION-PROSPECTIVE-001 / 1; attempt `{ATTEMPT}`.",
        f"Outcome: **{outcome}**. Findings: GOV-AUD-20261102-003 and GOV-AUD-20261102-004.",
        "", "## Authority, current identity and invocation ordering",
        f"Fresh scoped one-time applier: `{ROLE}`, SHA-256 `{ref(ROLE)['sha256']}`.",
        f"Current runtime agent `{AGENT}`, host `{i['runtime']['host_session']}`, Copilot invocation `{i['runtime']['copilot_agent_session_id']}`, principal `{i['runtime']['principal']}`.",
        "Current assignment plus hashed role establishes identity; host session title is not role proof. Current registry showed only this actor running; idle historical actors were not competing writers.",
        "Preparer owns the approved proposal attempt. All four definition paths/hashes are distinct. Applier also differs from excluded Orchestrator and Governance Remediation definitions. Verifier/reviewer remain planned identity-only, with no future attempts or capability claims.",
        f"Fresh Human exact approval/designation (ASCII wording): '{APPROVAL}'",
        f"Separate actual Human stage-start (ASCII wording): '{START}'",
        "Source: actual parent-conversation Human decisions explicitly supplied in this invocation. Authenticated message/author IDs and original decision time are unavailable and not invented.",
        f"Exact bindings and exclusions: `{i['human_authorization']['path']}`, SHA-256 `{i['human_authorization']['sha256']}`.",
        "Root adoption freshly resolved through GitHub OWNER issue comment 6522916236; initial bootstrap Audit authority was not reused. Normal finding-led non-Master continuation under Governance section 3 plus current exact approval/start authorizes only this stage. Product root and candidate Master baseline remain unadopted. Product Requirement/Plan: N/A.",
        f"Invocation `{OWN}/attempt.json`, SHA-256 `{ref(OWN + '/attempt.json')['sha256']}`, was validated, flushed, atomically published without overwrite, and independently reopened in a fresh separate call before substantive comparison/application.",
        f"Independent invocation readback: `{OWN}/checkpoint-0001.json`, SHA-256 `{ref(OWN + '/checkpoint-0001.json')['sha256']}`.",
        "Current ACLs, R_OK/W_OK, file attributes, tool/runtime evidence, hidden-inclusive inventory and strict JSON/byte selftests establish capability without a source-write probe. Publication used validated .partial, fsync, atomic same-filesystem Windows no-overwrite rename and readback.",
        "", "## Exact package and preflight",
        f"Canonical approved proposal preparer report: `{PROPOSER}/report.md`, SHA-256 `{PACKAGE['report.md'][1]}`.",
        f"Proposal: `{PROPOSER}/attachments/exact-proposal.json`, SHA-256 `{PACKAGE['attachments/exact-proposal.json'][1]}`.",
        f"Patch: `{PROPOSER}/attachments/minimal.patch`, SHA-256 `{PACKAGE['attachments/minimal.patch'][1]}`.",
        "All six supplied package fingerprints and nested relied bindings were recomputed. The full approved report/proposal, actor bindings, route, exclusions and byte contract were read. Exact supplied approval/designation binds the same package, five targets, base/after fingerprints, byte properties, actors and assurance route.",
        f"Preflight: `{OWN}/evidence/preflight.json`, SHA-256 `{ref(OWN + '/evidence/preflight.json')['sha256']}`.",
        "All five bases and complete sequential single-occurrence UTF-8 byte reconstructions were validated before the first source write. Every sequential byte offset matched; reverse replacements recovered each exact base. The reconstructed native unified diff exactly equalled the approved patch bytes. All five bases were rechecked as one set immediately before application; each open handle rechecked its base.",
        "", "## Actual application", "",
        "| Target | Before bytes / SHA-256 | Actual after bytes / SHA-256 | Readback |",
        "|---|---|---|---|"]
    for r in results:
        lines.append(f"| `{r['path']}` | {r['before']['bytes']} / `{r['before']['sha256']}` | {r['after']['bytes']} / `{r['after']['sha256']}` | exact PASS |")
    lines += ["", "All successful writes used the approved sequential byte replacements only; UTF-8 no BOM, CRLF and final-newline states preserved (first four absent, fifth present). All other bytes in each target equal the reconstruction; no reformatting or cleanup.",
        f"Actual runtime error: {error!r}; preservation error: {preservation_error!r}. No rollback performed. Full actual state, including all five targets, is bound in evidence.",
        "", "## Preservation, evidence and limitations",
        f"Evidence: `{evidence['path']}`, SHA-256 `{evidence['sha256']}`.",
        f"Complete input manifest: `{i['input_manifest']['path']}`, SHA-256 `{i['input_manifest']['sha256']}`.",
        "Inventory includes hidden .github and all existing repository files/records; .git internals and this own attempt excluded. Inventory is not a claim of substantive reading of every file. Git HEAD, branch, origin and index were checked separately. Endpoint inventory confirms only the five approved targets changed outside this own attempt; pre-existing modifications and historical records are preserved.",
        "No other source/stage, Master, product, historical or other-actor record change; no staging, commit, push or adoption. Current endpoint evidence cannot establish continuous absence of mutation/reversion or exclude same-principal tampering. Restrictions are procedural, not enforced sandbox isolation. No exhaustive trusted event log or OS-wide liveness proof. Exact publication timestamps not captured; UTC preparation times are not publication times.",
        "", "## Handoff and stop",
        "Application completion is only exact authorized-byte application, not independent Verification, Review, Audit, effectiveness, closure or baseline adoption. Both findings remain accepted, not closed. Prior resolved findings were not reopened. Latest complete Audit 20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f remains reported INCONSISTENT until a new full Audit.",
        "Next permitted gate only after complete successful Application: separate fresh Human Verification stage-start for the planned distinct independent verifier. It must match the approved definition path/hash, publish/read back its own fresh invocation, and establish current qualification then. Review requires passing independent Verification plus a separate fresh start; complete Audit follows passing Review plus its own fresh start. Residual-risk disclosure remains mandatory; no later stage is started here.",
        f"Result is published after this report at `{OWN}/result.json` and binds final report/evidence bytes. Terminal fresh readback checkpoint follows. STOP."]
    report = publish_bytes(OWN + "/report.md", ("\n".join(lines) + "\n").encode("utf-8"))
    result = publish("result.json", meta("application_result", outcome=outcome,
        report=report, evidence=evidence, invocation=ref(OWN + "/attempt.json"),
        invocation_readback=ref(OWN + "/checkpoint-0001.json"), preflight=ref(OWN + "/evidence/preflight.json"),
        human_authorization=i["human_authorization"], input_manifest=i["input_manifest"],
        package=package(), actors=i["actor_definitions"], applier_exclusions=i["excluded_applier_definitions"],
        targets=results, actual_targets=actuals, errors=[error, preservation_error],
        finding_dispositions={f"GOV-AUD-20261102-00{x}": "ACCEPTED_NOT_CLOSED_PENDING_INDEPENDENT_ASSURANCE_AND_FULL_AUDIT" for x in (3, 4)},
        next_gate="Separate fresh Human independent Verification start" if outcome == "COMPLETED" else "STOP: reconcile actual partial/failure state under governance",
        downstream_started=False, effectiveness_claimed=False, adopted=False))
    print(json.dumps({"outcome": outcome, "report": report, "result": result, "evidence": evidence}))

def terminal():
    r = load(OWN + "/result.json")
    for k in ("report", "evidence", "invocation", "invocation_readback", "preflight", "human_authorization", "input_manifest"):
        bound(r[k])
    e = load(r["evidence"]["path"])
    compare_manifest(e["final_inventory"])
    check(gitstate() == e["final_repository"], "Final readback Git state changed")
    for a in e["actual_targets"]:
        bound(a)
    check(r["outcome"] == "COMPLETED", "Failure outcome; do not publish success checkpoint")
    p = load(PROPOSER + "/attachments/exact-proposal.json")
    for t in p["targets"]:
        bound({"path": t["path"], "bytes": t["expected_after_bytes"], "sha256": t["expected_after_sha256"]})
    cp = publish("checkpoint-0002.json", meta("terminal_independent_readback", outcome="PASS",
        result=ref(OWN + "/result.json"), report=r["report"], evidence=r["evidence"],
        exact_five_after_validated=True, all_non_target_inputs_unchanged=True,
        repository=e["final_repository"], own_final_records=[ref(q.relative_to(ROOT).as_posix())
            for q in sorted(path(OWN).rglob("*")) if q.is_file() and not q.name.endswith(".partial")],
        no_downstream_start=True))
    print(json.dumps({"report": r["report"], "result": ref(OWN + "/result.json"), "evidence": r["evidence"], "checkpoint": cp,
        "actual_targets": e["actual_targets"]}))

if __name__ == "__main__":
    check(Path.cwd().resolve() == ROOT.resolve(), "Wrong working directory")
    {"selftest": lambda: print(selftest()), "qualify": qualify, "readback": readback,
     "preflight": preflight, "apply": apply, "terminal": terminal}[sys.argv[1]]()
