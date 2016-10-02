from ChallongeAPI import add_players
from ChallongeAPI import add_matches
from collections import Counter
from multiprocessing.dummy import Pool
from AdjustedKatzRankClass import AKR
import GraphUtils as gu
import json

class SD:
	def __init__(self, multiGraph=None, aliasList=None, aliasSet=None, aliasDict=None, tourneyCount=None):
		self.multiGraph = multiGraph
		if not multiGraph:
			self.multiGraph = {}

		self.aliasList = aliasList
		if not aliasList:
			self.aliasList = []

		self.aliasSet = aliasSet
		if not aliasSet:
			self.aliasSet = set()

		self.aliasDict = aliasDict
		if not aliasDict:
			self.aliasDict = {}

		self.tourneyCount = tourneyCount
		if not tourneyCount:
			self.tourneyCount = Counter()

	############################

	# invoke this function on a fresh SD
	# assoc is association dict of challonge tags
	#	assoc = {non-preferred tag : preferred tag}
	# build assoc using challonge module directly
	def init_from_assoc(self, assoc):
		for player in assoc:
			self.aliasSet.add(player)
			if assoc[player] not in self.aliasSet:
				self.aliasSet.add(assoc[player])
				self.aliasList.append(assoc[player])
				self.aliasDict[assoc[player]] = len(self.aliasList)-1
			self.aliasDict[player] = self.aliasDict[assoc[player]]

	def challonge_add_players(self, tourneyID):
		add_players(tourneyID, self.aliasSet, self.aliasDict, self.aliasList, self.tourneyCount)
		print "players added for %s" % tourneyID

	def challonge_init_multiGraph(self):
		self.multiGraph = {i: Counter() for i in range(len(self.aliasList))}

	def challonge_add_matches(self, tourneyID):
		add_matches(tourneyID, self.multiGraph, self.aliasDict)
		print "matches added for %s" % tourneyID

	# run all 3 challonge functions above on a list of tourneys
	# only run this if you won't add any more tourneys afterwards
	def challonge_add_tourneys(self, tourneys):
		multipool = Pool(8)

		multipool.map(self.challonge_add_players, tourneys)
		self.challonge_init_multiGraph()
		multipool.map(self.challonge_add_matches, tourneys)

		# Note: the above is the multi-process equivalent of:

		# for tourneyID in tourneys:
		# 	self.challonge_add_players(tourneyID)
		# self.challonge_init_multiGraph()
		# for tourneyID in tourneys:
		# 	self.challonge_add_matches(tourneyID)

		# because the functions' run-times are mostly dependent on the challonge server response,
		# we save a lot of time by initiating 4 resource calls simultaneously

	############################

	# call all graphutils functions
	# much of this data is currently unused but still useful
	def calc_data(self):
		self.M = gu.MG_to_M(self.multiGraph)
		data = gu.MG_to_G(self.multiGraph)
		self.G = data[0]
		self.D = data[1]
		self.A = gu.G_to_A(self.G)
		self.partition = gu.SCC(self.G)
		self.inCycle = gu.record_cycles(self.G, self.partition)
		self.isBelow = gu.record_isBelow(self.G, self.inCycle)
		self.stronglyBelow = gu.record_stronglyBelow(self.G, self.isBelow, self.inCycle)

	############################

	def calc_AKR(self):
		self.AKR = AKR(self.multiGraph, self.A)
		self.AKR.reduce()

	############################

	def record_AKR_ranking(self, outfilename='AKR.json', tourney_cutoff=None):
		outdict = {'ranking': {}, 'data': {}, 'nowins': []}
		rank = 0
		rank_ct = 0
		tier = 0
		for arr in self.AKR.rankdata[::-1]:
			idx = rank_ct
			rank = 0
			rank_ct = 0
			for playerid, score in arr[::-1][:idx]:
				rank_ct += 1
				outdict['data'][rank_ct][1].append(round(score, 2))
				if tourney_cutoff and self.tourneyCount[playerid] < tourney_cutoff:
					continue
				rank += 1

			for playerid, score in arr[::-1][idx:]:
				rank_ct += 1
				outdict['data'][rank_ct] = (self.aliasList[playerid], [round(score, 2)])
				if tourney_cutoff and self.tourneyCount[playerid] < tourney_cutoff:
					continue				
				rank += 1
				outdict['ranking'][rank] = (self.aliasList[playerid], tier, round(score, 2))
			tier += 1
		for playerid in self.AKR.nowins:
			outdict['nowins'].append(self.aliasList[playerid])

		with open(outfilename, 'w') as outfile:
			json.dump(outdict, outfile)

	def print_AKR_ranking(self, tourney_cutoff=None, rank_cutoff=None):
		rank = 0
		rank_ct = 0
		tier = 1
		print "\nRank : Player" + " "*22 + "Tier, Score\n" + "="*46
		for arr in self.AKR.rankdata[::-1]:
			tie_ct = 0
			prev_score = None
			for playerid, score in arr[::-1][rank_ct:]:
				rank_ct += 1
				if tourney_cutoff and self.tourneyCount[playerid] < tourney_cutoff:
					continue

				if score == prev_score:
					tie_ct += 1
				else:
					rank += 1+tie_ct

				if rank_cutoff and rank > rank_cutoff:
					return
				print "%-*s : %-*s(%d, %s)" % (4, rank, 30, self.aliasList[playerid], tier, round(score, 2))
				prev_score = score
			tier += 1

		print "\n%d total players in tournament data" % len(self.aliasList)
		print "%d players omitted for no wins" % len(self.AKR.nowins)
		if tourney_cutoff:
			low_att = len(self.aliasList)-len(self.AKR.nowins)-rank_ct
			print "%d players omitted for low attendance" % low_att