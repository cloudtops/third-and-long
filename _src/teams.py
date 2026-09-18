"""Team palettes + the contrast math that makes them usable on both themes.

Brand colors are picked for ink legibility, not logo accuracy: where a club's
primary is black or white, its secondary stands in. Colors only — no logos,
no wordmarks.
"""
import colorsys

GROUND_LIGHT = "#EDEEE9"
GROUND_DARK = "#101317"

# nickname-slug: (display name, primary, secondary, conference, division)
TEAMS = {
 "bills":      ("Buffalo Bills",        "#00338D", "#C60C30", "afc", "East"),
 "dolphins":   ("Miami Dolphins",       "#008E97", "#FC4C02", "afc", "East"),
 "patriots":   ("New England Patriots", "#002244", "#C60C30", "afc", "East"),
 "jets":       ("New York Jets",        "#125740", "#FFFFFF", "afc", "East"),

 "ravens":     ("Baltimore Ravens",     "#241773", "#9E7C0C", "afc", "North"),
 "bengals":    ("Cincinnati Bengals",   "#FB4F14", "#101820", "afc", "North"),
 "browns":     ("Cleveland Browns",     "#FF3C00", "#311D00", "afc", "North"),
 "steelers":   ("Pittsburgh Steelers",  "#FFB612", "#101820", "afc", "North"),

 "texans":     ("Houston Texans",       "#03202F", "#A71930", "afc", "South"),
 "colts":      ("Indianapolis Colts",   "#002C5F", "#A2AAAD", "afc", "South"),
 "jaguars":    ("Jacksonville Jaguars", "#006778", "#D7A22A", "afc", "South"),
 "titans":     ("Tennessee Titans",     "#0C2340", "#4B92DB", "afc", "South"),

 "broncos":    ("Denver Broncos",       "#FB4F14", "#002244", "afc", "West"),
 "chiefs":     ("Kansas City Chiefs",   "#E31837", "#FFB81C", "afc", "West"),
 "raiders":    ("Las Vegas Raiders",    "#A5ACAF", "#101820", "afc", "West"),
 "chargers":   ("Los Angeles Chargers", "#0080C6", "#FFC20E", "afc", "West"),

 "bears":      ("Chicago Bears",        "#0B162A", "#C83803", "nfc", "North"),
 "lions":      ("Detroit Lions",        "#0076B6", "#B0B7BC", "nfc", "North"),
 "packers":    ("Green Bay Packers",    "#203731", "#FFB612", "nfc", "North"),
 "vikings":    ("Minnesota Vikings",    "#4F2683", "#FFC62F", "nfc", "North"),

 "cowboys":    ("Dallas Cowboys",       "#003594", "#869397", "nfc", "East"),
 "giants":     ("New York Giants",      "#0B2265", "#A71930", "nfc", "East"),
 "eagles":     ("Philadelphia Eagles",  "#004C54", "#A5ACAF", "nfc", "East"),
 "commanders": ("Washington Commanders","#5A1414", "#FFB612", "nfc", "East"),

 "falcons":    ("Atlanta Falcons",      "#A71930", "#101820", "nfc", "South"),
 "panthers":   ("Carolina Panthers",    "#0085CA", "#101820", "nfc", "South"),
 "saints":     ("New Orleans Saints",   "#D3BC8D", "#101820", "nfc", "South"),
 "buccaneers": ("Tampa Bay Buccaneers", "#D50A0A", "#FF7900", "nfc", "South"),

 "cardinals":  ("Arizona Cardinals",    "#97233F", "#FFB612", "nfc", "West"),
 "rams":       ("Los Angeles Rams",     "#003594", "#FFA300", "nfc", "West"),
 "49ers":      ("San Francisco 49ers",  "#AA0000", "#B3995D", "nfc", "West"),
 "seahawks":   ("Seattle Seahawks",     "#002244", "#69BE28", "nfc", "West"),
}

# ------------------------------------------------------------------ color math

def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def _hex(r, g, b):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c * 255))) for c in (r, g, b))

def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _lum(h):
    r, g, b = _rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def _shift(h, dl, sat_boost=1.0):
    r, g, b = _rgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = max(0.02, min(0.98, ll + dl))
    # never saturate a near-neutral: silver must stay silver, not drift to blue
    if ss > 0.15:
        ss = max(0.0, min(1.0, ss * sat_boost))
    return _hex(*colorsys.hls_to_rgb(hh, ll, ss))

def fit(color, ground, target=4.5, lighten=False):
    """Nudge lightness until the color clears `target` contrast against `ground`."""
    cur = color
    boost = 1.06 if lighten else 1.0
    for _ in range(70):
        if contrast(cur, ground) >= target:
            return cur
        nxt = _shift(cur, 0.02 if lighten else -0.02, boost)
        if nxt == cur:
            break
        cur = nxt
    return cur

def readable_on(bg):
    """Pick ink or chalk for text sitting on `bg`."""
    return "#101418" if contrast("#101418", bg) >= contrast("#F2F3EF", bg) else "#F2F3EF"

def mix(a, b, t):
    ra, ga, ba = _rgb(a); rb, gb, bb = _rgb(b)
    return _hex(ra + (rb - ra) * t, ga + (gb - ga) * t, ba + (bb - ba) * t)

# ------------------------------------------------------------------ derived

def chroma(color):
    """Raw colourfulness, 0-1. Cheap, and it does the one job needed here.

    HLS saturation lies about near-blacks: #101820 reads 0.33 because it is a
    very dark blue, but on screen it is black. Max minus min channel doesn't.
    _rgb returns 0-1 floats, so this is on that scale too.
    """
    r, g, b = _rgb(color)
    return max(r, g, b) - min(r, g, b)


# below this, a "second colour" is really black, white or silver, and using it
# as an accent just looks like the accent broke
CHROMA_FLOOR = 0.16


def hero_muted(fg, hero):
    """The hero's secondary text: dimmed toward the ground, but never past 4.5:1.

    A flat 42% mix reads fine on the near-black default ground and fails on ten
    of the club colours, so the mix backs off until it clears.
    """
    t = 0.42
    out = mix(fg, hero, t)
    while contrast(out, hero) < 4.5 and t > 0.02:
        t -= 0.03
        out = mix(fg, hero, t)
    return out


def palette():
    """slug -> every color the site needs for that team, precomputed."""
    out = {}
    for slug, (name, primary, secondary, conf, div) in TEAMS.items():
        # the entry accent has to read on both grounds
        light = fit(primary, GROUND_LIGHT, 4.5, lighten=False)
        dark = fit(primary, GROUND_DARK, 4.5, lighten=True)
        # a near-black primary can't be lightened into anything but grey — fall back
        # to the secondary, but only if the secondary is actually a color
        if contrast(dark, GROUND_DARK) < 4.5 and _sat(secondary) >= 0.25:
            alt = fit(secondary, GROUND_DARK, 4.5, lighten=True)
            if contrast(alt, GROUND_DARK) >= 4.5:
                dark = alt
        # mid-tone brands where neither ink nor chalk clears 4.5 on the raw hex:
        # walk the hero ground away from the text until it does
        hero = primary
        fg = readable_on(hero)
        for _ in range(40):
            if contrast(fg, hero) >= 4.5:
                break
            hero = _shift(hero, 0.02 if fg == "#101418" else -0.02)
        # the second accent: only when the club actually has one
        if chroma(secondary) >= CHROMA_FLOOR:
            pick2_l = fit(secondary, GROUND_LIGHT, 4.5, lighten=False)
            pick2_d = fit(secondary, GROUND_DARK, 4.5, lighten=True)
            # the hash strip sits on the club's own hero ground, and it is a
            # graphic rather than text, so 3:1 is the bar
            tick = fit(secondary, hero, 3.0, lighten=(fg != "#101418"))
            if contrast(tick, hero) < 3.0:
                tick = mix(fg, hero, 0.76)
        else:
            pick2_l, pick2_d = light, dark
            tick = mix(fg, hero, 0.76)

        out[slug] = dict(
            name=name, conf=conf, div=div,
            light=light, dark=dark,
            pick2L=pick2_l, pick2D=pick2_d, hashTick=tick,
            hero=hero, heroFg=fg,
            heroMuted=hero_muted(fg, hero),
            heroRule=mix(fg, hero, 0.76),
        )
    return out

def _sat(h):
    r, g, b = _rgb(h)
    return colorsys.rgb_to_hls(r, g, b)[2]

DIV_ORDER = ["North", "East", "South", "West"]

def by_division():
    p = palette()
    groups = []
    for conf in ("afc", "nfc"):
        for div in DIV_ORDER:
            members = [(s, p[s]) for s in TEAMS
                       if p[s]["conf"] == conf and p[s]["div"] == div]
            groups.append((f"{conf.upper()} {div}", sorted(members, key=lambda x: x[1]["name"])))
    return groups

NAME_TO_SLUG = {v[0]: k for k, v in TEAMS.items()}
