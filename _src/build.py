"""
3rd & Long — static site generator.

Every word of editorial copy on the output comes from Adam's reports.
This file supplies structure and labels only (nav, headings that repeat his own
section names, and functional UI text).
"""
import re, sys, json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "content"))
import teams as TEAMS_MOD
import midseason2024 as MS24
import preseason2025 as PS25
import midseason2025 as MS25
import preseason2026 as PS26
from posts import POSTS
import standings as STANDINGS
import leaders as LEADERS_MOD
import power as POWER_MOD

ROOT = HERE.parent

SITE = "https://third-and-long.vercel.app"
SITE_NAME = "3rd &amp; Long"

# cache-busting suffixes, filled in by main() from the built file contents.
# Without these, the year-long immutable cache header pins visitors to a
# stale stylesheet and there is no way for them to know to hard-reload.
V = {"css": "", "team": "", "nav": ""}

# ---------------------------------------------------------------- editions

EDITIONS = [
    dict(slug="2026-preseason", kind="Preseason",
         title="2026&ndash;2027 NFL Preseason Report", season="2026",
         type="divisions", mod=PS26, extras=True, rec_label="2025", author="Adam Long"),
    dict(slug="2025-midseason", kind="Midseason",
         title="2025 NFL Midseason Report", season="2025",
         type="rankings", mod=MS25, sub="Power Rankings", author="Adam Long"),
    dict(slug="2025-preseason", kind="Preseason",
         title="2025&ndash;2026 NFL Preseason Report", season="2025",
         type="divisions", mod=PS25, extras=True, rec_label="2024", author="Adam Long"),
    dict(slug="2024-midseason", kind="Midseason",
         title="2024 NFL Midseason Report", season="2024",
         type="rankings", mod=MS24, sub="Week 10 Power Rankings", author="Adam Long"),
]

DIV_ORDER = ["North", "East", "South", "West"]
CONF_FULL = {"afc": "American Football Conference", "nfc": "National Football Conference"}

# ---------------------------------------------------------------- helpers

def tslug(name):
    """Map a team name in the copy to its palette class."""
    slug = TEAMS_MOD.NAME_TO_SLUG.get(name)
    if not slug:
        raise SystemExit(f"No palette for team name: {name!r}")
    return "t-" + slug

def esc_attr(s):
    return s.replace('"', "&quot;")

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

def award_dd(pos, name, club):
    p = f'<span class="pos">{pos}</span> ' if pos else ""
    return (f'<span class="who">{p}{name}</span>'
            f'<span class="club">{club}</span>')

# ---------------------------------------------------------------- renderers

def render_standings_grid(mod):
    cards = []
    by_conf = {"afc": [], "nfc": []}
    for conf, name, teams in mod.DIVISIONS:
        by_conf[conf].append((name, teams))
    for conf in ("afc", "nfc"):
        for name, teams in sorted(by_conf[conf], key=lambda x: DIV_ORDER.index(x[0])):
            rows = "".join(
                f"<li><b>{t[0]}</b>{t[1]}</li>" for t in teams)
            cards.append(
                f'<div class="gcard conf--{conf}">'
                f'<h3>{conf.upper()} {name}</h3><ol>{rows}</ol></div>')
    return ('<section class="section" id="standings"><div class="wrap">'
            '<h2>Division Standings</h2>'
            f'<div class="grid">{"".join(cards)}</div></div></section>')

def render_divisions(mod, extras, rec_label="2024"):
    out = []
    by_conf = {"afc": [], "nfc": []}
    for conf, name, teams in mod.DIVISIONS:
        by_conf[conf].append((name, teams))

    for conf in ("afc", "nfc"):
        out.append(f'<div class="conf conf--{conf}" id="{conf}">')
        out.append('<div class="band"><div class="wrap">'
                   f'<span class="abbr">{conf.upper()}</span>'
                   f'<span class="full">{CONF_FULL[conf]}</span></div></div>')
        for name, teams in sorted(by_conf[conf], key=lambda x: DIV_ORDER.index(x[0])):
            out.append(f'<section class="division" id="{conf}-{name.lower()}">'
                       '<div class="wrap"><header class="div-head">'
                       f'<span class="kicker">{conf.upper()}</span><h2>{name}</h2>'
                       '</header><div class="teams">')
            for t in teams:
                if extras:
                    rank, team, record, breakout, text = t
                    meta = ('<dl class="tmeta">'
                            f'<div><dt>{rec_label}</dt><dd>{record}</dd></div>'
                            f'<div><dt>Breakout Candidate</dt><dd>{breakout}</dd></div>'
                            '</dl>')
                else:
                    rank, team, text = t
                    meta = ""
                first = " team--1" if rank == 1 else ""
                out.append(
                    f'<article class="team tc {tslug(team)}{first}"'
                    f' id="{tslug(team)}">'
                    f'<div class="rank" aria-hidden="true">{rank}</div>'
                    f'<div class="team-body"><div class="team-head"><h3>{team}</h3></div>'
                    f'{meta}<p>{text}</p></div></article>')
            out.append('</div></div></section>')
        out.append('</div>')
    return "".join(out)

def render_seeding(mod):
    cols = []
    for conf in ("afc", "nfc"):
        rows = "".join(f"<li><b>{i}</b>{team}</li>"
                       for i, team in enumerate(mod.SEEDING[conf], 1))
        cols.append(f'<div class="gcard conf--{conf}">'
                    f'<h3>{conf.upper()}</h3><ol>{rows}</ol></div>')
    return ('<section class="section" id="seeding"><div class="wrap">'
            '<h2>Playoff Seeding</h2>'
            f'<div class="grid grid--two">{"".join(cols)}</div></div></section>')

def render_rankings_grid(mod):
    rows = "".join(
        f'<li class="conf--{conf}"><b>{rank}</b><span>{team}</span>'
        f'<i>{rec}</i></li>'
        for rank, team, rec, conf, _ in mod.TEAMS)
    return ('<section class="section" id="rankings"><div class="wrap">'
            '<h2>Power Rankings</h2>'
            f'<ol class="rgrid">{rows}</ol></div></section>')

def render_rankings(mod):
    out = ['<div class="wrap"><div class="teams teams--ranked">']
    for rank, team, rec, conf, text in mod.TEAMS:
        anchor = f' id="r{rank}"' if rank in (1, 9, 17, 25) else ""
        out.append(
            f'<article class="team tc {tslug(team)} conf--{conf}"{anchor}>'
            f'<i class="anch" id="{tslug(team)}" aria-hidden="true"></i>'
            f'<div class="rank" aria-hidden="true">{rank}</div>'
            f'<div class="team-body"><div class="team-head">'
            f'<h3>{team}</h3><span class="rec">{rec}</span></div>'
            f'<p>{text}</p></div></article>')
    out.append("</div></div>")
    return "".join(out)

def render_awards(awards):
    items = []
    for entry in awards:
        label, pick = entry[0], entry[1]
        runner = entry[2] if len(entry) > 2 else None
        block = f'<div class="award"><dt>{label}</dt><dd>{award_dd(*pick)}</dd>'
        if runner:
            block += (f'<dd class="runner"><span class="rlabel">Runner-up</span>'
                      f'{award_dd(*runner)}</dd>')
        items.append(block + "</div>")
    return ('<section class="section awards" id="awards"><div class="wrap">'
            '<h2>Awards</h2>'
            f'<dl class="award-list">{"".join(items)}</dl></div></section>')

def render_lede(mod):
    if not getattr(mod, "LEDE", None):
        return ""
    return ('<section class="lede"><div class="wrap">'
            f'<p>{mod.LEDE}</p></div></section>')

def render_body(ed):
    mod = ed["mod"]
    parts = [render_lede(mod)]
    if ed["type"] == "divisions":
        parts.append(render_standings_grid(mod))
        parts.append(render_divisions(mod, ed["extras"], ed.get("rec_label", "2024")))
        if hasattr(mod, "SEEDING"):
            parts.append(render_seeding(mod))
        parts.append(render_awards(mod.AWARDS))
    else:
        parts.append(render_rankings_grid(mod))
        parts.append(render_rankings(mod))
        parts.append(render_awards(mod.AWARDS))
    return "".join(parts)

def nav_links(ed):
    if ed["type"] == "divisions":
        links = [("#standings", "Standings")]
        for conf in ("afc", "nfc"):
            for d in DIV_ORDER:
                links.append((f"#{conf}-{d.lower()}", f"{conf.upper()} {d}"))
        if hasattr(ed["mod"], "SEEDING"):
            links.append(("#seeding", "Seeding"))
        links.append(("#awards", "Awards"))
    else:
        links = [("#rankings", "Rankings"), ("#r1", "1&ndash;8"), ("#r9", "9&ndash;16"),
                 ("#r17", "17&ndash;24"), ("#r25", "25&ndash;32"), ("#awards", "Awards")]
    return ('<nav class="nav" aria-label="Sections"><div class="nav-inner">'
            + "".join(f'<a href="{h}">{t}</a>' for h, t in links)
            + "</div></nav>")

def matchup(post):
    """Two-team colour strip for a game breakdown."""
    pair = post.get("teams")
    if not pair:
        return ""
    pal = TEAMS_MOD.palette()
    cells = []
    for slug in pair:
        d = pal.get(slug)
        if not d:
            raise SystemExit(f"Unknown team slug in post {post['slug']!r}: {slug!r}")
        cells.append(f'<div class="mu-team tc t-{slug}"><span class="mu-bar"></span>'
                     f'<span class="mu-name">{d["name"]}</span></div>')
    # "vs", not "at": the pair is written winner-first, which says nothing
    # about who hosted
    return f'<div class="matchup">{cells[0]}<span class="mu-v">vs</span>{cells[1]}</div>'

def post_classes(post):
    """Two teams colour from the first; one team also takes over the hero ground."""
    pair = post.get("teams")
    if pair:
        return f" tc t-{pair[0]}"
    solo = post.get("team")
    if solo:
        if solo not in TEAMS_MOD.TEAMS:
            raise SystemExit(f"Unknown team in post {post['slug']!r}: {solo!r}")
        return f" tc t-{solo} th-{solo}"
    return ""

def build_post(post):
    url = f"{SITE}/posts/{post['slug']}"
    author = post.get("author", "Adam Long")
    plain = strip_tags(post["title"])
    desc = f"{plain} by {author}."
    out = []
    for para in post["body"]:
        if isinstance(para, dict):          # {"quote": ..., "cite": ...}
            cite = (f'<cite>{para["cite"]}</cite>' if para.get("cite") else "")
            out.append(f'<blockquote class="post-quote"><p>{para["quote"]}</p>'
                       f'{cite}</blockquote>')
        elif isinstance(para, (list, tuple)):
            items = "".join(f"<li>{x}</li>" for x in para)
            out.append(f'<ul class="post-list">{items}</ul>')
        elif para.startswith("## "):
            out.append(f'<h2 class="post-h">{para[3:]}</h2>')
        else:
            out.append(f"<p>{para}</p>")
    body = "".join(out)
    if post.get("image"):
        src, alt = post["image"]
        body += (f'<figure class="post-fig">'
                 f'<img src="/assets/img/{src}" alt="{esc_attr(alt)}" '
                 f'loading="lazy"></figure>')
    # noindex keeps a page out of search results; the link still works for
    # anyone you send it to
    extra = ('<meta name="robots" content="noindex, nofollow">\n'
             if post.get("noindex") else "")
    html = (
        head(f"{plain} &mdash; 3rd &amp; Long", desc, url,
             f"og-post-{post['slug']}.png", extra)
        + site_bar()
        + f'<div class="hero hero--post{post_classes(post)}"><div class="wrap">'
          f'<p class="hero-eyebrow">{post["kind"]}</p>'
          f'<h1>{post["title"]}</h1>'
          f'<p class="byline"><span>By {author}</span>'
          f'<span class="sep">/</span><span class="dim">{post["date"]}</span></p>'
          '</div></div><div class="hash"></div>'
        + f'<main id="main"><section class="section post-body"><div class="wrap">'
          f'{matchup(post)}{body}</div></section></main>'
        + FOOT
        + f'<script src="/assets/js/nav.js{V["nav"]}" defer></script>\n</body>\n</html>\n')
    d = ROOT / "posts" / post["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    return len(html)

# ---------------------------------------------------------------- page shell

def head(title, desc, url, og_img, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{esc_attr(desc)}">
<meta name="author" content="Adam Long">
<link rel="canonical" href="{url}">

<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc_attr(strip_tags(title))}">
<meta property="og:description" content="{esc_attr(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc_attr(strip_tags(title))}">
<meta name="twitter:description" content="{esc_attr(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/{og_img}">

<meta name="theme-color" content="#EDEEE9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101317" media="(prefers-color-scheme: dark)">

<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Zilla+Slab:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css{V["css"]}">
<script src="/assets/js/team.js{V["team"]}"></script>
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def picker_panel():
    cols = []
    for label, members in TEAMS_MOD.by_division():
        rows = "".join(
            f'<button type="button" data-team="{slug}">'
            f'<span class="sw" style="background:{d["hero"]}"></span>{d["name"]}</button>'
            for slug, d in members)
        cols.append(f'<div class="pick-col"><h4>{label}</h4>{rows}</div>')
    return ('<div class="pick-panel" id="pickPanel" hidden>'
            f'<div class="pick-grid">{"".join(cols)}</div>'
            '<div class="pick-foot">'
            '<button type="button" class="pick-reset" data-team="">Clear</button>'
            '</div></div>')

def site_bar(home=False):
    name = (f'<p class="site-name">{SITE_NAME}</p>' if home
            else f'<a class="site-name" href="/">{SITE_NAME}</a>')
    back = ('<a class="bar-link" href="/teams">Teams</a>' if home else
            '<a class="bar-link" href="/teams">Teams</a>'
            '<a class="bar-link" href="/">All reports</a>')
    btn = ('<button type="button" class="pick-btn" id="pickBtn" aria-expanded="false" '
           'aria-controls="pickPanel"><span class="dot" aria-hidden="true"></span>'
           '<span id="pickLabel">Pick your team</span></button>')
    return ('<header class="site-bar"><div class="wrap">'
            f'{name}<div class="bar-right">{back}{btn}</div></div>'
            f'{picker_panel()}</header>')

FOOT = ('<div class="wrap"><footer class="foot">'
        f'<span>{SITE_NAME}</span><span>Adam Long</span>'
        '</footer></div>')

def team_entries():
    """Every paragraph Adam has written about each club, oldest edition last.

    Reads the same content modules the reports are built from, so a team page
    is a re-cut of his writing, never a summary of it.
    """
    out = {slug: [] for slug in TEAMS_MOD.TEAMS}
    for ed in EDITIONS:
        mod = ed["mod"]
        if ed["type"] == "divisions":
            for conf, div, teams in mod.DIVISIONS:
                for t in teams:
                    if ed.get("extras"):
                        rank, team, record, breakout, text = t
                    else:
                        rank, team, text = t
                        record = breakout = ""
                    meta = [f'{div} #{rank}']
                    if record:
                        meta.append(f'{ed.get("rec_label","")} {record}'.strip())
                    if breakout:
                        meta.append(f'Breakout: {breakout}')
                    out[tslug(team)[2:]].append((ed, " &middot; ".join(meta), text))
        else:
            for rank, team, rec, conf, text in mod.TEAMS:
                meta = [f'Ranked #{rank}']
                if rec:
                    meta.append(rec)
                out[tslug(team)[2:]].append((ed, " &middot; ".join(meta), text))
    return out


def team_posts(slug):
    return [p for p in POSTS
            if slug in (p.get("teams") or ()) or p.get("team") == slug]


def build_team(slug, entries):
    pal = TEAMS_MOD.palette()[slug]
    url = f"{SITE}/teams/{slug}"
    name = pal["name"]
    desc = f"Everything Adam Long has written about the {name}."

    blocks = []
    for ed, meta, text in entries:
        anchor = f'/{ed["slug"]}#t-{slug}'
        blocks.append(
            '<article class="tp-entry"><header>'
            f'<p class="tp-when">{ed["season"]} &middot; {ed["kind"]}</p>'
            f'<p class="tp-meta">{meta}</p></header>'
            f'<p>{text}</p>'
            f'<p class="tp-more"><a href="{anchor}">Read the full '
            f'{ed["season"]} {ed["kind"].lower()} report</a></p></article>')

    posts = team_posts(slug)
    if posts:
        cards = "".join(
            f'<a class="ed" href="/posts/{p["slug"]}">'
            f'<span class="when">{p["date"]} &middot; {p["kind"]}</span>'
            f'<h3>{p["title"]}</h3>'
            f'<span class="go">By {p.get("author", "Adam Long")}</span></a>'
            for p in posts)
        blocks.append('<div class="tp-posts"><h2>Posts</h2>'
                      f'<div class="ed-list">{cards}</div></div>')

    body = ("".join(blocks) if blocks
            else '<p class="tp-empty">No entries yet.</p>')

    html = (
        head(f"{name} &mdash; 3rd &amp; Long", desc, url, f"og-team-{slug}.png")
        + site_bar()
        + f'<div class="hero hero--post tc t-{slug} th-{slug}"><div class="wrap">'
          '<p class="hero-eyebrow">Team</p>'
          f'<h1>{name}</h1>'
          f'<p class="byline"><span>{len(entries)} report '
          f'{"entry" if len(entries) == 1 else "entries"}</span></p>'
          '</div></div><div class="hash"></div>'
        + f'<main id="main"><section class="section tp"><div class="wrap">'
          f'{body}</div></section></main>'
        + FOOT + "\n</body>\n</html>\n")
    d = ROOT / "teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    return len(html)


def build_teams_index():
    pal = TEAMS_MOD.palette()
    cols = []
    for label, members in TEAMS_MOD.by_division():
        rows = "".join(
            f'<li class="tc t-{slug}"><a href="/teams/{slug}">{d["name"]}</a></li>'
            for slug, d in members)
        cols.append(f'<div class="gcard"><h3>{label}</h3>'
                    f'<ul class="tix">{rows}</ul></div>')
    # wider tracks than the default grid: full club names shouldn't wrap
    url = f"{SITE}/teams"
    html = (
        head("Teams &mdash; 3rd &amp; Long",
             "Every club, and everything Adam Long has written about them.",
             url, "og-teams.png")
        + site_bar()
        + '<div class="hero hero--post"><div class="wrap">'
          '<p class="hero-eyebrow">Index</p><h1>Teams</h1>'
          '</div></div><div class="hash"></div>'
        + '<main id="main"><section class="section"><div class="wrap">'
          f'<div class="grid tix-grid">{"".join(cols)}</div>'
          '</div></section></main>'
        + FOOT + "\n</body>\n</html>\n")
    d = ROOT / "teams"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    return len(html)


# ---------------------------------------------------------------- pages

def build_edition(ed):
    url = f"{SITE}/{ed['slug']}"
    plain = strip_tags(ed["title"])
    desc = f'{plain} by {ed.get("author", "Adam Long")}.'
    sub = f'<p class="hero-sub">{ed["sub"]}</p>' if ed.get("sub") else ""
    html = (
        head(f"{plain} &mdash; 3rd &amp; Long", desc, url, f"og-{ed['slug']}.png")
        + site_bar()
        + '<div class="hero"><div class="wrap">'
          f'<p class="hero-eyebrow">{ed["kind"]}</p>'
          f'<h1>{ed["title"]}</h1>{sub}'
          f'<p class="byline"><span>By {ed.get("author", "Adam Long")}</span></p>'
          '</div></div><div class="hash"></div>'
        + nav_links(ed)
        + f'<main id="main">{render_body(ed)}</main>'
        + FOOT
        + f'<script src="/assets/js/nav.js{V["nav"]}" defer></script>\n</body>\n</html>\n')
    d = ROOT / ed["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    return len(html)

HERO_PHOTO = "hero.jpg"   # drop a file at assets/img/<this> and rebuild

def hero_photo():
    """Emit the photo layer only if the file is actually there."""
    if not (ROOT / "assets/img" / HERO_PHOTO).exists():
        return "", ""
    return (" has-photo",
            f'<div class="hero-photo" style="background-image:url(/assets/img/{HERO_PHOTO})"></div>')

def resolve_team(name, where):
    """Nickname or full club name -> palette slug. Loud on a miss."""
    n = name.strip().lower().rstrip(",")
    by_nick = {k: k for k in TEAMS_MOD.TEAMS}
    by_full = {v[0].lower(): k for k, v in TEAMS_MOD.TEAMS.items()}
    slug = by_full.get(n) or by_nick.get(n)
    if not slug:
        slug = next((k for k in by_nick if n.endswith(k)), None)
    if not slug:
        raise SystemExit(f"{where}: unknown team {name.strip()!r}")
    return slug


def team_exact(name):
    """Exact club lookup — nickname or full name. None on a miss, no guessing.

    Deliberately stricter than resolve_team(): this one runs against things that
    are usually player names, so the endswith fallback would be a liability.
    """
    n = name.strip().lower().rstrip(",.")
    if n in TEAMS_MOD.TEAMS:
        return n
    for k, v in TEAMS_MOD.TEAMS.items():
        if v[0].lower() == n:
            return k
    return None


RANK_RE = re.compile(r"^(T-)?(\d+)\.\s+(.*)$")


HIST, PREV = [], None

HISTORY = HERE / "content" / "power_history.json"


def week_slug(week):
    """'After Week 1' -> 'week-1'. Stable enough to be a URL for the season."""
    sl = re.sub(r"[^a-z0-9]+", "-", week.strip().lower()).strip("-")
    return re.sub(r"^after-", "", sl) or "week"


def load_history():
    if not HISTORY.exists():
        return []
    return json.loads(HISTORY.read_text(encoding="utf-8"))


def record_week(rows):
    """Append this week's board to the archive, or update it if already there.

    Keyed on WEEK, so rebuilding after a typo fix corrects that week rather than
    stacking a duplicate. The file is the only state the site keeps between
    builds, and it lives in _src, so it travels with the repo.
    """
    hist = load_history()
    if not rows:
        return hist, None
    entry = {"week": POWER_MOD.WEEK.strip(),
             "slug": week_slug(POWER_MOD.WEEK),
             "order": [slug for _r, slug, _n, _rec, _c in rows],
             "records": {slug: rec for _r, slug, _n, rec, _c in rows}}
    if hist and hist[-1]["week"] == entry["week"]:
        hist[-1] = entry
    else:
        hist.append(entry)
    HISTORY.write_text(json.dumps(hist, indent=1) + "\n", encoding="utf-8")
    prev = hist[-2] if len(hist) > 1 else None
    return hist, prev


def movement(slug, rank, prev):
    """+n / -n against the previous archived week. Blank for a team's first week."""
    if not prev or slug not in prev["order"]:
        return ""
    was = prev["order"].index(slug) + 1
    d = was - rank
    if d == 0:
        return '<s class="mv mv--flat" title="No change">&ndash;</s>'
    arrow = "&#9650;" if d > 0 else "&#9660;"
    cls = "up" if d > 0 else "down"
    word = "up" if d > 0 else "down"
    return (f'<s class="mv mv--{cls}" title="{word.capitalize()} {abs(d)} from {prev["week"]}">'
            f'{arrow}{abs(d)}</s>')


def parse_power():
    """The weekly 1-32 board, in the order it was typed."""
    raw = (POWER_MOD.RANKS or "").strip()
    if not raw or not (POWER_MOD.WEEK or "").strip():
        return None

    pal = TEAMS_MOD.palette()
    rows, seen = [], {}
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip().rstrip(",")
        if not line:
            continue
        line = re.sub(r"^\d+\.\s*", "", line)          # leading rank is decoration
        rec = ""
        m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", line)
        if m:
            line, rec = m.group(1).strip(), m.group(2).strip()
        slug = resolve_team(line, f"power.py line {lineno}")
        if slug in seen:
            raise SystemExit(f"power.py: {pal[slug]['name']} listed twice "
                             f"(lines {seen[slug]} and {lineno})")
        seen[slug] = lineno
        d = pal[slug]
        rows.append((len(rows) + 1, slug, d["name"], rec, d["conf"]))

    missing = [TEAMS_MOD.TEAMS[k][0] for k in TEAMS_MOD.TEAMS if k not in seen]
    if missing:
        raise SystemExit(f"power.py is missing {len(missing)} teams: "
                         + ", ".join(sorted(missing)))
    return rows


def power_board(rows, prev, linked=True):
    """The 1-32 list itself, shared by the landing page and the archive pages."""
    out = []
    for rank, slug, name, rec, conf in rows:
        label = (f'<a href="/teams/{slug}">{name}</a>') if linked else name
        out.append(f'<li class="tc t-{slug} conf--{conf}"><b>{rank}</b>'
                   f'<span>{label}</span>'
                   f'<i>{rec}</i>'
                   + (movement(slug, rank, prev) if prev else "") + "</li>")
    # no previous week on file means no movement column at all, rather than a
    # row of blanks that still eats width
    cls = "rgrid pr-grid" + ("" if prev else " pr-grid--nomv")
    return f'<ol class="{cls}">{"".join(out)}</ol>'


def archive_links(hist, current=None):
    """Only worth showing once there is more than one week on file."""
    if len(hist) < 2:
        return ""
    links = []
    for h in hist:
        if h["slug"] == current:
            links.append(f'<b>{h["week"]}</b>')
        else:
            links.append(f'<a href="/rankings/{h["slug"]}">{h["week"]}</a>')
    return f'<p class="wk-archive">{" ".join(links)}</p>'


def power_section(hist, prev):
    rows = parse_power()
    if not rows:
        return ""
    return ('<section class="section power-now" id="power"><div class="wrap">'
            '<h2>Power Rankings</h2>'
            f'<p class="stand-week">{POWER_MOD.WEEK}</p>'
            f'{power_board(rows, prev)}'
            f'{archive_links(hist, week_slug(POWER_MOD.WEEK))}'
            '</div></section>')


def build_week_page(hist, i):
    """One archived week, with the movement it had at the time."""
    h = hist[i]
    prev = hist[i - 1] if i else None
    pal = TEAMS_MOD.palette()
    rows = [(n + 1, slug, pal[slug]["name"], h.get("records", {}).get(slug, ""),
             pal[slug]["conf"])
            for n, slug in enumerate(h["order"])]
    url = f"{SITE}/rankings/{h['slug']}"
    title = f"Power Rankings &mdash; {h['week']}"
    html = (
        head(f"{title} &mdash; 3rd &amp; Long",
             f"NFL power rankings, {h['week']}, by Adam Long.", url,
             f"og-week-{h['slug']}.png")
        + site_bar()
        + '<div class="hero hero--post"><div class="wrap">'
          '<p class="hero-eyebrow">Power Rankings</p>'
          f'<h1>{h["week"]}</h1>'
          '<p class="byline"><span>By Adam Long</span></p>'
          '</div></div><div class="hash"></div>'
        + '<main id="main"><section class="section power-now"><div class="wrap">'
        + power_board(rows, prev)
        + archive_links(hist, h["slug"])
        + '</div></section></main>'
        + FOOT + "\n</body>\n</html>\n")
    d = ROOT / "rankings" / h["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")
    return len(html)


def parse_leaders():
    """Blocks of 'Category' then 'Player, Team, Value' lines. Order preserved."""
    raw = (LEADERS_MOD.LEADERS or "").strip()
    if not raw or not (LEADERS_MOD.WEEK or "").strip():
        return None

    pal = TEAMS_MOD.palette()
    blocks, current = [], None
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line:
            # a blank line closes a block only once that block has leaders in it,
            # so a heading can sit on its own line with air underneath
            if current and current[1]:
                current = None
            continue
        if current is None:
            current = (line, [])
            blocks.append(current)
            continue

        rank = ""
        m = RANK_RE.match(line)
        if m:
            rank = ("T-" if m.group(1) else "") + m.group(2)
            line = m.group(3)

        parts = [p.strip() for p in line.split(",") if p.strip()]
        if len(parts) < 2:
            raise SystemExit(f"leaders.py line {lineno}: can't read {line!r} "
                             "(expected at least 'Player, Value')")
        value, rest = parts[-1], parts[:-1]

        # last field before the value is a club -> it's the team column.
        # a lone field that IS a club -> the row is a team, colored, no sub-line.
        slug, club = "", ""
        if len(rest) > 1 and team_exact(rest[-1]):
            slug = team_exact(rest[-1])
            club = pal[slug]["name"]
            rest = rest[:-1]
        elif len(rest) == 1 and team_exact(rest[0]):
            slug = team_exact(rest[0])

        current[1].append((slug, rank, ", ".join(rest), club, value))

    blocks = [b for b in blocks if b[1]]
    if not blocks:
        raise SystemExit("leaders.py: WEEK is set but no leaders were listed")
    return blocks


def leaders_section():
    blocks = parse_leaders()
    if not blocks:
        return ""
    cards = []
    for title, rows in blocks:
        items = []
        for i, (slug, rank, player, club, value) in enumerate(rows, 1):
            open_tag = f'<li class="tc t-{slug}">' if slug else "<li>"
            sub_line = f"<em>{club}</em>" if club else ""
            items.append(f'{open_tag}<b>{rank or i}</b>'
                         f'<span class="ld-who">{player}{sub_line}</span>'
                         f'<i>{value}</i></li>')
        items = "".join(items)
        cards.append(f'<div class="gcard ld-card"><h3>{title}</h3>'
                     f'<ol class="ld-list">{items}</ol></div>')
    return ('<section class="section leaders-now" id="leaders"><div class="wrap">'
            '<h2>Stat Leaders</h2>'
            f'<p class="stand-week">{LEADERS_MOD.WEEK}</p>'
            f'<div class="grid">{"".join(cards)}</div>'
            '</div></section>')


def parse_standings():
    """Turn the pasted record block into division tables, or None if not set up yet.

    Accepts full club names or nicknames, in any order. Sorting is done here so
    the weekly update is only ever a list of records.
    """
    raw = (STANDINGS.RECORDS or "").strip()
    if not raw or not (STANDINGS.WEEK or "").strip():
        return None

    by_nick = {k: k for k in TEAMS_MOD.TEAMS}
    by_full = {v[0].lower(): k for k, v in TEAMS_MOD.TEAMS.items()}

    found = {}
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip().rstrip(",")
        if not line:
            continue
        m = re.match(r"^(.*?)[\s,]+(\d+)-(\d+)(?:-(\d+))?$", line)
        if not m:
            raise SystemExit(f"standings.py line {lineno}: can't read {line!r} "
                             "(expected e.g. 'Bills 4-1')")
        name = m.group(1).strip().lower().rstrip(",")
        w, l, t = int(m.group(2)), int(m.group(3)), int(m.group(4) or 0)

        slug = resolve_team(m.group(1), f"standings.py line {lineno}")
        if slug in found:
            raise SystemExit(f"standings.py: {TEAMS_MOD.TEAMS[slug][0]} listed twice")
        found[slug] = (w, l, t)

    missing = [TEAMS_MOD.TEAMS[k][0] for k in TEAMS_MOD.TEAMS if k not in found]
    if missing:
        raise SystemExit("standings.py is missing " + str(len(missing)) + " teams: "
                         + ", ".join(sorted(missing)))

    pal = TEAMS_MOD.palette()
    groups = []
    for conf in ("afc", "nfc"):
        for div in DIV_ORDER:
            rows = []
            for slug, (w, l, t) in found.items():
                d = pal[slug]
                if d["conf"] != conf or d["div"] != div:
                    continue
                played = w + l + t
                pct = (w + 0.5 * t) / played if played else 0.0
                rec = f"{w}-{l}" + (f"-{t}" if t else "")
                rows.append((slug, d["name"], rec, pct, w, w - l))
            # win pct, then win differential, then wins. The differential
            # matters early: 0-0 must outrank 0-1, and both are .000.
            rows.sort(key=lambda r: (-r[3], -r[5], -r[4], r[1]))
            groups.append((conf, f"{conf.upper()} {div}", rows))
    return groups


def standings_section():
    groups = parse_standings()
    if not groups:
        return ""
    cards = []
    for conf, label, rows in groups:
        items = "".join(
            f'<li class="tc t-{slug}"><b>{i}</b>'
            f'<span><a href="/teams/{slug}">{name}</a></span><i>{rec}</i></li>'
            for i, (slug, name, rec, _pct, _w, _d) in enumerate(rows, 1))
        cards.append(f'<div class="gcard conf--{conf}">'
                     f'<h3>{label}</h3><ol class="stand-list">{items}</ol></div>')
    return ('<section class="section standings-now" id="standings"><div class="wrap">'
            '<h2>Current Standings</h2>'
            f'<p class="stand-week">{STANDINGS.WEEK}</p>'
            f'<div class="grid">{"".join(cards)}</div>'
            '</div></section>')


def posts_section():
    """Only renders once there is something to show."""
    if not [p for p in POSTS if not p.get("unlisted")]:
        return ""
    rows = []
    for p in POSTS:
        if p.get("unlisted"):   # reachable by link, just not on the index
            continue
        rows.append(
            f'<a class="ed" href="/posts/{p["slug"]}">'
            f'<span class="when">{p["date"]} &middot; {p["kind"]}</span>'
            f'<h3>{p["title"]}</h3>'
            f'<span class="go">By {p.get("author", "Adam Long")}</span></a>')
    return ('<section class="section editions" id="posts"><div class="wrap">'
            '<h2>Posts</h2>'
            f'<div class="ed-list">{"".join(rows)}</div>'
            '</div></section>')

def home_nav(sections):
    """Sticky section tabs for the landing page.

    Built from the sections that actually rendered, so a blank WEEK or an empty
    posts list can never leave a tab pointing at nothing.
    """
    links = [(a, t) for a, t, body in sections if body]
    if len(links) < 2:
        return ""
    return ('<nav class="nav" aria-label="Sections"><div class="nav-inner">'
            + "".join(f'<a href="#{a}">{t}</a>' for a, t in links)
            + "</div></nav>")


def build_landing():
    cards = []
    for ed in EDITIONS:
        cards.append(
            f'<a class="ed" href="/{ed["slug"]}">'
            f'<span class="when">{ed["season"]} &middot; {ed["kind"]}</span>'
            f'<h3>{ed["title"]}</h3>'
            f'<span class="go">Read</span></a>')
    reports = ('<section class="section editions" id="reports"><div class="wrap">'
               '<h2>Reports</h2>'
               f'<div class="ed-list">{"".join(cards)}</div>'
               '</div></section>')
    sections = [
        ("power", "Power Rankings", power_section(HIST, PREV)),
        ("standings", "Standings", standings_section()),
        ("leaders", "Stat Leaders", leaders_section()),
        ("posts", "Posts", posts_section()),
        ("reports", "Reports", reports),
    ]
    html = (
        head("3rd &amp; Long", "NFL reports by Adam Long.", f"{SITE}/", "og.png")
        + site_bar(home=True)
        + f'<div class="hero hero--home{hero_photo()[0]}">{hero_photo()[1]}<div class="wrap">'
          '<h1>3rd &amp; Long</h1>'
          '<p class="byline"><span>Adam Long</span></p>'
          '<p class="hero-blurb">Your football roadmap for the next six months. Detailed analysis, predictions, and sleeper picks for the current NFL season. Fan written, fan created.</p>'
          '</div></div><div class="hash"></div>'
        + home_nav(sections)
        + '<main id="main">'
        + "".join(body for _a, _t, body in sections)
        + '</main>'
        + FOOT
        + f'<script src="/assets/js/nav.js{V["nav"]}" defer></script>'
          "\n</body>\n</html>\n")
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    return len(html)

# ---------------------------------------------------------------- artifact

def build_artifact(css):
    tabs = "".join(
        f'<button class="etab{" on" if i==0 else ""}" id="tab-{ed["slug"]}" '
        f'data-panel="{ed["slug"]}" type="button">{ed["season"]} {ed["kind"]}</button>'
        for i, ed in enumerate(EDITIONS))
    panels = []
    for i, ed in enumerate(EDITIONS):
        sub = f'<p class="hero-sub">{ed["sub"]}</p>' if ed.get("sub") else ""
        panels.append(
            f'<div class="panel" id="panel-{ed["slug"]}"{"" if i==0 else " hidden"}>'
            '<div class="hero"><div class="wrap">'
            f'<p class="hero-eyebrow">{ed["kind"]}</p>'
            f'<h1>{ed["title"]}</h1>{sub}'
            '<p class="byline"><span>By Adam Long</span></p>'
            '</div></div><div class="hash"></div>'
            f'{render_body(ed)}</div>')

    js = """
(function(){
  var tabs = [].slice.call(document.querySelectorAll('.etab'));
  tabs.forEach(function(t){
    t.addEventListener('click', function(){
      tabs.forEach(function(o){
        o.classList.toggle('on', o === t);
        document.getElementById('panel-' + o.dataset.panel).hidden = (o !== t);
      });
      window.scrollTo(0, 0);
    });
  });
})();
"""
    return (f"<title>3rd &amp; Long</title>\n<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Zilla+Slab:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap">\n'
            f"<style>{css}</style>\n"
            f'<header class="site-bar"><div class="wrap"><p class="site-name">{SITE_NAME}</p>'
            f'<div class="bar-right"><button type="button" class="pick-btn" id="pickBtn" '
            f'aria-expanded="false" aria-controls="pickPanel"><span class="dot" aria-hidden="true">'
            f'</span><span id="pickLabel">Pick your team</span></button></div></div>'
            f'{picker_panel()}</header>'
            f'<nav class="nav nav--tabs"><div class="nav-inner">{tabs}</div></nav>'
            + "".join(panels)
            + FOOT
            + f"<script>{team_js()}{js}</script>\n")

# ---------------------------------------------------------------- css

BASE = """/* ===========================================================
   3rd & Long — base
   =========================================================== */

*,*::before,*::after{box-sizing:border-box}
html{color-scheme:light}
:root[data-theme="dark"]{color-scheme:dark}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark}}
img,svg,video{max-width:100%;height:auto}
[hidden]{display:none!important}
:focus-visible{outline:2px solid var(--pick);outline-offset:2px}

.skip-link{
  position:absolute;left:-9999px;top:0;z-index:100;
  background:var(--ink);color:var(--ground);
  font-family:var(--f-cond);font-weight:600;font-size:.85rem;
  text-transform:uppercase;letter-spacing:.14em;
  padding:.7rem 1rem;text-decoration:none;
}
.skip-link:focus{left:0}

"""

EXTRA = """
/* ===========================================================
   components added for the multi-edition site
   =========================================================== */

a.site-name{text-decoration:none}
.bar-link{
  font-family:var(--f-cond);font-weight:600;font-size:.8rem;
  text-transform:uppercase;letter-spacing:.14em;
  color:var(--hero-muted);text-decoration:none;
}
.bar-link:hover{color:var(--hero-fg)}

.hero--home h1{font-size:clamp(3rem,11vw,6.5rem);max-width:none}
.hero-blurb{
  margin:1.6rem 0 0;max-width:56ch;
  font-size:clamp(1rem,2vw,1.15rem);line-height:1.55;
  color:var(--hero-muted);font-weight:300;
}
.hero-sub{
  font-family:var(--f-cond);font-weight:600;font-size:.9rem;
  text-transform:uppercase;letter-spacing:.2em;
  color:var(--hero-muted);margin:1rem 0 0;
}

/* edition tabs (artifact) */
.nav--tabs .nav-inner{gap:.25rem}
.etab{
  flex:0 0 auto;background:none;border:0;cursor:pointer;
  font-family:var(--f-cond);font-weight:600;font-size:.82rem;
  text-transform:uppercase;letter-spacing:.13em;color:var(--muted);
  padding:.85rem .55rem;border-bottom:2px solid transparent;white-space:nowrap;
}
.etab:hover{color:var(--ink)}
.etab.on{color:var(--ink);border-bottom-color:var(--pick)}

/* per-team meta (2025 preseason) */
.tmeta{
  display:flex;flex-wrap:wrap;gap:.35rem 1.5rem;margin:0 0 .9rem;
  font-family:var(--f-cond);font-size:.85rem;
}
.tmeta div{display:flex;gap:.45rem;align-items:baseline}
.tmeta dt{
  text-transform:uppercase;letter-spacing:.14em;color:var(--muted);font-weight:600;
}
.tmeta dd{margin:0;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}

/* record chip on power-ranking entries */
.rec{
  font-family:var(--f-cond);font-weight:600;font-size:.9rem;
  font-variant-numeric:tabular-nums;color:var(--muted);
  letter-spacing:.04em;
}

/* power-rankings summary */
.rgrid{
  list-style:none;margin:1.9rem 0 0;padding:0;
  display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));
  gap:1px;background:var(--rule);border:1px solid var(--rule);
}
.rgrid li{
  background:var(--surface);padding:.5rem .75rem;
  display:grid;grid-template-columns:1.85rem 1fr auto;gap:.5rem;align-items:baseline;
  font-family:var(--f-cond);font-size:.98rem;font-weight:500;
}
.rgrid b{font-variant-numeric:tabular-nums;font-weight:700;color:var(--conf)}
.rgrid i{font-style:normal;color:var(--muted);font-variant-numeric:tabular-nums;font-size:.88rem}

.teams--ranked{gap:clamp(1.75rem,3.5vw,2.4rem)}
.teams--ranked .team{scroll-margin-top:3.6rem}
.teams--ranked .rank{color:var(--conf)}

.grid--two{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.gcard li i{font-style:normal}

/* awards: pick + runner-up */
.award dd.runner{
  margin-top:.75rem;padding-top:.7rem;border-top:1px solid var(--rule);
}
.award dd.runner .who{font-size:1.05rem}
.rlabel{
  display:block;font-family:var(--f-cond);font-weight:600;font-size:.68rem;
  text-transform:uppercase;letter-spacing:.16em;color:var(--muted);margin-bottom:.15rem;
}

/* editions list */
.ed-list{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));
  gap:1rem;margin-top:1.9rem;
}
a.ed{
  display:flex;flex-direction:column;gap:.35rem;
  border:1px solid var(--rule);background:var(--surface);
  padding:1.15rem 1.2rem 1.25rem;text-decoration:none;color:inherit;
  border-left:3px solid var(--pick2);
  transition:border-color .15s ease,transform .15s ease;
}
a.ed:hover{transform:translateY(-2px)}
a.ed .when{
  font-family:var(--f-cond);font-weight:600;font-size:.76rem;
  text-transform:uppercase;letter-spacing:.16em;color:var(--muted);
}
a.ed h3{
  font-family:var(--f-display);font-weight:600;font-size:1.3rem;
  margin:0;line-height:1.18;
}

/* ===========================================================
   team palettes — one accent per club, contrast-fitted to both themes
   =========================================================== */

.tc{--team:var(--team-l)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tc{--team:var(--team-d)}}
:root[data-theme="dark"] .tc{--team:var(--team-d)}

__TEAMCSS__

.team.tc{gap:clamp(.6rem,2vw,1.05rem)}
.team.tc .rank{color:var(--team)}
.team.tc .team-body{
  border-left:3px solid var(--team);
  padding-left:clamp(.85rem,2.2vw,1.3rem);
}

/* the hero eyebrow sits on the themed hero, so it can't use the accent */
.hero-eyebrow{color:var(--hero-accent,var(--pick))}

/* ---------- team picker ---------- */

.site-bar{position:relative}
.bar-right{display:flex;align-items:center;gap:1rem}
.pick-btn{
  display:inline-flex;align-items:center;gap:.45rem;
  background:none;border:1px solid var(--hero-rule);border-radius:2px;
  color:var(--hero-fg);cursor:pointer;
  font-family:var(--f-cond);font-weight:600;font-size:.74rem;
  text-transform:uppercase;letter-spacing:.14em;
  padding:.3rem .6rem .26rem;
}
.pick-btn:hover{border-color:var(--hero-fg)}
.pick-btn .dot{
  width:.62rem;height:.62rem;border-radius:50%;
  background:currentColor;flex:0 0 .62rem;
}
.pick-panel{
  position:absolute;left:0;right:0;top:100%;z-index:40;
  background:var(--surface);border-bottom:1px solid var(--rule);
  padding:1.4rem var(--pad) 1.1rem;
  box-shadow:0 14px 30px rgba(0,0,0,.2);
}
.pick-grid{
  max-width:1120px;margin:0 auto;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(184px,1fr));
  gap:1.3rem 1.6rem;
}
.pick-col h4{
  font-family:var(--f-cond);font-weight:700;font-size:.72rem;
  text-transform:uppercase;letter-spacing:.18em;color:var(--muted);
  margin:0 0 .5rem;
}
.pick-col button{
  display:flex;align-items:center;gap:.55rem;width:100%;
  background:none;border:0;padding:.26rem 0;cursor:pointer;text-align:left;
  font-family:var(--f-cond);font-weight:500;font-size:.95rem;color:var(--ink-2);
}
.pick-col button:hover{color:var(--ink)}
.pick-col button .sw{
  width:.72rem;height:.72rem;flex:0 0 .72rem;border-radius:1px;
  outline:1px solid rgba(128,128,128,.35);outline-offset:-1px;
}
.pick-foot{
  max-width:1120px;margin:1.1rem auto 0;padding-top:.9rem;
  border-top:1px solid var(--rule);
}
.pick-reset{
  background:none;border:0;padding:0;cursor:pointer;
  font-family:var(--f-cond);font-weight:600;font-size:.74rem;
  text-transform:uppercase;letter-spacing:.14em;color:var(--muted);
}
.pick-reset:hover{color:var(--ink)}

@media (max-width:520px){
  .bar-right{gap:.7rem}
  .pick-btn{font-size:.7rem;letter-spacing:.1em}
}


/* ---------- optional hero photograph ---------- */

.hero{position:relative;isolation:isolate}
.hero .wrap{position:relative;z-index:2}
.hero-photo{
  position:absolute;inset:0;z-index:1;
  background-size:cover;background-position:center 38%;
}
.hero-photo::after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(100deg,
    var(--hero-bg) 0%,
    var(--hero-bg) 26%,
    color-mix(in srgb,var(--hero-bg) 72%,transparent) 55%,
    color-mix(in srgb,var(--hero-bg) 34%,transparent) 100%);
}
.hero.has-photo .wrap{padding-block:clamp(3rem,9vw,6rem) clamp(3.5rem,9vw,6rem)}

/* at phone width the text sits over the middle of the frame, so the scrim
   has to come from the bottom instead of the side */
@media (max-width:680px){
  .hero-photo::after{
    background:linear-gradient(180deg,
      color-mix(in srgb,var(--hero-bg) 62%,transparent) 0%,
      color-mix(in srgb,var(--hero-bg) 88%,transparent) 45%,
      var(--hero-bg) 100%);
  }
}


/* ---------- short posts ---------- */

.hero--post h1{max-width:20ch}
.post-body p{
  max-width:var(--measure);margin:0 0 1.15rem;color:var(--ink-2);
  font-size:1.08rem;line-height:1.68;
}
.post-body p:last-child{margin-bottom:0}
.post-body p:first-of-type{font-size:1.2rem;line-height:1.6;color:var(--ink)}

.matchup{
  display:flex;align-items:stretch;gap:1.1rem;flex-wrap:wrap;
  margin:0 0 2.2rem;padding-bottom:1.6rem;
  border-bottom:1px solid var(--rule);
}
.mu-team{display:flex;align-items:center;gap:.7rem}
.mu-bar{width:6px;align-self:stretch;min-height:2rem;background:var(--team)}
.mu-name{
  font-family:var(--f-cond);font-weight:700;
  font-size:clamp(1.05rem,2.8vw,1.35rem);
  text-transform:uppercase;letter-spacing:.015em;
}
.mu-v{
  align-self:center;font-family:var(--f-cond);font-weight:600;font-size:.8rem;
  text-transform:uppercase;letter-spacing:.18em;color:var(--muted);
}


/* ---------- weekly power rankings ---------- */

.editions,.power-now,.standings-now,.leaders-now{scroll-margin-top:3.4rem}
.power-now .rgrid{margin-top:1.4rem}
/* The in-report grid flows left to right. A weekly board should read straight
   down the column instead: 1 under 2 under 3. CSS columns fill top-to-bottom,
   so the rules go on the rows and on the column gutter, not through a grid gap.
   Wider tracks than the in-report grid too, so "Washington Commanders" still
   sits on one line next to its record. */
.pr-grid{
  display:block;columns:3;column-gap:1px;gap:0;
  column-rule:1px solid var(--rule);
  background:var(--surface);border-bottom:0;
}
.pr-grid li{break-inside:avoid;border-bottom:1px solid var(--rule)}
@media (max-width:900px){.pr-grid{columns:2}}
@media (max-width:620px){.pr-grid{columns:1}}
.pr-grid b{color:var(--team,var(--conf))}
.pr-grid li{font-weight:600;color:var(--ink-2)}
.pr-grid span{min-width:0}






.post-quote{
  max-width:var(--measure);margin:1.6rem 0 1.8rem;
  padding-left:clamp(.9rem,2vw,1.4rem);
  border-left:3px solid var(--team,var(--pick));
}
.post-quote p{
  font-size:clamp(1.05rem,2vw,1.2rem);font-style:italic;color:var(--ink);
  line-height:1.45;
}
.post-quote cite{
  display:block;margin-top:.6rem;font-style:normal;
  font-family:var(--f-cond);font-weight:600;font-size:.82rem;
  text-transform:uppercase;letter-spacing:.14em;color:var(--muted);
}

.post-h{
  font-family:var(--f-display);font-weight:700;
  font-size:clamp(1.25rem,2.4vw,1.55rem);line-height:1.2;letter-spacing:-.015em;
  max-width:var(--measure);margin:2.4rem 0 .9rem;
}
.post-body p + .post-h{margin-top:2.4rem}
.post-list{
  max-width:var(--measure);margin:1rem 0 0;padding-left:1.1rem;
  display:grid;gap:.7rem;
}
.post-list li{padding-left:.2rem}

.post-fig{margin:1.8rem 0 0;max-width:var(--measure)}
.post-fig img{display:block;width:100%;height:auto;border:1px solid var(--rule)}

/* ---------- team pages ---------- */

.anch{display:block;height:0;scroll-margin-top:4.5rem}
.tp{padding-top:clamp(2rem,4vw,3rem)}
.tp-entry{
  max-width:var(--measure);
  padding-bottom:clamp(1.6rem,3vw,2.2rem);
  margin-bottom:clamp(1.6rem,3vw,2.2rem);
  border-bottom:1px solid var(--rule);
}
.tp-entry:last-of-type{border-bottom:0}
.tp-when{
  margin:0;font-family:var(--f-cond);font-weight:700;font-size:.78rem;
  text-transform:uppercase;letter-spacing:.16em;color:var(--team,var(--pick));
}
.tp-meta{
  margin:.25rem 0 .9rem;font-family:var(--f-cond);font-size:.85rem;
  color:var(--muted);letter-spacing:.03em;
}
.tp-entry p{margin:0}
.tp-more{margin-top:.9rem!important}
.tp-more a{
  font-family:var(--f-cond);font-weight:600;font-size:.78rem;
  text-transform:uppercase;letter-spacing:.14em;
  color:var(--pick);text-decoration:none;
}
.tp-more a:hover{text-decoration:underline}
.tp-posts{margin-top:clamp(1.5rem,3vw,2.2rem)}
.tp-posts h2{margin-bottom:1rem}
.tp-empty{color:var(--muted)}

.tix-grid{grid-template-columns:repeat(auto-fill,minmax(360px,1fr))}
.tix{list-style:none;margin:0;padding:0;display:grid;gap:.4rem}
.tix li{
  /* .gcard li is a two-column grid for numbered lists; these rows are just a name */
  display:block;
  font-family:var(--f-cond);font-size:1rem;font-weight:600;
  border-left:3px solid var(--team,var(--rule));padding-left:.6rem;
}
.tix a{color:var(--ink-2);text-decoration:none}
.tix a:hover{color:var(--ink);text-decoration:underline}

.team{scroll-margin-top:4.5rem}

/* movement against last week's archived board */
.mv{
  text-decoration:none;font-style:normal;
  font-family:var(--f-cond);font-weight:700;font-size:.78rem;
  font-variant-numeric:tabular-nums;letter-spacing:.02em;
  margin-left:.5rem;white-space:nowrap;
}
.mv--up{color:var(--up)}
.mv--down{color:var(--down)}
.mv--flat{color:var(--rule)}

.wk-archive{
  margin:1.1rem 0 0;font-family:var(--f-cond);font-size:.82rem;
  text-transform:uppercase;letter-spacing:.13em;color:var(--muted);
  display:flex;flex-wrap:wrap;gap:.2rem 1rem;
}
.wk-archive a{color:var(--pick);text-decoration:none}
.wk-archive a:hover{text-decoration:underline}
.wk-archive b{color:var(--ink)}

/* team names on the weekly boards link to that club's page */
.pr-grid span a,.stand-list span a{color:inherit;text-decoration:none}
.pr-grid span a:hover,.stand-list span a:hover{text-decoration:underline}
.pr-grid li{grid-template-columns:1.85rem 1fr auto auto}
.pr-grid--nomv li{grid-template-columns:1.85rem 1fr auto}

/* the club's second colour, and the tick strip under the hero. Both default
   to what the site already used, so nothing changes until a team is picked. */
:root{--pick2:var(--pick);--hash-tick:var(--hero-rule)}

:root{--up:#1F7A3D;--down:#C0392B}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){--up:#1B9D46;--down:#EF4231}
}
:root[data-theme="dark"]{--up:#1B9D46;--down:#EF4231}

/* ---------- weekly standings ---------- */

.standings-now .grid{margin-top:1.4rem}
.stand-week{
  font-family:var(--f-cond);font-weight:600;font-size:.82rem;
  text-transform:uppercase;letter-spacing:.16em;color:var(--muted);
  margin:.6rem 0 0;
}
.stand-list{list-style:none;margin:0;padding:0;display:grid;gap:.32rem}
.stand-list li{
  display:grid;grid-template-columns:1.35rem 1fr auto;gap:.5rem;align-items:baseline;
  font-family:var(--f-cond);font-size:1rem;font-weight:500;color:var(--muted);
}
.stand-list li b{font-variant-numeric:tabular-nums;font-weight:600;color:var(--rule)}
.stand-list li i{
  font-style:normal;font-variant-numeric:tabular-nums;
  font-size:.92rem;color:var(--muted);
}
.stand-list li:first-child{color:var(--ink);font-weight:700}
.stand-list li:first-child b{color:var(--team,var(--conf))}
.stand-list li:first-child i{color:var(--ink-2);font-weight:600}


/* ---------- stat leaders ---------- */

.leaders-now .grid{margin-top:1.4rem}
.ld-list{list-style:none;margin:0;padding:0;display:grid;gap:.55rem}
.ld-list li{
  display:grid;grid-template-columns:minmax(1.35rem,auto) 1fr auto;gap:.55rem;
  align-items:baseline;
  font-family:var(--f-cond);font-size:1rem;color:var(--ink-2);
}
.ld-list li b{
  font-variant-numeric:tabular-nums;font-weight:700;
  color:var(--team,var(--muted));
}
.ld-who{display:flex;flex-direction:column;min-width:0;overflow-wrap:break-word;line-height:1.28}
.ld-who em{
  font-style:normal;font-size:.82rem;color:var(--muted);
  letter-spacing:.06em;text-transform:uppercase;margin-top:.05rem;
}
.ld-list li i{
  font-style:normal;font-variant-numeric:tabular-nums;
  font-weight:700;color:var(--ink);
}
.ld-list li:first-child{color:var(--ink);font-weight:600}
/* .gcard li:first-child b paints the top row with --conf, which these cards
   don't have. The club color is the point here, so take it back. */
.ld-list li:first-child b{color:var(--team,var(--muted))}
/* the category count is yours, so the last row can end short — same trick as
   the power grid: rules on the cards, not through the gaps */
.leaders-now .grid{background:var(--surface)}
.leaders-now .ld-card{outline:1px solid var(--rule)}

a.ed .go{
  margin-top:.5rem;font-family:var(--f-cond);font-weight:600;font-size:.78rem;
  text-transform:uppercase;letter-spacing:.16em;color:var(--pick);
}
"""

def team_js():
    import json
    pal = TEAMS_MOD.palette()
    table = {k: {"name": v["name"], "l": v["light"], "d": v["dark"],
                 "l2": v["pick2L"], "d2": v["pick2D"], "tk": v["hashTick"],
                 "bg": v["hero"], "fg": v["heroFg"],
                 "mu": v["heroMuted"], "ru": v["heroRule"]}
             for k, v in pal.items()}
    return "(function(){var T=" + json.dumps(table, separators=(",", ":")) + ";" + r"""
var root=document.documentElement,KEY="tal.team",VARS=["--pick","--pick2","--hash-tick","--hero-bg","--hero-fg","--hero-muted","--hero-rule","--hero-accent"];
function isDark(){var a=root.getAttribute("data-theme");
  if(a==="dark")return true; if(a==="light")return false;
  try{return matchMedia("(prefers-color-scheme: dark)").matches}catch(e){return false}}
function read(){try{return localStorage.getItem(KEY)||""}catch(e){return ""}}
function save(v){try{v?localStorage.setItem(KEY,v):localStorage.removeItem(KEY)}catch(e){}}
function label(t){var el=document.getElementById("pickLabel");if(el)el.textContent=t}
function apply(slug){
  var t=T[slug],st=root.style;
  if(!t){VARS.forEach(function(p){st.removeProperty(p)});root.removeAttribute("data-team");label("Pick your team");return}
  st.setProperty("--pick",isDark()?t.d:t.l);
  st.setProperty("--pick2",isDark()?t.d2:t.l2);
  st.setProperty("--hash-tick",t.tk);
  st.setProperty("--hero-bg",t.bg);
  st.setProperty("--hero-fg",t.fg);
  st.setProperty("--hero-muted",t.mu);
  st.setProperty("--hero-rule",t.ru);
  st.setProperty("--hero-accent",t.fg);
  root.setAttribute("data-team",slug);
  label(t.name);
}
apply(read());
try{matchMedia("(prefers-color-scheme: dark)").addEventListener("change",function(){apply(read())})}catch(e){}
function wire(){
  label(T[read()]?T[read()].name:"Pick your team");
  var btn=document.getElementById("pickBtn"),panel=document.getElementById("pickPanel");
  if(!btn||!panel)return;
  function open(v){panel.hidden=!v;btn.setAttribute("aria-expanded",v?"true":"false")}
  btn.addEventListener("click",function(e){e.stopPropagation();open(panel.hidden)});
  panel.addEventListener("click",function(e){
    var b=e.target.closest("button[data-team]");if(!b)return;
    var v=b.getAttribute("data-team");save(v);apply(v);open(false)});
  document.addEventListener("click",function(e){
    if(!panel.hidden&&!panel.contains(e.target)&&e.target!==btn)open(false)});
  document.addEventListener("keydown",function(e){if(e.key==="Escape")open(false)});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",wire);else wire();
})();"""

# ---------------------------------------------------------------- run

def main():
    for p in ["assets/css", "assets/js", "assets/img"]:
        (ROOT / p).mkdir(parents=True, exist_ok=True)

    core = (HERE / "core.css").read_text(encoding="utf-8").strip()
    js = (HERE / "core.js").read_text(encoding="utf-8").strip()

    pal = TEAMS_MOD.palette()
    tcss = "\n".join(
        f'.t-{k}{{--team-l:{v["light"]};--team-d:{v["dark"]}}}\n'
        # the club's hero ground, already walked until its text clears 4.5:1
        f'.th-{k}{{--hero-bg:{v["hero"]};--hero-fg:{v["heroFg"]};'
        f'--hero-muted:{v["heroMuted"]};--hero-accent:{v["heroMuted"]};'
        f'--hero-rule:{v["heroRule"]}}}'
        for k, v in sorted(pal.items()))
    css = BASE + core + "\n" + EXTRA.replace("__TEAMCSS__", tcss)
    (ROOT / "assets/css/styles.css").write_text(css, encoding="utf-8")
    (ROOT / "assets/js/team.js").write_text(
        "/* Per-team palettes + the picker in the masthead. */\n" + team_js() + "\n",
        encoding="utf-8")
    (ROOT / "assets/js/nav.js").write_text(
        "/* Highlights the current section in the sticky nav while you scroll. */\n"
        + js + "\n", encoding="utf-8")

    import hashlib
    def ver(path):
        h = hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]
        return f"?v={h}"
    V["css"] = ver("assets/css/styles.css")
    V["team"] = ver("assets/js/team.js")
    V["nav"] = ver("assets/js/nav.js")

    global HIST, PREV
    HIST, PREV = record_week(parse_power())

    n = build_landing()
    print(f"index.html                {n:>7,} bytes")
    for ed in EDITIONS:
        n = build_edition(ed)
        print(f"{ed['slug']}/index.html  {n:>7,} bytes")

    for post in POSTS:
        n = build_post(post)
        print(f"posts/{post['slug']}/index.html  {n:>7,} bytes")

    for i, h in enumerate(HIST):
        n = build_week_page(HIST, i)
        print(f"rankings/{h['slug']}/index.html  {n:>7,} bytes")

    entries = team_entries()
    for slug in sorted(entries):
        build_team(slug, entries[slug])
    print(f"teams/*/index.html        {len(entries)} clubs")
    n = build_teams_index()
    print(f"teams/index.html          {n:>7,} bytes")

    art = build_artifact(css)
    (HERE / "artifact.html").write_text(art, encoding="utf-8")
    print(f"artifact.html             {len(art):>7,} bytes")

    urls = ([f"{SITE}/"] + [f"{SITE}/{e['slug']}" for e in EDITIONS]
            + [f"{SITE}/posts/{p['slug']}" for p in POSTS if not p.get("noindex")]
            + [f"{SITE}/rankings/{h['slug']}" for h in HIST]
            + [f"{SITE}/teams"]
            + [f"{SITE}/teams/{slug}" for slug in sorted(TEAMS_MOD.TEAMS)])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    print(f"sitemap.xml               {len(urls)} urls")

main()
