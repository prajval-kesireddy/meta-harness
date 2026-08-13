#!/usr/bin/env python3
"""Builds index.html from the live data: registry ratings + harness catalog.
Re-run after every registry update; the public index never goes stale by hand.
"""

import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
MH = HERE.parent / "metaharness"

UNCERTAINTY = (0.7, 1.6)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_index_rows(entries):
    rows = []
    for i, e in enumerate(sorted(entries, key=lambda x: -x["score"]), 1):
        rows.append(f"""
      <div class="row reveal">
        <div class="row-no">{i:02d}</div>
        <div class="row-body">
          <div class="row-name">{esc(e['name'])} <span class="row-type">{esc(e['type'])}</span></div>
          <p class="row-why">{esc(e['why'])}</p>
          <div class="row-meta">verified {e['last_verified']} &middot; <a href="{e['source']}">source</a></div>
        </div>
        <div class="row-score">{e['score']}<span class="row-score-of">/10</span></div>
      </div>""")
    return "\n".join(rows)


def build_usecase_cards(harnesses):
    cards = []
    for key, b in harnesses.items():
        lo = b["base_agent_hours"] * UNCERTAINTY[0]
        hi = b["base_agent_hours"] * 2.0 * UNCERTAINTY[1]  # typical config spread
        cards.append(f"""
      <div class="uc reveal">
        <h3>{esc(b['title'])}</h3>
        <p>{esc(b['tagline'])}</p>
        <div class="uc-est">{lo:.0f}&ndash;{hi:.0f} agent-hours typical</div>
      </div>""")
    return "\n".join(cards)


def main():
    registry = json.loads((MH / "registry" / "registry.json").read_text(encoding="utf-8"))
    harnesses = json.loads((MH / "harnesses.json").read_text(encoding="utf-8"))
    harnesses.pop("_schema", None)

    template = (HERE / "template.html").read_text(encoding="utf-8")
    html = (template
            .replace("{{INDEX_ROWS}}", build_index_rows(registry["entries"]))
            .replace("{{USECASE_CARDS}}", build_usecase_cards(harnesses))
            .replace("{{ENTRY_COUNT}}", str(len(registry["entries"])))
            .replace("{{UPDATED}}", registry.get("updated", str(date.today()))))
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"Built index.html: {len(registry['entries'])} index entries, "
          f"{len(harnesses)} use cases.")


if __name__ == "__main__":
    main()
