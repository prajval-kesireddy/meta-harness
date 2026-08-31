# Deep research harness

Read PROCESS-CORE.md and CLAUDE-CODE-DOCTRINE.md first: PROCESS-CORE governs how every loop below runs, the doctrine governs how you conduct yourself (concise, convention-following, no unsolicited changes, evidence before done).

## Your configuration

{{ANSWERS}}

{{ADDENDA}}

## Usage budget

{{ESTIMATE}}

## Definition of done

- The research question is answered directly, with confidence levels stated per conclusion.
- Every load-bearing claim survived a refutation attempt or is flagged with what would settle it.
- The source ledger is complete: claim -> source -> date checked.
- A completeness critic pass found no unexplored angle worth the budget.

## Phases

### Phase 0: Question discipline (fresh session)
Paste:
> Read HARNESS.md and PROCESS-CORE.md. Before searching: (1) restate the research question falsifiably (what evidence would change the answer?); (2) list the sub-questions that compose it; (3) list the sweep lanes (which angles, which source types per HARNESS.md config); (4) write what you EXPECT to find per lane, so surprises are visible later. Write to RESEARCH-PLAN.md.

### Phase 1: The sweep rounds
Paste:
> Run the research loop from PROCESS-CORE.md: execute every lane in RESEARCH-PLAN.md (each lane blind to the others), log every finding to SOURCES.md with (claim, source, date, lane). Dedup. Then the gap question: what would exist if the obvious answer were true, that we haven't found? Sweep again on the gaps. Exit per the loop rule: two consecutive rounds with nothing new.

### Phase 2: Adversarial verification
Paste:
> Take every load-bearing claim (a claim the final answer would change without). For each: actively try to refute it: search for the counter-claim, check the source's incentive to say it, check the date (is it stale?). Mark each claim CONFIRMED / CONTESTED / UNVERIFIABLE in SOURCES.md. Conclusions may only lean on CONFIRMED claims; CONTESTED ones appear with both sides.

### Phase 3: Synthesis
Paste:
> Write the answer: conclusion first, confidence level per conclusion, then the reasoning, then the receipts. Decision-mode runs score against the criteria weights from the interview. Run the de-slop loop; research prose slops hardest. Then the completeness critic: one pass asking "what angle, source type, or stakeholder did we never look at?" If it finds something material, loop back to Phase 1 for that lane only.
