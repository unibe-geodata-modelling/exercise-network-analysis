#script for analysing shortes paths from all nodes in road network of Canton Zurich to Zurich main central station
import numpy as np
import pandas as pd
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt


#general workspace settings
myworkspace="C:/DATA/develops/zh"

#input data: the csv file for nodes and edges
nodesfile=myworkspace+"/zh_nodes.shp"
edgesfile=myworkspace+"/zh_roads.shp"
#input data: the roads file
nodesgdf = gpd.read_file(nodesfile)
edgesgdf = gpd.read_file(edgesfile)
outgraphfile=myworkspace+"/graph_normalcondition.gml"

#output data: the nodes distances file
nodesbetweennesscentralityfile=open(myworkspace+"/betweennesscentrality_normalsituation.csv","w")
nodesbetweennesscentralityfile.write("nodeid"+";"+"betweennesscentrality"+"\n")

#create graph
G = nx.Graph()
#loop through the road shapefile
for index, row in edgesgdf.iterrows():
    if row.ID_Road not in G:
        length = row.SHAPE_Leng
        nodeid1=row.nodeid1
        nodeid2 = row.nodeid2
        xcoord1=nodesgdf[nodesgdf["nodeid"]==row.nodeid1].x
        ycoord1 = nodesgdf[nodesgdf["nodeid"] == row.nodeid1].y
        if row.nodeid1 not in G:
            G.add_node(row.nodeid1, pos=(xcoord1, ycoord1))
        xcoord2=nodesgdf[nodesgdf["nodeid"]==row.nodeid2].x
        ycoord2 = nodesgdf[nodesgdf["nodeid"] == row.nodeid2].y
        if row.nodeid2 not in G:
            G.add_node(row.nodeid2, pos=(xcoord2, ycoord2))
        G.add_edge(row.nodeid1, row.nodeid2, weight=length)
print("network graph created ...")

#write graph to file
nx.write_gml(G, outgraphfile)

#calculate betweenness centrality for all nodes and write it to the output file
#Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v.
#parameter k is the number of the sample to safe time, k=1000 --> ca. 1% of the total network is taken as a sample
#if k=None, the full network will be considered. This needs some hours of computation
betweennesscentrality=nx.betweenness_centrality(G, k=1000, normalized=True, endpoints=True)
betweennesscentrality=nx.betweenness_centrality(G, k=None, normalized=True, endpoints=True)
for n in betweennesscentrality:
    nodesbetweennesscentralityfile.write(str(n)+";"+str(betweennesscentrality[n])+"\n")
nodesbetweennesscentralityfile.close()
print("betweenness centrality for nodes in ZH traffic network computed and exported to file ...")




