# metaharness

metaharness gives your AI the best skills and harnesses for what you're making — and tells it exactly how and when to use them.

Say the outcome first: website, video, deck, research, launch, social, docs. metaharness asks a short interview, then composes a harness with minimal skill installs (over-installing degrades agents), a staged runbook, the model mix per stage (Opus for taste, Sonnet for loops, Haiku for bulk where it fits), iteration loops, verification gates, and an honest estimate of how much of your Claude plan's weekly usage the run will burn.

## Quick start

```bash
python metaharness.py list                 # see the 10 use cases
python metaharness.py run website          # interview -> composed harness
python metaharness.py registry website     # rated tools for a use case
python metaharness.py sources              # the sources behind the index
python metaharness.py validate             # self-check every data file
```

`run` writes a project folder containing:

| File | What it is |
|---|---|
| `HARNESS.md` | Your process: phases, paste-ready runbook prompts, loops, gates, and your usage budget |
| `PROCESS-CORE.md` | The operating system every harness shares: loop mechanics, verification law, session discipline |
| `INSTALL.md` | The exact install commands, deliberately minimal (piling on skills makes agents worse) |
| `.claude/CLAUDE.md` + `.claude/skills/harness-os/` | Wires the process into Claude Code so it holds across sessions |
| `estimate.json` | The machine-readable usage estimate |

Then: run INSTALL.md's commands, open Claude Code in the folder, paste the Phase 0 prompt from HARNESS.md. The harness does the rest.

## Use cases (v1)

website, video, ai-video-generation, pitch-deck, document, research, business-launch, social-content, icp-targeting, competitive-analysis.

## The index

`registry/registry.json` is an editorially rated index of the agent-tool ecosystem. Scores answer one question: does this measurably improve outcomes when composed into a harness? Install counts and star counts don't answer that. `registry/sources.json` declares every source the index reads (GitHub, Hacker News, the MCP registry, npm, plus curated directories), and `registry/research_update.py` sweeps the live ones daily, flags cross-source signals, and catches stale entries; nothing enters the registry unrated.

```bash
python registry/research_update.py    # run a scan now
```

## Honest limits

- Estimates are bands, not promises; taste iterations dominate the variance.
- The harness raises the ceiling and the floor; it does not remove the human gates (taste calls, publish decisions, payments).
- Gen-AI media (video/image models) bills separately from your Claude plan; every estimate says so where it applies.
