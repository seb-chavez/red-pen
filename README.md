# Red Pen

*Short where prose runs long. Detailed where engineers need detail.*

PMs and founders write the docs everyone else has to read: PRDs, strategy briefs, status updates. Drafted with an AI agent, those docs come out long, padded, and easy to dismiss as "AI wrote this." Red Pen holds each doc type to a length budget, and it never cuts the detail engineers need to build from.

| Plugin | For | What it cuts |
| ------ | --- | ------------ |
| [Caveman](https://github.com/JuliusBrussee/caveman) | Anyone using an agent | How the agent talks to you |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Engineers | How much code gets written |
| **Red Pen** | PMs and founders | How long your shared docs get, without cutting what engineers need |

## Why

The obvious fix, "be concise," breaks specs: a PRD trimmed for word count leaves engineers guessing, and guessing ships the wrong thing. So Red Pen gives each doc type a **ceiling** and a **floor**:

| Doc type | Ceiling | Floor |
| -------- | ------- | ----- |
| Strategy, founder brief | One page; mission in one sentence | The bet, who pays, proof, biggest risk, kill condition |
| Status update | 150 words | What changed, what is blocked, what you need |
| PRD requirements | None | Every trigger, branch, limit, and term an engineer needs |
| Slack | 1 to 3 sentences | The ask or the answer |

When they conflict, the floor wins. Full rules: [rules/red-pen.md](rules/red-pen.md).

## Results

Five fictional PM docs, each written from notes and edited from a bloated draft. Sonnet, 3 runs per cell, median. Same docs, same prompts, three arms. [Full report](eval/results/2026-10-04-sonnet.md).

| | No skill | Caveman | **Red Pen** |
| - | --: | --: | --: |
| Strategy doc, written from notes (words) | 821 | 607 | **251** |
| Status update, edited (words) | 178 | 134 | **85** |
| Facts kept (numbers, dates, decisions) | 99% | 99% | **99%** |
| AI tells per doc (em dashes, "pivotal," "in conclusion") | 0.3 | 0.1 | **0.0** |
| PRD behaviors **wrong or missing**, edited from a thin draft (of 7) | 2.0 | 1.0 | **0.0** |

That last row is the one other tools can't claim. The draft PRD left several behaviors unspecified. With no skill, the model filled them in with plausible, wrong answers ("reply R adds the patient to the waitlist"; the real spec sends a link to rebook). Red Pen wrote **Open question** instead. A confident wrong spec is worse than an honest gap.

When it wrote PRDs from complete notes, every arm got all 7 behaviors right. Red Pen just used fewer words.

## Before and after

A 696-word founder brief ("In today's rapidly evolving healthcare landscape...") became:

> **The bet:** Owner-run practices with 3 to 15 dentists will pay a flat $399 a month to cut no-shows, if setup takes a day instead of six weeks.
>
> ...
>
> **Proof so far:** 61 clinics served. $1.2M annual recurring revenue [check: 61 clinics at $399 a month is about $0.29M a year. Confirm the pricing, the ARR, or whether other plans exist].

305 words, every number and the kill condition kept. It also caught an arithmetic error we had planted in the test draft by accident.

## Install

**Claude Code:**

```
/plugin marketplace add seb-chavez/red-pen
/plugin install red-pen@red-pen
```

Or turn it on for everyone in a repo, in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "red-pen": { "source": { "source": "github", "repo": "seb-chavez/red-pen" } }
  },
  "enabledPlugins": { "red-pen@red-pen": true }
}
```

**Cursor, Codex, or any agent that reads `AGENTS.md`:** paste [rules/red-pen.md](rules/red-pen.md) into your `AGENTS.md` or rules file.

## Use

It is on from the first message, in the main session and every sub-agent. To edit an existing draft:

```
/red-pen path/to/draft.md          # full: returns the edited draft
/red-pen path/to/draft.md lite     # lists cuts, changes nothing
/red-pen path/to/draft.md ultra    # also asks whether the doc should exist
```

Every edit reports `Words: before → after`, what was cut, what moved behind links, and what was kept or added on purpose. Say "red pen off" to stop.

## How it is measured

- **On every PR (free):** `python -m unittest discover -s tests` checks the scoring code, the test docs, the manifests, and the hook. No model calls.
- **Before a release (maintainer, by hand):** `python3 eval/bench.py --model sonnet --repeats 3`. Runs through the `claude` CLI in `--safe-mode`, so it bills to your Claude plan, needs no API key, and ignores your personal setup. Results land in [eval/results/](eval/results/) with every raw output.

Words, facts kept, and AI tells are counted by code. PRD behaviors are scored by a judge model against the true intended answer for each one.

**Limits:** five docs, one model, three runs per cell. The test docs are fictional and written by the author. Treat the numbers as directional, and rerun them on your own docs.

## License

MIT. The ladder pattern is inspired by [Ponytail](https://github.com/DietrichGebert/ponytail); the comparison arm uses [Caveman](https://github.com/JuliusBrussee/caveman)'s skill, fetched at run time.
