import pickle
import networkx as nx
import random

# 读取已构建好的网络
with open('ccnRandom.gpickle', 'rb') as f:
    G_ccn = pickle.load(f)
with open('csnRandom.gpickle', 'rb') as f:
    G_csn = pickle.load(f)

# 设置抽样比例和抽样次数
sampling_ratio = 0.01
num_samples = 100

# 对CCN网络进行抽样并计算聚类系数
clustering_coefs_ccn = []
for _ in range(num_samples):
    sampled_nodes_ccn = random.sample(G_ccn.nodes(), int(len(G_ccn.nodes()) * sampling_ratio))
    sampled_G_ccn = G_ccn.subgraph(sampled_nodes_ccn)
    clustering_coefs_ccn.append(nx.average_clustering(sampled_G_ccn))
avg_clustering_coef_ccn = sum(clustering_coefs_ccn) / num_samples

print(f"CCNRandom网络的平均聚类系数: {avg_clustering_coef_ccn}")

# 对CSN网络进行抽样并计算聚类系数
clustering_coefs_csn = []
for _ in range(num_samples):
    sampled_nodes_csn = random.sample(G_csn.nodes(), int(len(G_csn.nodes()) * sampling_ratio))
    sampled_G_csn = G_csn.subgraph(sampled_nodes_csn)
    clustering_coefs_csn.append(nx.average_clustering(sampled_G_csn))
avg_clustering_coef_csn = sum(clustering_coefs_csn) / num_samples

print(f"CSNRandom网络的平均聚类系数: {avg_clustering_coef_csn}")