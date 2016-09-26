# GraphRank

GraphRank is a ranking algorithm intended to rank players in a tournament-based competitive scene, namely for Super Smash Bros Melee. It is designed for use with the Challonge API, but tournament data can be directly added as well.

## Usage

The current intended and documented functionality of the GraphRank package is to (1) retrieve tournament data from Challonge and (2) to calculate an approximate ranking of associated players.

GraphRank is a simple Python package, installed in the usual way. First, download and extract the tar file located in dist, then navigate to the folder and run:

	python setup.py install

For an example on how to generate rankings from Challonge links, see the "example.py" script in the example directory.

## Requirements

- NumPy
- pychallonge (https://github.com/russ-/pychallonge)

# Background

The core mathematics behind GraphRank are graph theoretic. GraphRank views the competitive scene as a graph with vertices as players, with an edge from A to B if "A beats B".

Once this graph is retrieved from tournament results, centrality analysis is ran on various portions of the graph algorithmically to order the players by skill. This is similar to Google's PageRank algorithm, which views websites as nodes and links between them as edges. PageRank uses centrality to determine the "influential" nodes, roughly the nodes receiving the most links. Similarly, GraphRank roughly finds the players who receive the most wins. (For more information, see Katz Centrality: https://en.wikipedia.org/wiki/Centrality#Katz_centrality_and_PageRank)

## Ranking Paradigm

GraphRank focuses on using the entire network of player data to infer connections between any pair of players. This is a completely different philosophy from the only existing algorithms, which are entirely point based. Point based algorithms are more explicit and detail oriented, without much focus on inference of data. Because competitive scenes which rely on tournaments have much less data than competitive scenes such as DoTa or LoL, data inference must be prioritized. (For more details, read my blog post about the subject: http://www.meleeitonme.com/guest-article-the-state-of-smash-and-rankings/)

## Ongoing Development:

GraphRank is still in Beta and is published mostly for sake of documentation and proof of concept. Issues such as optimizations and unit testing will be dealt with when the package is intended for more wide use.

Upcoming updates should be focued on:

- Accuracy of the Katz Centrality and correcting algorithm
- Addition of functionality such as excluding players with too few tournaments or games
- More data files added

For any questions, please contact me via github.