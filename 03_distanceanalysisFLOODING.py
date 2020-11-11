#script for analysing shortes paths from all nodes in road network of Canton Zurich to Zurich main central station
import pandas as pd
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt

#general workspace settings
myworkspace="C:/DATA/develops/zh"

#input data: the csv file for nodes and edges
nodesfile=myworkspace+"/zh_nodes.shp"
edgesfile=myworkspace+"/zh_roads.shp"
floodmap=myworkspace+"/WB_HW_IK100_F_LV03.shp"
#input data: the roads file
nodesgdf = gpd.read_file(nodesfile)
edgesgdf = gpd.read_file(edgesfile)
floodmapgdf=gpd.read_file(floodmap)

#output data: the nodes distances file
nodesdistancesfile=open(myworkspace+"/nodesdistancesflooding.csv","w")
nodesdistancesfile.write("nodeid"+";"+"distancetoZHsbbFLOOD"+"\n")

nodesgdf.plot()
edgesgdf.plot()
floodmapgdf.plot()

#intersect nodes and edges with flood map
floodednodes=gpd.overlay(nodesgdf, floodmapgdf, how='intersection')
floodededges=gpd.overlay(edgesgdf, floodmapgdf, how='intersection')

#create lists of flooded nodes and flooded edges (will not be part of the created graph
listoffloodededges=floodednodes["ID_Road"].unique().tolist()
listoffloodednodes=floodededges["ID_Road"].unique().tolist()

#create graph
G = nx.Graph()
nodesidlist=[]
edgesidlist=[]
#loop through the road shapefile
for index, row in edgesgdf.iterrows():
    if row.ID_Road not in listoffloodededges:
        length = row.SHAPE_Leng
        if row.nodeid1 not in listoffloodednodes:
            xcoord=nodesgdf[nodesgdf["nodeid"]==row.nodeid1].x
            ycoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid1].y
            if row.nodeid1 not in G:
                G.add_node(row.nodeid1, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid1)
        if row.nodeid2 not in listoffloodednodes:
            xcoord=nodesgdf[nodesgdf["nodeid"]==row.nodeid2].x
            ycoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid2].y
            if row.nodeid2 not in G:
                G.add_node(row.nodeid2, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid2)
        edgesidlist.append(row.ID_Road)
        if row.nodeid1 not in listoffloodednodes and row.nodeid2 not in listoffloodednodes:
            G.add_edge(row.nodeid1, row.nodeid2, weight=length)
print("network graph created ...")

#calculate shortest distance to Zurich main railway station during flooding
#target is main railway station in Zurich = node_id 76266
targetnode=72356
#calculate shortest path for each node
i=0
for n in list(G.nodes):
    print(i)
    sourcenode =n
    if nx.has_path(G,sourcenode,targetnode):
        distancetoZHsbbFLOOD=nx.shortest_path_length(G,source=sourcenode, target=targetnode, weight="weight")
        nodesdistancesfile.write(str(sourcenode)+";"+str(distancetoZHsbbFLOOD)+"\n")
    i+=1
nodesdistancesfile.close()
print("shortest paths to ZH main station during flooding computed ...")


