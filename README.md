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
├── index.html                  landing page — weekly sections + list of reports
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
                                plus power.py / standings.py / leaders.py,
                                the three weekly updates
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

The landing page's own tabs generate from whichever sections rendered, so a
blank `WEEK` or an empty posts list never leaves a tab pointing at nothing.

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

## Weekly power rankings

`_src/content/power.py`. Set `WEEK`, then list all 32 teams in your order, one
per line. The leading number is decoration — the build renumbers from the order
you typed, so moving a team up is a cut and paste, never a renumber. The record
in parentheses is optional.

```
1. Seattle Seahawks (1-0)
Buffalo Bills (1-0)
49ers
```

Blank `WEEK` hides the section; a missing or misspelled team stops the build and
names it.

**The archive runs itself.** Every build writes the current board into
`_src/content/power_history.json`, keyed on `WEEK`, and publishes it at
`/rankings/<week>`. Rebuilding the same week corrects that entry rather than
adding a duplicate, so fixing a typo is safe. Once there are two weeks on file
each team gets a movement chip against the previous one, and a row of links to
past weeks appears under the board. Don't hand-edit the JSON; change `power.py`
and rebuild.

## Weekly standings

`_src/content/standings.py` is the one file you touch during the season. Set
`WEEK` to the dateline, paste the 32 records into `RECORDS`, one per line.
Nicknames or full names, any order:

```
Bills 4-1
Miami Dolphins 1-4
Packers 3-1-1
```

The build sorts each division by win percentage (a tie counts as half a win),
so you never reorder anything — you are only ever updating numbers. Then
`python3 _src/build.py` and push.

Two guards, both deliberate: leaving `WEEK` blank hides the whole section, so
the site never shows stale standings; and if any of the 32 teams is missing or
misspelled the build stops and names it, rather than publishing a table with
holes in it.

## Stat leaders

`_src/content/leaders.py`, same rhythm as standings. Set `WEEK`, then blocks
separated by a blank line — first line is the category, the rest are leaders:

```
Passing Yards
Sam Darnold, Seahawks, 253
Drake Maye, Patriots, 241

Sacks
Maxx Crosby, Raiders, 2.0
```

You pick the categories; they aren't fixed in the code. The team is optional
and colors the row — drop it and write `Player, Value` instead. If the whole row
*is* a club (`San Francisco 49ers, 70.3%`), it gets that club's color too.

Rank is optional. Start a line with `1.` or `T-1.` and it prints exactly that;
leave it off and the build numbers down the list. For a tie, put every name on
one line with the value last:

```
T-1. Derrick Henry, D&rsquo;Andre Swift, 3
```

Nothing is re-sorted. Your typed order is the published order, which is why
values can be anything: `1,204`, `4.5`, `12 (T-1st)`. Blank `WEEK` hides the
section; a misspelled team stops the build and names it.

## Team pages

`/teams/<slug>` collects every paragraph written about a club across all four
reports, newest first, each linking back to its place in the full report, plus
any posts tagged with that team. `/teams` is the index, linked from the masthead
on every page, and the team names on the power rankings and standings link
straight through.

Nothing here is authored. The pages re-cut `_src/content/*.py` at build time, so
a new report shows up on all 32 team pages the moment it's added to `EDITIONS`.

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
