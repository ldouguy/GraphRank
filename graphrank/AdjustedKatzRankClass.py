import GraphUtils as gu
import numpy as np

class AKR:
	def __init__(self, multiGraph, A):
		self.rankdata = []
		self.remaining = range(len(multiGraph))
		self.nowins = []

		self.A = A

		for i in multiGraph:
			if not multiGraph[i]:
				self.nowins.append(i)
				self.remaining.remove(i)
		self.count = len(self.remaining)

		currA = self.A[np.ix_(self.remaining, self.remaining)]

		eigval = max(abs(np.linalg.eig(currA)[0]))
		if not eigval or eigval < 1.6:
			eigval = 1.6
		escale = round(.8*eigval**(-1), 2)

		rankdata = gu.KRank(currA, escale, 50, reverse=False)
		self.currank = [(self.remaining[i], j) for i, j in rankdata]

	def reduce(self):
		if len(self.currank) <= 5:
			# I don't understand why I need to make this check
			# If I don't, rankdata somehow gets the last currank appended twice
			if self.rankdata[-1] != self.currank:
				self.rankdata.append(self.currank)

		else:
			self.rankdata.append(self.currank)

			#find point of change after cutoff point
			n = len(self.currank)/3
			while self.currank[n] == self.currank[n+1]:
				n += 1

			for i in [i for i,j in self.currank[:n]]:
				self.remaining.remove(i)

			currA = self.A[np.ix_(self.remaining, self.remaining)]
			eigval = max(abs(np.linalg.eig(currA)[0]))
			if not eigval or eigval < 1.6:
				eigval = 1.6
			escale = round(.8*eigval**(-1), 2)

			drankdata = gu.DRank(currA, escale, 50, float(len(self.rankdata))/self.count, reverse=False)
			self.currank = [(self.remaining[i], j) for i, j in drankdata]

			self.reduce()