# GraphRank

GraphRank is a ranking algorithm intended to rank players in a tournament-based competitive scene, namely for Super Smash Bros Melee. It is designed for use with the Challonge API, but tournament data can be directly added as well.

## Usage

GraphRank is a simple Python package, installed in the usual way. First, clone this repo or download the necessary files, and install from the command line (with root access) in the usual way:

	python setup.py install

Or simply execute code from the directory containing the graphrank module.

For an example on how to generate rankings from Challonge links, see the "example.py" script in the example directory.

Documentation is incomplete and in the process of updating.

## Requirements

- NumPy
- pychallonge (https://github.com/russ-/pychallonge)

# Background

The core mathematics behind GraphRank are graph theoretic. GraphRank views the competitive scene as a graph with vertices as players, with an edge from A to B if "A beats B".

Once this graph is retrieved from tournament results, centrality analysis is ran on various portions of the graph algorithmically to order the players by skill. This is similar to Google's PageRank algorithm, which views websites as nodes and links between them as edges. PageRank uses centrality to determine the "influential" nodes, roughly the nodes receiving the most links. Similarly, GraphRank roughly finds the players who receive the most wins. (For more information, see Katz Centrality: https://en.wikipedia.org/wiki/Centrality#Katz_centrality_and_PageRank)

## Ranking Paradigm

GraphRank focuses on using the entire network of player data to infer connections between any pair of players. This is a completely different philosophy from the only existing algorithms, which are entirely point based. Point based algorithms are more explicit and detail oriented, without much focus on inference of data. Because competitive scenes which rely on tournaments have much less data than competitive scenes such as DotA or LoL, data inference must be prioritized. (For more details, read my blog post about the subject: http://www.meleeitonme.com/guest-article-the-state-of-smash-and-rankings/)

## Ongoing Development:

GraphRank is still in Beta and is published mostly for sake of documentation and proof of concept. Issues such as optimizations and unit testing will be dealt with when the package is intended for more wide use.

Upcoming updates should be focused on:

- Accuracy of the Katz Centrality and correcting algorithm
- Addition of defensive coding checks and unittests
- Addition of other APIs, such as from Smashgg
- Improvements to data storage and reusability of saved data

For any questions, please contact me via github.