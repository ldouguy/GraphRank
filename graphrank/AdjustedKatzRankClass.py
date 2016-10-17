import GraphUtils as gu
import numpy as np

class AKR:
	def __init__(self, multiGraph, M):
		self.rankdata = []
		self.remaining = range(len(multiGraph))
		self.prevRemaining = range(len(multiGraph))
		self.nowins = []

		self.M = M

		for i in range(len(M)):
			for j in range(len(M)):
				self.M[i, j] = self.M[i, j]**.5

		for i in multiGraph:
			if not multiGraph[i]:
				self.nowins.append(i)
				self.remaining.remove(i)
		self.count = len(self.remaining)

		currM = self.M[np.ix_(self.remaining, self.remaining)]
		self.prevM = self.M

		eigval = max(abs(np.linalg.eig(currM)[0]))
		if not eigval or eigval < 1.6:
			eigval = 1.6
		escale = round(1*eigval**(-1), 2)

		K = gu.KRank(currM, escale, 50)
		rankdata = sorted(zip(range(len(currM)), K), key=lambda v: v[1])
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

			currM = self.M[np.ix_(self.remaining, self.remaining)]
			eigval = max(abs(np.linalg.eig(currM)[0]))
			if not eigval or eigval < 1.6:
				eigval = 1.6
			escale = round(1*eigval**(-1), 2)

			lscale = float(self.count - len(self.remaining))/self.count

			K = gu.KRank(currM, escale, 50)
			KL = gu.KRank(currM, escale, 50, direction=0)

			D = [i-j**.5 for i, j in zip(K, KL)]

			drankdata = sorted(zip(range(len(currM)), K), key=lambda v: v[1])

			# krank = gu.KRank(currM, escale, 50, reverse=False)
			# klrank = gu.KRank(currM, escale, 50, reverse=False, direction=0)

			# drankdata = [(i, j - lscale*k) for ((i, j), (n, k)) in zip(krank, klrank)]

			self.currank = [(self.remaining[i], j) for i, j in drankdata]
			self.prevM = currM
			self.prevRemain = self.remaining

			self.reduce()