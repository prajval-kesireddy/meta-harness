# Meta-Harness workstream

Global rules apply (~/.claude/CLAUDE.md). Editing sessions here reply with PART 2 ack.

## What this is
A side project: a meta-harness tool. People using AI coding agents get mediocre outcomes because they run a bare harness. This tool interviews the user about the outcome they want (website, video, document, business asset, etc.), then composes and installs the best current harness for that outcome: the right skills, the right process loops (design iteration, verification passes, screenshot audits), the right tools from the live ecosystem. It also tells the user up front what quality to expect and roughly what share of their Claude plan's weekly usage the run will burn.

## Push rule (Praj, 2026-08-13)
This workstream has its OWN repo: https://github.com/prajval-kesireddy/meta-harness.git. When Praj says "push" or "push it" with no other detail, push to `main` of that repo. This overrides the default work-repo-branch pattern for this folder only. The folder is nested inside the Work repo; the nested repo is intentional.

## Core mentality (Praj, 2026-08-13)
The real value of this free, open MIT product is prescribing the right tool stack for each outcome: the latest GitHub tools, skills, MCPs, and the specific stack COMBINATIONS that reliably improve websites, videos, decks, research, launches, social, docs, and other non-code outputs. The registry + daily market scan powers the prescription; the harness composer is the delivery mechanism. Every blueprint must reflect what's winning right now, with sources and last-verified dates, never trained-knowledge defaults.

## Product shape (Praj, 2026-08-13)
- Free + open (MIT), star-optimized: the public site explains and proves the prescription engine, not a paid funnel. It is not an ordered popularity chart; ratings exist to decide what improves outcomes when composed into a harness.
- Installed tool: composes the harness inside a session. Asks a couple of questions max (never overbearing), honest about token expectations, hyper-prescriptive once it knows the goal: what to install, how to use it, when to use it, and which model to run per stage. It reads from the same index the public site shows.
- Positioning angle: metaharness gives your AI the best skills and harnesses for what you're making — and tells it exactly how and when to use them. Lead with non-code outcomes; for pure code, hand off to gstack/superpowers/ECC.

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
- 2D flat illustrations for CARD images in a BLUE-LEANING PASTEL palette (Praj 2026-08-13 evening: powder blue/periwinkle leads, mint/blush/butter accents, warm off-white ground; "pastel is a texture", the first all-green set was rejected). 3D-rendered-elements stills for BACKGROUNDS only; motion is CODE-DRIVEN like FintechX (probed: no videos, no CSS anims, Framer-Motion JS transforms) — parallax, glide chips on offset-path, marquee, floating terminal. Baked AI ambient videos of landscapes = rejected. Generation stack: Higgsfield by default, Gemini ADC fine when Praj calls for it (he did for the pastel regen).
- Site is 3 pages: index.html (single-scroll marketing, FintechX-copied), harnesses.html (explorer: 2 tabs + search), resources.html ($300 Gemini ADC guide). build_site.py regenerates from harnesses.json + registry.json, then the webp-optimize snippet rewrites refs (rerun BOTH after data edits).

## Where we left off
- 2026-08-13 ~17:45 EST: ALL SHIPPED + pastel/motion pass done. Live at https://metaharness.vercel.app (Vercel project linked to GitHub, deploys on push; push via `git push origin main:main`; the block-git hook regexes any `-f` as force-push, so never chain `rm -f`/`add -f` with a push command). 10 harnesses, blue-led pastel 2D cards (Gemini ADC), 3 Higgsfield grain motion loops (dots pipeline band, logo dots river in the bill section, silk waves above footer; mp4 ignore now scoped to promo/). Hero has a load cascade + FintechX-recorded spring reveals. Higgsfield spend total ~220 credits (~95 left); Gemini ~$8 total. Supabase project "metaharness" empty (voting killed); deletable. Next: rate INBOX.md candidates, cron the daily scan, evidence gallery (bare vs harnessed), skills.sh listing.
