# Video harness

Read PROCESS-CORE.md first; it governs how every loop below runs.

## Your configuration

{{ANSWERS}}

{{ADDENDA}}

## Usage budget

{{ESTIMATE}}

Gen-AI footage note: if your path generates footage (Veo/Sora-class), the clips bill separately (API credits or a tool subscription) on top of plan usage. The agent-hours estimate covers the harness work only.

## Definition of done

- A rendered file at final resolution plays start to finish with synced audio.
- The first 3 seconds pass the hook audit (would a cold viewer keep watching?).
- Every text element is legible on a phone-sized preview.
- Pacing audit passes: no beat overstays, cuts land on audio beats where present.

## Phases

### Phase 0: Script and beat sheet (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. Before any production: write the script as a beat sheet: one row per beat with (timestamp budget, on-screen visual, VO/text line, purpose of the beat). The whole video's job in one sentence goes at the top. Run the de-slop loop on all VO/text. Write to SCRIPT.md. No production yet.

USER GATE: read SCRIPT.md. Changing a beat here costs seconds; changing it after render costs the render.

### Phase 1: Production setup
Paste:
> Read SCRIPT.md. Set up the production path per HARNESS.md config: Remotion project scaffold (explainer path), shot-prompt kit with style anchor + continuity notes (gen-AI path), or the cut list + caption spec (short-form path). Produce ONE test unit end to end (one beat rendered / one shot generated / one clip cut) and audit it before scaling to the rest.

### Phase 2: The frame loop
Paste:
> Produce all beats. Then run the design loop adapted to video: extract stills at every beat boundary plus any text-heavy frame, audit each still (composition, legibility at phone size, brand consistency, continuity with neighbors), fix the top 3 issues, re-render affected beats. Repeat to convergence per PROCESS-CORE.md.

### Phase 3: Audio and pacing
Paste:
> Lock audio: VO track and/or music placed, levels sane (-14 LUFS target for social). Then the pacing audit: watch the full render, mark every moment attention would drop, tighten those cuts. Cuts land on audio beats where a track exists.

### Phase 4: Ship
Paste:
> Final render at target resolution + a phone-preview render. Verify per PROCESS-CORE.md: play the actual output file, check duration, audio sync at 3 spot points, first-3-seconds hook, and report with the file path and a stills strip as evidence.
