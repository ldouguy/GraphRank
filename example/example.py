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
MISD.challonge_add_tourneys(tourneys)

# then calculate the rankings and spit out a data file and/or print the results

MISD.calc_data()
MISD.calc_AKR()
MISD.AKR.reduce()
MISD.record_AKR_ranking("example.json")
MISD.print_AKR_ranking()