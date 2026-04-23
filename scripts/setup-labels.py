#!/usr/bin/env python3
"""
Creates standard GitHub labels for the Enclave repo.
Usage: GITHUB_TOKEN=<pat> python scripts/setup-labels.py yousef-yy4u/enclave
"""
import os, sys, json
import urllib.request, urllib.error

LABELS = [
    # Type
    {"name": "bug",              "color": "d73a4a", "description": "Something isn't working"},
    {"name": "enhancement",      "color": "a2eeef", "description": "New feature or improvement"},
    {"name": "documentation",    "color": "0075ca", "description": "Documentation only"},
    {"name": "chore",            "color": "e4e669", "description": "Build, CI, or maintenance"},
    {"name": "security",         "color": "ee0701", "description": "Security-related issue"},
    {"name": "performance",      "color": "fbca04", "description": "Performance improvement"},
    # Difficulty
    {"name": "good first issue", "color": "7057ff", "description": "Good for newcomers"},
    {"name": "help wanted",      "color": "008672", "description": "Extra attention needed"},
    # Status
    {"name": "needs triage",     "color": "ededed", "description": "Awaiting maintainer review"},
    {"name": "wontfix",          "color": "ffffff", "description": "Out of scope"},
    {"name": "duplicate",        "color": "cfd3d7", "description": "Already reported"},
    # Component
    {"name": "backend",          "color": "0e8a16", "description": "FastAPI / Python"},
    {"name": "frontend",         "color": "1d76db", "description": "Next.js / TypeScript"},
    {"name": "rag",              "color": "5319e7", "description": "Retrieval / embedding pipeline"},
    {"name": "auth",             "color": "f9d0c4", "description": "Authentication / RBAC"},
    {"name": "docker",           "color": "2496ed", "description": "Docker / infrastructure"},
    {"name": "dependencies",     "color": "0366d6", "description": "Dependency update"},
]

def main():
    if len(sys.argv) != 2:
        print("Usage: GITHUB_TOKEN=<pat> python scripts/setup-labels.py OWNER/REPO")
        sys.exit(1)

    repo  = sys.argv[1]
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)

    base = f"https://api.github.com/repos/{repo}/labels"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }

    created, skipped, failed = 0, 0, 0
    for label in LABELS:
        data = json.dumps(label).encode()
        req  = urllib.request.Request(base, data=data, headers=headers, method="POST")
        try:
            urllib.request.urlopen(req)
            print(f"  created : {label['name']}")
            created += 1
        except urllib.error.HTTPError as e:
            if e.code == 422:
                print(f"  exists  : {label['name']}")
                skipped += 1
            else:
                print(f"  FAILED  : {label['name']} ({e.code})")
                failed += 1

    print(f"\nDone — {created} created, {skipped} already existed, {failed} failed")

if __name__ == "__main__":
    main()
