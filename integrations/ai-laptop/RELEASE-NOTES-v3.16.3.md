# AI Laptop v3.16.3 — Governed task execution (test candidate)

## Artifact
Cumulative ZIP: `v3.16.3-governed-task-execution.zip` (provided in the ChatGPT project; **not uploaded as a binary to this GitHub fork**).
SHA-256: `0e8ab99c15eac0acb29edb724882643622d6044de649d58773a5f76c6ed15da6`

## Changes
- Direct task creation and delegated-task creation atomically enqueue a matching agent job.
- Extend the worker to produce read-only model responses, record evidence and mark the task complete when a substantive response is returned; blocked or failed work is not presented as successful.
- Keep action-oriented work out of the new executor pending a separately governed approval path; no tool writes are introduced by this patch.
- Require a completed worker record for public `PUT /tasks/{task_id}/phase` to mark verified completion.
- Fix quoted API key parsing in `ai-agent-reliability`, `ai-agent-recovery-audit`, `ai-agent-prompt-audit`, and `ai-agent-memory-trust`; add required argument checks.
- Install Hermes MCP launcher in stable `/opt/ai-proxy/integrations/hermes` location; provide opt-in non-root config migration helper.
- Cumulative packaging includes `install.sh`, `install-openwebui-functions.sh`, docs, previous tests and changelog.

## Verification
Offline Python compilation, Bash syntax, API-auth helper quote handling and 3 source-level regression tests passed. **Live model inference, behavior quality, and host-upgrade tests are still pending.** A non-empty model response is a technical completion criterion, not proof that the answer is factually correct.

## Upgrade and rollback
Back up the existing runtime DB, Docker volumes and `/opt/ai-proxy/.env`; run the cumulative installer as a non-root sudo-capable user. Test one synthetic read-only task and check `GET /tasks/{id}` before use. Retain the v3.16.2 archive for rollback. Existing stranded tasks in DISCOVER are not automatically migrated. Semantic Mem0 recall and restart-persistence validations remain open.

## GitHub scope
This repository is the Hermes Agent fork used for the integration pilot, **not** the full AI Laptop installer repository. GitHub hosts these integration notes only; the source ZIP artifact is delivered in the ChatGPT conversation.
