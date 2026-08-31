#!/usr/bin/env python3
"""Daily market scan: sweeps the best sources on the internet for new/rising
agent tooling, ranks candidates by a CROSS-SOURCE signal (a tool surfacing in
more than one source is the thing no other directory computes), and flags
registry entries going stale. Writes ranked candidates to INBOX.md for
editorial rating — nothing enters registry.json without a human/agent actually
judging it; unrated indexing is the failure mode of every existing directory.

Sources come from sources.json (the same file the public site renders), so the
scan and the site never drift. Live lanes (method=github|hackernews|
mcp-registry|npm) are swept here; reference/community lanes are curated and
pulled at compose-time.

Usage:  python research_update.py            # scan + rank + stale check
Schedule (Windows):
  schtasks /Create /SC DAILY /ST 07:00 /TN metaharness-scan ^
    /TR "python <abs-path>\\research_update.py"
Schedule (cron):  0 7 * * *  python <abs-path>/research_update.py

Stdlib only; unauthenticated public APIs (rate limits are fine at this volume).
Set GITHUB_TOKEN to raise the GitHub limit and speed the sweep.
"""

import json
import math
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "registry.json"
SOURCES = HERE / "sources.json"
INBOX = HERE / "INBOX.md"

FRESH_DAYS = 14      # "pushed/posted recently" bar for the live lanes
STALE_DAYS = 30      # registry entries older than this get flagged
UA = "metaharness-scan"
GH_SLEEP = 0.5 if os.environ.get("GITHUB_TOKEN") else 6.0  # respect the 10/min unauth limit

# Per-signal log normalizers: raw -> 0..1. Denominator = the log10 that scores
# a 1.0 (stars 5.7 => ~500k stars = 1.0, so the 100k-300k tier spreads instead
# of flat-lining; hn 3.4 => ~2.5k points; npm 7.0 => ~10M weekly downloads).
NORMDEN = {"stars": 5.7, "hn_points": 3.4, "npm_dl": 7.0}
FRESH_BASE = 0.30    # a freshly-published item with no popularity signal yet
CORROBORATION = 0.18 # bonus per extra source a candidate appears in


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json", "User-Agent": UA,
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
           if "api.github.com" in url and os.environ.get("GITHUB_TOKEN") else {}),
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def extract_repo(url):
    """github.com/owner/repo(.git)?/... -> 'owner/repo' (lowercased), else None."""
    if not url:
        return None
    m = re.search(r"github\.com[/:]+([^/]+)/([^/#?]+)", url, re.I)
    if not m:
        return None
    owner, repo = m.group(1), re.sub(r"\.git$", "", m.group(2))
    if owner.lower() in ("sponsors", "topics", "search", "features"):
        return None
    return f"{owner}/{repo}".lower()


def norm(kind, raw):
    if raw and raw > 0 and kind in NORMDEN:
        return min(1.0, math.log10(raw + 1) / NORMDEN[kind])
    if kind == "fresh":
        return FRESH_BASE
    return 0.0


# --------------------------------------------------------------- fetchers
# Each returns a list of candidate dicts:
#   {name, url, desc, repo(optional), kind, raw, source}

def fetch_github(cfg):
    out, pushed = [], (date.today() - timedelta(days=FRESH_DAYS)).isoformat()
    for i, q in enumerate(cfg.get("queries", [])):
        if i:
            time.sleep(GH_SLEEP)
        url = ("https://api.github.com/search/repositories?q="
               + urllib.parse.quote(f"{q} pushed:>{pushed}")
               + "&sort=stars&order=desc&per_page=10")
        try:
            items = get(url).get("items", [])
        except Exception as e:
            out.append({"_error": f"github '{q}': {e}"})
            continue
        for it in items:
            out.append({
                "name": it["full_name"], "url": it["html_url"],
                "desc": (it.get("description") or "")[:150],
                "repo": it["full_name"].lower(), "kind": "stars",
                "raw": it.get("stargazers_count", 0), "source": "github",
                "extra": f"pushed {it['pushed_at'][:10]}",
            })
    return out


def fetch_hackernews(cfg):
    out, minp = [], cfg.get("min_points", 20)
    for q in cfg.get("queries", []):
        url = ("https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=15&query="
               + urllib.parse.quote(q)
               + "&numericFilters=" + urllib.parse.quote(f"points>={minp}"))
        try:
            hits = get(url).get("hits", [])
        except Exception as e:
            out.append({"_error": f"hackernews '{q}': {e}"})
            continue
        for h in hits:
            link = h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}"
            out.append({
                "name": (h.get("title") or "")[:150], "url": link,
                "desc": (h.get("title") or "")[:150],
                "repo": extract_repo(h.get("url")), "kind": "hn_points",
                "raw": h.get("points", 0), "source": "hackernews",
                "extra": f"{h.get('num_comments', 0)} comments",
            })
    return out


def fetch_mcp_registry(cfg):
    out = []
    url = f"https://registry.modelcontextprotocol.io/v0/servers?limit={cfg.get('limit', 50)}"
    try:
        servers = get(url).get("servers", [])
    except Exception as e:
        return [{"_error": f"mcp-registry: {e}"}]
    for item in servers:
        s = item.get("server", item) if isinstance(item, dict) else {}
        name = s.get("name", "")
        repo_url = (s.get("repository") or {}).get("url") if isinstance(s.get("repository"), dict) else None
        repo = extract_repo(repo_url) or (name.split("io.github.")[-1].lower()
                                          if name.startswith("io.github.") else None)
        out.append({
            "name": name, "url": repo_url or "https://registry.modelcontextprotocol.io",
            "desc": (s.get("description") or "")[:150], "repo": repo,
            "kind": "fresh", "raw": 0, "source": "mcp-registry",
            "extra": "official MCP registry",
        })
    return out


def fetch_npm(cfg):
    out, enrich = [], cfg.get("enrich_top", 8)
    seen = []
    for q in cfg.get("queries", []):
        url = ("https://registry.npmjs.org/-/v1/search?size=12&text="
               + urllib.parse.quote(q))
        try:
            objs = get(url).get("objects", [])
        except Exception as e:
            out.append({"_error": f"npm '{q}': {e}"})
            continue
        for o in objs:
            pkg = o.get("package", {})
            name = pkg.get("name")
            if not name or name in seen:
                continue
            seen.append(name)
            links = pkg.get("links", {})
            repo_url = links.get("repository") or ""
            out.append({
                "name": name, "url": repo_url or links.get("npm") or f"https://www.npmjs.com/package/{name}",
                "desc": (pkg.get("description") or "")[:150],
                "repo": extract_repo(repo_url), "kind": "npm_dl",
                "raw": 0, "source": "npm", "extra": "npm package",
                "_pkg": name,
            })
    # Enrich the strongest few with real weekly downloads (hard usage signal).
    for c in out[:enrich]:
        if "_pkg" not in c:
            continue
        try:
            d = get("https://api.npmjs.org/downloads/point/last-week/"
                    + urllib.parse.quote(c["_pkg"], safe="@/"))
            c["raw"] = d.get("downloads", 0)
            c["extra"] = f"{c['raw']:,}/wk downloads"
        except Exception:
            pass
    return out


FETCHERS = {"github": fetch_github, "hackernews": fetch_hackernews,
            "mcp-registry": fetch_mcp_registry, "npm": fetch_npm}


# --------------------------------------------------------------- aggregate

def canonical_key(c):
    return c.get("repo") or (c.get("url", "") or c.get("name", "")).rstrip("/").lower()


def aggregate(candidates, known):
    """Dedup across sources; keep best per-kind signal; union sources."""
    merged = {}
    for c in candidates:
        if "_error" in c:
            continue
        key = canonical_key(c)
        if not key or key in known:
            continue
        m = merged.get(key)
        if not m:
            m = {"name": c["name"], "url": c["url"], "desc": c.get("desc", ""),
                 "repo": c.get("repo"), "sources": set(), "signals": {},
                 "extra": {}}
            merged[key] = m
        m["sources"].add(c["source"])
        m["extra"][c["source"]] = c.get("extra", "")
        kind, raw = c["kind"], c.get("raw", 0)
        if raw >= m["signals"].get(kind, -1):
            m["signals"][kind] = raw
        # prefer a longer/real description and a github url
        if len(c.get("desc", "")) > len(m["desc"]):
            m["desc"] = c["desc"]
        if "github.com" in (c.get("url") or "") and "github.com" not in m["url"]:
            m["url"] = c["url"]
    for m in merged.values():
        best = max((norm(k, v) for k, v in m["signals"].items()), default=0.0)
        m["composite"] = min(1.4, best + CORROBORATION * (len(m["sources"]) - 1))
        m["heat"] = round(m["composite"] * 100)
    return merged


def signal_detail(m):
    bits = []
    order = [("stars", "★"), ("hn_points", "HN"), ("npm_dl", "npm"), ("fresh", "new")]
    for kind, label in order:
        if kind in m["signals"]:
            v = m["signals"][kind]
            bits.append(f"{label} {v:,}" if v else label)
    return " · ".join(bits) or "listed"


# --------------------------------------------------------------- main

def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]
    by_id = {s["id"]: s for s in sources}

    known = set()
    for e in reg["entries"]:
        known.add(e["name"].lower())
        r = extract_repo(e.get("source", ""))
        if r:
            known.add(r)

    all_cands, per_source, errors = [], {}, []
    for s in sources:
        method = s.get("scan", {}).get("method")
        fetcher = FETCHERS.get(method)
        if not fetcher:
            continue
        cands = fetcher(s["scan"])
        errs = [c["_error"] for c in cands if "_error" in c]
        errors += errs
        good = [c for c in cands if "_error" not in c]
        per_source[s["id"]] = len(good)
        all_cands += good

    merged = aggregate(all_cands, known)
    ranked = sorted(merged.values(), key=lambda m: -m["composite"])
    corroborated = [m for m in ranked if len(m["sources"]) > 1]

    # ---- write INBOX.md
    L = [f"# Scan inbox: {date.today()}", "",
         "Ranked candidates from the daily multi-source sweep. Rate 0-10 "
         "(editorial: does it improve OUTCOMES in a composed harness?) and move "
         "keepers into registry.json, or strike a reject with one line why. "
         "Signal is cross-source: a ★ marks a tool that surfaced in more than "
         "one source, which is the strongest buy signal here.", "",
         f"Sources swept live: " + ", ".join(
             f"{by_id[k]['name']} ({per_source[k]})" for k in per_source) + ".",
         f"Unique candidates: {len(merged)} · corroborated (>1 source): "
         f"{len(corroborated)}.", ""]

    L += ["## Ranked candidates (cross-source signal)", ""]
    for m in ranked[:30]:
        star = " ★" if len(m["sources"]) > 1 else ""
        srcs = "+".join(sorted(m["sources"]))
        L.append(f"- [ ] **{m['name']}** — heat {m['heat']}{star} "
                 f"[{srcs}] · {signal_detail(m)} — {m['desc']} — {m['url']}")
    L.append("")

    # per-lane sections for editorial context
    for sid in per_source:
        lane = [m for m in ranked if sid in m["sources"]]
        if not lane:
            continue
        L.append(f"## Lane: {by_id[sid]['name']}")
        for m in lane[:10]:
            L.append(f"- [ ] {m['name']} ({signal_detail(m)}) — {m['url']}")
        L.append("")

    if errors:
        L.append("## Sweep errors (degraded lanes; scan continued)")
        L += [f"- {e}" for e in errors]
        L.append("")

    stale = [e for e in reg["entries"]
             if (date.today() - datetime.strptime(
                 e["last_verified"], "%Y-%m-%d").date()).days > STALE_DAYS]
    if stale:
        L.append("## Going stale (re-verify these still exist and ship)")
        L += [f"- [ ] {e['name']} (last verified {e['last_verified']})" for e in stale]
        L.append("")

    INBOX.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Scan done: {len(merged)} unique candidates "
          f"({len(corroborated)} corroborated), {len(stale)} stale, "
          f"{len(errors)} lane errors -> {INBOX.name}")
    for sid, n in per_source.items():
        print(f"  {by_id[sid]['name']:16} {n} candidates")


if __name__ == "__main__":
    main()
