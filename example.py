from graphrank.SmashggAPI import SmashggAPI as SAPI
from graphrank.ChallongeAPI import ChallongeAPI as CAPI
from graphrank.PlayerDataClass import PlayerData as PD

from graphrank.SmashDataClass import SmashData as SD

import json

tourneys = ["sweetprologue-meleesingles", "michigansmash-sweetmeleesingles17", "michigansmash-sweetmeleesingles18", "GrandPrix3Melee", "beachsmash-BB8", "beachsmash-BB9", "beachsmash-BB10"]

CAPI = CAPI("graphrank", "z3eYCSivr8d1A65b2OW4lAP8XZ5cK6zaZ20Jo2ek", tourneys)

with open('data/assocs/MI_assoc.json') as datafile:
    assoc = json.load(datafile)

MIPD = PD(assoc=assoc)
CAPI.add_players(MIPD)

MISD = SD(MIPD, CAPI)
MISD.init_multiGraph()
MISD.record_matches()

MISD.calc_data()
MISD.calc_AKR()

MISD.AKR.reduce()
# MISD.record_AKR_ranking("example.json", tourney_cutoff=2)
MISD.print_AKR_ranking(tourney_cutoff=2)