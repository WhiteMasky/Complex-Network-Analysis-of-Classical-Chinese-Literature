import networkx as nx
import pickle
import random
from collections import defaultdict
import numpy as np

import matplotlib.pyplot as plt

def calc_knn(G, sample_nodes):
    # Calculate the average nearest neighbor degree for sample nodes
    knn_k = defaultdict(list)
    for node in sample_nodes:
        neighbors = list(G.neighbors(node))
        if len(neighbors) > 0:  # Make sure the node has at least one neighbor
            avg_degree = sum(G.degree(n) for n in neighbors) / len(neighbors)
            knn_k[G.degree(node)].append(avg_degree)

    # For each degree value, calculate the average nearest neighbor degree
    for degree, knn_values in knn_k.items():
        knn_k[degree] = sum(knn_values) / len(knn_values)

    return knn_k

# Read the pre-built networks
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# Randomly sample nodes from the networks
def sample_graph(G, sample_size):
    return random.sample(G.nodes(), sample_size)

# Perform sampling on the networks
sample_size = 50000  # Number of nodes to sample, adjust as needed
sample_nodes_ccn = sample_graph(G_ccn, sample_size)
sample_nodes_csn = sample_graph(G_csn, sample_size)

# Calculate the relationship between the average nearest neighbor degree and the degree of the samples
knn_k_ccn = calc_knn(G_ccn, sample_nodes_ccn)
knn_k_csn = calc_knn(G_csn, sample_nodes_csn)

# Calculate the Pearson correlation coefficient
def calc_pearson_correlation(knn_k):
    degrees, knn_values = zip(*[(k, v) for k, v in knn_k.items()])
    return np.corrcoef(degrees, knn_values)[0, 1]

r_ccn = calc_pearson_correlation(knn_k_ccn)
r_csn = calc_pearson_correlation(knn_k_csn)

# Plot the double logarithmic coordinate graph and add the fitting line
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.loglog(list(knn_k_ccn.keys()), list(knn_k_ccn.values()), 'bo', markersize=4, label='Data')
ax1.set_title(f'CCN Average Nearest Neighbor Degree vs. Degree\nPearson correlation: {r_ccn:.4f}')
ax1.set_xlabel('Degree $k$')
ax1.set_ylabel('Average Nearest Neighbor Degree $k_{nn}(k)$')

# Add the fitting line
x_ccn = np.log10(list(knn_k_ccn.keys()))
y_ccn = np.log10(list(knn_k_ccn.values()))
coeffs_ccn = np.polyfit(x_ccn, y_ccn, 1)
ax1.loglog(10**x_ccn, 10**(coeffs_ccn[0]*x_ccn + coeffs_ccn[1]), 'r-', label='Fit')
ax1.legend()

ax2.loglog(list(knn_k_csn.keys()), list(knn_k_csn.values()), 'go', markersize=4, label='Data')
ax2.set_title(f'CSN Average Nearest Neighbor Degree vs. Degree\nPearson correlation: {r_csn:.4f}')
ax2.set_xlabel('Degree $k$')
ax2.set_ylabel('Average Nearest Neighbor Degree $k_{nn}(k)$')

# Add the fitting line
x_csn = np.log10(list(knn_k_csn.keys()))
y_csn = np.log10(list(knn_k_csn.values()))
coeffs_csn = np.polyfit(x_csn, y_csn, 1)
ax2.loglog(10**x_csn, 10**(coeffs_csn[0]*x_csn + coeffs_csn[1]), 'r-', label='Fit')
ax2.legend()

fig.tight_layout()
plt.show()
