from graphrank.SmashggAPI import SmashggAPI as SAPI
from graphrank.ChallongeAPI import ChallongeAPI as CAPI
from graphrank.PlayerDataClass import PlayerData as PD
from graphrank.SmashDataClass import SmashData as SD
from graphrank.AssocBuilder import AssocBuilder as AB

tourneys = ["beachsmash-BB25", "beachsmash-summitsingles", "beachsmash-bb23", "beachsmash-bb24", "beachsmash-msswtop64", "beachsmash-bb21"]

CAPI = CAPI("graphrank", "z3eYCSivr8d1A65b2OW4lAP8XZ5cK6zaZ20Jo2ek", tourneys)
AB = AB(CAPI)
AB.save_to_json("MIrecent.json")

MIPD = PD(assoc=AB.assoc)
CAPI.add_players(MIPD)

MISD = SD(MIPD, CAPI)
MISD.init_multiGraph()
MISD.record_matches()

MISD.calc_data()
MISD.calc_AKR()

MISD.AKR.reduce()
MISD.record_AKR_ranking("exampleAB.json", tourney_cutoff=2)
MISD.print_AKR_ranking(tourney_cutoff=2)