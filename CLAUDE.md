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

## Where we left off
- 2026-08-13: workstream created, Stage 1 build starting.
