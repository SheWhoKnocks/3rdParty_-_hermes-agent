# AI Laptop v3.16.2 — Hermes Pilot Automation & Credential Clarity

**Scope:** Experimental integration files on the Hermes fork; not a full production AI Laptop deployment.

## Changes
- Added a rerunnable, dry-run-first setup helper for Hermes context configuration.
- Added a read-only health report for local LiteLLM, Hermes configuration, systemd gateway, API/A2A ports and Docker access.
- Added a **credential glossary** explaining every key's human name, owning service, purpose, source file, and required/optional status.
- No full Hermes reinstall, API key rotation, credential copy, Docker group membership change, gateway restart, or production routing change.
- Added a focused unittest file.

## Credentials
- `LITELLM_MASTER_KEY` — **LiteLLM Proxy Master API Key**: lets Hermes call the model proxy. Usually in `/opt/ai-proxy/.env`.
- `AGENT_RUNTIME_API_KEY` — **AI Laptop Agent Runtime Service API Key**: authenticates the governed MCP reads against the existing structured personal-data service. Usually in `/opt/ai-proxy/.env`. This credential may be broadly privileged.
- `HERMES_CUSTOM_127_0_0_1_4000_API_KEY` — **Hermes Saved LiteLLM Endpoint Key**: locally stored copy of the LiteLLM key, in `~/.hermes/.env`; do not re-enter each release.
- `GITHUB_TOKEN` — **Optional GitHub API Token**: Skills Hub rate limit support, not needed for the pilot.

**Secrets never belong in release files or GitHub commits.** See README for a presence-only check.

## Validation required
Run `python3 -m unittest discover -s integrations/ai-laptop -p 'test_*.py'` and `python3 integrations/ai-laptop/pilot_check.py` on the target machine. Live sandbox, MCP adapter and calendar writes remain unverified.
