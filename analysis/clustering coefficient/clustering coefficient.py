import networkx as nx
import matplotlib.pyplot as plt
import pickle
import random
from collections import defaultdict
from scipy.optimize import curve_fit

def calc_c_k(G):
    # 计算每个节点的度和聚类系数
    degrees = dict(G.degree())
    clustering_coeffs = nx.clustering(G)

    # 将同一度值的节点的聚类系数累加,并计数
    c_k = defaultdict(list)
    for node, degree in degrees.items():
        c_k[degree].append(clustering_coeffs[node])

    # 对于每一度值,计算平均聚类系数
    for degree, coeffs in c_k.items():
        c_k[degree] = sum(coeffs) / len(coeffs)

    return c_k

# 读取已构建好的网络
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# 从网络中随机抽取节点
def sample_graph(G, sample_size):
    sampled_nodes = random.sample(G.nodes(), sample_size)
    sampled_graph = G.subgraph(sampled_nodes)
    return sampled_graph

# 对网络进行采样
sample_size = 10000  # 抽取节点数量,可以根据需要调整
sampled_ccn = sample_graph(G_ccn, sample_size)
sampled_csn = sample_graph(G_csn, sample_size)

# 计算采样网络的聚类系数与度的关系
c_k_ccn = calc_c_k(sampled_ccn)
c_k_csn = calc_c_k(sampled_csn)

# 定义幂律拟合函数
def powerlaw(x, a, b):
    return a * (x**b)

# 对CCN进行拟合,去除度k<10的数据点
ccn_degrees, ccn_avg_ccs = zip(*[(k, v) for k, v in c_k_ccn.items() if k >= 10])
ccn_popt, _ = curve_fit(powerlaw, ccn_degrees, ccn_avg_ccs)

# 对CSN进行拟合,去除度k<10的数据点
csn_degrees, csn_avg_ccs = zip(*[(k, v) for k, v in c_k_csn.items() if k >= 10])
csn_popt, _ = curve_fit(powerlaw, csn_degrees, csn_avg_ccs)

# 绘制双对数坐标图
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