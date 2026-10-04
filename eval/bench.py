"""Benchmark: no skill vs Caveman vs Red Pen on five PM docs, two modes each.

Runs through the `claude` CLI in --safe-mode (no CLAUDE.md, plugins, or hooks), so it bills
to your Claude plan and needs no API key. Maintainers run it by hand before a release.

    python3 eval/bench.py --model sonnet --repeats 3
"""
import argparse
import json
import re
import statistics
import subprocess
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import checks

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "eval" / "fixtures"
RESULTS = ROOT / "eval" / "results"
CAVEMAN_URL = "https://raw.githubusercontent.com/JuliusBrussee/caveman/main/plugins/caveman/skills/caveman/SKILL.md"
MODES = {
    "write": "Write a {type} from these notes. Return only the document.\n\n{notes}",
    "edit": "Here is a draft {type}. Revise it so it is ready to share. Return only the revised document.\n\n{draft}",
}
JUDGE = """You are the engineer who must write the tech spec for this PRD. Below are behaviors with the true intended answer. For each, decide whether the PRD:
- "correct": states the true answer (wording may differ);
- "flagged": names it as an open question or undecided;
- "wrong": states a different behavior than the truth;
- "missing": says nothing usable (vague wording like "follows up appropriately" is missing).

Behaviors:
{items}

Reply with only JSON: {{"verdicts": ["correct" | "flagged" | "wrong" | "missing", ...]}} in the same order.

PRD:
{doc}"""


def arms():
    rules = (ROOT / "rules" / "red-pen.md").read_text()
    skill = (ROOT / "skills" / "red-pen" / "SKILL.md").read_text()
    with urllib.request.urlopen(CAVEMAN_URL, timeout=30) as r:
        caveman = r.read().decode()
    return {
        "baseline": "You are a helpful assistant.",
        "caveman": caveman,
        "red-pen": rules + "\n\n" + skill,
    }


def claude(prompt, system, model):
    with tempfile.TemporaryDirectory() as cwd:
        out = subprocess.run(
            ["claude", "-p", prompt, "--safe-mode", "--tools", "", "--no-session-persistence",
             "--model", model, "--output-format", "json", "--system-prompt", system],
            cwd=cwd, capture_output=True, text=True, timeout=600,
        )
    data = json.loads(out.stdout)
    return data.get("result", ""), data.get("total_cost_usd", 0.0)


def spec_coverage(doc, rubric, model):
    """Returns ({correct, flagged, wrong, missing}, cost). Wrong or missing is what leaves engineers guessing."""
    items = "\n".join(f"{i + 1}. {b['behavior']}. Truth: {b['truth']}" for i, b in enumerate(rubric))
    reply, cost = claude(JUDGE.format(items=items, doc=doc), "You are a careful senior software engineer.", model)
    try:
        verdicts = json.loads(re.search(r"\{.*\}", reply, re.S).group(0))["verdicts"]
        return {v: verdicts.count(v) for v in ("correct", "flagged", "wrong", "missing")}, cost
    except (AttributeError, ValueError, KeyError):
        return None, cost


def run_one(job):
    doc_name, meta, mode, arm, system, model, judge_model = job
    fx = FIXTURES / doc_name
    prompt = MODES[mode].format(type=meta["type"], notes=(fx / "notes.md").read_text(),
                                draft=(fx / "draft.md").read_text())
    text, cost = claude(prompt, system, model)
    kept, total, missing = checks.facts_kept(text, meta["must_keep"])
    row = {"doc": doc_name, "mode": mode, "arm": arm, "words": checks.words(text),
           "facts_kept": kept, "facts_total": total, "missing": missing,
           "tells": checks.tells(text)["total"], "cost": cost, "output": text}
    if meta.get("spec"):
        row["spec"], judge_cost = spec_coverage(text, meta["spec_rubric"], judge_model)
        row["cost"] += judge_cost
    print(f"  {doc_name:14} {mode:5} {arm:8} {row['words']:5} words  facts {kept}/{total}  tells {row['tells']}", flush=True)
    return row


def median(rows, key):
    vals = [r[key] for r in rows if r.get(key) is not None]
    return statistics.median(vals) if vals else None


def report(rows, model, repeats):
    arm_names = ["baseline", "caveman", "red-pen"]
    lines = [f"# Red Pen benchmark, {date.today()} ({model}, {repeats} runs per cell, median)", ""]
    for mode in MODES:
        lines += [f"## {mode.capitalize()} mode", "",
                  "| Doc | " + " | ".join(arm_names) + " |", "| --- |" + " --: |" * len(arm_names)]
        docs = sorted({r["doc"] for r in rows})
        for doc in docs:
            cells = []
            for arm in arm_names:
                rs = [r for r in rows if r["doc"] == doc and r["mode"] == mode and r["arm"] == arm]
                cells.append(f"{median(rs, 'words'):.0f}" if rs else "")
            lines.append(f"| {doc} (words) | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## Totals across all docs and modes", "",
              "| Metric | " + " | ".join(arm_names) + " |", "| --- |" + " --: |" * len(arm_names)]
    def per_arm(fn):
        return " | ".join(fn([r for r in rows if r["arm"] == a]) for a in arm_names)
    lines.append("| Median words | " + per_arm(lambda rs: f"{median(rs, 'words'):.0f}") + " |")
    lines.append("| Facts kept | " + per_arm(lambda rs: f"{100 * sum(r['facts_kept'] for r in rs) / sum(r['facts_total'] for r in rs):.0f}%") + " |")
    lines.append("| AI tells per doc | " + per_arm(lambda rs: f"{statistics.mean(r['tells'] for r in rs):.1f}") + " |")
    spec = lambda rs, k: [r["spec"][k] for r in rs if r.get("spec")]
    for mode in MODES:
        in_mode = lambda rs: [r for r in rs if r["mode"] == mode]
        lines.append(f"| PRD behaviors correct or flagged, {mode} (of 7) | " + per_arm(lambda rs: f"{statistics.mean(c + f for c, f in zip(spec(in_mode(rs), 'correct'), spec(in_mode(rs), 'flagged'))):.1f}") + " |")
        lines.append(f"| PRD behaviors wrong or missing, {mode} (of 7) | " + per_arm(lambda rs: f"{statistics.mean(w + m for w, m in zip(spec(in_mode(rs), 'wrong'), spec(in_mode(rs), 'missing'))):.1f}") + " |")
    lines.append("| Cost (USD, total) | " + per_arm(lambda rs: f"{sum(r['cost'] for r in rs):.2f}") + " |")
    lines += ["", "Words, facts kept, and AI tells are counted by `eval/checks.py`. PRD behaviors are scored by a judge model against the 7 behaviors and their true answers in `fixtures/prd/meta.json`: correct, flagged as an open question, wrong (a different behavior than intended), or missing. In edit mode the draft omits several answers, so flagging them is correct and inventing them is wrong. Wrong or missing is what leaves engineers guessing. Raw outputs are in the matching `raw/` file."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--docs", nargs="*", default=None)
    ap.add_argument("--rescore", help="Re-judge spec docs in an existing raw .jsonl and rewrite its report")
    args = ap.parse_args()

    if args.rescore:
        raw = Path(args.rescore)
        rows = [json.loads(l) for l in raw.read_text().splitlines()]
        spec_rows = [r for r in rows if json.loads((FIXTURES / r["doc"] / "meta.json").read_text()).get("spec")]
        rubric = lambda r: json.loads((FIXTURES / r["doc"] / "meta.json").read_text())["spec_rubric"]
        with ThreadPoolExecutor(args.workers) as pool:
            scores = list(pool.map(lambda r: spec_coverage(r["output"], rubric(r), args.judge_model), spec_rows))
        for r, (score, cost) in zip(spec_rows, scores):
            r.pop("engineer_questions", None)
            r["spec"] = score
            r["cost"] += cost
        raw.write_text("".join(json.dumps(r) + "\n" for r in rows))
        model, repeats = raw.stem.split("-", 3)[3], len(rows) // (len({(r["doc"], r["mode"], r["arm"]) for r in rows}))
        (RESULTS / f"{raw.stem}.md").write_text(report(rows, model, repeats))
        print(f"rescored {len(spec_rows)} rows, wrote eval/results/{raw.stem}.md")
        return

    systems = arms()
    docs = args.docs or sorted(p.name for p in FIXTURES.iterdir() if p.is_dir())
    jobs = [(d, json.loads((FIXTURES / d / "meta.json").read_text()), mode, arm, systems[arm], args.model, args.judge_model)
            for d in docs for mode in MODES for arm in systems for _ in range(args.repeats)]
    print(f"{len(jobs)} runs", flush=True)
    with ThreadPoolExecutor(args.workers) as pool:
        rows = list(pool.map(run_one, jobs))

    stem = f"{date.today()}-{args.model}"
    (RESULTS / "raw").mkdir(parents=True, exist_ok=True)
    with open(RESULTS / "raw" / f"{stem}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    (RESULTS / f"{stem}.md").write_text(report(rows, args.model, args.repeats))
    print(f"wrote eval/results/{stem}.md")


if __name__ == "__main__":
    main()
