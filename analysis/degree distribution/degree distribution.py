import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pickle
import numpy as np

def degree_distribution(G):
    degrees = nx.degree_histogram(G)
    return [degrees[d]/float(G.number_of_nodes()) for d in range(len(degrees))]

# 读取已构建好的网络
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# 计算度分布
ccn_deg_dist = degree_distribution(G_ccn)
csn_deg_dist = degree_distribution(G_csn)

# power law拟合函数
def powerlaw(x, a, b):
    return a * (x**b)

# 手动选择 x_min
x_min_ccn = 5
x_min_csn = 5

# 对CCN进行拟合
degrees_ccn = np.array(range(1, len(ccn_deg_dist) + 1))
ccn_degrees_filtered = degrees_ccn[degrees_ccn >= x_min_ccn]
ccn_deg_dist_filtered = np.array(ccn_deg_dist)[degrees_ccn >= x_min_ccn]
ccn_fit = curve_fit(powerlaw, ccn_degrees_filtered, ccn_deg_dist_filtered)
ccn_gamma = ccn_fit[0][1]

# 对CSN进行拟合
degrees_csn = np.array(range(1, len(csn_deg_dist) + 1))
csn_degrees_filtered = degrees_csn[degrees_csn >= x_min_csn]
csn_deg_dist_filtered = np.array(csn_deg_dist)[degrees_csn >= x_min_csn]
csn_fit = curve_fit(powerlaw, csn_degrees_filtered, csn_deg_dist_filtered)
csn_gamma = csn_fit[0][1]

# 绘制log-log度分布图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.loglog(degrees_ccn, ccn_deg_dist, 'bo', markersize=4, label='Data')
ax1.set_title('CCN Degree Distribution')
ax1.set_xlabel('Degree $k$')
ax1.set_ylabel('$P(k)$')
ax1.loglog(ccn_degrees_filtered, powerlaw(ccn_degrees_filtered, *ccn_fit[0]), 'r--', label='Fit: $k^{:.2f}$'.format(ccn_gamma))
ax1.legend()

ax2.loglog(degrees_csn, csn_deg_dist, 'go', markersize=4, label='Data')
ax2.set_title('CSN Degree Distribution')
ax2.set_xlabel('Degree $k$')
ax2.set_ylabel('$P(k)$')
ax2.loglog(csn_degrees_filtered, powerlaw(csn_degrees_filtered, *csn_fit[0]), 'r--', label='Fit: $k^{:.2f}$'.format(csn_gamma))
ax2.legend()

fig.tight_layout()
plt.show()
