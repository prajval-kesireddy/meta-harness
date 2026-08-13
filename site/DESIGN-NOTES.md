# Design notes: metaharness public site

## The one job
A Claude Code user who suspects their output could be better lands here, understands within one screen that the harness is the missing layer, and leaves with the clone command (or at minimum scrolls the rated index and bookmarks it).

## Art direction: the field catalog
Every AI tool site is dark-mode glow. This one is a printed instrument: an editorial field catalog / rated index, like a well-set periodical about equipment. Cream paper, near-black ink, one vermilion accent used like a rubber stamp. The rated index IS the visual centerpiece: entries set like catalog listings with big mono scores and hairline rules between rows (structural rules dividing entries, never decorative underlines under headings).

- Paper: #F7F3EA. Ink: #1C1710. Muted ink: #6E6659. Vermilion accent: #C93D1B. Mono data ink on paper.
- Display: Fraunces (optical size, tight, 500-600 weight). Body: Source Serif 4. Data/commands: IBM Plex Mono.
- Layout: strong left-aligned column with a generous right margin on desktop; catalog rows full-width; asymmetric hero (oversized display line, small mono annotations).
- Motion: restrained. Scroll-reveal on rows (opacity+4px rise, staggered), hover state on index rows (paper darkens a step, score stamps vermilion). Respect prefers-reduced-motion.
- Signature move: the scorecard rows: №, name, score set huge in mono, one-line verdict, verified date. Reads like a printed review index; nobody else's tool page looks like this.

## Site-specific checklist (adds to the base 9)
10. Command blocks look like real terminal input (mono, copy-friendly, no fake window chrome).
11. Scores scannable in under a second per row; the verdict line never wraps past 2 lines.
12. Usage-estimate table reads honestly: bands, plan rows, no precision theater.
13. Zero dark-mode glow, zero gradient meshes: if a detail wouldn't survive print, cut it.
