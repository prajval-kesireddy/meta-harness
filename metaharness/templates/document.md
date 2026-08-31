# Document / PDF harness

Read PROCESS-CORE.md and CLAUDE-CODE-DOCTRINE.md first: PROCESS-CORE governs how every loop below runs, the doctrine governs how you conduct yourself (concise, convention-following, no unsolicited changes, evidence before done).

## Your configuration

{{ANSWERS}}

{{ADDENDA}}

## Usage budget

{{ESTIMATE}}

## Definition of done

- The full document reads clean start to finish in one sitting: consistent voice, no section-quality decay.
- De-slop loop passed on every section (a sharp reader clocks nothing as machine-written).
- Research-backed claims all trace to the source ledger; assumptions are labeled.
- The output file renders correctly in its real target app: margins, page breaks, figures, table of contents.

## Phases

### Phase 0: Reader and skeleton (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. Before drafting: (1) define the reader in 2 sentences (who, what they know already, what they should do after reading); (2) write the skeleton: every section with its one-sentence takeaway and target length; (3) if this is research-backed, run the research loop FIRST and build the source ledger in SOURCES.md. Write skeleton to OUTLINE.md. No prose yet.

USER GATE: approve OUTLINE.md. Restructuring after drafting wastes half the budget.

### Phase 1: Voice anchor
Paste:
> Draft ONLY the most important section (usually the opening or the core argument). Run the de-slop loop on it until it genuinely reads human. This section becomes the voice anchor: extract its patterns (sentence rhythm, density, person, how evidence is introduced) into VOICE.md. Every later section is drafted against VOICE.md and audited against the anchor.

### Phase 2: Batch draft with per-section loops
Paste:
> Draft the remaining sections one at a time. Per section: draft against VOICE.md -> de-slop loop -> claims check against SOURCES.md -> move on. For documents over 10 pages, run sections in fresh sessions per PROCESS-CORE.md session discipline; quality decay across a long context is the #1 long-document failure.

### Phase 3: Whole-document pass
Paste:
> Read the FULL document end to end as the defined reader. Audit against the prose & typeset checklist below (transitions, repetition, voice drift from the anchor, front-loading). Fix the top issues, re-read the affected joins.

### Phase 4: Typeset and ship
Paste:
> Produce the final format per HARNESS.md config. For designed PDF: typeset via the HTML-to-PDF pipeline, then render every page to an image and audit (margins, orphans/widows, figure placement, heading breaks); fix and re-render to convergence. For docx: generate, then open-verify the actual file. Report done with rendered-page evidence per PROCESS-CORE.md.

## Prose & typeset checklist

1. Reads in the defined reader's voice from line one; matches VOICE.md, with no section-quality decay.
2. De-slopped: no rule-of-three, no inflated abstractions, no vague attribution ("studies show"), no filler transitions.
3. The payoff is front-loaded; the reader isn't made to earn the point.
4. Every load-bearing claim traces to SOURCES.md; assumptions are labeled as assumptions.
5. One clear structure: headings are informative and sections neither overlap nor repeat.
6. Typeset output is clean: margins, no orphans or widows, figures placed, sane page and heading breaks.
7. Opens correctly in the real target app with formatting intact.
