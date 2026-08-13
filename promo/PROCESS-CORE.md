# Harness operating system (shared core)

Every metaharness-generated harness runs on the same operating system. The use-case file you're reading this from defines WHAT to build; this file defines HOW the agent works. Copy both into the project; the agent must follow both.

## The four laws

1. **Definition of done before work.** The first phase of every harness produces a concrete, checkable definition of done. No phase starts until its exit condition is written down. "Looks good" is not an exit condition; "all 9 checklist items pass on the live URL" is.

2. **Loops, not passes.** Quality comes from iteration with fresh eyes, never from one careful attempt. Every loop has: a produce step, an audit step against a written checklist, and an exit condition (checklist passes, or 2 consecutive iterations produce no material improvement). Cap loops at 6 iterations; if not converging by then, the checklist is wrong: stop and fix the checklist.

3. **Audit with a different instrument than you produced with.** Code gets audited by rendering it and looking at pixels. Prose gets audited by reading it aloud-in-head as the target reader. Claims get audited by trying to refute them. Never let the agent grade its own homework in the same modality it did the homework.

4. **Verify before claiming done.** Every "it's finished" requires evidence gathered AFTER the last change: the actual screenshot, the actual render, the actual test output, the actual live URL fetched. A claim without post-change evidence is a lie the agent hasn't caught yet.

## The loop library

**Design loop (visual things: pages, slides, frames, images).**
Produce -> screenshot at real viewport sizes (desktop 1440, mobile 390) -> audit against the design checklist -> fix the top 3 issues only -> re-screenshot -> repeat. Fixing everything at once each round causes regressions; top-3 keeps each iteration reviewable. The design checklist lives in the use-case file.

**Build-verify loop (functional things: features, pipelines, scripts).**
Write the failing check first (test, or a concrete manual probe) -> implement -> run the check -> only then next unit. When a bug appears: reproduce it first, state the hypothesis, then fix. Never stack a second fix on an unverified first fix.

**Research loop (finding things out).**
Sweep from multiple angles (each angle is blind to the others) -> dedup -> verify load-bearing claims by trying to refute them -> log to the source ledger -> ask "what would I expect to exist that I haven't found?" -> sweep again. Exit: 2 consecutive sweeps surface nothing new.

**De-slop loop (anything a human will read).**
Draft -> strip AI tells (run the humanizer skill: inflated symbolism, rule-of-three, mirrored contrasts, vague attribution, filler) -> read as the actual target reader -> tighten. Exit: nothing left that a sharp reader would clock as machine-written.

## Session and context discipline

- One phase per session when phases are big. Long sessions degrade: the agent stops re-reading its own rules. Each phase's runbook prompt is written to be pasted into a FRESH session.
- State lives in files, never in chat: decisions in DECISIONS.md, open items in TODO.md, the definition of done in the harness file. A new session must be able to resume from files alone.
- When a session drifts (agent arguing with the checklist, repeated failed fixes), kill it and restart from files. Restarting is cheaper than steering a drifted context.

## Budget discipline

- The estimate in your HARNESS.md is a budget, not trivia. At each phase boundary, note roughly how much of the budget is spent (wall-clock agent-hours is a fine proxy).
- If a phase runs 2x its share of the estimate, stop: the scope is wrong or the loop isn't converging. Cut scope deliberately instead of grinding.

## Escalation to the human

The agent stops and surfaces (instead of guessing) only for: credentials/accounts, paying for anything, publishing anywhere public, deleting things it didn't create, and any decision the harness file marks as a USER GATE. Everything else: make the best call, write it in DECISIONS.md, keep moving.
