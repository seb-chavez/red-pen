---
name: red-pen
description: Use when a draft is too long or reads like AI wrote it, or before sharing a PRD, strategy doc, brief, status update, or Slack message. Cuts the draft to its doc type's budget, keeps every fact a reader acts on, adds detail a spec is missing, and reports what changed. Triggers on "red pen", "trim", "cut this down", "too wordy", "this reads like AI", "make this shorter".
argument-hint: "[path or pasted text] [lite|full|ultra]"
---

# Red Pen

Edit a draft down to the shortest version that still does its job. The rules (ladder, budgets, never-cut list, engineer test, cut-on-sight list) are in [rules/red-pen.md](../../rules/red-pen.md). This skill is the procedure.

## Intensity

| Level | What it does |
| ----- | ------------ |
| **lite** | Leaves the draft alone. Lists what to cut, one line each, with the words each cut saves |
| **full** (default) | Returns the edited draft. Assumes the doc should exist (ladder rungs 2 to 6) |
| **ultra** | Full, plus rung 1: challenges whether the doc should exist at all or could be a Slack message |

## Steps

1. **Name the doc type** and look up its ceiling and floor. If the type is unclear, ask once.
2. **Find the point**: the one or two sentences the reader must leave with. If you cannot, the draft has no point yet; say so and stop. If the type's floor names the point (a strategy doc's bet, a status update's ask), it goes in the doc as the first line.
3. **Mark what cannot be cut**: the floor for this type plus the never-cut list. If a risk has no owner, flag it; never invent one.
4. **Climb the ladder**, whole sections first, sentences last:
   - Section nobody would miss: delete it.
   - Section reproducing another doc: one sentence and a link, only after confirming the linked doc holds that content. If it does not, keep the content and flag it.
   - Sentence with no new fact: delete it.
   - Anything on the cut-on-sight list: cut or rewrite.
5. **Lead with the point.** Each section's first sentence is its answer.
6. **Check the ceiling.** Still over? Move detail behind links until only the floor is left, then stop. The floor wins: report the overage and which floor items cause it. Merge sections to meet section limits; never split one into two.
7. **Check the floor.** For a PRD or spec, run the engineer test on every requirement and add what is missing.

## Output

The edited draft, then four lines to the user (never inside the doc):

```
Words: <before> → <after> (<percent> change)
Cut: <what kinds of material went, in one line>
Moved behind links: <sections, or "none">
Kept or added on purpose: <floor items, engineer-test additions, and why>
```

Edit a file in place only when asked. Otherwise return the draft and let the user choose.

## Common mistakes

| Mistake | Fix |
| ------- | --- |
| Shortening every sentence but keeping every section | Delete whole sections first; sentence edits come last |
| Cutting a number or source to hit the word count | Those are the floor. Move prose behind a link instead |
| Trimming spec requirements | Requirements have a floor, not a ceiling. Trim the narrative |
| Putting the four report lines in the doc | They go to the user only |
