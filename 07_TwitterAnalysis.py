#script for exemplarily showing th emining of twitter data and creating graphs from twitter data
import pandas as pd
import matplotlib.pyplot as plt
import twint
import networkx as nx

#configure twint setting, access to twitter data
c = twint.Config()
c.Pandas = True
username = 'JanosAmmann' #this must be the twitter username of the person from whom you will analyse the twitter accounts that he/she is following. Change it accordingly
number_of_levels=2 #how many levels of depth in the analysis are considered. Attention: delimit it to up to max 2 levels if you show the code in live exercises
c.Username = username

#create graph
G = nx.Graph()
nodeslist=[]
#add the first node, the user
G.add_node(username)
nodeslist.append(username)
nodeslevels=[]
nodeslevels.append(username)

#get followings from user
#level 0
list_of_followings=[]
try:
    twint.run.Following(c)
    list_of_followings = twint.storage.panda.Follow_df['following'][username]
    nodeslevels.append(list_of_followings)
    for item in list_of_followings:
        G.add_node(item)
        G.add_edge(username, item)
        nodeslist.append(item)
except KeyError:
    print('IndexError')
#other levels
for level in range(1,number_of_levels+1):
    print("level: "+str(level))
    nodeslevelsB=[]
    for node in nodeslevels[level]:
        print(node)
        list_of_followings = []
        c.Username = node
        try:
            twint.run.Following(c)
            list_of_followings = twint.storage.panda.Follow_df['following'][node]
            for item in list_of_followings:
                if item not in G.nodes:
                    nodeslist.append(item)
                    G.add_node(item)
                    G.add_edge(node, item)
                else:
                    G.add_edge(node, item)
                nodeslevelsB.append(item)
        except KeyError:
            print('IndexError')
    nodeslevels.append(nodeslevelsB)
#save the graph to file
nx.write_gexf(G, path="C:/DATA/twitterdata.gexf")

#plot the graph
plt.figure(figsize=(15, 15))
nx.draw(G, with_labels=True)
plt.savefig("C:/Users/evama/OneDrive/Documents/Python/Twitter/twitteranalysis_standardlayout.png")
plt.close()
#alternative plot
plt.figure(figsize=(15, 15))
nx.draw_kamada_kawai(G, with_labels=True)
plt.savefig("C:/Users/evama/OneDrive/Documents/Python/Twitter/twitteranalysis_kamada_kawai_layout.png")
plt.close()
#alternative plot
plt.figure(figsize=(15, 15))
nx.draw_spectral(G, with_labels=True)
plt.savefig("C:/Users/evama/OneDrive/Documents/Python/Twitter/twitteranalysis_spectrallayout.png")
plt.close()




