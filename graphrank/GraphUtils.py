import numpy as np

# G denotes dict representation of graph with ID1 in G[ID2] if player 2 beats player 1
# MG denotes multigraph dict representation of graph (MG = {winner: {loser: score}})
# M denotes matrix representation of graph with n = M[i][j] where player i beats player j n times
# A denotes matrix adjacency matrix
# T denotes "touching" matrix (symm(A))

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

# Katz Centrality
############################

def katz_degree(A, k):
    katz = k*A

    curr = A.copy()
    curr_damp = k

    for i in range(10):
        curr *= A
        curr_damp *= k
        katz += curr_damp*curr

    return katz

# using damping coeff = .5 for ease of use now, can make this configurable
def KRank(A):
    D = katz_degree(A, .5)
    K = (np.sum(D, axis=1)).flatten().tolist()[0]

    players = range(len(A))

    KRank = sorted(players, key=lambda v: K[v], reverse=True)

    return KRank

def DRank(A):
    D = katz_degree(A, .5)
    K = (np.sum(D, axis=1)).flatten().tolist()[0]
    KL = (np.sum(D, axis=0)).flatten().tolist()[0]

    players = range(len(A))

    DRank = sorted(players, key=lambda v: K[v] - KL[v], reverse=True)

    return DRank