# Pitch deck harness

Read PROCESS-CORE.md first; it governs how every loop below runs.

## Your configuration

{{ANSWERS}}

{{ADDENDA}}

## Usage budget

{{ESTIMATE}}

## Definition of done

- Every slide passes the design checklist rendered at full size.
- The narrative gate passed: the deck read aloud as a story holds, no slide repeats another's point.
- Every quantitative claim has a source or is marked as an assumption ON the slide.
- Output opens correctly in the real target app (PowerPoint/Keynote/PDF viewer), fonts intact.

## Phases

### Phase 0: Narrative before slides (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. No slides yet. First: write the deck as a 10-15 sentence story, one sentence per future slide, in NARRATIVE.md. Each sentence is the takeaway of that slide (the thing said if the audience only reads headlines). Then list, per slide, the single piece of evidence that earns its headline. Flag every claim we don't have a number for.

USER GATE: fix the flagged claims. A designed deck with hollow claims is worse than no deck.

### Phase 1: System and hero slides
Paste:
> Read NARRATIVE.md. Define the slide system per HARNESS.md config (type pair, 3-color system, grid, one signature motif) in a system spec slide. Then design the 3 hardest slides first (usually: title, the core product/insight slide, the traction/numbers slide) and run the design loop on them: render to image, audit, fix top 3, re-render. These 3 set the bar for everything else.

### Phase 2: Full build against the system
Paste:
> Build every remaining slide strictly against the approved system. Charts follow honest-chart rules: axes start where they should, no 3D, one message per chart, source line under every chart. Then render ALL slides to images and run one design-loop round across the full set, checking cross-slide consistency (alignment drift between slides is the tell of a machine-built deck).

### Phase 3: Ship
Paste:
> Export to the target format. Verify per PROCESS-CORE.md: open the actual exported file, page through every slide rendered, check fonts survived, run the narrative gate one final time reading only headlines in order. Report with the rendered slide strip as evidence.

## Deck design checklist

1. One idea per slide; the headline states it as a claim, not a topic ("Retention doubles after week 2", never "Retention").
2. No AI-design tells (no decorative heading underlines, no eyebrow labels, no icon-triplet filler rows).
3. Type scale and grid identical across all slides; motif appears consistently.
4. Data ink only in charts: no decoration, honest axes, sourced.
5. Whitespace is the default; density is the exception reserved for appendix.
6. Read the deck at thumbnail size: hierarchy still works.
