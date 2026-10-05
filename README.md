# Reel Maker

An agent skill that plans, scripts, and captions short vertical videos for Instagram Reels, TikTok, and YouTube Shorts. It turns an idea or product into a **ready-to-record reel pack**: opening hooks, voiceover, visual directions, post caption, call-to-action, and a test plan.

It is a writing and planning workflow expressed in Markdown instructions. It does not record your screen, render a video, upload posts, send messages, or guarantee views. An AI assistant reads the instructions and produces the creative materials.

## Exactly what it does

The skill supports four modes:

| Mode | What you provide | What the assistant produces |
| --- | --- | --- |
| New reel | A topic or product, audience, available proof, and any preferences | A complete reel pack with five hook options, a recommended opening, script, visuals, edit notes, caption, call-to-action, and test plan |
| Critique or rewrite | Your draft hook, script, or caption | A checklist-based critique and a before/after rewrite, preserving as much of your draft as possible |
| Adapt a reference | A reference reel or its transcript and your own topic | Its beat order and word budget translated into original wording for your topic |
| Post-mortem | A published reel's content and available performance metrics | Possible explanations for weak results and one concrete variable to test next, with uncertainty made explicit |

For a new reel, it follows this process:

1. Collect only missing essentials: topic, intended viewer, offer, format, length, and goal. Ask at most two questions; state reasonable assumptions for the rest.
2. Choose an angle suited to the actual product or topic. The hook bank contains twelve archetypes, including a specific question, first-person proof, discovery, a practical tip, and a problem followed by a fix.
3. Write five original hooks across at least three archetypes. Each hook has a spoken line of no more than seventeen words, opening on-screen text, and a first-frame visual. Recommend one and explain the choice.
4. Build the voiceover around ordered beats: hook, setup, value, visible proof, and call-to-action. Target a spoken word budget appropriate to the requested length, using approximately 3.4 words per second as an initial estimate.
5. Give the editor concrete visual directions: screen inserts or cutaways, caption treatment, and changes in emphasis roughly every three to four seconds. Show the real result early.
6. Write a copy-ready post caption and relevant hashtags. When a comment-keyword offer fits, use one short keyword in the final spoken line, closing screen text, and caption's first line.
7. Check that the claims can be demonstrated and that the promised reward can actually be delivered. Never invent statistics, screens, earnings, results, or a product's capabilities.
8. Propose a small test: vary one element and compare posts at the same age against the creator's own history.

For product demos, provide documentation, footage, screenshots, or a local project path when your assistant has file access. The skill asks for real proof; local source access and live product testing depend on the assistant and tools you use.

## What a reel pack contains

```text
Working title, assumptions, angle, format, and estimated length
Five hooks with spoken text, opening text, and first-frame visuals
Beat-by-beat voiceover and visual directions
Editing and recording notes
Copy-ready post caption and hashtags
Call-to-action, keyword, reward, and delivery plan
Pre-publish checklist
One-variable test plan
```

An estimated duration is a planning aid. Read the script aloud and adjust it to your own speaking pace. Beat order is useful; the research's source timestamps were unreliable and are not treated as precise timing instructions.

## Install for Codex in one project

Codex discovers project skills in `.agents/skills`. From the project where you want to use this skill:

**PowerShell**

```powershell
New-Item -ItemType Directory -Force -Path .agents/skills | Out-Null
git clone https://github.com/Develifture/reel-maker.git .agents/skills/reel-maker
```

**macOS or Linux**

```sh
mkdir -p .agents/skills
git clone https://github.com/Develifture/reel-maker.git .agents/skills/reel-maker
```

Use an empty destination. Installation stays in that project. Invoke the skill in your next prompt with `$reel-maker`; if it does not appear, restart Codex. See the [official local skill discovery documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

The same `SKILL.md` format can be used by another assistant that supports agent skills; follow that assistant's discovery and invocation instructions.

## Example requests

```text
$reel-maker
Create a 40-second English reel for my Revit Auto Dimension tool.
The audience is architects. Use a real screen recording.
End with "Comment REVIT for the tool details."
Read my product documentation before writing feature claims.
```

```text
$reel-maker
Give me five hooks for a tutorial on making room schedules in Revit.
Keep each hook under seventeen words and describe its opening visual.
```

```text
$reel-maker
Critique this script. Preserve its tone, fix unsupported claims,
and tighten it to thirty seconds: [paste script]
```

```text
$reel-maker
This reel received 2,000 views and 12 comments after forty-eight hours.
Here are the script and my recent account results: [paste details].
Suggest one variable to test in the next comparable reel.
```

## Evidence and practical limits

The instructions draw on a local analysis of **199 Instagram reels**, primarily AI and developer-tool content posted between April and October 2026. The local feature-building helper was rerun before this repository was published and returned 199 qualifying records. The raw dataset is not included; the evidence reference documents its method, reported comparisons, and limitations.

This is observational research, not a controlled experiment or a universal formula for viral content:

- Reusing a successful hook did not reproduce its original view count. Account reach and time since posting remain major confounds.
- Within-creator comparisons found no reliable view effect from the tested craft choices. Sample size was limited and many comparisons were explored.
- Keyword offers and placing the call-to-action first in the caption were associated with more comments in this sample. That measures response to the offer and does not establish increased reach or causation.
- The source lacks follower counts, retention curves, shares, saves, paid promotion information, and distribution details.
- Applying its structures to architecture, education, or other niches is a practical adaptation, not evidence that the same results will transfer.

Read [references/evidence.md](references/evidence.md) for the numbers and caveats. The strongest usable principle is to show specific, genuine proof and test original material on your own account.

## Included files

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Skill metadata, mode selection, workflow, output format, and honesty constraints |
| [references/hook-bank.md](references/hook-bank.md) | Twelve opening archetypes with templates and illustrative examples |
| [references/script-templates.md](references/script-templates.md) | Seven narrative structures and approximate word budgets |
| [references/cta-and-caption.md](references/cta-and-caption.md) | Calls-to-action, comment keywords, post captions, and reported funnel observations |
| [references/test-loop.md](references/test-loop.md) | Logging, comparisons at the same post age, and small iteration tests |
| [references/evidence.md](references/evidence.md) | Dataset description, reported findings, and methodological limits |
| [scripts/features.py](scripts/features.py) | Optional Python research helper for a compatible local reel-watcher dataset |

The references load only when relevant. The Python helper is not needed to write a reel or use the documented workflow.

## Optional research helper

`scripts/features.py` uses the Python standard library. Its functions load `data/studies/*.json` from a local reel-watcher project, extract per-reel features, and compare groups using median engagement rates and within-author relative views where available. Its Mann–Whitney U calculation is an approximate exploratory comparison, not a complete statistical analysis package.

Set `REEL_WATCHER_ROOT` to the project that contains your compatible study files. By default, it looks under the current working directory. Without that dataset, it raises a descriptive missing-data error.

For example, from this repository on Windows:

```powershell
$env:REEL_WATCHER_ROOT = 'C:\path\to\your\reel-watcher-project'
python -c "import sys; sys.path.insert(0, 'scripts'); import features; rows = features.build(); print(len(rows)); print(features.fmt_res(features.compare(rows, 'keyword offer', lambda r: r['offer'])))"
```

The equivalent environment variable can be set on macOS or Linux. The script's study paths are portable. It does not download reels, contact an AI API, require API keys, or publish anything.
