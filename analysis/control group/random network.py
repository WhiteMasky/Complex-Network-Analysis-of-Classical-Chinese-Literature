import pickle
import networkx as nx

# Generate the first random network and save it
G_random1 = nx.gnm_random_graph(156879, 3119616)
with open('ccnRandom.gpickle', 'wb') as f:
    pickle.dump(G_random1, f)

# Generate the second random network and save it
G_random2 = nx.gnm_random_graph(74837, 2766801)
with open('csnRandom.gpickle', 'wb') as f:
    pickle.dump(G_random2, f)
