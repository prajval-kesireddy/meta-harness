# AI video generation harness

Read PROCESS-CORE.md and CLAUDE-CODE-DOCTRINE.md first: PROCESS-CORE governs how every loop below runs, the doctrine governs how you conduct yourself (concise, convention-following, no unsolicited changes, evidence before done).

## Your configuration

{{ANSWERS}}

{{ADDENDA}}

## Usage budget

{{ESTIMATE}}

Generation spend note: video model credits/API costs sit OUTSIDE your Claude plan and usually exceed the agent-time cost. Budget 1.5-2x generations per kept shot; a 10-shot film means planning for 15-20 generations. The harness preflights per-shot cost before burning anything.

## Definition of done

- The finished cut plays start to finish and reads as ONE film: no style drift, no character drift, no lighting jumps between shots.
- Every kept shot traces to its anchor frame; the continuity ledger is complete.
- Generation spend landed within the preflighted budget (overages logged with why).
- Exports are platform-correct (resolution, aspect, bitrate) and verified by playing the actual files.

## Phases

### Phase 0: Creative lock (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. No generation yet. Produce: (1) the film in one sentence; (2) the shot list: per shot its purpose, duration, camera, and content; (3) the style anchor: one reusable prompt fragment that defines look, palette, lighting, and finish for EVERY generation; (4) character/product reference plan where continuity matters. Write SHOTLIST.md.

USER GATE: approve SHOTLIST.md. A killed shot here costs nothing; a killed shot after generation costs real money.

### Phase 1: Anchor frames
Paste:
> Generate one STILL per key shot using the style anchor (stills are 10-50x cheaper than video). Lay the anchors side by side and audit as a set: does this look like one film? Fix drift at the anchor level. Only anchors that pass become generation inputs.

### Phase 2: Shot generation
Paste:
> Preflight cost per shot, choosing the cheapest model that clears each shot's quality bar (the registry ranks current models by value). Generate image-to-video from each anchor. Per shot: keep/kill against the anchor, ledger the keeps, regenerate kills with tightened prompts. Log spend as you go against the budget.

### Phase 3: Continuity audit
Paste:
> Extract a stills strip from all keepers and review as a set against the continuity checklist below (style drift, character/product drift, lighting or time-of-day jumps). Regenerate offenders with tightened references. Cap 3 rounds; if a shot won't converge, recompose it rather than brute-forcing credits into it.

### Phase 4: Assembly and finish
Paste:
> Cut the keepers, place music/VO (timing locks to audio), run one color-consistency pass over the assembled cut, export per platform. Verify per PROCESS-CORE.md: play the actual exports, spot-check sync, attach the stills strip and the final spend tally as evidence.

## Continuity checklist

1. One film: style, palette, and finish read identical across every shot (the anchor held).
2. Characters and products are the SAME across shots: face, wardrobe, proportions, logo — no drift.
3. Lighting and time-of-day stay consistent between adjacent shots unless the cut intends the change.
4. Every kept shot traces to an approved anchor frame; no orphan generations in the cut.
5. No uncanny tells left in frame (warping hands or faces, melting text, broken physics): offenders get recut, not shipped.
6. Spend stayed within the preflighted budget; overages are logged with why.
7. Exports are platform-correct and verified by playing the actual files.
