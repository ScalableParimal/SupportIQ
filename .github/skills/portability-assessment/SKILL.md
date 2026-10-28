---
name: portability-assessment
description: Executes the governed SDLC Portability Assessment process using the repository Portability Assessment Guideline, Prompt, and Request.
---

# SDLC Portability Assessment Skill

## Purpose and governing artifacts

Execute the governed portability assessment defined by its current Guideline, Prompt, and Request. Follow the three Master Governance documents. The Skill supplies mechanics, not new authority.

## Preconditions

Resolve the Request, explicit source framework and target identities/revisions, read scope, trigger, human decisions, and authorized output scope before inspecting inputs. Stop if target, scope, permission, or applicable governance source is missing. A source-framework path is not permission to inspect a target and vice versa.

## Execution

1. Record whether this is an initial assessment, explicit reassessment, or material-change reassessment. Resolve any prior result and compare source/target revisions, scope, and changed inputs before reusing evidence.
2. Inspect source-framework and target-project evidence separately and only within authorized paths. Fingerprint available inputs. Execute no project scripts, tests, workflows, or runtime operations unless separately and expressly authorized.
3. Apply the Guideline dimensions, applicability rules, determinations, evidence classes, and concern-routing categories. Do not infer universal portability, auto-create findings, or turn a target gap into a framework defect.
4. Produce the Guideline's report with provenance, scope, separate evidence inventories, determinations, adaptations, possible blockers, confidence/limitations, next processes, reassessment trigger, and any actual human decision supplied. Preserve its wording and attribution; never invent a decision.
5. For a recommended possible blocker, request an explicit decision by the identified target-project human. If absent, mark pending and recommend a hold; do not claim a decision or enforce one autonomously.
6. Bind result metadata to report, source/target revisions, and authorized attempt. Publish only within this actor's explicit record scope and persistence contract; do not alter another process's records.
7. Identify the next governed process for each concern, then stop.

## Boundaries

No automatic invocation of another Agent; no Orchestrator activation; no source or target writes; no product implementation; no requirement/plan approval; no Human Acceptance; no commit/push. Do not initiate a parallel lifecycle. Static evidence cannot establish runtime success.
