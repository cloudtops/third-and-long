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
        slug="week-2-chiefs-colts",
        kind="Game of the Week",
        title="Kansas City 33, Indianapolis 30",
        author="Adam Long",
        date="Week 2",
        teams=("chiefs", "colts"),
        body=[
            "So, in the preseason, I wrote about how the NFL&rsquo;s latest "
            "dynastic reign had finally come to an end, and parity had finally "
            "returned to the game&rsquo;s biggest stage without the looming "
            "specter of doom that is Patrick Mahomes II and Andy Reid. Fast "
            "forward two weeks and this take is aging like milk. Sunday "
            "night&rsquo;s bout between the Colts and the Chiefs had all the "
            "classic hallmarks of an early 2020s Kansas City Devil Magic Bowl. "
            "After an early strike from QB Daniel Jones to second-year man TE "
            "Tyler Warren put Indy up a score, Mahomes and Co. answered back with "
            "a field goal and a touchdown to the ageless wonder TE Travis "
            "Swift-Kelce. The Colts responded with two field goals of their own "
            "before Mahomes again drove down the field and hit WR Xavier Worthy "
            "in the end zone to take the lead. Lead changes abounded in this "
            "contest, lending to the exciting nature of this primetime matchup, "
            "and All-Pro RB Jonathan Taylor scampered in on a 24-yard touchdown "
            "rush to put the Colts ahead just before the half. Kansas City tacked "
            "on a field goal and a score (to WR Jalen Royals) in the second half, "
            "which was matched by Taylor&rsquo;s second touchdown run of the game "
            "with five minutes remaining to even the score in regulation.",

            "Overtime starts, our first primetime matchup of the season to go to "
            "extra innings. Kansas City opened the period with a ho-hum field goal "
            "drive. Indy got the ball back, and QB Daniel Jones hit WR Laquon "
            "Treadwell on a deep bomb that the beleaguered wideout promptly "
            "fumbled. Wait, let&rsquo;s see that one again. Oh, he got touched by "
            "Chiefs&rsquo; DB L&rsquo;Jarius Sneed before getting up? Nice! The "
            "Colts were now in the red area, and after getting stopped behind the "
            "sticks by the Kansas City defense, they elected to kick a field goal. "
            "I think most Indianapolis fans would tell you, and most NFL fans in "
            "general, that if you give the football back to Mahomes in Arrowhead "
            "with only a field goal needed for the win and three minutes on the "
            "clock that the game is essentially already over. Colts&rsquo; HC "
            "Shane Steichen has to go for the score there. The Chiefs got the win "
            "at home on a Harrison Butker 40-yard field goal as time expired, "
            "because of course they did. P.S. Patrick Mahomes now holds the NFL "
            "record for regular season overtime winning streak with an 8-0 mark. "
            "This shit isn&rsquo;t ever going to end, is it.",
        ],
    ),
    dict(
        slug="rookie-radar-antonio-williams",
        kind="Rookie Radar",
        title="Antonio Williams, WR, Washington Commanders",
        author="Noah Labao",
        date="Week 1",
        team="commanders",
        body=[
            "Attentive eyes during the Commanders opener in Philly may have "
            "locked in on a wideout who may be on track to become one of "
            "5&rsquo;s go-to targets. In a role that Brandon Aiyuk was so sure he "
            "was going to get in the offseason, the third-round rookie caught all "
            "four of his targets for 64 yards and a touchdown, which was good "
            "enough to earn props with PFF. They graded him as the highest-graded "
            "rookie in all of football for Week 1 at 91.2, with 5.82 yards per "
            "route run. Among receivers with double-digit snaps, only Zay Flowers "
            "beat that number.",

            "## College Bio: Clemson Tigers (2022 to 2025)",

            "Williams was a four-year contributor at Clemson and left as a "
            "two-time All-ACC pick (first team in 2024, third team in 2025). He "
            "showed up ready to roll, leading the Tigers as a true freshman in "
            "2022 with 56 catches for 604 yards and four scores while earning "
            "Freshman All-America honors. He finished his college run with 208 "
            "catches, 2,336 receiving yards, and 21 touchdowns across 42 games, "
            "with his 2024 season (75 catches, 904 yards, 11 TDs) as the clear "
            "high point. Best part for a wideout: he barely put the ball on the "
            "ground, reportedly dropping under 2 percent of his targets in his "
            "final Clemson season.",

            "His year-by-year college line: 56 catches, 604 yards, and 4 TDs in "
            "2022; 22 catches, 224 yards, and 2 TDs in an injury-shortened 2023; "
            "a monster 75 catches, 904 yards, and 11 TDs in 2024; and 55 catches, "
            "604 yards, and 4 TDs in 2025.",

            "## High School Recruiting Profile: Dutch Fork HS (Irmo, SC)",

            "Williams was a stud, winning three state titles and losing just one "
            "game across his high-school career while piling up 137 catches for "
            "2,458 yards and 23 touchdowns. The consensus four-star and top-100 "
            "national prospect was a heavily recruited target, at one point "
            "ranking Georgia, Auburn, Florida State, Notre Dame, Ole Miss, and "
            "South Carolina in his top six. South Carolina was long viewed as the "
            "favorite until Clemson swept in with a late offer and landed his "
            "commitment.",

            "On the athletic side, he backed up the tape at his pre-draft workouts "
            "with a 4.41 forty, a 39.5-inch vertical, and a 10-foot-4 broad jump, "
            "all at 5-foot-11 and a half, 187 pounds, with a 6-foot-4 wingspan.",

            "## Scheme Fit: Why He Works in Washington",

            "Washington&rsquo;s offense runs on Jayden Daniels&rsquo; quick-game "
            "rhythm and a ton of motion, and that setup rewards receivers who can "
            "separate early and finish clean. That&rsquo;s Williams in a nutshell. "
            "Just look at how they used him in the opener: a 16-yard grab that set "
            "up the offense&rsquo;s first touchdown of the year, and a 33-yard "
            "pickup on third-and-14 where he simply ran away from the "
            "Eagles&rsquo; secondary. With Terry McLaurin pulling coverage and "
            "gadget looks flying around the formation, Williams fits as the "
            "efficient underneath-to-intermediate separator who makes defenses pay "
            "for single coverage on the back side. His target quality is already "
            "highly productive on one of the more impressive rookie WR debuts in "
            "recent history.",

            "## Similarity Comp: Darnell Mooney",

            "Picture Darnell Mooney: a compact, sub-4.45 separator who wins with "
            "clean routes and real vertical juice instead of size. Like Mooney, "
            "Williams isn&rsquo;t the biggest guy in the huddle, but he stacks "
            "defenders, tracks the deep ball, and gives his quarterback that "
            "reliable &ldquo;just find a way to get open&rdquo; option when it "
            "matters. If Washington keeps feeding him the way the arrow is "
            "pointing, the Mooney comp might end up underselling how high this "
            "ceiling really is.",

            "## On The Radar",

            "A few more rookies worth keeping an eye on in the coming weeks:",

            [
                "Caleb Douglas, WR, Miami Dolphins - 5 catches on 7 targets for "
                "94 yards (a franchise record for receiving yards in a Dolphins "
                "debut).",

                "Josiah Trotter, LB, Tampa Bay Buccaneers - 10 tackles (2 for "
                "loss), 1 sack, and a 38-yard pick-six (the first player in NFL "
                "history with a pick-six and a sack in his debut).",

                "Kaelon Black, RB, San Francisco 49ers - 65 yards on 14 carries, "
                "emerged as Christian McCaffrey&rsquo;s primary backup, chipping "
                "in on the ground in the Niners&rsquo; win.",
            ],
        ],
    ),
    dict(
        slug="nirv-column-mascots",
        kind="Guest Column",
        title="The Nirv Column",
        author="Noah Irving",
        date="2026 Week 1",
        noindex=True,   # the piece ends with a real phone number
        body=[
            "Well well well, who do we have here! Some poor soul that stumbled "
            "upon the Nirv Column (title is a work in progress). It is both an "
            "honor and a privilege to be able to drive my words to you all, in "
            "the vehicle that is 3rd &amp; Long (title not a work in progress, it "
            "slaps). Without further ado, let&rsquo;s get into the fun stuff.",

            "If you&rsquo;re looking for my Super Mario World walkthrough, "
            "you&rsquo;ll wanna go <a href=\"/posts/nirv-super-mario-world\">here</a>.",

            "And if you&rsquo;re looking for my Washington State Cougar Football "
            "recap, you&rsquo;ll wanna go "
            "<a href=\"/posts/nirv-wsu-cougar-football\">here</a>.",

            "Now that that&rsquo;s out of the way&hellip;.",

            "Football. More than a word, more than a noun, more than a game. It "
            "means something to me, to you, to everyone. It means scouring the "
            "waiver wires for some 3rd string RB that you pray gets a chance to "
            "see the field. It means firing up the crockpot for a fresh batch of "
            "chili on a blustery, gloomy November Sunday. And if you&rsquo;re that "
            "one K-State fan, it means shoving a beefy 5-layer burrito up your "
            "south mouth because you lost to BYU.",

            "Football is fun. Football is exciting. Football is the church that I "
            "pray to every Monday, Thursday, and Sunday (and the occasional "
            "Wednesday, Saturday, I think a Tuesday during COVID). Football is life.",

            "And today, we&rsquo;ll be shedding some light on another aspect of "
            "this beautiful game: mascots.",

            "According to our lovely AI overlords, mascots are &lsquo;to serve as "
            "a living symbol of a team&rsquo;s identity while entertaining crowds "
            "and connecting the franchise to its local community.&rsquo;",

            "Booooooooorrrrrriiiiinnnnnggggg.",

            "If I wanted a symbol of team identity that connects the franchise to "
            "its community, I&rsquo;d start at Magic City (shoutout Lou Will Lemon "
            "Pepper) and skip the dumb red bird. But nuh uh, not with the likes of "
            "Sir Purr, Jaxson de Ville, hell even that big Blue thing in Indy that "
            "just hip thrusts. Mascots are more than just buzzwords to make the "
            "fans feel more connected. They are the cornerstone of the very game "
            "we love and root for.",

            "Steely McBeam, Viktor the Viking, even T.D. the weird Dolphins mascot "
            "(literally stands for The Dolphin. So dumb but I absolutely love it). "
            "These are the true heroes we see on our TVs, week in and week out. "
            "Doing it purely for the love of the game; not for money or publicity. "
            "Simply because the feel of that foam head restricting your breathing, "
            "it means something to them. And in turn, means something to me.",

            "And the saddest part: not even all NFL teams adopt these beautiful "
            "creatures. We have a staggering 4!!!!! teams that have nothing to "
            "represent them: the Chargers, Packers, Giants and Jets.",

            "Giant Jets?! Never mind&hellip;",

            "Anyways, crazy that these teams think they can skate away without "
            "something &lsquo;to serve as a living symbol of a team&rsquo;s "
            "identity while entertaining crowds and connecting the franchise to "
            "its local community.&rsquo; So with my time today, I&rsquo;d like to "
            "propose options for these four sorry franchises.",

            "<strong>The Chargers</strong>",

            "Boltman. How in the hell could you ever get rid of Boltman. Half "
            "bolt, half&hellip;.man. ALL PLEASURE. Partied hard but loved harder. "
            "And sadly, I don&rsquo;t think taking him out of retirement would be "
            "the correct answer. All good things come to an end; Boltman&rsquo;s "
            "was objectively too soon, but we can&rsquo;t dwell. That&rsquo;s why "
            "I&rsquo;d love to introduce: BoltWOman.",

            "I know, I know- in this economy?! And to that I say: yeah. Madison "
            "Beer as BoltWOman. Don&rsquo;t like it? Very fair. Find your own "
            "friends and write your own column. But I mean, c&rsquo;mon. "
            "We&rsquo;ve had our share of the Sweeney&rsquo;s and "
            "Carpenter&rsquo;s of the world, so it&rsquo;s about damn time we get "
            "some shine on Ms Beer. And what better way to do that, than turning "
            "her into a living lightning bolt with boo&hellip;.with a huge "
            "personality. Just the juice Joe Alt needs to chip and protect. We "
            "salute you, Ms Beer!",

            "<strong>The Packers</strong>",

            "Idk just give them like a big wheel of cheese or something. Call him "
            "Cheeseman Professor Cheese. Make him stinky. Other cheese-like "
            "attributes. Idk.",

            "In all seriousness, I did a little digging into Green Bay, WI. Did "
            "you know it is the oldest city in Wisconsin? Long short, back in the "
            "day it was a trade route for the French. Oui oui! Eventually the "
            "British came along, blah blah blah history stuff, and here we are "
            "today: where the drunken, cheese-curd-loving Wisconsinites (?) have "
            "sunk their teeth into the beautiful city known as Titletown.",

            "Old, French, cheese&hellip;. There&rsquo;s a joke in there somewhere. "
            "But my proposal, for the mascot of the Green Bay Packers, would be "
            "the Curd Crew. A bunch of short guys and gals, dressed as cheese "
            "curds, rocking berets and turning a blind eye to any off-field RB "
            "scandals (or on field terrible QB play). Either that, or just make "
            "Favre the face of the team. He&rsquo;s been a model citizen off the "
            "field and deeply cares about the welfare of the city. Or was that "
            "the one in Mississippi&hellip;",

            "<strong>The Giants</strong>",

            "The New York&hellip;.Football&hellip;GIANTS!!!! I mean, just a damn "
            "shame this team doesn&rsquo;t have a mascot to represent them. An odd "
            "franchise, filled with ups and downs. Eli Manning will forever be a "
            "legend, as will Plaxico Burress in his own right. OBJ, the infamous "
            "boat pic, it is a team that has seen the highest of highs and the "
            "lowest of lows. And don&rsquo;t get me wrong, they are in a great "
            "spot now! Young core, new but established head coach, and Cam Skat. "
            "Just a DOG. A face meant for radio but a game meant for television. "
            "I&rsquo;m high on the Giants this year (and that&rsquo;ll be the only "
            "football analysis you&rsquo;ll get from me).",

            "And it&rsquo;s NY! So many iconic things tied into that city. But "
            "when they zig, you gotta zag. My idea for the NY Football Giants "
            "mascot?",

            "Kelsey Plum.",

            "I mean, why not? To my (limited) knowledge, there has never been a "
            "living PERSON to represent a franchise as a mascot. And I can&rsquo;t "
            "think of a better person for the job than KP (5x All-Star, 2x "
            "Champion, 15.5pts / 2.5rbs / 4.3ast career split). She doesn&rsquo;t "
            "even have to wear blue, red, or anything Giants related. Just trot "
            "her out to the field for every game, and let ol Kels do the rest.",

            "For those counting at home, that is now TWO (2) female mascots. "
            "Champion of the people over here.",

            "<strong>The Jets</strong>",

            "Oh man. I have many thoughts. Many jokes. A second joke just hit, "
            "actually.",

            "I&rsquo;m gonna be honest, just give them an Airbus A380. Like a "
            "real, decommissioned (I don&rsquo;t think they fly them anymore), "
            "full on Airbus. Have it just hover over the field during the entire "
            "game. I&rsquo;m sure they could sell tickets for those seats. Lands "
            "for halftime, does the Dr. Pepper Tuition giveaway (cross platform, "
            "multi dimensional), then back up to hover she goes. Have some TSA "
            "agents making people take off their shoes in the stands. I want it "
            "all. But it starts with an Airbus. And ends with Geno hoisting the "
            "Lombardi.",

            "And there ya have it, the 2026 NFL Week 1 Recap as told by yours "
            "truly! We&rsquo;ll be responding to voicemails for our next column, "
            "so feel free to give us a call at (360) 340-1858. And really let us "
            "hear it!!",
        ],
    ),
    dict(
        slug="nirv-super-mario-world",
        unlisted=True,   # linked from the column, kept off the index
        kind="Guest Column",
        title="The Complete Guide to Super Mario World (SNES)",
        author="Noah Irving",
        date="Week 1",
        body=[
            "Alright you cool cats and kittens, welcome to your all-in-one Super "
            "Mario World walkthrough. Not to milk my own cow here, but I&rsquo;ve "
            "put in ungodly amounts of time into this game, so I&rsquo;d like to "
            "think I have some knowledge that I can share with the masses.",

            "TO START: tackle Yoshi&rsquo;s Island 1, and make your way up to the "
            "Yellow Switch Palace. This will just fill in some gaps of missing "
            "blocks you&rsquo;ll inevitably encounter on your journey to taking "
            "down Bowser.",

            "After that, continue through the game path as normal, and take down "
            "that first castle (shoutout Iggy). Keep it pushin until you get to "
            "Donut Plains 2. You&rsquo;ll see in the Donut Plains area, a lot of "
            "the levels are a red dot instead of yellow. This means there are "
            "actually 2 ways to beat the level; one that will progress you as "
            "normal, and another that will lead you to some sort of secret area. "
            "Donut Plains 2 will be the first secret area you really want to "
            "unlock; the Green Switch Palace. Same as the yellow, but if you "
            "encounter one in your journey, it&rsquo;ll give you a feather. Woo!",

            "IMMEDIATELY AFTER DONUT PLAINS 2, the Donut Ghost House. Arguably the "
            "most important level in the entire game. This one also has a secret "
            "way to beat the level. You&rsquo;ll need a cape; just fly up and to "
            "the left when you first start the level. Walk along the platform at "
            "the top of the screen, go through the ticker tape&hellip;.and "
            "you&rsquo;ve just unlocked the Top Secret Area. Free mushies, fire "
            "flowers, feathers, and Yoshi&rsquo;s. As much. As. You. Want.",

            "Alright&hellip;.now that that&rsquo;s done with, keep moving forward "
            "through the game. You&rsquo;ll eventually get inside the cave to "
            "Vanilla Dome 1. Beat it normal, then on Vanilla Dome 2, you&rsquo;ll "
            "want the secret beat to unlock the Red Switch Palace. Keep going "
            "through (the normal beat) of Vanilla Dome 2, all the way through "
            "castle #3. Go through Cheese Bridge and Cookie Mountain, slay the "
            "beast that is Ludwig in castle #4, and make your way "
            "to&hellip;..the Forest of Illusion&hellip;.",

            "Not gonna lie, y&rsquo;all are on your own in the forest. Just like "
            "how I had to suffer my way through it, you get to too. Just "
            "don&rsquo;t forget to grab the Blue Switch Palace ;)",

            "Now that you&rsquo;ve made it through, your reward is Chocolate "
            "Island. One of the better islands, especially considering the "
            "geopolitical climate&hellip;but it is not without its checkered past. "
            "Make your way through and conquer Wendy, and now the fun begins. The "
            "Valley of Bowser&hellip;",

            "We&rsquo;ll leave it at that for this week. Maybe next time I&rsquo;ll "
            "give you the rest of the walkthrough, maybe it&rsquo;ll be a different "
            "game. Maybe I won&rsquo;t be invited back as a guest writer. Life is a "
            "beautiful thing&hellip;.",
        ],
    ),
    dict(
        slug="nirv-wsu-cougar-football",
        unlisted=True,   # linked from the column, kept off the index
        kind="Guest Column",
        title="The Complete Guide to WSU Cougar Football",
        author="Noah Irving",
        date="Week 1",
        image=("nirv-wsu.png", "Kevin from The Office, captioned: IT'S BAD"),
        body=[],
    ),
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
