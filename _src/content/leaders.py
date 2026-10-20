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

WEEK = "After Week 6"

LEADERS = """
Passing Yards
1. Matthew Stafford (LAR), 1794
2. CJ Stroud (HOU), 1714
3. Jordan Love (GB), 1684

Passing TDs
T-1. Kirk Cousins (LV), Trevor Lawrence (JAX), Brock Purdy (SF), 14
T-4. Jared Goff (DET), Tyler Shough (NO), Aaron Rodgers (PIT), 12

Rushing Yards
1. Kenneth Walker III (KC), 665
2. Bijan Robinson (ATL), 641
3. James Cook (BUF), 627

Rushing TDs
1. Josh Allen (BUF), 8
T-2. Jahmyr Gibbs (DET), Derrick Henry (BAL), Jonathan Taylor (IND), Christian McCaffrey (SF), Javonte Williams (DAL), 7

Receiving Yards
1. Jaxon Smith-Njigba (SEA), 717
2. Chris Olave (NO), 580
3. CeeDee Lamb (DAL), 577

Receiving TDs
1. Jaxon Smith-Njigba (SEA), 7
2. Christian Watson (GB), 6
T-3. Amon-Ra St. Brown (DET), Isaiah Likely (NYG), George Kittle (SF), 5

Team DVOA
1. San Francisco 49ers, 46.1%
2. Kansas City Chiefs, 28.9%
3. Jacksonville Jaguars, 27.7%

Sacks
1. Will Anderson Jr. (HOU), 7.5
2. Greg Rousseau (BUF), 6.0
3. Dallas Turner (MIN), 5.5
"""
