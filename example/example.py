from graphrank.SmashDataClass import SD
from graphrank import GraphUtils as gu
import json

# The SD class from the SmashDataClass module is the only object needed to run GraphRank
# SD stores tournament data from Challonge links and calculates a ranking
# The following example is the most likely use case:

# first, build a dictionary of associated player names, called assoc here

with open('../data/MI_assoc.json') as datafile:
    assoc = json.load(datafile)

# then initialize an empty SD and call init_from_assoc() to prepare the player data

MISD = SD()
MISD.init_from_assoc(assoc)

# then iterate through tournaments, given by challonge URL name, and add each tourney's data

tourneys = ["sweetprologue-meleesingles", "michigansmash-sweetmeleesingles17", "michigansmash-sweetmeleesingles18", "GrandPrix3Melee", "beachsmash-BB8", "beachsmash-BB9", "beachsmash-BB10"]
for tourneyID in tourneys:
	MISD.challonge_add_players(tourneyID)
MISD.challonge_init_multiGraph()
for tourneyID in tourneys:
	MISD.challonge_add_matches(tourneyID)

# call calc_AKR() to return the final rankings

ranking = MISD.calc_AKR()

# print the results and write them to a file or whatever you'd like

print "Rankings:\n--------------"
for i in range(len(ranking)):
    print "%s: %s" % (i+1, MISD.aliasList[ranking[i]])

with open('example.json', 'w') as outfile:
	json.dump([MISD.aliasList[x] for x in ranking], outfile, indent=2)