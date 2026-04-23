#!/usr/bin/env python3
"""
Verify all active Enclave services from the host.
Usage: python3 scripts/health-check.py
"""
import os
import sys
import urllib.request
import urllib.error

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

ENABLE_DOCUMENT_EDITOR = os.getenv("ENABLE_DOCUMENT_EDITOR", "false").lower() == "true"

CHECKS = [
    ("PostgreSQL (via backend)", "http://localhost:8000/health"),
    ("Backend /health", "http://localhost:8000/health"),
    ("Frontend", "http://localhost:3000"),
    ("Ollama", "http://localhost:11434/api/tags"),
]

if ENABLE_DOCUMENT_EDITOR:
    CHECKS.append(("ONLYOFFICE", "http://localhost:8443/healthcheck"))

all_ok = True

for name, url in CHECKS:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            status = resp.status
        if status == 200:
            print(f"{GREEN}[OK]    {name}{RESET}")
        else:
            print(f"{YELLOW}[WARN]  {name} — HTTP {status}{RESET}")
            all_ok = False
    except urllib.error.URLError as e:
        print(f"{RED}[FAIL]  {name} — {e.reason}{RESET}")
        all_ok = False
    except Exception as e:
        print(f"{RED}[FAIL]  {name} — {e}{RESET}")
        all_ok = False

if not ENABLE_DOCUMENT_EDITOR:
    print(f"{YELLOW}[SKIP]  ONLYOFFICE — ENABLE_DOCUMENT_EDITOR=false{RESET}")

print()
if all_ok:
    print(f"{GREEN}All active services healthy.{RESET}")
    sys.exit(0)
else:
    print(f"{RED}One or more services failed.{RESET}")
    sys.exit(1)
