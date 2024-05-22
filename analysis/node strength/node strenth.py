import networkx as nx
import matplotlib.pyplot as plt
import pickle
import numpy as np
from scipy.optimize import curve_fit

def calc_strength(G):
    # 计算每个节点的度和强度
    degrees = dict(G.degree())
    strengths = dict(G.degree(weight='weight'))

    # 将同一度值的节点的强度累加,并计数
    strength_degree = {}
    for node, degree in degrees.items():
        if degree not in strength_degree:
            strength_degree[degree] = []
        strength_degree[degree].append(strengths[node])

    # 对于每一度值,计算平均强度
    avg_strength_degree = {}
    for degree, strengths in strength_degree.items():
        avg_strength_degree[degree] = sum(strengths) / len(strengths)

    return avg_strength_degree

# 读取已构建好的网络
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# 计算网络的强度与度的关系
strength_degree_ccn = calc_strength(G_ccn)
strength_degree_csn = calc_strength(G_csn)

# 定义幂律拟合函数
def powerlaw(x, a, b):
    return a * (x**b)

# 对CCN进行拟合
ccn_degrees, ccn_avg_strengths = zip(*[(d, s) for d, s in strength_degree_ccn.items() if d > 0])
ccn_popt, _ = curve_fit(powerlaw, ccn_degrees, ccn_avg_strengths)

# 对CSN进行拟合
csn_degrees, csn_avg_strengths = zip(*[(d, s) for d, s in strength_degree_csn.items() if d > 0])
csn_popt, _ = curve_fit(powerlaw, csn_degrees, csn_avg_strengths)

# 绘制双对数坐标图
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