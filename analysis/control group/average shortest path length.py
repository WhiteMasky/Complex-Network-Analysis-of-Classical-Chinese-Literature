import networkx as nx
import pickle
import random
import numpy as np

def calc_avg_shortest_path_length(G, sample_ratio, num_samples):
    num_nodes = len(G.nodes())
    sample_size = int(num_nodes * sample_ratio)

    avg_shortest_path_lengths = []

    for _ in range(num_samples):
        node_pairs = random.sample(list(G.nodes()), sample_size)

        shortest_path_lengths = []
        for source, target in zip(node_pairs[::2], node_pairs[1::2]):
            try:
                shortest_path_lengths.append(nx.shortest_path_length(G, source, target))
            except nx.NetworkXNoPath:
                pass  # Skip if there is no path between the two nodes

        if shortest_path_lengths:
            avg_shortest_path_lengths.append(sum(shortest_path_lengths) / len(shortest_path_lengths))

    overall_avg_shortest_path_length = sum(avg_shortest_path_lengths) / len(avg_shortest_path_lengths)

    return overall_avg_shortest_path_length


# Read the pre-built networks
with open('ccnRandom.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('csnRandom.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# Set the sampling ratio and number of samples
sample_ratio = 0.01
num_samples = 100

# Calculate the average shortest path length for CCN and CSN
avg_spl_ccn = calc_avg_shortest_path_length(G_ccn, sample_ratio, num_samples)
avg_spl_csn = calc_avg_shortest_path_length(G_csn, sample_ratio, num_samples)

print(f'CCNRandom Average Shortest Path Length: {avg_spl_ccn:.2f}')
print(f'CSNRandom Average Shortest Path Length: {avg_spl_csn:.2f}')
