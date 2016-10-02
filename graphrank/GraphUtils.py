import numpy as np
from collections import Counter

# data conversion utils
###########################

# G denotes dict representation of graph with ID1 in G[ID2] if player 2 beats player 1
# D denotes dict of draws: j in D[i] if i and j beat each other equal times
# MG denotes multigraph dict representation of graph (MG = {winner: {loser: score}})
# M denotes matrix representation of graph with n = M[i][j] where player i beats player j n times
# A denotes matrix adjacency matrix (A[i][j] = 1 if i beats j)
# T denotes "touching" matrix (symm(A) or T[i][j] = 1 if A[i][j] or A[j][i] = 1)

def MG_to_M(MG):
	count = len(MG)
	M = [[0 for i in range(count)] for i in range(count)]
	for winner in MG:
		for loser in MG[winner]:
			M[winner][loser] = MG[winner][loser]
	return np.matrix(M)

# record draws as a second dictionary
# TO DO: write function which determines who wins
#   function(array(matches)) where matches are (winner, date) pairs

def MG_to_G(MG):
    G = {v: set() for v in MG}
    D = {v: set() for v in MG}
    for w in MG:
        for l in MG[w]:
            if MG[w][l] > MG[l][w]:
                G[w].add(l)
            elif MG[w][l] > 0 and MG[w][l] == MG[l][w]:
                D[w].add(w)

    return [G, D]

def reverse_G(G):
    reverse = {v: set() for v in G}
    for v in G:
        for w in G[v]:
            reverse[w].add(v)

    return reverse

def G_to_A(G):
    A = [[0 for v in G] for v in G]

    for v in G:
        for w in G[v]:
            A[v][w] = 1

    return np.matrix(A)

# Katz Centrality
############################

def katz_degree(A, k, lim):
    katz = k*A

    curr = A.copy()
    curr_damp = k

    for i in range(lim):
        curr *= A
        curr_damp *= k
        katz += curr_damp*curr

    return katz

# direction gives direction of arrows in graph
# 0 for losses, 1 for wins(default)
def KRank(A, k, lim, direction=1, reverse=True):
    D = katz_degree(A, k, lim)
    K = (np.sum(D, axis=direction)).flatten().tolist()[0]

    players = zip(range(len(A)), K)

    KRank = sorted(players, key=lambda v: v[1], reverse=reverse)

    return KRank

def DRank(A, k, lim, scale, reverse=True):
    B = katz_degree(A, k, lim)
    K = (np.sum(B, axis=1)).flatten().tolist()[0]
    KL = (np.sum(B, axis=0)).flatten().tolist()[0]

    players = zip(range(len(A)), [K[v] - scale*KL[v] for v in range(len(K))])

    DRank = sorted(players, key=lambda v: v[1], reverse=reverse)

    return DRank

# Tarjan
########################

SCC_idx = 0
p_index = 0

def SCC(G):
    V_index = {
        v : None for v in G
    }
    lowlink = {
        v : None for v in G
    }
    S = []
    partition = []

    #in case multiple calls to this function are made, reset global values
    global SCC_idx, p_index
    SCC_idx, p_index = 0, 0

    for v in G:
        if not V_index[v]:
            strongconnect(G, v, V_index, lowlink, S, partition)

    return partition

def strongconnect(G, v, V_index, lowlink, S, partition):
    global SCC_idx, p_index
    V_index[v] = SCC_idx
    lowlink[v] = SCC_idx
    SCC_idx += 1
    S.append(v)

    for w in G[v]:
        if not V_index[w]:
            strongconnect(G, w, V_index, lowlink, S, partition)
            lowlink[v] = min(lowlink[v], lowlink[w])
        elif w in S:
            lowlink[v] = min(lowlink[v], lowlink[w])

    if lowlink[v] == V_index[v]:
        partition.append(set())

        w = S.pop()

        while v != w:
            partition[p_index].add(w)

            w = S.pop()

        partition[p_index].add(w)

        p_index += 1

# Cycles
###########################

def record_cycles(G, partition):
    in_cycle = {
        v: set() for v in G
    }

    for S in partition:
        for v in S:
            S1 = G[v] & S
            S2 = set()
            for w in S1:
                S2 |= G[w]
            for w in S2:
                if v in G[w]:
                    in_cycle[v].add(w)
                    in_cycle[w].add(v)

    return in_cycle

def record_isBelow(G, inCycle):
    isBelow = {
        v: set() for v in G
    }

    for v in G:
        for w in G[v]-inCycle[v]:
            isBelow[v] |= G[w]-inCycle[w]

    return isBelow

def record_stronglyBelow(G, isBelow, inCycle):
    stronglyBelow = {
        v: set() for v in G
    }

    connectCount = Counter()

    for v in G:
        for w in G[v]-inCycle[v]:
            for x in G[w]-inCycle[w]:
                connectCount[(v, x)] += 1

    for (v, w) in connectCount:
        if connectCount[(v, w)] > 1:
            stronglyBelow[v].add(w)

    return stronglyBelow