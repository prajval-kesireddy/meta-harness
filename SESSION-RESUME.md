# SESSION-RESUME — Meta-Harness (single entry point to resume 100%)

Last updated: 2026-08-31 ~02:45 EST. This is the ONE resume file (merged from the
2026-08-13 founding session, the 2026-08-13 evening engine session, and the
2026-08-31 push session). Read this + `DECISIONS.md` (D1–D13) + `TODO.md` +
`CLAUDE.md`. Everything below is verified green unless marked otherwise.
**Everything through commit `521606d` is PUSHED and LIVE.**

---

## 0. Identity, rules, environment
- **Repo:** `prajval-kesireddy/meta-harness`, nested inside the Work repo (intentional,
  Praj's call). Its OWN repo. **Push rule:** when Praj says "push" with no detail, run
  `git push origin main:main`. Vercel project "metaharness" is linked to the repo and
  auto-deploys on push → **https://metaharness.vercel.app**.
- **Hook trap:** the block-git hook regexes ANY `-f` in a chained command as force-push.
  NEVER chain `rm -f` / `add -f` with a push. (This is why the mp4 gitignore got scoped
  to `promo/` instead of using `git add -f`.)
- **Dogfood directive (Praj):** operate under the product's own harness IN sessions here:
  the five laws, state in files (DECISIONS.md/TODO.md), loops with evidence, no skipped
  gates. The site itself was built by running `metaharness.py run website` on itself.
- **Environment:** Windows 11, cwd = repo root, PowerShell (fresh process per call — no
  cd/env persistence), tools: git, gh, curl, python, node, go. Playwright + chromium
  cached; Remotion in `promo/` (its ffmpeg via `npx remotion ffmpeg` — the ms-playwright
  ffmpeg build can't decode h264).
- **Gotchas:** (a) `site/assets/img/*.png` is gitignored — the deploy serves `.webp`;
  `build_site.py` bakes the png→webp ref rewrite in; `site/assets/logos/*.png` DO commit.
  (b) Browser pane blocks raw localhost → headless Playwright for screenshots (a
  `.claude/launch.json` attach config on port 8414 also works when the pane is displayed).
  (c) Remotion: hooks before any early return or React #310 at random frames.
  (d) Full-page Playwright screenshots show a phantom card tint (stitching artifact) —
  verify with computed styles before "fixing".
  (e) Vertex 429s hard on bursts: generate in pairs + ~25s sleep, retry singles.
  (f) Higgsfield CloudFront URLs join as `..._<timestamp>_<jobid>.png` (underscore, not slash).

## 1. What the product is (and why)
Praj's thesis: output quality is set by the HARNESS around the model (skills installed,
loops, verification), and nobody composes that layer per outcome. Product = CLI + data +
site + installable skill that composes the best current harness for an OUTCOME, with the
token bill stated up front. The moat is the live market analysis: the rated index + daily
multi-source scan of the ecosystem, prescribing the stack COMBINATIONS that win right now.
Positioning line (site hero): "Give your AI the intuition of the best in the world at any task."
Framing on the site: everything you make is three inputs — model, resources, skills+process —
and we rule the third. Voting system: explicitly KILLED by Praj (Supabase project
"metaharness" sits empty; deletable). Non-code outcomes first; pure code hands off to
gstack/superpowers/ECC/OpenCode.

- `metaharness/metaharness.py` — CLI: `list | validate | sources | registry [uc] | run <uc> [--yes --answers FILE --out DIR --plan pro|max5x|max20x]`.
  Interview (3-4 questions, count stated up front), estimator (agent-hour bands ×
  uncertainty 0.7–1.6, % of Pro/Max5x/Max20x weekly), composer (HARNESS.md with pipeline +
  per-stage models, PROCESS-CORE.md, CLAUDE-CODE-DOCTRINE.md, INSTALL.md incl. conditional
  installs like reference-stealing tools only when a reference URL was given, `.claude/`
  wiring + harness-os skill, estimate.json).
- `metaharness/harnesses.json` — **10** blueprints: website, video, pitch-deck, document,
  research, business-launch, social-content, ai-video-generation, icp-targeting,
  competitive-analysis. Each: exactly 3-4 questions (website: reference→type→assets→extras,
  per Praj's spec), staged pipeline (stage/what/stack/model/loop), estimator mults,
  installs, MCPs. `_`-prefixed keys (`_schema`, `_model_doctrine`) stripped on load.
  Model doctrine: Opus where taste concentrates, Sonnet production loops, Haiku bulk.
- `metaharness/templates/` — PROCESS-CORE.md (5 laws; 5th = "Live over remembered") +
  CLAUDE-CODE-DOCTRINE.md (conduct layer distilled from the x1xhlol Claude Code internals
  extraction + top harness packs) + 10 runbook templates with numbered audit checklists
  wired into their loops (video=Frame & cut, ai-video-generation=Continuity,
  social-content=Post, document=Prose & typeset, parity with website/pitch-deck).
- `metaharness/registry/` — `registry.json` (**24** rated entries, editorial 0-10 scores on
  "does it improve outcomes composed into a harness", last_verified dates),
  `sources.json` (**13** sources; single source of truth for scanner AND site so they can't
  drift), `research_update.py` (multi-source daily scan), `INBOX.md` (scan output, rate
  candidates into registry.json manually).
- `site/` — 3 pages: `index.html` (single-scroll marketing, FintechX-copied),
  `harnesses.html` (explorer: 2 tabs — harness pipelines + rated index — with search),
  `resources.html` ($300 Gemini ADC guide: ~2,200 2K images ≈ ~4,500 Higgsfield credits).
  `build_site.py` regenerates index+harnesses from harnesses.json + registry.json +
  sources.json (webp rewrite baked in). `assets/logos/` = real tool logos (Praj rule:
  referenced tool with findable logo MUST show it).
- `skills/metaharness/SKILL.md` — installable skill; fetches harnesses.json +
  registry.json + sources.json from raw.githubusercontent LIVE (never memory), states
  question count, bill-before-work, composes, then tailors 2-3 questions deeper.
  Interview may continue at gates (pick an aesthetic after research, approve script before
  render) — staged, never nagging.
- `promo/` — Remotion promo (27s, 1080p, field-catalog aesthetic beat sheet in SCRIPT.md;
  renders gitignored).
- `COMPETITION.md` — live competitive map. Verdict: composer + tested-stack ratings + cost
  honesty = unoccupied wedge; directory-alone = dead lane. Direct-ish: davila7/
  claude-code-templates (catalog, no composition), skills.sh (install-count leaderboard),
  garrytan/gstack (~128k★, celebrity one-size code harness), affaan-m/ECC (~240k★, code).
  Threats: Anthropic absorbing it natively; skills.sh adding editorial bundles; vertical
  SaaS on time-to-first-output. Weaknesses Praj knows: ratings are n=1 editorial until the
  evidence gallery exists; index rots without the daily scan run+rated.

## 2. Design system (the site) — evolution + current state
- **v1 (retired):** cream "field catalog" editorial look (Fraunces/Source Serif/Plex Mono).
- **v2 (LIVE):** FintechX copy per Praj (reference https://fintechx-wbs.framer.website/,
  probed live): white ground, ink #1D1D1D, gray #4D585F, panel #EDF1F4, blue #1D4ED8 lead
  accent, dark #05080C blocks; Bricolage Grotesque display + Inter body + IBM Plex Mono
  data; pill buttons; giant centered hero with inline badge chip; floating dark terminal
  card over the hero visual showing the real 4-question interview.
- **Art direction (Praj, locked):** 2D flat illustration CARDS in a BLUE-LEANING PASTEL
  palette (powder/sky/cornflower blue leads; blush/butter/mint accents; warm off-white
  ground; "pastel is a texture"; no purple takeover, green never leads — the first
  all-green set was rejected and regenerated). 3D-rendered stills for BACKGROUNDS only
  (section washes at ~.16 opacity). Motion is CODE-DRIVEN like FintechX (recorded via
  Playwright: elements enter at opacity 0 + translateY(20px), spring with tiny overshoot,
  per-element viewport trigger, ~80ms stagger; hero gets a load cascade). Plus 3
  Higgsfield grain motion LOOPS as mp4 (dots-pipeline band before outcomes grid; dark
  dots river forming the three-bar logo in the bill section; silk waves above footer;
  ~650KB each, first-frame posters). Baked ambient AI landscape videos = rejected.
- **Logo:** three stacked offset rounded bars (white/blue/white on ink rounded square),
  inline SVG everywhere + assets/favicon.svg.
- **Generation stack + spend (2026-08-13):** Higgsfield ~220 credits (24 stills + 3 loops,
  ~95 credits left); Gemini ADC ~$8 (2D cards + extras). Higgsfield default, Gemini ADC
  when Praj calls it. nano_banana_pro = 2 credits/1k image; minimax_h3 loops = 20/ea.

## 3. Shipped by session
**Founding session (2026-08-13 day):** 3-stage plan executed: Stage 1 core product
(8→10 harnesses, interview, composer, estimator, registry, GitHub-only scan v1) verified
end-to-end; Stage 2 dogfood (site via its own website harness with 3+ design loops; 27s
Remotion promo via the video harness incl. the React #310 hooks fix); Stage 3 ship
(repo → GitHub main, Vercel live). Competitive analysis delivered in chat via its own
harness process. FintechX redesign, 24 Higgsfield stills, logo, resources page,
in-session skill, first pastel regen (rejected), blue-pastel regen (accepted), motion
loops, entrance animation system.

**Engine session (2026-08-13 evening) — all verified:**
- **Multi-source scan (the moat):** `research_update.py` GitHub-only → GitHub multi-lane +
  Hacker News (hn.algolia.com) + MCP official registry (registry.modelcontextprotocol.io/
  v0/servers, items are `{server,_meta}`) + npm (search + api.npmjs.org/downloads).
  Stdlib only, per-source degradation, cross-source dedup, INBOX ranked by composite
  cross-source corroboration signal (a repo in >1 source ranks up — no directory computes
  this). Verified: **183 unique candidates, 0 lane errors** unauthenticated. Reddit
  hard-403s datacenter IPs → reference-source only (sentiment via agent-reach at
  compose-time).
- **CLI hardening:** `validate` (structural self-check incl. logo-file existence) +
  `sources` commands; bug fixed where `_model_doctrine` crashed `list`/`validate`
  (now strips all `_` keys); stdout reconfigured utf-8 for Windows consoles.
- **Site Sources section:** 13 source logos from sources.json (tiles + marquee, live/
  curated tags); new logos (npm, modelcontextprotocol, awesomelists, ycombinator, skills,
  glama, pulsemcp, smithery; refreshed producthunt/reddit/x). Mobile overflow fixed
  (`overflow-x:clip` on html+body), zero h-scroll verified at 1440+390.
- **Doctrine:** CLAUDE-CODE-DOCTRINE.md created and wired into compose() + all 10
  template headers. Research answer preserved: Claude Code core is CLOSED
  ("All Rights Reserved"; npm ships a compiled binary) but open three ways — internals
  extracted (x1xhlol Prompt.txt/Tools.json), MIT reimplementations (OpenCode, claw-code,
  shareAI-lab/learn-claude-code), `.claude` packs (superpowers, gstack, ECC).
  Recommendation: run OpenCode, upgrade-in-place with superpowers.
- **Registry deltas:** +OpenCode, +gstack, +ECC (21→24); superpowers install corrected to
  `/plugin install superpowers@claude-plugins-official`; BMAD org → `bmad-code-org`.
- **Open-source packaging:** README, LICENSE (MIT), CONTRIBUTING, .github.

**Push session (2026-08-31):** committed everything above as `521606d` (27 files,
+821/−199, secret-scan clean), pushed to main, Vercel redeploy verified live (sources
section serving). Then this resume merge.

## 4. Verify / rebuild commands
```
cd metaharness            ; python metaharness.py validate   # -> 10 blueprints, 24 entries, 13 sources, valid
                            python metaharness.py list|sources|registry website
                            python metaharness.py run website --yes --out <tmp>   # composes; emits CLAUDE-CODE-DOCTRINE.md
cd metaharness\registry   ; $env:GITHUB_TOKEN=(gh auth token); python research_update.py   # scan -> INBOX.md
cd site                   ; python build_site.py             # -> 24 entries, 13 sources (4 live), webp refs rewritten
```
Screenshots: headless Playwright (site/_audit.py pattern) over localhost or `file://`;
serve locally with `serve.ps1 -Dir <site> -Port 8414` (pid file
`%TEMP%\claude-localhost-8414.pid`). Delete temp `_*.py` / `_*.png` after (gitignored anyway).

## 5. Open items / next steps (nothing blocking)
1. Rate the INBOX.md candidates (183 from the verified scan) into registry.json.
2. Cron the daily scan (schtasks/cron snippet in research_update.py docstring) and surface
   the dated index publicly (search-traffic flywheel).
3. Evidence gallery: same brief run bare vs harnessed, outputs side by side — this is what
   makes the ratings defensible and is the marketing.
4. skills.sh listing / distribution push for `npx skills add prajval-kesireddy/meta-harness`.
5. (Optional) Surface the coding-agent doctrine on the site as a selling point.
6. Research follow-ups flagged by agents: verify `charmbracelet/crush`, `earendil-works/pi`,
   `ruvnet/claude-flow` vs `ruflo` before indexing.
7. Housekeeping: empty Supabase project "metaharness" deletable from dashboard; Remotion
   promo's terminal beat still says "3 questions" (site says 4) — refresh before using the
   video anywhere public.

## 6. Claude Code transcript location for these sessions
Everything in this file happened inside the Claude Code project folder
`C:\Users\amark\.claude\projects\C--Users-amark-Downloads-Demos-Work-Side-Hustles-Meta-Harness\`
(the slug for this workstream folder). Contents as of 2026-08-31:
- `5e923bae-7a95-48ed-8ce7-da8b478160f8.jsonl` — the full transcript of the founding
  session (2026-08-13 day: stages 1-3, FintechX redesign, pastel/motion pass) which was
  resumed on 2026-08-31 for the push + this resume merge. ~17MB.
- `memory/` — that project's persistent memory dir.
The 2026-08-13 evening engine session (multi-source scan, doctrine, packaging) ran in this
same project folder; if its transcript isn't listed above it was compacted/cleared, and its
full state is preserved in §3 here + DECISIONS.md + TODO.md.

## 7. Retained backing docs (keep, this file is the entry point)
`DECISIONS.md` (D1–D13 + status), `TODO.md` (engine-session checklist, 14/14 complete),
`CLAUDE.md` (workstream rules + where-we-left-off), `COMPETITION.md` (full map),
`site/DESIGN-NOTES.md` (v1 art direction; superseded by §2 here), `promo/SCRIPT.md`.
conversations.md is retired everywhere; never recreate it.
