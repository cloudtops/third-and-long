# 3rd & Long

NFL reports by Adam Long. Static site — no build step at deploy time, no
dependencies, no framework.

**All editorial copy on this site is written by Adam.** The generator supplies
structure only: navigation, section headings that repeat his own section names,
and functional UI text (button labels, the 404 page, alt text). If you add a
report, put the text in `_src/content/` and rebuild — don't write prose into
the templates.

---

## Files

```
.
├── index.html                  landing page — list of reports
├── 2026-preseason/index.html
├── 2025-midseason/index.html
├── 2025-preseason/index.html
├── 2024-midseason/index.html
├── 404.html
├── favicon.ico                 32/16 — legacy browsers
├── favicon.svg                 modern browsers, scales cleanly
├── apple-touch-icon.png        180×180 — iOS home screen
├── icon-192.png / icon-512.png PWA
├── site.webmanifest
├── robots.txt
├── sitemap.xml
├── vercel.json                 clean URLs + asset caching
├── assets/
│   ├── css/styles.css          all styling, token-driven
│   ├── js/nav.js               sticky-nav scroll spy (the only JS on the site)
│   └── img/og-*.png            1200×630 link preview card per report
└── _src/                       the generator
    ├── build.py
    ├── render.py               regenerates the og cards and icons
    └── content/*.py            one module per report — the actual writing
```

The icon is a sideline down marker: yellow ground, black numeral. High contrast
so it still reads at 16px in a tab strip.

---

## Deploy

### Vercel

```bash
git init
git add .
git commit -m "3rd & Long"
gh repo create third-and-long --public --source=. --push
```

Import the repo at [vercel.com/new](https://vercel.com/new). Framework preset:
**Other**. No build command, no output directory — the HTML is already built.

Or from the terminal:

```bash
npx vercel --prod
```

### GitHub Pages

Push to `main`, then Settings → Pages → Source: **Deploy from a branch** →
`main` / `root`.

Catch: a project page serves from `/<repo-name>/`, which breaks the
root-absolute asset paths. Either use a custom domain, or set `SITE` in
`_src/build.py` and find/replace `href="/` → `href="./`.

---

## After you pick a domain

Link previews need absolute URLs or iMessage and Slack show nothing. Change
`SITE` at the top of `_src/build.py` and re-run it, then update `robots.txt`.

```bash
python3 _src/build.py
```

Test the preview at [opengraph.dev](https://opengraph.dev).

---

## Adding a report

1. Copy the closest existing module in `_src/content/` — `preseason2026.py`
   for a division-standings report, `midseason2025.py` for power rankings.
2. Paste your text into it. Keep it verbatim; the build escapes nothing, so
   write `&amp;` for a literal ampersand and use `<em>` for italics.
3. Add an entry to the `EDITIONS` list at the top of `_src/build.py` — slug,
   kind (Preseason / Midseason), title, season, and type
   (`divisions` or `rankings`).
4. Add a card to `CARDS` in `_src/render.py` so it gets a link preview.
5. Run `python3 _src/build.py && python3 _src/render.py`.

The landing page, sitemap, and nav all generate from `EDITIONS`, so nothing
else needs touching.

---

## Posts (game of the week, blog entries, guest pieces)

Short pieces live in `_src/content/posts.py` as a list of dicts, newest first,
and publish to `/posts/<slug>`. The file has the full field reference at the
top. Add an entry, run `python3 _src/build.py`, done — the landing page grows a
"Posts" section, the sitemap picks it up, nothing else to touch.

The `Posts` section is hidden entirely while the list is empty, so the site
doesn't advertise a section with nothing in it.

**Guest writers:** set `author` on the post and the byline follows through to
the page, the meta description, and the landing card. Same field works on the
big reports in `EDITIONS`.

**Game breakdowns:** set `teams=("lions", "bears")` using slugs from
`teams.py`, and the post gets a matchup strip with both clubs' colors. An
unknown slug fails the build with the offending value rather than rendering
a colorless strip.

## Team colors

`_src/teams.py` holds all 32 palettes and the contrast math. Two things use it:

**Per-entry accent (always on).** Every team's rank numeral and left spine take
that club's primary. The class is emitted at build time from the team name in
the copy, so a typo in a team name fails the build loudly rather than silently
losing the color.

**The picker (opt-in).** The control in the masthead stores a choice in
`localStorage` and sets `--pick` and the `--hero-*` tokens from that team's
palette. Conference crimson/navy is deliberately left alone so the standings
still read AFC vs NFC at a glance.

Every color is contrast-fitted, not used raw: each palette is nudged in
lightness until it clears 4.5:1 against the light ground and again against the
dark ground, and hero text picks ink or chalk by luminance — with the hero
ground itself walked a few steps if neither clears. That's why the Steelers
render as `#8F6200` on white and `#FFB612` on black rather than one unreadable
gold. Colors only, no logos or wordmarks.

## How the CSS works

Everything is driven by custom properties at the top of `styles.css`. Three
theme states are handled: bare `:root` is light, a `prefers-color-scheme: dark`
media query covers the default "system" setting, and
`:root[data-theme="dark"|"light"]` lets you force one if you add a toggle.

Conference color is set per-section by `.conf--afc` / `.conf--nfc`, which
define a local `--conf` that rank numerals, team names, and division kickers
all read from. Restyle a conference by changing one variable.

Type is Zilla Slab (headlines + body) and Archivo Narrow (team names, numerals,
labels), both from Google Fonts. Swap them via `--f-display` and `--f-cond` in
`_src/core.css` — but the rank rail and team-name sizes are tuned to Archivo
Narrow's width, so a much narrower or wider face needs those clamps retuned.
