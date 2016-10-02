import challonge
challonge.set_credentials("thugz", "Xa800POPVzeEDIciibV0HLPtQvPYpiXE5zbRuhqq")

def add_players(tourneyID, aliasSet, aliasDict, aliasList, tourneyCount):
	players = challonge.participants.index(tourneyID)

	for player in players:
		if player['name'] not in aliasSet:
			aliasSet.add(player['name'])
			aliasList.append(player['name'])
			aliasDict[player['name']] = len(aliasList)-1

		# this assumes that challonge player id is greater than #(players)
		# probably safe assumption, should probably formalize check later
		# use an assert and raise an error otherwise
		aliasDict[player['id']] = aliasDict[player['name']]
		tourneyCount[player['id']] += 1

def add_matches(tourneyID, multiGraph, aliasDict):
	matches = challonge.matches.index(tourneyID)

	for match in matches:
		winner = aliasDict[match['winner-id']]
		loser = aliasDict[match['loser-id']]
		multiGraph[winner][loser] += 1