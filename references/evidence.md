# Evidence behind reel-maker

## Dataset and method
- 199 Instagram reels with a video analysis (6 image posts excluded), posted 2026-04-01 to 2026-10-05, collected in a local reel-watcher research project. The source dataset is not bundled with this skill.
- Per reel: caption, views, likes, comments, duration, then a Gemini analysis of hook (spoken, on-screen, visual, type), format, shot types, caption style, editing, music and sound effects, beats, transcript, call-to-action and giveaway. Sources: `data/studies/*.json` (raw) and `data/synthesis/all_reels.json` (joined, with my review of each reel's contact sheets).
- Niche: almost all AI, Claude and developer-tool content (183 English, 13 Arabic, 2 Spanish, 1 unknown). Median views 81K.
- Beat timestamps from the analysis ran past real video length, so they were never used. Beat order and labels were.
- Engagement rates (likes/views, comments/views) were used as the fairer signal, because follower counts were not available.
- To re-run: `scripts/features.py` builds the per-reel table and the comparison helpers. Set `REEL_WATCHER_ROOT` to your research project containing `data/studies/*.json`, or run from that project's root. The script uses only the Python standard library; without a matching dataset it reports a missing-data error.

## Headline numbers
| Metric | p25 | Median | p75 | p90 |
|---|---|---|---|---|
| Views | 19K | 81K | 180K | 491K |
| Likes / views | 1.66% | 2.14% | 2.58% | 2.93% |
| Comments / views | 0.16% | 0.91% | 2.08% | 3.58% |
Duration median 41s (middle half 29 to 52s). Hook median 13 words (9 to 17). Spoken script median 139 words (98 to 184), about 3.4 to 3.5 words per second.

## What nearly every reel shares (table stakes)
Bold-claim hook 166 of 199; hook shown as on-screen text 192 of 199; a call-to-action beat 178; a proof beat 137; talking head 106, screen recording 45, tutorial 12, skit 11; jump cuts about 60%; zoom-ins about 64%; sound effects about 51%; music about 28%; word-by-word captions about two thirds; keyword offer 133 (130 single-word). Most common beat order: hook, setup, value, proof, call-to-action (68 reels).

## Finding 1: identical hooks, very different views
| Hook | Larger account | Smaller account |
|---|---|---|
| "You can now run Claude Code completely free with almost unlimited usage" | 491K | 5.1K |
| "Most people don't realize you can teach Claude Code ... to watch YouTube" | 1.26M | 5.5K |
| "This is one of the most slept on GitHub repos right now" | 280K | 5.6K |
| "Claude is over 100,000 skills, but ... you only need five" | 906K | 142K |
| "Did you know that if you come to this GitHub repo here" | 609K | 81K |
Conclusion: hook wording does not explain views on its own. Audience and distribution do.

## Finding 2: within-creator tests found no reliable craft effect
Method: for each reel from a creator with at least 3 reels, divide its views by the median of that creator's other reels (relative views; 77 reels). Compare reels with and without each feature. About 40 features were tested; at p<0.05 about two false positives would be expected by chance, and none of the view-based differences came close to p<0.05.

| Feature | Relative views with vs without | n |
|---|---|---|
| Question hook | 1.16x vs 0.95x | 10 / 67 |
| Number in hook | 1.11x vs 0.95x | 21 / 56 |
| "free" in hook | 1.18x vs 0.95x | 24 / 53 |
| First-person hook | 1.27x vs 0.92x | 10 / 67 |
| Hook up to 10 words / 11 to 18 / 19 or more | 0.88x / 1.05x / 0.87x | 17 / 42 / 18 |
| Duration under 30s / 30 to 45s / 45 to 60s / 60s or more | 1.12x / 1.05x / 1.11x / 0.75x | 18 / 33 / 20 / 6 |
| Proof beat | 0.92x vs 1.12x | 51 / 26 |
| Keyword offer | 1.04x vs 0.94x | 58 / 19 |
| Word-by-word captions | 1.06x vs 0.84x | 55 / 22 |
| Jump cuts / zoom / sound effects / music | 1.11x / 0.95x / 1.14x / 0.98x | 45 / 54 / 38 / 20 |
| Talking head vs other | 0.94x vs 1.04x | 44 / 33 |
Reading: nothing consistent. The sample is small (17 creators), so absence of evidence is not proof of no effect. The practical conclusion: do the recipe, then test on your own account.

## Finding 3: likes per view (weak hints)
Rates are not driven by account size in the same way. The differences below are weak, with p between 0.01 and 0.05 across many tests.
| Feature | Likes/views |
|---|---|
| First-person hook | 2.6% vs 2.1% (n=22) |
| "Here's how" promise | 2.8% vs 2.1% (n=9) |
| Skit format | 2.6% vs 2.1% (n=11) |
| Reel under 30s | 2.0% vs 2.2% |
| Reel 60s or longer | 2.4% vs 2.1% |
| Hook up to 10 words | 2.0% vs 2.2% |
Reading: slightly more likes per view for personal, longer or story-led reels; slightly fewer for very short punchy ones.

## Finding 4: the comment funnel is the clearest measurable lever
- Keyword offer: comments/views 1.56% (133 reels) vs 0.07% (66 reels).
- Among offer reels, post caption opening with the call-to-action line: 1.91% vs 1.00% (72 vs 61, p<0.001).
- Keyword unlocks a guide or setup: 2.0% vs 1.3% (p=0.046, weak).
- Also asking viewers to follow: 1.0% vs 1.7% (p=0.14, hint).
These show comments, not extra reach. Comments inflate when a link is gated behind them.

## Finding 5: timing and topic overlap (confounded)
Reels covering the same named tool (12 clusters with at least 4 reels from at least 3 creators) were ranked by date: earlier reels tended to have more views (mean Spearman rho -0.72). Restricting to reels at least 14 days old: mean rho -0.57 over 8 clusters. Confound: older reels have had longer to accumulate views, and a saved collection favours survivors. Median views by reel age: 0 to 3 days 9K, 3 to 7 days 33K, 7 to 14 days 48K, 14 to 30 days 34K, 30 to 60 days 112K, 60 to 120 days 277K. Treat "post early on something new" as a plausible lever, not a proven one.

## Review of credibility (my read of the reels' contact sheets)
Credibility ratings across 200 records: high 10, medium-high 9, medium 64, low-medium 26, mixed 25, low 14, plus others. Low ratings usually came from staged screens, invented figures, hype that the demo did not support, or a lead-gen funnel hiding a thin product.

## What the data cannot tell us
- Follower counts, so views cannot be adjusted for audience size.
- Retention curves, shares, saves, follows, the posting time, or how the platform distributed each reel.
- Whether a reel was boosted or paid for.
- Anything outside the AI and developer-tool niche. Structure, word budgets and the funnel mechanics are likely to transfer; specific topic angles may not.
- Gemini's beat timestamps (unreliable) and the "why it works" text (an explanation written after the fact).
