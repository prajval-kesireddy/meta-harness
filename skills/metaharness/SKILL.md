---
name: metaharness
description: Use when the user wants a great OUTCOME from their AI (a website, video, pitch deck, document, research report, business launch, social content system, or competitive analysis) rather than help with existing code. Composes the best current harness for that outcome: minimal skill installs, a staged pipeline with per-stage model calls, iteration loops, verification gates, and an honest token budget. Trigger on "build me a website/video/deck", "I want to launch", "research X for me", "analyze my competition", or any ask where the deliverable is an outcome, not a code change.
---

# metaharness: compose the best harness for what they're doing

You are about to do what the best practitioners do by hand: engineer the working layer around the model before doing the work. Follow this exactly.

## Step 1: Get the blueprint (live, never from memory)

Fetch these two files from the source of truth:
- https://raw.githubusercontent.com/prajval-kesireddy/meta-harness/main/metaharness/harnesses.json
- https://raw.githubusercontent.com/prajval-kesireddy/meta-harness/main/metaharness/registry/registry.json

If offline, use a local clone if present; otherwise say the index is unreachable and continue with the conversation's best judgment, flagged as unverified.

## Step 2: The interview (short, stated up front)

Match the user's ask to one of the 8 use cases. Tell them how many questions you have BEFORE asking (blueprints carry 3-4), then ask ONLY those questions, conversationally, in one message. If their original request already answered a question, don't re-ask it; say what you inferred.

The interview is allowed to continue LATER, at pipeline gates where the user has something concrete to react to: after idea research, present 3 aesthetic directions and ask them to pick; before a render, get the script approved. Tell them up front which gates will come back to them, so the process feels staged, never nagging.

## Step 3: State the bill before composing

From the blueprint's estimator params, tell them: estimated agent-hours as a band, roughly what % of their plan's weekly usage (ask which plan only if unknown), and any costs outside the plan (media generation, paid APIs). This is a hard rule of the product: the bill comes before the work.

## Step 4: Compose the harness

Create in the project folder:
- `HARNESS.md`: the blueprint's pipeline (stage, model, stack, exit condition per stage), phase runbook prompts, definition of done, their answers, and the estimate.
- `PROCESS-CORE.md`: fetch from https://raw.githubusercontent.com/prajval-kesireddy/meta-harness/main/metaharness/templates/PROCESS-CORE.md
- `.claude/CLAUDE.md` + `.claude/skills/harness-os/SKILL.md`: wire the process so it survives sessions.
- `INSTALL.md`: the blueprint's installs plus any conditional ones (reference-stealing installs only if they gave a reference URL). Keep it MINIMAL; over-installing skills degrades agents, and saying so is part of the product's honesty.

## Step 5: Tailor beyond the blueprint

This is where you beat the static CLI. With the harness composed, go deeper on THEIR specifics: their taste (ask for one thing they love and one they hate in the category), their existing assets, their constraints (deadline, budget, brand rules). Fold every answer into HARNESS.md as config notes and extra checklist lines. Two or three tailoring questions max; never overbear.

## Step 6: Run it

Offer to start Phase 0 immediately. Follow HARNESS.md and PROCESS-CORE.md to the letter: the stated model per stage, the loops to their written exit conditions, evidence before any "done" claim, and the budget checked at each phase boundary.
