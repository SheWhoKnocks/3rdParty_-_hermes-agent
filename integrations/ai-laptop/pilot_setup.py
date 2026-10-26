#!/usr/bin/env python3
"""Dry-run-first Hermes pilot configuration; preserves the working model provider."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import os
import shutil
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Back up Hermes config and apply only context override")
    parser.add_argument("--context", type=int, choices=[65536, 131072], default=65536)
    args = parser.parse_args()
    config = Path.home() / ".hermes" / "config.yaml"
    if not config.is_file() or not shutil.which("hermes"):
        print("Missing Hermes CLI or ~/.hermes/config.yaml. Install Hermes as your normal user.", file=sys.stderr)
        return 2
    result = subprocess.run(["hermes", "config", "get", "model.context_length"], capture_output=True, text=True, timeout=20)
    print("Hermes config:", config)
    print("Current context:", result.stdout.strip() if result.returncode == 0 else "unavailable")
    print("Requested Hermes minimum-compliant context:", args.context)
    print("WARNING: This does not configure Ollama or LiteLLM actual context. Verify backend allocation >= requested context first.")
    print("Credential definitions:")
    print("  LITELLM_MASTER_KEY = LiteLLM Proxy Master API Key (Hermes model inference).")
    print("  AGENT_RUNTIME_API_KEY = AI Laptop Agent Runtime Service API Key (MCP personal-data reads).")
    print("  Hermes saved endpoint key = ~/.hermes/.env (reused; NOT re-requested).")
    print("No API keys are read, printed, or changed by this script.")
    if not args.apply:
        print("DRY RUN: no changes. Use --apply only if an override is needed.")
        return 0
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = config.with_name("config.yaml.ai-laptop-backup-" + stamp)
    shutil.copy2(config, backup)
    os.chmod(backup, 0o600)
    print("Backup:", backup)
    applied = subprocess.run(["hermes", "config", "set", "model.context_length", str(args.context)], check=False)
    if applied.returncode:
        shutil.copy2(backup, config)
        os.chmod(config, 0o600)
        print("Configuration restored after error.", file=sys.stderr)
        return applied.returncode
    print("Updated Hermes metadata only; backend context must be configured separately and verified. Other settings unchanged.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
