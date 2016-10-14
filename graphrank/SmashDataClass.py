from ChallongeAPI import ChallongeAPI as CAPI
from SmashggAPI import SmashggAPI as SAPI
from collections import Counter
from PlayerDataClass import PlayerData as PD
from AdjustedKatzRankClass import AKR
import GraphUtils as gu
import json

class SmashData:
	def __init__(self, PD, CAPI=None, SAPI=None):
		self.PD = PD
		self.CAPI = CAPI
		self.SAPI = SAPI

	############################

	def init_multiGraph(self):
		self.multiGraph = {i: Counter() for i in range(len(self.PD.aliasList))}

	def record_matches(self):
		flag = False
		if self.CAPI:
			self.CAPI.add_matches(self.PD, self.multiGraph)
			flag = True
		if self.SAPI:
			self.SAPI.add_matches(self.PD, self.multiGraph)
			flag = True

		if not flag:
			print "There is no API object to add data from."

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
				if tourney_cutoff and self.PD.tourneyCount[playerid] < tourney_cutoff:
					continue
				rank += 1

			for playerid, score in arr[::-1][idx:]:
				rank_ct += 1
				outdict['data'][rank_ct] = (self.PD.aliasList[playerid], [round(score, 2)])
				if tourney_cutoff and self.PD.tourneyCount[playerid] < tourney_cutoff:
					continue				
				rank += 1
				outdict['ranking'][rank] = (self.PD.aliasList[playerid], tier, round(score, 2))
			tier += 1
		for playerid in self.AKR.nowins:
			outdict['nowins'].append(self.PD.aliasList[playerid])

		with open(outfilename, 'w') as outfile:
			json.dump(outdict, outfile)

	def print_AKR_ranking(self, tourney_cutoff=None, rank_cutoff=None):
		rank = 0
		rank_ct = 0
		tier = 1
		final_tie = 0
		print "\nRank : Player" + " "*22 + "Tier, Score\n" + "="*46
		for arr in self.AKR.rankdata[::-1]:
			tie_ct = 0
			prev_score = None
			for playerid, score in arr[::-1][rank_ct:]:
				rank_ct += 1
				if tourney_cutoff and self.PD.tourneyCount[playerid] < tourney_cutoff:
					continue

				if score == prev_score:
					tie_ct += 1
				else:
					rank += 1+tie_ct
					tie_ct = 0

				if rank_cutoff and rank > rank_cutoff:
					return
				print "%-*s : %-*s(%d, %s)" % (4, rank, 30, self.PD.aliasList[playerid], tier, round(score, 2))
				prev_score = score
			tier += 1
			final_tie = tie_ct

		print "\n%d total players in tournament data" % len(self.PD.aliasList)
		print "%d players omitted for no wins" % len(self.AKR.nowins)
		if tourney_cutoff:
			low_att = len(self.PD.aliasList)-len(self.AKR.nowins)-rank-final_tie
			print "%d players omitted for low attendance" % low_att