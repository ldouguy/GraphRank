from ChallongeAPI import add_players
from ChallongeAPI import add_matches
from collections import defaultdict
from GraphReduceClass import GR
import GraphUtils as GU

class SD:
	def __init__(self, multiGraph=None, aliasList=None, aliasSet=None, aliasDict=None):
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

	############################

	def challonge_add_players(self, tourneyID):
		add_players(tourneyID, self.aliasSet, self.aliasDict, self.aliasList)

	def challonge_init_multiGraph(self):
		self.multiGraph = {i: defaultdict(int) for i in range(len(self.aliasList))}

	def challonge_add_matches(self, tourneyID):
		add_matches(tourneyID, self.multiGraph, self.aliasDict)

	# invoke this function on a fresh SD
	# assoc is association dict of challonge tags
	#	assoc = {non-preferred tag : preferred tag}
	# build assoc using challonge module directly
	
	def init_from_assoc(assoc):
		for player in assoc:
			self.aliasSet.add(player)
			if assoc[player] not in self.aliasSet:
				self.aliasSet.add(assoc[player])
				self.aliasList.append(assoc[player])
				self.aliasDict[assoc[player]] = len(self.aliasList)-1
			self.aliasDict[player] = self.aliasDict[assoc[player]]

	############################

	def calc_setCounts(self):
		self.setCounts = GU.MG_to_M(self.multiGraph)
		return self.setCounts

	def calc_GR(self):
		arr = GU.MG_to_G(self.multiGraph)
		part = GU.SCC(arr[0])
		inCycle = GU.record_cycles(arr[0], part)
		self.GR = GR(arr[0], arr[1], inCycle, GU.record_above(arr[0], inCycle))

		return self.GR

	def print_GR(self):
		for v in self.GR.top:
			print "%d : %s" % (v, self.aliasList[v])
			print self.GR.records[v]