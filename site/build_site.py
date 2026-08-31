#!/usr/bin/env python3
"""Builds index.html + harnesses.html from live data (registry ratings +
harness blueprints + sources). Re-run after every registry, blueprint or
sources update; the webp rewrite is baked in. resources.html is static."""

import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
MH = HERE.parent / "metaharness"

UNCERTAINTY = (0.7, 1.6)

# Official logo per registry entry / tool keyword (Praj rule: if a referenced
# tool has a findable logo, it gets used).
LOGOS = {
    "anthropics/skills: frontend-design": "anthropic.svg",
    "anthropics/skills: pptx": "anthropic.svg",
    "anthropics/skills: pdf + docx": "anthropic.svg",
    "obra/superpowers": "github.svg",
    "playwright MCP": "playwright.svg",
    "humanizer": "github.svg",
    "remotion skill": "remotion.svg",
    "agent-reach": "github.svg",
    "wshobson/agents": "github.svg",
    "GSAP skills (core + ScrollTrigger)": "greensock.svg",
    "context7 MCP": "upstash.svg",
    "ffmpeg": "ffmpeg.svg",
    "Vercel deploy (CLI or MCP)": "vercel.svg",
    "ElevenLabs TTS": "elevenlabs.svg",
    "spec-kit": "github.svg",
    "BMAD-METHOD": "github.svg",
    "davila7/claude-code-templates": "github.svg",
    "skills.sh registry": "vercel.svg",
    "firecrawl MCP": "firecrawl.png",
    "Gemini image gen (Vertex AI)": "googlegemini.svg",
    "Lighthouse CI": "lighthouse.svg",
    "garrytan/gstack": "github.svg",
    "affaan-m/ECC": "github.svg",
}

STAGE_TOOL_LOGOS = {
    "frontend-design": "anthropic.svg", "playwright": "playwright.svg",
    "humanizer": "claude.svg", "gsap": "greensock.svg", "remotion": "remotion.svg",
    "ffmpeg": "ffmpeg.svg", "pptx": "anthropic.svg", "pdf": "anthropic.svg",
    "docx": "anthropic.svg", "lighthouse": "lighthouse.svg", "vercel": "vercel.svg",
    "netlify": "vercel.svg", "gemini": "googlegemini.svg", "agent-reach": "github.svg",
    "subagent": "claude.svg", "elevenlabs": "elevenlabs.svg", "tts": "elevenlabs.svg",
    "firecrawl": "firecrawl.png", "google fonts": "googlegemini.svg",
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def stage_logos(stack):
    low, seen, out = stack.lower(), set(), []
    for key, logo in STAGE_TOOL_LOGOS.items():
        if key in low and logo not in seen:
            seen.add(logo)
            out.append(f'<img src="assets/logos/{logo}" alt="" title="{esc(stack)}">')
    return "".join(out[:3])


LIVE_METHODS = {"github", "hackernews", "mcp-registry", "npm"}


def build_source_tiles(sources):
    """The Sources section: every source we index from, with its real logo and
    what it contributes. Rendered from registry/sources.json so the site can
    never claim a source the scanner doesn't actually read (or vice versa)."""
    tiles = []
    for s in sources:
        live = s.get("scan", {}).get("method") in LIVE_METHODS
        tag = "live scan" if live else s.get("category", "")
        cls = " live" if live else ""
        tiles.append(f"""
      <div class="srctile reveal">
        <div class="srctile-top"><img src="assets/logos/{s['logo']}" alt="{esc(s['name'])}" title="{esc(s['name'])}"><span class="srctile-tag{cls}">{esc(tag)}</span></div>
        <div class="srctile-name">{esc(s['name'])}</div>
        <p class="srctile-what">{esc(s['contributes'])}</p>
      </div>""")
    return "\n".join(tiles)


def build_source_marquee(sources):
    """A logo river of every source, duplicated for a seamless marquee."""
    row = "".join(f'<img src="assets/logos/{s["logo"]}" alt="{esc(s["name"])}" title="{esc(s["name"])}">'
                  for s in sources)
    return row + row


def build_index_rows(entries):
    rows = []
    for i, e in enumerate(sorted(entries, key=lambda x: -x["score"]), 1):
        logo = LOGOS.get(e["name"])
        logo_html = (f'<img class="row-logo" src="assets/logos/{logo}" alt="">'
                     if logo else '<div class="row-logo-blank"></div>')
        rows.append(f"""
      <div class="row" data-search="{esc(e['name'].lower())} {esc(e['type'])} {esc(e['why'].lower())}">
        {logo_html}
        <div>
          <div class="row-name">{esc(e['name'])} <span class="row-type">{esc(e['type'])}</span></div>
          <p class="row-why">{esc(e['why'])}</p>
          <div class="row-meta">verified {e['last_verified']} &middot; <a href="{e['source']}" style="color:var(--blue)">source</a></div>
        </div>
        <div class="row-score">{e['score']}<i>/10</i></div>
      </div>""")
    return "\n".join(rows)


def build_harness_cards(harnesses):
    cards = []
    for key, b in harnesses.items():
        lo = b["base_agent_hours"] * UNCERTAINTY[0]
        hi = b["base_agent_hours"] * 2.0 * UNCERTAINTY[1]
        nq = len(b["questions"])

        qs = []
        for i, q in enumerate(b["questions"], 1):
            detail = ("free answer" if q.get("freeform")
                      else " / ".join(o["label"].split(" (")[0] for o in q["options"]))
            qs.append(f"""
        <div class="hq"><div class="hq-no">Q{i}</div>
          <div><div class="hq-prompt">{esc(q['prompt'])}</div>
          <div class="hq-detail">{esc(detail)}</div></div></div>""")

        stages = []
        for i, s in enumerate(b.get("pipeline", []), 1):
            stages.append(f"""
        <div class="rstage">
          <div class="rstage-model">{s['model']}</div>
          <div class="rstage-name">{i}. {esc(s['stage'])}</div>
          <div class="rstage-what">{esc(s['what'])}</div>
          <div class="rstage-tools">{stage_logos(s['stack'])}</div>
        </div>""")

        blob = (b["title"] + " " + b["tagline"] + " " + key + " " +
                " ".join(s["stage"] for s in b.get("pipeline", []))).lower()
        cards.append(f"""
    <article class="hcard" id="{key}" data-search="{esc(blob)}">
      <div class="hcard-head"><h3>{esc(b['title'])}</h3>
        <div class="hcard-est">{lo:.0f}&ndash;{hi:.0f} agent-hours typical</div></div>
      <p class="hcard-tag">{esc(b['tagline'])}</p>
      <div class="qhead">{nq} questions. That's the whole interview. (Follow-ups come later, at gates where you have something to react to.)</div>
      <div class="hq-list">{''.join(qs)}</div>
      <div class="qhead">Then the pipeline runs:</div>
      <div class="ribbon" style="margin-top:0"><div class="ribbon-track">{''.join(stages)}</div></div>
    </article>""")
    return "\n".join(cards)


def main():
    registry = json.loads((MH / "registry" / "registry.json").read_text(encoding="utf-8"))
    harnesses = json.loads((MH / "harnesses.json").read_text(encoding="utf-8"))
    harnesses = {k: v for k, v in harnesses.items() if not k.startswith("_")}
    sources = json.loads((MH / "registry" / "sources.json").read_text(encoding="utf-8"))["sources"]
    live_n = sum(1 for s in sources if s.get("scan", {}).get("method") in LIVE_METHODS)
    tokens = {
        "{{HARNESS_CARDS}}": build_harness_cards(harnesses),
        "{{INDEX_ROWS}}": build_index_rows(registry["entries"]),
        "{{ENTRY_COUNT}}": str(len(registry["entries"])),
        "{{UPDATED}}": registry.get("updated", str(date.today())),
        "{{SOURCE_TILES}}": build_source_tiles(sources),
        "{{SOURCE_MARQUEE}}": build_source_marquee(sources),
        "{{SOURCE_COUNT}}": str(len(sources)),
        "{{LIVE_SOURCE_COUNT}}": str(live_n),
    }

    # Bake the previously-manual webp rewrite into the build: any assets/img/*.png
    # ref becomes .webp when that .webp exists on disk (the deployed PNGs are
    # gitignored). One command now keeps the site in sync with the backend.
    imgdir = HERE / "assets" / "img"
    rewrites = [0]

    def to_webp(html):
        def repl(m):
            rel = m.group(1)
            name = rel.rsplit("/", 1)[-1]
            if (imgdir / (name[:-4] + ".webp")).exists():
                rewrites[0] += 1
                return rel[:-4] + ".webp"
            return rel
        return re.sub(r"(assets/img/[A-Za-z0-9_\-]+\.png)", repl, html)

    for tpl, out in (("template_index.html", "index.html"),
                     ("template_tool.html", "harnesses.html")):
        html = (HERE / tpl).read_text(encoding="utf-8")
        for k, v in tokens.items():
            html = html.replace(k, v)
        html = to_webp(html)
        (HERE / out).write_text(html, encoding="utf-8")
    print(f"Built index.html + harnesses.html: {len(harnesses)} harnesses, "
          f"{len(registry['entries'])} index entries, {len(sources)} sources "
          f"({live_n} live), {rewrites[0]} webp refs rewritten.")


if __name__ == "__main__":
    main()
