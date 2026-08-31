# Competitive analysis harness

Read PROCESS-CORE.md and CLAUDE-CODE-DOCTRINE.md first: PROCESS-CORE governs how every loop below runs, the doctrine governs how you conduct yourself (concise, convention-following, no unsolicited changes, evidence before done).

## Your configuration

{{ANSWERS}}

{{ADDENDA}}

## Usage budget

{{ESTIMATE}}

## Definition of done

- Every named competitor VERIFIED to exist and ship (their own site/repo/app fetched, not remembered).
- Per competitor: positioning in their own words, pricing, traction receipts (funding/stars/reviews/hiring/release cadence), and community sentiment from real threads.
- The map answers the configured decision (build / position / market-reality), with an honest "where you lose" section.
- Freshness sweep ran: launches from the last 90 days checked (ProductHunt, HN, GitHub trending, X). Stale maps are the #1 failure of AI competitive analysis.

## Phases

### Phase 0: Market frame (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. Frame before sweeping: (1) restate the subject product and buyer from the interview; (2) define the axes that MATTER for the configured decision (not generic feature grids: what dimensions would change the verdict?); (3) list the sweep lanes: direct rivals, adjacent tools, incumbent bundles, non-consumption workarounds, plus the freshness lane (last-90-days launches). Write MARKET-FRAME.md.

### Phase 1: Discovery sweeps
Paste:
> Run the research loop across every lane in MARKET-FRAME.md. Sources per lane: competitor sites, GitHub (stars/velocity for dev tools), ProductHunt and HN launches, app stores where relevant, Reddit/X/community threads for what buyers actually use, review sites for pricing and complaints. Log every candidate to COMPETITORS.md with (name, lane, one-line what-it-is, source URL, date found). Exit per loop rule: two rounds finding nothing new.

### Phase 2: Verification and profiling
Paste:
> For each candidate that survives dedup: VERIFY it. Fetch their actual site/repo/listing. Profile: positioning verbatim from their own page, pricing, traction receipts (funding rounds, GitHub stars + commit recency, review counts, team size signals, release cadence), and 2-3 real community threads about them (what users praise, what they hate). Kill entries that turn out dead, vaporware, or misremembered. Mark each profile CONFIRMED with the fetch date.

### Phase 3: Sentiment and gap mining
Paste:
> Mine the complaint surface: across every competitor's community threads and reviews, list what buyers keep asking for that nobody ships. This complaint list IS the differentiation surface. Cross-reference against the subject product: which complaints does it answer, which does it share?

### Phase 4: The verdict
Paste:
> Write COMPETITIVE-MAP.md: (1) the answer to the configured decision, stated first, with confidence; (2) the map (competitors positioned on the axes from MARKET-FRAME.md); (3) per-competitor profiles with receipts; (4) the differentiation surface from the complaint mining; (5) "where you lose": the honest section on who beats the subject product and for which buyer; (6) if standing-watch is configured, the monitoring kit: saved queries, watch script, weekly re-scan runbook. De-slop loop, then the completeness critic: which lane got the least attention, and would budget there change the verdict?
