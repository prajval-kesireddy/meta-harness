# Competitive map: Meta-Harness

Subject: a tool that interviews you about the OUTCOME you want (website, video, deck, research, business, content), then composes and installs the best current harness for it (skills + MCPs + process runbook + verification loops), with an honest token-cost estimate. Public face: a rated, daily-refreshed index of the best agent tools. Decision this feeds: build / keep building. Sweep run 2026-08-13, sources fetched live.

## Lane 1: Direct (closest to the wedge)

**davila7/claude-code-templates (aitmpl.com)** — CONFIRMED 2026-08-13. The closest existing thing: open-source CLI + web dashboard, ~1,000 components (agents, commands, skills, hooks, MCPs, settings), one-command install into Claude Code. Where it stops: it's a parts store with a search box. No outcome interview, no composition logic (it installs what you pick, it doesn't pick), no process runbooks, no token estimates, and it's aimed at developers configuring dev workflows, not outcomes like "a video" or "a launch."
- Threat: HIGH on surface overlap, MEDIUM on the actual wedge.

**skills.sh (Vercel, Jan 2026)** — CONFIRMED. The skill registry with real install-count leaderboards (find-skills ~3M installs, frontend-design ~760k), refreshed daily. Owns distribution AND the popularity signal. Where it stops: popularity is not curation (installs measure marketing, not outcomes), no bundles/stacks, no process layer, no cost honesty.
- Threat: HIGH for the public-index moat. Competing with skills.sh on "directory" loses; competing on OPINION (rated, tested, combined into stacks) is open.

**Anthropic itself** — the platform risk. Claude Code already ships find-skills, plugin marketplaces, and native skill suggestions; Anthropic ships official skills (frontend-design, pptx, pdf, docx). If Anthropic builds outcome-based harness composition natively, the private tool becomes a feature. History says platforms absorb the generic version and leave the opinionated version alone.
- Threat: STRUCTURAL. Mitigation: be the opinionated cross-ecosystem layer (skills + MCPs + non-Anthropic tools + process), move faster than a platform can.

## Lane 2: Process frameworks (own "harness engineering" for code)

- **GitHub spec-kit** (~80k stars) — spec-driven development, the biggest. Code only.
- **BMAD-METHOD** (~37k stars) — 20+ persona agents, 50+ guided workflows. Heavy (users report ~230M tokens/week on big projects, $800-2,000/mo API), dev-focused, steep learning curve. Its weight is the complaint surface: people want the outcomes without adopting a religion.
- **obra/superpowers, claude-flow, agent-os** — process/orchestration for software work.
- Threat: LOW-MEDIUM directly (all code-centric), HIGH as pattern proof: the market already pays attention to "process beats prompts." None of them serve "I want a great video/deck/launch."

## Lane 3: Directories (the saturated lane)

Skill directories: claudemarketplaces.com (23,600+ skills), claudeskills.info, skillselion, majiayu000/claude-skill-registry. MCP directories: Glama (22,775 servers), mcp.so, PulseMCP, Smithery, mcp.directory, mcpreview (community ratings), official registry.modelcontextprotocol.io. Plus static awesome-lists (awesome-claude-code, awesome-harness-engineering).
- Threat to "another directory": FATAL — this lane is done. Threat to a RATED, TESTED, stack-combination index: LOW, because none of them run the tools. Their common ceiling: they index metadata (stars, installs); nobody publishes "we ran this harness stack and here's the output quality."

## Lane 4: Non-consumption (the real competitor)

Most target users currently: paste prompts raw into Claude/ChatGPT and accept mediocre output, or pay vertical SaaS per outcome (Framer/Lovable/v0 for sites, Runway/OpusClip for video, Gamma/Beautiful.ai for decks, Jasper for content). The vertical tools are the honest benchmark: they deliver decent outcomes with ZERO setup. The meta-harness pitch against them is control + quality ceiling + one subscription (your Claude plan) instead of five SaaS bills.

## Complaint mining (what buyers keep saying, nobody ships)

1. "Too many skills installed makes the agent WORSE" (HN/Reddit, repeatedly) → prescriptive minimal-install is a feature nobody markets.
2. "Which of the 900k skills actually work?" → trust/rating layer missing everywhere; install counts don't answer it.
3. "36.7% of public MCP servers have SSRF holes, 41% no auth" (BlueRock) → security vetting as part of curation is unclaimed.
4. "Claude forgets its skills mid-session" → process files + hooks (the harness OS) fix what installs alone don't.
5. Token anxiety: usage limits are the #1 recurring complaint thread; NOBODY publishes honest per-task burn estimates.

## Where we lose (honest)

- Anyone already deep in BMAD/spec-kit for code work: not our buyer, they're served.
- A non-technical person who wants a website in 10 minutes: Lovable/Framer beats us on time-to-first-output; we win on ceiling, not floor.
- If skills.sh adds editorial curation + bundles, the public-index moat halves overnight.
- The index rots without the daily scan actually running. A stale "best tools" page is worse than none.

## Verdict

Wedge is real and currently unoccupied: outcome interview → composed minimal harness → process runbook → honest token budget, across NON-CODE outcomes, backed by a rated index that actually tests stacks. Directory alone: dead on arrival. Composer + tested-stack ratings + cost honesty: differentiated. Full reasoning and adoption read: delivered in chat 2026-08-13.
