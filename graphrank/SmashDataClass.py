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

	def challonge_add_players(self, tourneyID):
		add_players(tourneyID, self.aliasSet, self.aliasDict, self.aliasList, self.tourneyCount)
		print "players added for %s" % tourneyID

	def challonge_init_multiGraph(self):
		self.multiGraph = {i: Counter() for i in range(len(self.aliasList))}

	def challonge_add_matches(self, tourneyID):
		add_matches(tourneyID, self.multiGraph, self.aliasDict)
		print "matches added for %s" % tourneyID

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

	# To do:
	# if tourneyCount[playerid] < threshold, do not include in rankings
	# list same rank for tied scores (finish rank_ct/curr_score code)
	# figure out why 2nd tier in AKR is broken

	def record_AKR_ranking(self, outfilename='AKR.json', threshold=None):
		outdict = {'ranking': {}, 'data': {}}
		rank = 0
		# rank_ct = 0
		# curr_score = [0, 0]
		tier = 0
		for arr in self.AKR.rankdata[::-1]:
			idx = rank
			rank = 0
			for playerid, score in arr[::-1][:idx]:
				rank += 1
				outdict['data'][rank][1].append(round(score, 2))

			for playerid, score in arr[::-1][idx:]:
				rank += 1
				outdict['ranking'][rank] = (self.aliasList[playerid], tier, round(score, 2))

				outdict['data'][rank] = (self.aliasList[playerid], [round(score, 2)])
			tier += 1

		with open(outfilename, 'w') as outfile:
			json.dump(outdict, outfile, indent=2)

	def print_AKR_ranking(self, threshold=None, cutoff=None):
		rank = 0
		# rank_ct = 0
		# curr_score = [0,0]
		tier = 1
		print "\nRank : Player" + " "*22 + "Tier, Score\n" + "="*46
		for arr in self.AKR.rankdata[::-1]:
			for playerid, score in arr[::-1][rank:]:
				rank += 1
				if cutoff and rank > cutoff:
					return
				print "%-*s : %-*s(%d, %s)" % (4, rank, 30, self.aliasList[playerid], tier, round(score, 2))
			tier += 1