# SESSION-RESUME — Meta-Harness (single entry point to resume 100%)

Last updated: 2026-08-13 ~18:37 EST. Read this + `DECISIONS.md` (D1–D13) +
`TODO.md`. Everything below is verified green unless marked otherwise. Nothing
has been pushed this session.

---

## 0. Identity, rules, environment
- **Repo:** `prajval-kesireddy/meta-harness`, nested inside the Work repo (intentional).
  Its OWN repo. **Push rule:** when Praj says "push", run `git push origin main:main`
  (Vercel auto-deploys → https://metaharness.vercel.app). The block-git hook regexes any
  `-f` as force-push — NEVER chain `rm -f`/`add -f` with a push command.
- **Dogfood directive (Praj):** operate under the Claude Code harness IN this session —
  the four/five laws, state in files (DECISIONS.md/TODO.md), loops with evidence, no
  skipped gates. I have been doing this.
- **Environment:** Windows, cwd = repo root, PowerShell (fresh process per call — no cd/env
  persistence), tools: git, gh, curl, python, node, go. Use Windows `\` paths.
- **Gotchas:** (a) `site/assets/img/*.png` is gitignored — the deploy serves `.webp`, so the
  build rewrites img refs to webp; `site/assets/logos/*.png` are NOT ignored (they commit).
  (b) Browser pane blocks localhost → use headless Playwright for screenshots.
  (c) Remotion: hooks before any early return. (d) Full-page screenshots show a phantom
  card tint (stitching artifact) — verify with computed styles.

## 1. What the product is
CLI + data + site + skill that composes the best harness for an OUTCOME.
- `metaharness/metaharness.py` — CLI: `list | validate | sources | registry [uc] | run <uc> [--yes --out DIR --plan]`.
- `metaharness/harnesses.json` — **10** blueprints (website, video, pitch-deck, document,
  research, business-launch, social-content, ai-video-generation, icp-targeting,
  competitive-analysis). Note two underscore keys (`_schema`, `_model_doctrine`) are stripped on load.
- `metaharness/templates/*.md` — PROCESS-CORE (5 laws) + **CLAUDE-CODE-DOCTRINE** (conduct) + 10 runbooks.
- `metaharness/registry/` — `registry.json` (**24** rated entries), `sources.json` (**13** sources,
  single source of truth for scanner + site), `research_update.py` (multi-source daily scan), `INBOX.md` (scan output).
- `site/` — 3 pages (index/harnesses/resources). `build_site.py` regenerates index.html +
  harnesses.html from harnesses.json + registry.json + sources.json and **bakes the webp rewrite in**.
- `skills/metaharness/SKILL.md` — the installable skill (fetches harnesses.json + registry.json + sources.json live).
- `promo/` — Remotion promo video.

## 2. Everything shipped THIS session (all verified)
**A. Multi-source scan engine (the moat).**
- `research_update.py` rewritten GitHub-only → **multi-source**: GitHub (multi-lane),
  Hacker News (hn.algolia.com Algolia API), MCP official registry
  (registry.modelcontextprotocol.io/v0/servers — items are `{server,_meta}`), npm
  (search + `api.npmjs.org/downloads` signal). Stdlib only; degrades per-source; dedups
  across sources; ranks INBOX by a **composite cross-source signal** (a repo in >1 source
  gets a corroboration bonus — the thing no directory computes). Verified run: **183 unique
  candidates, 0 lane errors** unauthenticated. Reddit hard-403s datacenter IPs → it's a
  REFERENCE source only (community sentiment via agent-reach at compose-time).
- `sources.json` (13 sources) drives BOTH scanner and site → backend↔site can't drift.

**B. CLI hardening.**
- Added `validate` (structural self-check of harnesses/registry/sources incl. logo-file
  existence) and `sources` commands.
- **Bug fixed:** `load_harnesses()` only stripped `_schema`; the later `_model_doctrine`
  key crashed `list`/`validate`. Now strips ALL `_`-prefixed keys. Also `sys.stdout`
  reconfigured to utf-8 for Windows consoles.
- PROCESS-CORE gained a **5th law "Live over remembered"** (no trained-in defaults).

**C. Site "Sources" section + logos (Praj: "logos are crucial to report").**
- New `#sources` section on index.html renders **all 13 source logos** from sources.json
  (`build_source_tiles` + `build_source_marquee`), with live/curated tags.
- Logos added to `site/assets/logos/`: `npm.svg`, `modelcontextprotocol.svg`,
  `awesomelists.svg`, `ycombinator.svg` (Hacker News), `skills.png`, `glama.svg`,
  `pulsemcp.png`, `smithery.png` (+ refreshed producthunt/reddit/x from simple-icons).
- `build_site.py`: renders sources; **webp rewrite baked in** (assets/img/*.png→.webp when
  the webp exists); LOGOS map extended (gstack/ECC→github.svg).
- **Mobile overflow fixed** (pre-existing hero glide-chips): `overflow-x:clip` on html+body.
  Verified zero horizontal scroll at 1440 + 390 via headless Playwright.

**D. "Act as good as Claude Code" + harness quality.**
- Created `templates/CLAUDE-CODE-DOCTRINE.md` — CONDUCT layer distilled from the verified
  Claude Code internals (x1xhlol extraction) + top harness packs. Wired into `compose()`
  (copies into every generated project), generated `.claude/CLAUDE.md` + `harness-os` skill,
  a PROCESS-CORE pointer, and all **10 template headers**.
- Added sharp numbered audit checklists to the produce-loop templates that lacked them and
  wired each into its loop: video = **Frame & cut**, ai-video-generation = **Continuity**,
  social-content = **Post**, document = **Prose & typeset** (parity with website/pitch-deck).

**E. Registry deltas (from 3 parallel research agents, verified live).**
- Added: **OpenCode** (the open Claude Code alt), **garrytan/gstack**, **affaan-m/ECC** (21→**24**).
- Fixed: obra/superpowers install → `/plugin install superpowers@claude-plugins-official`;
  BMAD source org → `bmad-code-org`.

## 3. The research answer (context for the registry deltas)
"Is the Claude Code harness open source?" → **Core is CLOSED** (`anthropics/claude-code` is
"All Rights Reserved"; repo = issue tracker + plugin examples; npm ships a compiled binary).
But it's open THREE ways: **internals extracted** (`x1xhlol/system-prompts-and-models-of-ai-tools`
has Prompt.txt + Tools.json), **reimplementations you can run** (OpenCode, claw-code,
shareAI-lab/learn-claude-code — MIT, run on ANTHROPIC_API_KEY), and **`.claude` packs**
(superpowers, gstack, ECC). Recommendation given: run **OpenCode**, upgrade-in-place with **superpowers**.

## 4. Verify / rebuild commands
```
cd metaharness            ; python metaharness.py validate   # -> 10 blueprints, 24 entries, 13 sources, valid
                            python metaharness.py list|sources|registry website
                            python metaharness.py run website --yes --out <tmp>   # composes; emits CLAUDE-CODE-DOCTRINE.md
cd metaharness\registry   ; $env:GITHUB_TOKEN=(gh auth token); python research_update.py   # scan -> INBOX.md
cd site                   ; python build_site.py             # -> 24 entries, 13 sources (4 live), 38 webp refs
```
Screenshots: headless Playwright over a `file://` URL (site/_audit.py or a temp script);
localhost is blocked in the browser pane. Delete temp `_*.py` / `_*.png` after.

## 5. Todos — ALL DONE (14/14 this session; SQL `todos` table is per-session/non-persistent)
research-sources, sources-json, scan-rewrite, composer-harden, pipeline-rigor, logos-add,
site-sources-section, site-rebuild-verify (engine+site pass); harness-official-internals,
harness-oss-reimplementations, harness-dotclaude-packs (research lanes);
apply-registry-deltas, doctrine-wire, template-checklists (this pass).

## 6. Open items / next steps (nothing blocking)
1. **PUSH** — not done. `git push origin main:main` → Vercel redeploys. Awaiting Praj's "push".
2. (Optional, offered) Surface the new coding-agent doctrine on the site as a selling point.
3. Backlog from CLAUDE.md: rate remaining `INBOX.md` candidates into registry; cron the daily
   scan (schtasks/cron snippet in research_update.py docstring); evidence gallery (bare vs
   harnessed); skills.sh listing.
4. Research follow-ups the agents flagged: verify `charmbracelet/crush` (Go OpenCode fork),
   `earendil-works/pi`, and `ruvnet/claude-flow` vs `ruflo` before indexing.

## 7. Changed/new files this session (git status intent)
Modified: metaharness/{README.md, metaharness.py, registry/INBOX.md, registry/registry.json,
registry/research_update.py, templates/*.md (PROCESS-CORE + all 10 runbooks)},
site/{assets/site.css, build_site.py, index.html, harnesses.html, template_index.html,
assets/logos/{producthunt,reddit,x,ycombinator}.svg}, skills/metaharness/SKILL.md.
New (untracked): DECISIONS.md, TODO.md, SESSION-RESUME.md,
metaharness/registry/sources.json, metaharness/templates/CLAUDE-CODE-DOCTRINE.md,
site/assets/logos/{awesomelists.svg, glama.svg, modelcontextprotocol.svg, npm.svg,
pulsemcp.png, skills.png, smithery.png}.

## 8. Retained backing docs (NOT session-resume files; keep)
`DECISIONS.md` (decision log D1–D13 + "Status: SHIPPED"), `TODO.md` (checklist, all complete),
`CLAUDE.md` (workstream context), `COMPETITION.md` (competitive map). This SESSION-RESUME.md
is the single entry point; the others hold the detail.
