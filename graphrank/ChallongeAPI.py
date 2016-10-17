import challonge
import json
import os
from collections import Counter
from multiprocessing.dummy import Pool
from pprint import pprint


class ChallongeAPI:
	def __init__(self, user, secretKey, tourneys):
		self.user = user
		self.secretKey = secretKey

		challonge.set_credentials(self.user, self. secretKey)

		self.playerDict = {}
		self.ctourneyCount = Counter()
		self.matchData = {}

		multipool = Pool(8)
		multipool.map(self._get_players, tourneys)
		multipool.map(self._get_matches, tourneys)

	def _get_players(self, tourneyID):
		playerDict = {}
		if os.path.isfile("data/challonge/players/" + tourneyID + "playerdata.json"):
			with open("data/challonge/players/" + tourneyID + "playerdata.json") as playerData:
				playerDict = json.load(playerData)
		else:
			players = challonge.participants.index(tourneyID)
			for player in players:
				playerDict[player['id']] = player['name']
			with open("data/challonge/players/" + tourneyID + "playerdata.json", "w") as outfile:
				json.dump(playerDict, outfile, indent=2)

		for pid in playerDict:
			self.playerDict[int(pid)] = playerDict[pid]
			self.ctourneyCount[int(pid)] += 1

	def _get_matches(self, tourneyID):
		matchData = {}
		if os.path.isfile("data/challonge/matches" + tourneyID + "matchdata.json"):
			with open("data/challonge/matches/" + tourneyID + "matchdata.json") as matchesData:
				matchData = json.load(matchesData)
		else:
			matches = challonge.matches.index(tourneyID)
			for match in matches:
				if match['winner-id'] not in matchData:
					matchData[match['winner-id']] = Counter()
				matchData[match['winner-id']][match['loser-id']] += 1

			with open("data/challonge/matches/" + tourneyID + "matchdata.json", "w") as outfile:
				json.dump(matchData, outfile, indent=2)

		for wid in matchData:
			if wid not in self.matchData:
				self.matchData[wid] = Counter()
			for lid in matchData[wid]:
				self.matchData[wid][lid] += matchData[wid][lid]

	####################################################

	def add_players(self, PD):
		for nid in self.playerDict:
			name = self.playerDict[nid]
			if name not in PD.aliasSet:
				PD.aliasSet.add(name)
				PD.aliasList.append(name)
				PD.idDict[name] = len(PD.aliasList)-1

			# this assumes that challonge player id is greater than #(players)
			# probably safe assumption, should probably formalize check later
			# use an assert and raise an error otherwise
			PD.idDict[nid] = PD.idDict[name]
			PD.tourneyCount[PD.idDict[nid]] += self.ctourneyCount[nid]

	def add_matches(self, PD, multiGraph):					
		for winnerid in self.matchData:
			for loserid in self.matchData[winnerid]:
				multiGraph[PD.idDict[winnerid]][PD.idDict[loserid]] += self.matchData[winnerid][loserid]