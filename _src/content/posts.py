# Short posts — game-of-the-week breakdowns, blog entries, guest pieces.
#
# Newest first. Every field is yours to write; nothing here is generated.
#
#   slug    url segment, lives at /posts/<slug>
#   kind    the eyebrow above the title, e.g. "Game of the Week", "Notebook"
#   title   the headline
#   author  byline — set this for guest writers
#   date    whatever dateline you want: "Week 3", "Week 3 · 2026", "November 2026"
#   teams   optional ("slug", "slug") from teams.py — draws the matchup strip
#           and colors the post with both clubs. NFL only; leave it off for a
#           college game or anything else the 32 palettes don't cover.
#   body    list of paragraphs. Use &rsquo; for apostrophes, <em>..</em> for italics.
#
# Example of the shape (delete the quotes and fill it in):
#
# dict(
#     slug="week-1-lions-bears",
#     kind="Game of the Week",
#     title="...",
#     author="Adam Long",
#     date="Week 1",
#     teams=("lions", "bears"),
#     body=["First paragraph.", "Second paragraph."],
# ),

POSTS = [
    dict(
        slug="week-1-bills-texans",
        kind="Game of the Week",
        title="Buffalo 36, Houston 31",
        author="Adam Long",
        date="Week 1",
        teams=("bills", "texans"),
        body=[
            "After a heartbreaking loss in the divisional round last year, the "
            "Buffalo Bills start off 2026 with a chip on their shoulder and eyes "
            "for their franchise&rsquo;s first Lombardi Trophy. Storylines galore "
            "ahead of this one on whether or not QB Josh Allen could get it done "
            "against a Texans defense that has given him fits in recent years. We "
            "got a fairly resounding &ldquo;Yes&rdquo; in that regard, as the "
            "Bills&rsquo; signal caller, who accounted for 357 total yards to go "
            "along with four total touchdowns, led Buffalo to an electrifying win "
            "over one of the league&rsquo;s most vaunted defenses. After dealing "
            "with the lack of a true blue #1 target for Allen over the last few "
            "years, the Bills may have finally found their man in newcomer WR D.J. "
            "Moore, who came over from Chicago. Moore accounted for 100 yards on "
            "the nose to go along with a touchdown grab, and cemented himself as "
            "Buffalo&rsquo;s top receiving option alongside TE Dalton Kincaid. "
            "Kincaid, who excelled against the Texans&rsquo; staunch secondary in "
            "his own right, hauled in five passes to the tune of 130 yards. Allen "
            "has made a strong case for his second MVP season through one week of "
            "play. Buffalo&rsquo;s defense looked lost at times, but eventually "
            "played just well enough to secure the W against Houston QB C.J. "
            "Stroud, who showed shades of his excellent 2023 form in which he won "
            "Offensive Rookie of the Year. Stroud guided the Houston offense right "
            "down to the wire until their last-gasp opportunity was foiled by "
            "Stroud&rsquo;s second lost fumble of the contest. Turnovers have "
            "plagued Stroud in recent years, as the quarterback&rsquo;s pair of "
            "fumbles (including the one that lost the game) surely had Texans fans "
            "flashing back in horror to the absolute disasterclass that was their "
            "2025 divisional round matchup in New England. Houston&rsquo;s biggest "
            "bright spot on offense looks to be the addition of RB David "
            "Montgomery, who accounted for 79 total yards and three total "
            "touchdowns.",

            "The biggest surprise for me in this matchup was how outmatched "
            "Houston&rsquo;s defense looked against Allen and the Bills. Allen "
            "cemented himself and his squad as the apex of the AFC, and Houston "
            "now has a longer road ahead, especially if their calling card may not "
            "be as vicious as advertised.",
        ],
    ),
    dict(
        slug="week-1-texas-ohio-state",
        kind="Bonus",
        title="Texas 24, Ohio State 23",
        author="Adam Long",
        date="Week 1",
        body=[
            "The college football world&rsquo;s first marquee matchup of the "
            "season pitted the top-ranked Ohio State Buckeyes against the "
            "fourth-ranked Texas Longhorns. In what was certainly the best game of "
            "the day, and what will likely be one of the best games of the season, "
            "Texas rallied from a 20-point fourth-quarter deficit to upset the "
            "nation&rsquo;s #1 team in front of a packed home stadium in Austin.",

            "Saturday was a tale of two halves for both teams. The Buckeyes began "
            "the day firing on all cylinders both offensively and defensively, as "
            "Arthur Smith and Matt Patricia had their respective units rolling to "
            "the tune of a 20-3 lead going into halftime. Junior QB Julian Sayin "
            "reignited his connection with Heisman hopeful WR Jeremiah Smith, who "
            "had eight receptions for 164 yards and a score. Ohio State&rsquo;s "
            "defense locked up QB Arch Manning and Co. for the entire first three "
            "quarters, although the score could&rsquo;ve been much closer at the "
            "half if not for a few key drops by Longhorns receivers. Manning was "
            "much better than his statline indicated (23/37, 195 yd, 1 TD/1 INT), "
            "especially in the clutch when it mattered most. At the start of the "
            "fourth quarter, Manning was a man possessed, consistently escaping "
            "pressure and fitting balls into tight windows to move the chains. "
            "After a late Ohio State field goal miss from 45 yards out, Manning "
            "drove his offense down the length of the field and took the lead on a "
            "1-yard RB Hollywood Smothers touchdown with 25 seconds remaining.",

            "I&rsquo;ve had a lot of questions about this Texas Longhorns team "
            "under the guidance of HC Steve Sarkisian, and with Manning at the "
            "helm. But consider this win above everything else when it comes to "
            "the newly crowned #1-ranked team. Manning and Texas, at least through "
            "one week, absolutely deserve their ranking and as of today are the "
            "best, most complete team in college football.",
        ],
    ),
]
