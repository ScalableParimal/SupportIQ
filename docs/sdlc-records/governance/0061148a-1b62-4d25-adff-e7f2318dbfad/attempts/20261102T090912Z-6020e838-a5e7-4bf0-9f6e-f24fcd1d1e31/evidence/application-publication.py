"""Actor-owned execution evidence. Windows exclusive, flushed, no-overwrite publication."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
OWN = Path(__file__).resolve().parent.parent.relative_to(ROOT)
ATTEMPT = OWN.name
INV = json.loads((OWN / "attempt.json").read_bytes())
PACKAGE = Path(INV["authorization"]["canonical_package"]["path"]).parent
CHECKS = []


def digest(b):
    return hashlib.sha256(b).hexdigest().upper()


def ref(path):
    p = Path(path)
    if p.is_absolute():
        p = p.relative_to(ROOT)
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": digest(b)}


def read(path):
    return json.loads(Path(path).read_bytes())


def check(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def binding(r, origin):
    p = Path(r["path"].replace("\\", "/"))
    check(not p.is_absolute() and ".." not in p.parts, "Unsafe reference: " + origin)
    actual = ref(p)
    check(actual["sha256"] == r["sha256"].upper(), "Digest mismatch: " + origin)
    if "bytes" in r and r["bytes"] is not None:
        check(actual["bytes"] == r["bytes"], "Byte count mismatch: " + origin)
    CHECKS.append({"origin": origin, "actual": actual, "outcome": "PASS"})
    return actual


def walk(v, origin):
    if isinstance(v, dict):
        if isinstance(v.get("path"), str) and isinstance(v.get("sha256"), str):
            binding(v, origin)
        for k, item in v.items():
            walk(item, origin + "/" + k)
    elif isinstance(v, list):
        for i, item in enumerate(v):
            walk(item, origin + "/" + str(i))


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], text=True).strip()


def safe_output(p):
    p = Path(p)
    check(p.is_relative_to(OWN), "Output outside own scope")
    check(not os.path.lexists(p), "Final output collision: " + str(p))
    for parent in [p.parent, *p.parents]:
        if parent == Path("."):
            break
        if os.path.lexists(parent):
            check(not parent.is_symlink() and not os.path.isjunction(parent),
                  "Reparse-point output ancestor: " + str(parent))
    return p


def publish(p, b, is_json=False):
    p = safe_output(p)
    check(b.decode("utf-8").encode("utf-8") == b, "UTF-8 roundtrip failed")
    check(not b.startswith(b"\xef\xbb\xbf") and b"\r" not in b, "Encoding/newline")
    if is_json:
        json.loads(b)
    p.parent.mkdir(parents=True, exist_ok=True)
    partial = p.with_name(p.name + ".partial")
    check(not os.path.lexists(partial), "Partial collision")
    with open(partial, "xb") as h:
        check(h.write(b) == len(b), "Short write")
        h.flush()
        os.fsync(h.fileno())
    check(partial.read_bytes() == b, "Partial readback mismatch")
    if is_json:
        json.loads(partial.read_bytes())
    check(not os.path.lexists(p), "Final collision at publish")
    # Windows os.rename does not replace an existing destination.
    check(os.name == "nt", "Windows no-overwrite semantics required")
    os.rename(partial, p)
    check(p.read_bytes() == b, "Published readback mismatch")
    return ref(p)


def metadata(kind):
    return {
        "schema_version": "1.0", "record_type": kind,
        "record_id": ATTEMPT + ":" + kind, "work_id": INV["work_id"],
        "attempt_id": ATTEMPT, "cycle_id": INV["cycle_id"],
        "cycle_number": INV["cycle_number"], "creator": ATTEMPT,
        "role": INV["role"], "process": INV["process"],
        "subject_type": "FINDING", "finding_id": INV["finding_id"],
        "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "clock_basis": "Current host UTC preparation sample, not original decision time",
    }


def put_json(p, d):
    b = (json.dumps(d, ensure_ascii=True, indent=2) + "\n").encode("utf-8")
    check(json.loads(b) == d, "Serializer parse-check")
    return publish(p, b, True)


def preservation():
    expected = {r["path"]: r for r in INV["repository"]["preexisting_file_manifest"]}
    actual = {}
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if ".git" in rel.parts or rel.is_relative_to(OWN) or not p.is_file():
            continue
        actual[rel.as_posix()] = ref(rel)
    check(actual == expected, "Pre-existing path/byte endpoint drift")
    for k, args in [("head", ("rev-parse", "HEAD")),
                    ("branch", ("branch", "--show-current")),
                    ("origin", ("remote", "get-url", "origin")),
                    ("status_porcelain", ("status", "--porcelain=v1"))]:
        check(git(*args) == INV["repository"][k], "Repository context drift: " + k)
    return {"preexisting_files_compared": len(expected), "all_paths_bytes_match": True,
            "head_branch_origin_status_match": True, "only_excluded_scope": OWN.as_posix(),
            "limitations": INV["qualification"]["limitations"]}


def validate():
    CHECKS.clear()
    for r in INV["input_references"] + INV["governing"]:
        binding(r, "qualified_invocation")
    request = read(PACKAGE / "attachments/exact-approval-request.json")
    evidence = read(PACKAGE / "evidence/finalized-decision-evidence.json")
    preparer = read(PACKAGE / "attempt.json")
    result = read(PACKAGE / "result.json")
    scope = request["exact_approval_scope"]
    check(scope == INV["authorization"]["scope_as_presented"], "Scope drift")
    check(scope == evidence["approval_scope"], "Request/evidence scope disagreement")
    for name, d in [("request", request), ("evidence", evidence),
                    ("preparer", preparer), ("result", result)]:
        walk(d, name)
        check(d["work_id"] == INV["work_id"], "Work binding")
        check(d["cycle_id"] == INV["cycle_id"] and d["cycle_number"] == INV["cycle_number"],
              "Cycle binding")
    check(request["canonical_package"] == ref(PACKAGE / "report.md"), "Package binding")
    roles = scope["roles"]
    pairs = [(r["definition"]["path"], r["definition"]["sha256"]) for r in roles.values()]
    check(len(set(pairs)) == 4 and len({p[0] for p in pairs}) == 4, "Actor separation")
    check(roles["publisher"]["definition"] == INV["actor_identity"]["definition"], "Publisher")
    check(roles["publisher"]["future_attempt_identity"] == ATTEMPT, "Publisher attempt")
    check(roles["publisher"]["designated_scope"] == OWN.as_posix(), "Publisher scope")
    check(roles["preparer"]["current_attempt"] == ref(PACKAGE / "attempt.json"), "Preparer attempt")
    check(preparer["actor_identity"]["definition"] == roles["preparer"]["definition"],
          "Preparer identity")
    check(preparer["attempt_id"] != ATTEMPT, "Reused preparer attempt")
    for excluded in scope["excluded_publisher_definitions"]:
        check(excluded["path"] != INV["actor_identity"]["definition"]["path"] and
              excluded["sha256"] != INV["actor_identity"]["definition"]["sha256"],
              "Excluded publisher actor")
    check(Path(scope["target"]).parent == OWN / "attachments", "Target scope")
    check(scope["base_condition"]["presence"] == "ABSENT" and
          scope["base_condition"]["base_sha256"] is None and
          scope["base_condition"]["base_bytes"] is None, "Base semantics")
    check(scope["base_condition"]["application_attempt_path"] == OWN.as_posix(), "Base scope")
    check(not os.path.lexists(scope["target"]), "Target no longer absent")
    for p in [Path(scope["target"]), OWN / "report.md", OWN / "result.json",
              OWN / "evidence/application-evidence.json"]:
        safe_output(p)
    payload = Path(scope["payload_source"]["path"]).read_bytes()
    check(len(payload) == scope["expected_after_bytes"] == scope["payload_bytes"] == 3438,
          "Payload size")
    check(digest(payload) == scope["expected_after_sha256"] == scope["payload_sha256"],
          "Payload expected-after digest")
    check(payload.isascii() and not payload.startswith(b"\xef\xbb\xbf") and b"\r" not in payload
          and payload.endswith(b"\n") and not payload.endswith(b"\n\n"), "Payload encoding")
    check(b"`n" not in payload and b"${" not in payload and b"$(" not in payload,
          "Payload unresolved template or escaped newline")
    report_bytes = (PACKAGE / "report.md").read_bytes()
    embedded = re.findall(rb"```markdown\r?\n(.*?)```", report_bytes, re.S)
    check(len(embedded) == 1 and embedded[0] == payload, "Report payload embedding")
    citations = []
    for label, content in [("canonical report", report_bytes), ("payload", payload)]:
        # Validate every explicit path/byte/digest citation, not only structured references.
        matches = re.findall(
            rb"`([^`\r\n]+)` \((\d+) bytes; SHA-256 `([A-F0-9]{64})`\)", content)
        for path, count, h in matches:
            r = {"path": path.decode("ascii"), "bytes": int(count), "sha256": h.decode("ascii")}
            citations.append(binding(r, label + "/citation"))
    check(len(citations) >= 20, "Unexpectedly missing canonical citations")
    for response_key in ["original_response", "attributed_response"]:
        r = evidence[response_key]
        text = r["exact_text"]
        check(len(text) == r["codepoints"] == 133, "Response codepoints")
        check(len(text.encode("utf-8")) == r["utf8_bytes"], "Response byte length")
        check(digest(text.encode("utf-8")) == r["sha256_utf8_without_newline"], "Response digest")
        source = r["source"]
        source_path = source["path"] if isinstance(source, dict) else source
        source_bytes = Path(source_path).read_bytes()
        if source_path.endswith(".json"):
            def strings(v):
                if isinstance(v, str):
                    yield v
                elif isinstance(v, dict):
                    for x in v.values():
                        yield from strings(x)
                elif isinstance(v, list):
                    for x in v:
                        yield from strings(x)
            check(text in list(strings(json.loads(source_bytes))), "Original text source")
        else:
            check(text in source_bytes.decode("utf-8"), "Attributed text source")
    original = evidence["original_response"]["exact_text"]
    attributed = evidence["attributed_response"]["exact_text"]
    diffs = [(i, ord(a), ord(b)) for i, (a, b) in enumerate(zip(original, attributed)) if a != b]
    check(diffs == [(27, 63, 167), (42, 63, 167)], "Character distinction")
    for r in evidence["source_fingerprint_manifest"]:
        binding(r, "approved source manifest")
    check(len(evidence["source_fingerprint_manifest"]) == 76, "Source coverage count")
    preserved = preservation()
    return scope, payload, {
        "input_binding_checks": list(CHECKS), "input_binding_count": len(CHECKS),
        "all_bindings_match": True, "structured_scope_agreement": True,
        "exact_payload_embedding_match": True, "explicit_citations_checked": len(citations),
        "all_four_actors_distinct": True, "publisher_exclusions_match": True,
        "verifier_reviewer": "Planned definition identities only; no attempts, runtime capability or stage starts",
        "response_differences": diffs, "source_files_checked": 76, "preservation": preserved,
    }


def run():
    mode = sys.argv[1]
    if mode == "preflight":
        scope, payload, checks = validate()
        d = metadata("application_preflight")
        d.update({"invocation": ref(OWN / "attempt.json"), "script": ref(Path(__file__)),
                  "independent_invocation_readback":
                  "Separate PowerShell Get-FileHash/ReadAllBytes/ConvertFrom-Json passed before script creation or comparison",
                  "authorization": INV["authorization"], "validation": checks,
                  "base": INV["base_observation"], "target": scope["target"],
                  "expected_after": ref(scope["payload_source"]["path"]),
                  "application_started": False})
        print(json.dumps(put_json(OWN / "evidence/preflight.json", d), indent=2))
        cp = metadata("checkpoint")
        cp.update({"sequence": 1, "last_confirmed_boundary": "All exact package/input/base checks PASS; no substantive publication",
                   "invocation": ref(OWN / "attempt.json"), "preflight": ref(OWN / "evidence/preflight.json"),
                   "unfinished": "Independent preflight readback, repeat binding/base checks, approved exact publication and readback",
                   "pending_gate": "No downstream stage authorized"})
        print(json.dumps(put_json(OWN / "checkpoint-0001.json", cp), indent=2))
    elif mode == "apply":
        preflight = read(OWN / "evidence/preflight.json")
        checkpoint = read(OWN / "checkpoint-0001.json")
        binding(checkpoint["preflight"], "independent preflight checkpoint")
        binding(preflight["invocation"], "independent preflight invocation")
        binding(preflight["script"], "preflight execution script")
        scope, payload, checks = validate()
        # All checks completed before preparing the single substantive output.
        target = Path(scope["target"])
        before = {"path": target.as_posix(), "presence": "ABSENT", "bytes": None, "sha256": None}
        after = publish(target, payload)
        check(after["sha256"] == scope["expected_after_sha256"] and
              after["bytes"] == scope["expected_after_bytes"], "After validation")
        print(json.dumps({"application": "APPLIED EXACT BYTES", "before": before, "after": after}, indent=2))
        ev = metadata("application_evidence")
        ev.update({"invocation": ref(OWN / "attempt.json"), "preflight": ref(OWN / "evidence/preflight.json"),
                   "checkpoint": ref(OWN / "checkpoint-0001.json"), "script": ref(Path(__file__)),
                   "authorization": INV["authorization"], "validation": checks,
                   "approved_path_list": [target.as_posix()], "actual_substantive_path_list": [target.as_posix()],
                   "before": before, "after": after, "payload_source": ref(scope["payload_source"]["path"]),
                   "exact_byte_comparison": target.read_bytes() == payload,
                   "publication": "Exclusive binary .partial; validated/flushed/fsync; same-filesystem Windows no-overwrite rename; independent file open/read/hash",
                   "preservation_after_application": preservation(), "partial_failure": None,
                   "tool_outcomes": ["Qualified invocation published and independently read back",
                                     "All fingerprints, structured bindings and report citations checked before application",
                                     "Exact approved attachment published without overwrite; post-publish readback matches"],
                   "no_downstream_stage_started": True, "limitations": INV["qualification"]["limitations"]})
        ev_ref = put_json(OWN / "evidence/application-evidence.json", ev)
        lines = [
            "# Governance Amendment Application Report", "",
            "Outcome: COMPLETED -- EXACT APPROVED APPLICATION ONLY", "",
            "Work ID: " + INV["work_id"], "Finding: " + INV["finding_id"],
            "Cycle: " + INV["cycle_id"] + "; Cycle 1.", "Attempt: " + ATTEMPT, "",
            "## Authority, identity and scope", "",
            "The supplied Human designation, exact approval and separate fresh Application start",
            "are transcribed in the qualified invocation and bound evidence. Original authenticated",
            "message IDs/times are not exposed and are not invented. Current invocation capability",
            "was established through nonmutating reads, hashes, checks and effective inherited ACL.",
            "The invocation was published no-overwrite and independently read back before comparison.",
            "This is the designated distinct one-time applier, not standing authority.", "",
            "## Exact before/after", "",
            "Destination: `" + target.as_posix() + "`",
            "Before: ABSENT; byte count and SHA-256 are null, not an empty-file fingerprint.",
            "After: " + str(after["bytes"]) + " bytes; SHA-256 `" + after["sha256"] + "`.",
            "Exact source bytes equal destination bytes; UTF-8 no BOM, ASCII-only, LF, one final LF.",
            "Only the approved attachment plus this actor's required execution records were published.",
            "No original/source/other-actor record was changed; all pre-existing file paths/bytes and",
            "HEAD/branch/origin/status matched the qualified invocation at endpoint checks.", "",
            "## Validation evidence", "",
            "All " + str(checks["input_binding_count"]) + " structured/citation/source binding checks passed;",
            str(checks["explicit_citations_checked"]) + " explicit citations and 76 source fingerprints checked.",
            "All four role bindings are distinct; publisher exclusions passed. Verifier/reviewer remain",
            "planned definition identities only, not current runtime capabilities or started attempts.",
            "Payload embedding, response-source/digest bindings, metadata values and U+003F versus",
            "U+00A7 differences at offsets 27 and 42 passed. No payload reconstruction was used.",
            "Publication used validated/flushed .partial bytes and Windows atomic no-overwrite rename.",
            "Application evidence: `" + ev_ref["path"] + "`; SHA-256 `" + ev_ref["sha256"] + "`.", "",
            "## Limits and next gate", "",
            INV["qualification"]["limitations"], "",
            "This is application readback, not independent Verification, Review or effectiveness Audit.",
            "Latest Audit remains COMPLETED, CONSISTENT WITH MINOR FINDINGS and nonqualifying.",
            "GOV-AUD-20261102-001 is not closed by this application. No historical finding reopened.",
            "No source/product work, commit, push, root/Master adoption or downstream stage occurred.",
            "Next permitted gate: fresh Human initiation of the approval-bound independent Governance",
            "Verification actor. Review requires PASS Verification and its own fresh start; full Audit",
            "requires PASS Review and its own fresh start. STOP.", "",
        ]
        report_ref = publish(OWN / "report.md", "\n".join(lines).encode("utf-8"))
        terminal = metadata("process_result")
        terminal.update({"execution_status": "COMPLETED", "outcome": "EXACT APPROVED APPLICATION COMPLETED",
                         "report": report_ref, "evidence": ev_ref, "invocation": ref(OWN / "attempt.json"),
                         "canonical_package": ref(PACKAGE / "report.md"), "approval": INV["authorization"],
                         "repository": {k: v for k, v in INV["repository"].items() if k != "preexisting_file_manifest"},
                         "actor_identity": INV["actor_identity"], "before": before, "after": after,
                         "expected_after_validation": "PASS; exact bytes/hash/length/encoding",
                         "preservation": preservation(), "failure": None,
                         "unresolved": ["GOV-AUD-20261102-001 awaits independent assurance; latest Audit nonqualifying"],
                         "next_process": "Independent Governance Verification only after fresh Human stage-start",
                         "planned_verifier": scope["roles"]["verifier"],
                         "planned_reviewer": scope["roles"]["reviewer"],
                         "verification_review_audit_started": False, "effectiveness_claimed": False,
                         "standing_authority_claimed": False, "master_adoption": False,
                         "source_edit": False, "historical_record_edit": False,
                         "product_work": False, "commit": False, "push": False,
                         "limitations": INV["qualification"]["limitations"]})
        walk(terminal, "terminal prepublication")
        print(json.dumps(put_json(OWN / "result.json", terminal), indent=2))
        print(json.dumps({"report": report_ref, "attachment": after, "evidence": ev_ref}, indent=2))
    else:
        raise RuntimeError("Unknown mode")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        # Never roll back or retry automatically. Report the actual durable state.
        state = {"outcome": "CANNOT COMPLETE", "error": str(error),
                 "actual_own_files": [ref(p) for p in sorted(OWN.rglob("*")) if p.is_file()],
                 "no_rollback": True, "stop": True}
        print(json.dumps(state, indent=2))
        raise
