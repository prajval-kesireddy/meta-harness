# Contributing to metaharness

Thanks for helping make metaharness better. Keep changes small, sourced, and outcome-focused.

## Ground rules

- This project is free and MIT-licensed.
- Rate tools by **outcome improvement**, not popularity. Stars and installs are signals, not the score.
- Prefer small PRs: one tool, one source, or one harness improvement at a time.
- Run validation before submitting:

```powershell
python metaharness\metaharness.py validate
```

## Propose a tool for the rated index

1. Check `metaharness\registry\INBOX.md` and `metaharness\registry\registry.json` to avoid duplicates.
2. Add or update one entry in `metaharness\registry\registry.json`.
3. Score it from `0` to `10` on this question: **when composed into a harness, does this measurably improve the final outcome?**
4. Include:
   - `name`
   - `type`
   - `score`
   - `use_cases`
   - `install`
   - `why`
   - `source`
   - `last_verified` in `YYYY-MM-DD`
5. Run validation.

A good `why` is concrete: what outcome improves, where in the harness it belongs, and what evidence supports the score.

## Add a scan source

Add a source to `metaharness\registry\sources.json` when it helps find tools practitioners actually use.

Include:

- `id`, `name`, `url`, `category`, `role`
- what it contributes to the index
- the signal it provides
- a `scan` object if it can be swept automatically

If the source is curated rather than live-scanned, mark it honestly with the existing `reference` pattern.

## Add or improve a harness blueprint

Harnesses live in `metaharness\harnesses.json`; their runbooks live in `metaharness\templates\`.

For blueprint changes, update both sides:

1. Add or edit the harness in `harnesses.json`.
2. Add or edit the matching template in `metaharness\templates\`.
3. Keep the install set minimal. More tools can make agents worse.
4. Name the stage model deliberately: Opus for taste/judgment, Sonnet for production loops, Haiku for bulk.
5. Include verification gates with evidence, not vibes.
6. Run:

```powershell
python metaharness\metaharness.py list
python metaharness\metaharness.py validate
```

## Good first issues

- Rate one unchecked candidate from `metaharness\registry\INBOX.md` and either move it into `registry.json` or reject it with a short reason.
- Add a missing tool logo used by the public directory.
- Improve one `why` field so it explains the outcome improvement, not just the feature list.
- Tighten a harness template gate so it asks for concrete evidence before declaring done.

## PR checklist

- [ ] I changed only the files needed for this contribution.
- [ ] New ratings include `source` and `last_verified`.
- [ ] Harness changes include both blueprint and template updates where needed.
- [ ] `python metaharness\metaharness.py validate` passes.
