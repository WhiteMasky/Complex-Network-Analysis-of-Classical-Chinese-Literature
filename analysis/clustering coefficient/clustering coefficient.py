import networkx as nx
import pickle
import random
from collections import defaultdict
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

def calc_c_k(G):
    # Calculate the degree and clustering coefficient for each node
    degrees = dict(G.degree())
    clustering_coeffs = nx.clustering(G)

    # Accumulate clustering coefficients for nodes with the same degree and count them
    c_k = defaultdict(list)
    for node, degree in degrees.items():
        c_k[degree].append(clustering_coeffs[node])

    # Calculate the average clustering coefficient for each degree
    for degree, coeffs in c_k.items():
        c_k[degree] = sum(coeffs) / len(coeffs)

    return c_k

# Read pre-constructed networks
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# Randomly sample nodes from the network
def sample_graph(G, sample_size):
    sampled_nodes = random.sample(G.nodes(), sample_size)
    sampled_graph = G.subgraph(sampled_nodes)
    return sampled_graph

# Sample the networks
sample_size = 10000  # Adjust the number of nodes to sample as needed
sampled_ccn = sample_graph(G_ccn, sample_size)
sampled_csn = sample_graph(G_csn, sample_size)

# Calculate the clustering coefficient vs. degree relationship for the sampled networks
c_k_ccn = calc_c_k(sampled_ccn)
c_k_csn = calc_c_k(sampled_csn)

# Define the power-law fitting function
def powerlaw(x, a, b):
    return a * (x**b)

# Fit the CCN network, excluding data points with degree k<10
ccn_degrees, ccn_avg_ccs = zip(*[(k, v) for k, v in c_k_ccn.items() if k >= 10])
ccn_popt, _ = curve_fit(powerlaw, ccn_degrees, ccn_avg_ccs)

# Fit the CSN network, excluding data points with degree k<10
csn_degrees, csn_avg_ccs = zip(*[(k, v) for k, v in c_k_csn.items() if k >= 10])
csn_popt, _ = curve_fit(powerlaw, csn_degrees, csn_avg_ccs)

# Plot the data on a log-log scale
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.loglog(list(c_k_ccn.keys()), list(c_k_ccn.values()), 'bo', markersize=4, label='Data')
ax1.loglog(ccn_degrees, powerlaw(ccn_degrees, *ccn_popt), 'r-', label=f'Fit: a={ccn_popt[0]:.2e}, b={ccn_popt[1]:.2f}')
ax1.set_title('CCN Clustering Coefficient vs. Degree (Sampled)')
ax1.set_xlabel('Degree $k$')
ax1.set_ylabel('Average Clustering Coefficient $C(k)$')
ax1.legend()

ax2.loglog(list(c_k_csn.keys()), list(c_k_csn.values()), 'go', markersize=4, label='Data')
ax2.loglog(csn_degrees, powerlaw(csn_degrees, *csn_popt), 'r-', label=f'Fit: a={csn_popt[0]:.2e}, b={csn_popt[1]:.2f}')
ax2.set_title('CSN Clustering Coefficient vs. Degree (Sampled)')
ax2.set_xlabel('Degree $k$')
ax2.set_ylabel('Average Clustering Coefficient $C(k)$')
ax2.legend()

fig.tight_layout()
plt.show()
