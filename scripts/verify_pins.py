#!/usr/bin/env python3
"""Cross-platform pin check — mirrors scripts/verify-pins.sh for Windows lefthook."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG_JSON = ROOT / "package.json"
UV_LOCK = ROOT / "agent" / "uv.lock"

PINS = {
    "@copilotkit/react-core": "1.57.4",
    "@copilotkit/runtime": "1.57.4",
    "@copilotkit/a2ui-renderer": "1.57.4",
    "@copilotkit/react-ui": "1.57.4",
    "next": "16.1.6",
    "react": "19.2.4",
    "react-dom": "19.2.4",
}

PYTHON_PINS = {
    "langchain": "1.3.1",
    "langchain-core": "1.4.0",
    "langgraph": "1.2.1",
}


def main() -> int:
    if not PKG_JSON.is_file():
        print(f"FAIL: package.json not found at {PKG_JSON}", file=sys.stderr)
        return 1

    pkg = json.loads(PKG_JSON.read_text(encoding="utf-8"))
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    drift = 0

    print("pnpm verify-pins — comparing package.json against FROZEN.md\n")
    for name, expected in PINS.items():
        actual = deps.get(name, "")
        if not actual:
            print(f"DRIFT: {name} not declared in package.json (expected {expected})")
            drift += 1
        elif actual != expected:
            print(f"DRIFT: {name} is {actual} but FROZEN.md pins {expected}")
            drift += 1
        else:
            print(f"OK: {name} @ {actual}")

    if UV_LOCK.is_file():
        lock_text = UV_LOCK.read_text(encoding="utf-8")
        for name, expected in PYTHON_PINS.items():
            m = re.search(rf'name = "{re.escape(name)}"\s+version = "([^"]+)"', lock_text)
            if not m:
                print(f"DRIFT: {name} not found in agent/uv.lock (expected {expected})")
                drift += 1
            elif m.group(1) != expected:
                print(f"DRIFT: {name} is {m.group(1)} in uv.lock but FROZEN.md pins {expected}")
                drift += 1
            else:
                print(f"OK: {name} @ {expected} (agent/uv.lock)")

    if drift:
        print(f"\n{drift} pin drift detected.", file=sys.stderr)
        return 1
    print("\nAll pins match FROZEN.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
