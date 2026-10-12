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

WEEK = "After Week 4"

LEADERS = """
Passing Yards
1. Bryce Young, 1268
2. Jared Goff, 1214
3. Matthew Stafford, 1189

Passing TDs
T-1. Kirk Cousins, Brock Purdy, 11
T-3. Patrick Mahomes, Jared Goff, Bryce Young, 9

Rushing Yards
1. Kenneth Walker III, 537
2. James Cook, 421
3. Derrick Henry, 374

Rushing TDs
T-1. Josh Allen, Derrick Henry, 7
3. Jonathan Taylor, 6

Receiving Yards
1. CeeDee Lamb, 498
2. Jaxon Smith-Njigba, 481
3. Tee Higgins, 401

Receiving TDs
1. Jaxon Smith-Njigba, 6
2. Amon-Ra St. Brown, 5
T-3. George Kittle, CeeDee Lamb, Christian Watson, 4

Team Defense - DVOA
1. San Francisco 49ers, 54.8%
2. Jacksonville Jaguars, 40.2%
3. Kansas City Chiefs, 25.9%

Sacks
1. Greg Rousseau, 6.0
2. Dallas Turner, 5.5
T-3. Will Anderson Jr., T.J. Watt, 4.5
"""
