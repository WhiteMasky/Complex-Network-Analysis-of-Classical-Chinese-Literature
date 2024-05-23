import networkx as nx
import pickle
import numpy as np
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

def calc_strength(G):
    # Calculate the degree and strength of each node
    degrees = dict(G.degree())
    strengths = dict(G.degree(weight='weight'))

    # Accumulate the strengths of nodes with the same degree and count them
    strength_degree = {}
    for node, degree in degrees.items():
        if degree not in strength_degree:
            strength_degree[degree] = []
        strength_degree[degree].append(strengths[node])

    # Calculate the average strength for each degree value
    avg_strength_degree = {}
    for degree, strengths in strength_degree.items():
        avg_strength_degree[degree] = sum(strengths) / len(strengths)

    return avg_strength_degree

# Read the pre-constructed networks
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# Calculate the strength-degree relationship for the networks
strength_degree_ccn = calc_strength(G_ccn)
strength_degree_csn = calc_strength(G_csn)

# Define the power-law fitting function
def powerlaw(x, a, b):
    return a * (x**b)

# Fit the CCN network
ccn_degrees, ccn_avg_strengths = zip(*[(d, s) for d, s in strength_degree_ccn.items() if d > 0])
ccn_popt, _ = curve_fit(powerlaw, ccn_degrees, ccn_avg_strengths)

# Fit the CSN network
csn_degrees, csn_avg_strengths = zip(*[(d, s) for d, s in strength_degree_csn.items() if d > 0])
csn_popt, _ = curve_fit(powerlaw, csn_degrees, csn_avg_strengths)

# Plot the double-logarithmic coordinate graph
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.loglog(ccn_degrees, ccn_avg_strengths, 'bo', markersize=4, label='Data')
x_fit_ccn = np.logspace(np.log10(min(ccn_degrees)), np.log10(max(ccn_degrees)), 100)
ax1.loglog(x_fit_ccn, powerlaw(x_fit_ccn, *ccn_popt), 'r-', label=f'Fit: a={ccn_popt[0]:.2e}, b={ccn_popt[1]:.2f}')
ax1.set_title('CCN Node Strength vs. Degree')
ax1.set_xlabel('Degree $k$')
ax1.set_ylabel('Average Node Strength $s(k)$')
ax1.legend()

ax2.loglog(csn_degrees, csn_avg_strengths, 'go', markersize=4, label='Data')
x_fit_csn = np.logspace(0, np.log10(max(csn_degrees)), 100)
ax2.loglog(x_fit_csn, powerlaw(x_fit_csn, *csn_popt), 'r-', label=f'Fit: a={csn_popt[0]:.2e}, b={csn_popt[1]:.2f}')
ax2.set_title('CSN Node Strength vs. Degree')
ax2.set_xlabel('Degree $k$')
ax2.set_ylabel('Average Node Strength $s(k)$')
ax2.legend()

fig.tight_layout()
plt.show()
