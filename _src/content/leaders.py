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

WEEK = "After Week 1"

LEADERS = """
Passing Yards
1. Tyler Shough, 410
2. Jordan Love, 387
3. Bryce Young, 361

Passing TDs
1. Trevor Lawrence, 4
T-2. Kirk Cousins, Jaxson Dart, Brock Purdy, Jalen Hurts, Bryce Young, Carson Wentz, Tyler Shough, 3

Rushing Yards
1. Kenneth Walker III, 173
2. Jahmyr Gibbs, 156
3. Derrick Henry, 144

Rushing TDs
T-1. Derrick Henry, D&rsquo;Andre Swift, 3

Receiving Yards
1. Chris Olave, 182
2. Zay Flowers, 150
3. Christian Watson, 147

Receiving TDs
T-1. Jalen Coker, Isaiah Likely, Justin Jefferson, Ashton Jeanty, Dallas Goedert, Amon-Ra St. Brown, Christian Watson, 2

Sacks
T-1. Za&rsquo;Darius Smith, T.J. Watt, Alex Highsmith, Kwity Paye, Greg Rousseau, Aidan Hutchinson, 2.0

Team Defense - DVOA
1. San Francisco 49ers, 70.3%
2. Jacksonville Jaguars, 66.7%
3. Baltimore Ravens, 64.9%
"""
