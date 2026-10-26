# Chat model migration — 64K minimum (experimental)

## Why

Hermes v0.22.5 rejects a 4,096-token context; it enforces a minimum 64,000-token context. The older LiteLLM `Quick Chat` alias was designed for the previous custom request router, not a full agent harness. Keep that alias available for existing production clients, but use a dedicated LiteLLM `Chat` alias for Hermes.

## Deployment design (NOT automatically applied)

1. On the Ollama host, create a **separate** model derivative using a Modelfile, rather than changing the production model's global settings:

   ```bash
   printf 'FROM gemma4:e4b\nPARAMETER num_ctx 65536\n' > /tmp/ai-laptop-chat.Modelfile
   ollama create ai-laptop-chat -f /tmp/ai-laptop-chat.Modelfile
   ```

   The requested context is a runtime allocation target, **not proof** that it fits the available GPU/RAM or that the model handles tools well. Test the separate derivative and monitor `ollama ps` and `nvidia-smi`. This may be slow or require CPU/RAM offload.

2. Add a **new** LiteLLM model entry in the live LiteLLM YAML (determine the current mapped configuration path first; do not overwrite it):

   ```yaml
   model_list:
     # Preserve every existing model entry. Add the following item:
     - model_name: Chat
       litellm_params:
         model: ollama_chat/ai-laptop-chat
         api_base: http://ollama:11434
   ```

   The `api_base` shown above is only appropriate when the LiteLLM container can resolve the Ollama service as `ollama`. Reuse the working Ollama `api_base` from another model entry. Validate the full YAML before restarting only LiteLLM; validate `/v1/models` and a `Chat` inference request using the existing **LiteLLM Proxy Master API Key**.

3. After verifying `Chat` inference with 65,536 actual context allocation, switch Hermes interactively using `hermes setup model`: same LiteLLM endpoint and existing saved key, **model `Chat`**, Chat Completions transport, context length **65536**. Do not re-run the Hermes installer.

4. Start a fresh Hermes session and verify a simple response, the model label and actual context, then `hermes mcp list` / `hermes mcp test` and the eight-question read-only regression conversation. Do not turn on production writes yet.

## Checks and rollback

- Check `ollama ps`: the model handling Chat must actually allocate 65,536 context. A 4,096 allocation fails the acceptance gate, even if Hermes displays 65,536.
- Check `nvidia-smi` / system RAM during initial inference, and capture response latency before adoption.
- If 65,536 does not fit reliably on the laptop, benchmark on the larger inference workstation or select a smaller tool-capable model with a genuinely usable 64K window. Do not merely spoof context metadata.
- Preserve the pre-change LiteLLM YAML and existing provider credentials. Rollback = select the previous Hermes model and restore the original LiteLLM YAML; leave the legacy aliases intact.

This document is a **migration plan**, not evidence of live context verification.
