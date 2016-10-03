from graphrank.SmashDataClass import SD
from graphrank import GraphUtils as gu
import json

# The SD class from the SmashDataClass module is the only object needed to run GraphRank
# SD stores tournament data from Challonge links and calculates a ranking
# The following example is the most likely use case:

# first, build a dictionary of associated player names, called assoc here
# this will most likely be done manually, and by no means needs be exhaustive
# it is mostly important to associate players you expect to be highly ranked

with open('../data/MI_assoc.json') as datafile:
    assoc = json.load(datafile)

# then initialize an empty SD and call init_from_assoc() to prepare the player data

MISD = SD()
MISD.init_from_assoc(assoc)

# supply your Challonge API credentials to the SD object
# Note: please use your own Challonge account, the credentials below are for demonstration only

MISD.challonge_credentials("graphrank", "z3eYCSivr8d1A65b2OW4lAP8XZ5cK6zaZ20Jo2ek")

# then iterate through tournaments, given by challonge URL name, and add each tourney's data

tourneys = ["sweetprologue-meleesingles", "michigansmash-sweetmeleesingles17", "michigansmash-sweetmeleesingles18", "GrandPrix3Melee", "beachsmash-BB8", "beachsmash-BB9", "beachsmash-BB10"]
MISD.challonge_add_tourneys(tourneys)

# then calculate the necessary data and feed it into a ranking object

MISD.calc_data()
MISD.calc_AKR()

# and finally run the rankings and spit out a data file and/or print the result

MISD.AKR.reduce()
MISD.record_AKR_ranking("example.json", tourney_cutoff=2)
MISD.print_AKR_ranking(tourney_cutoff=2)