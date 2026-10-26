# AI Laptop + Hermes v3.16.2 — automated pilot setup

This optional integration belongs to the experimental Hermes branch, **not** to the production AI Laptop release tree. It does not replace production routing or install Hermes again.

## Credential names — what the installer is asking for

| Configuration variable | Human-readable name | Used for | Where to find it | Needed when |
| --- | --- | --- | --- | --- |
| `LITELLM_MASTER_KEY` | **LiteLLM Proxy Master API Key** | Authenticates Hermes to the existing local LiteLLM inference proxy (models such as the proposed Chat alias) | `/opt/ai-proxy/.env`, variable `LITELLM_MASTER_KEY` | Configuring Hermes inference or authenticated model diagnostics |
| `AGENT_RUNTIME_API_KEY` | **AI Laptop Agent Runtime Service API Key** | Authenticates the **read-only Hermes MCP adapter** to AI Laptop's Agent Runtime and authoritative project/reminder/calendar read endpoints | Usually `/opt/ai-proxy/.env`, variable `AGENT_RUNTIME_API_KEY`; verify the variable exists | Only when registering/testing the governed service-read adapter |
| `HERMES_CUSTOM_127_0_0_1_4000_API_KEY` | **Hermes saved LiteLLM endpoint key** | Hermes' copy of the LiteLLM credential for the configured custom endpoint | `~/.hermes/.env`, written by `hermes setup model` | Normally reused; do not re-enter on every release |
| `GITHUB_TOKEN` | **Optional GitHub API token** | Higher API rate limits for Hermes Skills Hub/GitHub integrations | User-created GitHub token with minimal scope | Not required for the local pilot |

**These are not interchangeable.** The LiteLLM key is for **model inference**; the Agent Runtime key is for **AI Laptop personal-assistant service data**. A GitHub token is not required for either.

### Verify existence without exposing secrets

```bash
sudo sh -c 'for n in LITELLM_MASTER_KEY AGENT_RUNTIME_API_KEY; do if grep -q "^$n=." /opt/ai-proxy/.env; then echo "$n: configured"; else echo "$n: missing or empty"; fi; done'
```

Do not post actual keys in chat, GitHub issues, terminals being recorded, or release archives. For interactive entry, use a hidden prompt. Do not commit `~/.hermes/.env` or `/opt/ai-proxy/.env`.

## Existing installation — skip repeated setup

Run as the normal Ubuntu account, not root. The automation detects Hermes and **does not** reinstall it or replace the working LiteLLM settings.

```bash
python3 integrations/ai-laptop/pilot_setup.py
```

That is a **dry run**. To apply only a bounded Hermes context override after seeing the plan:

```bash
python3 integrations/ai-laptop/pilot_setup.py --apply --context 65536
```

**Do not apply the 65,536-token metadata override until the actual Ollama model serving Chat has been configured and observed at 65,536 or higher.** Hermes enforces a minimum 64,000-token window and explicitly rejects 4,096. Merely editing Hermes config does not increase the model server context. The operator has now validated a deployed Chat alias backed by ai-laptop-chat at 65,536 context; do not assume it is installed on other hosts. Retain Quick Chat for existing clients until the new model route passes validation.

The apply command backs up `~/.hermes/config.yaml` and changes only `model.context_length`. All other settings, credentials, gateway/service state, Docker permissions, and Open WebUI routes remain unchanged.

Non-mutating health report:

```bash
python3 integrations/ai-laptop/pilot_check.py --output /tmp/ai-laptop-hermes-check.json
```

Without a LiteLLM key in the environment, authenticated model listing is marked as skipped; the diagnostic does not display or search for any key.

## Known integration gates

- The current Hermes CLI one-shot inference returned `PILOT_OK` through LiteLLM / Ollama.
- The local Hermes CLI's eight-turn test did not merge unrelated requests into a calendar event.
- The operator confirmed the AI Laptop **governed MCP adapter** is deployed, exposes 8 read-only tools, and returns 5 active reminders. The current registration must be repaired if its version-specific launcher directory disappears. Read-only tool naming does **not** make the broad Agent Runtime service credential read-only.
- Production calendar writes, API-server/Open WebUI connectivity, rootless Docker sandbox and egress firewall are **not yet verified**.
- Do not grant Hermes the production Docker socket or unrestricted Agent Runtime mutation capabilities.

## Release checklist

Every subsequent AI Laptop/Hermes release must document **every required key** with its human-readable name, service, purpose, location, whether optional, and safe retrieval method. No raw credentials belong in packaged artifacts.

## v3.16.3 validation status and durable MCP registration

See [VALIDATION-v3.16.3.md](VALIDATION-v3.16.3.md). Latest operator diagnostics: 17 PASS / 0 FAIL / 3 REVIEW / 10 PENDING. **This is not a release-ready certification.** Memory persistence, isolation and agent execution/safety gates are not yet complete.

**Known upgrade defect:** Hermes config may retain a launcher inside `/opt/AI-Install/v3.16.1-.../`. Removing the old release breaks the MCP server even when the current release is healthy. The target stable path is `/opt/ai-proxy/integrations/hermes/ai-laptop-reads-launch.sh`.

To migrate registration safely, **first install the launcher at the stable path**, then run the helper as the normal Hermes user:

```bash
python3 integrations/ai-laptop/migrate_mcp_launcher.py
python3 integrations/ai-laptop/migrate_mcp_launcher.py --apply
hermes mcp test ai_laptop_reads
```

The helper is dry-run-first, checks that the chosen launcher exists and is executable, and creates a timestamped backup of Hermes config on apply. It does not copy the launcher, reinstall Hermes, grant Docker permissions, modify credentials or change service routing. For manual recovery, the operator already verified switching the path from the retired v3.16.1 release to the v3.16.2 release. The stable path must be added to the cumulative AI Laptop installer separately.

**Hermes native memory is separate from AI Laptop Mem0.** An observed native memory write invocation did not establish Mem0 capture, and subsequent free-form memory search was unavailable. Do not mark memory working until synthetic authenticated write/read, cross-session persistence, isolation and cleanup pass.
