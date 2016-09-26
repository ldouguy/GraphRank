from graphrank.SmashDataClass import SD
from graphrank import GraphUtils as gu
import json

with open('../data/MI_assoc.json') as datafile:
    assoc = json.load(datafile)

MISD = SD()
MISD.init_from_assoc(assoc)
tourneys = ["sweetprologue-meleesingles", "michigansmash-sweetmeleesingles17", "michigansmash-sweetmeleesingles18", "GrandPrix3Melee", "beachsmash-BB8", "beachsmash-BB9", "beachsmash-BB10"]

for tourneyID in tourneys:
	MISD.challonge_add_players(tourneyID)
MISD.challonge_init_multiGraph()
for tourneyID in tourneys:
	MISD.challonge_add_matches(tourneyID)

ranking = MISD.calc_AKR()

print "Rankings:\n--------------"
for i in range(len(ranking)):
    print "%s: %s" % (i+1, MISD.aliasList[ranking[i]])

with open('example.json', 'w') as outfile:
	json.dump([MISD.aliasList[x] for x in ranking], outfile)