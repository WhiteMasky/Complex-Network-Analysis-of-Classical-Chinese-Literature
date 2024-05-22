import networkx as nx
import matplotlib.pyplot as plt
import pickle
import random
import seaborn as sns
import numpy as np

def calc_avg_shortest_path_length(G, sample_size):
    # 随机抽取节点对
    node_pairs = random.sample(list(G.nodes()), sample_size)

    # 计算最短路径长度
    shortest_path_lengths = []
    for source, target in zip(node_pairs[::2], node_pairs[1::2]):
        try:
            shortest_path_lengths.append(nx.shortest_path_length(G, source, target))
        except nx.NetworkXNoPath:
            pass  # 如果两个节点之间没有路径,则跳过

    # 计算平均最短路径长度
    avg_shortest_path_length = sum(shortest_path_lengths) / len(shortest_path_lengths)

    return avg_shortest_path_length, shortest_path_lengths

# 读取已构建好的网络
with open('../construction/ccn.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('../construction/csn.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# 计算平均最短路径长度和最短路径长度分布
sample_size = 50000  # 抽取的节点对数量,可以根据需要调整
avg_spl_ccn, spl_dist_ccn = calc_avg_shortest_path_length(G_ccn, sample_size)
avg_spl_csn, spl_dist_csn = calc_avg_shortest_path_length(G_csn, sample_size)

# 绘制最短路径长度分布图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# CCN图
sns.kdeplot(spl_dist_ccn, ax=ax1, color='b', fill=True)
ax1.axvline(avg_spl_ccn, color='r', linestyle='--', linewidth=2, label=f'Average: {avg_spl_ccn:.2f}')
ax1.set_title('CCN Shortest Path Length Distribution')
ax1.set_xlabel('Shortest Path Length')
ax1.set_ylabel('Density')
ax1.legend(loc='upper left')

# 创建右侧 y 轴
ax1_right = ax1.twinx()
counts_ccn, bins_ccn = np.histogram(spl_dist_ccn, bins=range(1, max(spl_dist_ccn)+2), density=True)
bins_ccn = 0.5 * (bins_ccn[:-1] + bins_ccn[1:])
ax1_right.plot(bins_ccn, counts_ccn, 'bs-', label='Probability')
ax1_right.set_ylabel('Probability')
ax1_right.legend(loc='lower right')  # 图例位置设置为右下角

# CSN图
sns.kdeplot(spl_dist_csn, ax=ax2, color='g', fill=True)
ax2.axvline(avg_spl_csn, color='r', linestyle='--', linewidth=2, label=f'Average: {avg_spl_csn:.2f}')
ax2.set_title('CSN Shortest Path Length Distribution')
ax2.set_xlabel('Shortest Path Length')
ax2.set_ylabel('Density')
ax2.legend(loc='upper left')

# 创建右侧 y 轴
ax2_right = ax2.twinx()
counts_csn, bins_csn = np.histogram(spl_dist_csn, bins=range(1, max(spl_dist_csn)+2), density=True)
bins_csn = 0.5 * (bins_csn[:-1] + bins_csn[1:])
ax2_right.plot(bins_csn, counts_csn, 'gs-', label='Probability')
ax2_right.set_ylabel('Probability')
ax2_right.legend(loc='lower right')  # 图例位置设置为右下角

fig.tight_layout()
plt.show()
