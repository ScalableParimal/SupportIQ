"""Own fresh retry publisher; preserved prior helper is a fingerprinted input."""
from pathlib import Path
import hashlib
import sys

PRIOR = Path(r"C:\PARIMAL_SHERE\SCALABLE_SOLUTIONS\SupportIQ\docs\sdlc-records\governance\0061148a-1b62-4d25-adff-e7f2318dbfad\attempts\20261102T115616Z-ab050be4-c4db-46ae-a5eb-a9fcf9bb41cb\evidence\publisher.py")
data = PRIOR.read_bytes()
text = data.decode("utf-8")
old = 'assert obj["outcome"] in ("PASS","COMPLETED")'
assert text.count(old) == 1
text = text.replace(old, '''assert obj["execution_status"] == "COMPLETED"
                if label == "application/result.json":
                    assert obj["outcome"] == "EXACT APPROVED BYTES APPLIED"
                elif label in ("verification/result.json", "review/result.json"):
                    assert obj["outcome"] == "PASS"
                else:
                    raise AssertionError("Unrecognized predecessor role")''')
text = text.replace("20261102T115616Z-ab050be4-c4db-46ae-a5eb-a9fcf9bb41cb", "20261102T115939Z-13d5ebf4-c6bb-44d9-8082-8e9031fbc17f")
text = text.replace("Yes, initiate the complete Governance Audit under the existing Work ID and Cycle 1 using the GOV-AUD-20261102-002 Application, Verification PASS and Review PASS",
                    "Yes, initiate a fresh complete Governance Audit retry with corrected process-specific preflight validation; no other stage")
text = text.replace('"outputs":{"report"', '"outputs":{"report"')
exec(compile(text, str(PRIOR) + ":fresh-retry-corrected", "exec"), globals())
