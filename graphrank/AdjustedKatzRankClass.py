import GraphUtils as gu
import numpy as np

# some lazy assumptions are made as written
# top_idx starts at 10, so there should be at least ~100 entries
# reduce() halts at 1/3 of player count, so player count/3 must be > top_idx

class AKR:
	def __init__(self, winDict):
		self.winDict = winDict

		adj = gu.G_to_A(winDict)
		KRank = gu.KRank(adj)

		self.top_idx = 10
		self.KRank = KRank
		self.top = set(KRank[:self.top_idx])

		self.ranking = []
		self.count = len(winDict)

		A = np.matrix([[0 for v in range(self.count)] for v in range(self.count)])
		for v in self.top:
			for w in winDict[v] & self.top:
				A[v, w] = 1

		self.top_A = A

	def reduce(self):
		top_i = [x for x in gu.KRank(self.top_A) if x in self.top][0]
		self.ranking.append(top_i)
		self.top.remove(top_i)

		i = self.KRank[self.top_idx]
		self.top.add(i)
		self.top_idx += 1

		for j in self.winDict[i] & self.top:
			self.top_A[i, j] = 1
		for j in self.top:
			if i in self.winDict[j]:
				self.top_A[j, i] = 1

		if self.top_idx < self.count/3:
			self.reduce()