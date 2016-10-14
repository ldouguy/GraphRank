from urllib2 import Request, urlopen, URLError
from urllib import quote_plus
from collections import Counter
from multiprocessing.dummy import Pool
import json

class SmashggAPI:
	def __init__(self, tourneys):
		self.phaseGroups = []
		self.playerDict = {}
		self.entrantDict = {}
		self.stourneyCount = Counter()
		self.matchData = {}

		multipool = Pool(8)
		multipool.map(self._get_phaseGroups, tourneys)

		self._curr_pids = set()
		for groups in self.phaseGroups:
			multipool.map(self._get_players, groups)
			for pid in self._curr_pids:
				self.stourneyCount[pid] += 1
			self._curr_pids = set()
			multipool.map(self._get_matches, groups)
		
	def _readURL(self, URL):
		request = Request(URL)
		try:
			response = urlopen(request)
			rawdata = response.read()
			return json.loads(rawdata)
		except URLError, e:
			print "Error detected:", e

	def _get_phaseGroups(self, tourneyID):

		eventURL = "https://api.smash.gg/tournament/" + tourneyID + "?expand%5B%5D=event"
		data = self._readURL(eventURL)
		eventID = None
		for event in data["entities"]["event"]:
			if event['name'] == "Melee Singles":
				eventID = event['id']
				break

		groupURL = "https://api.smash.gg/event/" + str(eventID) + "?expand%5B%5D=groups"
		data = self._readURL(groupURL)

		self.phaseGroups.append([])
		if "groups" in data['entities']:
			for group in data['entities']['groups']:
				self.phaseGroups[-1].append(group['id'])

	def _get_players(self, groupID):
		entrantsURL = "https://api.smash.gg/phase_group/" + str(groupID) + "?expand%5B%5D=entrants"
		data = self._readURL(entrantsURL)

		if "player" in data["entities"]:
			for player in data["entities"]["player"]:
				self.playerDict[int(player['id'])] = player['gamerTag']
				self.entrantDict[int(player['id'])] = int(player['entrantId'])
				self._curr_pids.add(int(player['id']))

	def _get_matches(self, groupID):
		setsURL = "https://api.smash.gg/phase_group/" + str(groupID) + "?expand%5B%5D=sets"
		data = self._readURL(setsURL)
		print setsURL, data['entities'].keys()

		if "sets" in data["entities"]:
			print "hooray"
			for match in data["entities"]["sets"]:
				if match["loserId"]:
					if match['winnerId'] not in self.matchData:
						self.matchData[match['winnerId']] = Counter()
					self.matchData[match['winnerId']][match['loserId']] += 1

	####################################################

	def add_players(self, PD):
		for pid in self.playerDict:
			name = self.playerDict[pid]
			eid = self.entrantDict[pid]
			if name not in PD.aliasSet:
				PD.aliasSet.add(name)
				PD.aliasList.append(name)
				PD.idDict[name] = len(PD.aliasList)-1

			# this assumes that challonge player id is greater than #(players)
			# probably safe assumption, should probably formalize check later
			# use an assert and raise an error otherwise
			PD.idDict[pid] = PD.idDict[name]
			PD.idDict[eid] = PD.idDict[name]
			PD.tourneyCount[PD.idDict[pid]] += self.stourneyCount[pid]

	def add_matches(self, PD, multiGraph):
		for winnerid in self.matchData:
			for loserid in self.matchData[winnerid]:
				multiGraph[PD.idDict[winnerid]][PD.idDict[loserid]] += self.matchData[winnerid][loserid]