import networkx as nx
import pickle
import random
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

def calc_avg_shortest_path_length(G, sample_size):
    # Randomly sample node pairs
    node_pairs = random.sample(list(G.nodes()), sample_size)

    # Calculate shortest path lengths
    shortest_path_lengths = []
    for source, target in zip(node_pairs[::2], node_pairs[1::2]):
        try:
            shortest_path_lengths.append(nx.shortest_path_length(G, source, target))
        except nx.NetworkXNoPath:
            pass  # Skip if there is no path between the two nodes

    # Calculate average shortest path length
    avg_shortest_path_length = sum(shortest_path_lengths) / len(shortest_path_lengths)

    return avg_shortest_path_length, shortest_path_lengths

# Read pre-constructed networks
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# Calculate average shortest path length and shortest path length distribution
sample_size = 50000  # Number of node pairs to sample, adjust as needed
avg_spl_ccn, spl_dist_ccn = calc_avg_shortest_path_length(G_ccn, sample_size)
avg_spl_csn, spl_dist_csn = calc_avg_shortest_path_length(G_csn, sample_size)

# Plot shortest path length distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# CCN graph
sns.kdeplot(spl_dist_ccn, ax=ax1, color='b', fill=True)
ax1.axvline(avg_spl_ccn, color='r', linestyle='--', linewidth=2, label=f'Average: {avg_spl_ccn:.2f}')
ax1.set_title('CCN Shortest Path Length Distribution')
ax1.set_xlabel('Shortest Path Length')
ax1.set_ylabel('Density')
ax1.legend(loc='upper left')

# Create right y-axis
ax1_right = ax1.twinx()
counts_ccn, bins_ccn = np.histogram(spl_dist_ccn, bins=range(1, max(spl_dist_ccn)+2), density=True)
bins_ccn = 0.5 * (bins_ccn[:-1] + bins_ccn[1:])
ax1_right.plot(bins_ccn, counts_ccn, 'bs-', label='Probability')
ax1_right.set_ylabel('Probability')
ax1_right.legend(loc='lower right')  # Set legend position to lower right

# CSN graph
sns.kdeplot(spl_dist_csn, ax=ax2, color='g', fill=True)
ax2.axvline(avg_spl_csn, color='r', linestyle='--', linewidth=2, label=f'Average: {avg_spl_csn:.2f}')
ax2.set_title('CSN Shortest Path Length Distribution')
ax2.set_xlabel('Shortest Path Length')
ax2.set_ylabel('Density')
ax2.legend(loc='upper left')

# Create right y-axis
ax2_right = ax2.twinx()
counts_csn, bins_csn = np.histogram(spl_dist_csn, bins=range(1, max(spl_dist_csn)+2), density=True)
bins_csn = 0.5 * (bins_csn[:-1] + bins_csn[1:])
ax2_right.plot(bins_csn, counts_csn, 'gs-', label='Probability')
ax2_right.set_ylabel('Probability')
ax2_right.legend(loc='lower right')  # Set legend position to lower right

fig.tight_layout()
plt.show()
