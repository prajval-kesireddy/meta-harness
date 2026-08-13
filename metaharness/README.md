# metaharness

Give your AI the intuition of the best in the world at any task.

A layer sits between your prompt and great output: the harness. Which skills are installed, how the work loops, what gets verified before "done." The people getting jaw-dropping results from the same models you use have simply engineered that layer, and almost nobody else knows it exists. metaharness asks you two or three questions about the outcome you want, then composes that layer for you: the exact skills and tools worth installing (from a rated, daily-refreshed index of the whole ecosystem, never from stale defaults), the process runbook the best practitioners actually follow, the verification loops that catch slop before you see it, and an honest estimate of how much of your Claude plan's weekly usage the run will burn.

## Quick start

```bash
python metaharness.py list                 # see the 8 use cases
python metaharness.py run website          # interview -> composed harness
python metaharness.py registry website     # rated tools for a use case
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

website, video, pitch-deck, document, research, business-launch, social-content, competitive-analysis.

## The index

`registry/registry.json` is the moat: an editorially RATED index of the agent-tool ecosystem. Scores answer one question: does this measurably improve outcomes when composed into a harness? Install counts and star counts don't answer that, which is why every existing directory, at any size, still leaves you guessing. `registry/research_update.py` sweeps GitHub daily for new candidates and flags stale entries; nothing enters the registry unrated.

```bash
python registry/research_update.py    # run a scan now
```

## Honest limits

- Estimates are bands, not promises; taste iterations dominate the variance.
- The harness raises the ceiling and the floor; it does not remove the human gates (taste calls, publish decisions, payments).
- Gen-AI media (video/image models) bills separately from your Claude plan; every estimate says so where it applies.
