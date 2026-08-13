# Meta-Harness workstream

Global rules apply (~/.claude/CLAUDE.md). Editing sessions here reply with PART 2 ack.

## What this is
A side project: a meta-harness tool. People using AI coding agents get mediocre outcomes because they run a bare harness. This tool interviews the user about the outcome they want (website, video, document, business asset, etc.), then composes and installs the best current harness for that outcome: the right skills, the right process loops (design iteration, verification passes, screenshot audits), the right tools from the live ecosystem. It also tells the user up front what quality to expect and roughly what share of their Claude plan's weekly usage the run will burn.

## Push rule (Praj, 2026-08-13)
This workstream has its OWN repo: https://github.com/prajval-kesireddy/meta-harness.git. When Praj says "push" or "push it" with no other detail, push to `main` of that repo. This overrides the default work-repo-branch pattern for this folder only. The folder is nested inside the Work repo; the nested repo is intentional.

## Core mentality (Praj, 2026-08-13)
The real value of this product is analyzing the whole market: the latest and greatest GitHub tools, skills, MCPs, and the specific stack COMBINATIONS practitioners are using that reliably produce outcomes. The registry + daily market scan is the product; the harness composer is the delivery mechanism. Every blueprint must reflect what's winning right now, with sources and last-verified dates, never trained-knowledge defaults.

## Product shape (Praj, 2026-08-13)
- Moat: indexing + RATING the best tools on the internet. The public website is a rated directory of the best stuff, refreshed by the daily market scan, and it markets the private tool.
- Private tool: installed, then composes the harness inside a session. Asks a couple of questions max (never overbearing), honest about token expectations, hyper-prescriptive once it knows the goal. It reads from the same index the public site shows.
- Marketing angle: give your AI the intuition of the best in the world at any task (best designer for websites, best editor for videos, and so on). That is literally what the harness install does.

## Key decisions
- 2026-08-13: Three-stage plan. Stage 1 = the core product (8 use-case harnesses incl. competitive-analysis, interview flow, harness composer, usage estimator, live registry + daily market-scan updater), shipped and verified end to end. Stage 2 = dogfood, runs IMMEDIATELY after Stage 1 in the same session (Praj directive): website harness builds this tool's own site, video harness path for its promo. Stage 3 = distribution (publish, registry listings, public daily scan, launch).
- 2026-08-13: Praj asked for the competitive landscape of this tool itself; keep COMPETITION.md current.
- Form factor: a Claude Code plugin/skill pack plus a Python CLI, because the target user already runs Claude Code and the harness IS the .claude folder it generates.

## Layout
- `metaharness/` the product: metaharness.py CLI, harnesses.json (8 blueprints), templates/ (PROCESS-CORE + 8 process templates), registry/ (registry.json rated index, research_update.py daily scan, INBOX.md candidates).
- `site/` public site: template.html + build_site.py (regenerates index.html from registry.json; rerun after registry edits). Served detached on port 8414 via serve.ps1 (pid file %TEMP%\claude-localhost-8414.pid). LAN: http://172.20.20.20:8414.
- `promo/` Remotion promo video (SCRIPT.md beat sheet, src/, out/promo.mp4).
- `COMPETITION.md` live competitive map.

## Gotchas
- Browser pane blocked raw localhost navigation; use preview_start with .claude/launch.json attach config, or headless Playwright (site/_audit.py) for design-loop screenshots.
- Full-page Playwright screenshots show a phantom tint on some grid cards (stitching artifact); verify with computed styles before "fixing".
- Remotion: hooks (useCurrentFrame etc.) must be called before any early return in a component or rendering dies with React #310 at random frames.

## Art direction (Praj, 2026-08-13, evening)
- 2D flat illustrations (emerald/cream, Higgsfield nano_banana_pro) for CARD images; 3D-rendered-elements stills for BACKGROUNDS only; motion is CODE-DRIVEN like FintechX (probed: no videos, no CSS anims, Framer-Motion JS transforms) — parallax, glide chips on offset-path, marquee, floating terminal. Baked AI ambient videos of landscapes = rejected. ONLY Higgsfield for generation from here on out (overrides the global Gemini rule for this workstream).
- Site is 3 pages: index.html (single-scroll marketing, FintechX-copied), harnesses.html (explorer: 2 tabs + search), resources.html ($300 Gemini ADC guide). build_site.py regenerates from harnesses.json + registry.json, then the webp-optimize snippet rewrites refs (rerun BOTH after data edits).

## Where we left off
- 2026-08-13 ~16:45 EST: ALL THREE STAGES SHIPPED. Live at https://metaharness.vercel.app (Vercel project "metaharness" linked to the GitHub repo, deploys on push to main; push works via `git push origin main:main`). 10 harnesses (added ai-video-generation, icp-targeting), 4-question website interview, pipelines with per-stage models, installable skill at skills/metaharness/. Higgsfield spend this session ~160 credits (~154 left). Supabase project "metaharness" exists empty (voting was killed); delete from dashboard if unwanted. Videos in site/assets/vid committed but unused (pulled per 2D-motion directive). Next: rate INBOX.md candidates, cron the daily scan, evidence gallery (bare vs harnessed), skills.sh listing.
