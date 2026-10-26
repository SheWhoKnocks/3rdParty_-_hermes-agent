# AI Laptop v3.16.3 — live validation and release blockers

**Status:** development/validation in progress, NOT certified or released. This folder is part of a Hermes fork integration PR; it is **not** the cumulative AI Laptop installer.

## Live findings supplied by the operator (2026-10-25 local)

- Hermes + LiteLLM `Chat` inference worked and Ollama's loaded `ai-laptop-chat` reported 65,536 context on GPU.
- Hermes MCP `ai_laptop_reads` connected and discovered **8 read-only tools**, and a real `reminders_all` request retrieved **5 active records**.
- MCP subsequently failed because `~/.hermes/config.yaml` referenced a deleted, version-specific v3.16.1 launcher. Changing the reference to the existing v3.16.2 launcher restored the handshake (8 tools) and reminder retrieval.
- Readiness result after repair: **17 PASS, 0 FAIL, 3 REVIEW, 10 PENDING**. This is *not* a production-ready gate.
- AI Laptop milestone health **16/16**; Docker Compose **21 running containers**; seven persistent agents had listening states and heartbeats.
- Mem0 `GET /ready` returned `{"status":"ready","symbolic_ready":true}`; Qdrant `/healthz` succeeded. This does not prove memory writes/recall.
- Agent Runtime job summary: health 2, home 20, life-assistant 59, orchestrator 70, productivity 7, wellness 2 completed; zero queued/running/failed in snapshot. Completed counts do not certify routing/policy compliance.
- Hermes native `memory` write *invocation* was observed, but a later Hermes invocation reported memory retrieval unavailable. Do **not** assume Hermes native memory was stored in AI Laptop Mem0.
- `sudo ai-agent-memory-trust --help` returned HTTP 401; investigate utility authentication/usage rather than treating it as an API schema failure.
- Reminder interpretation defect: UTC `2026-10-04T16:00:00Z` is **Oct 4, 10:00 MDT** and was already overdue on Oct 25, not upcoming. Keep UTC->`America/Edmonton` conversion deterministic, not model-only.

## Required v3.16.3 release gates

1. **Stable launcher:** install under `/opt/ai-proxy/integrations/hermes/` with executable permissions; migrate Hermes user config with backup; verify MCP handshake/tools after upgrade and after removing an old release directory. The helper in this branch can update the user config *after* the new launcher is installed; it does not install one.
2. **Memory:** authenticated Mem0 synthetic write, cross-session search, persistence across controlled restart, isolation between test users, deletion/cleanup, and safe error behavior.
3. **Agents:** actual per-agent dispatch with verified agent IDs/traces; test both persistent and definition-only dispatch. Validate health and wellness synthetic prompts, boundaries and escalation without personal data.
4. **Calendar/reminders:** compare authoritative records with local-time classification and due-date ranges; distinguish overdue/active/due today; detect likely duplicates without deleting user data.
5. **Authorization:** scoped reads, rejection of unauthorized writes, no secrets logged; do not treat a broadly privileged Agent Runtime key as read-only.
6. **Reliability:** rollback, restart recovery, relevant regressions and cumulative installer/README/changelog/checksum consistency.
7. **Reporting:** critical PASS/FAIL, REVIEW and PENDING must be distinct; **PENDING never counts as PASS**.

## Reproduction and operations

```bash
hermes mcp test ai_laptop_reads
hermes -z "Use the ai_laptop_reads reminders_all MCP tool. Report the number of active reminders returned."
sudo ai-agent-status
sudo ai-agent-jobs
sudo ai-assistant-milestone-status
curl -sS http://127.0.0.1:8765/ready
curl -sS http://127.0.0.1:6333/healthz
```

Keep Hermes commands under the normal user. Do not add the user to the Docker group. Never publish `.env` credentials, actual private memory contents, or unredacted agent histories.
