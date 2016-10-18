import GraphUtils as gu
import numpy as np

class AKR:
	def __init__(self, multiGraph, M, damp=.8, sieve=3, top=5, eiglim=1.6, wlcf=lambda x,y: x):
		self.rankdata = []
		self.remaining = range(len(multiGraph))
		self.prevRemaining = range(len(multiGraph))
		self.nowins = []

		self.M = M
		self.damp = damp
		self.sieve = sieve
		self.top = top
		self.eiglim = eiglim
		self.wlcf = wlcf

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
		if not eigval or eigval < eiglim:
			eigval = eiglim
		escale = damp*eigval**(-1)

		K = gu.KRank(currM, escale, 50)
		rankdata = sorted(zip(range(len(currM)), K), key=lambda v: v[1])
		self.currank = [(self.remaining[i], j) for i, j in rankdata]

	def reduce(self):
		while len(self.currank) > self.top:
			self.rankdata.append(self.currank)

			#find point of change after cutoff point
			n = max(1, len(self.currank)/self.sieve)
			while self.currank[n] == self.currank[n+1]:
				n += 1

			for i in [i for i,j in self.currank[:n]]:
				self.remaining.remove(i)

			currM = self.M[np.ix_(self.remaining, self.remaining)]
			eigval = max(abs(np.linalg.eig(currM)[0]))
			if not eigval or eigval < self.eiglim:
				eigval = self.eiglim
			escale = self.damp*eigval**(-1)

			# used for scaling losses in wlcf
			lscale = float(self.count - len(self.remaining))/self.count

			K = gu.KRank(currM, escale, 50)
			KL = gu.KRank(currM, escale, 50, direction=0)

			D = [self.wlcf(i, j) for i, j in zip(K, KL)]

			drankdata = sorted(zip(range(len(currM)), D), key=lambda v: v[1])

			self.currank = [(self.remaining[i], j) for i, j in drankdata]
			self.prevM = currM
			self.prevRemain = self.remaining

		# I don't understand why I need to make this check
		# If I don't, rankdata somehow gets the last currank appended twice
		if self.rankdata[-1] != self.currank:
			self.rankdata.append(self.currank)