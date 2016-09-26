import challonge
challonge.set_credentials("thugz", "Xa800POPVzeEDIciibV0HLPtQvPYpiXE5zbRuhqq")

def add_players(tourneyID, aliasSet, aliasDict, aliasList):
	players = challonge.participants.index(tourneyID)

	for player in players:
		if player['name'] not in aliasSet:
			aliasSet.add(player['name'])
			aliasList.append(player['name'])
			aliasDict[player['name']] = len(aliasList)-1
		aliasDict[player['id']] = aliasDict[player['name']]

def add_matches(tourneyID, multiGraph, aliasDict):
	matches = challonge.matches.index(tourneyID)

	for match in matches:
		winner = aliasDict[match['winner-id']]
		loser = aliasDict[match['loser-id']]
		multiGraph[winner][loser] += 1