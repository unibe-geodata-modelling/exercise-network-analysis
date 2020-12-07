#script for showing exemplarily the use of networkx for the analysis of co-authors networks

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


#general workspace settings
myworkspace="C:/DATA/develops/LiteratureAnalysis"

#input data: the txt file with all the papers of the GIUB with GIUB-professors as co-authors. Exported from BORIS.unibe.ch
papersfile=open(myworkspace+"/papersGIUB.txt", "r")

#list of GIUB professors, surnames used only --> further improvement needed if used for in-depth analysis.
proflist=["Bottazzi", "Brönnimann", "Gerber", "Grosjean", "Keiler", "Martius", "Mayer", "Messerli", "Schaefli", "Schurr", "Speranza", "Thieme", "Veit", "Zischg"]


#create a list of unique papers
paperslist=[]
for line in papersfile:
    if line not in paperslist:
        paperslist.append(line)
papersfile.close()

#create graph
G = nx.Graph()
G.add_nodes_from(proflist)

for paper in paperslist:
    isauthorlist=[]
    for prof in proflist:
        coauthorslist=proflist.copy()
        coauthorslist.remove(prof)
        if prof in paper:
            for coauthor in coauthorslist:
                if coauthor in paper:
                    G.add_edge(prof,coauthor)

#create a graph
plt.figure(figsize=(15, 15))
nx.draw_shell(G, with_labels=True,)

#analysis of the number of connections
coauthorships = {}
for x in G.nodes:
    coauthorships[x] = len(G[x])

print(coauthorships)