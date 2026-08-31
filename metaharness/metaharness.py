#!/usr/bin/env python3
"""metaharness: interviews you about the outcome you want, then composes the
best current harness for it: skills, MCPs, process runbook, verification
loops, and an honest estimate of what it costs in plan usage.

Usage:
  python metaharness.py list
  python metaharness.py validate
  python metaharness.py sources
  python metaharness.py run <use-case> [--out DIR] [--plan pro|max5x|max20x]
                             [--answers FILE.json] [--yes]
  python metaharness.py registry [use-case]

Stdlib only. Data lives in harnesses.json, registry/registry.json,
templates/*.md next to this file.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Weekly capacity in active agent-hours, Sonnet-heavy mix. Grounded in
# Anthropic's published ranges (Max 5x ~140-280 Sonnet-hours/week, Max 20x
# ~240-480, Pro ~40-80) as of 2026-08; a temporary +50% boost runs through
# 2026-08-19 and is deliberately NOT counted. Opus-heavy runs burn roughly
# 5x faster; the report says so instead of pretending precision.
PLAN_CAPACITY = {
    "pro":    {"label": "Pro ($20/mo)",      "hours": (40, 80)},
    "max5x":  {"label": "Max 5x ($100/mo)",  "hours": (140, 280)},
    "max20x": {"label": "Max 20x ($200/mo)", "hours": (240, 480)},
}

# Estimates carry honest uncertainty: real runs land inside this band around
# the point estimate depending on taste iterations and rework.
UNCERTAINTY = (0.7, 1.6)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_harnesses():
    data = load_json(ROOT / "harnesses.json")
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_registry():
    path = ROOT / "registry" / "registry.json"
    if path.exists():
        return load_json(path).get("entries", [])
    return []


def load_sources():
    path = ROOT / "registry" / "sources.json"
    if path.exists():
        return load_json(path).get("sources", [])
    return []


# ---------------------------------------------------------------- interview

def ask_option(q):
    print(f"\n{q['prompt']}")
    for i, opt in enumerate(q["options"], 1):
        print(f"  {i}. {opt['label']}")
    while True:
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(q["options"]):
            return q["options"][int(raw) - 1]["key"]
        keys = [o["key"] for o in q["options"]]
        if raw in keys:
            return raw
        print(f"Pick 1-{len(q['options'])}.")


def ask_freeform(q):
    print(f"\n{q['prompt']}")
    return input("> ").strip()


def collect_answers(blueprint, answers_file=None, yes=False):
    """Returns {question_id: answer}. answer is an option key or freeform text."""
    given = load_json(Path(answers_file)) if answers_file else {}
    answers = {}
    for q in blueprint["questions"]:
        qid = q["id"]
        if qid in given:
            answers[qid] = given[qid]
        elif q.get("freeform"):
            answers[qid] = "none" if yes else ask_freeform(q)
        elif yes:
            answers[qid] = q["options"][0]["key"]
        else:
            answers[qid] = ask_option(q)
    return answers


# ---------------------------------------------------------------- estimator

def freeform_is_set(value):
    return bool(value) and value.strip().lower() not in ("none", "no", "n/a", "-", "")


def resolve(blueprint, answers):
    """Walk questions+answers -> (multiplier, addenda[], fills{}, answer_lines[], extra_installs[])."""
    mult, addenda, fills, lines, extra_installs = 1.0, [], {}, [], []
    for q in blueprint["questions"]:
        ans = answers.get(q["id"], "")
        if q.get("freeform"):
            if freeform_is_set(ans):
                mult *= q.get("mult_if_set", 1.0)
                if q.get("addendum_if_set"):
                    addenda.append(q["addendum_if_set"] + f"\n  Provided: {ans}")
                extra_installs.extend(q.get("installs_if_set", []))
                lines.append(f"- {q['prompt']}  **{ans}**")
            else:
                lines.append(f"- {q['prompt']}  **(none)**")
            continue
        opt = next((o for o in q["options"] if o["key"] == ans), None)
        if opt is None:
            raise SystemExit(f"Unknown answer '{ans}' for question '{q['id']}' "
                             f"(valid: {[o['key'] for o in q['options']]})")
        mult *= opt.get("mult", 1.0)
        if opt.get("addendum"):
            addenda.append(opt["addendum"])
        fills.update(opt.get("fills", {}))
        extra_installs.extend(opt.get("installs_if_set", []))
        lines.append(f"- {q['prompt']}  **{opt['label']}**")
    return mult, addenda, fills, lines, extra_installs


def estimate(blueprint, mult):
    hours = blueprint["base_agent_hours"] * mult
    lo, hi = hours * UNCERTAINTY[0], hours * UNCERTAINTY[1]
    rows = {}
    for key, plan in PLAN_CAPACITY.items():
        cap_lo, cap_hi = plan["hours"]
        rows[key] = (100 * lo / cap_hi, 100 * hi / cap_lo)  # best..worst case
    return {"agent_hours": (round(lo, 1), round(hi, 1)), "plan_pct": rows}


def estimate_text(est, chosen_plan):
    lo, hi = est["agent_hours"]
    out = [f"Estimated active agent time: **{lo}-{hi} hours** "
           f"(iteration loops included; the band is real, not hedging)."]
    out.append("Share of your plan's weekly usage (Sonnet-heavy mix):")
    for key, plan in PLAN_CAPACITY.items():
        p_lo, p_hi = est["plan_pct"][key]
        marker = "  <-- your plan" if key == chosen_plan else ""
        out.append(f"- {plan['label']}: ~{p_lo:.0f}-{p_hi:.0f}% of the week{marker}")
    out.append("Running Opus-heavy multiplies burn roughly 5x. If the worst-case "
               "number worries you, cut scope at the interview, not mid-run.")
    return "\n".join(out)


# ---------------------------------------------------------------- composer

TARGET_CLAUDE_MD = """# {title} project (metaharness)

This project runs on a composed harness. Non-negotiables:

1. Read HARNESS.md, PROCESS-CORE.md, and CLAUDE-CODE-DOCTRINE.md before any work,
   every session. Conduct yourself by the doctrine: work like the best coding
   agents (concise, convention-following, no unsolicited changes, evidence
   before done).
2. Follow the phase runbook in HARNESS.md in order; never skip a USER GATE.
3. Every loop runs to its written exit condition; every "done" claim carries
   post-change evidence (screenshot, render, fetched URL, test output).
4. Decisions go in DECISIONS.md, open items in TODO.md; a fresh session must
   be able to resume from files alone.

Generated by metaharness on {today}. Estimate at generation time:
{estimate_short}
"""

TARGET_SKILL = """---
name: harness-os
description: Use at the start of EVERY session in this project, and whenever unsure how to proceed, iterate, or verify. Loads the composed harness process (HARNESS.md + PROCESS-CORE.md) that governs all work here.
---

Read HARNESS.md, PROCESS-CORE.md, and CLAUDE-CODE-DOCTRINE.md at the project
root, then follow them exactly: current phase's runbook prompt, loop mechanics,
exit conditions, verification-with-evidence before any completion claim, and the
doctrine's conduct rules (concise output, follow the codebase, no unsolicited
changes). If context has grown long enough that these rules feel distant,
re-read them before continuing.
"""


def pipeline_text(blueprint):
    stages = blueprint.get("pipeline", [])
    if not stages:
        return ""
    out = ["## The pipeline (stage, model, exit)", "",
           "Run stages in order. The model column matters: Opus where taste and "
           "judgment concentrate, Sonnet for production loops, Haiku for bulk "
           "mechanical passes. One-model-for-everything is the #2 harness "
           "mistake after over-installing skills.", ""]
    for i, s in enumerate(stages, 1):
        out.append(f"{i}. **{s['stage']}** [{s['model']}]: {s['what']} "
                   f"Stack: {s['stack']}. Exit: {s['loop']}.")
    return "\n".join(out)


def compose(usecase, blueprint, answers, plan, out_dir):
    mult, addenda, fills, answer_lines, extra_installs = resolve(blueprint, answers)
    est = estimate(blueprint, mult)
    est_text = estimate_text(est, plan)

    template = (ROOT / blueprint["template"]).read_text(encoding="utf-8")
    filled = (template
              .replace("{{ANSWERS}}", "\n".join(answer_lines))
              .replace("{{ADDENDA}}", "\n\n".join(f"**Config note:** {a}" for a in addenda))
              .replace("{{ESTIMATE}}", est_text + "\n\n" + pipeline_text(blueprint)))
    for key, val in fills.items():
        filled = filled.replace("{{" + key + "}}", val)
    # Strip any placeholder no answer filled.
    import re
    filled = re.sub(r"\{\{[A-Z_]+\}\}", "", filled)

    out = Path(out_dir)
    (out / ".claude" / "skills" / "harness-os").mkdir(parents=True, exist_ok=True)
    (out / "HARNESS.md").write_text(filled, encoding="utf-8")
    (out / "PROCESS-CORE.md").write_text(
        (ROOT / "templates" / "PROCESS-CORE.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    (out / "CLAUDE-CODE-DOCTRINE.md").write_text(
        (ROOT / "templates" / "CLAUDE-CODE-DOCTRINE.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    (out / ".claude" / "CLAUDE.md").write_text(
        TARGET_CLAUDE_MD.format(title=blueprint["title"], today=date.today(),
                                estimate_short=est_text.splitlines()[0]),
        encoding="utf-8")
    (out / ".claude" / "skills" / "harness-os" / "SKILL.md").write_text(
        TARGET_SKILL, encoding="utf-8")
    (out / "estimate.json").write_text(
        json.dumps({"use_case": usecase, "answers": answers,
                    "multiplier": round(mult, 2), "estimate": est,
                    "generated": str(date.today())}, indent=2),
        encoding="utf-8")

    # INSTALL.md: blueprint installs + top registry picks for this use case.
    lines = [f"# Install list: {blueprint['title']} harness", "",
             "Run these in the project folder. Install ONLY these; piling on extra "
             "skills makes the agent worse, not better.", ""]
    for item in blueprint.get("installs", []) + extra_installs:
        lines += [f"```bash\n{item['cmd']}\n```", f"{item['why']}", ""]
    for m in blueprint.get("mcps", []):
        lines += [f"```bash\n{m['cmd']}\n```", f"{m['name']}: {m['why']}", ""]
    picks = [e for e in load_registry()
             if usecase in e.get("use_cases", []) and e.get("score", 0) >= 8
             and not any(e.get("install") == i.get("cmd") for i in blueprint.get("installs", []))]
    if picks:
        lines += ["## Registry picks (rated, current)", ""]
        for e in sorted(picks, key=lambda x: -x.get("score", 0))[:5]:
            lines += [f"- **{e['name']}** ({e['score']}/10): {e['why']} "
                      f"Install: `{e.get('install', 'see source')}` "
                      f"(verified {e.get('last_verified', 'unknown')})"]
    (out / "INSTALL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return est, est_text


# ---------------------------------------------------------------- validation

REQUIRED_Q = {"id", "prompt"}
REQUIRED_STAGE = {"stage", "what", "stack", "model", "loop"}
LIVE_METHODS = {"github", "hackernews", "mcp-registry", "npm"}


def validate_data():
    """Structural self-check of the engine's data files. Returns a list of
    problems (empty == healthy). The engine refuses to pretend broken data is
    fine: a bad blueprint fails loud here, not deep inside compose()."""
    problems = []
    try:
        harnesses = load_harnesses()
    except Exception as e:
        return [f"harnesses.json: unparseable ({e})"]
    if not harnesses:
        problems.append("harnesses.json: no blueprints loaded")
    for key, b in harnesses.items():
        for field in ("title", "tagline", "quality_expectation",
                      "base_agent_hours", "template", "questions", "pipeline"):
            if field not in b:
                problems.append(f"{key}: missing '{field}'")
        if b.get("template") and not (ROOT / b["template"]).exists():
            problems.append(f"{key}: template not found: {b['template']}")
        for q in b.get("questions", []):
            if not REQUIRED_Q <= set(q):
                problems.append(f"{key}: question missing id/prompt near '{q.get('id', '?')}'")
            if not q.get("freeform") and not q.get("options"):
                problems.append(f"{key}: question '{q.get('id')}' has no options")
            for o in q.get("options", []):
                if "key" not in o or "label" not in o:
                    problems.append(f"{key}/{q.get('id')}: option missing key/label")
        for s in b.get("pipeline", []):
            miss = REQUIRED_STAGE - set(s)
            if miss:
                problems.append(f"{key}: stage '{s.get('stage', '?')}' missing {sorted(miss)}")
    for e in load_registry():
        for field in ("name", "type", "score", "why", "source", "last_verified"):
            if field not in e:
                problems.append(f"registry '{e.get('name', '?')}': missing '{field}'")
        if not isinstance(e.get("score"), int) or not 0 <= e.get("score", -1) <= 10:
            problems.append(f"registry '{e.get('name', '?')}': score not an int 0-10")
    logos = ROOT.parent / "site" / "assets" / "logos"
    for s in load_sources():
        for field in ("id", "name", "logo", "url", "contributes"):
            if field not in s:
                problems.append(f"source '{s.get('id', '?')}': missing '{field}'")
        method = s.get("scan", {}).get("method")
        if method and method not in LIVE_METHODS | {"reference", "community"}:
            problems.append(f"source '{s.get('id')}': unknown scan method '{method}'")
        if logos.exists() and s.get("logo") and not (logos / s["logo"]).exists():
            problems.append(f"source '{s.get('id')}': logo file missing: {s['logo']}")
    return problems


def cmd_validate():
    problems = validate_data()
    if not problems:
        print(f"OK: {len(load_harnesses())} blueprints, "
              f"{len(load_registry())} registry entries, "
              f"{len(load_sources())} sources — all structurally valid.")
        return
    print(f"{len(problems)} problem(s) found:")
    for p in problems:
        print(f"  - {p}")
    raise SystemExit(1)


def cmd_sources():
    sources = load_sources()
    if not sources:
        print("  (no sources.json; the index has no declared provenance)")
        return
    live = [s for s in sources if s.get("scan", {}).get("method") in LIVE_METHODS]
    ref = [s for s in sources if s.get("scan", {}).get("method") not in LIVE_METHODS]
    print("Live-scanned sources (swept daily by registry/research_update.py):\n")
    for s in live:
        print(f"  {s['name']:15} [{s.get('signal', '')}]  {s['contributes']}")
    print("\nCurated / community sources (reported with logos; pulled at compose-time):\n")
    for s in ref:
        print(f"  {s['name']:15} {s.get('role', ''):22} {s['url']}")
    print(f"\n{len(sources)} sources total. Edit registry/sources.json; the public "
          f"site regenerates from it via site/build_site.py, so the two never drift.")


# ---------------------------------------------------------------- commands

def cmd_list(harnesses):
    print("Use cases:\n")
    for key, b in harnesses.items():
        print(f"  {key:22} {b['tagline']}")
    print("\nRun: python metaharness.py run <use-case>")


def cmd_registry(usecase=None):
    entries = load_registry()
    if usecase:
        entries = [e for e in entries if usecase in e.get("use_cases", [])]
    for e in sorted(entries, key=lambda x: -x.get("score", 0)):
        print(f"  {e['score']:>2}/10  {e['name']:32} {e['why'][:80]}")
    if not entries:
        print("  (no entries; run registry/research_update.py)")


def cmd_run(harnesses, args):
    if args.use_case not in harnesses:
        raise SystemExit(f"Unknown use case '{args.use_case}'. "
                         f"Valid: {', '.join(harnesses)}")
    blueprint = harnesses[args.use_case]
    print(f"\n== {blueprint['title']} ==\n{blueprint['tagline']}\n")
    print(f"What to expect: {blueprint['quality_expectation']}")
    n = len(blueprint["questions"])
    print(f"\n{n} questions. That's the whole interview.")
    answers = collect_answers(blueprint, args.answers, args.yes)
    out_dir = args.out or f"./{args.use_case}-harness"
    est, est_text = compose(args.use_case, blueprint, answers, args.plan, out_dir)
    print(f"\nHarness written to {out_dir}\n")
    print(est_text.replace("**", ""))
    print(f"\nNext steps:\n  1. cd {out_dir}\n  2. Run the commands in INSTALL.md"
          f"\n  3. Open Claude Code and paste the Phase 0 prompt from HARNESS.md")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # em dashes on Windows consoles
    except Exception:
        pass
    p = argparse.ArgumentParser(prog="metaharness")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("validate")
    sub.add_parser("sources")
    reg = sub.add_parser("registry")
    reg.add_argument("use_case", nargs="?")
    run = sub.add_parser("run")
    run.add_argument("use_case")
    run.add_argument("--out")
    run.add_argument("--plan", choices=list(PLAN_CAPACITY), default="max5x")
    run.add_argument("--answers")
    run.add_argument("--yes", action="store_true",
                     help="non-interactive: default answers where not provided")
    args = p.parse_args()

    harnesses = load_harnesses()
    if args.cmd == "list":
        cmd_list(harnesses)
    elif args.cmd == "validate":
        cmd_validate()
    elif args.cmd == "sources":
        cmd_sources()
    elif args.cmd == "registry":
        cmd_registry(args.use_case)
    else:
        cmd_run(harnesses, args)


if __name__ == "__main__":
    main()
