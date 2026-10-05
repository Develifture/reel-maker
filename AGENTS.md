# Reel Maker repository guidance

This repository distributes one agent skill: `reel-maker`. It plans and writes Instagram Reels, TikTok videos, and YouTube Shorts. Its deliverables are text and recording directions.

## Using the skill

Read `SKILL.md` for reel-writing, script critique, reference adaptation, or performance-review requests. Load the linked reference that fits the task. `README.md` explains installation, examples, and the optional HyperFrames production handoff. `llms.txt` provides direct public Markdown URLs for agents fetching this repository remotely.

Use the actual product information and supplied footage when writing feature claims. State missing assumptions and evidence limitations. The source research covers 199 predominantly AI and developer-tool reels; it does not establish guaranteed reach or causation.

If the user asks for a rendered video, use a separately available video production workflow such as HyperFrames. Recording, rendering, posting, and reward delivery are separate actions from writing the reel pack.

## Maintaining the repository

- Preserve the required skill name `reel-maker` and valid YAML frontmatter in `SKILL.md`.
- Keep `agents/openai.yaml` and README capability descriptions consistent with the skill.
- Update `llms.txt` links if reference files move. Keep raw public links on the existing `main` branch.
- The optional `scripts/features.py` helper expects a local `data/studies` dataset selected by `REEL_WATCHER_ROOT`; the dataset is not distributed.
- Keep factual research caveats intact and document any measured changes to the helper.
- Keep credentials, local study data, and machine-specific private paths out of published files.
