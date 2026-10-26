#!/usr/bin/env python3
"""Repair an AI Laptop Hermes MCP launcher reference without changing credentials.

Dry-run by default. Run under the normal Hermes user, not sudo.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

OLD_PREFIX = "/opt/AI-Install/"
STABLE = "/opt/ai-proxy/integrations/hermes/ai-laptop-reads-launch.sh"
RELEASE_REL = "tools/hermes-pilot/ai-laptop-reads-launch.sh"

def migrate(config: Path, launcher: Path, apply: bool):
    if not config.is_file():
        raise RuntimeError(f"Hermes config missing: {config}")
    if not launcher.is_file():
        raise RuntimeError(f"Launcher missing: {launcher}")
    if not (launcher.stat().st_mode & 0o111):
        raise RuntimeError(f"Launcher is not executable: {launcher}")
    data = config.read_text()
    # Require only one existing AI Laptop launcher path to avoid changing unrelated config.
    import re
    matches = re.findall(r"/opt/AI-Install/[^\s\"']+/tools/hermes-pilot/ai-laptop-reads-launch\.sh", data)
    matches += [STABLE] if STABLE in data else []
    unique = sorted(set(matches))
    if len(unique) != 1:
        raise RuntimeError(f"Expected exactly one existing MCP launcher reference; found {len(unique)}")
    old = unique[0]
    if old == str(launcher):
        print("PASS already configured:", launcher)
        return
    print("Old launcher:", old)
    print("New launcher:", launcher)
    if not apply:
        print("DRY RUN: no changes made. Re-run with --apply.")
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = config.with_name(config.name + ".pre-mcp-migration-" + stamp + ".bak")
    shutil.copy2(config, backup)
    config.write_text(data.replace(old, str(launcher), 1))
    print("Updated Hermes config. Backup:", backup)
    print("Verify with: hermes mcp test ai_laptop_reads")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=Path.home()/".hermes/config.yaml")
    p.add_argument("--launcher", type=Path, default=Path(STABLE))
    p.add_argument("--apply", action="store_true")
    a=p.parse_args()
    try:
        migrate(a.config, a.launcher, a.apply)
    except (RuntimeError, OSError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
