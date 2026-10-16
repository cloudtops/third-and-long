# Staff picks for the primetime games, the fourth weekly update alongside
# standings.py, power.py and leaders.py. One card is rendered per game.
#
# TITLE is the headline on every card. WEEK is the small line bottom left.
# Blank either one, or empty GAMES, and no cards are made at all, so a stale
# board can never go out.
#
# Each game takes three things:
#
#   slot   the line top right, which also names the file it renders to
#   game   away team, away record, "at", home team, home record
#   picks  one person per line, "Name, Winner, Score"
#
# Winner is whichever club they took, and it sets the colour of that cell's
# bar. Score is written winner-first, exactly as it should print. Six picks
# fill the grid at three rows of two; four and eight also sit evenly. Keep the
# names in the same order across games so the cards read as a set.

TITLE = "Staff Primetime Predictions"
WEEK = "Week 6"

GAMES = [
    dict(
        slot="Thursday Night Football",
        game="Seahawks 3-2 at Broncos 3-2",
        result="Broncos 17-14",
        picks="""
        Chase Mooney, Seahawks, 21-17
        Noah Irving, Seahawks, 16-13
        Daniel Brents, Broncos, 17-13
        Noah Labao, Seahawks, 27-21
        Henry Houghton, Seahawks, 23-17
        Adam Long, Seahawks, 33-24
        """,
    ),
    dict(
        slot="Sunday Night Football",
        game="Cowboys 2-3 at Packers 3-2",
        picks="""
        Chase Mooney, Packers, 24-17
        Noah Irving, Cowboys, 27-24
        Daniel Brents, Cowboys, 30-21
        Noah Labao, Packers, 27-24
        Henry Houghton, Cowboys, 31-24
        Adam Long, Packers, 30-21
        """,
    ),
    dict(
        slot="Monday Night Football",
        game="Commanders 1-3-1 at 49ers 5-0",
        picks="""
        Chase Mooney, 49ers, 31-13
        Noah Irving, 49ers, 31-13
        Daniel Brents, 49ers, 28-10
        Noah Labao, 49ers, 35-13
        Henry Houghton, 49ers, 34-23
        Adam Long, Commanders, 31-27
        """,
    ),
]
