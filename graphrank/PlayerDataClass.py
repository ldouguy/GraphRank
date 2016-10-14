from collections import Counter
import json

class PlayerData:
	def __init__(self, aliasSet=None, tourneyCount=None, assoc=None, aliasList=None, idDict=None):
		self.aliasList = aliasList
		if not aliasList:
			self.aliasList = []

		self.aliasSet = aliasSet
		if not aliasSet:
			self.aliasSet = set()

		self.idDict = idDict
		if not idDict:
			self.idDict = {}

		self.tourneyCount = tourneyCount
		if not tourneyCount:
			self.tourneyCount = Counter()

		self.assoc = assoc
		if assoc:
			for player in assoc:
				self.aliasSet.add(player)
				if assoc[player] not in self.aliasSet:
					self.aliasSet.add(assoc[player])
					self.aliasList.append(assoc[player])
					self.idDict[assoc[player]] = len(self.aliasList)-1
				self.idDict[player] = self.idDict[assoc[player]]

	##########################

	def save_to_json(self, outfile="playerdata.json"):
		data = {
			"aliasSet": self.aliasSet,
			"aliasList": self.aliasList,
			"idDict": self.idDict,
			"tourneyCount": self.tourneyCount
		}

		with open(outfile, "w") as out:
			json.dump(data, out)