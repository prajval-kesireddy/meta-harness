# TODO — engine + sources + site logos

## Research (research loop; exit: 2 dry sweeps)
- [ ] Confirm scriptable open endpoints per source (HN Algolia, GitHub, MCP
      registry, npm, Reddit) and canonical URLs/logos for directory sources
      (skills.sh, Glama, Product Hunt, awesome-lists).

## Engine (build-verify loop)
- [ ] sources.json canonical source registry
- [ ] research_update.py multi-source rewrite + composite ranking
- [ ] metaharness.py hardening (validation) + keep CLI green
- [ ] PROCESS-CORE/templates rigor pass

## Site (design loop)
- [ ] add missing logos to site/assets/logos
- [ ] Sources section in template_index.html + build_site.py rendering
- [ ] rebuild site + webp rewrite, screenshot audit 1440/390

## Verify (law 4)
- [ ] run scan, run CLI, capture screenshots; update DECISIONS.md

---
## ALL COMPLETE (2026-08-13) — see DECISIONS.md "Status: SHIPPED"
Every item above is done and verified with evidence (scan output, `validate`
green, desktop+mobile screenshots, zero horizontal scroll). Not pushed — awaiting
Praj's "push". Re-sync the live site any time with: `python site/build_site.py`.
