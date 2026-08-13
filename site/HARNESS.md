# Website harness

Read PROCESS-CORE.md first; it governs how every loop below runs.

## Your configuration

- Single page or multi-page?  **Single page (landing, portfolio one-pager)**
- Is there an existing site whose look/feel you want to base this on? (paste URL, or 'none')  **(none)**
- Do you have the copy/content already, or should the agent write it?  **Agent writes it**
- Deploy where?  **Just local files for now**

**Config note:** Scope: one page. Every design loop iteration re-audits the full page top to bottom.

**Config note:** Copywriting phase is ACTIVE (Phase 1a): voice interview answers -> draft copy -> humanize pass -> user-facing copy review gate BEFORE design starts. Design around real copy, never lorem ipsum.

**Config note:** No deploy this run. Final phase produces a build folder and a one-command deploy note for later.

## Usage budget

Estimated active agent time: **2.7-6.2 hours** (iteration loops included; the band is real, not hedging).
Share of your plan's weekly usage (Sonnet-heavy mix):
- Pro ($20/mo): ~3-16% of the week
- Max 5x ($100/mo): ~1-4% of the week
- Max 20x ($200/mo): ~1-3% of the week  <-- your plan
Running Opus-heavy multiplies burn roughly 5x. If the worst-case number worries you, cut scope at the interview, not mid-run.

## Definition of done

- The site renders correctly at 1440px and 390px widths with zero horizontal scroll.
- Design checklist (below) passes on every page.
- All copy is final human-quality prose: no lorem ipsum, no AI tells.
- Lighthouse performance and accessibility both 90+.
- If deploying: live URL up, screenshot audit re-run against production.

## Phases

### Phase 0: Intent and taste lock (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. We're building the website described there. Before any code: (1) restate the site's ONE job in a sentence (what a visitor should do or feel); (2) propose an art direction in words: type pairing, palette, layout personality, one signature visual move that makes this site not look like a template; (3) write the design checklist for this specific site (start from the base checklist in HARNESS.md, add 3-5 site-specific items). Write all of it to DESIGN-NOTES.md. Do not write code yet.

USER GATE: skim DESIGN-NOTES.md. 2 minutes now saves the whole build from a taste mismatch.

### Phase 1: Structure and copy
Paste:
> Read HARNESS.md, PROCESS-CORE.md, DESIGN-NOTES.md. Build the full page structure with real final copy (write it now if none was provided, then run the de-slop loop on it). Semantic HTML, mobile-first CSS, the real content hierarchy. No decorative polish yet: this phase is about the bones being right. Screenshot at both viewports and confirm the structure reads correctly before calling the phase done.

### Phase 2: The design loop (the phase that matters)
Paste:
> Read DESIGN-NOTES.md and the design checklist. Run the design loop from PROCESS-CORE.md on the site: screenshot desktop 1440 and mobile 390, audit against the checklist, list every violation, fix the top 3, re-screenshot. Repeat until the checklist passes clean or two consecutive rounds change nothing material. Post the final screenshots and the checklist with pass/fail per item.

### Phase 3: Motion and depth (skip for plain content sites)
Paste:
> Add motion: scroll-triggered reveals, hover states, one signature interaction from DESIGN-NOTES.md. Use the GSAP skills. Respect prefers-reduced-motion. Then re-run one design-loop round; motion often breaks layout.

### Phase 4: Ship
Paste:
> Run Lighthouse (performance + accessibility, fix to 90+). Produce the final build folder and write a one-command deploy note for later. Then verify like PROCESS-CORE.md demands: fetch the final URL, screenshot both viewports, confirm every checklist item on the LIVE build, and report with the evidence attached.

## Base design checklist

1. No AI-design tells: no eyebrow labels over headings, no decorative underline bars under headings, no pill/chip tag rows, no rainbow gradients, no glow blobs, no over-rounded everything.
2. A real type scale (2 typefaces max, sizes from a scale, not ad hoc).
3. Spacing rhythm is consistent (one spacing unit, multiples only).
4. One accent color used with restraint; neutrals carry the page.
5. Every section earns its place; no filler sections ("Our Values" with three generic icons = delete).
6. Hierarchy survives squinting: blur your eyes, the important thing still reads first.
7. Mobile is designed, not just squished: nav, tap targets, line lengths all intentional at 390px.
8. Images/illustrations are consistent in style with each other and the brand.
9. The site has at least one moment of genuine craft a visitor might remember.
