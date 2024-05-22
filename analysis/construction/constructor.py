import json
import networkx as nx
import pickle

# Load CCN from JSON file and construct the graph
try:
    with open('ccn.gpickle', 'rb') as f:
        ccn = pickle.load(f)
    print("CCN loaded from file.")
except FileNotFoundError:
    with open('ccn.json', 'r', encoding='utf-8') as f:
        ccn_data = json.load(f)
    ccn = nx.Graph()
    for node1, neighbors in ccn_data.items():
        ccn.add_node(node1)
        for node2, weight in neighbors.items():
            ccn.add_edge(node1, node2, weight=weight)
    print("CCN constructed.")
    print(f"Number of nodes in CCN: {ccn.number_of_nodes()}")
    print(f"Number of edges in CCN: {ccn.number_of_edges()}")
    with open('ccn.gpickle', 'wb') as f:
        pickle.dump(ccn, f, pickle.HIGHEST_PROTOCOL)

# Load CSN from JSON file and construct the graph
try:
    with open('csn.gpickle', 'rb') as f:
        csn = pickle.load(f)
    print("\nCSN loaded from file.")
except FileNotFoundError:
    with open('csn.json', 'r', encoding='utf-8') as f:
        csn_data = json.load(f)
    csn = nx.Graph()
    for node1, neighbors in csn_data.items():
        csn.add_node(node1)
        for node2, weight in neighbors.items():
            csn.add_edge(node1, node2, weight=weight)
    print("\nCSN constructed.")
    print(f"Number of nodes in CSN: {csn.number_of_nodes()}")
    print(f"Number of edges in CSN: {csn.number_of_edges()}")
    with open('csn.gpickle', 'wb') as f:
        pickle.dump(csn, f, pickle.HIGHEST_PROTOCOL)
