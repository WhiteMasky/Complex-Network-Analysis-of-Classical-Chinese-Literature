import networkx as nx
import matplotlib.pyplot as plt
import pickle
import random
from collections import defaultdict
import numpy as np

def calc_knn(G, sample_nodes):
    # 计算样本节点的最近邻平均度
    knn_k = defaultdict(list)
    for node in sample_nodes:
        neighbors = list(G.neighbors(node))
        if len(neighbors) > 0:  # 确保节点至少有一个邻居
            avg_degree = sum(G.degree(n) for n in neighbors) / len(neighbors)
            knn_k[G.degree(node)].append(avg_degree)

    # 对于每一度值,计算平均最近邻度
    for degree, knn_values in knn_k.items():
        knn_k[degree] = sum(knn_values) / len(knn_values)

    return knn_k

# 读取已构建好的网络
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# 从网络中随机抽取节点
def sample_graph(G, sample_size):
    return random.sample(G.nodes(), sample_size)

# 对网络进行抽样
sample_size = 50000  # 抽取节点数量,可以根据需要调整
sample_nodes_ccn = sample_graph(G_ccn, sample_size)
sample_nodes_csn = sample_graph(G_csn, sample_size)

# 计算样本的最近邻平均度与度的关系
knn_k_ccn = calc_knn(G_ccn, sample_nodes_ccn)
knn_k_csn = calc_knn(G_csn, sample_nodes_csn)

# 计算皮尔逊相关系数
def calc_pearson_correlation(knn_k):
    degrees, knn_values = zip(*[(k, v) for k, v in knn_k.items()])
    return np.corrcoef(degrees, knn_values)[0, 1]

r_ccn = calc_pearson_correlation(knn_k_ccn)
r_csn = calc_pearson_correlation(knn_k_csn)

# 绘制双对数坐标图并添加拟合线
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.loglog(list(knn_k_ccn.keys()), list(knn_k_ccn.values()), 'bo', markersize=4, label='Data')
ax1.set_title(f'CCN Average Nearest Neighbor Degree vs. Degree\nPearson correlation: {r_ccn:.4f}')
ax1.set_xlabel('Degree $k$')
ax1.set_ylabel('Average Nearest Neighbor Degree $k_{nn}(k)$')

# 添加拟合线
x_ccn = np.log10(list(knn_k_ccn.keys()))
y_ccn = np.log10(list(knn_k_ccn.values()))
coeffs_ccn = np.polyfit(x_ccn, y_ccn, 1)
ax1.loglog(10**x_ccn, 10**(coeffs_ccn[0]*x_ccn + coeffs_ccn[1]), 'r-', label='Fit')
ax1.legend()

ax2.loglog(list(knn_k_csn.keys()), list(knn_k_csn.values()), 'go', markersize=4, label='Data')
ax2.set_title(f'CSN Average Nearest Neighbor Degree vs. Degree\nPearson correlation: {r_csn:.4f}')
ax2.set_xlabel('Degree $k$')
ax2.set_ylabel('Average Nearest Neighbor Degree $k_{nn}(k)$')

# 添加拟合线
x_csn = np.log10(list(knn_k_csn.keys()))
y_csn = np.log10(list(knn_k_csn.values()))
coeffs_csn = np.polyfit(x_csn, y_csn, 1)
ax2.loglog(10**x_csn, 10**(coeffs_csn[0]*x_csn + coeffs_csn[1]), 'r-', label='Fit')
ax2.legend()

fig.tight_layout()
plt.show()