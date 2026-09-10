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

ROOT = HERE.parent

SITE = "https://thirdandlong.vercel.app"
SITE_NAME = "3rd &amp; Long"

# ---------------------------------------------------------------- editions

EDITIONS = [
    dict(slug="2026-preseason", kind="Preseason",
         title="2026&ndash;2027 NFL Preseason Report", season="2026",
         type="divisions", mod=PS26, extras=False),
    dict(slug="2025-midseason", kind="Midseason",
         title="2025 NFL Midseason Report", season="2025",
         type="rankings", mod=MS25, sub="Power Rankings"),
    dict(slug="2025-preseason", kind="Preseason",
         title="2025&ndash;2026 NFL Preseason Report", season="2025",
         type="divisions", mod=PS25, extras=True),
    dict(slug="2024-midseason", kind="Midseason",
         title="2024 NFL Midseason Report", season="2024",
         type="rankings", mod=MS24, sub="Week 10 Power Rankings"),
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

def render_divisions(mod, extras):
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
                            f'<div><dt>2024</dt><dd>{record}</dd></div>'
                            f'<div><dt>Breakout Candidate</dt><dd>{breakout}</dd></div>'
                            '</dl>')
                else:
                    rank, team, text = t
                    meta = ""
                first = " team--1" if rank == 1 else ""
                out.append(
                    f'<article class="team tc {tslug(team)}{first}">'
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
            f'<div class="rank" aria-hidden="true">{rank}</div>'
            f'<div class="team-body"><div class="team-head">'
            f'<h3>{team}</h3><span class="rec">{rec}</span></div>'
            f'<p>{text}</p></div></article>')
    out.append("</div></div>")
    return "".join(out)

def render_awards_single(awards):
    items = "".join(
        f'<div class="award"><dt>{label}</dt><dd>{award_dd(*pick)}</dd></div>'
        for label, pick in awards)
    return ('<section class="section awards" id="awards"><div class="wrap">'
            '<h2>Awards</h2>'
            f'<dl class="award-list">{items}</dl></div></section>')

def render_awards_pair(awards):
    items = []
    for label, pick, runner in awards:
        items.append(
            f'<div class="award"><dt>{label}</dt>'
            f'<dd>{award_dd(*pick)}</dd>'
            f'<dd class="runner"><span class="rlabel">Runner-up</span>'
            f'{award_dd(*runner)}</dd></div>')
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
        parts.append(render_divisions(mod, ed["extras"]))
        if hasattr(mod, "SEEDING"):
            parts.append(render_seeding(mod))
        parts.append(render_awards_single(mod.AWARDS))
    else:
        parts.append(render_rankings_grid(mod))
        parts.append(render_rankings(mod))
        parts.append(render_awards_pair(mod.AWARDS))
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
<link rel="stylesheet" href="/assets/css/styles.css">
<script src="/assets/js/team.js"></script>
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
    back = "" if home else '<a class="bar-link" href="/">All reports</a>'
    btn = ('<button type="button" class="pick-btn" id="pickBtn" aria-expanded="false" '
           'aria-controls="pickPanel"><span class="dot" aria-hidden="true"></span>'
           '<span id="pickLabel">Pick your team</span></button>')
    return ('<header class="site-bar"><div class="wrap">'
            f'{name}<div class="bar-right">{back}{btn}</div></div>'
            f'{picker_panel()}</header>')

FOOT = ('<div class="wrap"><footer class="foot">'
        f'<span>{SITE_NAME}</span><span>Adam Long</span>'
        '</footer></div>')

# ---------------------------------------------------------------- pages

def build_edition(ed):
    url = f"{SITE}/{ed['slug']}"
    plain = strip_tags(ed["title"])
    desc = f"{plain} by Adam Long."
    sub = f'<p class="hero-sub">{ed["sub"]}</p>' if ed.get("sub") else ""
    html = (
        head(f"{plain} &mdash; 3rd &amp; Long", desc, url, f"og-{ed['slug']}.png")
        + site_bar()
        + '<div class="hero"><div class="wrap">'
          f'<p class="hero-eyebrow">{ed["kind"]}</p>'
          f'<h1>{ed["title"]}</h1>{sub}'
          '<p class="byline"><span>By Adam Long</span></p>'
          '</div></div><div class="hash"></div>'
        + nav_links(ed)
        + f'<main id="main">{render_body(ed)}</main>'
        + FOOT
        + '<script src="/assets/js/nav.js" defer></script>\n</body>\n</html>\n')
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

def build_landing():
    cards = []
    for ed in EDITIONS:
        cards.append(
            f'<a class="ed" href="/{ed["slug"]}">'
            f'<span class="when">{ed["season"]} &middot; {ed["kind"]}</span>'
            f'<h3>{ed["title"]}</h3>'
            f'<span class="go">Read</span></a>')
    html = (
        head("3rd &amp; Long", "NFL reports by Adam Long.", f"{SITE}/", "og.png")
        + site_bar(home=True)
        + f'<div class="hero hero--home{hero_photo()[0]}">{hero_photo()[1]}<div class="wrap">'
          '<h1>3rd &amp; Long</h1>'
          '<p class="byline"><span>Adam Long</span></p>'
          '<p class="hero-blurb">Your football roadmap for the next six months. Detailed analysis, predictions, and sleeper picks for the current NFL season. Fan written, fan created.</p>'
          '</div></div><div class="hash"></div>'
        + '<main id="main"><section class="section editions"><div class="wrap">'
          '<h2>Reports</h2>'
          f'<div class="ed-list">{"".join(cards)}</div>'
          '</div></section></main>'
        + FOOT + "\n</body>\n</html>\n")
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
  border-left:3px solid var(--pick);
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

a.ed .go{
  margin-top:.5rem;font-family:var(--f-cond);font-weight:600;font-size:.78rem;
  text-transform:uppercase;letter-spacing:.16em;color:var(--pick);
}
"""

def team_js():
    import json
    pal = TEAMS_MOD.palette()
    table = {k: {"name": v["name"], "l": v["light"], "d": v["dark"],
                 "bg": v["hero"], "fg": v["heroFg"],
                 "mu": v["heroMuted"], "ru": v["heroRule"]}
             for k, v in pal.items()}
    return "(function(){var T=" + json.dumps(table, separators=(",", ":")) + ";" + r"""
var root=document.documentElement,KEY="tal.team",VARS=["--pick","--hero-bg","--hero-fg","--hero-muted","--hero-rule","--hero-accent"];
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
        f'.t-{k}{{--team-l:{v["light"]};--team-d:{v["dark"]}}}' for k, v in sorted(pal.items()))
    css = BASE + core + "\n" + EXTRA.replace("__TEAMCSS__", tcss)
    (ROOT / "assets/css/styles.css").write_text(css, encoding="utf-8")
    (ROOT / "assets/js/team.js").write_text(
        "/* Per-team palettes + the picker in the masthead. */\n" + team_js() + "\n",
        encoding="utf-8")
    (ROOT / "assets/js/nav.js").write_text(
        "/* Highlights the current section in the sticky nav while you scroll. */\n"
        + js + "\n", encoding="utf-8")

    n = build_landing()
    print(f"index.html                {n:>7,} bytes")
    for ed in EDITIONS:
        n = build_edition(ed)
        print(f"{ed['slug']}/index.html  {n:>7,} bytes")

    art = build_artifact(css)
    (HERE / "artifact.html").write_text(art, encoding="utf-8")
    print(f"artifact.html             {len(art):>7,} bytes")

    urls = [f"{SITE}/"] + [f"{SITE}/{e['slug']}" for e in EDITIONS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    print(f"sitemap.xml               {len(urls)} urls")

main()
