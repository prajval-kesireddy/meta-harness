#!/usr/bin/env python3
"""Daily market scan: finds new/rising agent-tooling on GitHub and flags
registry entries going stale. Writes candidates to INBOX.md for editorial
rating (nothing enters registry.json without a human/agent actually judging
it; unrated indexing is the failure mode of every existing directory).

Usage:  python research_update.py            # scan + stale check
Schedule (Windows):
  schtasks /Create /SC DAILY /ST 07:00 /TN metaharness-scan ^
    /TR "python <abs-path>\\research_update.py"

Stdlib only; unauthenticated GitHub API (rate limit is fine at this volume).
Set GITHUB_TOKEN env var to raise limits.
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "registry.json"
INBOX = HERE / "INBOX.md"

SWEEPS = [
    # (label, GitHub search query) — each lane catches things the others miss.
    ("claude-skills", "topic:claude-skills"),
    ("claude-code tooling", "claude-code in:name,description,topics stars:>100"),
    ("mcp servers", "topic:mcp-server stars:>50"),
    ("agent skills", "agent skills in:name,description stars:>100"),
    ("agent harness", "agent harness in:name,description,readme stars:>30"),
]
FRESH_DAYS = 14      # "pushed recently" bar
STALE_DAYS = 30      # registry entries older than this get flagged


def gh_search(query, per_page=10):
    pushed = (date.today() - timedelta(days=FRESH_DAYS)).isoformat()
    url = ("https://api.github.com/search/repositories?q="
           + urllib.parse.quote(f"{query} pushed:>{pushed}")
           + f"&sort=stars&order=desc&per_page={per_page}")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "metaharness-scan",
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
           if os.environ.get("GITHUB_TOKEN") else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("items", [])


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    known = {e["source"].rstrip("/").lower() for e in reg["entries"]}
    known |= {e["name"].lower() for e in reg["entries"]}

    lines = [f"# Scan inbox: {date.today()}", "",
             "Candidates found by the daily sweep. Rate (0-10, editorial: does it "
             "improve OUTCOMES in a composed harness?) and move keepers into "
             "registry.json, or strike through rejects with one line why.", ""]
    found = 0
    for label, query in SWEEPS:
        lines.append(f"## Lane: {label}")
        try:
            items = gh_search(query)
        except Exception as e:  # rate limit / offline: report, keep going
            lines.append(f"- SWEEP FAILED: {e}")
            continue
        for it in items:
            url = it["html_url"].rstrip("/").lower()
            if url in known:
                continue
            found += 1
            lines.append(
                f"- [ ] **{it['full_name']}** ({it['stargazers_count']}★, "
                f"pushed {it['pushed_at'][:10]}): {(it.get('description') or '')[:140]} "
                f"— {it['html_url']}")
        lines.append("")

    stale = [e for e in reg["entries"]
             if (date.today() - datetime.strptime(
                 e["last_verified"], "%Y-%m-%d").date()).days > STALE_DAYS]
    if stale:
        lines.append("## Going stale (re-verify these still exist and ship)")
        lines += [f"- [ ] {e['name']} (last verified {e['last_verified']})"
                  for e in stale]

    INBOX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Scan done: {found} new candidates, {len(stale)} stale entries "
          f"-> {INBOX}")


if __name__ == "__main__":
    main()
