from SmashDataClass import SD
from numpy import linalg as LA
import GraphUtils as gu
import json

with open('MI_assoc.json') as datafile:
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
    print "%s: %s" % (i, MISD.aliasList[ranking[i]])