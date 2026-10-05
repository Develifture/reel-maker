"""reel-maker evidence script.
Usage: from features import *; rows = build(); print(fmt_res(compare(rows, "question hook", lambda r: r["h_q"])))

Build a per-reel feature table from data/studies and compare feature groups, controlling for account size
by (a) within-author relative views (leave-one-out author median, authors with >=3 reels) and (b) engagement rates."""
import json, os, re, statistics as st, math, collections, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
# Project that holds data/studies (override with the REEL_WATCHER_ROOT environment variable)
ROOT = Path(os.environ.get("REEL_WATCHER_ROOT") or Path.cwd()).expanduser()

def load():
    studies = ROOT / "data" / "studies"
    if not studies.is_dir():
        raise FileNotFoundError(
            f"Study data not found: {studies}. Set REEL_WATCHER_ROOT to your "
            "reel-watcher project. The research dataset is not bundled with this skill."
        )
    rows = []
    for f in studies.glob("*.json"):
        with f.open(encoding="utf-8") as source:
            d = json.load(source)
        if d.get("kind") != "video" or not d.get("analysis"):
            continue
        p, a = d["post"], d["analysis"]
        if not p.get("views"):
            continue
        rows.append((d, p, a))
    return rows

def words(s):
    return re.findall(r"[\w'’]+", s or "")

def build():
    rows = load()
    by_author = collections.defaultdict(list)
    for d, p, a in rows:
        by_author[p["author"]].append(p["views"])
    out = []
    for d, p, a in rows:
        views, likes, comments = p["views"], p.get("likes") or 0, p.get("comments") or 0
        dur = p.get("duration_s") or 0
        others = list(by_author[p["author"]])
        others.remove(views)
        rel = None
        if len(others) >= 2:
            rel = views / st.median(others)
        hook = (a.get("hook") or {})
        hs = hook.get("spoken") or ""
        hw = words(hs)
        cap = p.get("caption") or ""
        beats = a.get("structure_beats") or []
        cta = a.get("cta") or {}
        gv = a.get("giveaway") or {}
        ost = a.get("on_screen_text") or []
        ed = " ".join(a.get("editing_techniques") or []).lower()
        cs = (a.get("caption_style") or "").lower()
        shots = " ".join(a.get("shot_types") or []).lower()
        ms = a.get("music_sfx") or {}
        cta_beat = [b for b in beats if (b.get("beat") or "").lower() == "cta"]
        cta_frac = (cta_beat[0]["t"] / dur) if cta_beat and dur else None
        hl = hs.lower()
        f = {
            "code": d["code"], "author": p["author"], "views": views, "likes": likes, "comments": comments,
            "lr": likes / views, "cr": comments / views, "rel": rel, "dur": dur,
            "hook": hs, "hook_words": len(hw), "hook_type": (hook.get("type") or "").lower(),
            "fmt": (a.get("format") or "").lower(),
            "n_beats": len(beats), "has_proof": any((b.get("beat") or "").lower() == "proof" for b in beats),
            "has_cta": bool(cta_beat), "cta_frac": cta_frac,
            "offer": bool(gv.get("offered") and (gv.get("keyword") or "").strip()),
            "cap_words": len(words(cap)), "n_hash": cap.count("#"),
            "cap_starts_comment": bool(re.match(r"\s*(comment|dm|follow|drop|type|send)\b", cap, re.I)),
            "h_q": hs.strip().endswith("?") or bool(re.match(r"\s*(why|how|what|is|are|do|did|can|have|did)\b", hl)),
            "h_digit": bool(re.search(r"\d", hs)),
            "h_free": "free" in hl,
            "h_you": bool(re.search(r"\byou(r|'re|'ve)?\b", hl)),
            "h_i": bool(re.search(r"\b(i|i'm|i've|my|we|we've|our)\b", hl)),
            "h_neg": bool(re.search(r"\b(stop|don't|dont|never|struggl\w*|problem|stuck|mistake\w*|wrong|broken|killed|dead|banned|nobody|no one|slop|worst|waste\w*|losing|lose|fail\w*)\b", hl)),
            "h_hype": bool(re.search(r"\b(insane|crazy|unbelievable|mind|best|biggest|only|every|everything|entire|whole|literally|actually|ridiculous|wild|illegal)\b", hl)),
            "h_effort": bool(re.search(r"(\bin \d+ (second|minute|min|sec)|one (command|prompt|click|file|line)|single (command|prompt)|\d+ (second|minute)s?\b|minutes?\b)", hl)),
            "h_now": bool(re.search(r"\b(now|just|finally|new|released|dropped|launched)\b", hl)),
            "h_this": bool(re.search(r"\b(this|these|here's|here is|check)\b", hl)),
            "h_claude": bool(re.search(r"\b(claude|chatgpt|gpt|codex|gemini|ai)\b", hl)),
            "h_os": bool(hook.get("on_screen")),
            "ost0": any((x.get("t") or 0) <= 1.5 for x in ost),
            "n_ost": len(ost),
            "karaoke": bool(re.search(r"word|karaoke|animated|pop|highlight", cs)),
            "face": "talking" in shots or "face" in shots or "selfie" in shots,
            "n_ed": len(a.get("editing_techniques") or []),
            "zoom": "zoom" in ed, "jump": "jump" in ed,
            "music": str(ms.get("music", "")).lower().startswith("yes"),
            "sfx": str(ms.get("sfx", "")).lower().startswith("yes"),
            "lang": (a.get("transcript") or {}).get("language") if isinstance(a.get("transcript"), dict) else None,
            "kw": (gv.get("keyword") or "").strip(),
            "cta_spoken": cta.get("spoken") or "",
            "why": a.get("why_it_works") or "",
            "take": a.get("takeaway") or "",
            "date": p.get("post_date"),
            "transcript": ((a.get("transcript") or {}).get("text") if isinstance(a.get("transcript"), dict) else a.get("transcript")) or "",
        }
        out.append(f)
    return out

def mwu_p(a, b):
    """two-sided Mann-Whitney U p-value (normal approx, tie-corrected enough for exploration)."""
    n1, n2 = len(a), len(b)
    if n1 < 3 or n2 < 3:
        return None
    allv = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranks, i = {}, 0
    ties = 0
    r = [0.0] * len(allv)
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[k] = avg
        t = j - i + 1
        ties += t ** 3 - t
        i = j + 1
    R1 = sum(r[k] for k in range(len(allv)) if allv[k][1] == 0)
    U1 = R1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    N = n1 + n2
    sd = math.sqrt(n1 * n2 / 12 * ((N + 1) - ties / (N * (N - 1))))
    if sd == 0:
        return None
    z = (U1 - mu) / sd
    return math.erfc(abs(z) / math.sqrt(2))

def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else float("nan")

def compare(rows, name, pred, metric_keys=("rel", "lr", "cr", "views")):
    A = [r for r in rows if pred(r)]
    B = [r for r in rows if not pred(r)]
    res = {"name": name, "nA": len(A), "nB": len(B)}
    for k in metric_keys:
        a = [r[k] for r in A if r[k] is not None]
        b = [r[k] for r in B if r[k] is not None]
        res[k] = (med(a), med(b), mwu_p(a, b), len(a), len(b))
    return res

def fmt_res(res):
    def f(k, scale=1.0, pct=False):
        a, b, p, na, nb = res[k]
        if pct:
            s = f"{a*100:.1f}% vs {b*100:.1f}%"
        elif k == "rel":
            s = f"{a:.2f}x vs {b:.2f}x"
        else:
            s = f"{a/1000:.0f}K vs {b/1000:.0f}K"
        pv = "" if p is None else f" p={p:.2f}"
        return s + pv
    return (f"{res['name']:<38} n={res['nA']:>3}/{res['nB']:<3} | rel: {f('rel')} (n={res['rel'][3]}/{res['rel'][4]})"
            f" | likes/views {f('lr', pct=True)} | comments/views {f('cr', pct=True)} | views {f('views')}")
