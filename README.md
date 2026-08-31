# metaharness

metaharness gives your AI the best skills and harnesses for what you're making — and tells it exactly how and when to use them.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![daily scan](https://github.com/prajval-kesireddy/meta-harness/actions/workflows/daily-scan.yml/badge.svg)](https://github.com/prajval-kesireddy/meta-harness/actions/workflows/daily-scan.yml)

## What it is

metaharness is a free, MIT-licensed front door for outcome-first AI work: websites, videos, pitch decks, deep research, launch kits, social content, documents, ICP work, competitive analysis, and AI video.

You say the outcome you want. metaharness runs a short interview, then composes a harness: minimal skills/MCPs, a staged runbook with the right model per stage, evidence-based verification gates, and an honest token-budget estimate before you start.

## Quickstart

No package install exists yet. Clone the repo and run the stdlib Python CLI:

```powershell
git clone https://github.com/prajval-kesireddy/meta-harness.git
cd meta-harness
python metaharness\metaharness.py list
python metaharness\metaharness.py run website
```

For defaults without the interview:

```powershell
python metaharness\metaharness.py run website --yes
```

The Claude skill lives here:

```text
skills\metaharness\SKILL.md
```

Useful real commands:

```powershell
python metaharness\metaharness.py registry website
python metaharness\metaharness.py sources
python metaharness\metaharness.py validate
```

Current validation output:

```text
OK: 10 blueprints, 24 registry entries, 13 sources — all structurally valid.
```

Current `list` output begins:

```text
Use cases:

  website                A designed, deployed website that does not look AI-generated.
  video                  A finished rendered video: explainer, promo, or short-form.
  pitch-deck             A designed deck (.pptx or PDF) that reads investor-grade, not clip-art.
```

## How it works

1. **Short interview** — a few questions about the outcome, scope, references, assets, and constraints.
2. **Minimal install set** — only the skills/MCPs that help this outcome. Over-installing measurably degrades agents; restraint is a feature.
3. **Staged runbook** — which skill to use at which stage, which model to use per stage (Opus for taste/judgment, Sonnet for production loops, Haiku for bulk), iteration loops, and verification gates that demand evidence.
4. **Budget before burn** — an agent-hours band and rough share of your Claude plan's weekly usage before the run starts.

Example: the website harness starts with taste/reference capture, moves through copy and visual-system choices, builds with Sonnet, loops on real screenshots, adds motion, then ships only after performance/accessibility checks and live-URL evidence.

## The outcomes

| Harness | What it makes |
|---|---|
| `website` | A designed, deployed website that does not look AI-generated. |
| `video` | A finished rendered video: explainer, promo, or short-form. |
| `pitch-deck` | A designed deck (.pptx or PDF) that reads investor-grade, not clip-art. |
| `document` | A polished long-form document: report, whitepaper, ebook, proposal. |
| `research` | A genuinely researched answer to a hard question, with receipts. |
| `business-launch` | Name, brand, landing page, and first-customers outreach system for a new business. |
| `social-content` | A 30-day content system for one platform: pillars, hooks, posts, and visuals. |
| `ai-video-generation` | Cinematic AI footage that holds together: shots, continuity, and a finished cut. |
| `icp-targeting` | Figure out exactly who buys, find them, and say the right thing to each segment. |
| `competitive-analysis` | A real map of your market: who's winning, why, and where the opening is. |

Pure coding is not the fight here. For software-only work, metaharness can hand off to strong coding packs like gstack, superpowers, or ECC instead of pretending every job is the same job.

## The rated index + daily scan

The harnesses are backed by `metaharness\registry\registry.json`: a rated index of tools, skills, MCPs, APIs, and packs scored on whether they improve outcomes when composed into a harness.

A daily cross-source scan watches GitHub, Hacker News, the MCP registry, npm, and curated sources. The public directory is here: <https://metaharness.vercel.app>.

## Why prescription beats ranking

A directory gives your agent a menu. A giant always-on pack gives it a buffet.

metaharness gives it a recipe: which tools, in what order, under which model, with which checks before moving on. That matters because the best tool at the wrong stage is just expensive noise.

## Honest limits

- Estimates are bands, not promises; taste loops and rework create variance.
- Media generation, paid APIs, and external services can bill separately from your Claude plan.
- The harness raises the floor and ceiling, but the human still makes taste calls, publish calls, and business calls.
- The package story is early: clone + Python CLI works today; pip/npx-style installs are coming.

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), especially if you want to rate a new tool, add a scan source, or improve a harness blueprint.

## License

MIT. See [LICENSE](LICENSE).
