# AI Laptop v3.16.3 — Governed task execution (candidate)

The cumulative AI Laptop v3.16.3 ZIP has been built from the full v3.16.2 installer and is distributed in the ChatGPT project artifact, **not** as an asset in this Hermes fork.

## Summary
- Atomic task+queue persistence for POST /tasks and delegated tasks.
- Worker route for read-only model-generated answers; action-oriented requests blocked pending separately governed approval.
- Task completion evidence checks; prevent public phase API from claiming verified completion without completed worker evidence.
- Fix shell operator utilities' quoted API key loading and required argument validation.
- Retains full install.sh, install-openwebui-functions.sh, Docker Compose and documentation.

## Validation and limitations
- Offline static Python compilation, shell syntax, and targeted regression tests: PASS.
- **Not yet tested on the user's live AI Laptop.** This is a test candidate, not a production-certified release.
- Semantic Mem0 retrieval and restart persistence are outstanding.
- Pre-existing DISCOVER tasks are not automatically migrated.
- The companion ZIP and SHA256 must be downloaded from the ChatGPT artifact link; this repository does not host the ZIP binary.

## Upgrade
Back up /opt/ai-proxy, runtime volumes and .env first. Run the full cumulative install.sh as a sudo-capable non-root user, then verify endpoints, task creation and actual completion. Retain v3.16.2 for rollback.
