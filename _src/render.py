"""Link preview cards, one per page, generated from the site's own content.

Run after build.py. Every card is 1200x630 and carries information rather than
just a title, because a card with an empty right half is the thing that makes a
site look like a template.

    python3 _src/build.py && python3 _src/render.py
"""

import asyncio, re, sys, json
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
TMP = HERE / ".cards"; TMP.mkdir(exist_ok=True)

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "content"))
import teams as T
import power as POWER
import standings as STANDINGS
from posts import POSTS
import preseason2026 as PS26, preseason2025 as PS25
import midseason2025 as MS25, midseason2024 as MS24

PAL = T.palette()
NAME_TO_SLUG = T.NAME_TO_SLUG

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo+Narrow:wght@500;600;700&'
         'family=Zilla+Slab:wght@400;600;700&display=swap">')

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:630px;overflow:hidden;background:#101418;color:#EDEEE9;
 font-family:"Zilla Slab",Georgia,serif}
.mast{font-family:"Archivo Narrow",sans-serif;font-weight:700;font-size:24px;
 text-transform:uppercase;letter-spacing:.28em}
.kick{font-family:"Archivo Narrow",sans-serif;font-weight:600;font-size:21px;
 text-transform:uppercase;letter-spacing:.2em;color:#8B9490}
.who{font-family:"Archivo Narrow",sans-serif;font-weight:600;font-size:21px;
 text-transform:uppercase;letter-spacing:.16em}
"""

def page(css, body):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}'
            f"<style>{BASE}{css}</style></head><body>{body}</body></html>")


# ---------------------------------------------------------------- the board

BOARD_CSS = """
body{display:grid;grid-template-columns:1fr 1fr}
.left{padding:58px 34px 52px 68px;display:flex;flex-direction:column;min-width:0}
h1{font-weight:700;font-size:54px;line-height:1.02;letter-spacing:-.03em;
 margin-top:auto;margin-bottom:18px}
.left .kick{margin-top:9px;font-size:19px}
.right{background:#171B20;padding:44px 64px 44px 38px;display:flex;
 flex-direction:column;justify-content:center;min-width:0}
/* the label column has to hold "AFC N" on one line, or the rows double in
   height and eight of them stop fitting on a 630px card */
.row{display:grid;grid-template-columns:78px 1fr auto;gap:14px;align-items:baseline;
 padding:11px 0;border-bottom:1px solid #2C333A;
 font-family:"Archivo Narrow",sans-serif;font-size:23px;font-weight:600}
.row:last-child{border-bottom:0}
.row span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.row b{font-variant-numeric:tabular-nums;font-weight:700;font-size:20px;
 letter-spacing:.08em;white-space:nowrap}
.row i{font-style:normal;color:#8B9490;font-size:20px;font-variant-numeric:tabular-nums}
"""

def board_card(title, kicker, rows, foot):
    """rows: (label, colour, name, right)"""
    body_rows = "".join(
        f'<div class="row"><b style="color:{col}">{lab}</b>'
        f'<span>{name}</span><i>{right}</i></div>'
        for lab, col, name, right in rows)
    return page(BOARD_CSS,
        f'<div class="left"><span class="mast">3rd &amp; Long</span>'
        f'<h1>{title}</h1><div class="who">By Adam Long</div>'
        f'<div class="kick">{foot}</div></div>'
        f'<div class="right">{body_rows}</div>')


# ---------------------------------------------------------------- scoreboard

def score_card(a_slug, a_name, a_pts, b_slug, b_name, b_pts, kicker):
    A, B = PAL[a_slug], PAL[b_slug]
    css = """
body{display:flex;flex-direction:column}
.top{flex:1;display:grid;grid-template-columns:1fr 1fr}
.side{display:flex;flex-direction:column;justify-content:center;padding:0 68px;gap:6px}
.side.b{text-align:right;align-items:flex-end}
.club{font-family:"Archivo Narrow",sans-serif;font-weight:700;font-size:38px;
 text-transform:uppercase;letter-spacing:.1em;line-height:1.05}
.score{font-family:"Archivo Narrow",sans-serif;font-weight:700;font-size:162px;
 line-height:.86;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.bar{display:flex;justify-content:space-between;align-items:center;
 padding:24px 68px;background:#101418;
 font-family:"Archivo Narrow",sans-serif;font-weight:600;font-size:23px;
 text-transform:uppercase;letter-spacing:.18em}
.bar .dim{color:#8B9490}
"""
    return page(css,
        f'<div class="top">'
        f'<div class="side a" style="background:{A["hero"]};color:{A["heroFg"]}">'
        f'<span class="club">{a_name}</span><span class="score">{a_pts}</span></div>'
        f'<div class="side b" style="background:{B["hero"]};color:{B["heroFg"]}">'
        f'<span class="club">{b_name}</span><span class="score">{b_pts}</span></div>'
        f'</div><div class="bar"><span class="mast">3rd &amp; Long</span>'
        f'<span class="dim">{kicker}</span></div>')


# ---------------------------------------------------------------- club field

def club_card(slug, title, kicker, foot, foot_right=None):
    d = PAL[slug]
    foot_right = foot_right or d["name"]
    # a club name fits at 104px; a player-and-team headline does not, and an
    # overflowing card silently loses its footer
    plain = re.sub("<[^>]+>", "", title)
    size, measure = ((104, 11) if len(plain) <= 24 else
                     (74, 16) if len(plain) <= 40 else (56, 22))
    css = """
body{display:flex;flex-direction:column;padding:56px 68px 50px}
h1{font-weight:700;font-size:__SIZE__px;line-height:.98;letter-spacing:-.035em;
 margin-top:auto;max-width:__MEASURE__ch}
.row{display:flex;justify-content:space-between;align-items:baseline}
.foot{display:flex;justify-content:space-between;align-items:baseline;
 margin-top:26px;padding-top:22px;
 font-family:"Archivo Narrow",sans-serif;font-weight:600;font-size:21px;
 text-transform:uppercase;letter-spacing:.16em}
"""
    return page(css,
        f'<div class="row" style="color:{d["heroFg"]}">'
        f'<span class="mast">3rd &amp; Long</span>'
        f'<span class="kick" style="color:{d["heroMuted"]}">{kicker}</span></div>'
        f'<h1 style="color:{d["heroFg"]}">{title}</h1>'
        f'<div class="foot" style="color:{d["heroMuted"]};'
        f'border-top:1px solid {d["heroRule"]}">'
        f'<span>{foot}</span><span>{foot_right}</span></div>',
    ).replace("background:#101418", f'background:{d["hero"]}') \
     .replace("__SIZE__", str(size)).replace("__MEASURE__", str(measure))


# ---------------------------------------------------------------- plain title

STRIPES = "".join(
    f'<i style="background:{PAL[k]["hero"]}"></i>'
    for k in sorted(PAL, key=lambda k: (PAL[k]["conf"], PAL[k]["name"])))

def title_card(title, kicker, byline):
    css = """
body{display:flex;flex-direction:column;padding:58px 68px 0}
h1{font-weight:700;font-size:78px;line-height:1.0;letter-spacing:-.03em;
 max-width:15ch;margin-top:auto;margin-bottom:22px}
.row{display:flex;justify-content:space-between;align-items:baseline}
.who{padding-bottom:28px}
.band{display:flex;height:20px;margin:0 -68px}
.band i{flex:1}
"""
    return page(css,
        f'<div class="row"><span class="mast">3rd &amp; Long</span>'
        f'<span class="kick">{kicker}</span></div>'
        f'<h1>{title}</h1><div class="who">{byline}</div>'
        f'<div class="band">{STRIPES}</div>')


# ---------------------------------------------------------------- data helpers

def strip_tags(s):
    return re.sub("<[^>]+>", "", s).replace("&amp;", "&").replace("&ndash;", "–")


def power_rows(order, records, n=6):
    rows = []
    for i, slug in enumerate(order[:n], 1):
        d = PAL[slug]
        rows.append((str(i), d["dark"], d["name"], records.get(slug, "")))
    return rows


def division_leaders(mod, rec_label):
    rows = []
    for conf, div, tms in mod.DIVISIONS:
        for t in tms:
            if t[0] != 1:
                continue
            name, rec = t[1], (t[2] if len(t) == 5 else "")
            slug = NAME_TO_SLUG[name]
            rows.append((f"{conf.upper()} {div[:1]}", PAL[slug]["dark"], name, rec))
    return rows


def ranked_top(mod, n=8):
    rows = []
    for rank, name, rec, conf, _text in mod.TEAMS[:n]:
        slug = NAME_TO_SLUG[name]
        rows.append((str(rank), PAL[slug]["dark"], name, rec))
    return rows


SCORE_RE = re.compile(r"^(.*?)\s+(\d+),\s+(.*?)\s+(\d+)$")

# ---------------------------------------------------------------- the job list

def jobs():
    out = []

    hist = json.loads((HERE / "content" / "power_history.json").read_text())
    if hist:
        cur = hist[-1]
        out.append(("og.png", board_card(
            "NFL Power Rankings", "", power_rows(cur["order"], cur.get("records", {})),
            f'{cur["week"]} &middot; 32 teams')))
        for h in hist:
            out.append((f'og-week-{h["slug"]}.png', board_card(
                "Power Rankings", "", power_rows(h["order"], h.get("records", {})),
                h["week"])))

    out.append(("og-2026-preseason.png", board_card(
        "2026&ndash;2027 Preseason Report", "", division_leaders(PS26, "2025"),
        "Division picks &middot; 32 teams")))
    out.append(("og-2025-preseason.png", board_card(
        "2025&ndash;2026 Preseason Report", "", division_leaders(PS25, "2024"),
        "Division picks &middot; 32 teams")))
    out.append(("og-2025-midseason.png", board_card(
        "2025 Midseason Report", "", ranked_top(MS25),
        "Power rankings &middot; 32 teams")))
    out.append(("og-2024-midseason.png", board_card(
        "2024 Midseason Report", "", ranked_top(MS24),
        "Power rankings &middot; 32 teams")))

    for p in POSTS:
        name = f'og-post-{p["slug"]}.png'
        kicker = f'{p["kind"]} &middot; {p["date"]}'
        title = strip_tags(p["title"])
        m = SCORE_RE.match(title)
        pair = p.get("teams")
        if m and pair:
            out.append((name, score_card(pair[0], m.group(1), m.group(2),
                                         pair[1], m.group(3), m.group(4), kicker)))
        elif p.get("team"):
            out.append((name, club_card(p["team"], p["title"], p["kind"],
                                        f'By {p.get("author", "Adam Long")}')))
        else:
            out.append((name, title_card(p["title"], kicker,
                                         f'By {p.get("author", "Adam Long")}')))

    for slug, d in PAL.items():
        # the club name is already the headline, so the footer carries the
        # division instead of saying it twice
        out.append((f"og-team-{slug}.png",
                    club_card(slug, d["name"], "Team", "Every report entry",
                              f'{d["conf"].upper()} {d["div"]}')))

    out.append(("og-teams.png", title_card("Teams", "Index", "All 32 clubs")))
    return out


ICON = """<!doctype html><html><head><meta charset="utf-8">
<style>*{box-sizing:border-box;margin:0;padding:0}
html,body{width:512px;height:512px;overflow:hidden}svg{display:block}</style></head><body>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <rect width="512" height="512" fill="#101418"/>
  <g fill="#F2C74A">
    <rect x="112" y="70" width="88" height="185"/>
    <rect x="312" y="70" width="88" height="185"/>
    <rect x="112" y="255" width="288" height="88"/>
    <rect x="212" y="343" width="88" height="99"/>
  </g>
</svg></body></html>"""


async def main():
    work = jobs()
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(device_scale_factor=1)
        await pg.set_viewport_size({"width": 1200, "height": 630})
        for name, html in work:
            f = TMP / (name + ".html")
            f.write_text(html, encoding="utf-8")
            await pg.goto("file://" + str(f), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / "assets/img" / name))
        print(f"{len(work)} link preview cards")

        f = TMP / "icon.html"; f.write_text(ICON, encoding="utf-8")
        await pg.set_viewport_size({"width": 512, "height": 512})
        await pg.goto("file://" + str(f), wait_until="networkidle")
        await pg.screenshot(path=str(OUT / "icon-512.png"))
        await b.close()

asyncio.run(main())
