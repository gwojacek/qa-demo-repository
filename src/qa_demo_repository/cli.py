# src/qa_demo_repository/cli.py

import subprocess
import sys
from typing import List, Tuple


def run_check(cmd: List[str], name: str) -> Tuple[bool, str]:
    """Runs a subprocess command. Returns (success, output)."""
    print(f"\033[96m▶ Running {name}...\033[0m")
    try:
        result = subprocess.run(
            [sys.executable, "-m"] + cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(result.stdout)
        print(f"\033[92m✓ {name} passed\033[0m\n")
        return True, ""
    except subprocess.CalledProcessError as e:
        print(e.stdout or "")
        print(f"\033[91m✗ {name} failed\033[0m\n")
        return False, e.stdout or ""


def lints():
    checks = [
        (["black", "."], "black"),
        (["isort", "."], "isort"),
        (["flake8", "."], "flake8"),
    ]
    failed = []
    for cmd, name in checks:
        ok, _ = run_check(cmd, name)
        if not ok:
            failed.append(name)

    print("-" * 48)
    if failed:
        print(f"\033[91mFAILED checks: {', '.join(failed)}\033[0m")
        sys.exit(1)
    else:
        print("\033[92mAll checks passed! 🍰\033[0m")
        sys.exit(0)
