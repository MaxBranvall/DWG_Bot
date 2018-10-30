# Deals with Gold Bot
This is a bot that automatically converts MajorNelson's xbox sales into markdown tables. It also replaces the discount percentage with the discount price that links to the microsoft page for that game/add-on. These tables are then posted to /r/XboxOne for the convenience of the community.

Future versions will include info from sites such as TrueAchievements, MetaCritic, and HowLongToBeat integrated into the tables for each game.

# Known Bugs
* Games/add-ons with no href display the discount percentage and do not link to anything.

# Patched
* Bug01- Xbox360 prices were assigned to wrong games because the bot skipped a game when parsing the major nelson table.

* Bug02- When games are included in game pass the price shows as 'included'.

* Bug03- When an xbox 360 game has the same title as an xbox one game the 360 game will be skipped. Games with no href are not added to list.
