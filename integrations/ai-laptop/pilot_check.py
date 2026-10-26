#!/usr/bin/env python3
"""Read-only Hermes / LiteLLM readiness check. Never prints credentials."""
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import urllib.error
import urllib.request

def status(url, key=None):
    headers = {"Authorization": "Bearer " + key} if key else {}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=8) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return None

def cmd(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=12)
        return {"exit_code": result.returncode, "stdout": result.stdout.strip()[:200]}
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return {"exit_code": None, "stdout": ""}

def listening(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.3):
            return True
    except OSError:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--litellm-base", default="http://127.0.0.1:4000/v1")
    args = parser.parse_args()
    base = args.litellm_base.rstrip("/")
    key = os.environ.get("LITELLM_MASTER_KEY")
    report = {
        "hermes_cli_present": bool(shutil.which("hermes")),
        "hermes_config_present": (Path.home()/".hermes/config.yaml").is_file(),
        "litellm_readiness_http": status(base.removesuffix("/v1") + "/health/readiness"),
        "litellm_models_http": status(base + "/models", key) if key else "skipped: LiteLLM Proxy Master API Key not supplied",
        "hermes_gateway_status": cmd(["systemctl", "--user", "is-active", "hermes-gateway.service"])["stdout"],
        "docker_access_as_user": cmd(["docker", "info", "--format", "{{.ServerVersion}}"])["exit_code"] == 0,
        "hermes_api_port_8642": listening(8642),
        "hermes_a2a_port_9900": listening(9900),
        "credential_guide": {
            "LITELLM_MASTER_KEY": "LiteLLM Proxy Master API Key — model inference, /opt/ai-proxy/.env",
            "AGENT_RUNTIME_API_KEY": "AI Laptop Agent Runtime Service API Key — governed personal-data reads, /opt/ai-proxy/.env",
            "HERMES_CUSTOM_127_0_0_1_4000_API_KEY": "Hermes saved LiteLLM endpoint key — ~/.hermes/.env"
        },
        "safety": "No production service or configuration was changed; no raw credentials collected."
    }
    output = json.dumps(report, indent=2)
    print(output)
    if args.output:
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(output + "\n")
        os.chmod(args.output, 0o600)

if __name__ == "__main__":
    main()
