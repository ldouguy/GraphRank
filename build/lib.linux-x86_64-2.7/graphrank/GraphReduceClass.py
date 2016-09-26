import GraphUtils as gu

class GR:
	def __init__(self, winDict, drawDict, cycleDict, isBelow):
		records = {v: [set(), set(), set(), set()] for v in winDict}
		for v in winDict:
			for w in winDict[v]:
				records[v][0].add(w)
				records[w][1].add(v)
		for v in drawDict:
			records[v][2] = drawDict[v]

		#delete players with 0 results
		to_del = []
		for v in records:
			if not records[v][0] and not records[v][1] and not records[v][2]:
				to_del.append(v)
		for v in to_del:
			del records[v]

		self.records = records

		top = set()
		for v in records:
			if not records[v][1]:
				top.add(v)

		self.top = top
		self.ranking = []
		self.ranked = set()
		self.inCycle = cycleDict
		self.isBelow = isBelow

	def rank(self, player):
		records = self.records

		for v in records:
			records[v][1].discard(player)
			if player in records[v][0]:
				records[v][0].remove(player)
				records[v][3].add(player)

		self.ranking.append(player)
		self.ranked.add(player)
		self.top.remove(player)

		for v in records[player][1]:
			self.top.add(v)

		del records[player]

		flag = False
		for v in records:
			if not records[v][1]:
				self.top.add(v)
				flag = True
		if not flag:
			for v in records:
				if records[v][1].issubset(records[v][2]):
					self.top.add(v)
					if not flag:
						print "all players have losses"
					flag = True
		if not flag:
			print "all players have non-cyclic losses"

			if not self.top:
				best_ratio = 0
				best_v = None
				for v in records:
					a1 = len(records[v][1])+1
					a2 = len(self.isBelow[v])
					if a2/a1 > best_ratio:
						best_ratio = a2/a1
						best_v = v
				self.top.add(best_v)
				print "added %s" % best_v
				for w in records[best_v][1]:
					self.top.add(w)
					for x in records[w][1]:
						self.top.add(x)

		if len(self.top) == 1:
			v = list(self.top)[0]
			self.top |= records[v][1]