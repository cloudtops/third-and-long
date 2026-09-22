# Stat leaders — the second weekly update, alongside standings.py and power.py.
#
# WEEK is the dateline. Blank = the whole section is hidden, so the site never
# shows stale leaders.
#
# LEADERS: blocks separated by a blank line. The first line of a block is the
# category heading — you pick the categories, they aren't fixed. Every line
# after it is a leader:
#
#     Player, Team, Value
#     Player, Value
#
# Team is optional and colors the row. It can be a nickname or the full club
# name. If the whole row IS a club — "San Francisco 49ers, 70.3%" — it gets that
# club's color too, no second name needed.
#
# Rank is optional. Start a line with "1." or "T-1." and it prints exactly that;
# leave it off and the build numbers down the list for you:
#
#     Passing Yards
#     1. Sam Darnold, Seahawks, 253
#     2. Drake Maye, Patriots, 241
#
# Ties: list the names on one line, separated by commas, with the value last.
#
#     T-1. Derrick Henry, D&rsquo;Andre Swift, 3
#
# Order is preserved exactly as you type it — nothing gets re-sorted, so "4.5",
# "1,204" and "12 (T-1st)" all work as values. List as many or as few per
# category as you like. A misspelled team stops the build and names it.

WEEK = "After Week 2"

LEADERS = """
Passing Yards
1. Tyler Shough, 662
2. Bryce Young, 648
3. CJ Stroud, 627

Passing TDs
T-1. Kirk Cousins, Jared Goff, Bryce Young, Dak Prescott, 6

Rushing Yards
1. Kenneth Walker III, 290
2. Derrick Henry, 212
3. Jahmyr Gibbs, 208

Rushing TDs
T-1. Josh Allen, Derrick Henry, Jonathan Taylor, 4

Receiving Yards
1. Jaxon Smith-Njigba, 277
2. Chris Olave, 268
3. Dalton Kincaid, 225

Receiving TDs
T-1. Jaxon Smith-Njigba, Amon-Ra St. Brown, 4
T-3. Stefon Diggs, CeeDee Lamb, Christian Watson, 3

Sacks
1. Greg Rousseau, 4.0
2. T.J. Watt, 3.5
T-3. Alex Highsmith, Aidan Hutchinson, Dallas Turner, 3.0

Team Defense - DVOA
1. San Francisco 49ers, 78.0%
2. Buffalo Bills, 52.7%
3. Baltimore Ravens, 38.3%
"""
