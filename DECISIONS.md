# DECISIONS — engine-hardening + world-class sources + site logos

Session opened 2026-08-13. Dogfooding the Claude Code harness in-session (Praj).
Governed by site/PROCESS-CORE.md (the four laws) + the DoD below. A fresh
session must be able to resume from this file + TODO.md alone.

## The one job
Make the ENGINE the best in the world:
1. the harness-engineering pipeline (process core + composer + templates) more
   rigorous — "really really tough";
2. the market-scan/source layer sweeps the best sources on the internet
   (GitHub + Hacker News + MCP/skill registries + npm + community).
Every source gets a LOGO on the public site, and the site regenerates from the
same backend data. The registry + scan is the product; the site reports it.

## Definition of done
Engine
- research_update.py = multi-source scanner (GitHub multi-lane, Hacker News
  Algolia, MCP official registry, npm, Reddit, + configured directories),
  stdlib-only, degrades per-source, dedups across sources, ranks INBOX by a
  composite cross-source signal.
- sources.json = canonical source registry (name, url, contributes, logo,
  method); single source of truth for BOTH scanner and site.
- Composer/estimator hardened (input validation; no crash on bad data).
- Harness pipeline made tougher where it raises rigor; CLI + site build unbroken.
- `metaharness.py list|registry|run` and `research_update.py` both run green.
Site
- index.html gains a "Sources" section rendering ALL source logos from sources.json.
- Missing brand logos added (npm, MCP, Glama, skills.sh, ...).
- build_site.py regenerates from data incl. sources; webp refs rewritten;
  clean render at 1440 + 390, zero horizontal scroll.
Evidence (law 4)
- Scan output (per-source candidate counts), CLI smoke output, and desktop+mobile
  screenshots of the Sources section, all captured AFTER the final change.

## Decisions log
- D1 (2026-08-13): "latest hacker rank stuff" = Hacker News rankings; scanned via
  the open hn.algolia.com Algolia API (no auth). CONFIRMED live (8.6k story hits).
- D2 (2026-08-13): sources.json is the single source of truth shared by the
  scanner and the site build, so "site updates for every backend change" is
  structural, not manual.
- D3 (2026-08-13): Auto-scan lanes (confirmed live, no-auth, stdlib urllib):
  GitHub search (multi-lane, stars+push-recency), Hacker News (Algolia, points),
  MCP official registry (registry.modelcontextprotocol.io/v0/servers; each item
  is {server,_meta} — drill into .server), npm (registry search + downloads
  signal api.npmjs.org/downloads/point). 
- D4 (2026-08-13): Reddit hard-403s datacenter IPs even with a browser UA, so it
  is a REFERENCE source (logo+link) only; community sentiment is pulled at
  compose-time via agent-reach, never faked into the daily scan.
- D5 (2026-08-13): Curated/reference sources shown with logos (linked, not
  auto-scraped): skills.sh (install leaderboard), Glama, PulseMCP, Smithery
  (MCP directories), Product Hunt, Anthropic (official skills), awesome-claude-code
  (GitHub awesome-lists), Reddit + X (community). Confirmed via live web sweep.
- D6 (2026-08-13): INBOX ranks by a composite cross-source signal: per-source
  normalized signal (GitHub stars, HN points, npm downloads) blended, plus a
  corroboration bonus when the same repo surfaces in >1 source. Cross-source
  corroboration is the thing no existing directory computes.
- D7 (2026-08-13): FIXED a latent engine bug: load_harnesses() only stripped
  `_schema`, so the later-added `_model_doctrine` key crashed `list`/`validate`
  (any full iteration). Now strips ALL `_`-prefixed keys, matching the site
  build convention. `list` had been silently broken since that key landed.
- D8 (2026-08-13): Baked the previously-manual webp rewrite INTO build_site.py
  (assets/img/*.png -> .webp when the .webp exists on disk). One command now
  syncs the site to any backend change; removes the "rerun BOTH" footgun.
- D9 (2026-08-13): Added `overflow-x:clip` to html+body. Pre-existing hero
  glide-chips follow a desktop-width offset-path and caused mobile horizontal
  scroll (scrollW 1067 on a 390 viewport); clip is sticky-safe and satisfies the
  "zero horizontal scroll" checklist for the whole site incl. the new section.
- D10 (2026-08-13): Added a 5th process law "Live over remembered" to
  templates/PROCESS-CORE.md, tying every composed harness to the live registry +
  source scan (no trained-in defaults). Fixed README/SKILL.md drift (8 -> 10 use
  cases; SKILL now fetches sources.json too).
- D11 (2026-08-13): Registry deltas from live research (3 agents, verified):
  added OpenCode (open Claude Code alt), garrytan/gstack, affaan-m/ECC (21->24
  entries); fixed obra/superpowers install to the plugin path and BMAD org to
  bmad-code-org; mapped gstack/ECC logos; site rebuilt to 24 entries.
- D12 (2026-08-13): "Act as good as Claude Code" made durable: created
  templates/CLAUDE-CODE-DOCTRINE.md (a CONDUCT layer distilled from the verified
  Claude Code system prompt/tools via x1xhlol + top harness packs), and wired it
  into compose(), the generated .claude/CLAUDE.md + harness-os skill, a
  PROCESS-CORE pointer, and all 10 template headers. Every composed harness now
  ships the operating discipline of the best coding agents. Verified: doctrine
  file emitted + referenced in composed HARNESS.md.
- D13 (2026-08-13): Harness parity — added sharp numbered audit checklists to the
  four produce-and-audit templates that lacked them (video = Frame & cut,
  ai-video-generation = Continuity, social-content = Post, document = Prose &
  typeset) and wired each into its produce-audit loop, matching website/pitch-deck.

## Strategy pivot (2026-08-14): free tool + stars, prescription-first, non-code-first
Backed by live competitive research (3 agents, verified 2026-08-14).
- NOT selling. Free + open (MIT), optimized for GitHub stars. Front door flips
  from the marketing site to the repo README.
- REFRAME: drop "intuition of the best in the world." The value is concrete:
  "the best skills + best harnesses, and exactly HOW and WHEN to use them."
  PRESCRIPTION, not a ranked directory. We tell you what to use for your goal.
- LEAD WITH NON-CODE OUTCOMES (website, video, deck, research, launch, social,
  docs). Dev harnesses are owned by gstack (128k), superpowers (272k), ECC
  (240k) — do NOT compete there; hand off to them for pure code.
- Competitive finding: directories LIST/RANK; the big packs PRESCRIBE-HOW but
  bundle everything always-on, coding-only. Nobody does outcome-interview ->
  minimal composed stack -> staged runbook (which skill at which stage,
  model-per-stage, verification gates) -> honest token budget. Wedge is OPEN
  but replicable; moat = non-code coverage + runbook quality + honest budgets +
  the daily cross-source scan actually running.
- Demand verified: Anthropic itself admitted token-quota anxiety; "too many
  tools makes agents worse" is documented (context bloat). Anthropic's MCP Tool
  Search partly solves minimal-install, so lead with how/when/model + budget,
  not just "install fewer."
- Best-in-class today (honest): obra/superpowers is the consensus best tool.
- Path forward (verdict agent: tool is ~60% to must-star; missing 40%):
  (1) reposition non-code-first + prescription; (2) ship ONE devastating
  bare-vs-harnessed before/after (the viral hook); (3) automate the daily scan
  (cron) — index rot is existential; (4) star scaffolding (root README, LICENSE,
  CONTRIBUTING, topics); (5) publish the scan output + methodology.

### Shipped this pivot (2026-08-14, verified)
- Root front door created: README.md (prescription-first, non-code-first, honest
  quickstart, "menu/buffet/recipe" pitch), LICENSE (MIT, Prajval Kesireddy),
  CONTRIBUTING.md (how to rate a tool / add a source / add a harness). MIT +
  daily-scan Action badges wired.
- Index-rot fixed: .github/workflows/daily-scan.yml runs research_update.py daily
  (+ workflow_dispatch), commits INBOX.md/registry.json if changed. Needs the repo
  pushed + Actions enabled to go live.
- Repositioned off "intuition": site hero/subcopy, metaharness/README.md,
  skills/metaharness/SKILL.md, CLAUDE.md — all now prescription + non-code-first.
  "intuition" = 0 occurrences repo-wide. Site rebuilds green (10/24/13, 38 webp);
  localhost:8414 serves the new hero.
- STILL OPEN (highest-leverage next): the bare-vs-harnessed evidence gallery
  (the must-star hook); publish the scan publicly; then push + launch.

## Status (2026-08-13): SHIPPED
Engine: multi-source scanner live (GitHub + Hacker News + MCP registry + npm),
183 unique candidates / cross-source corroboration working; sources.json =
13 sources; metaharness.py hardened with `validate` + `sources`, all green
("10 blueprints, 21 registry entries, 13 sources — all valid"). Site: #sources
section renders all 13 real logos from sources.json, desktop + mobile clean,
zero horizontal scroll, 38 webp refs rewritten by the build. Evidence captured
via headless screenshots + scan/CLI output. NOT pushed (awaiting Praj's "push").
